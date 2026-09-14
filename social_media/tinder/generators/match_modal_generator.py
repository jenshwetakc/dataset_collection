from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


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
]


OPENERS = [
    "Say something nice 👋",
    "Send a message",
    "Start with a compliment",
    "Ask about their profile",
]


SUGGESTIONS = [
    "Hey! Nice to match with you 😊",
    "That photo is amazing!",
    "Coffee sometime?",
    "How's your day going?",
]


def generate_match_modal_data() -> dict:

    partner_name = random.choice(
        NAMES
    )

    return {

        "page_title":
            "It's a Match",

        "partner_name":
            partner_name,

        "my_avatar":
            get_random_avatar(),

        "partner_avatar":
            get_random_avatar(),

        "headline":
            "It’s a Match!",

        "subheadline":
            f"You and {partner_name} liked each other.",

        "composer_placeholder":
            random.choice(
                OPENERS
            ),

        "suggestions":
            random.sample(
                SUGGESTIONS,
                k=3,
            ),

        "show_suggestions":
            random.random() < 0.72,

        "show_confetti":
            random.random() < 0.85,

        "show_super_like":
            random.random() < 0.18,

        "navigation": [

            {
                "label": "Discover",
                "icon": "local_fire_department",
                "active": True,
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


if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_match_modal_data()
    )