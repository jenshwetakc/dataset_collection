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

NAMES = [
    "Mina",
    "Sofia",
    "Emma",
    "Yuna",
    "Hana",
    "Olivia",
    "Ava",
    "Maya",
    "Nina",
    "Lena",
    "Ella",
    "Grace",
    "Aria",
    "Chloe",
]


LOCATIONS = [
    "2 km away",
    "3 km away",
    "5 km away",
    "7 km away",
    "9 km away",
    "12 km away",
    "15 km away",
]


PLAN_NAMES = [
    "1 month",
    "6 months",
    "12 months",
]


# ==========================================================
# Locked Profile
# ==========================================================

def generate_locked_profile() -> dict:

    return {

        "id":
            fake.uuid4(),

        "name":
            random.choice(
                NAMES
            ),

        "age":
            random.randint(
                20,
                37,
            ),

        "image":
            get_random_profile_image(),

        "distance":
            random.choice(
                LOCATIONS
            ),

        "verified":
            random.random() < 0.35,
    }


# ==========================================================
# Plan
# ==========================================================

def generate_plan(
    index: int,
) -> dict:

    months = [
        1,
        6,
        12,
    ][index]

    monthly_price = random.choice([
        8.99,
        9.99,
        10.99,
        12.99,
    ])

    if months == 6:

        monthly_price *= 0.72

    elif months == 12:

        monthly_price *= 0.58

    monthly_price = round(
        monthly_price,
        2,
    )

    total_price = round(
        monthly_price * months,
        2,
    )

    return {

        "months":
            months,

        "title":
            PLAN_NAMES[index],

        "monthly_price":
            monthly_price,

        "total_price":
            total_price,

        "recommended":
            months == 6,
    }


# ==========================================================
# Feature
# ==========================================================

def generate_features() -> list[dict]:

    return [

        {
            "icon": "favorite",
            "title": "See who likes you",
            "description":
                "Match instantly with people who already liked you.",
        },

        {
            "icon": "visibility",
            "title": "Priority Likes",
            "description":
                "Your likes are shown sooner to people you like.",
        },

        {
            "icon": "restart_alt",
            "title": "Unlimited Rewinds",
            "description":
                "Go back when you accidentally swipe left.",
        },

        {
            "icon": "location_on",
            "title": "Passport",
            "description":
                "Match with people in different cities.",
        },

        {
            "icon": "block",
            "title": "Control what you see",
            "description":
                "Get more privacy and discovery controls.",
        },
    ]


# ==========================================================
# Generator
# ==========================================================

def generate_likes_data() -> dict:

    profile_count = random.randint(
        8,
        14,
    )

    return {

        "title":
            "Likes You",

        "subtitle":
            "People who already liked your profile",

        "like_count":
            profile_count,

        "profiles": [

            generate_locked_profile()

            for _ in range(
                profile_count
            )
        ],

        "features":
            generate_features(),

        "plans": [

            generate_plan(index)

            for index in range(
                3
            )
        ],

        "navigation": [

            {
                "label": "Discover",
                "icon": "local_fire_department",
                "active": False,
                "semantic": "discover",
            },

            {
                "label": "Explore",
                "icon": "grid_view",
                "active": False,
                "semantic": "explore",
            },

            {
                "label": "Likes",
                "icon": "favorite",
                "active": True,
                "semantic": "likes",
            },

            {
                "label": "Messages",
                "icon": "chat_bubble",
                "active": False,
                "semantic": "messages",
            },

            {
                "label": "Profile",
                "icon": "person",
                "active": False,
                "semantic": "profile",
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_likes_data()
    )