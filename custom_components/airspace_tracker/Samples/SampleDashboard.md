views:
  - title: Home
    sections:
      - type: grid
        cards:
          - type: entity
            entity: sensor.airspace_currently_tracking
            grid_options:
              columns: 12
              rows: 4
          - type: entity
            entity: sensor.airspace_history_today
            grid_options:
              columns: 12
              rows: 4
          - type: markdown
            title: 🛬 Furthest Flight Today
            content: >-
              |{% set f = state_attr('sensor.airspace_history_today',
              'furthest_flight') %} {{ f.flight }} || 🕒 {{ f.timestamp }}|

              |--|--|:-- |

              |📏 {{ f.distance_km }} km ||📍 Lat: {{ f.position.lat }}, Lon: {{
              f.position.lon }}  |

              |✈️ Altitude: {{ f.altitude_ft }} ft 
              |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|🧭
              Direction: {{ f.direction }}  |



              **🗺️ Location:** {{ f.location }}
            grid_options:
              columns: 12
              rows: 4
          - type: markdown
            title: ✈️ Current Tracked Flights
            content: >
              {% set sorted = state_attr('sensor.airspace_currently_tracking',
              'flights') | sort(attribute='distance_km') %}

              |Flight || Altitude || Distance  ||Direction|

              |--|--|--:|--|     ----:   |---|    :----   |

              {% for flight in sorted %}| {{ flight.flight }}
              |&nbsp;&nbsp;&nbsp;&nbsp;| {{ flight.altitude }} ft
              |&nbsp;&nbsp;&nbsp;&nbsp;| {{ flight.distance_km }} km
              |&nbsp;&nbsp;&nbsp;&nbsp;| {{ flight.direction }} |

              {% endfor %}
            grid_options:
              rows: auto
              columns: 12
          - type: markdown
            title: ✈️ Flights Seen Today
            content: >2-
                {% set last_seen = state_attr('sensor.airspace_history_today', 'last_seen') %}
                {% set sorted_pairs = last_seen.items() | sort(attribute='1', reverse=true) %}
                {% set flights = sorted_pairs | map(attribute=0) | list %}
                {% set times = sorted_pairs | map(attribute=1) | list %}
               {% set chunk_size = (flights | length // 4) + 1 %}
              | Flight Number | Last Seen || Flight Number | Last Seen || Flight
              Number | Last Seen || Flight Number | Last Seen |

              |--------|------:|----|--------|------:|---|--------|------:|---|-------|-----:| 
              {% for i in range(chunk_size) %}  {% set idx1 = i %}  {% set idx2
              = i + chunk_size %}  {% set idx3 = i + chunk_size * 2 %} {% set
              idx4 = i + chunk_size * 3 %}  {% if idx1 < flights | length %}   
              {% set f1 = flights[idx1] %}  {% else %}    {% set f1 = '' %}  {%
              endif %}  {% if idx2 < flights | length %}{% set f2 =
              flights[idx2] %}  {% else %}    {% set f2 = '' %}  {% endif %}  {%
              if idx3 < flights | length %}    {% set f3 = flights[idx3] %}  {%
              else %}    {% set f3 = '' %}   {% endif %}{% if idx4 < flights |
              length %}    {% set f4 = flights[idx4] %}  {% else %}    {% set f4
              = '' %}   {% endif %}

              | {{ f1 }} | {{ last_seen[f1].split(' ')[1] if f1 }}
              |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
              {{ f2 }} | {{ last_seen[f2].split(' ')[1] if f2 }}
              |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
              {{ f3 }} | {{ last_seen[f3].split(' ')[1] if f3 }} |
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              | {{ f4 }} | {{ last_seen[f4].split(' ')[1] if f4 }} | {% endfor
              %}
            grid_options:
              columns: 24
              rows: auto
        column_span: 3
