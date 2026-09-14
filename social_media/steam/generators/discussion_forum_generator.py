from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_avatar,
    get_random_game_cover,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

FORUM_CATEGORIES = [
    "General Discussions",
    "Help & Tips",
    "Bug Reports",
    "Trading",
    "Looking for Group",
    "Guides & Strategies",
]


THREAD_TAGS = [
    "Discussion",
    "Question",
    "Guide",
    "Bug",
    "Suggestion",
    "Trading",
]


THREAD_STATES = [
    "normal",
    "normal",
    "normal",
    "pinned",
    "locked",
]


# ==========================================================
# Title
# ==========================================================

def generate_thread_title() -> str:

    patterns = [
        lambda: fake.sentence(
            nb_words=random.randint(
                4,
                8,
            )
        ).rstrip("."),

        lambda: (
            "How do I "
            + fake.sentence(
                nb_words=random.randint(
                    3,
                    6,
                )
            ).rstrip("?")
            + "?"
        ),

        lambda: (
            "Anyone else having issues with "
            + fake.word().title()
            + "?"
        ),

        lambda: (
            fake.word().title()
            + " update discussion"
        ),

        lambda: (
            "Best strategy for "
            + fake.word().title()
        ),
    ]

    return random.choice(
        patterns
    )()


# ==========================================================
# Thread
# ==========================================================

def generate_thread() -> dict:

    state = random.choice(
        THREAD_STATES
    )

    replies = random.randint(
        0,
        850,
    )

    views = max(
        replies,
        random.randint(
            20,
            50000,
        ),
    )

    return {

        "title":
            generate_thread_title(),

        "tag":
            random.choice(
                THREAD_TAGS
            ),

        "state":
            state,

        "pinned":
            state == "pinned",

        "locked":
            state == "locked",

        "author": {
            "name":
                fake.user_name(),

            "avatar":
                get_random_avatar(),
        },

        "replies":
            replies,

        "views":
            views,

        "last_reply_author":
            fake.user_name(),

        "timestamp":
            random.choice([
                "Just now",
                "3 minutes ago",
                "18 minutes ago",
                "1 hour ago",
                "Today",
                "Yesterday",
                "3 days ago",
            ]),

        "unread":
            random.random() < 0.28,
    }


# ==========================================================
# Moderator
# ==========================================================

def generate_moderator() -> dict:

    return {

        "name":
            fake.user_name(),

        "avatar":
            get_random_avatar(),

        "role":
            random.choice([
                "Moderator",
                "Developer",
                "Community Manager",
            ]),

        "online":
            random.random() < 0.65,
    }


# ==========================================================
# Announcement
# ==========================================================

def generate_announcement() -> dict:

    return {

        "title":
            random.choice([
                "Community Guidelines",
                "Known Issues",
                "Patch Discussion",
                "Read Before Posting",
                "Official Support Information",
            ]),

        "timestamp":
            random.choice([
                "Today",
                "Yesterday",
                "2 days ago",
                "Last week",
            ]),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_discussion_forum_data() -> dict:

    threads = [
        generate_thread()
        for _ in range(
            random.randint(
                16,
                28,
            )
        )
    ]

    categories = []

    for category in FORUM_CATEGORIES:

        categories.append({
            "name":
                category,

            "count":
                random.randint(
                    20,
                    3500,
                ),

            "selected":
                False,
        })

    selected_category = random.choice(
        categories
    )

    selected_category["selected"] = True

    return {

        "title":
            "Discussions",

        "game": {
            "title":
                fake.catch_phrase(),

            "cover":
                get_random_game_cover(),
        },

        "search_placeholder":
            "Search discussions",

        "categories":
            categories,

        "threads":
            threads,

        "online_users":
            random.randint(
                400,
                50000,
            ),

        "thread_count":
            random.randint(
                2000,
                150000,
            ),

        "moderators": [
            generate_moderator()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],

        "announcements": [
            generate_announcement()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],

        "current_page":
            random.randint(
                1,
                5,
            ),

        "total_pages":
            random.randint(
                12,
                150,
            ),
    }