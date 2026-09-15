from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_avatar,
    get_random_character,
    get_random_reward,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

COURSES = [
    "Spanish",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Portuguese",
    "Chinese",
]

UNITS = [
    "Introduce yourself",
    "Talk about daily routines",
    "Order food and drinks",
    "Describe your family",
    "Ask for directions",
    "Talk about travel",
    "Discuss hobbies",
    "Describe your home",
    "Talk about school",
    "Make plans with friends",
]

LESSON_ICONS = [
    "star",
    "book_2",
    "chat_bubble",
    "headphones",
    "bolt",
    "restaurant",
    "home",
    "directions_walk",
    "flight",
    "school",
]

NAVIGATION_ITEMS = [
    {
        "label": "Learn",
        "icon": "home",
        "key": "learn",
    },
    {
        "label": "Practice",
        "icon": "fitness_center",
        "key": "practice",
    },
    {
        "label": "Leaderboards",
        "icon": "trophy",
        "key": "leaderboard",
    },
    {
        "label": "Quests",
        "icon": "task_alt",
        "key": "quests",
    },
    {
        "label": "Shop",
        "icon": "storefront",
        "key": "shop",
    },
    {
        "label": "Profile",
        "icon": "person",
        "key": "profile",
    },
]


# ==========================================================
# Lesson Node
# ==========================================================

def generate_lesson_node(
    index: int,
    completed_until: int,
) -> dict:

    if index < completed_until:

        state = "completed"

    elif index == completed_until:

        state = "current"

    else:

        state = "locked"

    return {
        "id":
            f"lesson_{index + 1}",

        "title":
            random.choice(
                [
                    "Lesson",
                    "Practice",
                    "Story",
                    "Review",
                    "Challenge",
                ]
            ),

        "icon":
            random.choice(
                LESSON_ICONS
            ),

        "state":
            state,

        "xp":
            random.choice(
                [
                    10,
                    15,
                    20,
                    25,
                ]
            ),

        "offset":
            random.choice(
                [
                    "left",
                    "center",
                    "right",
                    "center",
                ]
            ),
    }


# ==========================================================
# Quest
# ==========================================================

def generate_quest(
    index: int,
) -> dict:

    goal = random.choice(
        [
            3,
            5,
            10,
            15,
            20,
        ]
    )

    current = random.randint(
        0,
        goal
    )

    return {
        "title":
            random.choice(
                [
                    "Earn XP",
                    "Complete lessons",
                    "Get perfect lessons",
                    "Practice for 10 minutes",
                    "Score 80% or higher",
                    "Finish speaking exercises",
                ]
            ),

        "current":
            current,

        "goal":
            goal,

        "progress":
            round(
                current / goal,
                2,
            ),

        "reward":
            random.choice(
                [
                    5,
                    10,
                    15,
                    20,
                ]
            ),

        "image":
            get_random_reward(),
    }


# ==========================================================
# Generate Home Data
# ==========================================================

def generate_home_data() -> dict:

    course = random.choice(
        COURSES
    )

    unit_number = random.randint(
        1,
        25,
    )

    lesson_count = random.randint(
        8,
        14,
    )

    completed_until = random.randint(
        1,
        max(
            1,
            lesson_count - 2,
        )
    )

    lessons = [

        generate_lesson_node(
            index,
            completed_until,
        )

        for index
        in range(
            lesson_count
        )
    ]

    quests = [

        generate_quest(
            index
        )

        for index
        in range(
            random.randint(
                2,
                3,
            )
        )
    ]

    selected_nav = "learn"

    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,
                "selected":
                    item["key"]
                    == selected_nav,
            }
        )

    streak = random.randint(
        1,
        365,
    )

    gems = random.randint(
        80,
        5000,
    )

    hearts = random.randint(
        1,
        5,
    )

    daily_goal = random.choice(
        [
            10,
            20,
            30,
            50,
        ]
    )

    daily_xp = random.randint(
        0,
        daily_goal
    )

    return {

        # --------------------------------------------------
        # User
        # --------------------------------------------------

        "user": {

            "name":
                fake.first_name(),

            "avatar":
                get_random_avatar(),

            "level":
                random.randint(
                    2,
                    45,
                ),
        },


        # --------------------------------------------------
        # Course
        # --------------------------------------------------

        "course": {

            "name":
                course,

            "flag":
                random.choice(
                    [
                        "language",
                        "translate",
                        "public",
                    ]
                ),
        },


        # --------------------------------------------------
        # Stats
        # --------------------------------------------------

        "stats": {

            "streak":
                streak,

            "gems":
                gems,

            "hearts":
                hearts,
        },


        # --------------------------------------------------
        # Unit
        # --------------------------------------------------

        "unit": {

            "number":
                unit_number,

            "title":
                random.choice(
                    UNITS
                ),

            "subtitle":
                random.choice(
                    [
                        "Learn useful phrases",
                        "Build your vocabulary",
                        "Practice everyday conversations",
                        "Improve your communication skills",
                        "Master the basics",
                    ]
                ),
        },


        # --------------------------------------------------
        # Lessons
        # --------------------------------------------------

        "lessons":
            lessons,


        # --------------------------------------------------
        # Daily Goal
        # --------------------------------------------------

        "daily_goal": {

            "current":
                daily_xp,

            "goal":
                daily_goal,

            "progress":
                min(
                    1.0,
                    daily_xp
                    / daily_goal,
                ),
        },


        # --------------------------------------------------
        # Quests
        # --------------------------------------------------

        "quests":
            quests,


        # --------------------------------------------------
        # Character
        # --------------------------------------------------

        "character":

            get_random_character(),


        # --------------------------------------------------
        # Navigation
        # --------------------------------------------------

        "navigation_items":
            navigation_items,


        # --------------------------------------------------
        # Promo
        # --------------------------------------------------

        "promo": {

            "title":
                random.choice(
                    [
                        "Keep your streak alive!",
                        "Practice makes progress",
                        "You're doing great!",
                        "Ready for another lesson?",
                    ]
                ),

            "message":
                random.choice(
                    [
                        "Complete a lesson today to stay on track.",
                        "A few minutes of practice can make a difference.",
                        "Reach your daily XP goal and earn a reward.",
                    ]
                ),
        },
    }