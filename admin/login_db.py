import sqlite3
import hashlib

def hash_password(password):
    # Hash the password if it's numeric
    if password.isdigit():
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed
    return password  # Leave as-is if not numeric

def create_database():
    conn = sqlite3.connect('ProductRegistration.db')
    cursor = conn.cursor()

    # Create admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_admin(username, password):
    hashed_pw = hash_password(password)

    conn = sqlite3.connect('ProductRegistration.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        print(f"Admin '{username}' added.")
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    finally:
        conn.close()

def delete_table():
    # Connect to the database
    conn = sqlite3.connect('ProductRegistration.db')
    cursor = conn.cursor()

    # Delete the table if it exists
    try:
        cursor.execute("DROP TABLE IF EXISTS admin;")
        conn.commit()
        print("Table 'admin' deleted successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e)

    # Close the connection
    conn.close()

# Example usage
if __name__ == '__main__':
    create_database()
    