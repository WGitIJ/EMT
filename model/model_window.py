"""
EMT Palma API Client

This module provides an interface to the EMT Palma public transportation API,
handling bus arrival times and line information for the Palma de Mallorca area.
"""

import requests


class EMTApi:
    """
    Client for EMT Palma MAAS API.

    Provides methods to retrieve bus line colors and arrival times for specific stops.
    Handles authentication, error management, and data transformation.
    """

    # API Authentication Token
    API_TOKEN = (
        "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJzdWIiOiI3ODQ1NTUiLCJpYXQiOjE3NjE1"
        "Njg2MjksImV4cCI6MzMzOTQ0ODYyOSwidXNlcm5hbWUiOiIxNzYxNTY4NjI4NzY1NVJCVUtTUk81"
        "SU9BWkVXTjE0T0EiLCJ0b2tlbl9kZXZpY2UiOiJkNTk2YzExMzQ4MDExNjExZTNmMmYzMzllNzJl"
        "YjgzYzFkNmY2Mzc3ODhhYjQyODNjMzc4YzYyNmIzYjZkOWFjIiwiZGV2aWNlX3R5cGVfaWQiOjMs"
        "InJvbGVzIjoiQU5PTklNTyJ9.8d6suKy2_5aw1H6pGktFIizOwUqIYb1piFGKfAQUlCywq7vuW6-"
        "rh_7y7VSwoqdl"
    )

    # API Configuration
    BASE_URL = "https://www.emtpalma.cat/maas/api/v1"
    REQUEST_TIMEOUT = 10
    MAX_RESULTS = 8

    def __init__(self) -> None:
        """Initialize the API client and load line information."""
        self.line_colors = self._load_line_colors()
        self.lines_data = self._load_lines_data()

    def _load_line_colors(self) -> dict:
        """
        Load bus line colors from the EMT API.

        Returns:
            dict: Mapping of line codes to hex color values.
                 Returns empty dict if loading fails.
        """
        try:
            endpoint = f"{self.BASE_URL}/agency/lines/"
            headers = self._get_headers()

            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if not response.ok:
                print("Warning: Failed to load line colors from API")
                return {}

            data = response.json()
            colors = {}

            for line in data:
                line_code = str(line.get("code", ""))
                route_color = line.get("routeColor", "757575")
                colors[line_code] = f"#{route_color}"

            print(f"Successfully loaded {len(colors)} line colors")
            return colors

        except requests.RequestException as e:
            print(f"Network error while loading line colors: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error loading line colors: {e}")
            return {}

    def _load_lines_data(self) -> dict:
        """
        Load complete bus line information from the EMT API.

        Returns:
            dict: Mapping of line codes to line information dictionaries.
                 Returns empty dict if loading fails.
        """
        try:
            endpoint = f"{self.BASE_URL}/agency/lines/"
            headers = self._get_headers()

            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if not response.ok:
                print("Warning: Failed to load lines data from API")
                return {}

            data = response.json()
            lines_info = {}

            for line in data:
                line_code = str(line.get("code", ""))
                if line_code:
                    lines_info[line_code] = {
                        "id": line_code,
                        "name": line.get("name", ""),
                        "long_name": line.get("longName", ""),
                        "color": f"#{line.get('routeColor', '757575')}"
                    }

            print(f"Successfully loaded {len(lines_info)} lines information")
            return lines_info

        except requests.RequestException as e:
            print(f"Network error while loading lines data: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error loading lines data: {e}")
            return {}

    def get_arrivals(self, stop_id: int) -> list | str:
        """
        Retrieve arrival times for a specific bus stop.

        Args:
            stop_id: The numeric identifier of the bus stop.

        Returns:
            list: List of arrival dictionaries with keys:
                 - 'line': Line number
                 - 'color': Line color (hex)
                 - 'dest': Destination
                 - 'time': Arrival time string
            str: Error code if request fails:
                 - 'token_expired': Authentication failed
                 - 'no_internet': Network/connection error
                 - 'invalid_stop': Stop not found or no data available
        """
        try:
            endpoint = f"{self.BASE_URL}/agency/stops/{stop_id}/timestr"
            headers = self._get_headers()

            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
                return "token_expired"

            if not response.ok:
                return "no_internet"

            data = response.json()

            if not isinstance(data, list) or not data:
                return "invalid_stop"

            arrivals = []

            for entry in data:
                line_code = str(entry.get("lineCode", "N/A"))
                vehicles = entry.get("vehicles", [])

                for vehicle in vehicles:
                    destination = (vehicle.get("destination") or "Unknown")[:30]
                    seconds_remaining = vehicle.get("seconds", 0)
                    minutes_remaining = max(0, seconds_remaining // 60)

                    arrival_time = "Now" if minutes_remaining == 0 else f"{minutes_remaining}min"
                    line_color = self.line_colors.get(line_code, "#757575")

                    arrivals.append({
                        "line": line_code,
                        "color": line_color,
                        "dest": destination,
                        "time": arrival_time
                    })

            return arrivals[:self.MAX_RESULTS]

        except requests.exceptions.ConnectionError:
            return "no_internet"
        except requests.exceptions.Timeout:
            return "no_internet"
        except Exception as e:
            print(f"Unexpected error retrieving arrivals: {e}")
            return "no_internet"

    def _get_headers(self) -> dict:
        """
        Get standard HTTP headers for API requests.

        Returns:
            dict: Headers dictionary with authorization and user agent.
        """
        return {
            "accept": "*/*",
            "authorization": self.API_TOKEN,
            "user-agent": "EMT-Palma-Client/1.0"
        }

    def get_all_lines(self) -> dict | str:
        """
        Retrieve all available bus lines information.

        Returns:
            dict: Dictionary of line codes to line information.
            str: Error code if request fails.
        """
        return self.lines_data if self.lines_data else "no_data"

    def get_line_sublines(self, line_id: int | str) -> list | str:
        try:
            endpoint = f"{self.BASE_URL}/agency/lines/{line_id}/sublines"
            headers = self._get_headers()

            print(f"Requesting sublines for line {line_id}: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
                return "token_expired"

            if not response.ok:
                print(f"API request failed with status {response.status_code}: {response.text[:200]}")
                return "no_internet"

            data = response.json()
            print(f"API response received: {type(data)}")

            # Handle different response formats
            if isinstance(data, dict):
                if "sublines" in data:
                    data = data["sublines"]
                elif "subLines" in data:
                    data = data["subLines"]
                elif "data" in data:
                    data = data["data"]
                else:
                    print(f"Unexpected dict response format: {list(data.keys())}")
                    return "invalid_data"

            if not isinstance(data, list):
                print(f"Expected list, got {type(data)}")
                return "invalid_data"

            sublines = []
            for subline in data:
                subline_id = subline.get("subLineId") or subline.get("id") or subline.get("sublineId") or subline.get("code")
                name = subline.get("shortName") or subline.get("longName") or subline.get("name") or subline.get("description") or subline.get("sublineName", "")
                direction = subline.get("longName") or subline.get("direction") or subline.get("way") or ""

                if subline_id is not None:
                    sublines.append({
                        "id": str(subline_id),
                        "name": name,
                        "direction": direction
                    })

            print(f"Successfully parsed {len(sublines)} sublines for line {line_id}")
            return sublines

        except requests.exceptions.ConnectionError:
            print("Connection error while fetching sublines")
            return "no_internet"
        except requests.exceptions.Timeout:
            print("Timeout error while fetching sublines")
            return "no_internet"
        except Exception as e:
            print(f"Unexpected error fetching sublines: {e}")
            import traceback
            traceback.print_exc()
            return "no_internet"

    def get_line_stops(self, line_id: int | str) -> list | str:
        """
        Get stops for a specific bus line.

        Args:
            line_id: The line identifier

        Returns:
            list: List of stops with coordinates and information
            str: Error code if request fails
        """
        try:
            endpoint = f"{self.BASE_URL}/agency/stops?line={line_id}"
            headers = self._get_headers()

            print(f"Requesting stops for line {line_id}: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
                return "token_expired"

            if not response.ok:
                print(f"API request failed with status {response.status_code}: {response.text[:200]}")
                return "no_internet"

            data = response.json()
            print(f"API response received: {type(data)}")

            if not isinstance(data, list):
                print(f"Expected list, got {type(data)}")
                return "invalid_data"

            stops = []
            for stop in data:
                stop_id = stop.get("id") or stop.get("stopCode")
                name = stop.get("stopName") or stop.get("stopDesc", "Sin nombre")

                # Get coordinates
                lat = stop.get("stopLat")
                lng = stop.get("stopLon")

                # Convert coordinates to float if they exist
                try:
                    if lat is not None and lng is not None:
                        lat = float(lat)
                        lng = float(lng)
                    else:
                        # Skip stops without coordinates
                        continue
                except (ValueError, TypeError):
                    continue

                if stop_id is not None:
                    stops.append({
                        "id": str(stop_id),
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    })

            print(f"Successfully parsed {len(stops)} stops for line {line_id}")
            return stops[:20]  # Limit to 20 stops for performance

        except requests.exceptions.ConnectionError:
            print("Connection error while fetching line stops")
            return "no_internet"
        except requests.exceptions.Timeout:
            print("Timeout error while fetching line stops")
            return "no_internet"
        except Exception as e:
            print(f"Unexpected error fetching line stops: {e}")
            import traceback
            traceback.print_exc()
            return "no_internet"
