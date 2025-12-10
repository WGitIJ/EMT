"""
EMT Palma Bus Arrival Application

Main entry point for the EMT Palma bus arrival monitoring application.
Provides real-time bus arrival information for Palma de Mallorca stops.
"""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from controller.controller_window import BusController
from view.uiEMT import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Main application window.

    Sets up the UI and initializes the controller to handle
    business logic and user interactions.
    """

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
    """Application entry point."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()