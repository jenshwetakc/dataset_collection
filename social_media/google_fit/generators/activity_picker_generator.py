from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

ACTIVITY_PICKER_STATES = [
    "browse",
    "search_active",
    "filtered",
    "no_results",
    "recent_empty",
    "activity_selected",
]


# ==========================================================
# Categories
# ==========================================================

ACTIVITY_CATEGORIES = [
    {
        "key": "popular",
        "label": "Popular",
        "icon": "star",
    },
    {
        "key": "cardio",
        "label": "Cardio",
        "icon": "favorite",
    },
    {
        "key": "strength",
        "label": "Strength",
        "icon": "fitness_center",
    },
    {
        "key": "mind_body",
        "label": "Mind & body",
        "icon": "self_improvement",
    },
    {
        "key": "outdoor",
        "label": "Outdoor",
        "icon": "landscape",
    },
]


# ==========================================================
# Activities
# ==========================================================

ACTIVITIES = [
    {
        "key": "walking",
        "name": "Walking",
        "icon": "directions_walk",
        "category": "cardio",
        "popular": True,
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "key": "running",
        "name": "Running",
        "icon": "directions_run",
        "category": "cardio",
        "popular": True,
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "key": "cycling",
        "name": "Cycling",
        "icon": "directions_bike",
        "category": "cardio",
        "popular": True,
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "key": "hiking",
        "name": "Hiking",
        "icon": "hiking",
        "category": "outdoor",
        "popular": True,
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "key": "strength_training",
        "name": "Strength training",
        "icon": "fitness_center",
        "category": "strength",
        "popular": True,
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "key": "yoga",
        "name": "Yoga",
        "icon": "self_improvement",
        "category": "mind_body",
        "popular": True,
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "key": "pilates",
        "name": "Pilates",
        "icon": "accessibility_new",
        "category": "mind_body",
        "popular": False,
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "key": "swimming",
        "name": "Swimming",
        "icon": "pool",
        "category": "cardio",
        "popular": True,
        "supports_distance": True,
        "supports_route": False,
    },
    {
        "key": "rowing",
        "name": "Rowing",
        "icon": "rowing",
        "category": "strength",
        "popular": False,
        "supports_distance": True,
        "supports_route": False,
    },
    {
        "key": "elliptical",
        "name": "Elliptical",
        "icon": "exercise",
        "category": "cardio",
        "popular": False,
        "supports_distance": True,
        "supports_route": False,
    },
    {
        "key": "dance",
        "name": "Dance",
        "icon": "music_note",
        "category": "cardio",
        "popular": False,
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "key": "meditation",
        "name": "Meditation",
        "icon": "spa",
        "category": "mind_body",
        "popular": False,
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "key": "tennis",
        "name": "Tennis",
        "icon": "sports_tennis",
        "category": "outdoor",
        "popular": False,
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "key": "basketball",
        "name": "Basketball",
        "icon": "sports_basketball",
        "category": "outdoor",
        "popular": False,
        "supports_distance": False,
        "supports_route": False,
    },
]


# ==========================================================
# Recent Activities
# ==========================================================

def generate_recent_activities() -> list[dict]:

    count = random.randint(
        3,
        5,
    )

    return [
        dict(activity)
        for activity in random.sample(
            ACTIVITIES,
            k=count,
        )
    ]


# ==========================================================
# Categories
# ==========================================================

def generate_categories(
    selected_key: str | None = None,
) -> list[dict]:

    result = []

    for category in ACTIVITY_CATEGORIES:

        result.append(
            {
                **category,
                "selected":
                    (
                        category["key"]
                        == selected_key
                    ),
            }
        )

    return result


# ==========================================================
# Browse State
# ==========================================================

def generate_browse_state() -> dict:

    popular = [
        dict(activity)
        for activity in ACTIVITIES
        if activity["popular"]
    ]

    return {

        "query":
            "",

        "categories":
            generate_categories(),

        "recent":
            generate_recent_activities(),

        "activities":
            popular,

        "selected_activity":
            None,

        "active_filter":
            None,

        "message":
            None,

        "description":
            None,
    }


# ==========================================================
# Search State
# ==========================================================

def generate_search_state() -> dict:

    query = random.choice(
        [
            "run",
            "walk",
            "yoga",
            "swim",
            "cycle",
        ]
    )

    results = [
        dict(activity)
        for activity in ACTIVITIES
        if query.lower()
        in activity["name"].lower()
    ]

    return {

        "query":
            query,

        "categories":
            generate_categories(),

        "recent":
            [],

        "activities":
            results,

        "selected_activity":
            None,

        "active_filter":
            None,

        "message":
            None,

        "description":
            None,
    }


# ==========================================================
# Filtered State
# ==========================================================

def generate_filtered_state() -> dict:

    category = random.choice(
        [
            item
            for item in ACTIVITY_CATEGORIES
            if item["key"] != "popular"
        ]
    )

    results = [
        dict(activity)
        for activity in ACTIVITIES
        if (
            activity["category"]
            == category["key"]
        )
    ]

    return {

        "query":
            "",

        "categories":
            generate_categories(
                selected_key=
                    category["key"]
            ),

        "recent":
            [],

        "activities":
            results,

        "selected_activity":
            None,

        "active_filter":
            category,

        "message":
            None,

        "description":
            None,
    }


# ==========================================================
# No Results
# ==========================================================

def generate_no_results_state() -> dict:

    query = random.choice(
        [
            "underwater running",
            "mountain surfing",
            "aerial recovery",
            "speed meditation",
        ]
    )

    return {

        "query":
            query,

        "categories":
            generate_categories(),

        "recent":
            [],

        "activities":
            [],

        "selected_activity":
            None,

        "active_filter":
            None,

        "message":
            "No activities found",

        "description":
            (
                f'No activity matches "{query}". '
                "Try another search or browse by category."
            ),
    }


# ==========================================================
# Recent Empty
# ==========================================================

def generate_recent_empty_state() -> dict:

    return {

        "query":
            "",

        "categories":
            generate_categories(),

        "recent":
            [],

        "activities": [
            dict(activity)
            for activity in ACTIVITIES
            if activity["popular"]
        ],

        "selected_activity":
            None,

        "active_filter":
            None,

        "message":
            "No recent activities",

        "description":
            (
                "Activities you track often will appear "
                "here for quicker access."
            ),
    }


# ==========================================================
# Selected Activity
# ==========================================================

def generate_selected_state() -> dict:

    base = (
        generate_browse_state()
    )

    selected = random.choice(
        ACTIVITIES
    )

    base.update(
        {
            "selected_activity":
                dict(selected),
        }
    )

    return base


# ==========================================================
# Public Generator
# ==========================================================

def generate_activity_picker_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            ACTIVITY_PICKER_STATES
        )


    if state not in (
        ACTIVITY_PICKER_STATES
    ):

        raise ValueError(
            f"Unknown activity picker state: "
            f"{state}. "
            f"Available states: "
            f"{ACTIVITY_PICKER_STATES}"
        )


    if state == "browse":

        state_data = (
            generate_browse_state()
        )

    elif state == "search_active":

        state_data = (
            generate_search_state()
        )

    elif state == "filtered":

        state_data = (
            generate_filtered_state()
        )

    elif state == "no_results":

        state_data = (
            generate_no_results_state()
        )

    elif state == "recent_empty":

        state_data = (
            generate_recent_empty_state()
        )

    else:

        state_data = (
            generate_selected_state()
        )


    return {

        "state":
            state,

        "title":
            "Add activity",

        **state_data,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in (
        ACTIVITY_PICKER_STATES
    ):

        print(
            "\n"
            "======================================"
        )

        print(
            state.upper()
        )

        print(
            "======================================"
        )

        pprint(
            generate_activity_picker_data(
                state=state
            )
        )