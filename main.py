# main.py - Authentication functions only

import sqlite3
import bcrypt
import os
from typing import Optional

# Get DB_PATH from config if available, otherwise calculate it
try:
    from config import DB_PATH
except ImportError:
    # Fallback if config.py doesn't exist
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'DATA')
    DB_PATH = os.path.join(DATA_DIR, 'intelligence_platform.db')

# ----------------------------
# Password Hashing Functions
def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

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
def register_user_cli():
    """Register a new user (for CLI use)."""
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
# Login Function (Streamlit compatible - no prints)
def login_user(user_name: str, password: str) -> bool:
    """Login a user by verifying their credentials."""
    users = _load_users()
    stored_hash: Optional[str] = users.get(user_name)

    if stored_hash is None:
        return False

    return verify_password(password, stored_hash)

# ----------------------------
# CLI Main Loop
def main():
    create_users_table()

    while True:
        print("\n=== USER AUTH SYSTEM ===")
        print("1) Register")
        print("2) Login")
        print("3) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user_cli()
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ")
            if login_user(username, password):
                print("Login successful.")
            else:
                print("Invalid credentials.")
        elif choice == "3":
            print("bye bye :3")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()