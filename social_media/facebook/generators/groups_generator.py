# social_media/facebook/generators/groups_generator.py

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

GROUP_STATES = [
    "default",
    "default",
    "discover",
    "joined_groups",
    "group_preview",
    "create_group",
    "invite_people",
    "group_menu_open",
    "search_active",
]


GROUP_CATEGORIES = [
    {
        "name": "Gaming",
        "icon": "sports_esports",
    },
    {
        "name": "Travel",
        "icon": "flight",
    },
    {
        "name": "Food",
        "icon": "restaurant",
    },
    {
        "name": "Photography",
        "icon": "photo_camera",
    },
    {
        "name": "Fitness",
        "icon": "fitness_center",
    },
    {
        "name": "Technology",
        "icon": "devices",
    },
    {
        "name": "Books",
        "icon": "menu_book",
    },
    {
        "name": "Art",
        "icon": "palette",
    },
]


GROUP_NAMES = [
    "Photography Lovers",
    "Weekend Travelers",
    "Home Cooking Club",
    "Tech Enthusiasts",
    "Daily Fitness",
    "Book Lovers",
    "Creative Designers",
    "Gaming Community",
    "Coffee Lovers",
    "Nature Explorers",
    "Startup Founders",
    "Language Exchange",
    "Cycling Community",
    "Pet Owners Club",
]


PRIVACY_TYPES = [
    "Public group",
    "Private group",
]


POST_FREQUENCIES = [
    "10+ posts a day",
    "5 posts a day",
    "3 posts a day",
    "Active today",
    "Very active",
]


# ==========================================================
# Group
# ==========================================================

def generate_group(
    index: int,
) -> dict:

    member_count = random.randint(
        120,
        980000,
    )

    return {
        "id":
            index,

        "name":
            random.choice(
                GROUP_NAMES
            ),

        "cover":
            get_random_cover_image(),

        "members":
            member_count,

        "privacy":
            random.choice(
                PRIVACY_TYPES
            ),

        "activity":
            random.choice(
                POST_FREQUENCIES
            ),

        "joined":
            random.random() < 0.35,

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "friends_in_group":
            random.randint(
                0,
                18,
            ),
    }


# ==========================================================
# Groups
# ==========================================================

def generate_groups(
    count: int = 14,
) -> list[dict]:

    return [
        generate_group(index)
        for index in range(count)
    ]


# ==========================================================
# Invitable People
# ==========================================================

def generate_invitable_person(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "selected":
            random.random() < 0.25,
    }


def generate_invitable_people(
    count: int = 8,
) -> list[dict]:

    return [
        generate_invitable_person(index)
        for index in range(count)
    ]


# ==========================================================
# Navigation
# ==========================================================

def generate_group_navigation() -> list[dict]:

    return [
        {
            "name": "Your feed",
            "icon": "home",
        },
        {
            "name": "Discover",
            "icon": "explore",
        },
        {
            "name": "Your groups",
            "icon": "groups",
        },
        {
            "name": "Create new group",
            "icon": "add_circle",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_groups_state(
    group_count: int,
) -> dict:

    name = random.choice(
        GROUP_STATES
    )

    selected_group = None

    if name in {
        "group_preview",
        "invite_people",
        "group_menu_open",
    }:

        selected_group = random.randint(
            0,
            max(
                0,
                min(
                    group_count - 1,
                    7,
                )
            ),
        )

    selected_category = None

    if name == "discover":

        selected_category = random.choice(
            GROUP_CATEGORIES
        )["name"]

    search_text = ""

    if name == "search_active":

        search_text = random.choice(
            [
                "travel",
                "fitness",
                "photography",
                "gaming",
                "books",
            ]
        )

    return {
        "name":
            name,

        "selected_group":
            selected_group,

        "selected_category":
            selected_category,

        "search_text":
            search_text,
    }


# ==========================================================
# Create Group Draft
# ==========================================================

def generate_create_group_data() -> dict:

    return {
        "name":
            "",

        "privacy":
            random.choice(
                [
                    "Public",
                    "Private",
                ]
            ),

        "invite_count":
            random.randint(
                0,
                5,
            ),
    }


# ==========================================================
# Complete Groups Data
# ==========================================================

def generate_groups_data() -> dict:

    groups = generate_groups(
        count=random.randint(
            12,
            18,
        )
    )

    joined_groups = [
        group
        for group in groups
        if group["joined"]
    ]

    if not joined_groups:

        groups[0]["joined"] = True

        joined_groups = [
            groups[0]
        ]

    return {
        "navigation":
            generate_group_navigation(),

        "categories":
            GROUP_CATEGORIES,

        "groups":
            groups,

        "joined_groups":
            joined_groups,

        "invite_people":
            generate_invitable_people(
                count=random.randint(
                    6,
                    10,
                )
            ),

        "create_group":
            generate_create_group_data(),

        "state":
            generate_groups_state(
                group_count=len(
                    groups
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_groups_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK GROUPS GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Groups:",
        len(
            data["groups"]
        ),
    )

    print(
        "Joined groups:",
        len(
            data["joined_groups"]
        ),
    )

    print(
        "Invite people:",
        len(
            data["invite_people"]
        ),
    )

    print(
        "State:",
        data["state"],
    )