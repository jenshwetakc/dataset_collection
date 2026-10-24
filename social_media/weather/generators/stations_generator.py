from __future__ import annotations

import copy
import random


STATION_STATES = (
    "overview",
    "coastal_filtered",
    "table_view",
    "station_expanded",
    "compare_stations",
    "search_results",
    "station_dialog",
    "display_settings",
)

STATION_LIBRARY = (
    ("Seoul Central", "Urban"),
    ("Seoul Riverside", "Urban"),
    ("Busan Harbor", "Coastal"),
    ("Busan Airport", "Coastal"),
    ("Incheon Coast", "Coastal"),
    ("Incheon Central", "Urban"),
    ("Jeju North", "Coastal"),
    ("Jeju South", "Coastal"),
    ("Daegu Central", "Urban"),
    ("Daejeon Park", "Urban"),
    ("Gwangju Central", "Urban"),
    ("Sokcho Coast", "Coastal"),
    ("Gangneung Beach", "Coastal"),
    ("Pyeongchang Ridge", "Mountain"),
    ("Taebaek Summit", "Mountain"),
    ("Jirisan Valley", "Mountain"),
    ("Chuncheon Lake", "Inland"),
    ("Andong Riverside", "Inland"),
)

CONDITIONS = (
    ("Sunny", "sunny"),
    ("Cloudy", "cloud"),
    ("Light rain", "rainy"),
    ("Partly cloudy", "partly_cloudy_day"),
    ("Windy", "air"),
)


def generate_stations_data(
    *,
    sample_index: int,
) -> dict:
    stations = []

    for index, (name, region) in enumerate(STATION_LIBRARY):
        condition, icon = random.choice(CONDITIONS)
        temperature = random.randint(12, 27)
        wind = random.randint(4, 35)

        stations.append({
            "id": f"station_{index:02d}",
            "name": name,
            "region": region,
            "condition": condition,
            "icon": icon,
            "temperature": temperature,
            "feels_like": temperature - random.randint(0, 3),
            "humidity": random.randint(35, 90),
            "wind": wind,
            "gust": wind + random.randint(3, 12),
            "direction": random.choice(
                ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            ),
            "pressure": random.randint(1004, 1024),
            "visibility": random.randint(5, 20),
            "rainfall": (
                round(random.uniform(0.4, 6.0), 1)
                if icon == "rainy"
                else 0.0
            ),
            "updated": f"{random.randint(1, 8)} min ago",
            "favorite": index in {0, 2, 6, 13},
            "selected": index in {0, 2, 13},
            "expanded": False,
            "history": [
                {
                    "time": f"{hour:02d}:00",
                    "temperature": temperature + random.randint(-2, 2),
                    "humidity": random.randint(40, 85),
                }
                for hour in range(11, 17)
            ],
        })

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "dialog_type": None,
        "view": "cards",
        "query": "",
        "region": "All",
        "regions": ["All", "Urban", "Coastal", "Mountain", "Inland"],
        "stations": stations,
        "settings": {
            "humidity": True,
            "pressure": True,
            "rainfall": True,
            "favorites_first": False,
        },
    }


def apply_stations_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in STATION_STATES:
        raise ValueError(f"Unknown station state: {state}")

    data = copy.deepcopy(base_data)
    data["state"] = state

    if state == "coastal_filtered":
        data["region"] = "Coastal"

    elif state == "table_view":
        data["view"] = "table"

    elif state == "station_expanded":
        data["stations"][0]["expanded"] = True

    elif state == "compare_stations":
        data["view"] = "compare"

    elif state == "search_results":
        data["query"] = "Seoul"

    elif state == "station_dialog":
        data["popup_visible"] = True
        data["dialog_type"] = "station"

    elif state == "display_settings":
        data["popup_visible"] = True
        data["dialog_type"] = "settings"

    visible = [
        station
        for station in data["stations"]
        if (
            data["region"] == "All"
            or station["region"] == data["region"]
        )
        and (
            not data["query"]
            or data["query"].casefold()
            in station["name"].casefold()
        )
    ]

    if data["settings"]["favorites_first"]:
        visible.sort(
            key=lambda station: not station["favorite"]
        )

    data["visible_stations"] = visible
    data["comparison"] = [
        station
        for station in data["stations"]
        if station["selected"]
    ]
    data["detail_station"] = data["stations"][0]
    data["favorites"] = [
        station
        for station in data["stations"]
        if station["favorite"]
    ]

    data["summary"] = {
        "count": len(visible),
        "average": round(
            sum(station["temperature"] for station in visible)
            / len(visible),
            1,
        ) if visible else 0,
        "maximum_wind": max(
            (station["wind"] for station in visible),
            default=0,
        ),
        "rain_count": sum(
            station["rainfall"] > 0
            for station in visible
        ),
    }

    return data