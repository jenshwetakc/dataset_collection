from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

BROWSE_STATES = [
    "default",
    "search_active",
    "filtered",
    "empty_search",
    "offline",
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "active": False,
    },
    {
        "label": "Journal",
        "icon": "view_timeline",
        "active": False,
    },
    {
        "label": "Browse",
        "icon": "explore",
        "active": True,
    },
    {
        "label": "Profile",
        "icon": "person",
        "active": False,
    },
]


# ==========================================================
# Categories
# ==========================================================

HEALTH_CATEGORIES = [
    {
        "key": "activity",
        "title": "Activity",
        "icon": "directions_run",
        "description": "Steps, distance and movement",
    },
    {
        "key": "body",
        "title": "Body measurements",
        "icon": "monitor_weight",
        "description": "Weight, height and body composition",
    },
    {
        "key": "sleep",
        "title": "Sleep",
        "icon": "bedtime",
        "description": "Sleep duration and schedule",
    },
    {
        "key": "heart",
        "title": "Heart",
        "icon": "favorite",
        "description": "Heart rate and cardiovascular data",
    },
    {
        "key": "nutrition",
        "title": "Nutrition",
        "icon": "restaurant",
        "description": "Food, hydration and nutrition",
    },
    {
        "key": "vitals",
        "title": "Vitals",
        "icon": "monitor_heart",
        "description": "Oxygen, temperature and respiratory data",
    },
]


# ==========================================================
# Data Types
# ==========================================================

DATA_TYPES = [
    {
        "title": "Steps",
        "icon": "footprint",
        "category": "Activity",
        "value": "7,482",
        "unit": "steps",
    },
    {
        "title": "Distance",
        "icon": "route",
        "category": "Activity",
        "value": "5.6",
        "unit": "km",
    },
    {
        "title": "Heart rate",
        "icon": "favorite",
        "category": "Heart",
        "value": "72",
        "unit": "bpm",
    },
    {
        "title": "Sleep",
        "icon": "bedtime",
        "category": "Sleep",
        "value": "7h 24m",
        "unit": "",
    },
    {
        "title": "Weight",
        "icon": "monitor_weight",
        "category": "Body measurements",
        "value": "63.4",
        "unit": "kg",
    },
    {
        "title": "Blood oxygen",
        "icon": "spo2",
        "category": "Vitals",
        "value": "98",
        "unit": "%",
    },
    {
        "title": "Calories burned",
        "icon": "local_fire_department",
        "category": "Activity",
        "value": "1,820",
        "unit": "Cal",
    },
    {
        "title": "Hydration",
        "icon": "water_drop",
        "category": "Nutrition",
        "value": "1.7",
        "unit": "L",
    },
]


# ==========================================================
# Search Suggestions
# ==========================================================

SEARCH_SUGGESTIONS = [
    "Heart rate",
    "Sleep",
    "Steps",
    "Weight",
    "Calories",
    "Blood oxygen",
    "Hydration",
]


# ==========================================================
# Default
# ==========================================================

def generate_default_state() -> dict:

    featured = random.sample(
        DATA_TYPES,
        k=4,
    )

    return {
        "categories":
            [
                dict(item)
                for item
                in HEALTH_CATEGORIES
            ],

        "featured":
            featured,

        "search_query":
            "",

        "search_results":
            [],

        "filter_label":
            None,
    }


# ==========================================================
# Search
# ==========================================================

def generate_search_active_state() -> dict:

    query = random.choice(
        [
            "heart",
            "sleep",
            "weight",
            "activity",
        ]
    )

    results = [
        item
        for item
        in DATA_TYPES
        if (
            query.lower()
            in item["title"].lower()
            or query.lower()
            in item["category"].lower()
        )
    ]

    return {
        "categories":
            [],

        "featured":
            [],

        "search_query":
            query,

        "search_results":
            results,

        "suggestions":
            random.sample(
                SEARCH_SUGGESTIONS,
                k=4,
            ),

        "filter_label":
            None,
    }


# ==========================================================
# Filtered
# ==========================================================

def generate_filtered_state() -> dict:

    category = random.choice(
        [
            "Activity",
            "Heart",
            "Sleep",
            "Vitals",
        ]
    )

    results = [
        item
        for item
        in DATA_TYPES
        if item["category"] == category
    ]

    return {
        "categories":
            [],

        "featured":
            [],

        "search_query":
            "",

        "search_results":
            results,

        "filter_label":
            category,
    }


# ==========================================================
# Empty Search
# ==========================================================

def generate_empty_search_state() -> dict:

    query = random.choice(
        [
            "blood sugar trend",
            "rowing cadence",
            "metabolic age",
            "recovery score",
        ]
    )

    return {
        "categories":
            [],

        "featured":
            [],

        "search_query":
            query,

        "search_results":
            [],

        "suggestions":
            random.sample(
                SEARCH_SUGGESTIONS,
                k=3,
            ),

        "filter_label":
            None,
    }


# ==========================================================
# Offline
# ==========================================================

def generate_offline_state() -> dict:

    return {
        "categories":
            [],

        "featured":
            [],

        "search_query":
            "",

        "search_results":
            [],

        "filter_label":
            None,
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_browse_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            BROWSE_STATES
        )

    if state not in BROWSE_STATES:

        raise ValueError(
            f"Unknown browse state: {state}"
        )


    if state == "default":

        state_data = (
            generate_default_state()
        )

    elif state == "search_active":

        state_data = (
            generate_search_active_state()
        )

    elif state == "filtered":

        state_data = (
            generate_filtered_state()
        )

    elif state == "empty_search":

        state_data = (
            generate_empty_search_state()
        )

    else:

        state_data = (
            generate_offline_state()
        )


    return {

        "state":
            state,

        "title":
            "Browse",

        "navigation_items": [
            dict(item)
            for item
            in NAVIGATION_ITEMS
        ],

        **state_data,
    }


if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_browse_data()
    )