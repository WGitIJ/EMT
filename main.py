import sys
<<<<<<< Updated upstream
from PyQt6.QtWidgets import QApplication, QMainWindow
from controller.controller_window import BusController  # ← Descomentado y corregido
from view.uiEMT import Ui_MainWindow  # ← Asegúrate de que esté en la misma carpeta


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Inicia el controlador, que conecta lógica y vista
        self.controller = BusController(view=self.ui)  # ← Activado
=======

from PyQt6.QtWidgets import QApplication, QMainWindow, QSizePolicy 
from PyQt6.QtCore import Qt

from view.uiEMT import Ui_MainWindow
from controller.controller_window import BusController


class MainWindow(QMainWindow):
    WINDOW_TITLE = "EMT Palma - Bus Arrivals"

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(600, 500)
        self.resize(1200, 800)
        self.setWindowState(Qt.WindowState.WindowNoState)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Responsive: elementos principales se expanden
        self.ui.centralwidget.setContentsMargins(10, 10, 10, 10)
        self.ui.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Scroll areas responsive
        for scroll in [self.ui.scrollArea, self.ui.scrollArea_2, self.ui.scrollArea_3]:
            if hasattr(self.ui, scroll.objectName()):  # Seguridad
                scroll.setWidgetResizable(True)
                scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Entrada y botón flexibles
        self.ui.stopLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.ui.checkButton.setMinimumWidth(100)

        # Layout principal
        self.ui.verticalLayout.setSpacing(10)
        self.ui.verticalLayout.setContentsMargins(15, 15, 15, 15)

        self.controller = BusController(view=self.ui)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
>>>>>>> Stashed changes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("EMT Palma - Bus Arrivals")
    window.show()
    sys.exit(app.exec())