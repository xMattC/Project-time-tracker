import sys

from PyQt6.QtCore import QDate, QTime, pyqtSignal
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox

from gui.ui_files.ui_mod_log_window import Ui_ModifyLogWindow
from tracker.storage import get_session_by_id, init_db
from tracker.core import amend_db_session
from gui.calendar_window import CalendarWindow
from PyQt6.QtGui import QIcon

class ModifyLogWindow(QDialog, Ui_ModifyLogWindow):
    """Dialog for modifying log session details."""

    # Signal emitted when a session is updated
    session_updated = pyqtSignal()

    def __init__(self):
        """Initialize the window, set up UI and database."""
        super().__init__()
        self.setupUi(self)  # Set up the UI
        init_db()  # Initialize the database
        self.session_id = None  # Will be set later
        self.dateEdit_clock_in.setDisplayFormat('dd MMM yy')
        self.dateEdit_clock_out.setDisplayFormat('dd MMM yy')
        self.setWindowTitle("Edit Log")
        self.setWindowIcon(QIcon('images/logo.png'))
        self.calendar_window = None  # Keeps a persistent reference

        # Connect buttons to their actions
        self.buttonBox.accepted.connect(self.accept_action)
        self.buttonBox.rejected.connect(self.reject_action)

        # Connect calendar button (clock-in) to open calendar window
        self.pushButton_calendar_clock_in.clicked.connect(self.calendar_clock_in_time)
        self.pushButton_calendar_clock_out.clicked.connect(self.calendar_clock_out_time)

    def load_session(self, session_id):
        """Load session data into UI for editing."""
        self.session_id = session_id
        session_data = get_session_by_id(session_id)

        if not session_data:
            print(f"No session found with ID: {session_id}")
            return

        self.set_default_time(self.dateEdit_clock_in, self.timeEdit_clock_in, session_data['clock_in'])
        self.set_default_time(self.dateEdit_clock_out, self.timeEdit_clock_out, session_data['clock_out'])

    @staticmethod
    def set_default_time(date_widget, time_widget, timestamp):
        """Sets the default date and time from a timestamp string."""
        date, time = timestamp.split(' ')
        hours, minutes, seconds = map(int, time[:8].split(':'))
        date_widget.setDate(QDate.fromString(date, 'yyyy-MM-dd'))
        time_widget.setTime(QTime(hours, minutes, seconds))

    def get_clock_in_time(self) -> str:
        """Return clock-in date and time as 'YYYY-MM-DD HH:MM:SS'."""
        date = self.dateEdit_clock_in.date().toString("yyyy-MM-dd")
        time = self.timeEdit_clock_in.time().toString("HH:mm:ss")
        return f"{date} {time}"

    def get_clock_out_time(self) -> str:
        """Return clock-out date and time as 'YYYY-MM-DD HH:MM:SS'."""
        date = self.dateEdit_clock_out.date().toString("yyyy-MM-dd")
        time = self.timeEdit_clock_out.time().toString("HH:mm:ss")
        return f"{date} {time}"

    def calendar_clock_in_time(self):
        """Open calendar window for selecting clock-in date."""
        self.calendar_window_in = CalendarWindow()
        self.calendar_window_in.date_selected.connect(self.set_clock_in_date)
        self.calendar_window_in.exec()

    def calendar_clock_out_time(self):
        """Open calendar window for selecting clock-out date."""
        self.calendar_window_out = CalendarWindow()
        self.calendar_window_out.date_selected.connect(self.set_clock_out_date)
        self.calendar_window_out.exec()

    def set_clock_in_date(self, date):
        """Set selected clock-in date in the date edit field."""
        self.dateEdit_clock_in.setDate(date)

    def set_clock_out_date(self, date):
        """Set selected clock-out date in the date edit field."""
        self.dateEdit_clock_out.setDate(date)

    def accept_action(self):
        """Validate inputs, update session, and close the dialog."""
        try:
            clock_in = self.get_clock_in_time()
            clock_out = self.get_clock_out_time()

            if clock_in >= clock_out:
                QMessageBox.warning(self, "Invalid Time", "Clock-in must be before clock-out.")
                return

            amend_db_session(self.session_id, "clock_in", clock_in)
            amend_db_session(self.session_id, "clock_out", clock_out)
            self.session_updated.emit()  # Emit the session updated signal
            self.accept()  # Close the dialog
        except Exception as e:
            print(f"Failed to update session {self.session_id}: {e}")
            QMessageBox.critical(self, "Error", "Failed to update the session. Please try again.")

    def reject_action(self):
        """Close the dialog without saving changes."""
        self.reject()  # Close the dialog without saving changes
