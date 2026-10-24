from __future__ import annotations

import random

from copy import deepcopy
from datetime import datetime, timedelta


TEN_DAY_STATES = [
    "overview",
    "rainy_week",
    "snowy_week",
    "day_expanded",
    "night_expanded",
    "units_dialog",
    "forecast_settings",
]

LOCATIONS = [
    "Seoul, South Korea",
    "Busan, South Korea",
    "Tokyo, Japan",
    "London, United Kingdom",
    "Toronto, Canada",
    "New York, United States",
]

CONDITIONS = [
    ("Sunny", "sunny"),
    ("Partly cloudy", "partly_cloudy_day"),
    ("Cloudy", "cloud"),
    ("Showers", "rainy"),
]


def temperature_text(value_c: float, unit: str) -> str:
    value = (
        value_c
        if unit == "C"
        else value_c * 9 / 5 + 32
    )
    return f"{round(value)}°"


def wind_text(value_kmh: float, unit: str) -> str:
    if unit == "mph":
        return f"{round(value_kmh / 1.609344)} mph"

    return f"{round(value_kmh)} km/h"


def generate_ten_day_data(
    *,
    sample_index: int,
) -> dict:
    return {
        "sample_index": sample_index,
        "location": random.choice(LOCATIONS),
        "start_date": "2026-10-06",
        "temperature_unit": random.choice(["C", "F"]),
        "base_temperature_c": random.randint(15, 25),
        "show_humidity": random.choice([True, False]),
        "show_uv": True,
        "show_sun_times": True,
        "updated_text": (
            f"Updated {random.randint(1, 10)} minutes ago"
        ),
    }


def apply_ten_day_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in TEN_DAY_STATES:
        raise ValueError(
            f"Unknown ten-day state: {state!r}"
        )

    data = deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": state in {
            "units_dialog",
            "forecast_settings",
        },
        "popup_type": (
            state
            if state in {
                "units_dialog",
                "forecast_settings",
            }
            else None
        ),
        "expanded_day_id": (
            0
            if state in {
                "day_expanded",
                "night_expanded",
            }
            else None
        ),
        "expanded_period": (
            "night"
            if state == "night_expanded"
            else "day"
        ),
    })

    unit = data["temperature_unit"]
    wind_unit = "km/h" if unit == "C" else "mph"
    data["wind_unit"] = wind_unit

    start = datetime.fromisoformat(data["start_date"])
    days = []

    for index in range(10):
        date = start + timedelta(days=index)

        if state == "snowy_week":
            condition, icon = "Snow showers", "weather_snowy"
            high_c = random.randint(-3, 2)
            precipitation = random.randint(55, 95)
            humidity = random.randint(70, 95)

        elif state == "rainy_week":
            condition, icon = "Rain", "rainy"
            high_c = (
                data["base_temperature_c"]
                + random.randint(-5, 0)
            )
            precipitation = random.randint(65, 100)
            humidity = random.randint(75, 98)

        else:
            condition, icon = random.choice(CONDITIONS)
            high_c = (
                data["base_temperature_c"]
                + random.randint(-3, 4)
            )
            precipitation = (
                random.randint(45, 80)
                if icon == "rainy"
                else random.randint(0, 25)
            )
            humidity = random.randint(40, 80)

        low_c = high_c - random.randint(5, 10)
        wind_kmh = random.randint(5, 28)
        direction = random.choice([
            "N", "NE", "E", "SE",
            "S", "SW", "W", "NW",
        ])

        night_condition = (
            condition
            if icon in {"rainy", "weather_snowy"}
            else "Partly cloudy"
            if icon == "partly_cloudy_day"
            else "Cloudy"
            if icon == "cloud"
            else "Clear"
        )

        night_icon = (
            icon
            if icon in {"rainy", "weather_snowy", "cloud"}
            else "partly_cloudy_night"
            if icon == "partly_cloudy_day"
            else "clear_night"
        )

        days.append({
            "id": index,
            "label": (
                "Today"
                if index == 0
                else date.strftime("%a")
            ),
            "date": date.strftime("%b %d"),
            "full_date": date.strftime("%A, %B %d"),
            "high": temperature_text(high_c, unit),
            "low": temperature_text(low_c, unit),
            "condition": condition,
            "icon": icon,
            "precipitation": precipitation,
            "wind": wind_text(wind_kmh, wind_unit),
            "direction": direction,
            "expanded": index == data["expanded_day_id"],
            "day": {
                "condition": condition,
                "icon": icon,
                "temperature": temperature_text(high_c, unit),
                "summary": (
                    f"{condition} during the day. "
                    f"Winds from the {direction}."
                ),
                "precipitation": precipitation,
                "wind": wind_text(wind_kmh, wind_unit),
                "humidity": humidity,
                "uv": random.randint(1, 7),
                "sun_label": "Sunrise",
                "sun_time": "06:24",
            },
            "night": {
                "condition": night_condition,
                "icon": night_icon,
                "temperature": temperature_text(low_c, unit),
                "summary": (
                    f"{night_condition} overnight with "
                    "cooler temperatures."
                ),
                "precipitation": max(
                    0,
                    min(
                        100,
                        precipitation + random.randint(-10, 10),
                    ),
                ),
                "wind": wind_text(
                    max(0, wind_kmh - 4),
                    wind_unit,
                ),
                "humidity": min(100, humidity + 5),
                "uv": 0,
                "sun_label": "Sunset",
                "sun_time": "18:12",
            },
        })

    data["days"] = days

    data["summary"] = {
        "rainy_week": "An unsettled stretch with frequent rain.",
        "snowy_week": "Cold conditions with recurring snow showers.",
    }.get(
        state,
        "A look ahead at the next ten days.",
    )

    data["wet_days"] = sum(
        day["precipitation"] >= 50
        for day in days
    )

    return data