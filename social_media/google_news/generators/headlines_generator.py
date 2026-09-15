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
# Constants
# ==========================================================

HEADLINE_STATES = [
    "standard",
    "breaking",
    "live",
    "category_focus",
    "dense",
]


CATEGORIES = [
    "Latest",
    "World",
    "Business",
    "Technology",
    "Science",
    "Health",
    "Entertainment",
    "Sports",
]


PUBLISHERS = [
    "The Daily Report",
    "World Journal",
    "Morning News",
    "Global Desk",
    "City Times",
    "News Network",
    "The Observer",
    "Business Review",
    "Tech Chronicle",
    "Science Today",
    "National News",
    "Current Affairs",
]


NAVIGATION_ITEMS = [
    {
        "label": "For you",
        "icon": "home",
        "selected": False,
    },
    {
        "label": "Headlines",
        "icon": "article",
        "selected": True,
    },
    {
        "label": "Following",
        "icon": "star",
        "selected": False,
    },
    {
        "label": "Newsstand",
        "icon": "newspaper",
        "selected": False,
    },
]


CATEGORY_ICONS = {
    "Latest": "breaking_news",
    "World": "public",
    "Business": "business_center",
    "Technology": "memory",
    "Science": "science",
    "Health": "health_and_safety",
    "Entertainment": "movie",
    "Sports": "sports_soccer",
}


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "Just now",
            "5 min ago",
            "12 min ago",
            "28 min ago",
            "45 min ago",
            "1 hour ago",
            "2 hours ago",
            "3 hours ago",
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
    }


def generate_title(
    min_words: int = 7,
    max_words: int = 14,
) -> str:

    return fake.sentence(
        nb_words=random.randint(
            min_words,
            max_words,
        )
    )


# ==========================================================
# Story Generator
# ==========================================================

def generate_story(
    *,
    size: str = "standard",
    live: bool = False,
    breaking: bool = False,
) -> dict:

    return {
        "title":
            generate_title(),

        "summary":
            fake.text(
                max_nb_chars=random.randint(
                    100,
                    200,
                )
            ),

        "publisher":
            generate_publisher(),

        "timestamp":
            generate_timestamp(),

        "image":
            get_random_article_image(),

        "size":
            size,

        "live":
            live,

        "breaking":
            breaking,

        "saved":
            random.random() < 0.18,

        "full_coverage":
            random.random() < 0.30,
    }


# ==========================================================
# Category
# ==========================================================

def generate_category(
    name: str,
    *,
    story_count: int | None = None,
) -> dict:

    if story_count is None:
        story_count = random.randint(
            4,
            7,
        )

    return {
        "name":
            name,

        "icon":
            CATEGORY_ICONS.get(
                name,
                "article",
            ),

        "stories": [
            generate_story(
                size=(
                    "large"
                    if index == 0
                    else "standard"
                )
            )
            for index in range(
                story_count
            )
        ],
    }


# ==========================================================
# Live Timeline
# ==========================================================

def generate_live_updates() -> list[dict]:

    count = random.randint(
        4,
        8,
    )

    updates = []

    for index in range(
        count
    ):

        updates.append(
            {
                "time":
                    random.choice(
                        [
                            "11:42",
                            "11:35",
                            "11:18",
                            "10:56",
                            "10:31",
                            "10:05",
                            "09:48",
                        ]
                    ),

                "text":
                    fake.sentence(
                        nb_words=random.randint(
                            8,
                            15,
                        )
                    ),

                "latest":
                    index == 0,
            }
        )

    return updates


# ==========================================================
# Main Generator
# ==========================================================

def generate_headlines_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            HEADLINE_STATES
        )
    )

    if selected_state not in HEADLINE_STATES:

        raise ValueError(
            f"Unknown headlines state: {selected_state}"
        )


    selected_category = (
        random.choice(
            CATEGORIES[1:]
        )
        if selected_state
        == "category_focus"
        else "Latest"
    )


    # ======================================================
    # Category Set
    # ======================================================

    if selected_state == "category_focus":

        category_names = [
            selected_category,
        ]

    elif selected_state == "dense":

        category_names = random.sample(
            CATEGORIES,
            k=random.randint(
                5,
                len(CATEGORIES),
            ),
        )

    else:

        category_names = random.sample(
            CATEGORIES,
            k=random.randint(
                3,
                5,
            ),
        )


    categories = [
        generate_category(
            category_name,
            story_count=(
                random.randint(
                    6,
                    9,
                )
                if selected_state == "dense"
                else None
            ),
        )
        for category_name
        in category_names
    ]


    # ======================================================
    # Breaking State
    # ======================================================

    breaking_story = None

    if selected_state == "breaking":

        breaking_story = (
            generate_story(
                size="hero",
                breaking=True,
            )
        )


    # ======================================================
    # Live State
    # ======================================================

    live_story = None

    live_updates = []

    if selected_state == "live":

        live_story = (
            generate_story(
                size="hero",
                live=True,
            )
        )

        live_updates = (
            generate_live_updates()
        )


    # ======================================================
    # Data
    # ======================================================

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

        "categories":
            CATEGORIES,

        "selected_category":
            selected_category,

        "breaking_story":
            breaking_story,

        "live_story":
            live_story,

        "live_updates":
            live_updates,

        "sections":
            categories,

        "page_title":
            (
                selected_category
                if selected_state
                == "category_focus"
                else "Headlines"
            ),

        "page_subtitle":
            random.choice(
                [
                    "Top stories from around the world",
                    "Today's most important stories",
                    "Latest news and developing stories",
                    "Stories making headlines right now",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in HEADLINE_STATES:

        print(
            "\n"
            "================================"
        )

        print(
            state.upper()
        )

        print(
            "================================"
        )

        pprint(
            generate_headlines_data(
                state=state
            )
        )