from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.google_fit.generators.media_generator import (
    get_random_avatar,
    get_random_workout_image,
)


fake = Faker()


# ==========================================================
# Constants
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
        "name": "Workout",
        "icon": "fitness_center",
    },
]


HEALTH_METRICS = [
    {
        "key": "heart_rate",
        "title": "Heart rate",
        "icon": "favorite",
        "unit": "bpm",
    },
    {
        "key": "sleep",
        "title": "Sleep",
        "icon": "bedtime",
        "unit": "hr",
    },
    {
        "key": "weight",
        "title": "Weight",
        "icon": "monitor_weight",
        "unit": "kg",
    },
    {
        "key": "oxygen",
        "title": "Blood oxygen",
        "icon": "spo2",
        "unit": "%",
    },
]


NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "active": True,
    },
    {
        "label": "Journal",
        "icon": "view_timeline",
        "active": False,
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
# Number Helpers
# ==========================================================

def _progress(
    value: float,
    goal: float,
) -> float:

    if goal <= 0:
        return 0.0

    return min(
        1.0,
        value / goal,
    )


# ==========================================================
# Main Activity Summary
# ==========================================================

def generate_activity_summary() -> dict:

    steps_goal = random.choice(
        [
            6000,
            7500,
            8000,
            10000,
            12000,
        ]
    )

    steps = random.randint(
        1800,
        int(
            steps_goal * 1.25
        ),
    )

    heart_goal = random.choice(
        [
            20,
            30,
            40,
            50,
        ]
    )

    heart_points = random.randint(
        4,
        int(
            heart_goal * 1.30
        ),
    )

    move_minutes_goal = random.choice(
        [
            45,
            60,
            75,
            90,
        ]
    )

    move_minutes = random.randint(
        15,
        int(
            move_minutes_goal * 1.20
        ),
    )

    distance = round(
        steps
        * random.uniform(
            0.00062,
            0.00082,
        ),
        1,
    )

    calories = random.randint(
        750,
        2450,
    )

    return {

        "steps": {
            "value": steps,
            "formatted":
                f"{steps:,}",
            "goal":
                steps_goal,
            "goal_formatted":
                f"{steps_goal:,}",
            "progress":
                _progress(
                    steps,
                    steps_goal,
                ),
        },

        "heart_points": {
            "value":
                heart_points,
            "goal":
                heart_goal,
            "progress":
                _progress(
                    heart_points,
                    heart_goal,
                ),
        },

        "move_minutes": {
            "value":
                move_minutes,
            "goal":
                move_minutes_goal,
            "progress":
                _progress(
                    move_minutes,
                    move_minutes_goal,
                ),
        },

        "calories": {
            "value":
                calories,
            "formatted":
                f"{calories:,}",
            "unit":
                "Cal",
        },

        "distance": {
            "value":
                distance,
            "formatted":
                f"{distance:.1f}",
            "unit":
                "km",
        },
    }


# ==========================================================
# Weekly Activity
# ==========================================================

def generate_weekly_activity() -> list[dict]:

    today = datetime.now()

    result = []

    for offset in range(
        6,
        -1,
        -1,
    ):

        date = (
            today
            - timedelta(
                days=offset
            )
        )

        value = random.randint(
            1800,
            12000,
        )

        result.append(
            {
                "day":
                    date.strftime(
                        "%a"
                    )[0],

                "date":
                    date.strftime(
                        "%b %d"
                    ),

                "value":
                    value,

                "height":
                    random.randint(
                        25,
                        100,
                    ),
            }
        )

    return result


# ==========================================================
# Recent Activity
# ==========================================================

def generate_recent_activity(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            4,
            7,
        )

    activities = []

    base_time = datetime.now()

    for index in range(
        count
    ):

        activity = random.choice(
            ACTIVITY_TYPES
        )

        duration_minutes = random.randint(
            12,
            92,
        )

        distance = round(
            random.uniform(
                0.8,
                12.0,
            ),
            1,
        )

        start_time = (
            base_time
            - timedelta(
                hours=random.randint(
                    1,
                    72,
                )
            )
        )

        calories = random.randint(
            60,
            620,
        )

        activities.append(
            {
                "title":
                    activity[
                        "name"
                    ],

                "icon":
                    activity[
                        "icon"
                    ],

                "duration":
                    f"{duration_minutes} min",

                "distance":
                    f"{distance:.1f} km",

                "calories":
                    f"{calories} Cal",

                "time":
                    start_time.strftime(
                        "%a, %H:%M"
                    ),

                "image":
                    (
                        get_random_workout_image()
                        if random.random() < 0.45
                        else None
                    ),
            }
        )

    return activities


# ==========================================================
# Health Metrics
# ==========================================================

def generate_health_metrics() -> list[dict]:

    values = {

        "heart_rate":
            lambda: (
                str(
                    random.randint(
                        58,
                        92,
                    )
                ),
                "bpm",
                f"Resting {random.randint(55, 75)} bpm",
            ),

        "sleep":
            lambda: (
                f"{random.randint(5, 8)}h "
                f"{random.randint(0, 59):02d}m",
                "",
                random.choice(
                    [
                        "Last night",
                        "Good sleep",
                        "On schedule",
                    ]
                ),
            ),

        "weight":
            lambda: (
                f"{random.uniform(48, 92):.1f}",
                "kg",
                random.choice(
                    [
                        "Latest measurement",
                        "Stable this week",
                        "Updated today",
                    ]
                ),
            ),

        "oxygen":
            lambda: (
                str(
                    random.randint(
                        95,
                        100,
                    )
                ),
                "%",
                "Latest reading",
            ),
    }

    selected = random.sample(
        HEALTH_METRICS,
        k=random.randint(
            3,
            len(
                HEALTH_METRICS
            ),
        ),
    )

    result = []

    for metric in selected:

        value, unit, subtitle = (
            values[
                metric["key"]
            ]()
        )

        result.append(
            {
                **metric,

                "value":
                    value,

                "unit":
                    unit,

                "subtitle":
                    subtitle,
            }
        )

    return result


# ==========================================================
# Insight
# ==========================================================

def generate_insight() -> dict:

    insights = [
        {
            "icon": "trending_up",
            "title": "You're moving more",
            "description":
                "You've been more active than your recent average.",
        },
        {
            "icon": "directions_walk",
            "title": "Keep your streak going",
            "description":
                "A short walk today can help you stay on track.",
        },
        {
            "icon": "bedtime",
            "title": "Sleep consistency",
            "description":
                "Your sleep schedule has been more consistent this week.",
        },
        {
            "icon": "favorite",
            "title": "Heart Points",
            "description":
                "Moderate activity can help you earn more Heart Points.",
        },
    ]

    return random.choice(
        insights
    )


# ==========================================================
# Greeting
# ==========================================================

def generate_greeting() -> str:

    hour = datetime.now().hour

    if hour < 12:
        return "Good morning"

    if hour < 18:
        return "Good afternoon"

    return "Good evening"


# ==========================================================
# Public Generator
# ==========================================================

def generate_home_data() -> dict:

    activity_summary = (
        generate_activity_summary()
    )

    return {

        "app_name":
            "Fit",

        "greeting":
            generate_greeting(),

        "user_name":
            fake.first_name(),

        "avatar":
            get_random_avatar(),

        "date_label":
            datetime.now().strftime(
                "%A, %B %d"
            ),

        "activity_summary":
            activity_summary,

        "weekly_activity":
            generate_weekly_activity(),

        "recent_activities":
            generate_recent_activity(),

        "health_metrics":
            generate_health_metrics(),

        "insight":
            generate_insight(),

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
        generate_home_data()
    )