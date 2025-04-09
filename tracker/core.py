from datetime import datetime
from .storage import get_connection

DB = get_connection()


def clock_in(project: str):
    cursor = DB.cursor()
    ongoing = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if ongoing:
        print(f"Already clocked in to: {ongoing['project_name']} at {ongoing['clock_in']}")
        return
    cursor.execute("INSERT INTO sessions (project_name, clock_in) VALUES (?, ?)", (project, datetime.now()))
    DB.commit()


def clock_out():
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if not session:
        print("No active session to clock out of.")
        return
    cursor.execute("UPDATE sessions SET clock_out = ? WHERE id = ?", (datetime.now(), session['id']))
    DB.commit()


def status():
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if session:
        print(f"Clocked in to: {session['project_name']} at {session['clock_in']}")
    else:
        print("No active session.")


def list_sessions():
    cursor = DB.cursor()
    rows = cursor.execute("SELECT id, project_name, clock_in, clock_out FROM sessions ORDER BY id DESC").fetchall()
    if not rows:
        print("No sessions found.")
        return
    for r in rows:
        print(dict(r))


def amend(session_id: int, field: str, value: str):
    if field not in {"clock_in", "clock_out"}:
        print("Field must be 'clock_in' or 'clock_out'")
        return

    try:
        parsed_value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid datetime format. Use YYYY-MM-DD HH:MM:SS")
        return

    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()

    if not session:
        print(f"No session found with ID {session_id}")
        return

    cursor.execute(f"UPDATE sessions SET {field} = ? WHERE id = ?", (parsed_value, session_id))
    DB.commit()
    print(f"{field} updated for session ID {session_id}")
