from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_game_banner,
    get_random_game_cover,
    get_random_game_screenshot,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

GENRES = [
    "Action",
    "Adventure",
    "RPG",
    "Strategy",
    "Simulation",
    "Indie",
    "Racing",
    "Sports",
    "Puzzle",
    "Horror",
    "Multiplayer",
    "Co-op",
    "Survival",
    "Open World",
]


GAME_STATES = [
    "Installed",
    "Not Installed",
    "Updating",
    "Cloud Sync",
]


ACTIVITY_TYPES = [
    "Achievement unlocked",
    "Played recently",
    "Screenshot uploaded",
    "Cloud save synchronized",
    "Game updated",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_game_title() -> str:

    templates = [
        lambda: f"{fake.word().title()} Odyssey",
        lambda: f"{fake.word().title()} Protocol",
        lambda: f"{fake.word().title()} Frontier",
        lambda: f"Project {fake.word().title()}",
        lambda: f"{fake.word().title()} Horizon",
        lambda: f"The {fake.word().title()} Realm",
        lambda: f"{fake.word().title()} Chronicles",
    ]

    return random.choice(
        templates
    )()


# ==========================================================
# Achievement
# ==========================================================

def generate_achievement() -> dict:

    return {

        "title":
            random.choice([
                "First Steps",
                "Explorer",
                "Veteran",
                "Master Builder",
                "Hidden Secret",
                "Perfect Run",
                "Survivor",
                "Champion",
            ]),

        "description":
            fake.sentence(
                nb_words=random.randint(
                    5,
                    10,
                )
            ),

        "icon":
            random.choice([
                "military_tech",
                "emoji_events",
                "workspace_premium",
                "stars",
                "trophy",
            ]),

        "unlocked":
            random.random() < 0.75,
    }


# ==========================================================
# Activity
# ==========================================================

def generate_activity() -> dict:

    return {

        "type":
            random.choice(
                ACTIVITY_TYPES
            ),

        "text":
            fake.sentence(
                nb_words=random.randint(
                    5,
                    12,
                )
            ),

        "timestamp":
            random.choice([
                "Just now",
                "12 minutes ago",
                "2 hours ago",
                "Yesterday",
                "3 days ago",
                "Last week",
            ]),
    }


# ==========================================================
# Library Game
# ==========================================================

def generate_library_game() -> dict:

    state = random.choice(
        GAME_STATES
    )

    playtime_hours = round(
        random.uniform(
            0.2,
            860,
        ),
        1,
    )

    last_played = random.choice([
        "Today",
        "Yesterday",
        "3 days ago",
        "Last week",
        "2 weeks ago",
        "Last month",
    ])

    progress = random.randint(
        0,
        100,
    )

    return {

        "title":
            generate_game_title(),

        "cover":
            get_random_game_cover(),

        "banner":
            get_random_game_banner(),

        "genres":
            random.sample(
                GENRES,
                k=random.randint(
                    2,
                    4,
                ),
            ),

        "state":
            state,

        "playtime":
            f"{playtime_hours:.1f} hrs",

        "last_played":
            last_played,

        "installed":
            state
            in {
                "Installed",
                "Updating",
                "Cloud Sync",
            },

        "update_progress":
            (
                progress
                if state == "Updating"
                else None
            ),

        "favorite":
            random.random() < 0.25,
    }


# ==========================================================
# Selected Game
# ==========================================================

def generate_selected_game() -> dict:

    game = generate_library_game()

    achievement_total = random.randint(
        20,
        80,
    )

    achievement_unlocked = random.randint(
        0,
        achievement_total,
    )

    game.update({

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "developer":
            fake.company(),

        "achievement_total":
            achievement_total,

        "achievement_unlocked":
            achievement_unlocked,

        "achievement_percent":
            round(
                achievement_unlocked
                / achievement_total
                * 100
            ),

        "achievements": [
            generate_achievement()
            for _ in range(
                5
            )
        ],

        "screenshots": [
            get_random_game_screenshot()
            for _ in range(
                4
            )
        ],

        "activity": [
            generate_activity()
            for _ in range(
                random.randint(
                    4,
                    7,
                )
            )
        ],
    })

    return game


# ==========================================================
# Main Generator
# ==========================================================

def generate_library_data() -> dict:

    selected_game = (
        generate_selected_game()
    )

    games = [
        selected_game,
    ]

    games.extend(
        generate_library_game()
        for _ in range(
            random.randint(
                14,
                24,
            )
        )
    )

    random.shuffle(
        games
    )

    selected_title = (
        selected_game["title"]
    )

    return {

        "brand":
            "STEAM",

        "library_title":
            random.choice([
                "LIBRARY",
                "My Games",
                "Game Library",
            ]),

        "search_placeholder":
            "Search library",

        "filters": [
            "Games",
            "Installed",
            "Favorites",
        ],

        "selected_filter":
            random.choice([
                "Games",
                "Installed",
                "Favorites",
            ]),

        "games":
            games,

        "selected_game":
            selected_game,

        "selected_title":
            selected_title,

        "storage": {

            "used":
                random.randint(
                    120,
                    850,
                ),

            "total":
                random.choice([
                    512,
                    1000,
                    2000,
                ]),
        },
    }