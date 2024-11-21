import re
from getpass import getpass
users_file = "users.txt"
results_file = "results.txt"
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
    with open(users_file, "a") as file:
        file.write(f"{username},{password},{full_name},{age},{email},{phone}\n")
    print("Registration successful!")
def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    try:
        with open(users_file, "r") as file:
            for line in file:
                user_data = line.strip().split(',')
                if user_data[0] == username and user_data[1] == password:
                    print("Login successful!")
                    return True
        print("Login failed. Please check your username and password.")
        return False
    except FileNotFoundError:
        print("User file not found. Please register first.")
        return False
def attempt_quiz():
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
    username = input("Enter your name for the result record: ")
    with open(results_file, "a") as file:
        file.write(f"{username},{subject},{score}/{len(quizzes[subject])}\n")
    print("Your result has been saved.")
def show_results():
    print("\n--- Results ---")
    try:
        with open(results_file, "r") as file:
            for line in file:
                username, subject, score = line.strip().split(',')
                print(f"Name: {username}, Subject: {subject}, Score: {score}")
    except FileNotFoundError:
        print("No results found.")
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
            if login():
                print("You are logged in!")
        elif op == '3':
            attempt_quiz()
        elif op == '4':
            show_results()
        elif op == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")
main()