import sys
from datetime import datetime
import requests

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QScrollArea,
    QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette

class BusArrivalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMT Palma - Tiempos REALES")
        self.setGeometry(100, 100, 680, 780)

        self.recent_stops = []
        self.recent_buttons = []

        self.init_ui()
        self.setup_auto_refresh()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        inp = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Parada (ej: 37)")
        self.input.returnPressed.connect(self.check)
        inp.addWidget(self.input)
        self.btn = QPushButton("Consultar")
        self.btn.clicked.connect(self.check)
        inp.addWidget(self.btn)
        layout.addLayout(inp)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        layout.addLayout(self.grid)

        self.time_lbl = QLabel("Listo")
        self.time_lbl.setStyleSheet("font-style: italic; color: #555;")
        layout.addWidget(self.time_lbl)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_w = QWidget()
        self.scroll_l = QVBoxLayout(self.scroll_w)
        self.scroll_l.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scroll_w)
        layout.addWidget(self.scroll)

    def check(self):
        txt = self.input.text().strip()
        if not txt.isdigit():
            self.show_error("Ingresa un número válido")
            return
        stop = int(txt)
        self.add_recent(stop)
        self.fetch(stop)
        self.input.clear()

    def add_recent(self, stop):
        if stop in self.recent_stops:
            self.recent_stops.remove(stop)
        self.recent_stops.insert(0, stop)
        self.recent_stops = self.recent_stops[:6]
        self.update_grid()

    def update_grid(self):
        for b in self.recent_buttons:
            b.deleteLater()
        self.recent_buttons.clear()
        for i, s in enumerate(self.recent_stops):
            btn = QPushButton(f"Parada {s}")
            btn.setFixedHeight(42)
            btn.clicked.connect(lambda _, x=s: self.fetch(x))
            btn.setStyleSheet("background:#e8f5e9;border:1px solid #4caf50;border-radius:8px;")
            self.grid.addWidget(btn, i // 3, i % 3)
            self.recent_buttons.append(btn)

    def fetch(self, stop):
        self.clear()
        result = self.get_real(stop)

        if result == "token_expired":
            self.show_error("Error: Token expirado")
        elif result == "no_internet":
            self.show_error("Error de conexión con la API")
        elif result == "invalid_stop":
            self.show_error("Esta parada no existe")
        else:
            self.time_lbl.setText(f"REAL: {datetime.now().strftime('%H:%M:%S')}")
            for bus in result:
                self.add_bus(bus)

 

    def get_real(self, stop):
        try:
            url = f"https://www.emtpalma.cat/maas/api/v1/agency/stops/{stop}/timestr"

            headers = {
                "accept": "*/*",
                "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJzdWIiOiI3ODQ1NTUiLCJpYXQiOjE3NjE1Njg2MjksImV4cCI6MzMzOTQ0ODYyOSwidXNlcm5hbWUiOiIxNzYxNTY4NjI4NzY1NVJCVUtTUk81SU9BWkVXTjE0T0EiLCJ0b2tlbl9kZXZpY2UiOiJkNTk2YzExMzQ4MDExNjExZTNmMmYzMzllNzJlYjgzYzFkNmY2Mzc3ODhhYjQyODNjMzc4YzYyNmIzYjZkOWFjIiwiZGV2aWNlX3R5cGVfaWQiOjMsInJvbGVzIjoiQU5PTklNTyJ9.8d6suKy2_5aw1H6pGktFIizOwUqIYb1piFGKfAQUlCywq7vuW6-rh_7y7VSwoqdl",
                "user-agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10)

            # 1️⃣ Token caducado
            if response.status_code == 401:
                return "token_expired"

            # 2️⃣ Error de conexión o servidor
            if not response.ok:
                return "no_internet"

            json_data = response.json()
            print(json_data)  # ← puedes dejar esto para depurar

            # 3️⃣ Si no hay datos o formato inesperado
            if not isinstance(json_data, list) or len(json_data) == 0:
                return "invalid_stop"

            # Colores por línea
            colors = {
                "1": "#d32f2f", "2": "#1976d2", "3": "#388e3c", "4": "#f57c00",
                "7": "#7b1fa2", "15": "#00796b", "20": "#c2185b", "23": "#512da8",
                "25": "#00796b", "default": "#757575"
            }

            result = []

            # 4️⃣ Procesar líneas y vehículos
            for entry in json_data:
                line = str(entry.get("lineCode", "N/A"))
                vehicles = entry.get("vehicles", [])

                for v in vehicles:
                    dest = (v.get("destination") or "Sin destino")[:30]
                    seconds = v.get("seconds", 0)

                    if isinstance(seconds, (int, float)):
                        mins = max(0, int(seconds / 60))
                        time = "YA" if mins == 0 else f"{mins}'"
                    else:
                        time = "Pronto"

                    result.append({
                        "line": line,
                        "color": colors.get(line, colors["default"]),
                        "dest": dest,
                        "time": time
                    })

            if not result:
                return "invalid_stop"

            return result[:8]  # mostrar solo los 8 primeros

        except requests.exceptions.ConnectionError:
            return "no_internet"
        except requests.exceptions.Timeout:
            return "no_internet"
        except Exception as e:
            print(f"[ERROR] {e}")
            return "no_internet"

    def clear(self):
        while self.scroll_l.count():
            item = self.scroll_l.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_bus(self, bus):
        row = QFrame()
        row.setStyleSheet("background:white;border:1px solid #eee;border-radius:10px;margin:3px;")
        lay = QHBoxLayout(row)

        lbl_line = QLabel(bus["line"])
        lbl_line.setFixedWidth(55)
        lbl_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_line.setStyleSheet("font-weight:bold;color:black;border-radius:10px;")

        pal = lbl_line.palette()
        pal.setColor(lbl_line.backgroundRole(), QColor(bus["color"]))
        lbl_line.setPalette(pal)
        lbl_line.setAutoFillBackground(True)
        lay.addWidget(lbl_line)

        lbl_dest = QLabel(bus["dest"])
        lbl_dest.setStyleSheet("font-size:14px;padding:5px;")
        lay.addWidget(lbl_dest, 1)

        lbl_time = QLabel(bus["time"])
        lbl_time.setStyleSheet("font-weight:bold;font-size:18px;color:#d32f2f;padding:5px;")
        lay.addWidget(lbl_time, alignment=Qt.AlignmentFlag.AlignRight)

        self.scroll_l.addWidget(row)

    def show_error(self, msg):
        color_map = {
            "Token": ("#d32f2f", "#ffebee"),
            "conexión": ("#f57c00", "#fff3e0"),
            "parada": ("#1976d2", "#e3f2fd")
        }
        for key, (c, bg) in color_map.items():
            if key in msg:
                color, bg_color = c, bg
                break
        else:
            color, bg_color = "#555", "#f5f5f5"

        lbl = QLabel(f"{msg}")
        lbl.setStyleSheet(f"""
            color:{color};
            background:{bg_color};
            padding:20px;
            border-radius:12px;
            margin:15px;
            font-weight:bold;
            font-size:16px;
            border: 2px solid {color};
        """)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clear()
        self.scroll_l.addWidget(lbl)
        self.time_lbl.setText("ERROR")

    def setup_auto_refresh(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.recent_stops and self.fetch(self.recent_stops[0]))
        self.timer.start(25000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = BusArrivalApp()
    win.show()
    sys.exit(app.exec())