import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QHeaderView
from PyQt6.QtCore import Qt

from tracker import core, reports
from tracker.storage import init_db, get_connection
from gui.ui_files.ui_main_window import Ui_MainWindow
from select_log_window import SelectLogWindow
from log_table_updater import LogTableUpdater
from total_hours_updater import ReportTableUpdater
from utils import get_all_unique_project_names, check_if_clocked_in

DB = get_connection()


class ProjectTrackerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        init_db()  # Initialise the database
        self.combi_box_default = "-- Choose --"
        self.button_clock_in.clicked.connect(self.clock_in)
        self.button_clock_out.clicked.connect(self.clock_out)
        self.pushButton_add_project.clicked.connect(self.add_new_project)
        # self.label_print_out.clicked.connect(self.)

        # self.report_updater = ReportTableUpdater(self.tableWidget_reports)
        self.select_log_window = None  # Keeps a persistent reference
        self.actionEdit_Logs.triggered.connect(self.open_select_log_window)

        # Table configurations
        self.tableWidget_sessions.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_sessions.verticalHeader().setVisible(False)

        self.tableWidget_reports.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_reports.verticalHeader().setVisible(False)
        self.tableWidget_reports.setSortingEnabled(True)

        # Print stats on init:
        self.label_print_out.setText(core.status())
        self.update_tables()
        self.update_project_combo_box()

    def clock_in(self):

        clocked_in = check_if_clocked_in()
        if clocked_in:
            self.error_msg_already_clocked_in(clocked_in['project_name'])
            self.comboBox_db_projects.setCurrentText(clocked_in['project_name'])
            return

        project = self.comboBox_db_projects.currentText()
        if project == self.combi_box_default:
            self.error_msg_no_project()
            return

        else:
            core.clock_in(project)
            self.label_print_out.setText(core.status())
            self.update_tables()

    def clock_out(self):
        core.clock_out()
        self.label_print_out.setText(core.status())
        self.update_tables()

    def update_tables(self):
        """Updates both sessions and hours tables."""
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
        print(result)
        updater = LogTableUpdater(self.tableWidget_sessions)
        updater.update_sessions_table(result)

    def update_project_combo_box(self):
        project_names = get_all_unique_project_names()
        self.comboBox_db_projects.clear()
        self.comboBox_db_projects.addItem(self.combi_box_default)
        self.comboBox_db_projects.addItems(project_names)

        clocked_in = check_if_clocked_in()
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

    def open_select_log_window(self):
        if self.select_log_window is None:
            self.select_log_window = SelectLogWindow()
        self.select_log_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectTrackerWindow()
    sys.exit(app.exec())
