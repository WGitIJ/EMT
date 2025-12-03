import requests

class EMTApi:

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
                return "token_expired"

            if not r.ok:
                return "no_internet"

            data = r.json()
            if not isinstance(data, list):
                return "no_internet"

            stops = []
            for s in data:
                # Algunos JSON usan 'code', otros 'stopCode' o 'id'
                raw_id = s.get("code") or s.get("stopCode") or s.get("id")
                name = s.get("name") or s.get("description") or "Sin nombre"

                if raw_id is None:
                    continue

                stop_id = str(raw_id)
                stops.append({"id": stop_id, "name": name})

            # Actualizamos la caché de paradas para búsquedas rápidas por id
            self._stops_by_id = {s["id"]: s["name"] for s in stops}

            return stops

        except requests.exceptions.ConnectionError:
            return "no_internet"
        except requests.exceptions.Timeout:
            return "no_internet"
        except Exception as e:
            print(f"[ERROR get_all_stops] {e}")
            return "no_internet"

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

    # --------------------------------------------------------
    # Consulta de tiempos de llegada
    # --------------------------------------------------------
    def get_arrivals(self, stop_id: int):
        try:
            url = f"https://www.emtpalma.cat/maas/api/v1/agency/stops/{stop_id}/timestr"
            headers = {
                "accept": "*/*",
                "authorization": self.TOKEN,
                "user-agent": "Mozilla/5.0"
            }

            r = requests.get(url, headers=headers, timeout=10)

            # 🔒 Token caducado
            if r.status_code == 401:
                return "token_expired"

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
