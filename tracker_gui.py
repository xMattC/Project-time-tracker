from gui.app import ProjectTrackerWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectTrackerWindow()
    sys.exit(app.exec())

