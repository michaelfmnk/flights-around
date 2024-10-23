from typing import Optional

import requests
from math import radians, sin, cos, sqrt, atan2
from .models import Flight

class FlightsAPI:
    def __init__(self, opensky_url: str, adsb_url: str):
        self.opensky_url = opensky_url
        self.adsb_url = adsb_url

    def get_planes_around_location(self, latitude: float, longitude: float, radius_km: int):
        url = f"{self.opensky_url}/api/states/all"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            planes = data.get('states', [])
            return [
                {
                    'icao24': plane[0],
                    'callsign': plane[1],
                    'latitude': plane[6],
                    'longitude': plane[5],
                    'altitude': plane[7]
                }
                for plane in planes
                if plane[6] is not None and plane[5] is not None and self._haversine(latitude, longitude, plane[6], plane[5]) <= radius_km
            ]
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def get_destination_by_callsign(self, callsign: str) -> Optional[Flight]:
        url = f"{self.adsb_url}/v0/callsign/{callsign}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            route = data["response"]["flightroute"]
            origin = route["origin"]
            destination = route["destination"]
            return Flight(
                callsign=callsign,
                origin=origin["name"],
                origin_iata=origin["iata_code"],
                destination=destination["name"],
                destination_iata=destination["iata_code"]
            )
        else:
            return None

    @staticmethod
    def _haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c