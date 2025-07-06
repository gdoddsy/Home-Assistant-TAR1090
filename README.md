# ✈️ Home Assistant TAR1090 Integration

![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom%20Repository-blue.svg)
![Integration Type](https://img.shields.io/badge/Home%20Assistant-Integration-orange)
![Async Safe](https://img.shields.io/badge/Async-Safe-brightgreen)
![License](https://img.shields.io/github/license/gdoddsy/Home-Assistant-TAR1090)
![Last Updated](https://img.shields.io/github/last-commit/gdoddsy/Home-Assistant-TAR1090)
![Stars](https://img.shields.io/github/stars/gdoddsy/Home-Assistant-TAR1090?style=social)

A modular, telemetry-enhanced aircraft tracker for Home Assistant — log every flight seen from your receiver, capture the furthest visitor with suburb-level insight, and visualize it all through polished dashboard cards.

---
## 🛠 What It Does

- Logs all aircraft seen today into a per-day JSON file
- Tracks the furthest flight and reverse geocodes its location
- Offers dashboard-friendly sensors and Markdown card templates for display
- Stores history neatly under: `/config/custom_components/airspace_tracker/data/`

---
## 🧠 Notes

- Requires a TAR1090 receiver producing live aircraft data in JSON format
- Reverse geocoding powered by OpenStreetMap via Geopy
- Uses async-safe file I/O: reading and writing handled with `asyncio.to_thread()` to avoid blocking Home Assistant’s event loop
- Stores per-day logs in `/config/custom_components/airspace_tracker/data/` using filenames like `flight_log_YYYY-MM-DD.json`
- Furthest flight is updated in real time when a more distant aircraft is seen
- Sensor attributes include:
  - `unique_flights`: List of ICAO callsigns seen today
  - `last_seen`: Dictionary of timestamps per flight
  - `furthest_flight`: Full metadata (position, altitude, direction, timestamp, location)
- Fully compatible with Markdown cards for real-time dashboard display

---

## 📦 Installation via HACS

This integration is designed for easy setup through [HACS](https://hacs.xyz/) (Home Assistant Community Store).

### 1. Add Custom Repository

In Home Assistant:

- Go to **HACS → Integrations → Explore & Add Repositories**
- Click the **menu (⋮)** in the upper right → **Custom repositories**
- Add: https://github.com/gdoddsy/Home-Assitant-TAR1090
- Select **Integration** as category.

### 2. Install Integration

- After adding the repo, search for **Airspace Tracker**
- Click **Download** to install

### 3. Restart Home Assistant

- Restart to register the new component

### 4. Add the Integration

- Navigate to **Settings → Devices & Services**
- Click **Add Integration**, search for **Airspace Tracker**, and follow the prompts

---
## 📂 Data Format

Each day creates a file in: `/config/custom_components/airspace_tracker/data`
With the format: `flight_log_YYYY-MM-DD.json`

Example content:

```json
{
  "flights": {
    "QFA739": "2025-07-06 15:17:08",
    "VOZ705": "2025-07-06 14:34:45",
    "QLK41D": "2025-07-06 14:34:45"
  },
  "furthest": {
    "flight": "QFA739",
    "position": { "lat": -33.895569, "lon": 148.348331 },
    "distance_km": 219.8,
    "direction": "W",
    "altitude_ft": 36000,
    "timestamp": "2025-07-06 15:17:08",
    "location": "Cootamundra, NSW"
  }
}
```
---
## 📊 Dashboard Examples

To help visualize aircraft tracking data, this integration includes sample Markdown card templates for:

- ✅ Flights Seen Today (with chunked table layout)
- ✅ Furthest Flight Today (with location, direction, and timestamp)

View the full example dashboards here:

➡️ [Sample Dashboard Cards](https://github.com/gdoddsy/Home-Assistant-TAR1090/blob/main/example_dashboard_cards.md)

You can copy these directly into your Home Assistant dashboard using the Markdown card type. Adjust `sensor.airspace_history_today` to match your sensor entity if you’ve renamed it.

---
## 📮 Future Ideas

- 🗓️ Log browser for browsing flight history by date
- 🧭 Directional breakdown by quadrant (e.g. N, NE, E...)
- 🗺️ Heatmaps for daily aircraft density
- 🏘️ Suburb-based analysis with aggregated counts
- 🧰 Option to cache geocoding results for performance
- 📦 Archive older logs into weekly summaries or compressed `.gz` files
- 🔧 Service calls to manually purge, refresh, or export logs

Have an idea or feature request? Feel free to open an issue or pull request on [GitHub](https://github.com/gdoddsy/Home-Assistant-TAR1090)!

---

## 🛠️ Credits

Created by [@gdoddsy](https://github.com/gdoddsy), with a passion for aircraft tracking, spatial analytics, and beautiful Home Assistant dashboards.

Reverse geocoding powered by [Geopy](https://github.com/geopy/geopy) and OpenStreetMap Nominatim.

Markdown cards inspired by the flexibility of [Home Assistant Lovelace](https://www.home-assistant.io/lovelace/), and designed for live telemetry readability ✈️📊.
