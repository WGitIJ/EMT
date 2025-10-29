import sys
import requests
import re
from datetime import datetime
from PyQt6 import QtWidgets, QtCore
import traceback




class BusArrivalApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        print("Iniciando aplicación EMT Palma...")

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("EMT Palma - Tiempo de Llegada")

        # === Variables ===
        self.recent_stops = []

        # === Layout del frame ===
        if self.ui.frame.layout() is None:
            self.frame_layout = QtWidgets.QVBoxLayout(self.ui.frame)
            self.frame_layout.setContentsMargins(20, 20, 20, 20)
            self.frame_layout.setSpacing(10)
        else:
            self.frame_layout = self.ui.frame.layout()

        # === Contenedor botones recientes ===
        self.recent_container = QtWidgets.QWidget()
        self.recent_layout = QtWidgets.QGridLayout(self.recent_container)
        self.recent_layout.setSpacing(6)

        # === Etiqueta de hora ===
        self.time_label = QtWidgets.QLabel("Última actualización: Nunca")
        self.time_label.setedAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 11px; color: #555; margin: 8px;")

        # === Área de resultados ===
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # === Reemplazar plainTextEdit ===
        self.ui.plainTextEdit.setParent(None)
        self.frame_layout.addWidget(self.scroll_area)

        # === Insertar elementos en orden ===
        self.frame_layout.insertWidget(2, self.recent_container)
        self.frame_layout.insertWidget(3, self.time_label)

        # === Conexiones ===
        self.ui.pushButton.clicked.connect(self.buscar_parada)
        self.ui.textEdit.returnPressed.connect(self.buscar_parada)

        print("Interfaz lista.")

    def buscar_parada(self):
        try:
            numero_parada = self.ui.textEdit.toPlainText().strip()
            print(f"Buscando parada: {numero_parada}")

            if not numero_parada.isdigit():
                self.mostrar_error("Error", "Introduce un número de parada válido.")
                return

            datos = self.obtener_datos_parada(numero_parada)
            if datos is None:
                self.mostrar_error("Error de red", "No se pudo conectar con EMT Palma.")
                return
            if not datos:
                self.mostrar_error("Sin datos", "No hay buses para esta parada.")
                return

            self.actualizar_hora()
            self.mostrar_resultados(datos)
            self.agregar_parada_reciente(numero_parada)

        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()
            self.mostrar_error("Error", str(e))

    def obtener_datos_parada(self, stop_id):
        url = f"https://www.emtpalma.cat/EMTPalma/FrontEnd/tiempoparada?stopId={stop_id}"
        print(f"Consultando: {url}")

        try:
            response = requests.get(url, timeout=10)
            print(f"HTTP: {response.status_code}")
            if response.status_code != 200:
                return None

            html = response.text

            # === EXTRAER FILAS CON REGEX (sin BeautifulSoup) ===
            # Buscamos: <tr><td>Línea</td><td>Destino</td><td>Tiempo</td></tr>
            patron_fila = r'<tr>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*</tr>'
            coincidencias = re.findall(patron_fila, html)

            llegadas = []
            for linea, destino, tiempo in coincidencias:
                linea = linea.strip()
                destino = destino.strip()
                tiempo = tiempo.strip().replace(" min.", "").strip()

                if "no" in tiempo.lower() or tiempo == "":
                    tiempo = "Sin datos"
                elif tiempo.isdigit():
                    mins = int(tiempo)
                    tiempo = "< 1 min" if mins == 0 else f"{mins} min"
                else:
                    tiempo = tiempo

                llegadas.append({
                    "linea": linea,
                    "destino": destino,
                    "tiempo": tiempo
                })

            print(f"Encontradas {len(llegadas)} llegadas.")
            return llegadas

        except Exception as e:
            print("Error en obtener_datos_parada:", e)
            return None

    def actualizar_hora(self):
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.setText(f"Última actualización: {ahora}")

    def mostrar_resultados(self, llegadas):
        # Limpiar
        for i in reversed(range(self.scroll_layout.count())):
            w = self.scroll_layout.itemAt(i).widget()
            if w: w.deleteLater()

        if not llegadas:
            label = QtWidgets.QLabel("No hay llegadas próximas.")
            label.setStyleSheet("color: #888; font-style: italic;")
            self.scroll_layout.addWidget(label)
            return

        for item in llegadas:
            color = self.color_linea(item["linea"])
            texto = f"• Línea {item['linea']} → {item['destino']}: {item['tiempo']}"
            label = QtWidgets.QLabel(texto)
            label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 13px; margin: 2px;")
            self.scroll_layout.addWidget(label)

        self.scroll_layout.addStretch()

    def color_linea(self, linea):
        colores = {
            "1": "#E30613", "2": "#0033A0", "3": "#00A650", "4": "#FFD700",
            "5": "#A05A2C", "7": "#FF69B4", "8": "#808080", "12": "#1E90FF",
            "15": "#8B4513", "20": "#32CD32", "25": "#FF4500", "30": "#4B0082",
            "35": "#00CED1", "46": "#DC143C"
        }
        return colores.get(linea, "#000000")

    def agregar_parada_reciente(self, stop_id):
        if stop_id in self.recent_stops:
            return
        self.recent_stops.append(stop_id)
        if len(self.recent_stops) > 12:
            self.recent_stops.pop(0)
        self.actualizar_botones_recientes()

    def actualizar_botones_recientes(self):
        for i in reversed(range(self.recent_layout.count())):
            w = self.recent_layout.itemAt(i).widget()
            if w: w.deleteLater()

        for i, stop in enumerate(self.recent_stops):
            btn = QtWidgets.QPushButton(f"Parada {stop}")
            btn.setFixedHeight(32)
            btn.setStyleSheet("margin: 2px;")
            btn.clicked.connect(lambda _, s=stop: self.reconsultar(s))
            self.recent_layout.addWidget(btn, i // 3, i % 3)

    def reconsultar(self, stop_id):
        self.ui.textEdit.setPlainText(stop_id)
        self.buscar_parada()

    def mostrar_error(self, titulo, mensaje):
        QtWidgets.QMessageBox.warning(self, titulo, mensaje)


# === EJECUTAR ===
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = BusArrivalApp()
        window.show()
        print("App ejecutándose. Usa parada 101 para probar.")
        sys.exit(app.exec())
    except Exception as e:
        print("ERROR FATAL:", e)
        traceback.print_exc()
        input("Presiona Enter...")