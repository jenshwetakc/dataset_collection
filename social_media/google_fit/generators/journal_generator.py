from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from social_media.google_fit.generators.media_generator import (
    get_random_workout_image,
)


# ==========================================================
# Activity Types
# ==========================================================

ACTIVITY_TYPES = [
    {
        "name": "Walking",
        "icon": "directions_walk",
    },
    {
        "name": "Running",
        "icon": "directions_run",
    },
    {
        "name": "Cycling",
        "icon": "directions_bike",
    },
    {
        "name": "Hiking",
        "icon": "hiking",
    },
    {
        "name": "Yoga",
        "icon": "self_improvement",
    },
    {
        "name": "Strength training",
        "icon": "fitness_center",
    },
    {
        "name": "Elliptical",
        "icon": "exercise",
    },
]


FILTERS = [
    {
        "label": "All",
        "icon": "apps",
        "active": True,
    },
    {
        "label": "Walking",
        "icon": "directions_walk",
        "active": False,
    },
    {
        "label": "Running",
        "icon": "directions_run",
        "active": False,
    },
    {
        "label": "Cycling",
        "icon": "directions_bike",
        "active": False,
    },
]


NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "active": False,
    },
    {
        "label": "Journal",
        "icon": "view_timeline",
        "active": True,
    },
    {
        "label": "Browse",
        "icon": "explore",
        "active": False,
    },
    {
        "label": "Profile",
        "icon": "person",
        "active": False,
    },
]


# ==========================================================
# Generate One Activity
# ==========================================================

def generate_activity(
    index: int,
    date: datetime,
) -> dict:

    activity_type = random.choice(
        ACTIVITY_TYPES
    )

    duration = random.randint(
        12,
        95,
    )

    has_distance = (
        activity_type["name"]
        in {
            "Walking",
            "Running",
            "Cycling",
            "Hiking",
        }
    )

    distance = (
        round(
            random.uniform(
                1.0,
                15.0,
            ),
            1,
        )
        if has_distance
        else None
    )

    calories = random.randint(
        70,
        750,
    )

    start_hour = random.randint(
        6,
        21,
    )

    start_minute = random.choice(
        [
            0,
            5,
            10,
            15,
            20,
            30,
            45,
            50,
        ]
    )

    start_time = date.replace(
        hour=start_hour,
        minute=start_minute,
    )

    heart_points = random.randint(
        2,
        18,
    )

    has_route = (
        has_distance
        and random.random() < 0.40
    )

    has_image = (
        random.random() < 0.30
    )

    return {

        "id":
            index,

        "title":
            activity_type[
                "name"
            ],

        "icon":
            activity_type[
                "icon"
            ],

        "time":
            start_time.strftime(
                "%H:%M"
            ),

        "duration":
            f"{duration} min",

        "distance":
            (
                f"{distance:.1f} km"
                if distance is not None
                else None
            ),

        "calories":
            f"{calories} Cal",

        "heart_points":
            heart_points,

        "has_route":
            has_route,

        "image":
            (
                get_random_workout_image()
                if has_image
                else None
            ),
    }


# ==========================================================
# Generate Day
# ==========================================================

def generate_day(
    date: datetime,
    starting_index: int,
) -> tuple[dict, int]:

    activity_count = random.randint(
        1,
        4,
    )

    activities = []

    current_index = (
        starting_index
    )

    for _ in range(
        activity_count
    ):

        activities.append(
            generate_activity(
                current_index,
                date,
            )
        )

        current_index += 1

    steps = random.randint(
        2500,
        15000,
    )

    calories = random.randint(
        1300,
        2800,
    )

    heart_points = random.randint(
        5,
        55,
    )

    return (
        {
            "date":
                date.strftime(
                    "%Y-%m-%d"
                ),

            "label":
                date.strftime(
                    "%A, %B %d"
                ),

            "short_label":
                date.strftime(
                    "%a %d"
                ),

            "steps":
                f"{steps:,}",

            "calories":
                f"{calories:,}",

            "heart_points":
                heart_points,

            "activities":
                activities,
        },
        current_index,
    )


# ==========================================================
# Summary
# ==========================================================

def generate_summary(
    days: list[dict],
) -> dict:

    total_activities = sum(
        len(
            day[
                "activities"
            ]
        )
        for day
        in days
    )

    total_minutes = 0

    for day in days:

        for activity in (
            day[
                "activities"
            ]
        ):

            total_minutes += int(
                activity[
                    "duration"
                ].split()[0]
            )

    active_days = len(
        [
            day
            for day in days
            if day["activities"]
        ]
    )

    return {

        "activity_count":
            total_activities,

        "active_days":
            active_days,

        "total_minutes":
            total_minutes,

        "hours":
            total_minutes // 60,

        "remaining_minutes":
            total_minutes % 60,
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_journal_data() -> dict:

    today = datetime.now()

    number_of_days = random.randint(
        6,
        10,
    )

    days = []

    activity_index = 0

    for offset in range(
        number_of_days
    ):

        date = (
            today
            - timedelta(
                days=offset
            )
        )

        day, activity_index = (
            generate_day(
                date,
                activity_index,
            )
        )

        days.append(
            day
        )

    return {

        "title":
            "Journal",

        "subtitle":
            "Your activity history",

        "filters": [
            dict(
                item
            )
            for item
            in FILTERS
        ],

        "days":
            days,

        "summary":
            generate_summary(
                days
            ),

        "navigation_items": [
            dict(
                item
            )
            for item
            in NAVIGATION_ITEMS
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_journal_data()
    )