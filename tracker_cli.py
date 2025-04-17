# tracker_cli.py — Command-line interface for the Project Time Tracker
#
# Usage:
#   python app_cli.py [command] [arguments]
#
# Example commands:
#   python tracker_cli.py clock-in "My Project"       # Start tracking time for a project
#   python tracker_cli.py clock-out                   # Stop current session
#   python tracker_cli.py status                      # Show current clocked-in session
#   python tracker_cli.py sessions                    # List all sessions
#   python tracker_cli.py amend 1 clock_in "2025-04-15 09:00:00"   # Amend a session
#   python tracker_cli.py report                      # Generate time tracking report
#
# Before using, ensure dependencies are installed:
#   pip install typer[all] tabulate

import typer
from tracker import core, reports
from tracker.storage import init_db

# Create a Typer app instance
app = typer.Typer()


# Automatically initialize the database before any command
@app.callback()
def init():
    init_db()


# Command: Start a new session
@app.command()
def clock_in(project: str):
    result = core.clock_in(project)
    print(result)


# Command: End the current session
@app.command()
def clock_out():
    result = core.clock_out()
    print(result)


# Command: Check current active session
@app.command()
def status():
    result = core.status()
    print(result)


# Command: Generate a summary report
@app.command()
def report():
    result = reports.generate_report()
    print(result)


# Command: List all recorded sessions
@app.command()
def sessions():
    result = reports.list_sessions()
    print(result)


# Command: Amend a session's timestamp
@app.command()
def amend(id: int, field: str, value: str):
    result = core.amend(id, field, value)
    print(result)


# Entry point when running from the command line
if __name__ == "__main__":
    app()
