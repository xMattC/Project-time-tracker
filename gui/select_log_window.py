import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QApplication, QHeaderView, QMainWindow, QMessageBox

from gui.ui_files.ui_select_log_window import Ui_SelectLogWindow
from log_table_updater import LogTableManager, LogTableUpdater
from modify_log_window import ModifyLogWindow
from tracker import reports
from tracker.storage import delete_sessions_by_ids, init_db
from utils import filter_sessions_by_project, get_all_unique_project_names


class SelectLogWindow(QMainWindow, Ui_SelectLogWindow):
    """Main window for selecting, editing, and deleting log sessions."""

    def __init__(self):
        """Initializes the UI, database, and sets up event bindings."""
        super().__init__()
        self.setupUi(self)
        self.show()

        # Initialize database (creates tables if not present)
        init_db()

        # Table manager abstraction to help interact with the log table
        self.session_table = LogTableManager(self.tableWidget_log_edit)

        # Configure table to allow multi-row selection and stretch columns
        self.tableWidget_log_edit.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_log_edit.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableWidget_log_edit.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_log_edit.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

        # Connect UI elements to methods
        self.comboBox_projects.currentIndexChanged.connect(self.combo_box_index_changed)
        self.pushButton_delete_log.clicked.connect(self.delete_selected_rows)
        self.pushButton_edit_log.clicked.connect(self.open_edit_log_window)
        self.tableWidget_log_edit.selectionModel().selectionChanged.connect(self.update_buttons_state)

        # Disable edit button by default (until a valid session is selected)
        self.pushButton_edit_log.setEnabled(False)

        # Reference to edit log window (keeps it open persistently)
        self.edit_log_window = None

        # Populate table and combo box with data on launch
        self.update_log_table()
        self.update_project_combo_box()

    def combo_box_index_changed(self):
        """Updates log table when the selected project in the combo box changes."""
        self.update_log_table()
        self.clear_table_selection()

    def update_log_table(self):
        """Fetches and filters session data, then updates the table display."""
        sessions = reports.list_sessions()["sessions"]  # Fetch all sessions from the report module
        selected_project = self.comboBox_projects.currentText().strip()  # Get currently selected project name
        filtered_sessions = filter_sessions_by_project(sessions, selected_project)  # Apply project filter

        # Sort sessions by clock-in time (descending)
        sorted_sessions = sorted(filtered_sessions, key=lambda session: session['clock_in'], reverse=True)

        LogTableUpdater(self.tableWidget_log_edit).update_sessions_table({"sessions": sorted_sessions})

    def update_project_combo_box(self):
        """Populates the project combo box with all unique project names."""
        self.comboBox_projects.clear()
        self.comboBox_projects.addItem("All Projects")  # Default option
        self.comboBox_projects.addItems(get_all_unique_project_names())  # Populate with all project names
        self.comboBox_projects.setCurrentText("All Projects")  # Set default selection

    def delete_selected_rows(self):
        """Deletes selected session rows after confirmation, then refreshes the UI."""
        session_ids = self.session_table.get_selected_session_ids()  # Get selected session IDs

        if not session_ids:
            QMessageBox.information(self, "No Selection", "Please select one or more rows to delete.")
            return

        # Confirm deletion message box
        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete {len(session_ids)} selected session(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Perform deletion, refresh data
        delete_sessions_by_ids(session_ids)
        self.update_log_table()
        self.update_project_combo_box()
        self.clear_table_selection()

        # Notify user
        QMessageBox.information(self, "Deleted", f"{len(session_ids)} session(s) were deleted.")

    def update_buttons_state(self):
        """Enables or disables the edit and delete buttons based on the current table selection."""
        selected_rows = self.tableWidget_log_edit.selectionModel().selectedRows()

        # Disable both buttons by default
        self.pushButton_edit_log.setEnabled(False)
        self.pushButton_delete_log.setEnabled(False)

        if not selected_rows:
            return

        first_row = selected_rows[0].row()
        duration_item = self.tableWidget_log_edit.item(first_row, 3)  # Column 3 is assumed to be 'Duration'

        if not duration_item:
            return

        # Enable edit button if only one row is selected and it’s not ongoing
        if len(selected_rows) == 1 and duration_item.text() != "Ongoing":
            self.pushButton_edit_log.setEnabled(True)

        # Enable delete button for any non-ongoing session
        if duration_item.text() != "Ongoing":
            self.pushButton_delete_log.setEnabled(True)

    def clear_table_selection(self):
        """Clears all selections in the log table and updates button states."""
        self.tableWidget_log_edit.clearSelection()
        self.update_buttons_state()

    def open_edit_log_window(self):
        """Opens the edit log window for the selected session."""
        selected_ids = self.session_table.get_selected_session_ids()

        if not selected_ids:
            QMessageBox.information(self, "No Selection", "Please select a session to edit.")
            return

        selected_id = selected_ids[0]

        if self.edit_log_window is None:
            self.edit_log_window = ModifyLogWindow()

            # Connect the signal from ModifyLogWindow to update the table
            self.edit_log_window.session_updated.connect(self.update_log_table)

        self.edit_log_window.load_session(selected_id)
        self.edit_log_window.show()
        self.update_log_table()

    def closeEvent(self, event):
        """Handles window close event and clears table selection before closing."""
        self.clear_table_selection()
        super().closeEvent(event)


if __name__ == "__main__":
    # Launch the application
    app = QApplication(sys.argv)
    window = SelectLogWindow()
    sys.exit(app.exec())
