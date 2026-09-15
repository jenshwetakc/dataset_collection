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

FOLLOWING_STATES = [
    "normal",
    "empty",
    "topic_focus",
    "manage",
    "source_grid",
    "unfollow_dialog",
]


# ==========================================================
# Constants
# ==========================================================

TOPICS = [
    "Artificial Intelligence",
    "Technology",
    "World",
    "Business",
    "Science",
    "Health",
    "Climate",
    "Space",
    "Entertainment",
    "Sports",
    "Travel",
    "Design",
]


PUBLISHERS = [
    "Global News",
    "Morning Journal",
    "Daily Chronicle",
    "The Observer",
    "World Report",
    "Tech Today",
    "Science Weekly",
    "Business Review",
    "City News",
    "Current Affairs",
    "National Desk",
    "The Daily Post",
]


TOPIC_ICONS = [
    "memory",
    "public",
    "business_center",
    "science",
    "health_and_safety",
    "eco",
    "rocket_launch",
    "movie",
    "sports_soccer",
    "flight",
    "palette",
    "language",
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
        "selected": False,
    },
    {
        "label": "Following",
        "icon": "star",
        "selected": True,
    },
    {
        "label": "Newsstand",
        "icon": "newspaper",
        "selected": False,
    },
]


# ==========================================================
# Basic Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "6 min ago",
            "14 min ago",
            "31 min ago",
            "48 min ago",
            "1 hour ago",
            "2 hours ago",
            "4 hours ago",
            "Yesterday",
        ]
    )


def generate_publisher() -> dict:

    name = random.choice(
        PUBLISHERS
    )

    return {
        "name":
            name,

        "logo":
            get_random_publisher_logo(),

        "description":
            random.choice(
                [
                    "Breaking news and analysis",
                    "Independent journalism",
                    "Latest stories and reports",
                    "News, features and analysis",
                    "Reporting from around the world",
                ]
            ),

        "followers":
            random.randint(
                10,
                950,
            )
            * 1000,
    }


# ==========================================================
# Story
# ==========================================================

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
                    100,
                    190,
                )
            ),

        "publisher":
            generate_publisher(),

        "image":
            get_random_article_image(),

        "timestamp":
            generate_timestamp(),

        "saved":
            random.random() < 0.20,

        "full_coverage":
            random.random() < 0.25,
    }


# ==========================================================
# Topic
# ==========================================================

def generate_topic(
    name: str | None = None,
    index: int = 0,
) -> dict:

    if name is None:

        name = random.choice(
            TOPICS
        )

    return {
        "id":
            index,

        "name":
            name,

        "icon":
            TOPIC_ICONS[
                index
                % len(
                    TOPIC_ICONS
                )
            ],

        "following":
            True,

        "notification":
            random.random() < 0.45,

        "story_count":
            random.randint(
                30,
                600,
            ),
    }


# ==========================================================
# Sources
# ==========================================================

def generate_sources(
    count: int,
) -> list[dict]:

    return [
        {
            **generate_publisher(),

            "following":
                True,

            "notification":
                random.random()
                < 0.35,
        }
        for _ in range(
            count
        )
    ]


# ==========================================================
# Focus Topic
# ==========================================================

def generate_focus_topic() -> dict:

    selected_topic = random.choice(
        TOPICS
    )

    return {
        "topic":
            generate_topic(
                selected_topic
            ),

        "description":
            random.choice(
                [
                    f"Latest coverage about {selected_topic}",
                    f"Stories and updates from {selected_topic}",
                    f"News selected from sources covering {selected_topic}",
                ]
            ),

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

def generate_unfollow_dialog(
    topics: list[dict],
    sources: list[dict],
) -> dict:

    use_topic = (
        random.random()
        < 0.50
    )

    if use_topic and topics:

        target = random.choice(
            topics
        )

        return {
            "type":
                "topic",

            "name":
                target["name"],

            "title":
                "Unfollow topic?",

            "message":
                (
                    "Stories from this topic will "
                    "no longer appear in Following."
                ),
        }

    target = random.choice(
        sources
    )

    return {
        "type":
            "source",

        "name":
            target["name"],

        "title":
            "Unfollow source?",

        "message":
            (
                "You can follow this source again "
                "at any time."
            ),
    }


# ==========================================================
# Main
# ==========================================================

def generate_following_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            FOLLOWING_STATES
        )
    )

    if selected_state not in FOLLOWING_STATES:

        raise ValueError(
            f"Unknown Following state: "
            f"{selected_state}"
        )


    # ======================================================
    # Empty State
    # ======================================================

    if selected_state == "empty":

        topics = []

        sources = []

        stories = []

    else:

        topic_count = random.randint(
            4,
            8,
        )

        selected_topics = random.sample(
            TOPICS,
            k=min(
                topic_count,
                len(TOPICS),
            ),
        )

        topics = [
            generate_topic(
                name=name,
                index=index,
            )
            for index, name
            in enumerate(
                selected_topics
            )
        ]

        sources = generate_sources(
            random.randint(
                4,
                9,
            )
        )

        stories = [
            generate_story()
            for _ in range(
                random.randint(
                    5,
                    9,
                )
            )
        ]


    # ======================================================
    # Topic Focus
    # ======================================================

    focus = None

    if selected_state == "topic_focus":

        focus = (
            generate_focus_topic()
        )


    # ======================================================
    # Dialog
    # ======================================================

    dialog = None

    if selected_state == "unfollow_dialog":

        dialog = (
            generate_unfollow_dialog(
                topics,
                sources,
            )
        )


    # ======================================================
    # Result
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

        "page_title":
            "Following",

        "page_subtitle":
            random.choice(
                [
                    "Stories from topics and sources you follow",
                    "Your personalized collection of news",
                    "News from your favorite topics and publishers",
                ]
            ),

        "topics":
            topics,

        "sources":
            sources,

        "stories":
            stories,

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

    for state in FOLLOWING_STATES:

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
            generate_following_data(
                state=state
            )
        )