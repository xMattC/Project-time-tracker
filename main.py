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
    rows = cursor.execute("SELECT project_name, clock_in, clock_out FROM sessions WHERE clock_out IS NOT NULL").fetchall()

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


if __name__ == "__main__":
    app()
