from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_avatar,
    get_random_game_banner,
    get_random_game_cover,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

PROFILE_STATES = [
    "Online",
    "Away",
    "Busy",
    "Offline",
]


BADGES = [
    "Community Ambassador",
    "Collector",
    "Veteran",
    "Workshop Creator",
    "Game Collector",
    "Event Participant",
]


# ==========================================================
# Game
# ==========================================================

def generate_profile_game() -> dict:

    playtime = round(
        random.uniform(
            1,
            950,
        ),
        1,
    )

    return {

        "title":
            fake.catch_phrase(),

        "cover":
            get_random_game_cover(),

        "playtime":
            f"{playtime:.1f} hrs",

        "last_played":
            random.choice([
                "Played today",
                "Played yesterday",
                "Played 3 days ago",
                "Played last week",
                "Played 2 weeks ago",
            ]),

        "achievement_percent":
            random.randint(
                5,
                100,
            ),
    }


# ==========================================================
# Friend
# ==========================================================

def generate_friend() -> dict:

    state = random.choice(
        PROFILE_STATES
    )

    return {

        "name":
            fake.user_name(),

        "avatar":
            get_random_avatar(),

        "state":
            state,

        "level":
            random.randint(
                1,
                250,
            ),
    }


# ==========================================================
# Achievement
# ==========================================================

def generate_achievement() -> dict:

    return {

        "title":
            random.choice([
                "Master Explorer",
                "First Victory",
                "Completionist",
                "Hidden Discovery",
                "Veteran Player",
                "Perfect Run",
            ]),

        "icon":
            random.choice([
                "emoji_events",
                "military_tech",
                "workspace_premium",
                "stars",
                "trophy",
            ]),

        "game":
            fake.catch_phrase(),
    }


# ==========================================================
# Comment
# ==========================================================

def generate_comment() -> dict:

    return {

        "author":
            fake.user_name(),

        "avatar":
            get_random_avatar(),

        "text":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    16,
                )
            ),

        "timestamp":
            random.choice([
                "Just now",
                "15 minutes ago",
                "2 hours ago",
                "Yesterday",
                "3 days ago",
                "Last week",
            ]),
    }


# ==========================================================
# Showcase
# ==========================================================

def generate_showcase() -> dict:

    showcase_type = random.choice([
        "Favorite Game",
        "Rare Achievement",
        "Item Showcase",
        "Screenshot Showcase",
    ])

    return {

        "type":
            showcase_type,

        "title":
            fake.catch_phrase(),

        "image":
            get_random_game_cover(),

        "description":
            fake.sentence(
                nb_words=random.randint(
                    6,
                    13,
                )
            ),
    }


# ==========================================================
# Main
# ==========================================================

def generate_profile_data() -> dict:

    level = random.randint(
        5,
        350,
    )

    games_owned = random.randint(
        25,
        1200,
    )

    friends = [
        generate_friend()
        for _ in range(
            random.randint(
                8,
                14,
            )
        )
    ]

    recent_games = [
        generate_profile_game()
        for _ in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    return {

        "user": {

            "name":
                fake.user_name(),

            "real_name":
                fake.name(),

            "avatar":
                get_random_avatar(),

            "banner":
                get_random_game_banner(),

            "state":
                random.choice(
                    PROFILE_STATES
                ),

            "location":
                fake.city(),

            "level":
                level,

            "summary":
                fake.paragraph(
                    nb_sentences=random.randint(
                        2,
                        4,
                    )
                ),
        },

        "stats": {

            "games":
                games_owned,

            "friends":
                len(
                    friends
                ),

            "groups":
                random.randint(
                    1,
                    30,
                ),

            "screenshots":
                random.randint(
                    5,
                    500,
                ),

            "reviews":
                random.randint(
                    0,
                    120,
                ),
        },

        "badges": [
            random.choice(
                BADGES
            )
            for _ in range(
                random.randint(
                    3,
                    6,
                )
            )
        ],

        "recent_games":
            recent_games,

        "friends":
            friends,

        "achievements": [
            generate_achievement()
            for _ in range(
                5
            )
        ],

        "showcases": [
            generate_showcase()
            for _ in range(
                random.randint(
                    2,
                    4,
                )
            )
        ],

        "comments": [
            generate_comment()
            for _ in range(
                random.randint(
                    4,
                    8,
                )
            )
        ],
    }