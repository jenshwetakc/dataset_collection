from __future__ import annotations

import calendar
import random
from datetime import date

from faker import Faker


fake = Faker()


NAVIGATION_ITEMS = [
    {
        "key": "learn",
        "label": "Learn",
        "icon": "home",
    },
    {
        "key": "practice",
        "label": "Practice",
        "icon": "fitness_center",
    },
    {
        "key": "leaderboard",
        "label": "Leaderboards",
        "icon": "trophy",
    },
    {
        "key": "quests",
        "label": "Quests",
        "icon": "task_alt",
    },
    {
        "key": "shop",
        "label": "Shop",
        "icon": "storefront",
    },
    {
        "key": "profile",
        "label": "Profile",
        "icon": "person",
    },
]


# ==========================================================
# Calendar
# ==========================================================

def generate_calendar_days() -> dict:

    today = date.today()

    year = today.year
    month = today.month

    first_weekday, days_in_month = (
        calendar.monthrange(
            year,
            month,
        )
    )

    cells = []

    # Monday-first layout
    for _ in range(
        first_weekday
    ):

        cells.append(
            {
                "empty": True,
            }
        )

    for day in range(
        1,
        days_in_month + 1,
    ):

        is_today = (
            day == today.day
        )

        studied = (
            day < today.day
            and random.random()
            < 0.82
        )

        if is_today:

            studied = random.random() < 0.6

        frozen = (
            not studied
            and day < today.day
            and random.random()
            < 0.12
        )

        cells.append(
            {
                "empty":
                    False,

                "day":
                    day,

                "today":
                    is_today,

                "studied":
                    studied,

                "frozen":
                    frozen,

                "xp":
                    (
                        random.randint(
                            5,
                            90,
                        )
                        if studied
                        else 0
                    ),
            }
        )

    return {
        "year":
            year,

        "month":
            month,

        "month_name":
            calendar.month_name[
                month
            ],

        "cells":
            cells,
    }


# ==========================================================
# Weekly Activity
# ==========================================================

def generate_week_activity() -> list[dict]:

    labels = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    values = [
        random.randint(
            0,
            80,
        )
        for _ in labels
    ]

    maximum = max(
        max(values),
        1,
    )

    return [
        {
            "label":
                label,

            "xp":
                value,

            "progress":
                value
                / maximum,
        }
        for label, value
        in zip(
            labels,
            values,
        )
    ]


# ==========================================================
# Milestones
# ==========================================================

def generate_milestones(
    streak: int,
) -> list[dict]:

    thresholds = [
        7,
        30,
        50,
        100,
        365,
    ]

    icons = [
        "local_fire_department",
        "bolt",
        "workspace_premium",
        "trophy",
        "diamond",
    ]

    return [
        {
            "days":
                threshold,

            "icon":
                icons[index],

            "reached":
                streak
                >= threshold,
        }
        for index, threshold
        in enumerate(
            thresholds
        )
    ]


# ==========================================================
# Generator
# ==========================================================

def generate_streak_data() -> dict:

    streak = random.randint(
        3,
        420,
    )

    best_streak = max(
        streak,
        streak
        + random.randint(
            0,
            180,
        ),
    )

    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,
                "selected":
                    False,
            }
        )

    return {
        "streak": {
            "current":
                streak,

            "best":
                best_streak,

            "weeks":
                streak // 7,

            "freeze_count":
                random.randint(
                    0,
                    3,
                ),

            "goal":
                random.choice(
                    [
                        7,
                        14,
                        30,
                        50,
                        100,
                    ]
                ),
        },

        "calendar":
            generate_calendar_days(),

        "week_activity":
            generate_week_activity(),

        "milestones":
            generate_milestones(
                streak
            ),

        "repair": {
            "visible":
                random.random()
                < 0.35,

            "days_missed":
                random.choice(
                    [
                        1,
                        2,
                    ]
                ),

            "price":
                random.choice(
                    [
                        200,
                        300,
                        500,
                    ]
                ),
        },

        "stats": {
            "gems":
                random.randint(
                    100,
                    5000,
                ),

            "hearts":
                random.randint(
                    1,
                    5,
                ),
        },

        "navigation_items":
            navigation_items,
    }