import psycopg2

try:
    print("Starting the database connection...")
    with psycopg2.connect(
        dbname="trivia game",   # Database name
        user="postgres",        # Username
        password="admin",       # Password
        host="localhost",       # Hostname
        port="5432"             # Port number
    ) as conn:
        print("Connection established successfully.")
        with conn.cursor() as cur:
            print("Cursor created successfully.")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    question_id SERIAL PRIMARY KEY,
                    question_text TEXT NOT NULL,
                    answer_a TEXT NOT NULL,
                    answer_b TEXT NOT NULL,
                    answer_c TEXT NOT NULL,
                    answer_d TEXT NOT NULL,
                    correct_answer CHAR(1) CHECK (correct_answer IN ('a', 'b', 'c', 'd')) NOT NULL
                );
            """)
            conn.commit()
            print("Table created successfully.")

            cur.execute('''  INSERT INTO questions (question_text, answer_a, answer_b, answer_c, answer_d, correct_answer) VALUES
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
            
            %''')
except Exception as e:
    print(f"Error: {e}")
