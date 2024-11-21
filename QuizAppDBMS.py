import re
import mysql.connector
from getpass import getpass
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "quiz_app"
}
quizzes = {
    "DSA": [
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n^2)"], "answer": "O(log n)"},
        {"question": "Which data structure is used in BFS?", "options": ["Stack", "Queue", "Tree"], "answer": "Queue"},
        {"question": "What is the worst-case time complexity of quicksort?", "options": ["O(n^2)", "O(n log n)", "O(n)"], "answer": "O(n^2)"},
        {"question": "Which of the following is not a linear data structure?", "options": ["Array", "Tree", "Linked List"], "answer": "Tree"},
        {"question": "Which data structure allows LIFO?", "options": ["Queue", "Stack", "Array"], "answer": "Stack"}
    ],
    "DBMS": [
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language"], "answer": "Structured Query Language"},
        {"question": "Which of these is not a type of database?", "options": ["Relational", "Distributed", "Tree"], "answer": "Tree"},
        {"question": "Which command is used to retrieve data?", "options": ["INSERT", "UPDATE", "SELECT"], "answer": "SELECT"},
        {"question": "Which key is used to uniquely identify rows?", "options": ["Foreign key", "Primary key", "Candidate key"], "answer": "Primary key"},
        {"question": "Which is a type of JOIN?", "options": ["FULL JOIN", "SEMI JOIN", "PARTIAL JOIN"], "answer": "FULL JOIN"}
    ],
    "Python": [
        {"question": "What is the output of '3 * 'abc'?", "options": ["'abcabcabc'", "'abc*3'", "Error"], "answer": "'abcabcabc'"},
        {"question": "Which of these is a mutable type?", "options": ["Tuple", "List", "String"], "answer": "List"},
        {"question": "Which function is used to convert a string to lowercase?", "options": ["lower()", "downcase()", "toLower()"], "answer": "lower()"},
        {"question": "Which of these is a loop structure?", "options": ["if", "for", "print"], "answer": "for"},
        {"question": "Which method is used to add an element to a list?", "options": ["add()", "append()", "insert()"], "answer": "append()"}
    ]
}

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit()

def register():
    print("Enter your details to register:")
    username = input("Username: ")
    password = getpass("Password: ")
    confirm_password = getpass("Confirm Password: ")
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return
    full_name = input("Full Name: ")
    age = input("Age: ")
    if not age.isdigit() or int(age) < 1:
        print("Invalid age. Please enter a valid number.")
        return
    email = input("Email: ")
    if not re.match(email_pattern, email):
        print("Invalid email format.")
        return
    phone = input("Phone Number: ")
    if not phone.isdigit() or len(phone) < 10:
        print("Invalid phone number. Please enter a 10-digit number.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, full_name, age, email, phone) VALUES (%s, %s, %s, %s, %s, %s)",
            (username, password, full_name, age, email, phone)
        )
        conn.commit()
        print("Registration successful!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        cursor.close()
        conn.close()
        return username
    else:
        print("Login failed. Please check your username and password.")
        cursor.close()
        conn.close()
        return None

def attempt_quiz(username):
    subject = input("Choose a subject: DSA, DBMS, Python: ").strip()
    if subject not in quizzes:
        print("Invalid subject choice.")
        return

    score = 0
    for q in quizzes[subject]:
        print("\n" + q["question"])
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        while True:
            try:
                answer = int(input("Enter the option number of your answer: ").strip())
                if 1 <= answer <= len(q["options"]):
                    break
                else:
                    print("Invalid option number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        if q["options"][answer - 1] == q["answer"]:
            score += 1

    print(f"\nYou scored {score} out of {len(quizzes[subject])}.")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO results (username, subject, score) VALUES (%s, %s, %s)",
        (username, subject, f"{score}/{len(quizzes[subject])}")
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Your result has been saved.")

def show_results():
    print("\n--- Results ---")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results")
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"Name: {row[1]}, Subject: {row[2]}, Score: {row[3]}")
    else:
        print("No results found.")
    cursor.close()
    conn.close()

def main():
    while True:
        op = input("""\nChoose an option: 
        1. Register
        2. Login
        3. Attempt Quiz
        4. Show Results
        5. Exit
        Enter your choice: """)
        if op == '1':
            register()
        elif op == '2':
            username = login()
            if username:
                print(f"Welcome, {username}!")
        elif op == '3':
            username = login()
            if username:
                attempt_quiz(username)
        elif op == '4':
            show_results()
        elif op == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

main()
