import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QScrollArea,
    QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, QDateTime


class BusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bus Arrival Time App")
        self.resize(600, 500)

        # --- Widgets principales ---
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("Introduce número de parada...")
        self.check_button = QPushButton("Consultar")

        self.check_button.clicked.connect(self.check_stop)

        # --- Layout superior: entrada + botón ---
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.stop_input)
        input_layout.addWidget(self.check_button)

        # --- Grid dinámico de paradas recientes ---
        self.recent_grid = QGridLayout()
        self.recent_stops = []

        # --- Label con la hora ---
        self.time_label = QLabel("Datos no actualizados")

        # --- ScrollArea para mostrar resultados ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        # --- Layout principal ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(self.recent_grid)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # --- Función principal: comprobar parada ---
    def check_stop(self):
        stop_number = self.stop_input.text().strip()

        if not stop_number.isdigit():
            QMessageBox.warning(self, "Error", "El número de parada no es válido.")
            return

        # Simulación de datos (en vez de llamada a API real)
        data = self.fake_api_request(stop_number)

        if not data:
            QMessageBox.information(self, "Sin datos", "No hay datos disponibles para esta parada.")
            return

        # Mostrar datos
        self.display_data(data)

        # Actualizar hora
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss dd/MM/yyyy")
        self.time_label.setText(f"Última actualización: {current_time}")

        # Añadir a paradas recientes
        self.add_recent_stop(stop_number)

    # --- Muestra los datos obtenidos ---
    def display_data(self, data):
        # Limpiar contenido anterior
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for line_info in data:
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.StyledPanel)
            layout = QHBoxLayout(frame)

            line_label = QLabel(f"🚌 Línea {line_info['line']}")
            line_label.setStyleSheet(f"color: {line_info['color']}; font-weight: bold;")
            time_label = QLabel(f"Llegada en {line_info['time']} min")

            layout.addWidget(line_label)
            layout.addWidget(time_label)
            layout.addStretch()

            self.scroll_layout.addWidget(frame)

    # --- Simula una consulta a la API ---
    def fake_api_request(self, stop_number):
        # Simulación de datos
        sample_data = {
            "1234": [
                {"line": "27", "time": 3, "color": "blue"},
                {"line": "45", "time": 8, "color": "red"},
            ],
            "5678": [
                {"line": "150", "time": 2, "color": "green"},
                {"line": "52", "time": 10, "color": "orange"},
            ],
        }
        return sample_data.get(stop_number, [])

    # --- Añadir botón de parada reciente ---
    def add_recent_stop(self, stop_number):
        if stop_number in self.recent_stops:
            return
        self.recent_stops.append(stop_number)
        row = len(self.recent_stops) // 4
        col = len(self.recent_stops) % 4

        btn = QPushButton(stop_number)
        btn.clicked.connect(lambda _, n=stop_number: self.quick_check(n))
        self.recent_grid.addWidget(btn, row, col)

    # --- Consulta rápida desde botón ---
    def quick_check(self, stop_number):
        self.stop_input.setText(stop_number)
        self.check_stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BusApp()
    window.show()
    sys.exit(app.exec())
 
