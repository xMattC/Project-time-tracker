from datetime import datetime

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem


class SessionTableUpdater:
    def __init__(self, table_widget):
        self.table_widget = table_widget

    def update_sessions_table(self, result):
        # Set the number of columns to 4 (including the new time difference column)
        self.table_widget.setRowCount(len(result["sessions"]))
        self.table_widget.setColumnCount(4)  # Now 4 columns
        self.table_widget.setHorizontalHeaderLabels(["Project", "Clock In", "Clock Out", "Duration"])

        for row_index, session in enumerate(result["sessions"]):
            # Convert clock_in to datetime, and format it for display
            try:
                clock_in = datetime.strptime(session["clock_in"], '%Y-%m-%d %H:%M:%S')
                formatted_clock_in = clock_in.strftime('%H:%M %d %b %y')  # Format: 16:35 10 Jan 23
            except ValueError:
                formatted_clock_in = "Invalid Date"
                clock_in = None  # Set to None if invalid format

            # Convert clock_out to datetime, and format it for display
            clock_out = session["clock_out"]
            formatted_clock_out = ""
            if clock_out and clock_out != '—':  # Only process if clock_out is not None or '—'
                try:
                    clock_out = datetime.strptime(clock_out, '%Y-%m-%d %H:%M:%S')
                    formatted_clock_out = clock_out.strftime('%H:%M %d %b %y')  # Format: 16:35 10 Jan 23
                except ValueError:
                    formatted_clock_out = "Invalid Date"
                    clock_out = None  # Set to None if invalid format

            # Calculate time difference (if both clock_in and clock_out are valid datetime objects)
            duration = ""
            if clock_in and clock_out:
                # Ensure both clock_in and clock_out are datetime objects before subtracting
                if isinstance(clock_in, datetime) and isinstance(clock_out, datetime):
                    time_diff = clock_out - clock_in  # Now we can safely subtract datetime objects
                    hours, remainder = divmod(time_diff.seconds, 3600)
                    minutes = remainder // 60
                    duration = f"{hours}h {minutes}m"
                else:
                    duration = "TBD"
            elif clock_in and not clock_out:
                duration = "Ongoing"  # If clock_in is present but no clock_out

            # Set formatted values in the table (4 columns now)
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(session["project_name"]))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(formatted_clock_in))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(formatted_clock_out))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(duration))  # Set duration in 4th column

            # Change the row color to green if the "Clock Out" box is empty (ongoing session)
            if not clock_out or clock_out == '—':
                for col_index in range(4):
                    item = self.table_widget.item(row_index, col_index)
                    if item:
                        item.setBackground(QColor(0, 255, 0))  # Green background
