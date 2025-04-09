import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tracker.db"

print(DB_PATH)


def get_connection():
    conn = sqlite3.connect(DB_PATH,
                           check_same_thread=False)  # This allows the connection to be used in multiple threads
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
