"""
EMT Palma Bus Controller

This module handles the business logic for the EMT Palma bus arrival application.
It manages user interactions, API communication, and data presentation.
"""

from typing import List, Dict, Any

from PyQt6.QtWidgets import QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QMainWindow
from PyQt6.QtCore import Qt, QDateTime

from model.model_window import EMTApi


class BusController:
    """
    Main controller for EMT Palma bus arrival application.

    Handles user input validation, API communication, recent stops management,
    and data presentation in the user interface.
    """

    MAX_RECENT_STOPS = 6

    def __init__(self, view) -> None:
        """
        Initialize the controller with view reference.

        Args:
            view: The main UI view instance.
        """
        self.view = view
        self.model = EMTApi()
        self.recent_stops: List[int] = []
        self._open_windows = []  # Keep references to prevent garbage collection
        self._current_map_window = None  # Reference to the current map window
        self._setup_connections()
        self._setup_lines_tab()

    def _setup_connections(self) -> None:
        """Configure signal-slot connections for UI elements."""
        self.view.checkButton.clicked.connect(self.on_check_stop)
        self.view.stopLineEdit.returnPressed.connect(self.on_check_stop)

    def _setup_lines_tab(self) -> None:
        """
        Initialize the lines tab with all available bus lines.
        """
        if not hasattr(self.view, "scrollArea_2"):
            return

        lines_data = self.model.get_all_lines()

        if lines_data == "no_data":
            self._show_error_message(
                "Data Error",
                "Unable to load bus lines information.",
                QMessageBox.Icon.Warning
            )
            return

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        for line_code, line_info in lines_data.items():
            # Create line display widget - responsive
            line_widget = QWidget()
            line_widget.setStyleSheet("""
                QWidget {
                    background-color: #3a3a3a;
                    border-radius: 8px;
                    padding: 4px;
                    margin: 2px;
                }
            """)
            line_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            line_layout = QHBoxLayout(line_widget)
            line_layout.setContentsMargins(8, 6, 8, 6)
            line_layout.setSpacing(10)

            # Line number button with color - responsive
            line_color = line_info.get('color', '#757575')
            line_button = QPushButton(line_code)
            line_button.setMinimumSize(45, 45)
            line_button.setMaximumSize(60, 60)
            line_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            line_button.setStyleSheet(
                f"QPushButton {{"
                f"background-color: {line_color}; "
                f"color: white; "
                f"border-radius: 22px; "
                f"font-weight: bold; "
                f"font-size: 14px; "
                f"border: 2px solid #2d2d2d;"
                f"min-width: 45px; "
                f"min-height: 45px; "
                f"max-width: 60px; "
                f"max-height: 60px;"
                f"}}"
                f"QPushButton:hover {{"
                f"background-color: {line_color}; "
                f"border: 2px solid #555555;"
                f"}}"
                f"QPushButton:pressed {{"
                f"background-color: {line_color}; "
                f"border: 2px solid #666666;"
                f"}}"
            )
            line_button.clicked.connect(lambda _, lid=line_code: self.on_line_clicked(lid))
            line_layout.addWidget(line_button)

            # Line name - responsive
            name_label = QLabel(line_info.get('name', line_code))
            name_label.setWordWrap(True)
            name_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #ffffff;
                    padding: 3px 6px;
                    font-weight: 500;
                    min-height: 15px;
                }
            """)
            name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            line_layout.addWidget(name_label, stretch=1)

            layout.addWidget(line_widget)

        # Replace existing content
        old_widget = self.view.scrollArea_2.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        self.view.scrollArea_2.setWidget(container)

    def on_check_stop(self) -> None:
        """
        Handle stop check request from user input.

        Validates input, queries API for arrivals, and updates the UI
        with results or appropriate error messages.
        """
        stop_text = self.view.stopLineEdit.text().strip()

        if not stop_text.isdigit():
            self._show_error_message(
                "Invalid Input",
                "Please enter a valid stop number.",
                QMessageBox.Icon.Warning
            )
            return

        stop_id = int(stop_text)
        self._add_to_recent_stops(stop_id)

        self.view.timeLabel.setText("Loading arrival times...")
        arrivals = self.model.get_arrivals(stop_id)

        # Handle API response
        if arrivals == "no_internet":
            self._show_error_message(
                "Connection Error",
                "Unable to connect to the server. Please check your internet connection.",
                QMessageBox.Icon.Critical
            )
            self.view.timeLabel.setText("Last update: -")
            return

        elif arrivals == "invalid_stop":
            self._show_error_message(
                "Stop Not Found",
                f"No data available for stop {stop_id}. Please verify the stop number.",
                QMessageBox.Icon.Warning
            )
            self.view.timeLabel.setText("Last update: -")
            return

        elif arrivals == "token_expired":
            self._show_error_message(
                "Authentication Error",
                "API token has expired. Please update the token in the model configuration.",
                QMessageBox.Icon.Critical
            )
            self.view.timeLabel.setText("Last update: -")
            return

        # Display successful results
        self._display_arrivals(arrivals)
        timestamp = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        self.view.timeLabel.setText(f"Last update: {timestamp}")

    def _add_to_recent_stops(self, stop_id: int) -> None:
        """
        Add a stop to the recent stops list.

        Maintains a maximum of MAX_RECENT_STOPS items, with most recent first.

        Args:
            stop_id: The stop number to add.
        """
        if stop_id in self.recent_stops:
            self.recent_stops.remove(stop_id)

        self.recent_stops.insert(0, stop_id)
        self.recent_stops = self.recent_stops[:self.MAX_RECENT_STOPS]
        self._update_recent_stops_grid()

    def _update_recent_stops_grid(self) -> None:
        """Refresh the recent stops grid in the UI."""
        layout = self.view.recentStopsLayout

        # Clear existing widgets
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add recent stops as buttons
        for index, stop_id in enumerate(self.recent_stops):
            button = QPushButton(str(stop_id))
            button.clicked.connect(lambda _, s=stop_id: self._load_recent_stop(s))

            row, col = divmod(index, 3)
            layout.addWidget(button, row, col)

    def _load_recent_stop(self, stop_id: int) -> None:
        """
        Load arrival data for a stop from the recent stops list.

        Args:
            stop_id: The stop number to query.
        """
        self.view.stopLineEdit.setText(str(stop_id))
        self.on_check_stop()

    def on_line_clicked(self, line_id: str) -> None:
        """
        Display sublines for a selected bus line.

        Args:
            line_id: The line identifier to show sublines for.
        """
        print(f"Loading sublines for line: {line_id}")

        if not hasattr(self.view, "scrollArea_3"):
            return

        # Show loading message
        loading_container = QWidget()
        loading_layout = QVBoxLayout(loading_container)
        loading_label = QLabel(f"Loading sublines for line {line_id}...")
        loading_label.setStyleSheet("font-size: 12px; color: #ffffff; padding: 10px;")
        loading_layout.addWidget(loading_label)

        old_widget = self.view.scrollArea_3.takeWidget()
        if old_widget:
            old_widget.deleteLater()
        self.view.scrollArea_3.setWidget(loading_container)

        # Fetch sublines
        sublines = self.model.get_line_sublines(line_id)

        # Handle errors
        if sublines == "no_internet":
            self._show_error_message(
                "Connection Error",
                "Unable to connect to the server to load sublines.",
                QMessageBox.Icon.Critical
            )
            self._show_empty_sublines()
            return

        elif sublines == "token_expired":
            self._show_error_message(
                "Authentication Error",
                "API token has expired. Please update the token.",
                QMessageBox.Icon.Critical
            )
            self._show_empty_sublines()
            return

        elif sublines == "invalid_data":
            self._show_error_message(
                "Data Error",
                "Invalid data received from the server.",
                QMessageBox.Icon.Warning
            )
            self._show_empty_sublines()
            return

        # Display sublines
        self._display_sublines(sublines, line_id)

    def open_window(self):
        from view import Second_Window  # importa aquí para evitar dependencias circulares
        # Si la ventana ya existe, no la recreamos
        if not hasattr(self, "map_window") or self.map_window is None:
            self.map_window = Second_Window()
        self.map_window.show()
        

    def on_subline_button_clicked(self, line_id: str, subline_id: str, subline_name: str) -> None:
        """
        Open map window with Folium when a subline button is clicked.

        Args:
            line_id: The line identifier
            subline_id: The subline identifier
            subline_name: The subline name
        """
        print(f"Opening Folium map window for line {line_id}, subline {subline_id}: {subline_name}")

        try:
            from view.map_window import MapWindow
            from PyQt6.QtCore import QTimer

            # If we already have a map window, update it with new line data
            if hasattr(self, '_current_map_window') and self._current_map_window and not self._current_map_window.isHidden():
                print("Updating existing map window")
                self._update_map_window(line_id, subline_id, subline_name)
                return

            # Create new map window
            map_window = MapWindow(line_id, subline_id, subline_name, model=self.model)

            # Keep reference to prevent garbage collection
            self._open_windows.append(map_window)
            self._current_map_window = map_window

            # Connect close event to remove from list
            map_window.destroyed.connect(lambda: self._on_window_closed(map_window))

            # Show the window
            map_window.show()
            map_window.raise_()
            map_window.activateWindow()
            map_window.setFocus()

            # Ensure window stays visible
            QTimer.singleShot(100, lambda: self._ensure_window_visible(map_window))

            print(f"Folium map window opened for subline {subline_id}")

        except Exception as e:
            print(f"Error opening map window: {e}")
            import traceback
            traceback.print_exc()
            self._show_error_message(
                "Error",
                f"Unable to open map window for subline {subline_id}: {str(e)}",
                QMessageBox.Icon.Critical
            )

    def _ensure_window_visible(self, window):
        """Ensure the window is visible and on top."""
        if window:
            window.show()
            window.raise_()
            window.activateWindow()
            window.setFocus()
            window.repaint()

    def _on_window_closed(self, window):
        """Called when a window is closed to clean up references."""
        if window in self._open_windows:
            self._open_windows.remove(window)
        if window == self._current_map_window:
            self._current_map_window = None

    def _update_map_window(self, line_id: str, subline_id: str, subline_name: str):
        """Update the existing map window with new line data."""
        if not self._current_map_window:
            return

        try:
            print(f"Updating map window with line {line_id}, subline {subline_id}")
            # Update the window properties
            self._current_map_window.line_id = line_id
            self._current_map_window.subline_id = subline_id
            self._current_map_window.subline_name = subline_name
            self._current_map_window.setWindowTitle(f"Mapa - Línea {line_id} - {subline_name}")

            # Reload the map with new data
            self._current_map_window._load_map()

            # Bring window to front
            self._current_map_window.raise_()
            self._current_map_window.activateWindow()
            self._current_map_window.setFocus()

        except Exception as e:
            print(f"Error updating map window: {e}")
            import traceback
            traceback.print_exc()

    def _display_sublines(self, sublines: List[Dict[str, Any]], line_id: str) -> None:
        """
        Display sublines information in the scrollable area.

        Args:
            sublines: List of subline dictionaries.
            line_id: The parent line identifier.
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        if not sublines:
            # No sublines available
            no_sublines_label = QLabel(f"No sublines available for line {line_id}.")
            no_sublines_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #ffffff;
                    padding: 15px;
                    background-color: #3a3a3a;
                    border-radius: 8px;
                }
            """)
            layout.addWidget(no_sublines_label)
        else:
            # Display each subline
            for subline in sublines:
                subline_widget = QWidget()
                subline_widget.setStyleSheet("""
                    QWidget {
                        background-color: #3a3a3a;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """)
                subline_layout = QHBoxLayout(subline_widget)
                subline_layout.setContentsMargins(12, 10, 12, 10)
                subline_layout.setSpacing(12)

                # Subline ID badge - responsive
                id_label = QLabel(f"#{subline['id']}")
                id_label.setStyleSheet("""
                    QLabel {
                        font-size: 12px;
                        font-weight: bold;
                        color: white;
                        background-color: #e67e22;
                        padding: 6px 12px;
                        border-radius: 12px;
                        min-width: 50px;
                        max-width: 80px;
                    }
                """)
                id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                id_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                subline_layout.addWidget(id_label)

                # Subline information - responsive
                info_widget = QWidget()
                info_layout = QVBoxLayout(info_widget)
                info_layout.setSpacing(2)
                info_layout.setContentsMargins(0, 0, 0, 0)

                # Subline name - responsive
                name_label = QLabel(subline.get('name', 'Unknown'))
                name_label.setWordWrap(True)
                name_label.setStyleSheet("""
                    QLabel {
                        font-size: 13px;
                        color: #ffffff;
                        font-weight: 500;
                        padding: 2px 0px;
                    }
                """)
                name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                info_layout.addWidget(name_label)

                # Direction if available - responsive
                if subline.get('direction'):
                    direction_label = QLabel(f"Direction: {subline['direction']}")
                    direction_label.setStyleSheet("""
                        QLabel {
                            font-size: 11px;
                            color: #cccccc;
                            font-style: italic;
                            padding: 1px 0px;
                        }
                    """)
                    direction_label.setWordWrap(True)
                    direction_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                    info_layout.addWidget(direction_label)

                info_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                subline_layout.addWidget(info_widget, stretch=1)

                # Add button to open window - responsive
                open_button = QPushButton("Abrir")
                open_button.setFixedHeight(35)
                open_button.setMinimumWidth(50)
                open_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 11px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:pressed {
                        background-color: #3d8b40;
                    }
                """)

                # Connect button to open window
                open_button.clicked.connect(
                    lambda checked, lid=line_id, sid=subline['id'], sname=subline.get('name', 'Unknown'):
                    self.on_subline_button_clicked(lid, sid, sname)
                )

                subline_layout.addWidget(open_button)
                layout.addWidget(subline_widget)

        # Replace existing content
        old_widget = self.view.scrollArea_3.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        self.view.scrollArea_3.setWidget(container)
        print(f"Displayed {len(sublines) if sublines else 0} sublines for line {line_id}")

    def _show_empty_sublines(self) -> None:
        """Display empty sublines area."""
        container = QWidget()
        layout = QVBoxLayout(container)
        empty_label = QLabel("Unable to load sublines.")
        empty_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #e74c3c;
                padding: 15px;
                background-color: #4a2a2a;
                border-radius: 8px;
            }
        """)
        layout.addWidget(empty_label)

        old_widget = self.view.scrollArea_3.takeWidget()
        if old_widget:
            old_widget.deleteLater()
        self.view.scrollArea_3.setWidget(container)

    def _display_arrivals(self, arrivals: List[Dict[str, Any]]) -> None:
        """
        Display bus arrival information in the scrollable results area.

        Args:
            arrivals: List of arrival dictionaries from the API.
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(8)

        for bus in arrivals:
            # Create arrival information block
            arrival_block = self._create_arrival_block(bus)
            layout.addWidget(arrival_block)

        # Replace existing content
        old_widget = self.view.scrollArea.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        self.view.scrollArea.setWidget(container)

    def _create_arrival_block(self, bus: Dict[str, Any]) -> QWidget:
        """
        Create a UI block displaying information for a single bus arrival.

        Args:
            bus: Dictionary containing bus arrival data.

        Returns:
            QWidget: Configured widget block with bus information.
        """
        block = QWidget()
        block.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QVBoxLayout(block)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(4)

        # Line number with color - responsive
        line_label = QLabel(f"<b>Line {bus['line']}</b>")
        line_label.setStyleSheet(
            f"color: {bus['color']}; font-size: 16px; font-weight: bold; padding: 2px 0px;"
        )
        line_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        line_label.setWordWrap(True)

        # Destination - responsive
        dest_label = QLabel(bus['dest'])
        dest_label.setStyleSheet("font-size: 13px; color: #666666; padding: 1px 0px;")
        dest_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        dest_label.setWordWrap(True)

        # Arrival time - responsive
        time_label = QLabel(bus['time'])
        time_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #d32f2f; padding: 2px 0px;")
        time_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        time_label.setWordWrap(True)

        layout.addWidget(line_label)
        layout.addWidget(dest_label)
        layout.addWidget(time_label)

        return block

    def _show_error_message(self, title: str, message: str, icon: QMessageBox.Icon) -> None:
        """
        Display an error message dialog to the user.

        Args:
            title: Dialog window title.
            message: Error message text.
            icon: QMessageBox icon type.
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()