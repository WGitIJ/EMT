<<<<<<< Updated upstream
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
=======
from typing import List, Dict, Any
import io

import folium

from PyQt6.QtWidgets import (
    QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QSizePolicy, QMainWindow
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWebEngineWidgets import QWebEngineView

from model.model_window import EMTApi


class BusController:
    MAX_RECENT_STOPS = 6

    def __init__(self, view) -> None:
        self.view = view
        self.model = EMTApi()
        self.recent_stops: List[int] = []
        self.map_windows: List[QMainWindow] = []

        self._setup_connections()
        self._setup_lines_tab()

    def _setup_connections(self) -> None:
        self.view.checkButton.clicked.connect(self.on_check_stop)
        self.view.stopLineEdit.returnPressed.connect(self.on_check_stop)

    def _setup_lines_tab(self) -> None:
        if not hasattr(self.view, "scrollArea_2"):
            return

        lines_data = self.model.get_all_lines()
        if lines_data == "no_data":
            self._show_error_message("Error", "No se pudieron cargar las líneas.", QMessageBox.Icon.Warning)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
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
            # Conectar el botón para mostrar las sublíneas de la línea
            # Usar lineId (ID numérico) para la API de sublíneas
            line_id = stop.get('lineId', stop['id'])
            circle_button.clicked.connect(lambda checked, lid=line_id: self.on_line_clicked(lid))
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
=======
        layout.setContentsMargins(15, 15, 15, 15)

        for line_code, line_info in lines_data.items():
            widget = QWidget()
            widget.setStyleSheet("""
                QWidget {
                    background-color: #3a3a3a;
                    border-radius: 12px;
                    padding: 10px;
                    margin: 5px;
                }
                QWidget:hover {
                    background-color: #444444;
                }
            """)
            hlayout = QHBoxLayout(widget)
            hlayout.setContentsMargins(15, 15, 15, 15)
            hlayout.setSpacing(20)

            color = line_info.get('color', '#757575')
            btn = QPushButton(line_code)
            btn.setFixedSize(70, 70)
            btn.setStyleSheet(
                f"QPushButton {{ background-color: {color}; color: white; border-radius: 35px; "
                f"font-weight: bold; font-size: 20px; border: 3px solid #2d2d2d; }}"
                f"QPushButton:hover {{ border: 3px solid #555555; }}"
                f"QPushButton:pressed {{ border: 3px solid #666666; }}"
            )
            btn.clicked.connect(lambda _, lid=line_code: self.on_line_clicked(lid))
            hlayout.addWidget(btn)

            name = QLabel(line_info.get('name', line_code))
            name.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 500;")
            name.setWordWrap(True)
            name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            hlayout.addWidget(name, stretch=1)

            layout.addWidget(widget)

        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
>>>>>>> Stashed changes

        old = self.view.scrollArea_2.takeWidget()
        if old:
            old.deleteLater()
        self.view.scrollArea_2.setWidget(container)
        self.view.scrollArea_2.setWidgetResizable(True)

    def on_line_clicked(self, line_id: str) -> None:
        print(f"Cargando sublíneas para la línea {line_id}")

        if not hasattr(self.view, "scrollArea_3"):
            return

        loading = QWidget()
        vbox = QVBoxLayout(loading)
        vbox.addWidget(QLabel(f"Cargando sublíneas de la línea {line_id}..."))
        old = self.view.scrollArea_3.takeWidget()
        if old:
            old.deleteLater()
        self.view.scrollArea_3.setWidget(loading)

        sublines = self.model.get_line_sublines(line_id)

        if isinstance(sublines, str):
            self._show_error_message("Error", "No se pudieron cargar las sublíneas.", QMessageBox.Icon.Critical)
            self._show_empty_sublines()
            return

        self._display_sublines(sublines, line_id)

    def _display_sublines(self, sublines: List[Dict[str, Any]], line_id: str) -> None:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        if not sublines:
            layout.addWidget(QLabel(f"No hay sublíneas para la línea {line_id}."))
        else:
            for sub in sublines:
                w = QWidget()
                w.setStyleSheet("background-color: #3a3a3a; border-radius: 12px;")
                h = QHBoxLayout(w)
                h.setContentsMargins(20, 15, 20, 15)
                h.setSpacing(20)

                id_lbl = QLabel(f"#{sub['id']}")
                id_lbl.setStyleSheet("background-color: #e67e22; color: white; padding: 12px 24px; border-radius: 24px; font-weight: bold; font-size: 14px;")
                id_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                h.addWidget(id_lbl)

                info = QWidget()
                vinfo = QVBoxLayout(info)
                vinfo.setContentsMargins(0, 0, 0, 0)
                vinfo.setSpacing(8)

                name = QLabel(sub.get('name', 'Desconocido'))
                name.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 500;")
                name.setWordWrap(True)
                vinfo.addWidget(name)

                if sub.get('direction'):
                    dir_lbl = QLabel(f"Dirección: {sub['direction']}")
                    dir_lbl.setStyleSheet("color: #cccccc; font-size: 13px; font-style: italic;")
                    dir_lbl.setWordWrap(True)
                    vinfo.addWidget(dir_lbl)

                h.addWidget(info, stretch=1)

                # Obtener tripIds
                trip_ids = self.model.get_subline_trip_ids(sub['id'])

                for trip_id in trip_ids:
                    # Obtener directionId
                    dir_id = "Desconocida"
                    endpoint_dir = f"{self.model.BASE_URL}/agency/lines/directions-subline?subLineId={sub['id']}"
                    try:
                        response_dir = requests.get(endpoint_dir, headers=self.model._get_headers(), timeout=self.model.REQUEST_TIMEOUT)
                        if response_dir.ok:
                            data_dir = response_dir.json()
                            for item in data_dir:
                                if str(item.get("tripId")) == str(trip_id):
                                    dir_id = str(item.get("directionId", "Desconocida"))
                                    break
                    except:
                        pass

                    dir_text = "Ida" if dir_id == "1" else "Vuelta" if dir_id == "2" else f"Dir {dir_id}"

                    btn = QPushButton(f"Abrir {dir_text}")
                    btn.setFixedHeight(45)
                    btn.setStyleSheet("""
                        QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 14px; padding: 0 20px; }
                        QPushButton:hover { background-color: #45a049; }
                        QPushButton:pressed { background-color: #3d8b40; }
                    """)
                    btn.clicked.connect(
                        lambda _, lid=line_id, sid=sub['id'], sn=sub.get('name', ''), tid=trip_id:
                            self.on_subline_button_clicked(lid, sid, f"{sn} ({dir_text})", tid)
                    )
                    h.addWidget(btn)

                layout.addWidget(w)

        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        old = self.view.scrollArea_3.takeWidget()
        if old:
            old.deleteLater()
        self.view.scrollArea_3.setWidget(container)
        self.view.scrollArea_3.setWidgetResizable(True)

    def on_subline_button_clicked(self, line_id: str, subline_id: str, subline_name: str, trip_id: str) -> None:
        print(f"Abriendo mapa embebido para sublínea {subline_id} - tripId {trip_id}")

        map_window = QMainWindow()
        map_window.setWindowTitle(f"Mapa - Línea {line_id} | Sublínea {subline_id} - {subline_name}")
        map_window.setMinimumSize(800, 600)
        map_window.resize(1200, 800)

        web_view = QWebEngineView()
        map_window.setCentralWidget(web_view)

        m = folium.Map(location=[39.5696, 2.6502], zoom_start=12, tiles="OpenStreetMap")

        stops = self.model.get_subline_stops(line_id, trip_id)
        shape_points = self.model.get_subline_shape(line_id, trip_id)

        # Dibujar ruta
        if shape_points:
            folium.PolyLine(
                locations=shape_points,
                color="red",
                weight=6,
                opacity=0.9
            ).add_to(m)

        # Dibujar paradas
        if stops:
            for i, stop in enumerate(stops):
                folium.Marker(
                    location=[stop['lat'], stop['lon']],
                    popup=f"<b style='font-size:16px'>{stop['name']}</b><br>ID: {stop['id']}",
                    tooltip=stop['name'],
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            background-color: red;
                            color: white;
                            width: 30px; height: 30px;
                            border-radius: 50%;
                            text-align: center;
                            line-height: 30px;
                            font-size: 14px;
                            font-weight: bold;
                            border: 3px solid white;
                            box-shadow: 0 0 8px rgba(0,0,0,0.6);
                        ">{i+1}</div>
                        """
                    )
                ).add_to(m)

            coords = [[s['lat'], s['lon']] for s in stops]
            m.fit_bounds(coords)
        elif shape_points:
            m.fit_bounds(shape_points)
        else:
            folium.Marker(
                [39.5696, 2.6502],
                popup="<b style='font-size:18px; color:red'>No se encontraron datos</b>",
                icon=folium.DivIcon(
                    html="""
                    <div style="
                        background-color: red;
                        color: white;
                        width: 50px; height: 50px;
                        border-radius: 50%;
                        text-align: center;
                        line-height: 50px;
                        font-size: 20px;
                        font-weight: bold;
                        border: 5px solid white;
                        box-shadow: 0 0 12px rgba(0,0,0,0.8);
                    ">!</div>
                    """
                )
            ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        web_view.setHtml(data.getvalue().decode())

        map_window.show()
        self.map_windows.append(map_window)

    def _show_empty_sublines(self) -> None:
        container = QWidget()
        layout = QVBoxLayout(container)
        lbl = QLabel("No se pudieron cargar las sublíneas.")
        lbl.setStyleSheet("color: #e74c3c; padding: 20px; background-color: #4a2a2a; border-radius: 8px;")
        layout.addWidget(lbl)
        old = self.view.scrollArea_3.takeWidget()
        if old:
            old.deleteLater()
        self.view.scrollArea_3.setWidget(container)

<<<<<<< Updated upstream
    # ================================================================
    # Manejo de clic en línea: mostrar paradas de la línea
    # ================================================================
    def on_line_clicked(self, line_id: str):
        """Muestra las sublíneas de una línea y las hace pulsables"""
        print(f"[INFO] Clic en línea con ID: {line_id}")

        # Mostrar mensaje de carga
        loading_container = QWidget()
        loading_layout = QVBoxLayout(loading_container)
        loading_label = QLabel("Cargando sublíneas...")
        loading_label.setStyleSheet("font-size: 12px; color: #ffffff; padding: 10px;")
        loading_layout.addWidget(loading_label)

        old_widget = self.view.scrollArea_3.takeWidget()
        if old_widget:
            old_widget.deleteLater()
        self.view.scrollArea_3.setWidget(loading_container)

        # Obtener las sublíneas de la línea usando el lineId
        sublines = self.model.get_line_sublines(line_id)

        # Manejo de errores
        if sublines == "no_internet":
            self.show_message("Error", f"No se pudo conectar con el servidor.\nRevisa la consola para más detalles.", QMessageBox.Icon.Critical)
            # Mostrar mensaje de error en el scroll
            error_container = QWidget()
            error_layout = QVBoxLayout(error_container)
            error_label = QLabel("Error al cargar sublíneas.\nNo se pudo conectar con el servidor.")
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
        elif sublines == "token_expired":
            self.show_message("Error", "Token caducado. Necesitas actualizarlo en el modelo.", QMessageBox.Icon.Critical)
            # Mostrar mensaje de error en el scroll
            error_container = QWidget()
            error_layout = QVBoxLayout(error_container)
            error_label = QLabel("Error: Token caducado.\nActualiza el token en el modelo.")
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

        if not sublines:
            # Si no hay paradas, mostrar un mensaje con estilo mejorado - Tema oscuro
            no_sublines_label = QLabel("No se encontraron sublíneas para esta línea.")
            no_sublines_label.setStyleSheet("""
                QLabel { font-size: 13px; color: #ffffff; padding: 15px; background-color: #3a3a3a; border-radius: 8px; }
            """)
            layout.addWidget(no_sublines_label)
        else:
            for subline in sublines:
                btn = QPushButton(f"Sublínea {subline['id']}: {subline['name']}")
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: #fff;
                        border-radius: 8px;
                        padding: 8px 16px;
                        margin-bottom: 5px;
                        font-size: 13px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #217dbb;
                    }
                """)
                # Pasa solo el id de la línea principal
                btn.clicked.connect(lambda checked, lid=line_id: self.on_subline_clicked(lid))
                layout.addWidget(btn)
        self.view.scrollArea_3.setWidget(container)
        print(f"[INFO] Se mostraron {len(sublines) if sublines else 0} sublíneas")

    def on_subline_clicked(self, line_id):
        """Abre un mapa Folium usando solo las paradas de la línea principal (API lines/{lineId}/stops)"""
        print(f"[INFO] Mostrar ruta principal de línea: {line_id}")
        stops = self.model.get_line_stops(line_id)
        if not stops or not isinstance(stops, list):
            self.show_message("Error", "No se pudo obtener la ruta de la línea principal.")
            return
        import folium
        import webbrowser
        points = []
        m = folium.Map(location=[39.5696, 2.6502], zoom_start=13, tiles="CartoDB dark_matter")
        for parada in stops:
            lat = parada.get("lat") or parada.get("latitude")
            lon = parada.get("lon") or parada.get("longitude")
            nombre = parada.get("name", "Sin nombre")
            if lat and lon:
                points.append((lat, lon))
                folium.Marker([lat, lon], tooltip=nombre, popup=nombre, icon=folium.Icon(color="blue")).add_to(m)
        if points:
            folium.PolyLine(points, color="red", weight=4, opacity=0.7).add_to(m)
            m.fit_bounds([points[0], points[-1]])
            m.save("ruta_linea_principal.html")
            webbrowser.open_new_tab("ruta_linea_principal.html")
        else:
            self.show_message("Sin datos","No hay puntos geográficos en la línea.")

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
=======
    def on_check_stop(self) -> None:
        stop_text = self.view.stopLineEdit.text().strip()
        if not stop_text.isdigit():
            self._show_error_message("Entrada inválida", "Por favor, introduce un número de parada válido.", QMessageBox.Icon.Warning)
            return

        stop_id = int(stop_text)
        self._add_to_recent_stops(stop_id)

        self.view.timeLabel.setText("Cargando tiempos de llegada...")
        arrivals = self.model.get_arrivals(stop_id)

        if arrivals == "no_internet":
            self._show_error_message("Error de conexión", "No se pudo conectar al servidor.", QMessageBox.Icon.Critical)
            self.view.timeLabel.setText("Última actualización: -")
            return
        elif arrivals == "invalid_stop":
            self._show_error_message("Parada no encontrada", f"No hay datos para la parada {stop_id}.", QMessageBox.Icon.Warning)
            self.view.timeLabel.setText("Última actualización: -")
            return
        elif arrivals == "token_expired":
            self._show_error_message("Error", "Token expirado.", QMessageBox.Icon.Critical)
            self.view.timeLabel.setText("Última actualización: -")
            return

        self._display_arrivals(arrivals)
        timestamp = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.view.timeLabel.setText(f"Última actualización: {timestamp}")

    def _display_arrivals(self, arrivals: List[Dict[str, Any]]) -> None:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        for bus in arrivals:
            block = QWidget()
            block_layout = QVBoxLayout(block)
            block_layout.setContentsMargins(15, 12, 15, 12)
            block_layout.setSpacing(6)

            line_lbl = QLabel(f"<b>Línea {bus['line']}</b>")
            line_lbl.setStyleSheet(f"color: {bus['color']}; font-size: 18px; font-weight: bold;")
            block_layout.addWidget(line_lbl)

            dest_lbl = QLabel(bus['dest'])
            dest_lbl.setStyleSheet("font-size: 14px; color: #cccccc;")
            dest_lbl.setWordWrap(True)
            block_layout.addWidget(dest_lbl)

            time_lbl = QLabel(bus['time'])
            time_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
            block_layout.addWidget(time_lbl)

            layout.addWidget(block)

        old = self.view.scrollArea.takeWidget()
        if old:
            old.deleteLater()
        self.view.scrollArea.setWidget(container)

    def _add_to_recent_stops(self, stop_id: int) -> None:
        if stop_id in self.recent_stops:
            self.recent_stops.remove(stop_id)
        self.recent_stops.insert(0, stop_id)
        self.recent_stops = self.recent_stops[:self.MAX_RECENT_STOPS]
        self._update_recent_stops_grid()

    def _update_recent_stops_grid(self) -> None:
        layout = self.view.recentStopsLayout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, stop in enumerate(self.recent_stops):
            btn = QPushButton(str(stop))
            btn.setStyleSheet("""
                QPushButton { background-color: #3498db; color: white; border-radius: 8px; padding: 10px; font-weight: bold; font-size: 14px; }
                QPushButton:hover { background-color: #5dade2; }
            """)
            btn.clicked.connect(lambda _, s=stop: self._load_recent_stop(s))
            row, col = divmod(i, 3)
            layout.addWidget(btn, row, col)

    def _load_recent_stop(self, stop_id: int) -> None:
        self.view.stopLineEdit.setText(str(stop_id))
        self.on_check_stop()

    def _show_error_message(self, title: str, message: str, icon=QMessageBox.Icon.Information) -> None:
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
>>>>>>> Stashed changes
        msg.setIcon(icon)
        msg.exec()