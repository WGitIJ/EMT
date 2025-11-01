import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from controller_window import BusController  # ← Descomentado y corregido
from view.main_window import Ui_MainWindow  # ← Asegúrate de que esté en la misma carpeta


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Inicia el controlador, que conecta lógica y vista
        self.controller = BusController(view=self.ui)  # ← Activado


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("EMT Palma - Bus Arrivals")
    window.show()
    sys.exit(app.exec())