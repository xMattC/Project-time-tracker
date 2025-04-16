from flask import Flask, render_template, request, redirect, url_for
from tracker import core

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/clock_in', methods=['POST'])
def clock_in():
    project = request.form.get('project')
    if project:
        core.clock_in(project)
    return redirect(url_for('home'))


@app.route('/clock_out', methods=['POST'])
def clock_out():
    core.clock_out()
    return redirect(url_for('home'))


@app.route('/status', methods=['GET'])
def status():
    core.status()
    return redirect(url_for('home'))


@app.route('/sessions', methods=['GET'])
def sessions():
    sessions_data = core.list_sessions()  # Assuming this function returns data
    return render_template('sessions.html', sessions=sessions_data)


if __name__ == "__main__":
    app.run(debug=True)
