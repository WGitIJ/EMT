from PyQt6.QtWidgets import QPushButton, QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QDateTime
from model.model_window import EMTApi  # ← CORREGIDO: nombre del archivo correcto


class BusController:

    def __init__(self, view):
        self.view = view
        self.model = EMTApi()
        self.recent_stops = []  # historial interno de paradas
        self.setup_connections()

    # ================================================================
    # Conexión de señales
    # ================================================================
    def setup_connections(self):
        self.view.checkButton.clicked.connect(self.on_check_stop)
        self.view.stopLineEdit.returnPressed.connect(self.on_check_stop)

    # ================================================================
    # Lógica principal: consultar parada
    # ================================================================
    def on_check_stop(self):
        stop_text = self.view.stopLineEdit.text().strip()
        if not stop_text.isdigit():
            self.show_message("Error", "Introduce un número de parada válido.", QMessageBox.Icon.Warning)
            return

        stop_id = int(stop_text)
        self.add_recent(stop_id)

        self.view.timeLabel.setText("Consultando datos...")
        arrivals = self.model.get_arrivals(stop_id)

        # Manejo de errores
        if arrivals == "no_internet":
            self.show_message("Error", "No se pudo conectar con el servidor.", QMessageBox.Icon.Critical)
            self.view.timeLabel.setText("Última actualización: -")
            return
        elif arrivals == "invalid_stop":
            self.show_message("Aviso", f"No se encontraron datos para la parada {stop_id}.", QMessageBox.Icon.Warning)
            self.view.timeLabel.setText("Última actualización: -")
            return
        elif arrivals == "token_expired":
            self.show_message("Error", "Token caducado. Necesitas actualizarlo en el modelo.", QMessageBox.Icon.Critical)
            self.view.timeLabel.setText("Última actualización: -")
            return

        # Mostrar resultados
        self.display_arrivals(arrivals)
        now = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.view.timeLabel.setText(f"Última actualización: {now}")

    # ================================================================
    # Historial de paradas
    # ================================================================
    def add_recent(self, stop):
        if stop in self.recent_stops:
            self.recent_stops.remove(stop)
        self.recent_stops.insert(0, stop)
        self.recent_stops = self.recent_stops[:6]
        self.update_grid()

    def update_grid(self):
        layout = self.view.recentStopsLayout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for i, stop in enumerate(self.recent_stops):
            button = QPushButton(str(stop))
            button.clicked.connect(lambda _, s=stop: self.load_recent_stop(s))
            row, col = divmod(i, 3)
            layout.addWidget(button, row, col)

    def load_recent_stop(self, stop):
        self.view.stopLineEdit.setText(str(stop))
        self.on_check_stop()

    # ================================================================
    # Mostrar resultados en el scroll
    # ================================================================
    def display_arrivals(self, arrivals):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(8)

        for bus in arrivals:
            # Número de línea con su color
            line_label = QLabel(f"<b>Línea {bus['line']}</b>")
            line_label.setStyleSheet(f"color: {bus['color']}; font-size: 18px; font-weight: bold;")

            # Destino y tiempo con estilo neutro
            dest_label = QLabel(f"{bus['dest']}")
            dest_label.setStyleSheet("font-size: 14px; color: #555;")

            time_label = QLabel(f"{bus['time']}")
            time_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #d32f2f;")

            # Agrupación en bloque
            block = QWidget()
            block_layout = QVBoxLayout(block)
            block_layout.addWidget(line_label)
            block_layout.addWidget(dest_label)
            block_layout.addWidget(time_label)
            block_layout.setContentsMargins(12, 8, 12, 8)

            layout.addWidget(block)

        # Limpiar scroll anterior
        old_widget = self.view.scrollArea.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        self.view.scrollArea.setWidget(container)



    # ================================================================
    # Utilidad: mensajes de error / aviso
    # ================================================================
    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.exec()