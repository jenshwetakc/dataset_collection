from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
)

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)

from social_media.spotify.generators.home_generator import (
    generate_player,
)


# ==========================================================
# Data Pools
# ==========================================================

TRACK_TITLES = [
    "Midnight Drive",
    "Golden Hour",
    "Lost in the City",
    "Northern Lights",
    "Slow Motion",
    "Daydream",
    "Open Roads",
    "Blue Horizon",
    "After Midnight",
    "Falling Stars",
    "Quiet Places",
    "New Beginnings",
    "Parallel Lines",
    "Summer Rain",
    "Echoes",
    "Daylight",
    "Stay Awhile",
    "Crystal Sky",
    "Ocean View",
    "Last Train Home",
]


ARTIST_NAMES = [
    "Maya Chen",
    "Leo Hart",
    "Aria Stone",
    "Noah Reed",
    "Luna Park",
    "The Midnight Echo",
    "River Lane",
    "Nova Lights",
    "Daniel Grey",
    "Hana Lee",
    "Elena Cruz",
    "James Monroe",
]


ALBUM_NAMES = [
    "Northern Lights",
    "After Midnight",
    "Golden Hour",
    "Fragments",
    "Blue Horizon",
    "City Dreams",
    "Parallel Lines",
    "Quiet Places",
    "Open Roads",
    "New Beginnings",
]


DEVICES = [
    "This device",
    "Living Room Speaker",
    "Bedroom Speaker",
    "Wireless Headphones",
    "Desktop",
    "Smart TV",
]


# ==========================================================
# Helpers
# ==========================================================

def random_duration_seconds() -> int:

    return random.randint(
        150,
        330,
    )


def format_duration(
    seconds: int,
) -> str:

    minutes = (
        seconds // 60
    )

    remaining = (
        seconds % 60
    )

    return (
        f"{minutes}:"
        f"{remaining:02d}"
    )


# ==========================================================
# Page Generator
# ==========================================================

def generate_now_playing_page() -> dict:

    duration_seconds = (
        random_duration_seconds()
    )

    progress_ratio = random.uniform(
        0.05,
        0.92,
    )

    elapsed_seconds = int(
        duration_seconds
        * progress_ratio
    )


    return {

        "navigation":
            generate_navigation(
                selected="home"
            ),

        "track": {

            "title":
                random.choice(
                    TRACK_TITLES
                ),

            "artist":
                random.choice(
                    ARTIST_NAMES
                ),

            "album":
                random.choice(
                    ALBUM_NAMES
                ),

            "image":
                get_random_album_cover(),

            "duration":
                format_duration(
                    duration_seconds
                ),

            "duration_seconds":
                duration_seconds,

            "elapsed":
                format_duration(
                    elapsed_seconds
                ),

            "elapsed_seconds":
                elapsed_seconds,

            "progress":
                progress_ratio,

            "liked":
                random.random() < 0.45,

            "explicit":
                random.random() < 0.10,
        },

        "playing":
            random.random() < 0.75,

        "shuffle":
            random.random() < 0.35,

        "repeat":
            random.random() < 0.30,

        "repeat_one":
            random.random() < 0.10,

        "volume":
            random.uniform(
                0.25,
                1.0,
            ),

        "device":
            random.choice(
                DEVICES
            ),

        "queue_count":
            random.randint(
                3,
                24,
            ),

        "lyrics_available":
            random.random() < 0.70,

        "player":
            generate_player(),
    }