from tracker.storage import get_connection

DB = get_connection()


def get_all_unique_project_names():
    cursor = DB.cursor()

    try:
        rows = cursor.execute("SELECT DISTINCT project_name FROM sessions ORDER BY project_name").fetchall()
        return [row["project_name"] for row in rows]

    except Exception as e:
        print(f"Error fetching project names: {e}")
        return []

    finally:
        cursor.close()


def check_if_clocked_in():
    """Returns the active session if clocked in, otherwise None."""
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    cursor.close()
    return session


def filter_sessions_by_project(sessions, project_name):
    """
    Filters the sessions based on the project name.
    If "All Projects" is selected or no project is specified, returns all sessions.
    """
    project_name = project_name.strip().lower()
    if not project_name or project_name == "all projects":
        return sessions
    return [session for session in sessions
            if session["project_name"].strip().lower() == project_name]
