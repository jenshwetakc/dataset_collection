from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_avatar,
    get_random_profile_image,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

CHAT_STATES = [

    "normal",

    "typing",

    "sending",

    "send_failed",

    "blocked",

    "unmatched",

    "empty",

]


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
]


MESSAGES = [
    "Hey 👋",
    "How was your day?",
    "Coffee sounds good ☕",
    "Haha exactly 😄",
    "That place looks amazing!",
    "What are you doing this weekend?",
    "I love that too!",
    "Maybe Friday evening?",
    "Sounds like a plan!",
    "Where was that photo taken?",
    "I need recommendations now 😂",
    "I've been wanting to try that place.",
]


TIMES = [
    "10:12",
    "10:18",
    "10:31",
    "10:47",
    "11:03",
    "11:28",
    "11:42",
    "12:08",
]


# ==========================================================
# Partner
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
            random.random() < 0.55,

        "verified":
            random.random() < 0.35,
    }


# ==========================================================
# Message
# ==========================================================

def generate_message(
    index: int,
) -> dict:

    sender = random.choice([
        "me",
        "them",
    ])

    message_type = (
        "image"
        if random.random() < 0.12
        else "text"
    )

    return {

        "id":
            fake.uuid4(),

        "sender":
            sender,

        "type":
            message_type,

        "text":
            (
                random.choice(
                    MESSAGES
                )
                if message_type == "text"
                else None
            ),

        "image":
            (
                get_random_profile_image()
                if message_type == "image"
                else None
            ),

        "time":
            random.choice(
                TIMES
            ),

        "read":
            sender == "me"
            and random.random() < 0.80,

        "index":
            index,
    }


# ==========================================================
# Failed Message
# ==========================================================

def generate_failed_message() -> dict:

    return {

        "id":
            fake.uuid4(),

        "sender":
            "me",

        "type":
            "text",

        "text":
            random.choice([
                "Are you free later?",
                "Coffee this weekend?",
                "That sounds great!",
            ]),

        "time":
            "12:21",

        "read":
            False,
    }


# ==========================================================
# State Content
# ==========================================================

def generate_state_content(
    state: str,
    partner_name: str,
) -> dict:

    if state == "blocked":

        return {

            "icon":
                "block",

            "title":
                "You blocked this match",

            "description":
                f"You can no longer send messages to {partner_name}.",

            "primary_action":
                "Unblock",

            "secondary_action":
                "Delete conversation",
        }


    if state == "unmatched":

        return {

            "icon":
                "person_remove",

            "title":
                "This match is no longer available",

            "description":
                "The conversation has ended and messages can no longer be sent.",

            "primary_action":
                "Back to matches",

            "secondary_action":
                None,
        }


    if state == "empty":

        return {

            "icon":
                "waving_hand",

            "title":
                f"Say hi to {partner_name}",

            "description":
                "You matched! Start the conversation with a message.",

            "primary_action":
                None,

            "secondary_action":
                None,
        }


    return {}


# ==========================================================
# Generator
# ==========================================================

def generate_chat_states_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CHAT_STATES
        )


    if state not in CHAT_STATES:

        raise ValueError(
            f"Unsupported chat state: {state}"
        )


    partner = (
        generate_partner()
    )


    if state == "empty":

        messages = []

    else:

        messages = [

            generate_message(
                index
            )

            for index in range(
                random.randint(
                    8,
                    15,
                )
            )
        ]


    return {

        "state":
            state,

        "partner":
            partner,

        "messages":
            messages,

        "failed_message":
            (
                generate_failed_message()
                if state == "send_failed"
                else None
            ),

        "state_content":
            generate_state_content(
                state,
                partner["name"],
            ),

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

    for state in CHAT_STATES:

        print(
            "\n=================================="
        )

        print(
            state.upper()
        )

        print(
            "=================================="
        )

        pprint.pp(
            generate_chat_states_data(
                state
            )
        )