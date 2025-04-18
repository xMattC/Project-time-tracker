from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidget, QAbstractItemView
from PyQt6.QtWidgets import QHeaderView
from tracker.storage import init_db, delete_sessions_by_ids
from tracker import reports
from gui.ui_files.ui_mod_log_window import Ui_ModifyLogWindow
from log_table_updater import LogTableUpdater, LogTableManager
from utils import get_all_unique_project_names, filter_sessions_by_project
from PyQt6.QtCore import Qt
import sys
from tracker.storage import get_session_by_id
from PyQt6.QtCore import QTime, QDate

from PyQt6.QtCore import QTime, QDate


class ModifyLogWindow(QDialog, Ui_ModifyLogWindow):
    def __init__(self, session_id):
        super().__init__()
        self.setupUi(self)  # Set up the UI first before any logic

        init_db()  # Initialize database connection
        self.session_id = session_id
        self.session_data = get_session_by_id(self.session_id)

        # Format clock in/out edit:
        self.dateEdit_clock_in.setDisplayFormat('dd MMM yy')
        self.dateEdit_clock_out.setDisplayFormat('dd MMM yy')

        # Connect button box signals to methods
        self.buttonBox.accepted.connect(self.accept_action)
        self.buttonBox.rejected.connect(self.reject_action)

        if self.session_data:
            self.set_clock_in_time(self.session_data['clock_in'])
            self.set_clock_out_time(self.session_data['clock_out'])

        # Show the window after UI has been set up
        self.show()

    def set_clock_in_time(self, clock_in_str):
        """Sets the clock-in date and time in the corresponding widgets."""
        clock_in_date = clock_in_str.split(' ')[0]  # Extract date (YYYY-MM-DD)
        clock_in_time = clock_in_str.split(' ')[1][:8]  # Extract time (HH:MM:SS), removing fractional seconds

        hours, minutes, seconds = map(int, clock_in_time.split(':'))

        self.dateEdit_clock_in.setDate(QDate.fromString(clock_in_date, 'yyyy-MM-dd'))
        self.timeEdit_clock_in.setTime(QTime(hours, minutes, seconds))

    def set_clock_out_time(self, clock_out_str):
        """Sets the clock-out date and time in the corresponding widgets."""
        clock_out_date = clock_out_str.split(' ')[0]  # Extract date (YYYY-MM-DD)
        clock_out_time = clock_out_str.split(' ')[1][:8]  # Extract time (HH:MM:SS), removing fractional seconds

        hours, minutes, seconds = map(int, clock_out_time.split(':'))

        self.dateEdit_clock_out.setDate(QDate.fromString(clock_out_date, 'yyyy-MM-dd'))
        self.timeEdit_clock_out.setTime(QTime(hours, minutes, seconds))

    def accept_action(self):
        """Handles the OK button click (accepted signal)."""
        self.accept()  # This closes the dialog

    def reject_action(self):
        """Handles the Cancel button click (rejected signal)."""
        self.reject()  # This closes the dialog without changes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModifyLogWindow("2")
    sys.exit(app.exec())
