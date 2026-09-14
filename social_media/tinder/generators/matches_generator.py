from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_avatar,
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


MESSAGES = [
    "Hey 👋",
    "How was your day?",
    "You have to show me that cafe 😄",
    "Haha I agree!",
    "What are you doing this weekend?",
    "That sounds fun!",
    "Coffee sometime?",
    "I love that place too.",
    "Nice meeting you 😊",
    "Where was that photo taken?",
]


TIMES = [
    "Now",
    "2m",
    "6m",
    "14m",
    "32m",
    "1h",
    "3h",
    "Yesterday",
    "Mon",
]


# ==========================================================
# Match Item
# ==========================================================

def generate_match() -> dict:

    return {

        "id":
            fake.uuid4(),

        "name":
            random.choice(
                NAMES
            ),

        "avatar":
            get_random_avatar(),

        "message":
            random.choice(
                MESSAGES
            ),

        "time":
            random.choice(
                TIMES
            ),

        "unread":
            random.random() < 0.38,

        "online":
            random.random() < 0.35,

        "verified":
            random.random() < 0.25,
    }


# ==========================================================
# New Match
# ==========================================================

def generate_new_match() -> dict:

    return {

        "id":
            fake.uuid4(),

        "name":
            random.choice(
                NAMES
            ),

        "avatar":
            get_random_avatar(),

        "new":
            random.random() < 0.7,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_matches_data() -> dict:

    return {

        "page_title":
            "Matches",

        "search_placeholder":
            "Search matches",

        "new_matches": [

            generate_new_match()

            for _ in range(
                random.randint(
                    5,
                    9,
                )
            )
        ],

        "matches": [

            generate_match()

            for _ in range(
                random.randint(
                    10,
                    18,
                )
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
                "active": False,
                "semantic": "likes",
            },

            {
                "label": "Messages",
                "icon": "chat_bubble",
                "active": True,
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
        generate_matches_data()
    )