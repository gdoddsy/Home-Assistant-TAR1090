from homeassistant.helpers.entity import Entity
from datetime import datetime
import logging
import os
import json
from .airspace_utils import get_data_path

_LOGGER = logging.getLogger(__name__)

class AirspaceHistorySensor(Entity):
    def __init__(self, entry_data):
        self._attr_name = "Airspace History Today"
        self._attr_unique_id = "airspace_history_today"
        self._attr_icon = "mdi:radar"
        self._attr_state = None
        self._attr_extra_state_attributes = {}
        self.date_key = datetime.now().strftime("%Y-%m-%d")

         # 🧭 Set relative path to flight log inside your component folder
        self.data_path = get_data_path(f"flight_log_{self.date_key}.json")

    async def async_update(self):
        last_seen_map = {}
        unique_flights = []
        total_seen = 0
        furthest = {}

        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r") as f:
                    history = json.load(f)

                # 🛩️ Flight timestamps
                daily_log = history.get("flights", {})
                if isinstance(daily_log, dict):
                    last_seen_map = daily_log
                    unique_flights = sorted(last_seen_map.keys())
                    total_seen = len(unique_flights)

                # 📡 Furthest flight
                furthest = history.get("furthest", {})

            except Exception as e:
                _LOGGER.error(f"Failed to read flight log for {self.date_key}: {e}")

        # 🧠 Set state and attributes
        self._attr_state = total_seen
        self._attr_extra_state_attributes = {
            "unique_flights": unique_flights,
            "last_seen": last_seen_map,
            "total_flights_seen": total_seen,
            "furthest_flight": furthest
        }