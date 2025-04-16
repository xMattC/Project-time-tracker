from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QFontDialog, QColorDialog
import sys
from main_window import Ui_MainWindow
from tracker import core, reports
from tracker.storage import init_db


class ProjectTrackerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        init_db()  # Initialise the database

        self.button_clock_in.clicked.connect(self.clock_in)
        self.button_clock_out.clicked.connect(self.clock_out)
        self.button_sessions.clicked.connect(self.sessions)
        self.button_report.clicked.connect(self.report)
        self.button_status.clicked.connect(self.status)
        # self.label_print_out.clicked.connect(self.)

        # Print stats on init:
        self.label_print_out.setText(core.status())

    def clock_in(self, project: str):
        message = core.clock_in(project)
        self.label_print_out.setText(str(message))

    def clock_out(self):
        message = core.clock_out()
        self.label_print_out.setText(str(message))

    def status(self):
        message = core.status()
        self.label_print_out.setText(str(message))

    def report(self):
        message = reports.generate_report()
        self.label_print_out.setText(str(message))

    def sessions(self):
        message = reports.list_sessions()
        self.label_print_out.setText(str(message))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectTrackerWindow()
    sys.exit(app.exec())
