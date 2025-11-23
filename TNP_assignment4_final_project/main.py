import quiz as qz
import question_bank as qb
import mysql.connector
from mysql.connector import Error

# --- CONFIGURATION ---
# TODO: Update 'password' with your actual MySQL root password
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql@123',
    'database': 'tnp_portal'
}

# Global state variables
logged_user = ""
is_logged = False


def get_db_connection():
    """Establishes connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def register():
    print("\n______Register new user__________")
    new_username = input("Enter your username: ").strip()

    conn = get_db_connection()
    if not conn: return

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT username FROM users WHERE username = %s", (new_username,))
        if cursor.fetchone():
            print("Username already registered")
        else:
            name = input("Enter your full name: ")
            password = input("Enter your password: ").strip()
            email = input("Enter your email address: ").strip()

            query = "INSERT INTO users (username, full_name, email, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (new_username, name, email, password))
            conn.commit()
            print(f"Registration successful for {new_username}!")

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    main()


def login():
    global logged_user, is_logged
    print("\n______Login__________")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_row = cursor.fetchone()

        if user_row:
            if str(user_row['password']) == password:
                logged_user = username
                is_logged = True
                print("Login successful!")
            else:
                print("Incorrect password")
        else:
            print("Username not found")

    except Error as e:
        print(f"Login Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    main()


def show_profile():
    if is_logged:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (logged_user,))
            user_row = cursor.fetchone()

            if user_row:
                print("\n--- User Profile ---")
                print(f"Username: {user_row['username']}")
                print(f"Name:     {user_row['full_name']}")
                print(f"Email:    {user_row['email']}")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        print("You must be logged in to show profile")
    main()


def update_profile():
    if is_logged:
        print("\n--- Update Profile ---")
        new_name = input("Enter new full name (or press Enter to skip): ")
        new_email = input("Enter new email (or press Enter to skip): ")
        new_password = input("Enter new password (or press Enter to skip): ")

        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        try:
            updates = 0
            if new_name:
                cursor.execute("UPDATE users SET full_name = %s WHERE username = %s", (new_name, logged_user))
                updates += 1
            if new_email:
                cursor.execute("UPDATE users SET email = %s WHERE username = %s", (new_email, logged_user))
                updates += 1
            if new_password:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, logged_user))
                updates += 1

            if updates > 0:
                conn.commit()
                print(f"Success! {updates} field(s) updated.")
            else:
                print("No changes made.")

        except Error as e:
            print(f"Update failed: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        print("You must be logged in to update profile")
    main()


def attempt_quiz():
    if is_logged:
        choice = input("""
        --- Select Quiz Topic ---
        1: PYTHON
        2: DBMS
        3: DSA
        Enter choice (1/2/3): """).strip()

        topic_name = ""
        final_score = 0

        if choice == '1':
            topic_name = "Python"
            final_score = qz.start_quiz(qb.python_quiz)
        elif choice == '2':
            topic_name = "DBMS"
            final_score = qz.start_quiz(qb.dbms_quiz)
        elif choice == '3':
            topic_name = "DSA"
            final_score = qz.start_quiz(qb.dsa_quiz)
        else:
            print("Invalid choice.")
            return

        # Save score to DB
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO quiz_results (username, topic, score) VALUES (%s, %s, %s)"
                cursor.execute(query, (logged_user, topic_name, final_score))
                conn.commit()
                print(f"\n[Database] Your score for {topic_name} has been saved!")
            except Error as e:
                print(f"Error saving score: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    else:
        print("Please login to attempt the quiz.")
    main()


def logout():
    global logged_user, is_logged
    if is_logged:
        print(f"Goodbye, {logged_user}! Logging out...")
        logged_user = ""
        is_logged = False
    else:
        print("You are not logged in.")
    main()


def terminate():
    print("Exiting application...")
    exit()


def main():
    while True:
        print('\n.....Welcome to LNCT Portal....')
        if is_logged:
            print(f"User: {logged_user}")

        response = input("""Choose option:
1. Registration
2. Login
3. Profile
4. Update profile
5. Logout
6. Attempt Quiz
7. Exit

Select option: """).strip()

        if response == '1':
            register()
        elif response == '2':
            login()
        elif response == '3':
            show_profile()
        elif response == '4':
            update_profile()
        elif response == '5':
            logout()
        elif response == '6':
            attempt_quiz()
        elif response == '7':
            terminate()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()