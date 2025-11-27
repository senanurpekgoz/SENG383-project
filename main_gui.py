import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QWidget
)
from PyQt5.QtGui import QColor
from scheduler import generate_schedule  # Import your scheduling logic


class BeePlanGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_data()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("BeePlan - Schedule Generator")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Buttons
        self.add_buttons()

        # Table Widget
        self.schedule_table = QTableWidget()
        self.layout.addWidget(self.schedule_table)

    def add_buttons(self):
        """Add buttons to the layout."""
        self.load_data_button = self.create_button("Load Data", self.load_data)
        self.generate_schedule_button = self.create_button("Generate Schedule", self.generate_schedule)

    def create_button(self, text, callback):
        """Helper to create and add a button."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button

    def init_data(self):
        """Initialize data containers."""
        self.courses = []
        self.rooms = []
        self.time_slots = []

    def load_data(self):
        """Load data from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if not file_name:
            return

        try:
            with open(file_name, 'r') as file:
                data = json.load(file)

            self.courses = data.get("courses", [])
            self.rooms = data.get("rooms", [])
            self.time_slots = data.get("time_slots", [])

            QMessageBox.information(self, "Success", "Data loaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")

    def generate_schedule(self):
        """Generate and display the schedule."""
        if not self.validate_data():
            return

        try:
            schedule = generate_schedule(self.courses, self.rooms, self.time_slots)
            self.populate_table(schedule)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate schedule: {e}")

    def validate_data(self):
        """Validate that the required data is loaded."""
        if not self.courses or not self.rooms or not self.time_slots:
            QMessageBox.warning(self, "Warning", "Please load valid data before generating the schedule.")
            return False
        return True

    def populate_table(self, schedule):
        """Populate the table widget with the generated schedule."""
        self.schedule_table.clear()

        days, hours = self.get_schedule_dimensions(schedule)
        self.setup_table_headers(days, hours)

        for (day, hour), entries in schedule.items():
            self.add_schedule_entry(day, hour, entries, days, hours)

    def get_schedule_dimensions(self, schedule):
        """Extract unique days and hours from the schedule."""
        days = sorted(set(day for day, _ in schedule.keys()))
        hours = sorted(set(hour for _, hour in schedule.keys()))
        return days, hours

    def setup_table_headers(self, days, hours):
        """Set up table headers."""
        self.schedule_table.setRowCount(len(hours))
        self.schedule_table.setColumnCount(len(days))
        self.schedule_table.setHorizontalHeaderLabels(days)
        self.schedule_table.setVerticalHeaderLabels([str(hour) for hour in hours])

    def add_schedule_entry(self, day, hour, entries, days, hours):
        """Add a single schedule entry to the table."""
        row = hours.index(hour)
        col = days.index(day)
        cell_text = "\n".join([f"{course['name']} ({room})" for course, room in entries])
        cell_item = QTableWidgetItem(cell_text)

        if len(entries) > 1:  # Conflict if more than one entry in the same slot
            cell_item.setBackground(QColor(255, 0, 0))  # Red background for conflicts

        self.schedule_table.setItem(row, col, cell_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeePlanGUI()
    window.show()
    sys.exit(app.exec_())