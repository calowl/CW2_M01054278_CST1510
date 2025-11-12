# My Project


# week 1
# Simple Python User Authentication (bcrypt)

A lightweight command-line user authentication system using `bcrypt`.

## Features
- Secure password hashing
- User registration and login
- Prevents duplicate usernames
- Handles missing or malformed user files

## How It Works
User credentials are stored in `users.txt` as:

username, bcrypt_hashed_password


Passwords are hashed and verified with bcrypt.

## Setup
```bash
pip install bcrypt
python main.py

Usage

Menu options:

Register – create a new user

Login – log in with credentials

Exit – quit the program