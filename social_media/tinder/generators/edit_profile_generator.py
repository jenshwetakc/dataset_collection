from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_profile_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

INTERESTS = [
    "Travel",
    "Coffee",
    "Photography",
    "Hiking",
    "Running",
    "Music",
    "Movies",
    "Dogs",
    "Cats",
    "Gaming",
    "Cooking",
    "Fitness",
    "Books",
    "Art",
    "Foodie",
    "Camping",
]


JOBS = [
    "Software Engineer",
    "Product Designer",
    "Graduate Student",
    "UX Researcher",
    "Photographer",
    "Marketing Manager",
    "Data Analyst",
]


SCHOOLS = [
    "Korea University",
    "Yonsei University",
    "Seoul National University",
    "Hanyang University",
    "Hongik University",
]


RELATIONSHIP_GOALS = [
    "Long-term partner",
    "Long-term, open to short",
    "Short-term, open to long",
    "New friends",
    "Still figuring it out",
]


GENDER_OPTIONS = [
    "Woman",
    "Man",
    "Non-binary",
]


ORIENTATIONS = [
    "Straight",
    "Bisexual",
    "Gay",
    "Lesbian",
    "Queer",
]


BIO_TEXTS = [
    "Coffee, weekend adventures, and trying every restaurant in Seoul.",
    "Always planning the next trip. Looking for someone who enjoys spontaneous plans.",
    "Designer by day, cafe explorer by weekend.",
    "Hiking, movies, photography, and too many playlists.",
]


# ==========================================================
# Photo Slot
# ==========================================================

def generate_photo_slot(
    index: int,
) -> dict:

    filled = (
        index < 4
        or random.random() < 0.45
    )

    return {

        "index":
            index,

        "filled":
            filled,

        "image":
            (
                get_random_profile_image()
                if filled
                else None
            ),

        "primary":
            index == 0,

        "processing":
            (
                filled
                and random.random() < 0.08
            ),
    }


# ==========================================================
# Interest
# ==========================================================

def generate_interest(
    label: str,
    selected: bool,
) -> dict:

    return {
        "label": label,
        "selected": selected,
    }


# ==========================================================
# Setting Row
# ==========================================================

def generate_setting_row(
    icon: str,
    label: str,
    value: str,
) -> dict:

    return {
        "icon": icon,
        "label": label,
        "value": value,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_edit_profile_data() -> dict:

    selected_interests = set(
        random.sample(
            INTERESTS,
            k=random.randint(
                4,
                6,
            ),
        )
    )

    photo_slots = [

        generate_photo_slot(index)

        for index in range(
            9
        )
    ]

    completion = random.randint(
        62,
        94,
    )

    return {

        "page_title":
            "Edit Profile",

        "completion":
            completion,

        "photo_slots":
            photo_slots,

        "bio":
            random.choice(
                BIO_TEXTS
            ),

        "bio_limit":
            500,

        "job":
            random.choice(
                JOBS
            ),

        "school":
            random.choice(
                SCHOOLS
            ),

        "location":
            random.choice([
                "Seoul",
                "Gangnam",
                "Mapo",
                "Hongdae",
                "Seongsu",
            ]),

        "relationship_goal":
            random.choice(
                RELATIONSHIP_GOALS
            ),

        "gender":
            random.choice(
                GENDER_OPTIONS
            ),

        "orientation":
            random.choice(
                ORIENTATIONS
            ),

        "interests": [

            generate_interest(
                interest,
                interest in selected_interests,
            )

            for interest
            in INTERESTS
        ],

        "smart_photos":
            random.random() < 0.65,

        "show_distance":
            random.random() < 0.80,

        "show_age":
            random.random() < 0.90,

        "profile_control_rows": [

            generate_setting_row(
                "favorite",
                "Relationship goals",
                random.choice(
                    RELATIONSHIP_GOALS
                ),
            ),

            generate_setting_row(
                "person",
                "Gender",
                random.choice(
                    GENDER_OPTIONS
                ),
            ),

            generate_setting_row(
                "diversity_3",
                "Sexual orientation",
                random.choice(
                    ORIENTATIONS
                ),
            ),

            generate_setting_row(
                "language",
                "Languages",
                random.choice([
                    "English, Korean",
                    "English",
                    "Korean, English, Japanese",
                ]),
            ),
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_edit_profile_data()
    )