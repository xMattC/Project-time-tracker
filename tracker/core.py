from datetime import datetime
from .storage import get_connection

DB = get_connection()


def clock_in(project: str):
    cursor = DB.cursor()
    ongoing = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if ongoing:
        return {"error": f"Already clocked in to: {ongoing['project_name']} at {ongoing['clock_in']}"}

    cursor.execute("INSERT INTO sessions (project_name, clock_in) VALUES (?, ?)", (project, datetime.now()))
    DB.commit()
    return {"message": f"Clocked in to {project} at {datetime.now()}"}


def clock_out():
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if not session:
        return {"error": "No active session to clock out of."}

    cursor.execute("UPDATE sessions SET clock_out = ? WHERE id = ?", (datetime.now(), session['id']))
    DB.commit()
    return {"message": f"Clocked out from {session['project_name']} at {datetime.now()}"}


def status():
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if session:
        return {"project": session['project_name'], "clock_in": session['clock_in']}
    else:
        return {"message": "No active session."}


def list_sessions():
    cursor = DB.cursor()
    rows = cursor.execute("SELECT id, project_name, clock_in, clock_out FROM sessions ORDER BY id DESC").fetchall()
    if not rows:
        return {"message": "No sessions found."}

    sessions = [{"id": r['id'], "project_name": r['project_name'], "clock_in": r['clock_in'], "clock_out": r['clock_out']} for r in rows]
    return {"sessions": sessions}


def amend(session_id: int, field: str, value: str):
    if field not in {"clock_in", "clock_out"}:
        return {"error": "Field must be 'clock_in' or 'clock_out'"}

    try:
        parsed_value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}

    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()

    if not session:
        return {"error": f"No session found with ID {session_id}"}

    cursor.execute(f"UPDATE sessions SET {field} = ? WHERE id = ?", (parsed_value, session_id))
    DB.commit()
    return {"message": f"{field} updated for session ID {session_id}"}
