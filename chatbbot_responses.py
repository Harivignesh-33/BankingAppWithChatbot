import sqlite3


def create_chatbot_responses_table():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # Create chatbot_responses table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    ''')

    # List of predefined questions and answers
    qa_pairs = [
        ("what is my balance?", "SELECT amt FROM cusdetails WHERE acno = ?"),
        ("show my transactions", "SELECT tt, amt, dat FROM trans WHERE acno = ? ORDER BY dat DESC"),
        ("who is the bank manager?", "The bank manager is Mr. John Doe."),
        ("what are your working hours?", "Our working hours are Monday to Friday, 9 AM to 5 PM."),
        ("how can I reset my password?",
         "You can reset your password by visiting the nearest branch or calling customer support."),
        (
        "can I open a new account online?", "Yes, you can open a new account online by visiting our official website."),
        ("what is the interest rate on savings accounts?", "Our savings account interest rate is 3.5% per annum."),
        ("how do I transfer money?",
         "You can transfer money using our mobile banking app or by visiting the nearest branch."),
        ("is online banking secure?", "Yes, we use the latest encryption technology to secure all transactions."),
        ("how do I apply for a loan?", "You can apply for a loan online or visit our branch for assistance."),
    ]

    # Insert questions and answers into the database
    for question, answer in qa_pairs:
        try:
            cursor.execute("INSERT INTO chatbot_responses (question, answer) VALUES (?, ?)", (question, answer))
        except sqlite3.IntegrityError:
            pass  # Ignore duplicate entries

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_chatbot_responses_table()
    print("Chatbot responses table created and populated successfully!")
