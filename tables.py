import sqlite3
import os
import pandas as pd
from config import DATA_DIR, DB_PATH

# Connect to DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create additional tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS cyber_incidents (
    incident_id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    severity TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS datasets_metadata (
    dataset_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    uploaded_by TEXT NOT NULL,
    upload_date TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS it_tickets (
    ticket_id INTEGER PRIMARY KEY,
    priority TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolution_time_hours REAL
)
""")

conn.commit()

def load_csv_to_table(filename, table_name):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    try:
        df = pd.read_csv(path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        print(f"Loaded {len(df)} rows into '{table_name}' from {filename}")
    except Exception as e:
        print(f"Failed to load {filename} -> {e}")

# Load tables (run once)
# load_csv_to_table('cyber_incidents.csv', 'cyber_incidents')
# load_csv_to_table('datasets_metadata.csv', 'datasets_metadata')
# load_csv_to_table('it_tickets.csv', 'it_tickets')

conn.close()