from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QScrollArea,
    QGridLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from datetime import datetime
from services.emt_service import EMTService
from services.database_service import DatabaseService

class BusArrivalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.emt_service = EMTService()
        self.db_service = DatabaseService()
        self.recent_stops = []
        self.init_ui()
        self.load_recent_stops()

    def init_ui(self):
        self.setWindowTitle("Bus Arrival Time")
        self.setMinimumSize(600, 500)
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        input_label = QLabel("Stop Number:")
        input_label.setFont(QFont("Arial", 10))
        input_layout.addWidget(input_label)

        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("Enter stop number...")
        self.stop_input.setFont(QFont("Arial", 10))
        self.stop_input.returnPressed.connect(self.search_stop)
        input_layout.addWidget(self.stop_input, 1)

        self.search_button = QPushButton("Search")
        self.search_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.search_button.setMinimumWidth(100)
        self.search_button.clicked.connect(self.search_stop)
        input_layout.addWidget(self.search_button)

        main_layout.addLayout(input_layout)

        recent_label = QLabel("Recent Stops:")
        recent_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        main_layout.addWidget(recent_label)

        self.recent_stops_widget = QWidget()
        self.recent_stops_layout = QGridLayout(self.recent_stops_widget)
        self.recent_stops_layout.setSpacing(8)
        main_layout.addWidget(self.recent_stops_widget)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        self.time_label = QLabel("Last updated: --")
        self.time_label.setFont(QFont("Arial", 9))
        self.time_label.setStyleSheet("color: #666;")
        main_layout.addWidget(self.time_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(200)

        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.results_layout.setSpacing(10)

        self.scroll_area.setWidget(self.results_widget)
        main_layout.addWidget(self.scroll_area, 1)

    def load_recent_stops(self):
        self.recent_stops = self.db_service.get_recent_stops()
        self.update_recent_stops_grid()

    def update_recent_stops_grid(self):
        while self.recent_stops_layout.count():
            child = self.recent_stops_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        max_cols = 5
        for index, stop in enumerate(self.recent_stops[:10]):
            row = index // max_cols
            col = index % max_cols

            button = QPushButton(str(stop))
            button.setMinimumWidth(80)
            button.setFont(QFont("Arial", 9))
            button.clicked.connect(lambda checked, s=stop: self.search_recent_stop(s))
            self.recent_stops_layout.addWidget(button, row, col)

    def search_recent_stop(self, stop_number):
        self.stop_input.setText(str(stop_number))
        self.search_stop()

    def search_stop(self):
        stop_number = self.stop_input.text().strip()

        if not stop_number:
            QMessageBox.warning(self, "Invalid Input", "Please enter a stop number.")
            return

        if not stop_number.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Stop number must be numeric.")
            return

        self.search_button.setEnabled(False)
        self.search_button.setText("Loading...")

        QTimer.singleShot(0, lambda: self.fetch_bus_data(stop_number))

    def fetch_bus_data(self, stop_number):
        try:
            data = self.emt_service.get_arrivals(stop_number)

            if not data or 'arrivals' not in data or not data['arrivals']:
                QMessageBox.information(self, "No Data", f"No arrival data available for stop {stop_number}.")
                self.search_button.setEnabled(True)
                self.search_button.setText("Search")
                return

            self.db_service.save_recent_stop(int(stop_number))
            self.load_recent_stops()

            self.display_results(data)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.setText(f"Last updated: {now}")

        except ConnectionError as e:
            QMessageBox.critical(self, "Connection Error", f"Could not connect to EMT service:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
        finally:
            self.search_button.setEnabled(True)
            self.search_button.setText("Search")

    def display_results(self, data):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        arrivals = data.get('arrivals', [])

        for arrival in arrivals:
            arrival_widget = self.create_arrival_widget(arrival)
            self.results_layout.addWidget(arrival_widget)

    def create_arrival_widget(self, arrival):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("QFrame { background-color: #f5f5f5; border-radius: 5px; padding: 10px; }")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)

        line_number = arrival.get('line', 'N/A')
        line_color = arrival.get('color', '#000000')

        line_label = QLabel(line_number)
        line_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        line_label.setStyleSheet(f"background-color: {line_color}; color: white; padding: 8px 12px; border-radius: 4px;")
        line_label.setFixedWidth(60)
        line_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(line_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        destination = arrival.get('destination', 'Unknown')
        destination_label = QLabel(f"Destination: {destination}")
        destination_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        info_layout.addWidget(destination_label)

        arrival_time = arrival.get('time', 'N/A')
        time_label = QLabel(f"Arrival: {arrival_time}")
        time_label.setFont(QFont("Arial", 10))
        info_layout.addWidget(time_label)

        layout.addLayout(info_layout, 1)

        return frame
