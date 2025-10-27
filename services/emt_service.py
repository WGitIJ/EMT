import requests
from typing import Dict, List, Optional

class EMTService:
    def __init__(self):
        self.base_url = "https://openbus.emtmadrid.es:9443/emt-proxy-server/last/geo"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })

    def get_arrivals(self, stop_id: str) -> Optional[Dict]:
        url = f"{self.base_url}/GetArriveStop.php"

        params = {
            'idStop': stop_id,
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or 'arrives' not in data:
                return {'arrivals': []}

            arrivals = []
            for arrive in data['arrives']:
                arrival_info = {
                    'line': arrive.get('lineId', 'N/A'),
                    'destination': arrive.get('destination', 'Unknown'),
                    'time': self.format_arrival_time(arrive),
                    'color': self.get_line_color(arrive.get('lineId', ''))
                }
                arrivals.append(arrival_info)

            return {'arrivals': arrivals}

        except requests.exceptions.ConnectionError:
            raise ConnectionError("Unable to connect to EMT service. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out. The EMT service may be slow or unavailable.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching data from EMT: {str(e)}")

    def format_arrival_time(self, arrive: Dict) -> str:
        bus_time_left = arrive.get('busTimeLeft', None)
        estimated_arrive = arrive.get('estimateArrive', None)

        if bus_time_left is not None:
            if bus_time_left == 0:
                return "Arriving now"
            elif bus_time_left < 60:
                return f"{bus_time_left} seconds"
            else:
                minutes = bus_time_left // 60
                return f"{minutes} min"
        elif estimated_arrive is not None:
            return f"~{estimated_arrive} min"
        else:
            return "N/A"

    def get_line_color(self, line_id: str) -> str:
        colors = {
            '1': '#1E3A8A',
            '2': '#DC2626',
            '3': '#16A34A',
            '5': '#059669',
            '6': '#7C3AED',
            '10': '#1D4ED8',
            '14': '#0891B2',
            '15': '#4F46E5',
            '27': '#B91C1C',
            '34': '#0EA5E9',
            '37': '#EA580C',
            '50': '#CA8A04',
            '146': '#8B5CF6',
            '147': '#EC4899',
        }
        return colors.get(line_id, '#374151')
