from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QDate, pyqtSignal

from gui.ui_files.ui_calendar_window import Ui_CalendarWindow
from tracker.storage import init_db


class CalendarWindow(QDialog, Ui_CalendarWindow):
    """
    A dialog window that allows the user to select a date from a calendar widget.
    Emits the selected date back to the parent window.
    """

    # Signal to emit the selected date back to the parent window
    date_selected = pyqtSignal(QDate)

    def __init__(self):
        """Initializes the CalendarWindow and sets up the UI and database."""
        super().__init__()  # Initialize the base class (QDialog)
        self.setupUi(self)  # Set up the UI components from the .ui file
        init_db()  # Initialize the database

        # Connect the 'accepted' signal of the buttonBox to emit the selected date
        self.buttonBox.accepted.connect(self.emit_selected_date)
        # Connect the 'rejected' signal of the buttonBox to close the dialog
        self.buttonBox.rejected.connect(self.reject)

    def emit_selected_date(self):
        """
        Emits the currently selected date to the parent window when the user clicks 'OK' or 'Accept'.
        Closes the dialog after emitting the date.
        """
        date = self.calendarWidget.selectedDate()  # Get the selected date from the calendar widget
        self.date_selected.emit(date)  # Emit the selected date using the date_selected signal
        self.accept()  # Accept the dialog (close it)
