from PyQt6.QtWidgets import QPushButton, QMessageBox, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QDateTime
from model.model_window import EMTApi  # ← CORREGIDO: nombre del archivo correcto


class BusController:

    def __init__(self, view):
        self.view = view
        self.model = EMTApi()
        self.recent_stops = []  # historial interno de paradas
        self.setup_connections()
        self.setup_lines_tab()

    # ================================================================
    # Conexión de señales
    # ================================================================
    def setup_connections(self):
        self.view.checkButton.clicked.connect(self.on_check_stop)
        self.view.stopLineEdit.returnPressed.connect(self.on_check_stop)

    # ================================================================
    # Pestaña "Consulta por lineas": cargar todas las paradas
    # ================================================================
    def setup_lines_tab(self):
        # Comprobamos que existen los widgets del tab de líneas
        if not hasattr(self.view, "scrollArea_2"):
            return

        stops = self.model.get_all_stops()

        if stops == "token_expired":
            self.show_message(
                "Token caducado",
                "No se puede cargar el listado de paradas porque el token ha caducado.\n"
                "Actualiza el token en el modelo.",
                QMessageBox.Icon.Warning,
            )
            return

        if stops == "no_internet":
            # No saturamos al usuario con más mensajes si ya hay problemas de red,
            # simplemente dejamos la pestaña vacía.
            return

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)

        for stop in stops:
            # Crear un widget horizontal para cada línea con estilo mejorado - Tema oscuro
            stop_widget = QWidget()
            stop_widget.setStyleSheet("""
                QWidget {
                    background-color: #3a3a3a;
                    border-radius: 8px;
                    padding: 5px;
                }
            """)
            stop_layout = QHBoxLayout(stop_widget)
            stop_layout.setContentsMargins(12, 10, 12, 10)
            stop_layout.setSpacing(12)
            
            # Botón circular con el número de la línea mejorado
            color = stop.get('color', '#757575')  # Color por defecto gris
            circle_button = QPushButton(str(stop['id']))
            circle_button.setFixedSize(50, 50)  # Tamaño más grande
            # Estilo del botón circular mejorado con sombra
            circle_button.setStyleSheet(
                f"QPushButton {{"
                f"background-color: {color}; "
                f"color: white; "
                f"border-radius: 25px; "  # Círculo perfecto
                f"font-weight: bold; "
                f"font-size: 16px; "
                f"border: 3px solid #2d2d2d;"
                f"}}"
                f"QPushButton:hover {{"
                f"background-color: {color}; "
                f"border: 3px solid #555555;"
                f"transform: scale(1.05);"
                f"}}"
                f"QPushButton:pressed {{"
                f"background-color: {color}; "
                f"border: 3px solid #666666;"
                f"}}"
            )
            # Conectar el botón para mostrar las paradas de la línea
            # Usar stopId si está disponible, sino usar el código de la línea
            stop_id = stop.get('stopId', stop['id'])
            circle_button.clicked.connect(lambda checked, sid=stop_id: self.on_line_clicked(sid))
            stop_layout.addWidget(circle_button)
            
            # Nombre de la línea con estilo mejorado - Tema oscuro
            name_label = QLabel(stop['name'])
            name_label.setWordWrap(True)
            name_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #ffffff;
                    padding: 5px;
                    font-weight: 500;
                }
            """)
            stop_layout.addWidget(name_label)
            
            # Añadir el widget de la línea al layout principal
            layout.addWidget(stop_widget)

        old_widget = self.view.scrollArea_2.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        self.view.scrollArea_2.setWidget(container)

    # ================================================================
    # Manejo de clic en línea: mostrar paradas de la línea
    # ================================================================
    def on_line_clicked(self, stop_id: str):
        """Muestra las paradas de una línea en scrollArea_3"""
        print(f"[INFO] Clic en línea con stopId: {stop_id}")
        
        # Mostrar mensaje de carga
        loading_container = QWidget()
        loading_layout = QVBoxLayout(loading_container)
        loading_label = QLabel(f"Cargando paradas...")
        loading_label.setStyleSheet("font-size: 12px; color: #ffffff; padding: 10px;")
        loading_layout.addWidget(loading_label)
        
        old_widget = self.view.scrollArea_3.takeWidget()
        if old_widget:
            old_widget.deleteLater()
        self.view.scrollArea_3.setWidget(loading_container)
        
        # Obtener las paradas de la línea usando el stopId
        stops = self.model.get_line_stops(stop_id)

        # Manejo de errores
        if stops == "no_internet":
            self.show_message("Error", f"No se pudo conectar con el servidor.\nRevisa la consola para más detalles.", QMessageBox.Icon.Critical)
            # Mostrar mensaje de error en el scroll
            error_container = QWidget()
            error_layout = QVBoxLayout(error_container)
            error_label = QLabel("❌ Error al cargar paradas.\nNo se pudo conectar con el servidor.")
            error_label.setStyleSheet("""
                QLabel {
                    font-size: 13px; 
                    color: #e74c3c; 
                    padding: 15px;
                    background-color: #4a2a2a;
                    border-radius: 8px;
                }
            """)
            error_layout.addWidget(error_label)
            self.view.scrollArea_3.setWidget(error_container)
            return
        elif stops == "token_expired":
            self.show_message("Error", "Token caducado. Necesitas actualizarlo en el modelo.", QMessageBox.Icon.Critical)
            # Mostrar mensaje de error en el scroll
            error_container = QWidget()
            error_layout = QVBoxLayout(error_container)
            error_label = QLabel("⚠️ Error: Token caducado.\nActualiza el token en el modelo.")
            error_label.setStyleSheet("""
                QLabel {
                    font-size: 13px; 
                    color: #e74c3c; 
                    padding: 15px;
                    background-color: #4a2a2a;
                    border-radius: 8px;
                }
            """)
            error_layout.addWidget(error_label)
            self.view.scrollArea_3.setWidget(error_container)
            return

        # Crear contenedor para las paradas con estilo mejorado
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        if not stops:
            # Si no hay paradas, mostrar un mensaje con estilo mejorado - Tema oscuro
            no_stops_label = QLabel("No se encontraron paradas para esta línea.")
            no_stops_label.setStyleSheet("""
                QLabel {
                    font-size: 13px; 
                    color: #ffffff; 
                    padding: 15px;
                    background-color: #3a3a3a;
                    border-radius: 8px;
                }
            """)
            layout.addWidget(no_stops_label)
        else:
            # Mostrar cada parada con estilo mejorado - Tema oscuro
            for stop in stops:
                stop_widget = QWidget()
                stop_widget.setStyleSheet("""
                    QWidget {
                        background-color: #3a3a3a;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """)
                stop_layout = QHBoxLayout(stop_widget)
                stop_layout.setContentsMargins(12, 10, 12, 10)
                stop_layout.setSpacing(12)

                # Badge con el ID de la parada
                id_label = QLabel(f"#{stop['id']}")
                id_label.setStyleSheet("""
                    QLabel {
                        font-size: 12px;
                        font-weight: bold;
                        color: white;
                        background-color: #3498db;
                        padding: 6px 12px;
                        border-radius: 12px;
                        min-width: 50px;
                    }
                """)
                id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                stop_layout.addWidget(id_label)

                # Nombre de la parada con estilo mejorado - Tema oscuro
                stop_label = QLabel(stop['name'])
                stop_label.setWordWrap(True)
                stop_label.setStyleSheet("""
                    QLabel {
                        font-size: 13px;
                        color: #ffffff;
                        padding: 5px;
                        font-weight: 500;
                    }
                """)
                stop_layout.addWidget(stop_label)

                layout.addWidget(stop_widget)

        # Actualizar el scroll con las paradas
        self.view.scrollArea_3.setWidget(container)
        print(f"[INFO] Se mostraron {len(stops) if stops else 0} paradas")

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

        # Nombre descriptivo de la parada (si se puede obtener)
        stop_name = self.model.get_stop_name(stop_id)
        if stop_name:
            stop_info = f"Parada {stop_id} - {stop_name}"
        else:
            stop_info = f"Parada {stop_id}"

        self.view.timeLabel.setText(f"{stop_info} | Consultando datos...")
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
        self.view.timeLabel.setText(f"{stop_info} | Última actualización: {now}")

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
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 8px;
                    font-size: 12px;
                    font-weight: bold;
                    border: none;
                    border-radius: 6px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """)
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
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(25)
        layout.setContentsMargins(15, 15, 15, 15)

        for bus in arrivals:
            # Esfera circular con el número de línea y su color
            line_color = bus['color']
            line_number = bus['line']
            
            # Widget contenedor para la esfera
            sphere_container = QWidget()
            sphere_layout = QVBoxLayout(sphere_container)
            sphere_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sphere_layout.setSpacing(10)
            sphere_layout.setContentsMargins(0, 0, 0, 0)
            
            # Esfera circular grande con el número de línea
            sphere_label = QLabel(line_number)
            sphere_label.setFixedSize(120, 120)  # Tamaño grande para la esfera
            sphere_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    background-color: {line_color};
                    font-size: 48px;
                    font-weight: bold;
                    border-radius: 60px;
                    border: 4px solid #2d2d2d;
                }}
            """)
            sphere_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sphere_layout.addWidget(sphere_label)
            
            # Información debajo de la esfera - Texto blanco
            info_widget = QWidget()
            info_layout = QVBoxLayout(info_widget)
            info_layout.setSpacing(5)
            info_layout.setContentsMargins(0, 0, 0, 0)
            
            # Destino
            dest_label = QLabel(f"📍 {bus['dest']}")
            dest_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #ffffff;
                    padding: 5px;
                    font-weight: 500;
                }
            """)
            dest_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dest_label.setWordWrap(True)
            info_layout.addWidget(dest_label)
            
            # Tiempo
            time_label = QLabel(f"⏱ {bus['time']}")
            time_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #ffffff;
                    padding: 5px;
                }
            """)
            time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_layout.addWidget(time_label)
            
            sphere_layout.addWidget(info_widget)
            layout.addWidget(sphere_container)

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