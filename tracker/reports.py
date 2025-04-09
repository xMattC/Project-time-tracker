from .storage import get_connection
from tabulate import tabulate
from datetime import datetime
import pandas as pd

DB = get_connection()


def tidy_timestamp(timestamp_str):
    """Convert timestamp string to a more readable format."""
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def generate_report():
    """Generate a report summarizing project hours."""
    cursor = DB.cursor()
    try:
        rows = cursor.execute(
            "SELECT project_name, clock_in, clock_out FROM sessions WHERE clock_out IS NOT NULL"
        ).fetchall()

        if not rows:
            print("No completed sessions yet.")
            return

        # Convert rows to DataFrame
        df = pd.DataFrame(rows, columns=["project_name", "clock_in", "clock_out"])

        # Tidy up the clock_in and clock_out
        df["clock_in"] = df["clock_in"].apply(tidy_timestamp)
        df["clock_out"] = df["clock_out"].apply(lambda x: tidy_timestamp(x))

        # Calculate the duration in hours
        df["duration_hours"] = (pd.to_datetime(df["clock_out"]) - pd.to_datetime(df["clock_in"])).dt.total_seconds() / 3600

        # Group by project and sum the durations
        summary = df.groupby("project_name")["duration_hours"].sum().reset_index()

        # Prepare the data for tabulate
        data = []
        for _, row in summary.iterrows():
            data.append([row["project_name"], f"{row['duration_hours']:.2f} hours"])

        # Define headers
        headers = ["Project", "Total Duration"]

        # Print the report using tabulate
        print(tabulate(data, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"Error generating report: {e}")
    finally:
        cursor.close()


def list_sessions():
    """List all sessions showing clock-in and clock-out times."""
    cursor = DB.cursor()
    try:
        rows = cursor.execute(
            "SELECT id, project_name, clock_in, clock_out FROM sessions ORDER BY id DESC"
        ).fetchall()

        if not rows:
            print("No sessions found.")
            return

        # Prepare data for tabulate
        data = []
        for r in rows:
            clock_in = tidy_timestamp(r['clock_in'])
            clock_out = tidy_timestamp(r['clock_out']) if r['clock_out'] else '—'
            data.append([r['id'], r['project_name'], clock_in, clock_out])

        # Define table headers
        headers = ["ID", "Project", "Clock In", "Clock Out"]

        # Print the table using tabulate
        print(tabulate(data, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"Error listing sessions: {e}")
    finally:
        cursor.close()