from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_avatar,
    get_random_achievement,
)


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


ACHIEVEMENT_TEMPLATES = [
    {
        "title": "Wildfire",
        "description": "Reach a learning streak",
        "icon": "local_fire_department",
    },
    {
        "title": "Scholar",
        "description": "Learn new words",
        "icon": "school",
    },
    {
        "title": "Champion",
        "description": "Finish first in a league",
        "icon": "trophy",
    },
    {
        "title": "Sharpshooter",
        "description": "Complete perfect lessons",
        "icon": "target",
    },
    {
        "title": "Quest Explorer",
        "description": "Complete daily quests",
        "icon": "task_alt",
    },
    {
        "title": "Early Riser",
        "description": "Practice in the morning",
        "icon": "wb_sunny",
    },
]


def generate_achievement(
    index: int,
) -> dict:

    template = random.choice(
        ACHIEVEMENT_TEMPLATES
    )

    total = random.choice(
        [
            10,
            20,
            30,
            50,
            100,
        ]
    )

    current = random.randint(
        0,
        total,
    )

    unlocked = (
        current >= total
    )

    return {
        "id":
            f"achievement_{index + 1}",

        "title":
            template["title"],

        "description":
            template["description"],

        "icon":
            template["icon"],

        "image":
            get_random_achievement(),

        "current":
            current,

        "total":
            total,

        "progress":
            min(
                1.0,
                current / total,
            ),

        "unlocked":
            unlocked,
    }


def generate_recent_activity(
    index: int,
) -> dict:

    return {
        "id":
            f"activity_{index + 1}",

        "title":
            random.choice(
                [
                    "Completed a lesson",
                    "Earned XP",
                    "Finished a quest",
                    "Extended streak",
                    "Moved up in the league",
                    "Completed a perfect lesson",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Spanish · Unit 6",
                    "French · Daily practice",
                    "Japanese · Section 2",
                    "Korean · Review",
                    "German · Beginner course",
                ]
            ),

        "icon":
            random.choice(
                [
                    "school",
                    "bolt",
                    "task_alt",
                    "local_fire_department",
                    "trophy",
                    "verified",
                ]
            ),

        "value":
            random.choice(
                [
                    "+10 XP",
                    "+15 XP",
                    "+20 XP",
                    "+30 XP",
                ]
            ),

        "time":
            random.choice(
                [
                    "5 min ago",
                    "18 min ago",
                    "1 hour ago",
                    "3 hours ago",
                    "Yesterday",
                ]
            ),
    }


def generate_profile_data() -> dict:

    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,

                "selected":
                    item["key"]
                    == "profile",
            }
        )

    achievement_count = random.randint(
        4,
        6,
    )

    activity_count = random.randint(
        5,
        9,
    )

    xp = random.randint(
        1500,
        75000,
    )

    current_level_xp = random.randint(
        20,
        90,
    )

    level_goal = 100

    return {
        "user": {
            "name":
                fake.name(),

            "username":
                "@"
                + fake.user_name(),

            "avatar":
                get_random_avatar(),

            "bio":
                random.choice(
                    [
                        "Learning a little every day.",
                        "Languages, coffee, and daily practice.",
                        "Trying to keep the streak alive!",
                        "Learning languages one lesson at a time.",
                    ]
                ),

            "joined":
                random.choice(
                    [
                        "Joined January 2025",
                        "Joined March 2024",
                        "Joined August 2026",
                        "Joined November 2023",
                    ]
                ),
        },

        "stats": {
            "streak":
                random.randint(
                    2,
                    500,
                ),

            "total_xp":
                xp,

            "league":
                random.choice(
                    [
                        "Gold",
                        "Sapphire",
                        "Ruby",
                        "Emerald",
                        "Diamond",
                    ]
                ),

            "top_finishes":
                random.randint(
                    0,
                    25,
                ),

            "followers":
                random.randint(
                    10,
                    2400,
                ),

            "following":
                random.randint(
                    5,
                    800,
                ),
        },

        "level": {
            "number":
                random.randint(
                    3,
                    50,
                ),

            "current":
                current_level_xp,

            "goal":
                level_goal,

            "progress":
                current_level_xp
                / level_goal,
        },

        "achievements": [
            generate_achievement(
                index
            )
            for index in range(
                achievement_count
            )
        ],

        "recent_activity": [
            generate_recent_activity(
                index
            )
            for index in range(
                activity_count
            )
        ],

        "navigation_items":
            navigation_items,
    }