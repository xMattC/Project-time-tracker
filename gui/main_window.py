import sys

from PyQt6.QtWidgets import QFileDialog, QMainWindow, QApplication, QMessageBox, QInputDialog, QHeaderView
from PyQt6.QtCore import Qt
import pandas as pd

from tracker import core, reports
from tracker.storage import init_db, get_connection
from gui.ui_files.ui_main_window import Ui_MainWindow
from select_log_window import SelectLogWindow
from log_table_updater import LogTableUpdater
from total_hours_updater import ReportTableUpdater
from utils import get_all_unique_project_names, check_if_clocked_in

DB = get_connection()


class ProjectTrackerWindow(QMainWindow, Ui_MainWindow):
    """Main window for the Project Tracker application. Manages clock-in/clock-out functionality,
    project tracking, session management, and report generation.
    """

    def __init__(self):
        """Initializes the main window, sets up UI, connects signals, and initializes the database."""
        super().__init__()
        self.setupUi(self)  # Set up the UI components from the .ui file
        self.show()  # Display the main window
        init_db()  # Initialize the database
        self.combi_box_default = "-- Choose --"

        # Connect buttons to their respective actions
        self.button_clock_in.clicked.connect(self.clock_in)  # Connect clock-in button
        self.button_clock_out.clicked.connect(self.clock_out)  # Connect clock-out button
        self.pushButton_add_project.clicked.connect(self.add_new_project)  # Connect add project button

        # Set up the select log window, this will store the window instance
        self.select_log_window = None  # Keeps a persistent reference
        self.actionEdit_Logs.triggered.connect(self.open_select_log_window)  # Action to open select log window

        # Action to export data to Excel
        self.actionExport_Data.triggered.connect(self.export_data_to_excel)

        # Configure session table settings
        self.tableWidget_sessions.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_sessions.verticalHeader().setVisible(False)  # Hide vertical header

        # Configure report table settings
        self.tableWidget_reports.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_reports.verticalHeader().setVisible(False)  # Hide vertical header
        self.tableWidget_reports.setSortingEnabled(True)  # Enable sorting

        # Print stats on initialization:
        self.label_print_out.setText(core.status())  # Set initial status in the label
        self.update_tables()  # Update the tables when the app starts
        self.update_project_combo_box()  # Update the project selection combo box

    def clock_in(self):
        """Handles clock-in action by checking if a project is selected and if already clocked in."""
        # Check if the user is already clocked in to a project
        clocked_in = check_if_clocked_in()
        if clocked_in:
            self.error_msg_already_clocked_in(clocked_in['project_name'])  # Show error message if already clocked in
            self.comboBox_db_projects.setCurrentText(clocked_in['project_name'])  # Set the project in the combo box
            return  # Exit the function if already clocked in

        # Check if a project is selected from the combo box
        project = self.comboBox_db_projects.currentText()
        if project == self.combi_box_default:
            self.error_msg_no_project()  # Show error if no project is selected
            return  # Exit the function if no project is selected

        core.clock_in(project)  # Clock in to the selected project
        self.label_print_out.setText(core.status())  # Update the status label with the current status
        self.update_tables()  # Update the tables to reflect the clock-in

    def clock_out(self):
        """Handles clock-out action, updating status and table data."""
        core.clock_out()  # Clock out of the current project
        self.label_print_out.setText(core.status())  # Update the status label with the current status
        self.update_tables()  # Update the tables to reflect the clock-out

    def update_tables(self):
        """Updates both the sessions table and the hours table."""
        self.update_sessions_table()  # Update the sessions table
        self.update_hours_table()  # Update the hours table

    def update_hours_table(self):
        """Updates the hours table with the latest report data."""
        # Remove any table sorting indicators
        self.tableWidget_reports.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

        # Generate the report and update the table with new data
        report = reports.generate_report()["report"]
        updater = ReportTableUpdater(self.tableWidget_reports)  # Create updater instance for the report table
        updater.update_table(report)  # Update the report table

    def update_sessions_table(self):
        """Fetches and updates the sessions table with the latest session data."""
        result = reports.list_sessions()  # Get the list of sessions
        updater = LogTableUpdater(self.tableWidget_sessions)  # Create updater instance for the sessions table
        updater.update_sessions_table(result)  # Update the sessions table

    def update_project_combo_box(self):
        """Updates the project combo box with available projects from the database."""
        project_names = get_all_unique_project_names()  # Get all unique project names
        self.comboBox_db_projects.clear()  # Clear the combo box before adding new items
        self.comboBox_db_projects.addItem(self.combi_box_default)  # Add default item for "Choose"
        self.comboBox_db_projects.addItems(project_names)  # Add project names to the combo box

        # Check if the user is currently clocked in and set the combo box accordingly
        clocked_in = check_if_clocked_in()
        if clocked_in:
            self.comboBox_db_projects.setCurrentText(clocked_in['project_name'])

    def add_new_project(self):
        """Prompts the user to enter a new project name and adds it to the combo box."""
        project, ok = QInputDialog.getText(self, "New Project", "Enter Project Name : ")  # Prompt for new project name
        if ok and project:  # If the user entered a valid project name
            self.comboBox_db_projects.addItem(project)  # Add new project to the combo box
            self.comboBox_db_projects.setCurrentText(project)  # Set the combo box to the new project

    def error_msg_no_project(self):
        """Displays an error message if no project is selected."""
        QMessageBox.information(self, "Error", "Please Select a project")  # Show error dialog

    def error_msg_already_clocked_in(self, project):
        """Displays an error message if the user is already clocked in to a project."""
        QMessageBox.information(self, "Error", f"Already clocked-in to {project}")  # Show error dialog

    def open_select_log_window(self):
        """Opens the log window to select and view session logs."""
        if self.select_log_window is None:  # Check if the log window is already open
            self.select_log_window = SelectLogWindow()  # Create new log window instance
        self.select_log_window.show()  # Show the log window

    def export_data_to_excel(self):
        """Exports both session and report data to an Excel file with two sheets: 'Sessions' and 'Report'."""
        try:
            # Prompt the user to choose a file path for saving the Excel file
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Excel Files (*.xlsx)")

            if not file_path:  # If the user cancels the save operation
                return  # Exit the function

            if not file_path.endswith(".xlsx"):  # Ensure the file has the .xlsx extension
                file_path += ".xlsx"

            # Query session data from the database
            session_df = pd.read_sql_query("SELECT * FROM sessions", DB)

            # Generate report data
            report_df = pd.DataFrame(reports.generate_report()["report"])

            # Export both session and report data to Excel with two separate sheets
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                session_df.to_excel(writer, sheet_name="Sessions", index=False)  # Export sessions to "Sessions" sheet
                report_df.to_excel(writer, sheet_name="Report", index=False)  # Export report to "Report" sheet

            QMessageBox.information(self, "Export Successful",
                                    f"Data exported to:\n{file_path}")  # Show success message

        except Exception as e:
            # Show error message if the export fails
            QMessageBox.warning(self, "Export Failed", f"Could not export data:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectTrackerWindow()  # Create the main window
    sys.exit(app.exec())  # Run the event loop
