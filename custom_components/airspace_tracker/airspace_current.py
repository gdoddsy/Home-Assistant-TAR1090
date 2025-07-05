from homeassistant.helpers.entity import Entity
import logging
from .airspace_utils import fetch_aircraft_data, enrich_aircraft, log_flight_seen


_LOGGER = logging.getLogger(__name__)

class AirspaceCurrentSensor(Entity):
    def __init__(self, entry_data):
        self._attr_name = "Airspace Currently Tracking"
        self._attr_unique_id = "airspace_current_count"
        self._attr_icon = "mdi:airplane-landing"
        self.url = entry_data["url"]
        self.rx_lat = entry_data["latitude"]
        self.rx_lon = entry_data["longitude"]
        self._attr_state = None
        self._attr_extra_state_attributes = {}


    async def async_update(self):
        #read JSON
        aircraft = await fetch_aircraft_data(self.hass, self.url)
        
        #populate my objects
        enriched = enrich_aircraft(self.rx_lat, self.rx_lon, aircraft)
        
        # store data for history
        for f in enriched:
            log_flight_seen(
                f["flight_number"],
                distance=f["distance_km"],
                position=f["position"],
                direction=f["direction"],
                altitude=f["altitude_ft"]
            )


        #sorting is a UI problem
        #enriched.sort(key=lambda f: f["distance_km"])
    
        self._attr_state = len(enriched)
        self._attr_extra_state_attributes = {
            "flights": [
                {
                    "flight": f["flight_number"],
                    "distance_km": f["distance_km"],
                    "direction": f["direction"],
                    "altitude": f["altitude_ft"]
                }
                for f in enriched
            ]
        }
