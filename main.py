import typer
from datetime import datetime
import db
import pandas as pd

DB = db.get_connection()
db.init_db()

app = typer.Typer()


@app.command()
def clock_in(project: str):
    print("clock_in function running")  # inside clock_in()
    cursor = DB.cursor()
    ongoing = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if ongoing:
        print(f"Already clocked in to: {ongoing['project_name']} at {ongoing['clock_in']}")
        return
    cursor.execute("INSERT INTO sessions (project_name, clock_in) VALUES (?, ?)", (project, datetime.now()))
    DB.commit()


@app.command()
def clock_out():
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if not session:
        return
    cursor.execute("UPDATE sessions SET clock_out = ? WHERE id = ?", (datetime.now(), session['id']))
    DB.commit()


@app.command()
def status():
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
    if session:
        print(f"Clocked in to: {session['project_name']} at {session['clock_in']}")
    else:
        print("No active session.")


@app.command()
def report():
    cursor = DB.cursor()
    rows = cursor.execute(
        "SELECT project_name, clock_in, clock_out FROM sessions WHERE clock_out IS NOT NULL").fetchall()

    if not rows:
        print("No completed sessions yet.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=["project_name", "clock_in", "clock_out"])

    # Convert timestamps to datetime
    df["clock_in"] = pd.to_datetime(df["clock_in"])
    df["clock_out"] = pd.to_datetime(df["clock_out"])

    # Calculate duration in hours
    df["duration_hours"] = (df["clock_out"] - df["clock_in"]).dt.total_seconds() / 3600

    # Group and sum durations by project
    summary = df.groupby("project_name")["duration_hours"].sum().reset_index()

    for _, row in summary.iterrows():
        print(f"Project: {row['project_name']} — {row['duration_hours']:.2f} hours")


@app.command()
def amend(
        session_id: int,
        clock_in: str = typer.Option(None, help="New clock-in time (YYYY-MM-DD HH:MM)"),
        clock_out: str = typer.Option(None, help="New clock-out time (YYYY-MM-DD HH:MM)"),
        project: str = typer.Option(None, help="New project name")
):
    """Amend a session's clock-in, clock-out, or project name."""
    cursor = DB.cursor()
    session = cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()

    if not session:
        print(f"No session found with ID {session_id}")
        return

    updates = []
    values = []

    if clock_in:
        try:
            datetime.strptime(clock_in, "%Y-%m-%d %H:%M")
            updates.append("clock_in = ?")
            values.append(clock_in)
        except ValueError:
            print("Invalid clock-in format. Use YYYY-MM-DD HH:MM")
            return

    if clock_out:
        try:
            datetime.strptime(clock_out, "%Y-%m-%d %H:%M")
            updates.append("clock_out = ?")
            values.append(clock_out)
        except ValueError:
            print("Invalid clock-out format. Use YYYY-MM-DD HH:MM")
            return

    if project:
        updates.append("project_name = ?")
        values.append(project)

    if not updates:
        print("No changes provided.")
        return

    values.append(session_id)
    update_query = f"UPDATE sessions SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(update_query, tuple(values))
    DB.commit()

    print(f"Session {session_id} updated.")


@app.command()
def sessions():
    """List all sessions (ID, project, clock in/out)."""
    cursor = DB.cursor()
    rows = cursor.execute("SELECT id, project_name, clock_in, clock_out FROM sessions").fetchall()
    for row in rows:
        _clock_in = pd.to_datetime(row['clock_in']).strftime("%Y-%m-%d %H:%M") if row['clock_in'] else "—"
        _clock_out = pd.to_datetime(row['clock_out']).strftime("%Y-%m-%d %H:%M") if row['clock_out'] else "—"
        print(f"[{row['id']}] {row['project_name']} — In: {_clock_in} | Out: {_clock_out}")


if __name__ == "__main__":
    app()
