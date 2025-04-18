from tracker.storage import get_connection
from tabulate import tabulate
from datetime import datetime
import pandas as pd

DB = get_connection()


def tidy_timestamp(timestamp_str):
    """Convert timestamp string to a more readable format."""
    try:
        # Try parsing the timestamp with microseconds
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        # If microseconds are not present, fallback to parsing without
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    # Return the formatted timestamp
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def generate_report():
    """Generate a report summarizing project hours."""
    cursor = DB.cursor()
    try:
        rows = cursor.execute(
            "SELECT project_name, clock_in, clock_out FROM sessions WHERE clock_out IS NOT NULL").fetchall()

        if not rows:
            message = {"message": "No completed sessions yet."}
            print(message["message"])
            return message

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=["project_name", "clock_in", "clock_out"])
        df["clock_in"] = df["clock_in"].apply(tidy_timestamp)
        df["clock_out"] = df["clock_out"].apply(tidy_timestamp)
        df["duration_hours"] = (pd.to_datetime(df["clock_out"]) - pd.to_datetime(
            df["clock_in"])).dt.total_seconds() / 3600

        # Group and summarize durations
        duration_summary = df.groupby("project_name")["duration_hours"].sum().reset_index()

        # Get latest clock_out per project
        latest_clock_outs = df.groupby("project_name")["clock_out"].max().reset_index()

        # Merge both summaries
        summary = pd.merge(duration_summary, latest_clock_outs, on="project_name")

        # Build return and display data
        report_data = []
        table_data = []
        for _, row in summary.iterrows():
            hours = int(row['duration_hours'])
            minutes = int((row['duration_hours'] - hours) * 60)
            duration_str = f"{hours}h {minutes}m"
            project_name = row["project_name"]
            latest_clock_out = row["clock_out"]

            report_data.append({
                "project_name": project_name,
                "duration": duration_str,
                "latest_clock_out": latest_clock_out  # Include this in the returned data
            })
            table_data.append([project_name, duration_str])

        headers = ["Project", "Duration"]
        table_str = tabulate(table_data, headers=headers, tablefmt="grid")

        return {
            "report": report_data,
            "table": table_str
        }

    except Exception as e:
        error_msg = {"error": f"Error generating report: {e}"}
        print(error_msg["error"])
        return error_msg

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
            message = {"message": "No sessions found."}
            print(message["message"])

            return message

        sessions = []
        table_data = []

        for r in rows:
            clock_in = tidy_timestamp(r["clock_in"])
            clock_out = tidy_timestamp(r["clock_out"]) if r["clock_out"] else "—"

            sessions.append({
                "id": r["id"],
                "project_name": r["project_name"],
                "clock_in": clock_in,
                "clock_out": clock_out,
            })

            table_data.append([r["id"], r["project_name"], clock_in, clock_out])

        headers = ["ID", "Project", "Clock In", "Clock Out"]
        table_str = tabulate(table_data, headers=headers, tablefmt="grid")
        print(table_str)

        return {
            "sessions": sessions,
            "table": table_str
        }

    except Exception as e:
        error_msg = {"error": f"Error listing sessions: {e}"}
        print(error_msg["error"])
        return error_msg

    finally:
        cursor.close()
