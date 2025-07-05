from .airspace_current import AirspaceCurrentSensor
from .airspace_history import AirspaceHistorySensor


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data["airspace_tracker"][entry.entry_id]
    async_add_entities([
        AirspaceCurrentSensor(data),
        AirspaceHistorySensor(data)
    ])
