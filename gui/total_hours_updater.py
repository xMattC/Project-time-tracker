from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
from datetime import datetime


class ReportTableUpdater:
    """Class for updating a table with project report data."""

    def __init__(self, table_widget):
        """Initialize the updater with a table widget."""
        self.table_widget = table_widget
        self.original_report_data = []  # To store the original order of the data

    def update_table(self, report_data):
        """Updates the table with sorted project report data."""
        self.original_report_data = report_data  # Save the original order
        sorted_report = sorted(
            report_data,
            key=lambda x: datetime.strptime(x["latest_clock_out"], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )

        self.populate_table(sorted_report)

    def populate_table(self, report_data):
        """Populates the table with the given report data."""
        self.table_widget.setRowCount(len(report_data))  # Set the number of rows based on report data
        self.table_widget.setColumnCount(2)  # Set the number of columns
        self.table_widget.setHorizontalHeaderLabels(["Project", "Duration"])  # Column headers
        self.table_widget.setSortingEnabled(False)  # Disable sorting while populating

        for row_index, entry in enumerate(report_data):
            project_item = QTableWidgetItem(entry["project_name"])  # Create table item for project name
            duration_str = entry["duration"]
            duration_item = QTableWidgetItem(duration_str)  # Create table item for duration

            # Extract hours and minutes for sorting
            try:
                hours, minutes = 0, 0
                parts = duration_str.split("h")  # Split by hours (if any)
                if len(parts) >= 1:
                    hours = int(parts[0].strip())  # Extract hours
                if len(parts) == 2:
                    minutes = int(parts[1].replace("m", "").strip())  # Extract minutes
                total_minutes = hours * 60 + minutes  # Convert to total minutes for sorting
            except:
                total_minutes = 0  # If there's an error, set total minutes to 0

            # Use Qt.ItemDataRole.UserRole to store sortable value (total minutes)
            duration_item.setData(Qt.ItemDataRole.UserRole, total_minutes)

            # Add project name and duration items to the table
            self.table_widget.setItem(row_index, 0, project_item)
            self.table_widget.setItem(row_index, 1, duration_item)

        # Enable sorting after all rows are populated
        self.table_widget.setSortingEnabled(True)
