import typer
from tracker import core, reports
from tracker.storage import init_db

app = typer.Typer()


@app.callback()
def init():
    init_db()


@app.command()
def clock_in(project: str):
    core.clock_in(project)


@app.command()
def clock_out():
    core.clock_out()


@app.command()
def status():
    core.status()


@app.command()
def report():
    reports.generate_report()


@app.command()
def sessions():
    reports.list_sessions()


@app.command()
def amend(id: int, field: str, value: str):
    core.amend(id, field, value)


if __name__ == "__main__":
    app()
