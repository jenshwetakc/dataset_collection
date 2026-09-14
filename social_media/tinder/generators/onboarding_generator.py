from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

INTERESTS = [

    {
        "label": "Travel",
        "icon": "flight",
    },

    {
        "label": "Coffee",
        "icon": "local_cafe",
    },

    {
        "label": "Photography",
        "icon": "photo_camera",
    },

    {
        "label": "Music",
        "icon": "headphones",
    },

    {
        "label": "Movies",
        "icon": "movie",
    },

    {
        "label": "Gaming",
        "icon": "sports_esports",
    },

    {
        "label": "Fitness",
        "icon": "fitness_center",
    },

    {
        "label": "Hiking",
        "icon": "hiking",
    },

    {
        "label": "Cooking",
        "icon": "restaurant",
    },

    {
        "label": "Books",
        "icon": "menu_book",
    },

    {
        "label": "Dogs",
        "icon": "pets",
    },

    {
        "label": "Cats",
        "icon": "pets",
    },

    {
        "label": "Art",
        "icon": "palette",
    },

    {
        "label": "Dancing",
        "icon": "music_note",
    },

    {
        "label": "Yoga",
        "icon": "self_improvement",
    },

    {
        "label": "Running",
        "icon": "directions_run",
    },

    {
        "label": "Foodie",
        "icon": "lunch_dining",
    },

    {
        "label": "Camping",
        "icon": "camping",
    },

    {
        "label": "K-pop",
        "icon": "mic",
    },

    {
        "label": "Beach",
        "icon": "beach_access",
    },

]


RELATIONSHIP_GOALS = [

    {
        "title": "Long-term partner",
        "subtitle": "I'm looking for something serious.",
        "icon": "favorite",
    },

    {
        "title": "Long-term, open to short",
        "subtitle": "Serious is ideal, but I'm open-minded.",
        "icon": "favorite_border",
    },

    {
        "title": "Short-term fun",
        "subtitle": "Keeping things casual.",
        "icon": "celebration",
    },

    {
        "title": "New friends",
        "subtitle": "Meeting interesting people.",
        "icon": "group",
    },

    {
        "title": "Still figuring it out",
        "subtitle": "Seeing where things go.",
        "icon": "explore",
    },

]


# ==========================================================
# Interest
# ==========================================================

def generate_interest(
    item: dict,
    selected: bool,
) -> dict:

    return {

        "id":
            fake.uuid4(),

        "label":
            item["label"],

        "icon":
            item["icon"],

        "selected":
            selected,
    }


# ==========================================================
# Goal
# ==========================================================

def generate_goal(
    item: dict,
    selected: bool,
) -> dict:

    return {

        "id":
            fake.uuid4(),

        "title":
            item["title"],

        "subtitle":
            item["subtitle"],

        "icon":
            item["icon"],

        "selected":
            selected,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_onboarding_data() -> dict:

    selected_interest_labels = set(

        item["label"]

        for item in random.sample(
            INTERESTS,
            k=random.randint(
                4,
                6,
            ),
        )
    )

    selected_goal = random.choice(
        RELATIONSHIP_GOALS
    )

    current_step = random.choice([
        2,
        3,
        4,
    ])

    total_steps = 5

    return {

        "page_title":
            "Tell us about yourself",

        "current_step":
            current_step,

        "total_steps":
            total_steps,

        "progress_percent":
            int(
                current_step
                / total_steps
                * 100
            ),

        "headline":
            "What are you into?",

        "description":
            "Choose a few interests to help us personalize your recommendations.",

        "min_interests":
            3,

        "max_interests":
            5,

        "interests": [

            generate_interest(
                item,
                item["label"]
                in selected_interest_labels,
            )

            for item in INTERESTS
        ],

        "goals": [

            generate_goal(
                item,
                item["title"]
                == selected_goal["title"],
            )

            for item in RELATIONSHIP_GOALS
        ],

        "show_goal_section":
            random.random() < 0.72,

        "show_skip":
            random.random() < 0.55,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_onboarding_data()
    )