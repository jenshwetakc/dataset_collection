from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_playlist_cover,
)

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)


# ==========================================================
# Data Pools
# ==========================================================

PLAYLIST_NAMES = [
    "Liked Songs",
    "Late Night Mix",
    "Study Sessions",
    "Road Trip",
    "Weekend Vibes",
    "Morning Energy",
    "Chill Collection",
    "Workout Rotation",
    "Daily Favorites",
    "New Discoveries",
    "Focus Mode",
    "Summer Memories",
    "Coding Playlist",
    "Running Mix",
    "Coffee Shop",
    "Evening Acoustic",
]


TRACK_TITLES = [
    "Midnight Drive",
    "Golden Hour",
    "Northern Lights",
    "After Midnight",
    "Slow Motion",
    "Daydream",
    "Open Roads",
    "Blue Horizon",
    "Quiet Places",
    "Summer Rain",
    "Parallel Lines",
    "Falling Stars",
]


ARTIST_NAMES = [
    "Maya Chen",
    "Leo Hart",
    "Aria Stone",
    "Noah Reed",
    "Luna Park",
    "River Lane",
    "Nova Lights",
    "Daniel Grey",
    "Hana Lee",
    "Elena Cruz",
]


# ==========================================================
# Playlist Item
# ==========================================================

def generate_playlist_item() -> dict:

    track_count = random.randint(
        12,
        180,
    )

    selected = (
        random.random() < 0.20
    )

    return {

        "title":
            random.choice(
                PLAYLIST_NAMES
            ),

        "subtitle":
            random.choice(
                [
                    f"Playlist • {track_count} songs",
                    f"{track_count} songs",
                    "Playlist • Spotify",
                ]
            ),

        "image":
            (
                get_random_playlist_cover()
                or
                get_random_album_cover()
            ),

        "selected":
            selected,

        "pinned":
            random.random() < 0.15,
    }


# ==========================================================
# Page Generator
# ==========================================================

def generate_add_to_playlist_page() -> dict:

    playlist_count = random.randint(
        8,
        16,
    )

    playlists = [

        generate_playlist_item()

        for _
        in range(
            playlist_count
        )
    ]


    selected_count = sum(
        1
        for item
        in playlists
        if item["selected"]
    )


    return {

        # ==================================================
        # Navigation
        # ==================================================

        "navigation":
            generate_navigation(
                selected="library"
            ),


        # ==================================================
        # Current Track
        # ==================================================

        "track": {

            "title":
                random.choice(
                    TRACK_TITLES
                ),

            "artist":
                random.choice(
                    ARTIST_NAMES
                ),

            "image":
                get_random_album_cover(),
        },


        # ==================================================
        # Sheet
        # ==================================================

        "title":
            "Add to playlist",

        "search_placeholder":
            "Find a playlist",

        "playlists":
            playlists,

        "selected_count":
            selected_count,

        "show_create_playlist":
            random.random() < 0.85,

        "multi_select":
            random.random() < 0.60,
    }