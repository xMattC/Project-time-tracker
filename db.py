import sqlite3
from pathlib import Path

DB_PATH = Path("tracker.db")
print(DB_PATH)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                clock_in TIMESTAMP NOT NULL,
                clock_out TIMESTAMP
            )
        ''')
