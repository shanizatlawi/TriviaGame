import numpy as np
import matplotlib.pyplot as plt
import psycopg2

try:
    # Establish the connection and cursor using the `with` statement
    with psycopg2.connect(
        dbname="trivia game",   # Database name
        user="postgres",        # Username (make sure it's correct)
        password="admin",       # Password (make sure it's correct)
        host="localhost",       # Hostname or IP address of the PostgreSQL server
        port="5432"             # Port number (default is 5432)
    ) as conn:
        with conn.cursor() as cur:

            def player_pie():
                print('Enter name to show player statistics charts.')
                player = input('Enter name: ')
                cur.execute('''SELECT player_id 
                               FROM players 
                               WHERE username = %s''', (player,))
                result = cur.fetchone()

                if result is None:
                    print('Username not registered. Please try again.')
                    return main()

                id_player = result[0]

                cur.execute('''SELECT COUNT(*) AS correct 
                               FROM player_answers 
                               WHERE player_id = %s AND is_correct = TRUE''',
                            (id_player,))
                correct = cur.fetchone()[0]

                cur.execute('''SELECT COUNT(*) AS wrong 
                               FROM player_answers 
                               WHERE player_id = %s AND is_correct = FALSE''',
                            (id_player,))
                wrong = cur.fetchone()[0]

                not_answered = 20 - (correct + wrong)

                labels = ['Correct', 'Wrong', 'Not Answered']
                slices = [correct, wrong, not_answered]
                colors = ['green', 'red', 'blue']
                explode = (0.1, 0, 0)

                plt.pie(slices, labels=labels, colors=colors, explode=explode)
                plt.title(f"{player}'s Answers Distribution")
                plt.show()


            def question_graph():
                print('Showing question statistics charts.')

                # Correct answers
                cur.execute('''SELECT question_id, COUNT(*) AS correct_count
                            FROM player_answers
                            WHERE is_correct = TRUE
                            GROUP BY question_id
                            ORDER BY question_id''')
                correct_array = np.array(cur.fetchall())

                # Incorrect answers
                cur.execute('''SELECT question_id, COUNT(*) AS false_count
                            FROM player_answers
                            WHERE is_correct = FALSE
                            GROUP BY question_id
                            ORDER BY question_id''')
                false_array = np.array(cur.fetchall())

                # Total players who answered
                cur.execute('''SELECT question_id, COUNT(*) AS total_answers
                            FROM player_answers
                            GROUP BY question_id
                            ORDER BY question_id''')
                total_array = np.array(cur.fetchall())

                # Total players (for unanswered calculation)
                cur.execute('''SELECT COUNT(*) AS players FROM players''')
                players_count = cur.fetchone()[0]  # Ensure players_count is defined

                # Get all questions
                cur.execute('''SELECT question_id FROM questions ORDER BY question_id''')
                all_questions = np.array(cur.fetchall())[:, 0]

                # Initialize counts
                correct_counts = np.zeros(len(all_questions))
                incorrect_counts = np.zeros(len(all_questions))
                unanswered_counts = np.zeros(len(all_questions))

                # Fill counts for each question
                for i, question_id in enumerate(all_questions):
                    if question_id in correct_array[:, 0]:
                        correct_counts[i] = correct_array[correct_array[:, 0] == question_id, 1].item()
                    if question_id in false_array[:, 0]:
                        incorrect_counts[i] = false_array[false_array[:, 0] == question_id, 1].item()
                    if question_id in total_array[:, 0]:
                        total_answers = total_array[total_array[:, 0] == question_id, 1].item()
                        unanswered_counts[i] = players_count - total_answers

                # Plotting
                x = np.arange(len(all_questions))  # Positions for each question
                bar_width = 0.25

                fig, ax = plt.subplots(figsize=(10, 6))

                ax.bar(x - bar_width, correct_counts, width=bar_width, label='Correct', color='green')
                ax.bar(x, incorrect_counts, width=bar_width, label='Incorrect', color='red')
                ax.bar(x + bar_width, unanswered_counts, width=bar_width, label='Unanswered', color='gray')

                # Add labels and title
                ax.set_xlabel('Question ID')
                ax.set_ylabel('Number of Answers')
                ax.set_title('Question Statistics')
                ax.set_xticks(x)
                ax.set_xticklabels(all_questions)
                ax.legend()

                # Show plot
                plt.tight_layout()
                plt.show()


            def main():
                while True:
                    print("a. show player's statistics chart")
                    print("b. show questions' statistics chart")
                    print('c. Exit')
                    choice = input('Enter a, b or c: ').strip().lower()
                    if choice == 'a':
                        player_pie()
                    elif choice == 'b':
                        question_graph()
                    elif choice == 'c':
                        print('Goodbye!')
                        break

            # Start the main function inside the 'with' block
            main()

except psycopg2.Error as e:
    print("Database error:", e)
