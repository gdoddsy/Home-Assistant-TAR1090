from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .sensor import AirspaceCountSensor
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    url = entry.data["url"]
    lat = entry.data["latitude"]
    lon = entry.data["longitude"]

    async_add_entities([AirspaceCountSensor(url, lat, lon)])
    return True