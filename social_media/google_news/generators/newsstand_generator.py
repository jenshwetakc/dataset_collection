from __future__ import annotations

import random

from faker import Faker

from social_media.google_news.generators.media_generator import (
    get_random_article_image,
    get_random_avatar,
    get_random_publisher_logo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

NEWSSTAND_STATES = [
    "featured",
    "categories",
    "publisher_focus",
    "subscribed",
    "manage",
    "subscription_dialog",
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "For you",
        "icon": "home",
        "selected": False,
    },
    {
        "label": "Headlines",
        "icon": "article",
        "selected": False,
    },
    {
        "label": "Following",
        "icon": "star",
        "selected": False,
    },
    {
        "label": "Newsstand",
        "icon": "newspaper",
        "selected": True,
    },
]


# ==========================================================
# Content Pools
# ==========================================================

PUBLISHERS = [
    "Global News",
    "Morning Journal",
    "World Report",
    "The Observer",
    "Daily Chronicle",
    "Tech Daily",
    "Science Today",
    "Business Review",
    "City News",
    "National Desk",
    "Current Affairs",
    "Market Weekly",
    "Sports Network",
    "Culture Review",
]


CATEGORIES = [
    "General",
    "Business",
    "Technology",
    "Science",
    "Health",
    "Sports",
    "Culture",
    "World",
]


CATEGORY_ICONS = {
    "General": "newspaper",
    "Business": "business_center",
    "Technology": "memory",
    "Science": "science",
    "Health": "health_and_safety",
    "Sports": "sports_soccer",
    "Culture": "palette",
    "World": "public",
}


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "8 min ago",
            "21 min ago",
            "42 min ago",
            "1 hour ago",
            "2 hours ago",
            "4 hours ago",
            "Yesterday",
        ]
    )


def generate_publisher() -> dict:

    return {
        "name":
            random.choice(
                PUBLISHERS
            ),

        "logo":
            get_random_publisher_logo(),

        "category":
            random.choice(
                CATEGORIES
            ),

        "description":
            random.choice(
                [
                    "Independent news and analysis",
                    "Breaking stories and in-depth reporting",
                    "News, features and commentary",
                    "Daily reporting from around the world",
                    "Trusted journalism and analysis",
                ]
            ),

        "followers":
            random.randint(
                12,
                980,
            )
            * 1000,

        "following":
            random.random() < 0.35,

        "notifications":
            random.random() < 0.4,
    }


def generate_story() -> dict:

    return {
        "title":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    14,
                )
            ),

        "summary":
            fake.text(
                max_nb_chars=random.randint(
                    90,
                    170,
                )
            ),

        "image":
            get_random_article_image(),

        "timestamp":
            generate_timestamp(),

        "saved":
            random.random() < 0.18,
    }


# ==========================================================
# Publisher Collection
# ==========================================================

def generate_publishers(
    count: int,
) -> list[dict]:

    return [
        generate_publisher()
        for _ in range(
            count
        )
    ]


# ==========================================================
# Category
# ==========================================================

def generate_category(
    name: str,
) -> dict:

    return {
        "name":
            name,

        "icon":
            CATEGORY_ICONS.get(
                name,
                "newspaper",
            ),

        "publishers":
            generate_publishers(
                random.randint(
                    4,
                    7,
                )
            ),
    }


# ==========================================================
# Publisher Focus
# ==========================================================

def generate_publisher_focus() -> dict:

    publisher = (
        generate_publisher()
    )

    publisher["following"] = True

    return {
        "publisher":
            publisher,

        "hero_story":
            generate_story(),

        "stories": [
            generate_story()
            for _ in range(
                random.randint(
                    5,
                    8,
                )
            )
        ],
    }


# ==========================================================
# Dialog
# ==========================================================

def generate_dialog(
    publisher: dict,
) -> dict:

    return {
        "publisher":
            publisher,

        "title":
            (
                "Follow this source?"
                if not publisher["following"]
                else "Unfollow this source?"
            ),

        "message":
            (
                "Stories from this publisher can appear "
                "in your Following feed."
            ),
    }


# ==========================================================
# Main
# ==========================================================

def generate_newsstand_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            NEWSSTAND_STATES
        )
    )

    if selected_state not in NEWSSTAND_STATES:

        raise ValueError(
            f"Unknown Newsstand state: "
            f"{selected_state}"
        )


    featured_publishers = (
        generate_publishers(
            random.randint(
                6,
                10,
            )
        )
    )


    categories = [
        generate_category(
            name
        )
        for name in random.sample(
            CATEGORIES,
            k=random.randint(
                4,
                len(CATEGORIES),
            ),
        )
    ]


    subscribed_publishers = [
        publisher
        for publisher
        in generate_publishers(
            random.randint(
                5,
                9,
            )
        )
    ]

    for publisher in (
        subscribed_publishers
    ):

        publisher[
            "following"
        ] = True


    focus = None

    if selected_state == "publisher_focus":

        focus = (
            generate_publisher_focus()
        )


    dialog = None

    if selected_state == "subscription_dialog":

        target = random.choice(
            featured_publishers
        )

        dialog = (
            generate_dialog(
                target
            )
        )


    return {

        "state":
            selected_state,

        "brand": {
            "name":
                "Google News",
        },

        "user": {
            "name":
                fake.name(),

            "avatar":
                get_random_avatar(),
        },

        "navigation":
            NAVIGATION_ITEMS,

        "page_title":
            "Newsstand",

        "page_subtitle":
            random.choice(
                [
                    "Discover news sources and publishers",
                    "Browse publishers from around the world",
                    "Find sources for the topics you care about",
                ]
            ),

        "featured_publishers":
            featured_publishers,

        "categories":
            categories,

        "subscribed_publishers":
            subscribed_publishers,

        "focus":
            focus,

        "dialog":
            dialog,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in NEWSSTAND_STATES:

        print(
            "\n=============================="
        )

        print(
            state.upper()
        )

        print(
            "=============================="
        )

        pprint(
            generate_newsstand_data(
                state=state
            )
        )