from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QUrl

try:
    # WebEngine permite incrustar un mapa (p. ej. OpenStreetMap / web EMT)
    from PyQt6.QtWebEngineWidgets import QWebEngineView

    HAS_WEBENGINE = True
except ImportError:
    # Si no está instalado PyQt6-WebEngine, mostramos un mensaje en lugar del mapa
    QWebEngineView = None
    HAS_WEBENGINE = False


class MapWindow(QMainWindow):
    """
    Ventana independiente que muestra un mapa de Palma/EMT.
    Usa QWebEngineView si está disponible; si no, muestra un aviso.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mapa EMT Palma")
        self.resize(900, 600)

        central = QWidget(self)
        layout = QVBoxLayout(central)
        central.setLayout(layout)
        self.setCentralWidget(central)

        if HAS_WEBENGINE:
            self.web_view = QWebEngineView(central)
            layout.addWidget(self.web_view)

            # Puedes cambiar la URL por la que más te guste (por ejemplo, un mapa propio)
            url = QUrl("https://www.emtpalma.cat/es/lineas")
            self.web_view.setUrl(url)
        else:
            info_label = QLabel(
                "Para ver el mapa incrustado necesitas instalar el paquete "
                "<b>PyQt6-WebEngine</b>.\n\n"
                "Ejemplo (en tu entorno):<br>"
                "<code>pip install PyQt6-WebEngine</code>",
                parent=central,
            )
            info_label.setWordWrap(True)
            layout.addWidget(info_label)


