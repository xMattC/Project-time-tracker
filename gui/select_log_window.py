from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget
from PyQt6.QtWidgets import QHeaderView
from tracker.storage import init_db, delete_sessions_by_ids
from tracker import reports
from gui.ui_files.ui_select_log_window import Ui_SelectLogWindow
from session_updater import SessionTableUpdater
from utility_functions import get_all_unique_project_names, filter_sessions_by_project
from session_updater import SessionTableManager
import sys


class SelectLogWindow(QMainWindow, Ui_SelectLogWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        init_db()

        # Table setup
        self.tableWidget_log_edit.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidget_log_edit.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_log_edit.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        self.session_table = SessionTableManager(self.tableWidget_log_edit)

        # Events
        self.comboBox_projects.currentIndexChanged.connect(self.update_log_table)
        self.pushButton_delete_log.clicked.connect(self.delete_selected_rows)

        # Initial UI load
        self.update_log_table()
        self.update_project_combo_box()

    def update_log_table(self):
        sessions = reports.list_sessions()["sessions"]
        selected_project = self.comboBox_projects.currentText().strip()

        filtered_sessions = filter_sessions_by_project(sessions, selected_project)

        updater = SessionTableUpdater(self.tableWidget_log_edit)
        updater.update_sessions_table({"sessions": filtered_sessions})

    def update_project_combo_box(self):
        self.comboBox_projects.clear()
        self.comboBox_projects.addItem("All Projects")
        self.comboBox_projects.addItems(get_all_unique_project_names())
        self.comboBox_projects.setCurrentText("All Projects")

    def delete_selected_rows(self):
        session_ids = self.session_table.get_selected_session_ids()

        if not session_ids:
            QMessageBox.information(self, "No Selection", "Please select one or more rows to delete.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {len(session_ids)} selected session(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        delete_sessions_by_ids(session_ids)
        self.update_log_table()
        self.update_project_combo_box()
        QMessageBox.information(self, "Deleted", f"{len(session_ids)} session(s) were deleted.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectLogWindow()  # The window you're working with
    sys.exit(app.exec())
