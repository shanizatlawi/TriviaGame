import psycopg2

try:
    # Establish the connection and cursor using the `with` statement
    with psycopg2.connect(
        dbname="trivia game",  # Database name (ensure it's correct)
        user="postgres",       # Username
        password="admin",      # Password
        host="localhost",      # Host
        port="5432"            # Port
    ) as conn:
        with conn.cursor() as cur:
          cur.etable_query)

            # Insert data into the table
            insert_data_query = """
            INSERT INTO questions (question_text, answer_a, answer_b, answer_c, answer_d, correct_answer) VALUES
            ('What is the capital of France?', 'Berlin', 'Madrid', 'Paris', 'Rome', 'c'),
            ('What is the largest planet in our solar system?', 'Earth', 'Jupiter', 'Mars', 'Saturn', 'b'),
            ('Which element has the chemical symbol O?', 'Gold', 'Oxygen', 'Iron', 'Silver', 'b'),
            ('What is the smallest prime number?', '1', '2', '3', '5', 'b'),
            ('Who wrote "Hamlet"?', 'Charles Dickens', 'William Shakespeare', 'Mark Twain', 'Jane Austen', 'b'),
            ('What is the square root of 64?', '6', '7', '8', '9', 'c'),
            ('What is the chemical formula for water?', 'H2O', 'CO2', 'O2', 'NaCl', 'a'),
            ('Who painted the Mona Lisa?', 'Vincent van Gogh', 'Leonardo da Vinci', 'Pablo Picasso', 'Claude Monet', 'b'),
            ('What is the capital city of Japan?', 'Beijing', 'Seoul', 'Bangkok', 'Tokyo', 'd'),
            ('Which planet is known as the Red Planet?', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'c'),
            ('What is the freezing point of water in Celsius?', '0', '32', '100', '-273', 'a'),
            ('Who discovered gravity?', 'Isaac Newton', 'Albert Einstein', 'Galileo Galilei', 'Marie Curie', 'a'),
            ('What is the largest mammal in the world?', 'Elephant', 'Blue Whale', 'Giraffe', 'Polar Bear', 'b'),
            ('What is the capital city of Italy?', 'Venice', 'Milan', 'Rome', 'Florence', 'c'),
            ('What is 5 + 7?', '10', '11', '12', '13', 'c'),
            ('Which is the longest river in the world?', 'Amazon', 'Nile', 'Yangtze', 'Mississippi', 'b'),
            ('What is the name of the smallest country in the world?', 'Monaco', 'Vatican City', 'Liechtenstein', 'San Marino', 'b'),
            ('Which gas do plants primarily use for photosynthesis?', 'Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Helium', 'b'),
            ('Who is the author of "1984"?', 'GeorgeOrwell', 'Aldous Huxley', 'Ray Bradbury', 'J.K. Rowling', 'a'),
            ('What is the hardest natural substance on Earth?', 'Gold', 'Iron', 'Diamond', 'Platinum', 'c');
            """
            cur.execute(insert_data_query)

            # Commit changes to the database
            conn.commit()
            print("Table created and data inserted successfully!")

except Exception as e:
    print("An error occurred:", e)
