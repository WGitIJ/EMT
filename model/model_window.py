import requests

class EMTApi:
<<<<<<< Updated upstream

    TOKEN = (
        "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJzdWIiOiI3ODQ1NTUiLCJpYXQiOjE3NjE1Njg2MjksImV4cCI6MzMzOTQ0ODYyOSwidXNlcm5hbWUiOiIxNzYxNTY4NjI4NzY1NVJCVUtTUk81SU9BWkVXTjE0T0EiLCJ0b2tlbl9kZXZpY2UiOiJkNTk2YzExMzQ4MDExNjExZTNmMmYzMzllNzJlYjgzYzFkNmY2Mzc3ODhhYjQyODNjMzc4YzYyNmIzYjZkOWFjIiwiZGV2aWNlX3R5cGVfaWQiOjMsInJvbGVzIjoiQU5PTklNTyJ9.8d6suKy2_5aw1H6pGktFIizOwUqIYb1piFGKfAQUlCywq7vuW6-rh_7y7VSwoqdl"
    )

    def __init__(self):
        self.line_colors = self.load_line_colors()
        # Caché opcional de paradas: id -> nombre
        self._stops_by_id = None

    # --------------------------------------------------------
    # Carga de colores de líneas
    # --------------------------------------------------------
    def load_line_colors(self):
        try:
            # ✅ Endpoint correcto: líneas con sus colores
            url = "https://www.emtpalma.cat/maas/api/v1/agency/lines/"
            headers = {
                "accept": "*/*",
                "authorization": self.TOKEN,
                "user-agent": "Mozilla/5.0"
            }
=======
    API_TOKEN = (
        "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJzdWIiOiI3ODQ1NTUiLCJpYXQiOjE3NjE1"
        "Njg2MjksImV4cCI6MzMzOTQ0ODYyOSwidXNlcm5hbWUiOiIxNzYxNTY4NjI4NzY1NVJCVUtTUk81"
        "SU9BWkVXTjE0T0EiLCJ0b2tlbl9kZXZpY2UiOiJkNTk2YzExMzQ4MDExNjExZTNmMmYzMzllNzJl"
        "YjgzYzFkNmY2Mzc3ODhhYjQyODNjMzc4YzYyNmIzYjZkOWFjIiwiZGV2aWNlX3R5cGVfaWQiOjMs"
        "InJvbGVzIjoiQU5PTklNTyJ9.8d6suKy2_5aw1H6pGktFIizOwUqIYb1piFGKfAQUlCywq7vuW6-"
        "rh_7y7VSwoqdl"
    )

    BASE_URL = "https://www.emtpalma.cat/maas/api/v1"
    REQUEST_TIMEOUT = 10
    MAX_RESULTS = 8

    def __init__(self) -> None:
        self.line_colors = self._load_line_colors()
        self.lines_data = self._load_lines_data()

    def _load_line_colors(self) -> dict:
        try:
            endpoint = f"{self.BASE_URL}/agency/lines/"
            headers = self._get_headers()
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)
>>>>>>> Stashed changes

            response = requests.get(url, headers=headers, timeout=10)
            if not response.ok:
                print("[WARN] No se pudieron obtener colores de líneas.")
                return {}

            data = response.json()

            colors = {}
            for line in data:
                code = str(line.get("code"))                     # ← campo real de tu JSON
                color = "#" + line.get("routeColor", "757575")   # ← routeColor sin almohadilla
                colors[code] = color

            return colors

        except Exception as e:
<<<<<<< Updated upstream
            print(f"[ERROR] No se pudieron cargar colores: {e}")
            return {}

    # --------------------------------------------------------
    # Listado de todas las paradas
    # --------------------------------------------------------
    def get_all_stops(self):
        try:
            url = "https://www.emtpalma.cat/maas/api/v1/agency/lines/"
            headers = {
                "accept": "*/*",
                "authorization": self.TOKEN,
                "user-agent": "Mozilla/5.0",
            }

            r = requests.get(url, headers=headers, timeout=15)

            if r.status_code == 401:
=======
            print(f"Error loading line colors: {e}")
            return {}

    def _load_lines_data(self) -> dict:
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

        except Exception as e:
            print(f"Error loading lines data: {e}")
            return {}

    def get_arrivals(self, stop_id: int) -> list | str:
        try:
            endpoint = f"{self.BASE_URL}/agency/stops/{stop_id}/timestr"
            headers = self._get_headers()
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
>>>>>>> Stashed changes
                return "token_expired"

            if not r.ok:
                return "no_internet"

            data = r.json()
            if not isinstance(data, list):
                return "no_internet"

            stops = []
            for s in data:
                # El 'code' es lo que se muestra (A1, A2, etc.)
                line_code = s.get("code")
                # El 'id' es el identificador numérico para las APIs
                line_id = s.get("id")
                name = s.get("name") or s.get("description") or "Sin nombre"

                if line_code is None or line_id is None:
                    continue

                line_code_str = str(line_code)
                # Obtener el color de la línea usando el código
                color = self.line_colors.get(line_code_str, "#757575")  # Color por defecto gris
                stops.append({
                    "id": line_code_str,  # Código de la línea para mostrar
                    "name": name,
                    "color": color,
                    "lineId": str(line_id)  # ID numérico para APIs de sublíneas/paradas
                })

            # Actualizamos la caché de paradas para búsquedas rápidas por id
            self._stops_by_id = {s["id"]: s["name"] for s in stops}

            return stops

        except Exception as e:
            print(f"[ERROR get_all_stops] {e}")
            return "no_internet"

<<<<<<< Updated upstream
    # --------------------------------------------------------
    # Obtener nombre de una parada concreta
    # --------------------------------------------------------
    def get_stop_name(self, stop_id: int | str):
        """
        Devuelve el nombre de la parada (str) o None si no se encuentra
        o si hubo algún problema al cargar los datos.
        """
        # Aseguramos que la caché está cargada
        if self._stops_by_id is None:
            stops = self.get_all_stops()
            if isinstance(stops, str):
                # "no_internet" / "token_expired"
                return None

        if self._stops_by_id is None:
            return None

        return self._stops_by_id.get(str(stop_id))
=======
    def _get_headers(self) -> dict:
        return {
            "accept": "*/*",
            "authorization": self.API_TOKEN,
            "user-agent": "EMT-Palma-Client/1.0"
        }

    def get_all_lines(self) -> dict | str:
        return self.lines_data if self.lines_data else "no_data"
>>>>>>> Stashed changes

    # --------------------------------------------------------
    # Consulta de tiempos de llegada
    # --------------------------------------------------------
    def get_arrivals(self, stop_id: int):
        try:
<<<<<<< Updated upstream
            url = f"https://www.emtpalma.cat/maas/api/v1/agency/stops/{stop_id}/timestr"
            headers = {
                "accept": "*/*",
                "authorization": self.TOKEN,
                "user-agent": "Mozilla/5.0"
            }

            r = requests.get(url, headers=headers, timeout=10)
=======
            endpoint = f"{self.BASE_URL}/agency/lines/{line_id}/sublines"
            headers = self._get_headers()
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)
>>>>>>> Stashed changes

            # 🔒 Token caducado
            if r.status_code == 401:
                return "token_expired"

<<<<<<< Updated upstream
            # ❌ Error de red o servidor
            if not r.ok:
                return "no_internet"

            data = r.json()
            if not isinstance(data, list) or len(data) == 0:
                return "invalid_stop"

            result = []

            for entry in data:
                line = str(entry.get("lineCode", "N/A"))
                vehicles = entry.get("vehicles", [])

                for v in vehicles:
                    dest = (v.get("destination") or "Sin destino")[:30]
                    seconds = v.get("seconds", 0)
                    mins = max(0, int(seconds / 60))
                    time_str = "YA" if mins == 0 else f"{mins}'"

                    # ✅ Ahora sí obtendrá colores reales
                    color = self.line_colors.get(line, "#757575")

                    result.append({
                        "line": line,
                        "color": color,
                        "dest": dest,
                        "time": time_str
                    })

            return result[:8]

        except requests.exceptions.ConnectionError:
            return "no_internet"
        except requests.exceptions.Timeout:
            return "no_internet"
        except Exception as e:
            print(f"[ERROR get_arrivals] {e}")
            return "no_internet"

    # --------------------------------------------------------
    # Obtener paradas de una línea específica
    # --------------------------------------------------------
    def get_line_stops(self, stop_id: int | str):
        """
        Obtiene las paradas de una línea específica usando la API.
        stop_id: El stopId obtenido de la respuesta de get_all_stops(), no el código de la línea.
        Devuelve una lista de paradas o un código de error.
        """
        try:
            headers = {
                "accept": "*/*",
                "authorization": self.TOKEN,
                "user-agent": "Mozilla/5.0"
            }
            
            # Usar el stopId directamente en la URL según el formato proporcionado
            # El tripId puede ser opcional o podemos intentar obtenerlo primero
            trip_id = 994  # Valor por defecto del ejemplo
            
            # Probar diferentes variaciones de la URL usando stopId
            url_variations = [
                f"https://www.emtpalma.cat/maas/api/v1/agency/lines/{stop_id}//stops?tripId={trip_id}&isLine=0&isLineNearStop=0&both=1",
                f"https://www.emtpalma.cat/maas/api/v1/agency/lines/{stop_id}/stops?tripId={trip_id}&isLine=0&isLineNearStop=0&both=1",
                f"https://www.emtpalma.cat/maas/api/v1/agency/lines/{stop_id}/stops",
                f"https://www.emtpalma.cat/maas/api/v1/agency/lines/{stop_id}/stops?tripId={trip_id}",
            ]
            
            for url in url_variations:
                print(f"[INFO] Intentando URL: {url}")
                r = requests.get(url, headers=headers, timeout=10)
                
                # Token caducado
                if r.status_code == 401:
                    print(f"[ERROR get_line_stops] Token caducado. Status: {r.status_code}")
                    return "token_expired"
                
                # Si funciona, usar esta URL
                if r.ok:
                    print(f"[SUCCESS] URL funcionó: {url}")
                    break
                else:
                    print(f"[WARN] URL falló con código {r.status_code}: {url}")
                    print(f"[WARN] Response: {r.text[:200]}")
            else:
                # Si ninguna URL funcionó
                print(f"[ERROR get_line_stops] Todas las URLs fallaron. Último código: {r.status_code}")
                print(f"[ERROR get_line_stops] Última respuesta: {r.text[:200]}")
                return "no_internet"

            # Si llegamos aquí, r.ok es True
            try:
                data = r.json()
            except Exception as e:
                print(f"[ERROR get_line_stops] No se pudo parsear JSON: {e}")
                print(f"[ERROR get_line_stops] Response text: {r.text[:500]}")
                return "no_internet"
            
            # La respuesta puede ser un diccionario o una lista
            if isinstance(data, dict):
                # Si es un diccionario, buscar la clave que contiene las paradas
                if "stops" in data:
                    data = data["stops"]
                elif "data" in data:
                    data = data["data"]
                else:
                    print(f"[ERROR get_line_stops] Formato de respuesta inesperado: {list(data.keys())}")
                    return "no_internet"
            
=======
            if not response.ok:
                print(f"Sublines request failed with status {response.status_code}: {response.text[:200]}")
                return "no_internet"

            data = response.json()

            if isinstance(data, dict):
                data = data.get("sublines") or data.get("subLines") or data.get("data") or []

>>>>>>> Stashed changes
            if not isinstance(data, list):
                print(f"[ERROR get_line_stops] La respuesta no es una lista: {type(data)}")
                return "no_internet"

            stops = []
            for stop in data:
                stop_id = stop.get("id") or stop.get("stopId") or stop.get("code") or stop.get("stopCode")
                name = stop.get("name") or stop.get("description") or stop.get("stopName") or "Sin nombre"
                
                if stop_id is None:
                    continue
                
                stops.append({
                    "id": str(stop_id),
                    "name": name
                })

            print(f"[INFO get_line_stops] Se encontraron {len(stops)} paradas para stopId {stop_id}")
            return stops

<<<<<<< Updated upstream
        except requests.exceptions.ConnectionError as e:
            print(f"[ERROR get_line_stops] Error de conexión: {e}")
            return "no_internet"
        except requests.exceptions.Timeout as e:
            print(f"[ERROR get_line_stops] Timeout: {e}")
            return "no_internet"
        except Exception as e:
            print(f"[ERROR get_line_stops] Error inesperado: {e}")
            import traceback
            traceback.print_exc()
            return "no_internet"

    # --------------------------------------------------------
    # Obtener sublíneas de una línea específica
    # --------------------------------------------------------
    def get_line_sublines(self, line_id: int | str):
        """
        Obtiene las sublíneas de una línea específica usando la API.
        Devuelve una lista de sublíneas o un código de error.
        """
        try:
            headers = {
                "accept": "*/*",
                "authorization": self.TOKEN,
                "user-agent": "Mozilla/5.0"
            }

            # URL para obtener sublíneas
            url = f"https://www.emtpalma.cat/maas/api/v1/agency/lines/{line_id}/sublines"
            print(f"[INFO] Intentando obtener sublíneas de la línea {line_id}: {url}")

            r = requests.get(url, headers=headers, timeout=10)

            # Token caducado
            if r.status_code == 401:
                print(f"[ERROR get_line_sublines] Token caducado. Status: {r.status_code}")
                return "token_expired"

            # Error de red o servidor
            if not r.ok:
                print(f"[ERROR get_line_sublines] Error HTTP {r.status_code}. URL: {url}")
                print(f"[ERROR get_line_sublines] Response: {r.text[:200]}")
                return "no_internet"

            data = r.json()

            # La respuesta puede ser un diccionario o una lista
            if isinstance(data, dict):
                # Si es un diccionario, buscar la clave que contiene las sublíneas
                if "sublines" in data:
                    data = data["sublines"]
                elif "data" in data:
                    data = data["data"]
                else:
                    print(f"[ERROR get_line_sublines] Formato de respuesta inesperado: {list(data.keys())}")
                    return "no_internet"

            if not isinstance(data, list):
                print(f"[ERROR get_line_sublines] La respuesta no es una lista: {type(data)}")
                return "no_internet"

            sublines = []
            for subline in data:
                # Según la respuesta real: subLineId, longName, shortName, etc.
                subline_id = subline.get("subLineId") or subline.get("id") or subline.get("sublineId")
                long_name = subline.get("longName")
                short_name = subline.get("shortName")
                name = long_name or short_name or subline.get("name") or "Sin nombre"
                direction = subline.get("direction") or subline.get("destiny") or "Sin dirección"

                if subline_id is None:
                    continue

                sublines.append({
                    "id": str(subline_id),
                    "name": name,
                    "direction": direction
                })

            print(f"[INFO get_line_sublines] Se encontraron {len(sublines)} sublíneas para la línea {line_id}")
            return sublines

        except requests.exceptions.ConnectionError as e:
            print(f"[ERROR get_line_sublines] Error de conexión: {e}")
            return "no_internet"
        except requests.exceptions.Timeout as e:
            print(f"[ERROR get_line_sublines] Timeout: {e}")
            return "no_internet"
        except Exception as e:
            print(f"[ERROR get_line_sublines] Error inesperado: {e}")
            import traceback
            traceback.print_exc()
            return "no_internet"

    # --------------------------------------------------------
    # Obtener paradas de una sublínea específica
    # --------------------------------------------------------
    def get_subline_stops(self, subline_id):
        import requests
        url = f"https://www.emtpalma.cat/maas/api/v1/agency/sublines/{subline_id}/stops"
        headers = {
            "accept": "*/*",
            "authorization": self.TOKEN,
            "user-agent": "Mozilla/5.0"
        }
        r = requests.get(url, headers=headers, timeout=10)
        if not r.ok:
            return []
        try:
            data = r.json()
        except Exception:
            return []
        if isinstance(data, dict):
            data = data.get("stops") or data.get("data") or []
        return data
=======
            print(f"Successfully parsed {len(sublines)} sublines for line {line_id}")
            return sublines

        except Exception as e:
            print(f"Unexpected error fetching sublines: {e}")
            return "no_internet"

    def get_subline_trip_ids(self, subline_id: str) -> list[str]:
        endpoint = f"{self.BASE_URL}/agency/lines/directions-subline?subLineId={subline_id}"
        headers = self._get_headers()

        try:
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
                print("Token expirado")
                return []

            if not response.ok:
                print(f"directions-subline falló: {response.status_code}")
                return []

            data = response.json()

            if not isinstance(data, list):
                print("Respuesta inesperada (no lista)")
                return []

            trip_ids = []
            for item in data:
                trip_id = item.get("tripId")
                if trip_id is not None:
                    trip_ids.append(str(trip_id))

            print(f"Trip IDs encontrados para subline {subline_id}: {trip_ids}")
            return trip_ids

        except Exception as e:
            print(f"Error en directions-subline: {e}")
            return []

    def get_subline_stops(self, line_id: str, trip_id: str) -> list:
        endpoint = (
            f"{self.BASE_URL}/agency/lines/{line_id}/stops"
            f"?tripId={trip_id}&isLine=0&isLineNearStop=0&both=1"
        )
        headers = self._get_headers()

        try:
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
                print("Token expirado en stops")
                return []

            if not response.ok:
                print(f"Stops falló: {response.status_code}")
                return []

            data = response.json()

            if not isinstance(data, list):
                print("Respuesta de stops inesperada")
                return []

            stops = []
            for item in data:
                stop_id = item.get("stopCode") or item.get("id") or item.get("stopGtfsId")
                name = item.get("stopName") or item.get("stopDesc") or "Parada"
                lat = item.get("stopLat")
                lon = item.get("stopLon")

                if stop_id and lat is not None and lon is not None:
                    try:
                        stops.append({
                            "id": str(stop_id),
                            "name": name,
                            "lat": float(lat),
                            "lon": float(lon)
                        })
                    except ValueError:
                        continue

            print(f"Stops: {len(stops)} paradas encontradas para tripId {trip_id}")
            return stops

        except Exception as e:
            print(f"Error en stops: {e}")
            return []

    def get_subline_shape(self, line_id: str, trip_id: str) -> list:
        endpoint = f"{self.BASE_URL}/agency/lines/{line_id}/shape?tripId={trip_id}"
        headers = self._get_headers()

        try:
            response = requests.get(endpoint, headers=headers, timeout=self.REQUEST_TIMEOUT)

            if response.status_code == 401:
                print("Token expirado en shape")
                return []

            if not response.ok:
                print(f"Shape falló: {response.status_code}")
                return []

            data = response.json()

            if not isinstance(data, list):
                print("Respuesta de shape inesperada")
                return []

            shape_points = []
            for item in data:
                lat = item.get("latitude")
                lon = item.get("longitude")
                if lat is not None and lon is not None:
                    try:
                        shape_points.append([float(lat), float(lon)])
                    except ValueError:
                        continue

            print(f"Shape: {len(shape_points)} puntos de recorrido para tripId {trip_id}")
            return shape_points

        except Exception as e:
            print(f"Error en shape: {e}")
            return []
>>>>>>> Stashed changes
