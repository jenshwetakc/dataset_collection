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
    "My Playlist",
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
]


PLAYLIST_DESCRIPTIONS = [
    "A collection of songs I love.",
    "Music for studying and staying focused.",
    "Songs for late nights and quiet moments.",
    "A playlist for the road.",
    "My current favorite tracks.",
    "Music to keep the energy going.",
    "A little bit of everything.",
    "Tracks for relaxing and slowing down.",
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
    "New Beginnings",
    "Crystal Sky",
    "Ocean View",
    "City Lights",
    "Last Train Home",
    "Echoes",
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
    "James Monroe",
    "Sora Kim",
]


# ==========================================================
# Suggested Track
# ==========================================================

def generate_suggested_track() -> dict:

    return {

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

        "explicit":
            random.random() < 0.12,

        "added":
            random.random() < 0.18,
    }


# ==========================================================
# Background Library Item
# ==========================================================

def generate_background_item() -> dict:

    return {

        "title":
            random.choice(
                PLAYLIST_NAMES
            ),

        "subtitle":
            random.choice(
                [
                    "Playlist",
                    "Playlist • Spotify",
                    "Playlist • 42 songs",
                    "Playlist • 28 songs",
                ]
            ),

        "image":
            (
                get_random_playlist_cover()
                or
                get_random_album_cover()
            ),
    }


# ==========================================================
# Page Generator
# ==========================================================

def generate_create_playlist_page() -> dict:

    mode = random.choice(
        [
            "create",
            "edit",
        ]
    )


    if mode == "create":

        title = "Create playlist"

        playlist_name = random.choice(
            [
                "",
                "My Playlist",
                "New Playlist",
            ]
        )

        description = random.choice(
            [
                "",
                random.choice(
                    PLAYLIST_DESCRIPTIONS
                ),
            ]
        )

    else:

        title = "Edit playlist"

        playlist_name = random.choice(
            PLAYLIST_NAMES
        )

        description = random.choice(
            PLAYLIST_DESCRIPTIONS
        )


    cover = None

    if (
        mode == "edit"
        or random.random() < 0.60
    ):

        cover = (
            get_random_playlist_cover()
            or
            get_random_album_cover()
        )


    suggested_track_count = (
        random.randint(
            4,
            8,
        )
    )


    background_item_count = (
        random.randint(
            6,
            12,
        )
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
        # Dialog State
        # ==================================================

        "mode":
            mode,

        "title":
            title,


        # ==================================================
        # Playlist
        # ==================================================

        "playlist": {

            "name":
                playlist_name,

            "description":
                description,

            "cover":
                cover,

            "public":
                random.random() < 0.70,

            "collaborative":
                random.random() < 0.20,
        },


        # ==================================================
        # Search
        # ==================================================

        "search_placeholder":
            random.choice(
                [
                    "Search for songs or episodes",
                    "Find songs for your playlist",
                    "Search Spotify",
                ]
            ),


        # ==================================================
        # Suggested Tracks
        # ==================================================

        "suggested_tracks": [

            generate_suggested_track()

            for _
            in range(
                suggested_track_count
            )
        ],


        # ==================================================
        # Background Page
        #
        # The modal sits above this content, allowing us to
        # test actual occlusion clipping.
        # ==================================================

        "background_items": [

            generate_background_item()

            for _
            in range(
                background_item_count
            )
        ],
    }