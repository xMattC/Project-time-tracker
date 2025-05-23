from datetime import datetime
from tracker.storage import get_connection

DB = get_connection()


def clock_in(project: str) -> str:
    cursor = DB.cursor()
    ongoing = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if ongoing:
        return f"Already clocked in to: {ongoing['project_name']} at {ongoing['clock_in']}"

    now = datetime.now()
    cursor.execute("INSERT INTO sessions (project_name, clock_in) VALUES (?, ?)", (project, now))
    DB.commit()
    return f"Clocked in to {project} at {now.strftime('%Y-%m-%d %H:%M:%S')}"


def clock_out() -> str:
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if not session:
        return "No active session to clock out of."

    now = datetime.now()
    formatted_time = now.strftime('%H:%M - %d %b %y')  # Format: 16:35 - 10 Jan 23
    cursor.execute("UPDATE sessions SET clock_out = ? WHERE id = ?", (now, session['id']))
    DB.commit()
    return f"Clocked-out: {session['project_name']}  \n{formatted_time}"


def status() -> str:
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if session:
        return f"Clocked-in"
    else:
        return "Clocked-out"


def list_sessions() -> str:
    cursor = DB.cursor()
    rows = cursor.execute("SELECT id, project_name, clock_in, clock_out FROM sessions ORDER BY id DESC").fetchall()
    if not rows:
        return "No sessions found."

    lines = []
    for row in rows:
        lines.append(
            f"ID: {row['id']} | Project: {row['project_name']} | In: {row['clock_in']} | Out: {row['clock_out'] or 'In Progress'}"
        )
    return "\n".join(lines)


def amend_db_session(session_id: int, field: str, value: str) -> str:
    if field not in {"clock_in", "clock_out"}:
        return "Error: Field must be 'clock_in' or 'clock_out'"

    try:
        parsed_value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "Error: Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"

    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()

    if not session:
        return f"Error: No session found with ID {session_id}"

    cursor.execute(f"UPDATE sessions SET {field} = ? WHERE id = ?", (parsed_value, session_id))
    DB.commit()
    return f"{field} updated for session ID {session_id}"
