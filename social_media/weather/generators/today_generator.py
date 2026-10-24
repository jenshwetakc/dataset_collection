from __future__ import annotations

import random

from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


TODAY_STATES = [
    "sunny",
    "rainy",
    "snowy",
    "night",
    "severe_alert",
    "location_search",
    "units_settings",
]

LOCATIONS = [
    "Seoul, South Korea",
    "Busan, South Korea",
    "London, United Kingdom",
    "New York, United States",
    "Tokyo, Japan",
    "Sydney, Australia",
    "Toronto, Canada",
    "Singapore",
]

CONDITIONS = {
    "sunny": {
        "label": "Sunny",
        "icon": "sunny",
        "temperature_range": (20, 34),
        "precipitation_range": (0, 10),
        "humidity_range": (30, 60),
        "wind_range": (3, 18),
        "summary": "Mostly clear skies throughout the day.",
    },
    "rainy": {
        "label": "Rain",
        "icon": "rainy",
        "temperature_range": (10, 22),
        "precipitation_range": (65, 100),
        "humidity_range": (75, 98),
        "wind_range": (8, 30),
        "summary": "Rain continues through the next few hours.",
    },
    "snowy": {
        "label": "Snow",
        "icon": "weather_snowy",
        "temperature_range": (-9, 1),
        "precipitation_range": (60, 95),
        "humidity_range": (65, 92),
        "wind_range": (5, 25),
        "summary": "Periods of snow with cold conditions.",
    },
    "night": {
        "label": "Clear",
        "icon": "clear_night",
        "temperature_range": (8, 20),
        "precipitation_range": (0, 15),
        "humidity_range": (45, 75),
        "wind_range": (2, 14),
        "summary": "Clear skies tonight with light winds.",
    },
    "severe_alert": {
        "label": "Thunderstorms",
        "icon": "thunderstorm",
        "temperature_range": (18, 29),
        "precipitation_range": (80, 100),
        "humidity_range": (70, 98),
        "wind_range": (30, 65),
        "summary": "Thunderstorms may bring heavy rain and gusty winds.",
    },
}

NEWS_TITLES = [
    "What to expect from this week's changing weather",
    "How clouds reveal changes in the forecast",
    "A closer look at seasonal weather patterns",
    "Understanding the hourly rain forecast",
    "Why temperatures feel different in the wind",
    "Your guide to the UV index",
]


def temperature_text(
    value_c: float,
    unit: str,
) -> str:
    value = (
        value_c
        if unit == "C"
        else value_c * 9 / 5 + 32
    )

    return f"{round(value)}°"


def speed_text(
    value_kmh: float,
    unit: str,
) -> str:
    if unit == "mph":
        return f"{round(value_kmh / 1.609344)} mph"

    return f"{round(value_kmh)} km/h"


def optional_image(
    directory: Path | None,
) -> str | None:
    if directory is None:
        return None

    directory = Path(directory)

    # Avoid repeated empty-directory warnings per news item.
    if not directory.is_dir():
        return None

    if not get_image_files(str(directory)):
        return None

    return get_random_image(directory)


def generate_today_data(
    *,
    sample_index: int,
    images_dir: Path | None = None,
) -> dict:
    unit = random.choice(["C", "F"])
    wind_unit = "km/h" if unit == "C" else "mph"

    return {
        "sample_index": sample_index,
        "state": "sunny",
        "popup_visible": False,
        "popup_type": None,
        "location": random.choice(LOCATIONS),
        "temperature_unit": unit,
        "wind_unit": wind_unit,
        "updated_text": (
            f"Updated {random.randint(1, 12)} minutes ago"
        ),
        "favorite": random.choice([True, False]),
        "notifications_enabled": random.choice([True, False]),
        "search_query": "Se",
        "search_results": [
            {
                "name": "Seoul",
                "region": "South Korea",
            },
            {
                "name": "Seattle",
                "region": "Washington, United States",
            },
            {
                "name": "Seville",
                "region": "Andalusia, Spain",
            },
        ],
        "saved_locations": random.sample(
            LOCATIONS,
            k=3,
        ),
        "news": [
            {
                "id": index,
                "title": title,
                "category": random.choice([
                    "Weather explained",
                    "Latest stories",
                    "Seasonal outlook",
                ]),
                "image": optional_image(images_dir),
            }
            for index, title in enumerate(
                random.sample(NEWS_TITLES, k=3)
            )
        ],
    }


def apply_today_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in TODAY_STATES:
        raise ValueError(
            f"Unknown today state: {state!r}"
        )

    data = deepcopy(base_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "location_search",
        "units_settings",
    }
    data["popup_type"] = (
        state
        if data["popup_visible"]
        else None
    )

    condition_key = (
        state
        if state in CONDITIONS
        else "sunny"
    )

    condition = CONDITIONS[condition_key]

    temperature_c = random.randint(
        *condition["temperature_range"]
    )
    feels_c = temperature_c + random.randint(-3, 3)
    high_c = max(
        temperature_c,
        temperature_c + random.randint(1, 5),
    )
    low_c = temperature_c - random.randint(3, 8)

    wind_kmh = random.randint(
        *condition["wind_range"]
    )
    precipitation = random.randint(
        *condition["precipitation_range"]
    )
    humidity = random.randint(
        *condition["humidity_range"]
    )

    unit = data["temperature_unit"]
    wind_unit = data["wind_unit"]

    data.update({
        "condition": condition["label"],
        "condition_icon": condition["icon"],
        "summary": condition["summary"],
        "temperature": temperature_text(
            temperature_c,
            unit,
        ),
        "feels_like": temperature_text(
            feels_c,
            unit,
        ),
        "high": temperature_text(high_c, unit),
        "low": temperature_text(low_c, unit),
        "precipitation": precipitation,
        "humidity": humidity,
        "wind": speed_text(wind_kmh, wind_unit),
        "wind_direction": random.choice([
            "N", "NE", "E", "SE",
            "S", "SW", "W", "NW",
        ]),
        "uv_index": (
            0
            if condition_key == "night"
            else random.randint(1, 9)
        ),
        "visibility": (
            "2 km"
            if condition_key == "snowy"
            else "5 km"
            if condition_key in {"rainy", "severe_alert"}
            else "16 km"
        ),
        "pressure": f"{random.randint(995, 1028)} hPa",
        "sunrise": "06:24",
        "sunset": "18:12",
        "alert": (
            {
                "title": "Severe Thunderstorm Warning",
                "description": (
                    "Heavy rain and strong wind gusts are "
                    "possible in the surrounding area."
                ),
                "expires": "Until 20:00 local time",
            }
            if condition_key == "severe_alert"
            else None
        ),
    })

    # Use a stable synthetic time rather than the current hour,
    # so the night state also has nighttime hourly labels.
    start_hour = (
        21
        if condition_key == "night"
        else 9
    )
    start = datetime(2026, 10, 6, start_hour)

    hourly = []

    for index in range(8):
        hour = start + timedelta(hours=index)
        hour_temperature = temperature_c + random.randint(-2, 2)
        rain_chance = max(
            0,
            min(
                100,
                precipitation + random.randint(-10, 10),
            ),
        )

        hourly.append({
            "id": index,
            "time": (
                "Now"
                if index == 0
                else hour.strftime("%H:%M")
            ),
            "temperature": temperature_text(
                hour_temperature,
                unit,
            ),
            "icon": condition["icon"],
            "condition": condition["label"],
            "precipitation": rain_chance,
        })

    data["hourly"] = hourly

    data["daily"] = [
        {
            "id": index,
            "day": (
                "Today"
                if index == 0
                else (start + timedelta(days=index)).strftime("%a")
            ),
            "icon": condition["icon"],
            "condition": condition["label"],
            "high": temperature_text(
                high_c + random.randint(-2, 2),
                unit,
            ),
            "low": temperature_text(
                low_c + random.randint(-2, 2),
                unit,
            ),
            "precipitation": max(
                0,
                min(
                    100,
                    precipitation + random.randint(-15, 15),
                ),
            ),
        }
        for index in range(5)
    ]

    return data