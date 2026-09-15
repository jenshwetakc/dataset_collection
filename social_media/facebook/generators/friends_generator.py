# social_media/facebook/generators/friends_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_cover_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

FRIEND_STATES = [
    "default",
    "default",
    "friend_requests",
    "suggestions",
    "request_menu_open",
    "profile_preview",
    "search_active",
]


MUTUAL_FRIEND_COUNTS = [
    1,
    2,
    3,
    5,
    7,
    12,
    18,
    24,
]


LOCATION_NAMES = [
    "Seoul",
    "Busan",
    "Tokyo",
    "New York",
    "London",
    "Toronto",
    "Sydney",
]


# ==========================================================
# Person
# ==========================================================

def generate_person(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "cover":
            get_random_cover_image(),

        "mutual_friends":
            random.choice(
                MUTUAL_FRIEND_COUNTS
            ),

        "location":
            random.choice(
                LOCATION_NAMES
            ),

        "online":
            random.random() < 0.35,
    }


# ==========================================================
# Friend Requests
# ==========================================================

def generate_friend_requests(
    count: int = 8,
) -> list[dict]:

    requests = []

    for index in range(count):

        person = generate_person(
            index
        )

        person["request_time"] = (
            random.choice(
                [
                    "2h",
                    "5h",
                    "1d",
                    "2d",
                    "3d",
                    "1w",
                ]
            )
        )

        requests.append(
            person
        )

    return requests


# ==========================================================
# Suggestions
# ==========================================================

def generate_suggestions(
    count: int = 12,
) -> list[dict]:

    return [
        generate_person(index)
        for index in range(count)
    ]


# ==========================================================
# Existing Friends
# ==========================================================

def generate_existing_friends(
    count: int = 16,
) -> list[dict]:

    return [
        generate_person(index)
        for index in range(count)
    ]


# ==========================================================
# Navigation
# ==========================================================

def generate_friend_navigation() -> list[dict]:

    return [
        {
            "name": "Home",
            "icon": "people",
        },
        {
            "name": "Friend requests",
            "icon": "person_add",
        },
        {
            "name": "Suggestions",
            "icon": "person_search",
        },
        {
            "name": "All friends",
            "icon": "group",
        },
        {
            "name": "Birthdays",
            "icon": "cake",
        },
        {
            "name": "Custom lists",
            "icon": "list",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_friends_state(
    request_count: int,
    suggestion_count: int,
) -> dict:

    name = random.choice(
        FRIEND_STATES
    )

    selected_person = None

    if name == "request_menu_open":

        selected_person = random.randint(
            0,
            max(
                0,
                min(
                    request_count - 1,
                    4,
                )
            ),
        )

    elif name == "profile_preview":

        selected_person = random.randint(
            0,
            max(
                0,
                min(
                    suggestion_count - 1,
                    5,
                )
            ),
        )

    return {
        "name":
            name,

        "selected_person":
            selected_person,

        "search_text":
            (
                fake.first_name()
                if name == "search_active"
                else ""
            ),
    }


# ==========================================================
# Complete Data
# ==========================================================

def generate_friends_data() -> dict:

    requests = generate_friend_requests(
        count=random.randint(
            5,
            9,
        )
    )

    suggestions = generate_suggestions(
        count=random.randint(
            8,
            14,
        )
    )

    existing_friends = (
        generate_existing_friends(
            count=random.randint(
                12,
                20,
            )
        )
    )

    return {

        "navigation":
            generate_friend_navigation(),

        "requests":
            requests,

        "suggestions":
            suggestions,

        "friends":
            existing_friends,

        "state":
            generate_friends_state(
                request_count=len(
                    requests
                ),
                suggestion_count=len(
                    suggestions
                ),
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_friends_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK FRIENDS GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Requests:",
        len(
            data["requests"]
        ),
    )

    print(
        "Suggestions:",
        len(
            data["suggestions"]
        ),
    )

    print(
        "Existing friends:",
        len(
            data["friends"]
        ),
    )

    print(
        "State:",
        data["state"],
    )