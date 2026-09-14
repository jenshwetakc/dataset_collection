from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_artist_image,
    get_random_artist_banner,
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
    "Sora Kim",
    "The Skyline",
]


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
    "Echoes",
    "Daylight",
]


GENRES = [
    "Pop",
    "Indie",
    "Alternative",
    "Electronic",
    "R&B",
    "Rock",
    "Ambient",
    "Dance",
]


# ==========================================================
# Helpers
# ==========================================================

def random_duration() -> str:

    minutes = random.randint(
        2,
        5,
    )

    seconds = random.randint(
        0,
        59,
    )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


def format_number(
    value: int,
) -> str:

    if value >= 1_000_000:

        return (
            f"{value / 1_000_000:.1f}M"
        )

    if value >= 1_000:

        return (
            f"{value / 1_000:.1f}K"
        )

    return str(
        value
    )


# ==========================================================
# Popular Track
# ==========================================================

def generate_popular_track(
    index: int,
) -> dict:

    plays = random.randint(
        100_000,
        300_000_000,
    )

    return {

        "number":
            index,

        "title":
            random.choice(
                TRACK_TITLES
            ),

        "image":
            get_random_album_cover(),

        "plays":
            format_number(
                plays
            ),

        "duration":
            random_duration(),

        "liked":
            random.random() < 0.20,

        "explicit":
            random.random() < 0.12,
    }


# ==========================================================
# Discography Item
# ==========================================================

def generate_discography_item() -> dict:

    release_type = random.choice(
        [
            "Album",
            "Single",
            "EP",
        ]
    )

    return {

        "title":
            random.choice(
                ALBUM_NAMES
            ),

        "image":
            get_random_album_cover(),

        "year":
            random.randint(
                2000,
                2026,
            ),

        "type":
            release_type,
    }


# ==========================================================
# Related Artist
# ==========================================================

def generate_related_artist() -> dict:

    return {

        "name":
            random.choice(
                ARTIST_NAMES
            ),

        "image":
            get_random_artist_image(),

        "followers":
            format_number(
                random.randint(
                    10_000,
                    20_000_000,
                )
            ),
    }


# ==========================================================
# Artist Page
# ==========================================================

def generate_artist_page() -> dict:

    artist_name = random.choice(
        ARTIST_NAMES
    )

    followers = random.randint(
        20_000,
        50_000_000,
    )

    monthly_listeners = random.randint(
        100_000,
        90_000_000,
    )


    popular_track_count = random.randint(
        5,
        10,
    )


    discography_count = random.randint(
        5,
        10,
    )


    related_count = random.randint(
        5,
        10,
    )


    return {

        "navigation":
            generate_navigation(
                selected="library"
            ),

        "artist": {

            "name":
                artist_name,

            "avatar":
                get_random_artist_image(),

            "banner":
                (
                    get_random_artist_banner()
                    or
                    get_random_artist_image()
                ),

            "verified":
                random.random() < 0.65,

            "followed":
                random.random() < 0.30,

            "followers":
                format_number(
                    followers
                ),

            "monthly_listeners":
                format_number(
                    monthly_listeners
                ),

            "genre":
                random.choice(
                    GENRES
                ),
        },

        "popular_tracks": [

            generate_popular_track(
                index + 1
            )

            for index in range(
                popular_track_count
            )
        ],

        "discography": [

            generate_discography_item()

            for _
            in range(
                discography_count
            )
        ],

        "related_artists": [

            generate_related_artist()

            for _
            in range(
                related_count
            )
        ],

        "player":
            generate_player(),
    }