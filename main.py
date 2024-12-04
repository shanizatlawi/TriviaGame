
import psycopg2

try:
    # Establish the connection and cursor using the `with` statement
    with psycopg2.connect(
        dbname="trivia game",   # Database name
        user="postgres",        # Username (make sure it's correct)
        password="admin",    # Password (make sure it's correct)
        host="localhost",    # Hostname or IP address of the PostgreSQL server
        port="5432"          # Port number (default is 5432)
    ) as conn:
     with conn.cursor() as cur:


        def show_login_menu():
            print("Welcome to the Trivia Game!")
            print("1. Register a new player")
            print("2. Log in with an existing player")
            print("3. show statistics")
            print("4. quit")


        def start_or_continue(player_id):
            while True:
                print("Do you want to continue your game?")
                print("a: Yes")
                print("b: No")
                choice = input("Enter a or b: ").strip().lower()

                if choice == "a":
                    print("Let's play")
                    return continue_game(player_id)
                elif choice == "b":
                    print("Do you want to start a new game?")
                    print("a: Yes")
                    print("b: No")
                    choice_2 = input("Enter a or b: ").strip().lower()

                    if choice_2 == "a":
                        print("Start the game!")
                        return restart_game(player_id)
                    elif choice_2 == "b":
                        print("Returning to the main menu.")
                        return main()
                    else:
                        print("Invalid input. Please enter 'a' or 'b'.")
                else:
                    print("Invalid input. Please enter 'a' or 'b'.")


        def register_player():
            username = input("Enter username: ")
            cur.execute("SELECT COUNT(*) FROM players WHERE username = %s", (username,))
            count = cur.fetchone()[0]
            if count > 0:
                print("Username already exists.")
                return register_player()
            else:
                password = input("Enter password: ")
                repeat_pw = input("Enter password again: ")
                if password != repeat_pw:
                    print("Passwords don't match. Please try again.")
                    return register_player()
                else:
                    email = input("Enter email: ")
                    cur.execute("SELECT COUNT(*) FROM players WHERE email = %s", (email,))
                    count = cur.fetchone()[0]
                    if count > 0:
                        print("Email already exists.")
                        return register_player()
                    try:
                        age = int(input("Enter age: "))
                    except ValueError:
                        print("Invalid age. Please enter a number.")
                        return register_player()  # Restart registration on invalid input

                try:
                    cur.execute(
                        '''INSERT INTO players (username, password, email, age) 
                        VALUES (%s, %s, %s, %s) RETURNING player_id;''',
                        (username, password, email, age))
                    player_id = cur.fetchone()[0]  # Retrieve the generated player_id
                    conn.commit()
                    print(f"Player registered successfully with ID: {player_id}")
                    start_or_continue(player_id)  # Proceed to the game options
                except psycopg2.Error as e:
                    print("Error occurred during registration:", e)


        def login_player():
            attempts = 0
            max_attempts = 2

            while attempts < max_attempts:
                username = input("Enter username: ")
                password = input("Enter password: ")

                try:
                    cur.execute(
                        "SELECT player_id FROM players WHERE username = %s AND password = %s",
                        (username, password)
                    )
                    result = cur.fetchone()

                    if result:
                        player_id = result[0]
                        print("Login successful!")
                        return player_id
                    else:
                        print("Invalid username or password.")
                        attempts += 1

                        if attempts == max_attempts:
                            print("Access denied, please register!")
                            return register_player()  # Proceed to registration after max attempts

                except psycopg2.Error as e:
                    print("Error occurred during login:", e)
                    return None  # Handle database errors and exit gracefully


        def ask_questions(player_id, questions):
            for question in questions:
                print(f"Question-id: {question[0]}")  # Question ID
                print(f"Question: {question[1]}")  # Question text
                print(f"a: {question[2]}")  # Answer A
                print(f"b: {question[3]}")  # Answer B
                print(f"c: {question[4]}")  # Answer C
                print(f"d: {question[5]}")  # Answer D


                while True:
                    player_answer = input("Enter your answer (a, b, c, or d): ").strip().lower()
                    # Ensure the player enters a valid choice
                    if player_answer in ['a', 'b', 'c', 'd']:
                        break  # Exit the loop if the answer is valid
                    else:
                        print("Invalid answer. Please enter 'a', 'b', 'c', or 'd'.")
                # Verify and save the player's answer
                correct_answer = question[6]  # Assuming question[6] is the correct answer
                is_correct = player_answer == correct_answer

                print(f"Player Answer: {player_answer}")  # Debugging: Check the value of player_answer
                print(f"Correct Answer: {correct_answer}")  # Debugging: Check the correct answer

                try:
                    # Save the player's answer to the database
                    cur.execute(
                        '''
                        INSERT INTO player_answers (player_id, question_id, selected_answer, is_correct)
                        VALUES (%s, %s, %s, %s)
                        ''',
                        (player_id, question[0],player_answer, is_correct)
                    )
                    print("Answer inserted successfully!")


                    # Update the `questions_solved` column in the `players` table
                    cur.execute(
                        '''
                        UPDATE players
                        SET questions_solved = questions_solved + 1
                        WHERE player_id = %s
                        ''',
                        (player_id,)
                    )

                    # Commit the changes
                    conn.commit()

                    # Feedback for the player
                    if is_correct:
                        print("Correct!")
                    else:
                        print(f"Wrong! The correct answer was {correct_answer}.")

                    # Prompt to continue or exit
                    while True:
                        print("Would you like to continue or exit?")
                        print("a: Exit")
                        print("b: Continue")
                        choice = input("Enter 'a' to exit or 'b' to continue: ").strip().lower()

                        if choice == 'a':
                            print("Goodbye!")
                            return  # Exit the function, no further questions will be asked
                        elif choice == 'b':
                            break  # Exit the inner loop and move to the next question
                        else:
                            print("Invalid choice. Please try again.")

                except psycopg2.Error as e:
                    print("Error saving answer or updating progress:", e)
                    conn.rollback()  # Roll back the transaction in case of an error

                # Continue feedback after the loop
                if is_correct:
                    update_achievement(player_id)  # Assuming this is a function you've implemented
                else:
                    print(f"Wrong! The correct answer was {correct_answer}.")


        def update_achievement(player_id):
            try:
                cur.execute("UPDATE high_scores SET score_id = score_id + 1, achieved_at = NOW() WHERE player_id = %s",
                            (player_id,))
                conn.commit()
            except psycopg2.Error as e:
                print("Error updating achievement:", e)


        def continue_game(player_id):
            try:
                cur.execute(
                    "SELECT MAX(question_id) FROM player_answers WHERE player_id = %s",
                    (player_id,)
                )
                last_question_id = cur.fetchone()[0] or 0
                cur.execute(
                    '''SELECT question_id, question_text, answer_a, answer_b, answer_c, answer_d, correct_answer
                    FROM questions WHERE question_id > %s ORDER BY question_id''',
                    (last_question_id,)
                )
                questions = cur.fetchall()
                if questions:
                    ask_questions(player_id, questions)
                else:
                    print("No more questions left to answer!")
            except psycopg2.Error as e:
                print("Error continuing game:", e)

        players_restarted = []

        def restart_game(player_id):
            try:
                if player_id not in players_restarted:
                    players_restarted.append(player_id)

                cur.execute("DELETE FROM player_answers WHERE player_id = %s", (player_id,))
                conn.commit()
                cur.execute("SELECT * FROM questions ORDER BY question_id")
                questions = cur.fetchall()
                ask_questions(player_id, questions)
            except psycopg2.Error as e:
                print("Error restarting game:", e)

        def count_players_answered():
            cur.execute('''SELECT
                            COUNT(*)
                            AS
                            players_answered
                            FROM
                            players
                            WHERE
                            questions_solved > 0;''')

            players_answered = cur.fetchone()[0]
            restarted_players_num = len(players_restarted)
            total_players = players_answered + restarted_players_num
            print(f"Number of players who have played so far: {total_players}")

        def show_active_players():
            cur.execute('''SELECT player_id FROM players WHERE questions_solved > 0''')
            active_players = cur.fetchall()
            print(active_players)

        def show_most_answered_correct():
            cur.execute('''SELECT question_id 
                        FROM player_answers
                        WHERE is_correct = TRUE
                    ''')
            count_lst = [row[0] for row in cur.fetchall()]

            if not count_lst:
                print("No questions have been answered correctly yet.")
                return []

            # Create a dictionary to count occurrences
            question_count = {}
            for question_id in count_lst:
                question_count[question_id] = question_count.get(question_id, 0) + 1

            max_answered = max(question_count.values())
            most_answered_questions = [question_id for question_id, count in question_count.items() if count == max_answered]

            return most_answered_questions


        def show_most_answered_incorrect():
            cur.execute('''SELECT question_id 
                             FROM player_answers
                             WHERE is_correct = FALSE
                         ''')
            count_lst = [row[0] for row in cur.fetchall()]

            if not count_lst:
                print("No questions have been answered incorrectly yet.")
                return []

            # Create a dictionary to count occurrences
            question_count = {}
            for question_id in count_lst:
                question_count[question_id] = question_count.get(question_id, 0) + 1

            max_answered = max(question_count.values())
            most_answered_questions = [question_id for question_id, count in question_count.items() if
                                       count == max_answered]

            return most_answered_questions


        def show_top_players():
            try:
                # Step 1: Get top player IDs from high_scores
                cur.execute(

                    '''
                    SELECT player_id 
                    FROM high_scores 
                    ORDER BY score_id DESC, achieved_at ASC 
                    LIMIT 10
                    '''
                )
                id_list = [row[0] for row in cur.fetchall()]  # Extract player IDs

                if not id_list:
                    print("No high scores available.")
                    return

                # Step 2: Fetch usernames for the retrieved player IDs
                cur.execute(
                    '''
                    SELECT username 
                    FROM players 
                    WHERE player_id = ANY(%s)
                    ORDER BY player_id
                    ''',
                    (id_list,)
                )
                name_list = [row[0] for row in cur.fetchall()]  # Extract usernames

                # Step 3: Display usernames
                print("Top Players:")
                for rank, name in enumerate(name_list, 1):
                    print(f"{rank}. {name}")

            except psycopg2.Error as e:
                print("Error fetching top players:", e)


        def show_expert_players():
            cur.execute(
                '''
                SELECT username 
                FROM players 
                ORDER BY questions_solved DESC
                LIMIT 10
                '''
            )
            expert_list = [row[0] for row in cur.fetchall()]  # Extract usernames from results
            return expert_list  # Return the list instead of printing it


        def show_player_answers_info():
            print('Enter player_id')
            check_player = input('Enter player_id: ')

            # Get the question IDs for the player
            cur.execute('''SELECT question_id FROM player_answers WHERE player_id = %s''', (check_player,))
            question_lst = [row[0] for row in cur.fetchall()]

            # Prepare the dictionary to store player's answers info
            players_answers_info = {}

            # Iterate through the questions and get answers
            for q in question_lst:
                # Get the question text
                cur.execute('''SELECT question_text FROM questions WHERE question_id = %s''', (q,))
                question_text_lst = [row[0] for row in cur.fetchall()]

                # Get whether the player's answer was correct
                cur.execute('''SELECT is_correct FROM player_answers WHERE question_id = %s AND player_id = %s''',
                            (q, check_player))
                answers_check_lst = [row[0] for row in cur.fetchall()]

                # Zip the question texts and answer statuses together
                for question_text, is_correct in zip(question_text_lst, answers_check_lst):
                    players_answers_info[question_text] = is_correct

            # Print the player's answers information
            if players_answers_info:
                print(f"Player {check_player}'s answer info:")
                for question, is_correct in players_answers_info.items():
                    print(f"Question: {question} - Answer is: {is_correct}")
            else:
                print(f"No answers found for player {check_player}.")


        def show_question_info():
            # Get the list of all questions
            cur.execute('''SELECT question_id, question_text FROM questions ORDER BY question_id''')
            questions = cur.fetchall()

            question_info_list = []

            for question_id, question_text in questions:
                # Get the count of players who answered this question
                cur.execute('''
                        SELECT COUNT(player_id) AS players_answered
                        FROM player_answers
                        WHERE question_id = %s
                    ''', (question_id,))
                players_answered = cur.fetchone()[0]

                # Get the count of correct answers for this question
                cur.execute('''
                        SELECT COUNT(*) AS players_right
                        FROM player_answers
                        WHERE question_id = %s AND is_correct = TRUE
                    ''', (question_id,))
                players_right = cur.fetchone()[0]

                # Get the count of incorrect answers for this question
                cur.execute('''
                        SELECT COUNT(*) AS players_wrong
                        FROM player_answers
                        WHERE question_id = %s AND is_correct = FALSE
                    ''', (question_id,))
                players_wrong = cur.fetchone()[0]

                # Store the information for this question
                question_info_list.append({
                    "question_id": question_id,
                    "question_text": question_text,
                    "players_answered": players_answered,
                    "players_right": players_right,
                    "players_wrong": players_wrong
                })

            # Display the information
            for info in question_info_list:
                print(f"Question ID: {info['question_id']}")
                print(f"Text: {info['question_text']}")
                print(f"Answered by: {info['players_answered']} players")
                print(f"Correct answers: {info['players_right']}")
                print(f"Incorrect answers: {info['players_wrong']}")
                print("-" * 40)


        def show_statistics():
            while True:
                print("Statistics Menu:")
                print("1. Number of players who have played")
                print("2. Active players")
                print("3. Most correctly answered question")
                print("4. Most incorrectly answered question")
                print("5. Top players")
                print("6. Expert players")
                print("7. Player's answers info")
                print("8. Questions statistics")
                print("9. Back to main menu")
                print('10 . player info  pie chart')

                choice = input("Enter your choice (1-9): ").strip()

                if choice == '1':
                    count_players_answered()
                elif choice == '2':
                    show_active_players()
                elif choice == '3':
                    print("Most answered correctly questions:",
                          show_most_answered_correct())
                elif choice == '4':
                    print("Most unanswered incorrectly questions:",
                          show_most_answered_incorrect())  # Logic needed for incorrect answers
                elif choice == '5':
                    show_top_players()
                elif choice == '6':
                    print("Expert Players:", show_expert_players())
                elif choice == '7':
                    show_player_answers_info()
                elif choice == '8':
                    show_question_info()
                elif choice == '9':
                    print("Returning to the main menu.")
                    return  # Exit statistics menu
                else:
                    print("Invalid choice. Please try again.")




        def main():
            while True:
                show_login_menu()
                choice = input("Enter your choice: ").strip()

                if choice == '1':
                    register_player()
                elif choice == '2':
                    player_id = login_player()
                    start_or_continue(player_id)
                elif choice == '3':
                    show_statistics()
                elif choice == '4':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

        main()


except psycopg2.Error as e:
    print("Database error:", e)
