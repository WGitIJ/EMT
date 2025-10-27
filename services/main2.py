import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QScrollArea, QGridLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

class BusArrivalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bus Arrival Time App")
        self.setMinimumSize(600, 400)

        # Store recently checked stops
        self.recent_stops = []

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Input section: Stop number field and button
        input_layout = QHBoxLayout()
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("Enter stop number")
        self.check_button = QPushButton("Check Stop")
        self.check_button.clicked.connect(self.check_stop)
        input_layout.addWidget(self.stop_input)
        input_layout.addWidget(self.check_button)
        main_layout.addLayout(input_layout)

        # Recent stops grid
        self.recent_stops_widget = QWidget()
        self.recent_stops_layout = QGridLayout(self.recent_stops_widget)
        main_layout.addWidget(self.recent_stops_widget)

        # Data retrieval time label
        self.time_label = QLabel("Last updated: Not yet retrieved")
        main_layout.addWidget(self.time_label)

        # Scroll area for bus arrival data
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

    def check_stop(self):
        stop_number = self.stop_input.text().strip()
        if not stop_number.isdigit():
            self.show_warning("Invalid input", "Please enter a valid stop number.")
            return

        # Fetch data (placeholder for actual API call)
        data = self.fetch_bus_data(stop_number)
        if not data:
            self.show_warning("Error", "No data available or server is down.")
            return

        # Update time label
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"Last updated: {current_time}")

        # Update scroll area with arrival data
        self.update_arrival_display(data)

        # Add to recent stops if not already present
        if stop_number not in self.recent_stops:
            self.recent_stops.append(stop_number)
            self.update_recent_stops()

    def fetch_bus_data(self, stop_number):
        # Placeholder for API request (replace with actual EMT API call)
        try:
            # Example: requests.get(f"https://api.emtmadrid.es/stop/{stop_number}")
            # This is a mock response; replace with actual API logic
            response = {
                "lines": [
                    {"line": "27", "color": "#FF0000", "arrival_time": "5 min"},
                    {"line": "34", "color": "#00FF00", "arrival_time": "10 min"},
                    {"line": "45", "color": "#0000FF", "arrival_time": "15 min"}
                ]
            }
            return response
        except requests.RequestException:
            return None

    def update_arrival_display(self, data):
        # Clear previous content
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # Add new arrival data
        for item in data.get("lines", []):
            line_label = QLabel(f"Line {item['line']} ({item['arrival_time']})")
            line_label.setStyleSheet(f"color: {item['color']}; font-size: 14px;")
            self.scroll_layout.addWidget(line_label)
        self.scroll_layout.addStretch()

    def update_recent_stops(self):
        # Clear previous buttons
        for i in reversed(range(self.recent_stops_layout.count())):
            self.recent_stops_layout.itemAt(i).widget().setParent(None)

        # Add buttons for recent stops (2 per row)
        for i, stop in enumerate(self.recent_stops):
            button = QPushButton(f"Stop {stop}")
            button.clicked.connect(lambda _, s=stop: self.recheck_stop(s))
            self.recent_stops_layout.addWidget(button, i // 2, i % 2)
        self.recent_stops_widget.adjustSize()

    def recheck_stop(self, stop_number):
        self.stop_input.setText(stop_number)
        self.check_stop()

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message, QMessageBox.StandardButton.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BusArrivalApp()
    window.show()
    sys.exit(app.exec())