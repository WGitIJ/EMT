"""
EMT Palma Bus Arrival Application

Main entry point for the EMT Palma bus arrival monitoring application.
Provides real-time bus arrival information for Palma de Mallorca stops.
"""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
# Import QtWebEngineWidgets to ensure it's available before QApplication creation
from PyQt6.QtWebEngineWidgets import QWebEngineView

from controller.controller_window import BusController
from view.uiEMT import Ui_MainWindow


class MainWindow(QMainWindow):

    WINDOW_TITLE = "EMT Palma - Bus Arrivals"

    def __init__(self) -> None:
        """Initialize the main application window."""
        super().__init__()

        # Set up user interface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize controller with UI reference
        self.controller = BusController(view=self.ui)

        # Configure window - responsive
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(700, 500)
        self.resize(900, 650)


def main() -> None:
    # Configure Qt attributes for WebEngine
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()