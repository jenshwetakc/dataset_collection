# social_media/facebook/generators/search_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_cover_image,
    get_random_post_image,
    get_random_product_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

SEARCH_STATES = [
    "default",
    "default",
    "people_results",
    "posts_results",
    "groups_results",
    "marketplace_results",
    "recent_searches",
    "search_filters_open",
    "result_menu_open",
    "profile_preview",
]


SEARCH_TABS = [
    "All",
    "Posts",
    "People",
    "Photos",
    "Videos",
    "Marketplace",
    "Pages",
    "Places",
    "Groups",
]


QUERY_OPTIONS = [
    "photography",
    "travel",
    "coffee",
    "design",
    "fitness",
    "technology",
    "books",
    "gaming",
]


POST_TEXTS = [
    "Sharing some recent moments from this week.",
    "A beautiful place worth visiting.",
    "Trying something new today.",
    "A few photos from the weekend.",
    "One of my favorite experiences recently.",
]


GROUP_NAMES = [
    "Photography Community",
    "Travel Lovers",
    "Coffee Enthusiasts",
    "Creative Designers",
    "Fitness Community",
    "Tech Discussion Group",
]


PRODUCT_NAMES = [
    "Wireless Headphones",
    "Camera",
    "Office Chair",
    "Desk Lamp",
    "Gaming Monitor",
    "Smart Watch",
]


# ==========================================================
# People
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
            random.randint(
                0,
                34,
            ),

        "location":
            fake.city(),

        "following":
            random.random() < 0.3,
    }


def generate_people(
    count: int = 8,
) -> list[dict]:

    return [
        generate_person(index)
        for index in range(count)
    ]


# ==========================================================
# Posts
# ==========================================================

def generate_post(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "author":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "text":
            random.choice(
                POST_TEXTS
            ),

        "image":
            (
                get_random_post_image()
                if random.random() < 0.7
                else None
            ),

        "timestamp":
            random.choice(
                [
                    "10 min",
                    "1 h",
                    "3 h",
                    "Yesterday",
                    "2 days ago",
                ]
            ),

        "reactions":
            random.randint(
                5,
                2400,
            ),

        "comments":
            random.randint(
                0,
                350,
            ),
    }


def generate_posts(
    count: int = 7,
) -> list[dict]:

    return [
        generate_post(index)
        for index in range(count)
    ]


# ==========================================================
# Groups
# ==========================================================

def generate_group(
    index: int,
) -> dict:

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
            random.randint(
                100,
                850000,
            ),

        "privacy":
            random.choice(
                [
                    "Public group",
                    "Private group",
                ]
            ),
    }


def generate_groups(
    count: int = 6,
) -> list[dict]:

    return [
        generate_group(index)
        for index in range(count)
    ]


# ==========================================================
# Marketplace
# ==========================================================

def generate_marketplace_item(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "title":
            random.choice(
                PRODUCT_NAMES
            ),

        "image":
            get_random_product_image(),

        "price":
            random.randint(
                20,
                1200,
            ),

        "location":
            fake.city(),
    }


def generate_marketplace_items(
    count: int = 8,
) -> list[dict]:

    return [
        generate_marketplace_item(index)
        for index in range(count)
    ]


# ==========================================================
# Recent Searches
# ==========================================================

def generate_recent_searches() -> list[dict]:

    searches = []

    for index in range(
        random.randint(
            5,
            8,
        )
    ):

        searches.append(
            {
                "id":
                    index,

                "query":
                    random.choice(
                        QUERY_OPTIONS
                    ),

                "icon":
                    random.choice(
                        [
                            "history",
                            "search",
                            "person",
                            "groups",
                        ]
                    ),
            }
        )

    return searches


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> dict:

    return {
        "date":
            random.choice(
                [
                    "Any date",
                    "Today",
                    "This week",
                    "This month",
                ]
            ),

        "source":
            random.choice(
                [
                    "Anyone",
                    "Friends",
                    "Groups",
                    "Pages",
                ]
            ),

        "location":
            random.choice(
                [
                    "Anywhere",
                    "Nearby",
                    fake.city(),
                ]
            ),
    }


# ==========================================================
# State
# ==========================================================

def generate_search_state(
    people_count: int,
    post_count: int,
) -> dict:

    name = random.choice(
        SEARCH_STATES
    )

    selected_result = None

    if name == "result_menu_open":

        selected_result = random.randint(
            0,
            max(
                0,
                min(
                    post_count - 1,
                    3,
                )
            ),
        )

    elif name == "profile_preview":

        selected_result = random.randint(
            0,
            max(
                0,
                min(
                    people_count - 1,
                    4,
                )
            ),
        )

    query = random.choice(
        QUERY_OPTIONS
    )

    return {
        "name":
            name,

        "selected_result":
            selected_result,

        "query":
            query,
    }


# ==========================================================
# Complete Search Data
# ==========================================================

def generate_search_data() -> dict:

    people = generate_people(
        count=random.randint(
            6,
            10,
        )
    )

    posts = generate_posts(
        count=random.randint(
            5,
            8,
        )
    )

    groups = generate_groups(
        count=random.randint(
            5,
            8,
        )
    )

    marketplace = generate_marketplace_items(
        count=random.randint(
            6,
            10,
        )
    )

    return {
        "tabs":
            SEARCH_TABS,

        "people":
            people,

        "posts":
            posts,

        "groups":
            groups,

        "marketplace":
            marketplace,

        "recent_searches":
            generate_recent_searches(),

        "filters":
            generate_filters(),

        "state":
            generate_search_state(
                people_count=len(
                    people
                ),
                post_count=len(
                    posts
                ),
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_search_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK SEARCH GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Query:",
        data["state"]["query"],
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "People:",
        len(
            data["people"]
        ),
    )

    print(
        "Posts:",
        len(
            data["posts"]
        ),
    )

    print(
        "Groups:",
        len(
            data["groups"]
        ),
    )

    print(
        "Marketplace:",
        len(
            data["marketplace"]
        ),
    )