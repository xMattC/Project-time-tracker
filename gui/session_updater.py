from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor
from datetime import datetime


class SessionTableUpdater:
    def __init__(self, table_widget):
        self.table_widget = table_widget

    def update_sessions_table(self, result):
        sessions = result["sessions"]
        self.table_widget.setRowCount(len(sessions))
        self.table_widget.setColumnCount(5)  # Now 5 columns, including hidden ID

        # Set headers
        self.table_widget.setHorizontalHeaderLabels(["Project", "Clock In", "Clock Out", "Duration", "ID"])

        for row_index, session in enumerate(sessions):
            # Parse Clock In
            try:
                clock_in = datetime.strptime(session["clock_in"], '%Y-%m-%d %H:%M:%S')
                formatted_clock_in = clock_in.strftime('%H:%M %d %b %y')
            except ValueError:
                formatted_clock_in = "Invalid Date"
                clock_in = None

            # Parse Clock Out
            clock_out = session["clock_out"]
            formatted_clock_out = ""
            if clock_out and clock_out != '—':
                try:
                    clock_out = datetime.strptime(clock_out, '%Y-%m-%d %H:%M:%S')
                    formatted_clock_out = clock_out.strftime('%H:%M %d %b %y')
                except ValueError:
                    formatted_clock_out = "Invalid Date"
                    clock_out = None

            # Calculate Duration
            duration = ""
            if clock_in and clock_out and isinstance(clock_in, datetime) and isinstance(clock_out, datetime):
                time_diff = clock_out - clock_in
                hours, remainder = divmod(time_diff.seconds, 3600)
                minutes = remainder // 60
                duration = f"{hours}h {minutes}m"
            elif clock_in and not clock_out:
                duration = "Ongoing"
            else:
                duration = "TBD"

            # Add items to table
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(session["project_name"]))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(formatted_clock_in))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(formatted_clock_out))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(duration))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(str(session["id"])))  # ID as string

            # Highlight ongoing sessions
            if not clock_out or clock_out == '—':
                for col_index in range(4):  # Only highlight visible columns
                    item = self.table_widget.item(row_index, col_index)
                    if item:
                        item.setBackground(QColor(0, 255, 0))  # Bright green

        # Hide the ID column (index 4)
        self.table_widget.setColumnHidden(4, True)


class SessionTableManager:
    def __init__(self, table_widget: QTableWidget, id_column: int = 4):
        self.table_widget = table_widget
        self.id_column = id_column

    def get_selected_session_ids(self):
        """
        Collects the session IDs for the selected rows in the table.
        """
        selected_rows = self.table_widget.selectionModel().selectedRows()
        session_ids = []
        for model_index in selected_rows:
            row = model_index.row()
            item = self.table_widget.item(row, self.id_column)
            if item:
                session_ids.append(item.text())
        return session_ids

    def clear_table(self):
        """Clears all rows in the table widget."""
        self.table_widget.setRowCount(0)
