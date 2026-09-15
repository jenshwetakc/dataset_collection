from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_course_image,
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


COURSES = [
    {
        "name": "Spanish",
        "icon": "translate",
    },
    {
        "name": "French",
        "icon": "language",
    },
    {
        "name": "German",
        "icon": "public",
    },
    {
        "name": "Japanese",
        "icon": "temple_buddhist",
    },
    {
        "name": "Korean",
        "icon": "language",
    },
    {
        "name": "Italian",
        "icon": "restaurant",
    },
    {
        "name": "Portuguese",
        "icon": "public",
    },
    {
        "name": "Chinese",
        "icon": "translate",
    },
    {
        "name": "Arabic",
        "icon": "language",
    },
    {
        "name": "Hindi",
        "icon": "translate",
    },
]


CATEGORY_TABS = [
    "Popular",
    "All",
    "European",
    "Asian",
]


def generate_course(
    index: int,
) -> dict:

    source = random.choice(
        COURSES
    )

    active = random.random() < 0.35

    progress = (
        random.randint(
            5,
            90,
        )
        if active
        else 0
    )

    learners = random.randint(
        100000,
        9000000,
    )

    return {
        "id":
            f"course_{index + 1}",

        "name":
            source["name"],

        "icon":
            source["icon"],

        "image":
            get_random_course_image(),

        "active":
            active,

        "progress":
            progress,

        "learners":
            learners,

        "level":
            (
                random.randint(
                    1,
                    25,
                )
                if active
                else None
            ),

        "featured":
            random.random() < 0.15,
    }


def generate_courses_data() -> dict:

    selected_tab = random.choice(
        CATEGORY_TABS
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

    course_count = random.randint(
        8,
        12,
    )

    courses = [
        generate_course(
            index
        )
        for index in range(
            course_count
        )
    ]

    return {
        "header": {
            "title":
                "Choose a course",

            "subtitle":
                random.choice(
                    [
                        "Pick a language and start learning.",
                        "Explore courses and continue your progress.",
                        "Choose what you want to learn next.",
                    ]
                ),
        },

        "search": {
            "placeholder":
                "Search languages",
        },

        "tabs": [
            {
                "label":
                    tab,

                "selected":
                    tab
                    == selected_tab,
            }
            for tab in CATEGORY_TABS
        ],

        "courses":
            courses,

        "current_courses":
            [
                course
                for course
                in courses
                if course["active"]
            ],

        "navigation_items":
            navigation_items,
    }