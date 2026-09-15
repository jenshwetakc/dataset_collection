from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

WEATHER_STATES = [

    "current",

    "hourly",

    "weekly",

    "location_search",

    "search_results",

    "saved_locations",

    "location_selected",

    "weather_alert",

    "details_open",

    "units_menu",

    "location_menu",
]


# ==========================================================
# Weather Conditions
# ==========================================================

CONDITIONS = [

    {
        "name": "Clear",
        "icon": "sunny",
    },

    {
        "name": "Partly Cloudy",
        "icon": "partly_cloudy_day",
    },

    {
        "name": "Cloudy",
        "icon": "cloud",
    },

    {
        "name": "Rain",
        "icon": "rainy",
    },

    {
        "name": "Thunderstorms",
        "icon": "thunderstorm",
    },

    {
        "name": "Snow",
        "icon": "weather_snowy",
    },

    {
        "name": "Fog",
        "icon": "foggy",
    },
]


# ==========================================================
# Cities
# ==========================================================

CITIES = [

    {
        "city": "Seoul",
        "country": "South Korea",
    },

    {
        "city": "Tokyo",
        "country": "Japan",
    },

    {
        "city": "London",
        "country": "United Kingdom",
    },

    {
        "city": "Paris",
        "country": "France",
    },

    {
        "city": "New York",
        "country": "United States",
    },

    {
        "city": "Berlin",
        "country": "Germany",
    },

    {
        "city": "Sydney",
        "country": "Australia",
    },

    {
        "city": "Toronto",
        "country": "Canada",
    },

    {
        "city": "Singapore",
        "country": "Singapore",
    },

    {
        "city": "Kathmandu",
        "country": "Nepal",
    },
]


# ==========================================================
# Alerts
# ==========================================================

ALERTS = [

    {
        "title": "Heavy Rain Warning",
        "message": "Heavy rainfall is expected this afternoon.",
        "icon": "rainy",
        "severity": "warning",
    },

    {
        "title": "Heat Advisory",
        "message": "High temperatures are expected during the afternoon.",
        "icon": "device_thermostat",
        "severity": "warning",
    },

    {
        "title": "Strong Wind Advisory",
        "message": "Strong winds are expected through the evening.",
        "icon": "air",
        "severity": "warning",
    },

    {
        "title": "Thunderstorm Warning",
        "message": "Thunderstorms may produce strong winds and heavy rain.",
        "icon": "thunderstorm",
        "severity": "danger",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_temperature(
    minimum: int = -5,
    maximum: int = 35,
) -> int:

    return random.randint(
        minimum,
        maximum,
    )


def generate_location() -> dict:

    return dict(
        random.choice(
            CITIES
        )
    )


def generate_condition() -> dict:

    return dict(
        random.choice(
            CONDITIONS
        )
    )


# ==========================================================
# Hourly Forecast
# ==========================================================

def generate_hourly_forecast() -> list[dict]:

    now = datetime.now()

    entries = []

    temperature = generate_temperature(
        8,
        30,
    )

    for index in range(
        12
    ):

        current_time = (
            now
            + timedelta(
                hours=index
            )
        )

        condition = (
            generate_condition()
        )

        temperature += random.choice(
            [
                -1,
                0,
                0,
                1,
            ]
        )

        entries.append(
            {
                "time":
                    (
                        "Now"
                        if index == 0
                        else current_time.strftime(
                            "%H:%M"
                        )
                    ),

                "temperature":
                    temperature,

                "condition":
                    condition[
                        "name"
                    ],

                "icon":
                    condition[
                        "icon"
                    ],

                "rain":
                    random.randint(
                        0,
                        80,
                    ),
            }
        )

    return entries


# ==========================================================
# Daily Forecast
# ==========================================================

def generate_daily_forecast() -> list[dict]:

    today = datetime.now()

    entries = []

    for index in range(
        7
    ):

        current_date = (
            today
            + timedelta(
                days=index
            )
        )

        condition = (
            generate_condition()
        )

        high = generate_temperature(
            12,
            34,
        )

        low = (
            high
            - random.randint(
                4,
                11,
            )
        )

        entries.append(
            {
                "day":
                    (
                        "Today"
                        if index == 0
                        else current_date.strftime(
                            "%A"
                        )
                    ),

                "date":
                    current_date.strftime(
                        "%b %d"
                    ),

                "condition":
                    condition[
                        "name"
                    ],

                "icon":
                    condition[
                        "icon"
                    ],

                "high":
                    high,

                "low":
                    low,

                "rain":
                    random.randint(
                        0,
                        85,
                    ),
            }
        )

    return entries


# ==========================================================
# Weather Details
# ==========================================================

def generate_details() -> list[dict]:

    return [

        {
            "label": "Feels Like",
            "icon": "device_thermostat",
            "value": f"{generate_temperature(10, 32)}°",
        },

        {
            "label": "Humidity",
            "icon": "humidity_percentage",
            "value": f"{random.randint(35, 90)}%",
        },

        {
            "label": "Wind",
            "icon": "air",
            "value": f"{random.randint(2, 38)} km/h",
        },

        {
            "label": "Visibility",
            "icon": "visibility",
            "value": f"{random.randint(4, 20)} km",
        },

        {
            "label": "Pressure",
            "icon": "speed",
            "value": f"{random.randint(995, 1035)} hPa",
        },

        {
            "label": "UV Index",
            "icon": "wb_sunny",
            "value": str(
                random.randint(
                    0,
                    11,
                )
            ),
        },

    ]


# ==========================================================
# Saved Locations
# ==========================================================

def generate_saved_locations() -> list[dict]:

    count = random.randint(
        3,
        6,
    )

    selected = random.sample(
        CITIES,
        k=min(
            count,
            len(
                CITIES
            ),
        ),
    )

    entries = []

    for index, location in enumerate(
        selected
    ):

        condition = (
            generate_condition()
        )

        entries.append(
            {
                "id":
                    index,

                "city":
                    location[
                        "city"
                    ],

                "country":
                    location[
                        "country"
                    ],

                "temperature":
                    generate_temperature(
                        3,
                        34,
                    ),

                "condition":
                    condition[
                        "name"
                    ],

                "icon":
                    condition[
                        "icon"
                    ],

                "selected":
                    index == 0,
            }
        )

    return entries


# ==========================================================
# Search Results
# ==========================================================

def generate_search_results() -> list[dict]:

    selected = random.sample(
        CITIES,
        k=random.randint(
            4,
            7,
        ),
    )

    return [

        {
            "city":
                location[
                    "city"
                ],

            "country":
                location[
                    "country"
                ],

            "icon":
                "location_on",
        }

        for location in selected
    ]


# ==========================================================
# Main
# ==========================================================

def generate_weather_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            WEATHER_STATES
        )


    if state not in WEATHER_STATES:

        raise ValueError(
            f"Unknown weather state: "
            f"{state}"
        )


    location = (
        generate_location()
    )

    condition = (
        generate_condition()
    )


    temperature = (
        generate_temperature(
            8,
            33,
        )
    )


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    if state in {
        "location_search",
        "search_results",
    }:

        search_query = random.choice(
            [
                "Seoul",
                "London",
                "Tokyo",
                "Berlin",
                "New",
            ]
        )


    # ======================================================
    # Units
    # ======================================================

    temperature_unit = random.choice(
        [
            "Celsius",
            "Fahrenheit",
        ]
    )


    wind_unit = random.choice(
        [
            "km/h",
            "mph",
            "m/s",
        ]
    )


    # ======================================================
    # Alert
    # ======================================================

    alert = None

    if state == "weather_alert":

        alert = dict(
            random.choice(
                ALERTS
            )
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "location":
            location,

        "condition":
            condition,

        "temperature":
            temperature,

        "high":
            temperature
            + random.randint(
                1,
                5,
            ),

        "low":
            temperature
            - random.randint(
                4,
                9,
            ),

        "hourly_entries":
            generate_hourly_forecast(),

        "daily_entries":
            generate_daily_forecast(),

        "details":
            generate_details(),

        "saved_locations":
            generate_saved_locations(),

        "search_query":
            search_query,

        "search_results":
            generate_search_results(),

        "alert":
            alert,

        "temperature_unit":
            temperature_unit,

        "wind_unit":
            wind_unit,

        "last_updated":
            datetime.now().strftime(
                "%H:%M"
            ),

        "sunrise":
            random.choice(
                [
                    "06:04",
                    "06:18",
                    "06:31",
                ]
            ),

        "sunset":
            random.choice(
                [
                    "18:42",
                    "18:55",
                    "19:10",
                ]
            ),
    }