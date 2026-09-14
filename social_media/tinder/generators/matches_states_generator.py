from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

MATCHES_STATES = [

    "normal",

    "loading",

    "empty",

    "search_results",

    "no_results",

    "new_match",

]


# ==========================================================
# Helpers
# ==========================================================

def generate_message_time() -> str:

    now = datetime.now()

    delta = timedelta(
        minutes=random.randint(
            0,
            60 * 24 * 5,
        )
    )

    message_time = (
        now - delta
    )

    if message_time.date() == now.date():

        return message_time.strftime(
            "%H:%M"
        )

    if (
        now.date()
        - message_time.date()
    ).days == 1:

        return "Yesterday"

    return message_time.strftime(
        "%a"
    )


def generate_message_text() -> str:

    return fake.sentence(
        nb_words=random.randint(
            3,
            9,
        )
    )


# ==========================================================
# Match
# ==========================================================

def generate_match() -> dict:

    return {

        "id":
            fake.uuid4(),

        "name":
            fake.first_name(),

        "avatar":
            get_random_avatar(),

        "message":
            generate_message_text(),

        "time":
            generate_message_time(),

        "unread":
            random.random() < 0.30,

        "unread_count":
            random.randint(
                1,
                5,
            ),

        "online":
            random.random() < 0.45,

        "verified":
            random.random() < 0.35,
    }


# ==========================================================
# New Match
# ==========================================================

def generate_new_match() -> dict:

    return {

        "id":
            fake.uuid4(),

        "name":
            fake.first_name(),

        "avatar":
            get_random_avatar(),

        "new":
            True,
    }


# ==========================================================
# State Content
# ==========================================================

def generate_state_content(
    state: str,
) -> dict:

    if state == "empty":

        return {

            "icon":
                "favorite_border",

            "title":
                "No matches yet",

            "description":
                "Keep swiping and your new matches will show up here.",

            "primary_action":
                "Start swiping",
        }


    if state == "no_results":

        return {

            "icon":
                "search_off",

            "title":
                "No conversations found",

            "description":
                "Try searching for a different name.",

            "primary_action":
                "Clear search",
        }


    if state == "new_match":

        return {

            "icon":
                "favorite",

            "title":
                "You have a new match!",

            "description":
                "Start a conversation and say hello.",

            "primary_action":
                "Send a message",
        }


    return {}


# ==========================================================
# Generator
# ==========================================================

def generate_matches_states_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            MATCHES_STATES
        )


    if state not in MATCHES_STATES:

        raise ValueError(
            f"Unsupported matches state: {state}"
        )


    search_query = (
        fake.first_name()
        if state in [
            "search_results",
            "no_results",
        ]
        else ""
    )


    if state == "empty":

        matches = []

        new_matches = []


    elif state == "loading":

        matches = []

        new_matches = []


    elif state == "search_results":

        matches = [

            generate_match()

            for _ in range(
                random.randint(
                    2,
                    5,
                )
            )
        ]

        new_matches = []


    elif state == "no_results":

        matches = []

        new_matches = []


    else:

        matches = [

            generate_match()

            for _ in range(
                random.randint(
                    8,
                    16,
                )
            )
        ]

        new_matches = [

            generate_new_match()

            for _ in range(
                random.randint(
                    4,
                    8,
                )
            )
        ]


    featured_new_match = (
        generate_new_match()
        if state == "new_match"
        else None
    )


    return {

        "state":
            state,

        "page_title":
            "Matches",

        "search_query":
            search_query,

        "search_placeholder":
            "Search matches",

        "matches":
            matches,

        "new_matches":
            new_matches,

        "featured_new_match":
            featured_new_match,

        "state_content":
            generate_state_content(
                state
            ),

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

    for state in MATCHES_STATES:

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
            generate_matches_states_data(
                state
            )
        )