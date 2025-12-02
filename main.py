import sqlite3
import bcrypt
from typing import Optional

# Import from config.py
from config import DB_PATH

# ----------------------------
# Password Hashing & 
def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

# ----------------------------
# Verification

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# ----------------------------
# Database Functions

def _load_users() -> dict:
    """Load all users from the database into a dictionary."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password_hash FROM users")
    users = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return users

# ----------------------------
# Database Initialization

def create_users_table():
    """Create the users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

# ----------------------------
# User Operations

def register_user():
    """Register a new user."""
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return

    hashed = hash_password(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()

# ----------------------------
# Login Function

def login_user(user_name: str, password: str) -> bool:
    """Login a user by verifying their credentials."""
    users = _load_users()
    stored_hash: Optional[str] = users.get(user_name)

    if stored_hash is None:
        print("User not found.")
        return False

    if verify_password(password, stored_hash):
        print("Login successful.")
        return True
    else:
        print("Invalid password.")
        return False

# ----------------------------
# Main Loop

def main():
    create_users_table()

    while True:
        print("\n=== USER AUTH SYSTEM ===")
        print("1) Register")
        print("2) Login")
        print("3) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ")
            login_user(username, password)
        elif choice == "3":
            print("bye bye :3")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()