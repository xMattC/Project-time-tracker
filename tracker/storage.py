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


def delete_sessions_by_ids(session_ids):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("DELETE FROM sessions WHERE id = ?", [(sid,) for sid in session_ids])
    conn.commit()


def get_session_by_id(session_id: int):
    """
    Retrieves a session's data from the database based on the session ID.

    param session_id: The ID of the session to retrieve.
    return: A dictionary containing session data, or None if no session is found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()

    if row:
        # Get the column names from the cursor
        column_names = [description[0] for description in cursor.description]
        # Create a dictionary mapping column names to row values
        session_data = dict(zip(column_names, row))
        return session_data
    return None
