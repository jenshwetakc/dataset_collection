from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_playlist_cover,
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

PLAYLIST_NAMES = [
    "Late Night Focus",
    "Deep Work",
    "Morning Energy",
    "Weekend Vibes",
    "Discover Weekly",
    "Chill Evening",
    "Coding Mode",
    "Road Trip",
    "Study Session",
    "Workout Hits",
    "Peaceful Piano",
    "Indie Mix",
    "Summer Memories",
    "Daily Rotation",
    "Fresh Finds",
    "Night Drive",
    "Coffee & Chill",
    "Feel Good Mix",
]


PLAYLIST_DESCRIPTIONS = [
    "Music to help you focus and stay productive.",
    "A collection of tracks for your daily routine.",
    "The songs you keep coming back to.",
    "Fresh music selected for your listening session.",
    "A mix made for quiet evenings and late nights.",
    "Your soundtrack for studying, working, and relaxing.",
    "Discover familiar favorites and something new.",
    "A playlist for wherever the day takes you.",
]


CREATOR_NAMES = [
    "Spotify",
    "Maya Chen",
    "Leo Hart",
    "Aria Stone",
    "Noah Reed",
    "Luna Park",
    "Daniel Grey",
    "Hana Lee",
    "Alex Morgan",
    "Jamie Park",
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
    "City Lights",
    "Paper Planes",
    "Endless Summer",
    "Moonlight",
    "Somewhere Else",
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


# ==========================================================
# Duration
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

def generate_playlist_track(
    index: int,
) -> dict:

    artist = random.choice(
        ARTIST_NAMES
    )

    album = random.choice(
        ALBUM_NAMES
    )

    return {

        "number":
            index,

        "title":
            random.choice(
                TRACK_TITLES
            ),

        "artist":
            artist,

        "album":
            album,

        "duration":
            random_duration(),

        "image":
            (
                get_random_album_cover()
            ),

        "liked":
            random.random() < 0.20,

        "explicit":
            random.random() < 0.12,

        "downloaded":
            random.random() < 0.08,
    }


# ==========================================================
# Playlist
# ==========================================================

def generate_playlist_page() -> dict:

    track_count = random.randint(
        14,
        30,
    )

    tracks = [

        generate_playlist_track(
            index + 1
        )

        for index in range(
            track_count
        )
    ]


    playlist_name = random.choice(
        PLAYLIST_NAMES
    )

    creator = random.choice(
        CREATOR_NAMES
    )


    total_minutes = sum(
        random.randint(
            3,
            5,
        )
        for _
        in tracks
    )


    hours = (
        total_minutes
        // 60
    )

    minutes = (
        total_minutes
        % 60
    )


    if hours > 0:

        duration_text = (
            f"{hours} hr "
            f"{minutes} min"
        )

    else:

        duration_text = (
            f"{minutes} min"
        )


    return {

        "navigation":
            generate_navigation(
                selected="library"
            ),

        "playlist": {

            "name":
                playlist_name,

            "description":
                random.choice(
                    PLAYLIST_DESCRIPTIONS
                ),

            "creator":
                creator,

            "image":
                (
                    get_random_playlist_cover()
                    or
                    get_random_album_cover()
                ),

            "track_count":
                track_count,

            "duration":
                duration_text,

            "public":
                random.random() < 0.85,

            "liked":
                random.random() < 0.35,

            "downloaded":
                random.random() < 0.15,

            "followers":
                random.randint(
                    120,
                    950000,
                ),
        },

        "tracks":
            tracks,

        "sort":
            random.choice(
                [
                    "Custom order",
                    "Title",
                    "Artist",
                    "Album",
                    "Recently added",
                ]
            ),

        "player":
            generate_player(),
    }