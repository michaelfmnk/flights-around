from math import radians, sin, cos, sqrt, atan2

import requests


# Helper function to calculate the distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


class FlightsAPI:
    def __init__(self, opensky_url, adsb_url):
        self.opensky_url = opensky_url
        self.adsb_url = adsb_url
        pass

    # Function to get planes around a specific location
    def get_planes_around_location(self, latitude, longitude, radius_km=50):
        # OpenSky API URL
        url = f"{self.opensky_url}/api/states/all"
        try:
            # Send request to OpenSky API
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                planes = data.get('states', [])
                planes_nearby = []

                # Iterate over the planes to find those within the specified radius
                for plane in planes:
                    plane_lat = plane[6]
                    plane_lon = plane[5]
                    plane_altitude = plane[7]

                    # Check if latitude and longitude are available
                    if plane_lat is not None and plane_lon is not None:
                        # Calculate distance to the plane
                        distance = haversine(latitude, longitude, plane_lat, plane_lon)
                        if distance <= radius_km:
                            planes_nearby.append({
                                'icao24': plane[0],
                                'callsign': plane[1],
                                'origin_country': plane[2],
                                'latitude': plane_lat,
                                'longitude': plane_lon,
                                'altitude': plane_altitude
                            })

                # Print out the nearby planes
                return planes_nearby
            else:
                print(f"Error fetching data: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def get_destination_by_callsign(self, callsign: str) -> (str, str):
        url = f"{self.adsb_url}/v0/callsign/{callsign}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            route = data["response"]["flightroute"]
            origin = route["origin"]
            destination = route["destination"]
            return "{} ({})".format(origin["name"], origin["iata_code"]), "{} ({})".format(destination["name"],
                                                                                           destination["iata_code"])
