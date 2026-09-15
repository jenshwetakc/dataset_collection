from __future__ import annotations

import random
from datetime import datetime, timedelta

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


# ==========================================================
# States
# ==========================================================

WEATHER_STATES = [

    "current_weather",

    "hourly_forecast",

    "ten_day_forecast",

    "city_list",

    "search_active",

    "precipitation_map",

    "severe_alert",

    "alert_detail",
]


WEATHER_STATE_WEIGHTS = [

    24,

    14,

    14,

    12,

    10,

    10,

    10,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Weather Conditions
# ==========================================================

CONDITIONS = [

    {
        "name": "Sunny",
        "icon": "sun",
    },

    {
        "name": "Mostly Sunny",
        "icon": "cloud-sun",
    },

    {
        "name": "Cloudy",
        "icon": "cloud",
    },

    {
        "name": "Rain",
        "icon": "cloud-rain",
    },

    {
        "name": "Showers",
        "icon": "cloud-drizzle",
    },

    {
        "name": "Thunderstorms",
        "icon": "cloud-lightning",
    },

    {
        "name": "Snow",
        "icon": "cloud-snow",
    },
]


# ==========================================================
# Cities
# ==========================================================

CITY_POOL = [

    {
        "name": "Seoul",
        "country": "South Korea",
    },

    {
        "name": "Busan",
        "country": "South Korea",
    },

    {
        "name": "Tokyo",
        "country": "Japan",
    },

    {
        "name": "New York",
        "country": "United States",
    },

    {
        "name": "London",
        "country": "United Kingdom",
    },

    {
        "name": "Paris",
        "country": "France",
    },

    {
        "name": "Singapore",
        "country": "Singapore",
    },

    {
        "name": "Sydney",
        "country": "Australia",
    },
]


# ==========================================================
# Current Weather
# ==========================================================

def generate_current_weather() -> dict:

    condition = random.choice(
        CONDITIONS
    )

    temperature = random.randint(
        -3,
        34,
    )


    return {

        "temperature":
            temperature,

        "condition":
            condition["name"],

        "condition_icon":
            get_lucide_icon(
                condition["icon"]
            ),

        "high":
            temperature
            + random.randint(
                2,
                6,
            ),

        "low":
            temperature
            - random.randint(
                3,
                8,
            ),

        "feels_like":
            temperature
            + random.randint(
                -2,
                2,
            ),

        "humidity":
            random.randint(
                35,
                90,
            ),

        "wind":
            random.randint(
                2,
                28,
            ),

        "visibility":
            random.randint(
                6,
                20,
            ),

        "uv_index":
            random.randint(
                0,
                9,
            ),

        "pressure":
            random.randint(
                995,
                1028,
            ),
    }


# ==========================================================
# Hourly Forecast
# ==========================================================

def generate_hourly_forecast(
    current_temperature: int,
) -> list[dict]:

    now = datetime.now()

    result = []


    for index in range(
        12
    ):

        current_time = (
            now
            + timedelta(
                hours=index
            )
        )

        condition = random.choice(
            CONDITIONS[:5]
        )


        result.append({

            "id":
                f"hour_{index}",

            "time":
                (
                    "Now"
                    if index == 0
                    else current_time.strftime(
                        "%-I %p"
                    )
                ),

            "temperature":
                current_temperature
                + random.randint(
                    -4,
                    4,
                ),

            "condition":
                condition["name"],

            "icon":
                get_lucide_icon(
                    condition["icon"]
                ),

            "precipitation":
                random.choice([
                    0,
                    0,
                    10,
                    20,
                    30,
                    50,
                    70,
                ]),
        })


    return result


# ==========================================================
# Ten Day Forecast
# ==========================================================

def generate_ten_day_forecast(
    current_temperature: int,
) -> list[dict]:

    now = datetime.now()

    result = []


    for index in range(
        10
    ):

        day = (
            now
            + timedelta(
                days=index
            )
        )

        condition = random.choice(
            CONDITIONS
        )

        low = (
            current_temperature
            + random.randint(
                -8,
                -1,
            )
        )

        high = (
            current_temperature
            + random.randint(
                1,
                8,
            )
        )


        result.append({

            "id":
                f"day_{index}",

            "day":
                (
                    "Today"
                    if index == 0
                    else day.strftime(
                        "%A"
                    )
                ),

            "icon":
                get_lucide_icon(
                    condition["icon"]
                ),

            "condition":
                condition["name"],

            "precipitation":
                random.choice([
                    0,
                    0,
                    10,
                    20,
                    40,
                    60,
                ]),

            "low":
                low,

            "high":
                high,
        })


    return result


# ==========================================================
# City
# ==========================================================

def generate_city_weather(
    city: dict,
) -> dict:

    weather = (
        generate_current_weather()
    )


    return {

        **city,

        "temperature":
            weather["temperature"],

        "condition":
            weather["condition"],

        "high":
            weather["high"],

        "low":
            weather["low"],
    }


# ==========================================================
# City List
# ==========================================================

def generate_city_list() -> list[dict]:

    count = random.randint(
        4,
        7,
    )


    cities = random.sample(
        CITY_POOL,
        k=count,
    )


    return [

        generate_city_weather(
            city
        )

        for city
        in cities
    ]


# ==========================================================
# Search
# ==========================================================

def generate_search_data() -> dict:

    query = random.choice([

        "Seo",

        "Bus",

        "Tokyo",

        "Lon",

        "New",
    ])


    results = [

        city

        for city
        in CITY_POOL

        if query.lower()
        in city["name"].lower()
    ]


    if not results:

        results = random.sample(
            CITY_POOL,
            k=4,
        )


    return {

        "query":
            query,

        "results":
            results,
    }


# ==========================================================
# Severe Alert
# ==========================================================

def generate_alert() -> dict:

    alert_type = random.choice([

        "Heavy Rain Warning",

        "Thunderstorm Advisory",

        "Heat Advisory",

        "Strong Wind Advisory",
    ])


    messages = {

        "Heavy Rain Warning":
            (
                "Heavy rainfall is expected in the area. "
                "Localized flooding may occur."
            ),

        "Thunderstorm Advisory":
            (
                "Thunderstorms with lightning and gusty winds "
                "are possible this afternoon."
            ),

        "Heat Advisory":
            (
                "High temperatures may create dangerous "
                "heat conditions."
            ),

        "Strong Wind Advisory":
            (
                "Strong winds may affect travel and outdoor "
                "activities."
            ),
    }


    return {

        "title":
            alert_type,

        "message":
            messages[
                alert_type
            ],

        "source":
            "Weather Service",

        "time":
            random.choice([
                "Until 6:00 PM",
                "Until 10:00 PM",
                "Through tonight",
                "Until tomorrow morning",
            ]),

        "severity":
            random.choice([
                "moderate",
                "high",
            ]),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_weather_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # Resolve State
    # ======================================================

    if state is None:

        state = random.choices(

            WEATHER_STATES,

            weights=
                WEATHER_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in WEATHER_STATES:

        raise ValueError(
            f"Unknown Weather state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Current City
    # ======================================================

    current_city = random.choice(
        CITY_POOL[:3]
    )


    # ======================================================
    # Current Weather
    # ======================================================

    current = (
        generate_current_weather()
    )


    # ======================================================
    # Alert
    # ======================================================

    alert = (
        generate_alert()
    )


    # ======================================================
    # Overlay
    # ======================================================

    is_overlay_state = (
        state
        == "alert_detail"
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "location":
            current_city,


        "current":
            current,


        "hourly":
            generate_hourly_forecast(
                current[
                    "temperature"
                ]
            ),


        "ten_day":
            generate_ten_day_forecast(
                current[
                    "temperature"
                ]
            ),


        "cities":
            generate_city_list(),


        "search":
            generate_search_data(),


        "alert":
            alert,


        # --------------------------------------------------
        # Precipitation Map
        # --------------------------------------------------

        "map": {

            "title":
                "Precipitation",

            "subtitle":
                "Next 12 Hours",

            "rain_cells": [

                {
                    "x":
                        random.randint(
                            5,
                            85,
                        ),

                    "y":
                        random.randint(
                            8,
                            78,
                        ),

                    "size":
                        random.randint(
                            40,
                            120,
                        ),

                    "intensity":
                        random.choice([
                            "light",
                            "medium",
                            "heavy",
                        ]),
                }

                for _ in range(
                    random.randint(
                        6,
                        12,
                    )
                )
            ],

            "timeline":
                random.randint(
                    10,
                    80,
                ),
        },


        # --------------------------------------------------
        # Icons
        # --------------------------------------------------

        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "list":
                get_lucide_icon(
                    "list"
                ),

            "location":
                resolve_icon(
                    "location",
                    "map-pin",
                ),

            "map":
                resolve_icon(
                    "map",
                    "map"
                ),

            "alert":
                get_lucide_icon(
                    "triangle-alert"
                ),

            "humidity":
                get_lucide_icon(
                    "droplets"
                ),

            "wind":
                get_lucide_icon(
                    "wind"
                ),

            "visibility":
                get_lucide_icon(
                    "eye"
                ),

            "uv":
                get_lucide_icon(
                    "sun"
                ),

            "pressure":
                get_lucide_icon(
                    "gauge"
                ),

            "back":
                resolve_icon(
                    "back",
                    "chevron-left",
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right",
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in WEATHER_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_weather_data(
                state=
                    state
            ),

            sort_dicts=False,
        )