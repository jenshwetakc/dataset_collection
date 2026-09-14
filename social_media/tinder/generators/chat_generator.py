from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_avatar,
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
]


TEXT_MESSAGES = [
    "Hey 👋",
    "How's your day going?",
    "Haha that sounds fun 😄",
    "I love that place too!",
    "We should definitely go sometime.",
    "What are you doing this weekend?",
    "Coffee sounds perfect ☕",
    "That photo is amazing!",
    "I've never been there before.",
    "You're making me hungry 😂",
    "I usually go there on weekends.",
    "That sounds like a good plan.",
    "Same! I was thinking exactly that.",
    "Okay, now I need recommendations.",
    "Maybe Friday evening?",
    "Deal 😄",
]


TIMES = [
    "10:21",
    "10:24",
    "10:27",
    "10:35",
    "10:41",
    "10:48",
    "11:03",
    "11:17",
    "11:32",
    "11:45",
    "12:04",
    "12:19",
]


REACTIONS = [
    "favorite",
    "sentiment_satisfied",
    "thumb_up",
]


# ==========================================================
# Chat Partner
# ==========================================================

def generate_partner() -> dict:

    return {

        "id":
            fake.uuid4(),

        "name":
            random.choice(
                NAMES
            ),

        "avatar":
            get_random_avatar(),

        "online":
            random.random() < 0.5,

        "verified":
            random.random() < 0.35,

        "distance_km":
            random.randint(
                1,
                15,
            ),
    }


# ==========================================================
# Text Message
# ==========================================================

def generate_text_message(
    sender: str,
    index: int,
) -> dict:

    reacted = (
        random.random()
        < 0.18
    )

    return {

        "id":
            fake.uuid4(),

        "type":
            "text",

        "sender":
            sender,

        "text":
            random.choice(
                TEXT_MESSAGES
            ),

        "time":
            random.choice(
                TIMES
            ),

        "read":
            sender == "me"
            and random.random() < 0.82,

        "reaction":
            (
                random.choice(
                    REACTIONS
                )
                if reacted
                else None
            ),

        "sequence":
            index,
    }


# ==========================================================
# Image Message
# ==========================================================

def generate_image_message(
    sender: str,
    index: int,
) -> dict:

    return {

        "id":
            fake.uuid4(),

        "type":
            "image",

        "sender":
            sender,

        "src":
            get_random_profile_image(),

        "time":
            random.choice(
                TIMES
            ),

        "read":
            sender == "me",

        "reaction":
            (
                "favorite"
                if random.random() < 0.25
                else None
            ),

        "sequence":
            index,
    }


# ==========================================================
# Messages
# ==========================================================

def generate_messages() -> list[dict]:

    count = random.randint(
        14,
        24,
    )

    messages = []

    sender = random.choice([
        "me",
        "them",
    ])

    for index in range(count):

        # Keep short conversational runs.
        if (
            index > 0
            and random.random() < 0.38
        ):
            sender = (
                "them"
                if sender == "me"
                else "me"
            )

        if random.random() < 0.12:

            message = (
                generate_image_message(
                    sender,
                    index,
                )
            )

        else:

            message = (
                generate_text_message(
                    sender,
                    index,
                )
            )

        messages.append(
            message
        )

    return messages


# ==========================================================
# Sidebar Match
# ==========================================================

def generate_sidebar_match() -> dict:

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
                TEXT_MESSAGES
            ),

        "time":
            random.choice([
                "Now",
                "4m",
                "18m",
                "1h",
                "4h",
                "Yesterday",
            ]),

        "unread":
            random.random() < 0.3,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_chat_data() -> dict:

    partner = (
        generate_partner()
    )

    return {

        "partner":
            partner,

        "messages":
            generate_messages(),

        "sidebar_matches": [

            generate_sidebar_match()

            for _ in range(
                random.randint(
                    7,
                    12,
                )
            )
        ],

        "composer_placeholder":
            "Type a message",

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
        generate_chat_data()
    )