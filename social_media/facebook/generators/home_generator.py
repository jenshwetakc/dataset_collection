# social_media/facebook/generators/home_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_post_image,
    get_random_profile_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

REACTION_ICONS = [
    "thumb_up",
    "favorite",
    "sentiment_very_satisfied",
]

POST_PRIVACY = [
    "public",
    "group",
    "lock",
]

SHORTCUT_ICONS = [
    "group",
    "bookmark",
    "schedule",
    "storefront",
    "ondemand_video",
    "event",
    "sports_esports",
]

SHORTCUT_NAMES = [
    "Friends",
    "Saved",
    "Memories",
    "Marketplace",
    "Video",
    "Events",
    "Gaming",
]

POST_TEXTS = [
    "Beautiful weather today. Hope everyone is having a wonderful day!",
    "A few moments from this week.",
    "Sometimes the simplest days become the best memories.",
    "Exploring somewhere new today.",
    "Coffee, good company, and a relaxing afternoon.",
    "Weekend adventures.",
    "Sharing a few photos from today.",
    "What a great way to start the day.",
    "Another productive day finished.",
    "One of my favorite moments recently.",
]

TIMESTAMPS = [
    "Just now",
    "5 min",
    "12 min",
    "25 min",
    "1 h",
    "2 h",
    "3 h",
    "Yesterday",
]


# ==========================================================
# User
# ==========================================================

def generate_current_user() -> dict:

    return {
        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Story
# ==========================================================

def generate_story(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.first_name(),

        "avatar":
            get_random_avatar(),

        "image":
            (
                get_random_post_image()
                or get_random_profile_image()
            ),

        "seen":
            random.random() < 0.3,
    }


def generate_stories(
    count: int = 6,
) -> list[dict]:

    return [
        generate_story(index)
        for index in range(count)
    ]


# ==========================================================
# Post
# ==========================================================

def generate_post(
    index: int,
) -> dict:

    has_image = (
        random.random()
        < 0.82
    )

    reaction_count = random.randint(
        4,
        6500,
    )

    comment_count = random.randint(
        0,
        850,
    )

    share_count = random.randint(
        0,
        320,
    )

    return {
        "id":
            index,

        "author":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "timestamp":
            random.choice(
                TIMESTAMPS
            ),

        "privacy_icon":
            random.choice(
                POST_PRIVACY
            ),

        "text":
            random.choice(
                POST_TEXTS
            ),

        "has_image":
            has_image,

        "image":
            (
                get_random_post_image()
                if has_image
                else None
            ),

        "reaction_icons":
            random.sample(
                REACTION_ICONS,
                k=random.randint(
                    1,
                    min(
                        3,
                        len(
                            REACTION_ICONS
                        ),
                    ),
                ),
            ),

        "reaction_count":
            reaction_count,

        "comment_count":
            comment_count,

        "share_count":
            share_count,
    }


def generate_posts(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            5,
            9,
        )

    return [
        generate_post(index)
        for index in range(count)
    ]


# ==========================================================
# Sidebar Shortcut
# ==========================================================

def generate_shortcuts() -> list[dict]:

    shortcuts = []

    for (
        name,
        icon,
    ) in zip(
        SHORTCUT_NAMES,
        SHORTCUT_ICONS,
    ):

        shortcuts.append(
            {
                "name":
                    name,

                "icon":
                    icon,
            }
        )

    return shortcuts


# ==========================================================
# Contacts
# ==========================================================

def generate_contact(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "online":
            random.random()
            < 0.72,
    }


def generate_contacts(
    count: int = 9,
) -> list[dict]:

    return [
        generate_contact(index)
        for index in range(count)
    ]


# ==========================================================
# Sponsored
# ==========================================================

def generate_sponsored() -> list[dict]:

    count = random.randint(
        1,
        2,
    )

    sponsored = []

    for index in range(count):

        sponsored.append(
            {
                "id":
                    index,

                "title":
                    fake.catch_phrase(),

                "domain":
                    fake.domain_name(),

                "image":
                    get_random_post_image(),
            }
        )

    return sponsored


# ==========================================================
# Home States
# ==========================================================

HOME_STATES = [
    "default",
    "default",
    "default",
    "post_menu_open",
]


def generate_home_state() -> dict:

    state = random.choice(
        HOME_STATES
    )

    selected_post = None

    if state == "post_menu_open":

        selected_post = random.randint(
            0,
            2,
        )

    return {
        "name":
            state,

        "selected_post":
            selected_post,
    }


# ==========================================================
# Complete Home Data
# ==========================================================

def generate_home_data() -> dict:

    user = generate_current_user()

    return {

        "current_user":
            user,

        "stories":
            generate_stories(
                count=random.randint(
                    5,
                    8,
                )
            ),

        "posts":
            generate_posts(),

        "shortcuts":
            generate_shortcuts(),

        "contacts":
            generate_contacts(
                count=random.randint(
                    7,
                    12,
                )
            ),

        "sponsored":
            generate_sponsored(),

        "state":
            generate_home_state(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_home_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK HOME GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "\nCurrent user:",
        data["current_user"]["name"],
    )

    print(
        "Stories:",
        len(
            data["stories"]
        ),
    )

    print(
        "Posts:",
        len(
            data["posts"]
        ),
    )

    print(
        "Shortcuts:",
        len(
            data["shortcuts"]
        ),
    )

    print(
        "Contacts:",
        len(
            data["contacts"]
        ),
    )

    print(
        "Sponsored:",
        len(
            data["sponsored"]
        ),
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "\n"
        "=========================================="
    )