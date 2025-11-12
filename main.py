import bcrypt
import os
from typing import Optional


# Password Hashing & Verification

def hash_password(plain_password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        plain_password (str): The user's plaintext password.

    Returns:
        str: UTF-8 string of the hashed password (including salt).
    """
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Args:
        plain_password (str): The password entered by the user.
        hashed_password (str): The hashed password stored in users.txt.

    Returns:
        bool: True if the password is correct, otherwise False.
    """
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# User File Handling


def _load_users(path: str = "users.txt") -> dict:
    """
    Load users and their hashed passwords from a text file.

    Args:
        path (str): Path to the users file. Defaults to 'users.txt'.

    Returns:
        dict: A dictionary mapping usernames -> password_hash.
    """
    users = {}
    if not os.path.exists(path):
        return users

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue  # skip empty lines
            try:
                stored_user, stored_hash = line.strip().split(",", 1)
                users[stored_user.strip()] = stored_hash.strip()
            except ValueError:
                # Skip malformed lines (e.g., missing comma)
                continue
    return users


# User Registration

def register_user():
    """
    Register a new user and store their hashed password.
    """
    user_name = input("Enter user name: ").strip()
    if not user_name:
        print("Username cannot be empty.")
        return

    password = input("Enter user password: ")
    if not password:
        print("Password cannot be empty.")
        return

    users = _load_users()
    if user_name in users:
        print("Username already exists.")
        return

    hashed = hash_password(password)
    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_name}, {hashed}\n")

    print("Registration successful.")


# User Login

def login_user(user_name: str, password: str) -> bool:
    """
    Attempt to log in a user by verifying their credentials.

    Args:
        user_name (str): The username to log in with.
        password (str): The plaintext password to verify.

    Returns:
        bool: True if login succeeds, False otherwise.
    """
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


# Main Program Loop

def main():
    """
    Command-line interface for registration and login.
    """
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
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# Entry Point

if __name__ == "__main__":
    main()
