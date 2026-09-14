from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_artist_image,
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
    "Paper Skies",
    "Lost Signals",
    "Summer Rain",
    "Ocean Avenue",
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
    "Ocean View",
    "Last Train Home",
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


# ==========================================================
# Track
# ==========================================================

def generate_album_track(
    index: int,
) -> dict:

    return {

        "number":
            index,

        "title":
            random.choice(
                TRACK_TITLES
            ),

        "duration":
            random_duration(),

        "liked":
            random.random() < 0.18,

        "explicit":
            random.random() < 0.10,

        "downloaded":
            random.random() < 0.08,
    }


# ==========================================================
# Album Page
# ==========================================================

def generate_album_page() -> dict:

    artist = random.choice(
        ARTIST_NAMES
    )

    track_count = random.randint(
        8,
        16,
    )

    tracks = [

        generate_album_track(
            index + 1
        )

        for index in range(
            track_count
        )
    ]


    total_minutes = sum(
        random.randint(
            3,
            5,
        )
        for _
        in tracks
    )


    release_year = random.randint(
        1995,
        2026,
    )


    album_type = random.choice(
        [
            "Album",
            "EP",
            "Single",
        ]
    )


    return {

        "navigation":
            generate_navigation(
                selected="library"
            ),

        "album": {

            "name":
                random.choice(
                    ALBUM_NAMES
                ),

            "artist":
                artist,

            "artist_image":
                get_random_artist_image(),

            "cover":
                get_random_album_cover(),

            "type":
                album_type,

            "year":
                release_year,

            "genre":
                random.choice(
                    GENRES
                ),

            "track_count":
                track_count,

            "duration":
                f"{total_minutes} min",

            "liked":
                random.random() < 0.35,

            "downloaded":
                random.random() < 0.20,
        },

        "tracks":
            tracks,

        "copyright":
            (
                f"© {release_year} "
                f"{artist} Records"
        ),

        "player":
            generate_player(),
    }