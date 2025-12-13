"""
Map Window Module

This module provides a window to display interactive maps using Folium and QWebEngineView.
Shows the route and stops for a specific bus line.
"""

import folium
from folium import plugins
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt


class MapWindow(QMainWindow):
    def __init__(self, line_id: str, subline_id: str, subline_name: str, model=None, parent=None):
        super().__init__(parent)
        self.line_id = line_id
        self.subline_id = subline_id
        self.subline_name = subline_name
        self.model = model

        self.setWindowTitle(f"Mapa - Línea {line_id}")
        self.setGeometry(200, 200, 1000, 700)
        self.setMinimumSize(800, 600)

        # Create web view for the map (fullscreen)
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Load and display the map
        self._load_map()


    def _load_map(self) -> None:
        """Load and display the map for the current line and subline."""
        try:
            # Get real stops for this line if model is available
            stops_data = []
            if self.model:
                stops_result = self.model.get_line_stops(self.line_id)
                if isinstance(stops_result, list) and stops_result:
                    stops_data = stops_result
                    print(f"Loaded {len(stops_data)} real stops for line {self.line_id}")
                else:
                    print(f"No real stops available for line {self.line_id}, using sample stops")

            # Create Folium map with stops and route
            map_html = self._create_folium_map(stops_data)

            # Load HTML into web view
            self.web_view.setHtml(map_html)

        except Exception as e:
            print(f"Error loading map: {e}")
            import traceback
            traceback.print_exc()

            error_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2>Error al cargar el mapa</h2>
                <p>{str(e)}</p>
                <p style="color: #666;">Error interno de la aplicación.</p>
                <p style="font-size: 12px; color: #999;">Línea: {self.line_id}, Sublínea: {self.subline_id}</p>
            </body>
            </html>
            """
            self.web_view.setHtml(error_html)

    def _create_folium_map(self, stops_data: list = None) -> str:
        """Create a Folium map with stops and route."""
        # Calculate center based on stops or use Palma coordinates
        if stops_data and len(stops_data) > 0:
            # Filter valid coordinates
            valid_stops = []
            for stop in stops_data:
                try:
                    lat = float(stop.get("lat"))
                    lng = float(stop.get("lng"))
                    if -90 <= lat <= 90 and -180 <= lng <= 180:
                        valid_stops.append({
                            "lat": lat,
                            "lng": lng,
                            "name": str(stop.get("name", "Sin nombre")).replace("'", "\\'")
                        })
                except (TypeError, ValueError):
                    continue

            if valid_stops:
                # Calculate center
                avg_lat = sum(stop['lat'] for stop in valid_stops) / len(valid_stops)
                avg_lng = sum(stop['lng'] for stop in valid_stops) / len(valid_stops)
                zoom_level = 13
            else:
                # Fallback to Palma
                avg_lat, avg_lng = 39.5696, 2.6502
                zoom_level = 12
                valid_stops = []
        else:
            # Generate line-specific sample stops when no real data available
            valid_stops, avg_lat, avg_lng, zoom_level = self._generate_line_specific_stops()

        # Create Folium map
        m = folium.Map(
            location=[avg_lat, avg_lng],
            zoom_start=zoom_level,
            tiles='OpenStreetMap'
        )

        # Add stops as markers
        if valid_stops:
            for i, stop in enumerate(valid_stops[:15]):  # Limit to 15 stops for performance
                folium.Marker(
                    [stop['lat'], stop['lng']],
                    popup=f'<b>Parada {i+1}</b><br>{stop["name"]}',
                    tooltip=f'Parada {i+1}: {stop["name"]}',
                    icon=folium.Icon(color='blue', icon='bus', prefix='fa')
                ).add_to(m)

            # Add route line connecting stops
            if len(valid_stops) > 1:
                route_coords = [[stop['lat'], stop['lng']] for stop in valid_stops[:15]]
                folium.PolyLine(
                    route_coords,
                    color='red',
                    weight=4,
                    opacity=0.8,
                    popup=f'Ruta de la línea {self.line_id}'
                ).add_to(m)
        else:
            # Add default marker for this line (centered)
            folium.Marker(
                [avg_lat, avg_lng],
                popup=f'Línea {self.line_id} - {self.subline_name}',
                tooltip=f'Línea {self.line_id}',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

            # Add circle around the center
            folium.Circle(
                radius=1000,
                location=[avg_lat, avg_lng],
                color='blue',
                fill=True,
                fill_opacity=0.3,
                popup=f'Centro aproximado de la línea {self.line_id}'
            ).add_to(m)

        # Get HTML representation - clean and simple
        return m.get_root().render()

    def _generate_line_specific_stops(self):
        """Generate line-specific sample stops when real data is not available."""
        # Base coordinates for Palma center
        base_lat, base_lng = 39.5696, 2.6502

        # Generate different stops based on line_id to make each map unique
        line_num = int(self.line_id) if self.line_id.isdigit() else ord(self.line_id[0])

        # Create line-specific stops by offsetting coordinates
        stops = []
        num_stops = 8

        for i in range(num_stops):
            # Create variation based on line number and stop index
            lat_offset = (line_num * 0.001) + (i * 0.002) + (line_num % 3) * 0.001
            lng_offset = (line_num * 0.002) + (i * 0.0015) - (line_num % 2) * 0.001

            lat = base_lat + lat_offset
            lng = base_lng + lng_offset

            # Generate stop name based on line and position
            directions = ["Norte", "Sur", "Este", "Oeste", "Centro", "Terminal", "Intercambiador", "Plaza"]
            stop_name = f"Parada {directions[i % len(directions)]} - Línea {self.line_id}"

            stops.append({
                "lat": lat,
                "lng": lng,
                "name": stop_name
            })

        # Calculate center
        avg_lat = sum(stop['lat'] for stop in stops) / len(stops)
        avg_lng = sum(stop['lng'] for stop in stops) / len(stops)
        zoom_level = 13

        return stops, avg_lat, avg_lng, zoom_level

    def closeEvent(self, event):
        """Called when the window is closed."""
        print(f"MapWindow closed for line {self.line_id}")
        super().closeEvent(event)
