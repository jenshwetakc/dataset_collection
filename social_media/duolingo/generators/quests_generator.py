from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Navigation
# ==========================================================

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
# Daily Quest Templates
# ==========================================================

DAILY_QUEST_TEMPLATES = [
    {
        "title": "Earn {goal} XP",
        "icon": "bolt",
        "goals": [10, 15, 20, 30, 40],
    },
    {
        "title": "Complete {goal} lessons",
        "icon": "school",
        "goals": [2, 3, 4, 5],
    },
    {
        "title": "Get {goal} perfect lessons",
        "icon": "verified",
        "goals": [1, 2, 3],
    },
    {
        "title": "Practice for {goal} minutes",
        "icon": "schedule",
        "goals": [5, 10, 15, 20],
    },
    {
        "title": "Complete {goal} speaking exercises",
        "icon": "mic",
        "goals": [2, 3, 5],
    },
    {
        "title": "Score 80% or higher {goal} times",
        "icon": "workspace_premium",
        "goals": [2, 3, 4],
    },
]


# ==========================================================
# Daily Quest
# ==========================================================

def generate_daily_quest(
    index: int,
) -> dict:

    template = random.choice(
        DAILY_QUEST_TEMPLATES
    )

    goal = random.choice(
        template["goals"]
    )

    current = random.randint(
        0,
        goal,
    )

    completed = (
        current >= goal
    )

    reward = random.choice(
        [
            5,
            10,
            15,
            20,
        ]
    )

    return {
        "id":
            f"daily_quest_{index + 1}",

        "title":
            template["title"].format(
                goal=goal
            ),

        "icon":
            template["icon"],

        "current":
            current,

        "goal":
            goal,

        "progress":
            min(
                1.0,
                current / goal,
            ),

        "completed":
            completed,

        "reward":
            reward,

        "claimable":
            (
                completed
                and random.random() < 0.55
            ),
    }


# ==========================================================
# Monthly Milestones
# ==========================================================

def generate_monthly_milestones(
    current_points: int,
    total_points: int,
) -> list[dict]:

    thresholds = [
        10,
        20,
        30,
        40,
        total_points,
    ]

    icons = [
        "redeem",
        "diamond",
        "inventory_2",
        "workspace_premium",
        "trophy",
    ]

    milestones = []

    for index, threshold in enumerate(
        thresholds
    ):

        milestones.append(
            {
                "threshold":
                    threshold,

                "icon":
                    icons[index],

                "reached":
                    current_points
                    >= threshold,
            }
        )

    return milestones


# ==========================================================
# Friend Quest
# ==========================================================

def generate_friend_quest() -> dict:

    goal = random.choice(
        [
            20,
            30,
            40,
            50,
        ]
    )

    current = random.randint(
        4,
        goal,
    )

    partner_name = fake.first_name()

    return {
        "partner": {
            "name":
                partner_name,

            "avatar":
                get_random_avatar(),
        },

        "user_avatar":
            get_random_avatar(),

        "title":
            random.choice(
                [
                    "Complete lessons together",
                    "Earn XP together",
                    "Finish perfect lessons",
                    "Complete learning sessions",
                ]
            ),

        "current":
            current,

        "goal":
            goal,

        "progress":
            min(
                1.0,
                current / goal,
            ),

        "days_left":
            random.randint(
                1,
                5,
            ),

        "reward":
            random.choice(
                [
                    "30 min XP boost",
                    "100 gems",
                    "Quest chest",
                    "Double XP boost",
                ]
            ),
    }


# ==========================================================
# Generate Quests Screen
# ==========================================================

def generate_quests_data() -> dict:

    daily_quests = [
        generate_daily_quest(
            index
        )
        for index in range(
            3
        )
    ]

    monthly_goal = random.choice(
        [
            40,
            50,
            60,
        ]
    )

    monthly_current = random.randint(
        5,
        monthly_goal,
    )

    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,

                "selected":
                    item["key"]
                    == "quests",
            }
        )

    return {
        "daily": {
            "title":
                "Daily Quests",

            "subtitle":
                random.choice(
                    [
                        "Complete quests to earn rewards.",
                        "Finish today's goals before time runs out.",
                        "Keep learning to collect rewards.",
                    ]
                ),

            "hours_left":
                random.randint(
                    1,
                    23,
                ),

            "minutes_left":
                random.randint(
                    0,
                    59,
                ),

            "quests":
                daily_quests,
        },

        "monthly": {
            "title":
                random.choice(
                    [
                        "September Challenge",
                        "Monthly Challenge",
                        "Learning Challenge",
                    ]
                ),

            "current":
                monthly_current,

            "goal":
                monthly_goal,

            "progress":
                monthly_current
                / monthly_goal,

            "milestones":
                generate_monthly_milestones(
                    monthly_current,
                    monthly_goal,
                ),
        },

        "friend_quest":
            generate_friend_quest(),

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

        "navigation_items":
            navigation_items,
    }