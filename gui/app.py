from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QInputDialog
from gui.main_window import Ui_MainWindow
from tracker import core, reports
from tracker.storage import init_db
import sys
from tracker.storage import get_connection

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
        self.button_sessions.clicked.connect(self.sessions)
        self.button_report.clicked.connect(self.report)
        self.button_status.clicked.connect(self.status)
        self.pushButton_add_project.clicked.connect(self.add_new_project)
        # self.label_print_out.clicked.connect(self.)

        # Print stats on init:
        self.label_print_out.setText(core.status())

        self.update_project_combo_box()

    def clock_in(self):
        project = self.comboBox_db_projects.currentText()
        if project == self.combi_box_default:
            self.error_msg_no_project()

        else:
            cursor = DB.cursor()
            clocked_in = cursor.execute("SELECT * FROM sessions WHERE clock_out IS NULL").fetchone()
            if clocked_in:
                self.error_msg_already_clocked_in(clocked_in['project_name'])

            else:
                result = core.clock_in(project)
                self.label_print_out.setText(str(result))

    def clock_out(self):
        message = core.clock_out()
        self.label_print_out.setText(str(message))

    def status(self):
        message = core.status()
        self.label_print_out.setText(str(message))

    def report(self):
        result = reports.generate_report()
        # self.label_print_out.setText(str(result))
        self.display_report_in_table(result["report"])

    def sessions(self):
        result = reports.list_sessions()
        # self.label_print_out.setText(str(result))
        self.display_sessions_in_table(result["sessions"])

    def display_report_in_table(self, report_data):
        self.tableWidget_reports.setRowCount(len(report_data))
        self.tableWidget_reports.setColumnCount(2)
        self.tableWidget_reports.setHorizontalHeaderLabels(["Project", "Duration"])

        for row_index, entry in enumerate(report_data):
            self.tableWidget_reports.setItem(row_index, 0, QTableWidgetItem(entry["project_name"]))
            self.tableWidget_reports.setItem(row_index, 1, QTableWidgetItem(entry["duration"]))

    def display_sessions_in_table(self, sessions):
        self.tableWidget.setRowCount(len(sessions))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Project", "Clock In", "Clock Out", "ID"])

        for row_index, session in enumerate(sessions):
            self.tableWidget.setItem(row_index, 0, QTableWidgetItem(session["project_name"]))
            self.tableWidget.setItem(row_index, 1, QTableWidgetItem(session["clock_in"]))
            self.tableWidget.setItem(row_index, 2, QTableWidgetItem(session["clock_out"]))
            self.tableWidget.setItem(row_index, 3, QTableWidgetItem(str(session["id"])))

    def update_project_combo_box(self):
        # add all project from db.
        project_names = get_all_unique_project_names()
        self.comboBox_db_projects.clear()
        self.comboBox_db_projects.addItem(self.combi_box_default)
        self.comboBox_db_projects.addItems(project_names)

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
