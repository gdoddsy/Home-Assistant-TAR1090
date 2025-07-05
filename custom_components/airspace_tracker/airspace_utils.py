import logging
from math import radians, cos, sin, sqrt, atan2, degrees
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from datetime import datetime
import json
import os


_LOGGER = logging.getLogger(__name__)

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

def compass_direction(bearing_deg):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    return directions[round(bearing_deg / 45) % 8]

async def fetch_aircraft_data(hass, url):
    session = async_get_clientsession(hass)
    try:
        async with session.get(url, timeout=5) as response:
            data = await response.json()
            return data.get("aircraft", [])
    except Exception as e:
        _LOGGER.error(f"Failed to fetch aircraft data: {e}")
        return []

def enrich_aircraft(rx_lat, rx_lon, aircraft):
    enriched = []
    for ac in aircraft:
        flight = ac.get("flight", "").strip()
        lat = ac.get("lat")
        lon = ac.get("lon")
        alt = ac.get("alt_baro") or ac.get("alt_geom")
        if flight and lat is not None and lon is not None and alt is not None:
            dist = round(haversine(rx_lat, rx_lon, lat, lon), 1)
            brng = round(bearing(rx_lat, rx_lon, lat, lon), 1)
            enriched.append({
                "flight_number": flight,
                "position": {"lat": lat, "lon": lon},
                "altitude_ft": alt,
                "distance_km": dist,
                "bearing_deg": brng,
                "direction": compass_direction(brng)
            })
    return enriched

def log_flight_seen(flight_number, file_path="/config/flight_log_today.json", distance=None, position=None, direction=None, altitude=None):
    date_key = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        history = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                history = json.load(f)

        # 👣 Log flight timestamp
        flights_today = history.get(date_key, {})
        if not isinstance(flights_today, dict):
            flights_today = {}

        flights_today[flight_number] = timestamp
        history[date_key] = flights_today

        # ✈️ Check & update furthest
        if distance is not None and position:
            furthest_entry = history.get("furthest", {}).get(date_key, {})
            prev_distance = furthest_entry.get("distance_km", 0)
            if distance > prev_distance:
                history.setdefault("furthest", {})[date_key] = {
                    "flight": flight_number,
                    "position": position,
                    "distance_km": distance,
                    "direction": direction,
                    "altitude_ft": altitude,
                    "timestamp": timestamp
                }

        # 💾 Save it back
        with open(file_path, "w") as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        _LOGGER.error(f"Error saving flight {flight_number} to log: {e}")
