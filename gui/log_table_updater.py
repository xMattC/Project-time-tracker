from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt6.QtGui import QColor
from datetime import datetime

# Constants to control column indexing
VISIBLE_COLUMNS = 4  # Number of visible columns (excluding hidden ID)
TOTAL_COLUMNS = 5  # Total number of columns including hidden ID column
ID_COLUMN_INDEX = 4  # Index of the hidden ID column


class LogTableUpdater:
    """
    Updates a QTableWidget with session data.
    """

    def __init__(self, table_widget: QTableWidget):
        """
        param table_widget: The QTableWidget instance to be updated.
        """
        self.table_widget = table_widget

    @staticmethod
    def _parse_datetime(value: str):
        """
        Parses a datetime string and returns both the datetime object and a human-readable string.

        param value: A datetime string in format '%Y-%m-%d %H:%M:%S'.
        return: Tuple (datetime object or None, formatted string or "Invalid Date")
        """
        try:
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return dt, dt.strftime('%H:%M %d %b %y')
        except ValueError:
            return None, "Invalid Date"

    def update_sessions_table(self, result: dict):
        """
        Populates the QTableWidget with session data from the result dictionary.

        param result: A dictionary containing session data under the key "sessions".
        """
        sessions = result["sessions"]
        self.table_widget.setRowCount(len(sessions))
        self.table_widget.setColumnCount(TOTAL_COLUMNS)

        # Set column headers
        self.table_widget.setHorizontalHeaderLabels(["Project", "Clock In", "Clock Out", "Duration", "ID"])

        for row_index, session in enumerate(sessions):

            # format clock-in data:
            clock_in, formatted_clock_in = self._parse_datetime(session["clock_in"])

            # format clock-out data
            raw_clock_out = session["clock_out"]
            if raw_clock_out and raw_clock_out != '—':
                clock_out, formatted_clock_out = self._parse_datetime(raw_clock_out)
            else:
                clock_out, formatted_clock_out = None, ""

            # calculate and format session total time:
            if clock_in and clock_out:
                time_diff = clock_out - clock_in
                hours, remainder = divmod(time_diff.seconds, 3600)
                minutes = remainder // 60
                duration = f"{hours}h {minutes}m"
            elif clock_in:
                duration = "Ongoing"
            else:
                duration = "TBD"

            # update table row by column item by column item:
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(session["project_name"]))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(formatted_clock_in))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(formatted_clock_out))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(duration))
            self.table_widget.setItem(row_index, ID_COLUMN_INDEX, QTableWidgetItem(str(session["id"])))

            # highlight current session row green if clocked-in:
            if not clock_out:
                for col_index in range(VISIBLE_COLUMNS):
                    item = self.table_widget.item(row_index, col_index)
                    if item:
                        item.setBackground(QColor(0, 255, 0))  # Bright green

        self.table_widget.setColumnHidden(ID_COLUMN_INDEX, True)


class LogTableManager:
    """
    Manages interaction with a QTableWidget for displaying and selecting session logs.
    """

    def __init__(self, table_widget: QTableWidget, id_column: int = ID_COLUMN_INDEX):
        """
        Initializes the manager with a reference to a QTableWidget.

        param table_widget: The QTableWidget instance to manage.
        param id_column: The column index containing session IDs.
        """
        self.table_widget = table_widget
        self.id_column = id_column

    def get_selected_session_ids(self) -> list[str]:
        """
        Returns a list of session IDs for the currently selected rows.

        return: A list of strings representing the selected session IDs.
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
        """ Removes all rows from the QTableWidget.

        return: None
        """
        self.table_widget.setRowCount(0)
