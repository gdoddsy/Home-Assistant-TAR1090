import logging
from math import radians, cos, sin, sqrt, atan2, degrees
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime
import json
import os
import asyncio



_LOGGER = logging.getLogger(__name__)

def get_data_path(filename):
    from pathlib import Path
    base_path = Path(__file__).parent / "data"
    base_path.mkdir(exist_ok=True)  # Ensure folder exists
    return str(base_path / filename)


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

# 📍 Reverse geocode
async def reverse_geocode(lat, lon):
    def blocking_lookup():
        try:
            geolocator = Nominatim(user_agent="airspace_snapshot")
            location = geolocator.reverse((lat, lon), language="en", timeout=10)
            return location.address if location else "Unknown"
        except GeocoderTimedOut:
            return "Timed out"
        except Exception as e:
            return f"Error: {e}"

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, blocking_lookup)

    
async def log_flight_seen(flight_number, distance=None, position=None, direction=None, altitude=None):
    date_key = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🔧 Compute full path like /config/custom_components/airspace_tracker/data/flight_log_2025-07-08.json
    file_path = get_data_path(f"flight_log_{date_key}.json")

    try:
        history = {}
        if os.path.exists(file_path):
            history = await asyncio.to_thread(load_history, file_path)

        # 👣 Log flight timestamp
        flights = history.get("flights", {})
        flights[flight_number] = timestamp
        history["flights"] = flights

        # ✈️ Check & update furthest
        if distance is not None and position:
            furthest_entry = history.get("furthest", {})
            prev_distance = furthest_entry.get("distance_km", 0)
            if distance > prev_distance:
                furthest_location = await reverse_geocode(position["lat"], position["lon"])
                history["furthest"] = {
                    "flight": flight_number,
                    "position": position,
                    "distance_km": distance,
                    "direction": direction,
                    "altitude_ft": altitude,
                    "timestamp": timestamp,
                    "location": furthest_location
                }

        # 💾 Save it back
        await asyncio.to_thread(save_history, file_path, history)


    except Exception as e:
        _LOGGER.error(f"Error saving flight {flight_number} to log: {e}")

def save_history(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        
def load_history(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

