from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class AirspaceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Basic validation
            url = user_input.get("url")
            lat = user_input.get("latitude")
            lon = user_input.get("longitude")
            if not url or lat is None or lon is None:
                errors["base"] = "invalid_input"
            else:
                return self.async_create_entry(title="Airspace Tracker", data=user_input)

        schema = vol.Schema({
            vol.Required("url", default="http://localhost/tar1090/data/aircraft.json"): str,
            vol.Required("latitude", default=0.0): vol.Coerce(float),
            vol.Required("longitude", default=0.0): vol.Coerce(float),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)