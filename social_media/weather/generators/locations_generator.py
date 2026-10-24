from __future__ import annotations

import copy
import random


LOCATION_STATES = (
    "overview",
    "search_results",
    "empty_locations",
    "manage_locations",
    "add_location_dialog",
    "remove_location_dialog",
)


CITY_LIBRARY = (
    {
        "id": "seoul",
        "name": "Seoul",
        "country": "South Korea",
        "local_time": "4:20 PM",
        "condition": "Partly cloudy",
        "icon": "partly_cloudy_day",
        "temperature": 22,
        "high": 25,
        "low": 16,
    },
    {
        "id": "busan",
        "name": "Busan",
        "country": "South Korea",
        "local_time": "4:20 PM",
        "condition": "Sunny",
        "icon": "sunny",
        "temperature": 24,
        "high": 26,
        "low": 18,
    },
    {
        "id": "tokyo",
        "name": "Tokyo",
        "country": "Japan",
        "local_time": "4:20 PM",
        "condition": "Light rain",
        "icon": "rainy",
        "temperature": 20,
        "high": 23,
        "low": 17,
    },
    {
        "id": "london",
        "name": "London",
        "country": "United Kingdom",
        "local_time": "8:20 AM",
        "condition": "Cloudy",
        "icon": "cloud",
        "temperature": 14,
        "high": 17,
        "low": 10,
    },
    {
        "id": "new_york",
        "name": "New York",
        "country": "United States",
        "local_time": "3:20 AM",
        "condition": "Clear night",
        "icon": "clear_night",
        "temperature": 16,
        "high": 21,
        "low": 13,
    },
    {
        "id": "sydney",
        "name": "Sydney",
        "country": "Australia",
        "local_time": "6:20 PM",
        "condition": "Windy",
        "icon": "air",
        "temperature": 19,
        "high": 22,
        "low": 15,
    },
)


def generate_locations_data(
    *,
    sample_index: int,
) -> dict:
    cities = copy.deepcopy(list(CITY_LIBRARY))
    random.shuffle(cities)

    saved = cities[:4]
    available = cities[4:]

    for index, city in enumerate(saved):
        offset = random.randint(-2, 2)

        city["temperature"] += offset
        city["high"] += offset
        city["low"] += offset

        city["pinned"] = index == 0
        city["precipitation"] = (
            random.randint(55, 90)
            if city["icon"] == "rainy"
            else random.randint(0, 25)
        )

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "dialog_type": None,
        "unit": "C",
        "query": "",
        "locations": saved,
        "available_locations": available,
        "search_results": [],
        "selected_location": None,
        "remove_target": None,
        "manage_mode": False,
        "updated_text": (
            f"Updated {random.randint(1, 9)} minutes ago"
        ),
    }


def apply_locations_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in LOCATION_STATES:
        raise ValueError(
            f"Unknown locations state: {state}"
        )

    data = copy.deepcopy(base_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "add_location_dialog",
        "remove_location_dialog",
    }

    if state == "search_results":
        target = data["locations"][0]
        data["query"] = target["name"][:3]
        data["search_results"] = [
            city
            for city in data["locations"]
            if data["query"].casefold()
            in city["name"].casefold()
        ]

    elif state == "empty_locations":
        data["available_locations"] = (
            data["locations"]
            + data["available_locations"]
        )
        data["locations"] = []

    elif state == "manage_locations":
        data["manage_mode"] = True

    elif state == "add_location_dialog":
        data["dialog_type"] = "add"
        target = data["available_locations"][0]
        data["query"] = target["name"][:2]
        data["search_results"] = [
            city
            for city in data["available_locations"]
            if data["query"].casefold()
            in city["name"].casefold()
        ]
        data["selected_location"] = target["id"]

    elif state == "remove_location_dialog":
        data["dialog_type"] = "remove"
        data["remove_target"] = data["locations"][-1]

    data["visible_locations"] = (
        data["search_results"]
        if state == "search_results"
        else data["locations"]
    )

    data["saved_count"] = len(data["locations"])

    return data