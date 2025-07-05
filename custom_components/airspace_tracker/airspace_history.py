from homeassistant.helpers.entity import Entity
from datetime import datetime
import logging
import os
import json

_LOGGER = logging.getLogger(__name__)

class AirspaceHistorySensor(Entity):
    def __init__(self, entry_data):
        self._attr_name = "Airspace History Today"
        self._attr_unique_id = "airspace_history_today"
        self._attr_icon = "mdi:radar"
        self._attr_state = None
        self._attr_extra_state_attributes = {}
        self.data_path = "/config/flight_log_today.json"
        self.furthest_path = "/config/furthest_flight.json"
        self.date_key = datetime.now().strftime("%Y-%m-%d")

    async def async_update(self):
        last_seen_map = {}
        unique_flights = []
        total_seen = 0
        history = {}
    
        # ✈️ Load flight codes with timestamps and furthest flight
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r") as f:
                    history = json.load(f)
    
                daily_log = history.get(self.date_key, {})
                if isinstance(daily_log, dict):
                    last_seen_map = daily_log
                    unique_flights = sorted(last_seen_map.keys())
                    total_seen = len(unique_flights)
            except Exception as e:
                _LOGGER.error(f"Failed to read flight log: {e}")
    
        # 📡 Load furthest flight from within history
        furthest = history.get("furthest", {}).get(self.date_key, {})
    
        # 🧠 Set state and attributes
        self._attr_state = total_seen
        self._attr_extra_state_attributes = {
            "unique_flights": unique_flights,
            "last_seen": last_seen_map,
            "total_flights_seen": total_seen,
            "furthest_flight": furthest
        }