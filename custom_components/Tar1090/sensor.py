import requests
from homeassistant.helpers.entity import Entity
from math import radians, cos, sin, sqrt, atan2, degrees

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def bearing(lat1, lon1, lat2, lon2):
    dlon = radians(lon2 - lon1)
    y = sin(dlon) * cos(radians(lat2))
    x = cos(radians(lat1)) * sin(radians(lat2)) - \
        sin(radians(lat1)) * cos(radians(lat2)) * cos(dlon)
    return (degrees(atan2(y, x)) + 360) % 360

class AirspaceCountSensor(Entity):
    def __init__(self, name, url, lat, lon):
        self._attr_name = name
        self._attr_unique_id = "airspace_current_count"
        self.url = url
        self.rx_lat = lat
        self.rx_lon = lon

    def fetch_data(self):
        try:
            r = requests.get(self.url, timeout=5)
            return r.json().get("aircraft", [])
        except Exception:
            return []

    def enrich_flights(self, aircraft):
        enriched = []
        for ac in aircraft:
            flight = ac.get("flight", "").strip()
            lat = ac.get("lat")
            lon = ac.get("lon")
            alt = ac.get("alt_baro") or ac.get("alt_geom")
            if flight and lat is not None and lon is not None and alt is not None:
                dist = round(haversine(self.rx_lat, self.rx_lon, lat, lon), 1)
                brng = round(bearing(self.rx_lat, self.rx_lon, lat, lon), 1)
                enriched.append({
                    "flight_number": flight,
                    "position": {"lat": lat, "lon": lon},
                    "altitude_ft": alt,
                    "distance_km": dist,
                    "bearing_deg": brng
                })
        return enriched

    @property
    def state(self):
        aircraft = self.fetch_data()
        return len(self.enrich_flights(aircraft))
    
    def setup_platform(hass, config, add_entities, discovery_info=None):
        url = config.get("url", "http://localhost:8080/data/aircraft.json")
        lat = config.get("latitude", 0)
        lon = config.get("longitude", 0)
        name = config.get("name", "Airspace Currently Tracking")
        add_entities([AirspaceCountSensor(name, url, lat, lon)])