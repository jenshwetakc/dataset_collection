from __future__ import annotations

import random

from copy import deepcopy
from datetime import datetime, timedelta


HOURLY_STATES = [
    "overview",
    "rainy",
    "snowy",
    "windy",
    "hour_expanded",
    "day_picker",
    "display_settings",
]

LOCATIONS = [
    "Seoul, South Korea",
    "Busan, South Korea",
    "Tokyo, Japan",
    "London, United Kingdom",
    "Toronto, Canada",
    "New York, United States",
]

CONDITIONS = {
    "clear": ("Sunny", "sunny"),
    "cloudy": ("Mostly cloudy", "cloud"),
    "rain": ("Rain", "rainy"),
    "snow": ("Snow", "weather_snowy"),
    "wind": ("Windy", "air"),
    "night": ("Clear", "clear_night"),
}


def temperature_text(value_c: float, unit: str) -> str:
    value = (
        value_c
        if unit == "C"
        else value_c * 9 / 5 + 32
    )
    return f"{round(value)}°"


def speed_text(value_kmh: float, unit: str) -> str:
    if unit == "mph":
        return f"{round(value_kmh / 1.609344)} mph"

    return f"{round(value_kmh)} km/h"


def generate_hourly_data(
    *,
    sample_index: int,
) -> dict:
    # Synthetic dates, independent of the machine clock.
    start = datetime(2026, 10, 6, 9)
    unit = random.choice(["C", "F"])

    days = [
        {
            "id": index,
            "label": (
                "Today"
                if index == 0
                else "Tomorrow"
                if index == 1
                else (start + timedelta(days=index)).strftime("%A")
            ),
            "date": (
                start + timedelta(days=index)
            ).strftime("%b %d"),
            "iso_date": (
                start + timedelta(days=index)
            ).strftime("%Y-%m-%d"),
        }
        for index in range(5)
    ]

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "popup_type": None,
        "location": random.choice(LOCATIONS),
        "temperature_unit": unit,
        "wind_unit": "km/h" if unit == "C" else "mph",
        "start_iso": start.isoformat(),
        "base_temperature_c": random.randint(15, 25),
        "days": days,
        "selected_day": 0,
        "selected_day_label": "Today",
        "selected_day_date": days[0]["date"],
        "expanded_hour_id": None,
        "show_feels_like": random.choice([True, False]),
        "show_humidity": random.choice([True, False]),
        "show_wind": True,
        "updated_text": (
            f"Updated {random.randint(1, 10)} minutes ago"
        ),
    }


def apply_hourly_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in HOURLY_STATES:
        raise ValueError(
            f"Unknown hourly state: {state!r}"
        )

    data = deepcopy(base_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "day_picker",
        "display_settings",
    }
    data["popup_type"] = (
        state if data["popup_visible"] else None
    )
    data["expanded_hour_id"] = (
        2 if state == "hour_expanded" else None
    )

    start = datetime.fromisoformat(data["start_iso"])
    base_temperature = data["base_temperature_c"]

    if state == "snowy":
        base_temperature = random.randint(-6, 0)

    rows = []

    for index in range(24):
        value = start + timedelta(hours=index)
        is_night = value.hour >= 19 or value.hour < 6

        if state == "rainy":
            key = "rain"
            precipitation = random.randint(65, 100)
            wind_kmh = random.randint(10, 30)
            humidity = random.randint(78, 98)
            amount_mm = round(random.uniform(0.3, 4.5), 1)

        elif state == "snowy":
            key = "snow"
            precipitation = random.randint(60, 95)
            wind_kmh = random.randint(8, 25)
            humidity = random.randint(70, 95)
            amount_mm = round(random.uniform(0.2, 2.5), 1)

        elif state == "windy":
            key = "wind"
            precipitation = random.randint(0, 25)
            wind_kmh = random.randint(35, 65)
            humidity = random.randint(35, 65)
            amount_mm = 0.0

        else:
            key = (
                "night"
                if is_night
                else "cloudy"
                if index % 4 == 2
                else "clear"
            )
            precipitation = random.randint(0, 20)
            wind_kmh = random.randint(4, 18)
            humidity = random.randint(40, 75)
            amount_mm = 0.0

        label, icon = CONDITIONS[key]

        temperature_c = (
            base_temperature
            + random.randint(-2, 2)
            - (4 if is_night else 0)
        )

        feels_c = temperature_c - (
            random.randint(3, 6)
            if state in {"snowy", "windy"}
            else random.randint(0, 2)
        )

        rows.append({
            "id": index,
            "time": value.strftime("%H:%M"),
            "date": value.strftime("%a, %b %d"),
            "new_day": index == 0 or value.hour == 0,
            "condition": label,
            "icon": icon,
            "temperature": temperature_text(
                temperature_c,
                data["temperature_unit"],
            ),
            "feels_like": temperature_text(
                feels_c,
                data["temperature_unit"],
            ),
            "precipitation": precipitation,
            "precipitation_amount": f"{amount_mm:.1f} mm",
            "humidity": humidity,
            "wind": speed_text(
                wind_kmh,
                data["wind_unit"],
            ),
            "gusts": speed_text(
                wind_kmh + random.randint(5, 18),
                data["wind_unit"],
            ),
            "direction": random.choice([
                "N", "NE", "E", "SE",
                "S", "SW", "W", "NW",
            ]),
            "uv_index": (
                0 if is_night else random.randint(1, 7)
            ),
            "cloud_cover": (
                random.randint(80, 100)
                if key in {"rain", "snow", "cloudy"}
                else random.randint(0, 35)
            ),
            "expanded": index == data["expanded_hour_id"],
        })

    data["hours"] = rows

    data["summary"] = {
        "overview": "Mostly dry conditions over the next 24 hours.",
        "rainy": "Rain is expected throughout much of the day.",
        "snowy": "Snow showers with temperatures near or below freezing.",
        "windy": "Strong winds with higher gusts during the afternoon.",
        "hour_expanded": "View detailed conditions for a selected hour.",
        "day_picker": "Mostly dry conditions over the next 24 hours.",
        "display_settings": "Mostly dry conditions over the next 24 hours.",
    }[state]

    data["notice"] = (
        "Strong winds expected. Gusts may reach "
        + max(
            rows,
            key=lambda row: int(
                row["gusts"].split()[0]
            ),
        )["gusts"]
        + "."
        if state == "windy"
        else None
    )

    data["high_precipitation_hours"] = sum(
        row["precipitation"] >= 50
        for row in rows
    )

    return data