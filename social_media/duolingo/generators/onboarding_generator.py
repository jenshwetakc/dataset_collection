from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_character,
    get_random_illustration,
)


fake = Faker()


# ==========================================================
# Languages
# ==========================================================

LANGUAGES = [
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
]


# ==========================================================
# Motivation
# ==========================================================

MOTIVATIONS = [
    {
        "key": "travel",
        "title": "Travel",
        "description": "Communicate more confidently while traveling.",
        "icon": "flight",
    },
    {
        "key": "career",
        "title": "Career",
        "description": "Improve opportunities at work.",
        "icon": "work",
    },
    {
        "key": "culture",
        "title": "Culture",
        "description": "Connect with another culture.",
        "icon": "public",
    },
    {
        "key": "school",
        "title": "School",
        "description": "Study for classes and exams.",
        "icon": "school",
    },
    {
        "key": "family",
        "title": "Family and friends",
        "description": "Talk with people who matter to you.",
        "icon": "groups",
    },
    {
        "key": "fun",
        "title": "Just for fun",
        "description": "Learn something new for yourself.",
        "icon": "sentiment_satisfied",
    },
]


# ==========================================================
# Experience
# ==========================================================

EXPERIENCE_LEVELS = [
    {
        "key": "new",
        "title": "I'm new to the language",
        "description": "Start from the very beginning.",
        "icon": "looks_one",
    },
    {
        "key": "some",
        "title": "I know some common words",
        "description": "Start with basic phrases and grammar.",
        "icon": "looks_two",
    },
    {
        "key": "intermediate",
        "title": "I can have simple conversations",
        "description": "Skip the earliest lessons.",
        "icon": "looks_3",
    },
    {
        "key": "advanced",
        "title": "I'm comfortable with the language",
        "description": "Take a placement test.",
        "icon": "workspace_premium",
    },
]


# ==========================================================
# Daily Goal
# ==========================================================

DAILY_GOALS = [
    {
        "key": "casual",
        "title": "Casual",
        "minutes": 5,
        "description": "A quick daily habit.",
        "icon": "coffee",
    },
    {
        "key": "regular",
        "title": "Regular",
        "minutes": 10,
        "description": "A steady learning routine.",
        "icon": "schedule",
    },
    {
        "key": "serious",
        "title": "Serious",
        "minutes": 15,
        "description": "Make strong daily progress.",
        "icon": "local_fire_department",
    },
    {
        "key": "intense",
        "title": "Intense",
        "minutes": 20,
        "description": "Challenge yourself every day.",
        "icon": "bolt",
    },
]


# ==========================================================
# Step Builders
# ==========================================================

def build_language_step() -> dict:

    options = random.sample(
        LANGUAGES,
        k=random.randint(
            4,
            len(LANGUAGES),
        ),
    )

    selected_index = random.randrange(
        len(options)
    )

    return {
        "key":
            "language",

        "step_number":
            1,

        "title":
            "What would you like to learn?",

        "subtitle":
            "Choose a language to begin your learning journey.",

        "layout":
            "grid",

        "options": [
            {
                **option,

                "selected":
                    index
                    == selected_index,
            }
            for index, option
            in enumerate(options)
        ],
    }


def build_motivation_step() -> dict:

    options = random.sample(
        MOTIVATIONS,
        k=random.randint(
            4,
            6,
        ),
    )

    selected_index = random.randrange(
        len(options)
    )

    return {
        "key":
            "motivation",

        "step_number":
            2,

        "title":
            "Why are you learning?",

        "subtitle":
            "We'll personalize your lessons around your goals.",

        "layout":
            "list",

        "options": [
            {
                **option,

                "selected":
                    index
                    == selected_index,
            }
            for index, option
            in enumerate(options)
        ],
    }


def build_experience_step() -> dict:

    selected_index = random.randrange(
        len(EXPERIENCE_LEVELS)
    )

    return {
        "key":
            "experience",

        "step_number":
            3,

        "title":
            "How much do you already know?",

        "subtitle":
            "Choose the option that best describes your experience.",

        "layout":
            "list",

        "options": [
            {
                **option,

                "selected":
                    index
                    == selected_index,
            }
            for index, option
            in enumerate(
                EXPERIENCE_LEVELS
            )
        ],
    }


def build_daily_goal_step() -> dict:

    selected_index = random.randrange(
        len(DAILY_GOALS)
    )

    return {
        "key":
            "daily_goal",

        "step_number":
            4,

        "title":
            "Choose your daily goal",

        "subtitle":
            "You can change this anytime.",

        "layout":
            "goal",

        "options": [
            {
                **option,

                "selected":
                    index
                    == selected_index,
            }
            for index, option
            in enumerate(
                DAILY_GOALS
            )
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_onboarding_data() -> dict:

    builders = [
        build_language_step,
        build_motivation_step,
        build_experience_step,
        build_daily_goal_step,
    ]

    builder = random.choice(
        builders
    )

    current_step = builder()

    total_steps = 4

    return {
        "total_steps":
            total_steps,

        "current_step":
            current_step,

        "progress":
            current_step[
                "step_number"
            ]
            / total_steps,

        "character":
            get_random_character(),

        "illustration":
            get_random_illustration(),

        "continue_label":
            (
                "START LEARNING"
                if current_step[
                    "step_number"
                ]
                == total_steps
                else "CONTINUE"
            ),

        "secondary_label":
            (
                "TAKE PLACEMENT TEST"
                if current_step[
                    "key"
                ]
                == "experience"
                else None
            ),
    }