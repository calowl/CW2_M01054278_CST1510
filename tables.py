import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect(
    r"C:\Users\caleb\VSCode\CW2_M01054278_CST1510\DATA\intelligence_platform.db"
)
cursor = conn.cursor()

# Create the 'users' table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user'
)
""")
conn.commit()

# Insert a user
cursor.execute(
    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
    ('bob', 'hashed_password_here', 'user')
)
conn.commit()

# Query and print all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print(users)

# Update a user's role
cursor.execute(
    "UPDATE users SET role = ? WHERE username = ?",
    ('admin', 'bob')
)
conn.commit()

# Delete a user safely
cursor.execute("DELETE FROM users WHERE username = ?", ('alice',))
conn.commit()
print(f"Deleted {cursor.rowcount} user(s)")

# Close the connection
conn.close()
