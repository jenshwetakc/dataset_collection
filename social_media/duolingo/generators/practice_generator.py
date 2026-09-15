from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_illustration,
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


PRACTICE_TYPES = [
    {
        "key": "mistakes",
        "title": "Review mistakes",
        "description": "Practice questions you recently missed.",
        "icon": "error_outline",
    },
    {
        "key": "listening",
        "title": "Listening practice",
        "description": "Train your listening comprehension.",
        "icon": "headphones",
    },
    {
        "key": "speaking",
        "title": "Speaking practice",
        "description": "Practice pronunciation and speaking.",
        "icon": "mic",
    },
    {
        "key": "words",
        "title": "Words",
        "description": "Review vocabulary you've learned.",
        "icon": "translate",
    },
]


WEAK_SKILLS = [
    "Food and drinks",
    "Daily routines",
    "Family",
    "Travel",
    "School",
    "Shopping",
    "Directions",
    "Weather",
    "Hobbies",
    "Introductions",
]


def generate_practice_type(
    index: int,
) -> dict:

    item = PRACTICE_TYPES[index]

    return {
        **item,

        "count":
            random.randint(
                3,
                28,
            ),

        "enabled":
            random.random()
            > 0.08,

        "image":
            get_random_illustration(),
    }


def generate_weak_skill(
    index: int,
) -> dict:

    score = random.randint(
        20,
        85,
    )

    return {
        "id":
            f"weak_skill_{index + 1}",

        "name":
            random.choice(
                WEAK_SKILLS
            ),

        "score":
            score,

        "progress":
            score / 100,

        "lessons":
            random.randint(
                1,
                6,
            ),

        "icon":
            random.choice(
                [
                    "restaurant",
                    "flight",
                    "home",
                    "school",
                    "directions_walk",
                    "shopping_bag",
                    "cloud",
                    "sports_esports",
                ]
            ),
    }


def generate_history_item(
    index: int,
) -> dict:

    return {
        "id":
            f"history_{index + 1}",

        "title":
            random.choice(
                [
                    "Mistake review",
                    "Listening session",
                    "Speaking practice",
                    "Vocabulary review",
                    "Personalized practice",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Spanish",
                    "French",
                    "Japanese",
                    "Korean",
                    "German",
                ]
            ),

        "xp":
            random.choice(
                [
                    10,
                    15,
                    20,
                    25,
                ]
            ),

        "accuracy":
            random.randint(
                65,
                100,
            ),

        "time":
            random.choice(
                [
                    "10 min ago",
                    "32 min ago",
                    "1 hour ago",
                    "Yesterday",
                    "2 days ago",
                ]
            ),

        "icon":
            random.choice(
                [
                    "fitness_center",
                    "headphones",
                    "mic",
                    "translate",
                    "school",
                ]
            ),
    }


def generate_practice_data() -> dict:

    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,
                "selected":
                    item["key"]
                    == "practice",
            }
        )

    weak_skill_count = random.randint(
        3,
        5,
    )

    history_count = random.randint(
        4,
        7,
    )

    return {
        "header": {
            "title":
                "Practice",

            "subtitle":
                random.choice(
                    [
                        "Strengthen your skills with personalized review.",
                        "Review what you've learned and keep improving.",
                        "Practice your weakest skills and build confidence.",
                    ]
                ),
        },

        "stats": {
            "streak":
                random.randint(
                    1,
                    365,
                ),

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

        "practice_types": [
            generate_practice_type(
                index
            )
            for index in range(
                len(
                    PRACTICE_TYPES
                )
            )
        ],

        "daily_review": {
            "title":
                "Personalized Practice",

            "description":
                random.choice(
                    [
                        "A review session based on your recent lessons.",
                        "Practice skills selected just for you.",
                        "Review weak areas and recent mistakes.",
                    ]
                ),

            "minutes":
                random.choice(
                    [
                        5,
                        10,
                        15,
                    ]
                ),

            "xp":
                random.choice(
                    [
                        10,
                        20,
                        30,
                    ]
                ),

            "image":
                get_random_illustration(),
        },

        "weak_skills": [
            generate_weak_skill(
                index
            )
            for index in range(
                weak_skill_count
            )
        ],

        "history": [
            generate_history_item(
                index
            )
            for index in range(
                history_count
            )
        ],

        "navigation_items":
            navigation_items,
    }