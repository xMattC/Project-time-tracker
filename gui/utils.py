from tracker.storage import get_connection

DB = get_connection()  # Get database connection

def get_all_unique_project_names():
    """Fetches all unique project names from the database."""
    cursor = DB.cursor()

    try:
        # Execute query to fetch distinct project names and sort them
        rows = cursor.execute("SELECT DISTINCT project_name FROM sessions ORDER BY project_name").fetchall()
        # Return a list of project names
        return [row["project_name"] for row in rows]

    except Exception as e:
        print(f"Error fetching project names: {e}")  # Print error if query fails
        return []  # Return an empty list if an error occurs

    finally:
        cursor.close()  # Ensure the cursor is closed after operation


def check_if_clocked_in():
    """Returns the active session if clocked in, otherwise None."""
    cursor = DB.cursor()
    # Execute query to find the session where clock_out is NULL (indicating it's still active)
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    cursor.close()  # Close the cursor
    return session  # Return the session if clocked in, otherwise None


def filter_sessions_by_project(sessions, project_name):
    """
    Filters the sessions based on the project name.
    If "All Projects" is selected or no project is specified, returns all sessions.
    """
    project_name = project_name.strip().lower()  # Clean and lower case the project name
    if not project_name or project_name == "all projects":
        return sessions  # Return all sessions if no project is specified or "All Projects" is selected
    # Filter sessions to match the project name
    return [session for session in sessions
            if session["project_name"].strip().lower() == project_name]
