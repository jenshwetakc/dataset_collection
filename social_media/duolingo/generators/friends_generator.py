from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_avatar,
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


TABS = [
    "Friends",
    "Followers",
    "Following",
]


ACTIVITY_TYPES = [
    {
        "icon": "local_fire_department",
        "text": "extended their streak",
    },
    {
        "icon": "trophy",
        "text": "moved up in the leaderboard",
    },
    {
        "icon": "task_alt",
        "text": "completed a quest",
    },
    {
        "icon": "bolt",
        "text": "earned XP",
    },
    {
        "icon": "workspace_premium",
        "text": "unlocked an achievement",
    },
]


def generate_person(
    index: int,
) -> dict:

    followers = random.randint(
        10,
        5000,
    )

    xp = random.randint(
        500,
        100000,
    )

    return {
        "id":
            f"person_{index + 1}",

        "name":
            fake.name(),

        "username":
            "@"
            + fake.user_name(),

        "avatar":
            get_random_avatar(),

        "xp":
            xp,

        "followers":
            followers,

        "streak":
            random.randint(
                1,
                600,
            ),

        "mutual":
            random.randint(
                0,
                12,
            ),

        "following":
            random.random()
            < 0.35,
    }


def generate_request(
    index: int,
) -> dict:

    person = generate_person(
        index
    )

    return {
        **person,

        "request_id":
            f"request_{index + 1}",

        "mutual":
            random.randint(
                1,
                15,
            ),
    }


def generate_activity(
    index: int,
) -> dict:

    activity_type = random.choice(
        ACTIVITY_TYPES
    )

    return {
        "id":
            f"activity_{index + 1}",

        "name":
            fake.first_name(),

        "avatar":
            get_random_avatar(),

        "icon":
            activity_type["icon"],

        "text":
            activity_type["text"],

        "value":
            random.choice(
                [
                    "+10 XP",
                    "+20 XP",
                    "+50 XP",
                    "7 days",
                    "30 days",
                    "Diamond",
                ]
            ),

        "time":
            random.choice(
                [
                    "5m",
                    "18m",
                    "1h",
                    "3h",
                    "Yesterday",
                ]
            ),
    }


def generate_friends_data() -> dict:

    selected_tab = random.choice(
        TABS
    )

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

    return {
        "header": {
            "title":
                "Friends",

            "subtitle":
                random.choice(
                    [
                        "Learn together and stay motivated.",
                        "Follow learners and celebrate progress.",
                        "Find friends and keep each other motivated.",
                    ]
                ),
        },

        "search": {
            "placeholder":
                "Search friends",
        },

        "tabs": [
            {
                "label":
                    tab,

                "selected":
                    tab
                    == selected_tab,
            }
            for tab in TABS
        ],

        "requests": [
            generate_request(
                index
            )
            for index in range(
                random.randint(
                    2,
                    4,
                )
            )
        ],

        "suggestions": [
            generate_person(
                index + 20
            )
            for index in range(
                random.randint(
                    4,
                    7,
                )
            )
        ],

        "activity": [
            generate_activity(
                index
            )
            for index in range(
                random.randint(
                    5,
                    8,
                )
            )
        ],

        "stats": {
            "followers":
                random.randint(
                    20,
                    2500,
                ),

            "following":
                random.randint(
                    10,
                    1200,
                ),

            "friends":
                random.randint(
                    5,
                    300,
                ),
        },

        "navigation_items":
            navigation_items,
    }