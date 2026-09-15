from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

WIDGETS_STATES = [
    "default",
    "weather_expanded",
    "calendar_expanded",
    "stocks",
    "news_feed",
    "sports",
    "tasks",
    "customize",
    "widget_menu",
    "loading",
    "offline",
]


# ==========================================================
# Weather
# ==========================================================

WEATHER_CONDITIONS = [
    {
        "condition": "Sunny",
        "icon": "sunny",
    },
    {
        "condition": "Partly cloudy",
        "icon": "partly_cloudy_day",
    },
    {
        "condition": "Cloudy",
        "icon": "cloud",
    },
    {
        "condition": "Light rain",
        "icon": "rainy",
    },
]


# ==========================================================
# News Pool
# ==========================================================

NEWS_POOL = [
    {
        "source": "Tech Daily",
        "title": "New developer tools improve everyday workflows",
        "icon": "terminal",
        "category": "Technology",
    },
    {
        "source": "World News",
        "title": "Cities introduce new digital public services",
        "icon": "public",
        "category": "World",
    },
    {
        "source": "Science Weekly",
        "title": "Researchers publish new computing study",
        "icon": "science",
        "category": "Science",
    },
    {
        "source": "Business Report",
        "title": "Technology sector sees another active week",
        "icon": "finance",
        "category": "Business",
    },
    {
        "source": "Design Journal",
        "title": "Interface design trends continue to evolve",
        "icon": "palette",
        "category": "Design",
    },
    {
        "source": "Campus News",
        "title": "University announces upcoming research events",
        "icon": "school",
        "category": "Education",
    },
]


# ==========================================================
# Stocks
# ==========================================================

STOCK_POOL = [
    {
        "symbol": "MSFT",
        "name": "Microsoft",
    },
    {
        "symbol": "AAPL",
        "name": "Apple",
    },
    {
        "symbol": "NVDA",
        "name": "NVIDIA",
    },
    {
        "symbol": "GOOG",
        "name": "Alphabet",
    },
]


# ==========================================================
# Tasks
# ==========================================================

TASK_POOL = [
    "Review experiment results",
    "Prepare research slides",
    "Check training logs",
    "Update dataset annotations",
    "Read new paper",
    "Send meeting notes",
]


# ==========================================================
# Widget Types
# ==========================================================

AVAILABLE_WIDGETS = [
    {
        "id": "weather",
        "title": "Weather",
        "icon": "sunny",
    },
    {
        "id": "calendar",
        "title": "Calendar",
        "icon": "calendar_month",
    },
    {
        "id": "stocks",
        "title": "Watchlist",
        "icon": "show_chart",
    },
    {
        "id": "tasks",
        "title": "To Do",
        "icon": "check_circle",
    },
    {
        "id": "sports",
        "title": "Sports",
        "icon": "sports_soccer",
    },
    {
        "id": "traffic",
        "title": "Traffic",
        "icon": "traffic",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_weather() -> dict:

    condition = random.choice(
        WEATHER_CONDITIONS
    )

    current = random.randint(
        8,
        32,
    )

    forecast = []

    for day in [
        "Today",
        "Sun",
        "Mon",
        "Tue",
        "Wed",
    ]:

        item = random.choice(
            WEATHER_CONDITIONS
        )

        low = random.randint(
            5,
            22,
        )

        high = random.randint(
            low + 2,
            min(
                low + 12,
                34,
            ),
        )

        forecast.append(
            {
                "day": day,
                "icon": item["icon"],
                "low": low,
                "high": high,
            }
        )

    return {
        "location":
            random.choice(
                [
                    "Seoul",
                    "Busan",
                    "Incheon",
                    "Daejeon",
                ]
            ),

        "temperature":
            current,

        "condition":
            condition["condition"],

        "icon":
            condition["icon"],

        "feels_like":
            current
            + random.randint(
                -2,
                2,
            ),

        "humidity":
            random.randint(
                35,
                85,
            ),

        "forecast":
            forecast,
    }


def generate_calendar() -> dict:

    selected_day = random.randint(
        1,
        30,
    )

    return {
        "month":
            random.choice(
                [
                    "September 2026",
                    "October 2026",
                ]
            ),

        "selected_day":
            selected_day,

        "days":
            list(
                range(
                    1,
                    31,
                )
            ),

        "events": [
            {
                "title": "Research meeting",
                "time": "2:30 PM",
            },
            {
                "title": "Project review",
                "time": "4:00 PM",
            },
            {
                "title": "Read papers",
                "time": "6:00 PM",
            },
        ],
    }


def generate_stocks() -> list[dict]:

    result = []

    for stock in STOCK_POOL:

        change = round(
            random.uniform(
                -4.5,
                5.5,
            ),
            2,
        )

        result.append(
            {
                **stock,

                "price":
                    round(
                        random.uniform(
                            90,
                            520,
                        ),
                        2,
                    ),

                "change":
                    change,

                "positive":
                    change >= 0,
            }
        )

    return result


def generate_tasks() -> list[dict]:

    count = random.randint(
        3,
        6,
    )

    return [
        {
            "title":
                title,

            "completed":
                random.random()
                < 0.30,
        }
        for title in random.sample(
            TASK_POOL,
            k=count,
        )
    ]


def generate_news() -> list[dict]:

    return random.sample(
        NEWS_POOL,
        k=random.randint(
            3,
            min(
                6,
                len(
                    NEWS_POOL
                ),
            ),
        ),
    )


def generate_sports() -> list[dict]:

    return [
        {
            "home": "Seoul FC",
            "away": "Busan FC",
            "home_score": random.randint(0, 4),
            "away_score": random.randint(0, 4),
            "status": "Final",
        },
        {
            "home": "Tigers",
            "away": "Bears",
            "home_score": random.randint(0, 8),
            "away_score": random.randint(0, 8),
            "status": "Today",
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_widgets_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            WIDGETS_STATES
        )


    if state not in WIDGETS_STATES:

        raise ValueError(
            f"Unknown widgets state: {state}"
        )


    active_widgets = random.sample(
        AVAILABLE_WIDGETS,
        k=random.randint(
            3,
            min(
                5,
                len(
                    AVAILABLE_WIDGETS
                ),
            ),
        ),
    )


    return {
        "state":
            state,

        "weather":
            generate_weather(),

        "calendar":
            generate_calendar(),

        "stocks":
            generate_stocks(),

        "tasks":
            generate_tasks(),

        "news":
            generate_news(),

        "sports":
            generate_sports(),

        "available_widgets":
            AVAILABLE_WIDGETS,

        "active_widgets":
            active_widgets,

        "selected_widget":
            (
                random.choice(
                    active_widgets
                )
                if state
                == "widget_menu"
                else None
            ),
    }