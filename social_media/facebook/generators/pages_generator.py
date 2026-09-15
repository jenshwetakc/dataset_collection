from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_cover_image,
    get_random_post_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

PAGE_STATES = [
    "default",
    "default",
    "managed_pages",
    "discover",
    "page_preview",
    "create_page",
    "page_switcher",
    "page_menu_open",
    "search_active",
]


PAGE_CATEGORIES = [
    {
        "name": "Business",
        "icon": "business_center",
    },
    {
        "name": "Community",
        "icon": "groups",
    },
    {
        "name": "Creator",
        "icon": "movie",
    },
    {
        "name": "Shopping",
        "icon": "shopping_bag",
    },
    {
        "name": "Education",
        "icon": "school",
    },
    {
        "name": "Entertainment",
        "icon": "theaters",
    },
]


PAGE_NAMES = [
    "Daily Design",
    "Coffee & Stories",
    "Urban Photography",
    "Travel Notes",
    "Creative Studio",
    "Tech Today",
    "Healthy Living",
    "Local Food Guide",
    "Modern Workspace",
    "Book Corner",
]


# ==========================================================
# Page
# ==========================================================

def generate_page(
    index: int,
    managed: bool = False,
) -> dict:

    return {
        "id":
            index,

        "name":
            random.choice(
                PAGE_NAMES
            ),

        "avatar":
            get_random_avatar(),

        "cover":
            get_random_cover_image(),

        "category":
            random.choice(
                PAGE_CATEGORIES
            )["name"],

        "followers":
            random.randint(
                120,
                980000,
            ),

        "likes":
            random.randint(
                80,
                750000,
            ),

        "managed":
            managed,

        "verified":
            random.random() < 0.25,

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "location":
            fake.city(),

        "following":
            random.random() < 0.3,
    }


# ==========================================================
# Collections
# ==========================================================

def generate_managed_pages(
    count: int = 4,
) -> list[dict]:

    return [
        generate_page(
            index=index,
            managed=True,
        )
        for index in range(
            count
        )
    ]


def generate_discovered_pages(
    count: int = 10,
) -> list[dict]:

    return [
        generate_page(
            index=index,
            managed=False,
        )
        for index in range(
            count
        )
    ]


# ==========================================================
# Recent Content
# ==========================================================

def generate_recent_content(
    count: int = 6,
) -> list[dict]:

    content = []

    for index in range(
        count
    ):

        content.append(
            {
                "id":
                    index,

                "image":
                    get_random_post_image(),

                "caption":
                    fake.sentence(
                        nb_words=random.randint(
                            6,
                            14,
                        )
                    ),
            }
        )

    return content


# ==========================================================
# Navigation
# ==========================================================

def generate_page_navigation() -> list[dict]:

    return [
        {
            "name": "Home",
            "icon": "home",
        },
        {
            "name": "Your Pages",
            "icon": "flag",
        },
        {
            "name": "Discover",
            "icon": "explore",
        },
        {
            "name": "Invites",
            "icon": "mail",
        },
        {
            "name": "Create",
            "icon": "add_circle",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_pages_state(
    managed_count: int,
    discovered_count: int,
) -> dict:

    name = random.choice(
        PAGE_STATES
    )

    selected_page = None

    if name in {
        "page_preview",
        "page_menu_open",
    }:

        selected_page = random.randint(
            0,
            max(
                0,
                min(
                    discovered_count - 1,
                    6,
                )
            ),
        )

    elif name == "page_switcher":

        selected_page = random.randint(
            0,
            max(
                0,
                managed_count - 1,
            ),
        )

    search_text = ""

    if name == "search_active":

        search_text = random.choice(
            [
                "design",
                "coffee",
                "travel",
                "books",
                "technology",
            ]
        )

    return {
        "name":
            name,

        "selected_page":
            selected_page,

        "search_text":
            search_text,
    }


# ==========================================================
# Create Page Draft
# ==========================================================

def generate_create_page_data() -> dict:

    return {
        "name":
            "",

        "category":
            random.choice(
                PAGE_CATEGORIES
            )["name"],

        "bio":
            "",
    }


# ==========================================================
# Complete Data
# ==========================================================

def generate_pages_data() -> dict:

    managed_pages = (
        generate_managed_pages(
            count=random.randint(
                3,
                5,
            )
        )
    )

    discovered_pages = (
        generate_discovered_pages(
            count=random.randint(
                8,
                12,
            )
        )
    )

    return {
        "navigation":
            generate_page_navigation(),

        "categories":
            PAGE_CATEGORIES,

        "managed_pages":
            managed_pages,

        "discovered_pages":
            discovered_pages,

        "recent_content":
            generate_recent_content(
                count=6
            ),

        "create_page":
            generate_create_page_data(),

        "state":
            generate_pages_state(
                managed_count=len(
                    managed_pages
                ),
                discovered_count=len(
                    discovered_pages
                ),
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_pages_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK PAGES GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Managed pages:",
        len(
            data["managed_pages"]
        ),
    )

    print(
        "Discovered pages:",
        len(
            data["discovered_pages"]
        ),
    )

    print(
        "State:",
        data["state"],
    )