from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QInputDialog, QHeaderView
from tracker import core, reports
from tracker.storage import init_db
import sys
from tracker.storage import get_connection
from datetime import datetime
from PyQt6.QtCore import Qt

from gui.ui_files.ui_main_window import Ui_MainWindow
from gui.ui_files.ui_select_data_window import Ui_SelectDataWindow
from gui.ui_files.ui_calendar_window import Ui_CalendarWindow
from session_updater import SessionTableUpdater
from total_hours_updater import ReportTableUpdater

DB = get_connection()


def get_all_unique_project_names():
    cursor = DB.cursor()

    try:
        rows = cursor.execute("SELECT DISTINCT project_name FROM sessions ORDER BY project_name").fetchall()
        return [row["project_name"] for row in rows]

    except Exception as e:
        print(f"Error fetching project names: {e}")
        return []

    finally:
        cursor.close()


class ProjectTrackerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        init_db()  # Initialise the database
        self.combi_box_default = "-- Choose --"
        self.button_clock_in.clicked.connect(self.clock_in)
        self.button_clock_out.clicked.connect(self.clock_out)
        self.button_sessions.clicked.connect(self.update_sessions_table)
        self.button_report.clicked.connect(self.update_hours_table)
        self.pushButton_add_project.clicked.connect(self.add_new_project)
        # self.label_print_out.clicked.connect(self.)

        # self.report_updater = ReportTableUpdater(self.tableWidget_reports)

        # Set-up hours and sessions tables
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_reports.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget_reports.verticalHeader().setVisible(False)
        self.tableWidget_reports.setSortingEnabled(True)

        # Print stats on init:
        self.label_print_out.setText(core.status())
        self.update_hours_table()
        self.update_sessions_table()
        self.update_project_combo_box()

    def clock_in(self):

        cursor = DB.cursor()
        clocked_in = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
        if clocked_in:
            self.error_msg_already_clocked_in(clocked_in['project_name'])
            self.comboBox_db_projects.setCurrentText(clocked_in['project_name'])
            return

        project = self.comboBox_db_projects.currentText()
        if project == self.combi_box_default:
            self.error_msg_no_project()

        else:
            core.clock_in(project)
            self.label_print_out.setText(core.status())
            self.update_sessions_table()
            self.update_hours_table()

    def clock_out(self):
        core.clock_out()
        self.label_print_out.setText(core.status())
        self.update_sessions_table()
        self.update_hours_table()

    def update_hours_table(self):
        # Remove any table sorting:
        self.tableWidget_reports.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

        report = reports.generate_report()["report"]
        updater = ReportTableUpdater(self.tableWidget_reports)
        updater.update_table(report)

    def update_sessions_table(self):
        result = reports.list_sessions()
        updater = SessionTableUpdater(self.tableWidget)
        updater.update_sessions_table(result)

    def update_project_combo_box(self):
        project_names = get_all_unique_project_names()
        self.comboBox_db_projects.clear()
        self.comboBox_db_projects.addItem(self.combi_box_default)
        self.comboBox_db_projects.addItems(project_names)
        cursor = DB.cursor()
        clocked_in = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
        if clocked_in:
            self.comboBox_db_projects.setCurrentText(clocked_in['project_name'])

    def add_new_project(self):
        project, ok = QInputDialog.getText(self, "New Project", "Enter Project Name : ")
        if ok and project:
            self.comboBox_db_projects.addItem(project)
            self.comboBox_db_projects.setCurrentText(project)

    def error_msg_no_project(self):
        QMessageBox.information(self, "Error", "Please Select a project")

    def error_msg_already_clocked_in(self, project):
        QMessageBox.information(self, "Error", f"Already clocked-in to {project}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectTrackerWindow()
    sys.exit(app.exec())
