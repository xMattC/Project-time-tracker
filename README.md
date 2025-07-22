
# Hour Tracker Project

This Python project is designed to help track hours for various projects, following a simple clock-in/clock-out style system. It includes a modular structure, utilizing PyQt6 for a graphical user interface (GUI). Whether you are tracking billable hours for clients or managing your personal project time, this tool is flexible and easy to use.

## Technologies Used

- **Python**: Core language for backend functionality, data handling, and business logic.
- **PyQt6**: Framework used to create the desktop GUI for user interaction.
- **SQLite**: Lightweight relational database for storing time entries.


## Features

- **Clock In/Out**: Start and stop tracking time for specific projects with ease.
- **Edit Logs**: Modify time entries if corrections or updates are required.
- **Delete Logs**: Remove time entries that are no longer relevant or were entered incorrectly.
- **Export to CSV**: Export time logs into a CSV format for external use or further analysis.

## Screenshots

Here are some screenshots of the application in action:

- **Clock In/Clock Out Interface**:

  ![Clock In/Out](gui/images/clock-in-out.png)

- **Edit/Delete Logs**:

  ![Edit/Delete Logs](gui/images/edit-delete.png)


## Installation Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/xMattC/Project-time-tracker
cd Project-time-tracker
```

### Step 2: Set Up a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python -m venv .env
```

Activate the virtual environment:

- On Windows:
  ```bash
  .env\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source .env/bin/activate
  ```

### Step 3: Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the GUI

To launch the GUI:

```bash
python main.py
```

The application window will open, allowing you to:
   - **Clock In**: Start tracking time for a specific project.
   - **Clock Out**: End the tracking for the current project.
   - **Add Project**: Manually enter a new project.
   - **Edit Logs**: Modify existing time entries as needed.
   - **Delete Logs**: Remove any unnecessary or incorrect time entries.
   - **Export to CSV**: Export your time logs to a CSV file for further use.

### Database

The project uses a **SQLite** database to store time logs. The database will be automatically initialized when the application runs for the first time.

### TODO

- [ ] Create a user-friendly Windows installer:
    - Convert the script into a standalone `.exe` using PyInstaller.
    - Bundle it with an installer (e.g., Inno Setup) to allow installation to Program Files.
    - Add a Desktop shortcut with a custom icon.
