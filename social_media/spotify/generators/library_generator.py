from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_playlist_cover,
    get_random_artist_image,
    get_random_podcast_cover,
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
    "Daily Mix",
    "Morning Energy",
    "Deep Work",
    "Weekend Vibes",
    "Discover Weekly",
    "Chill Evening",
    "Coding Mode",
    "Road Trip",
    "Study Session",
    "Workout Hits",
    "Peaceful Piano",
    "Throwback Favorites",
    "Summer Memories",
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
    "Echoes",
    "Daylight",
]


PODCAST_NAMES = [
    "Tech Today",
    "Design Stories",
    "Daily Conversations",
    "Science Explained",
    "Creative Minds",
    "The Productivity Show",
    "World Stories",
    "Developer Radio",
    "Future Thinking",
    "Inside Innovation",
]


LIBRARY_FILTERS = [
    {
        "name": "Playlists",
        "semantic": "playlists",
    },
    {
        "name": "Artists",
        "semantic": "artists",
    },
    {
        "name": "Albums",
        "semantic": "albums",
    },
    {
        "name": "Podcasts & Shows",
        "semantic": "podcasts",
    },
]


SORT_OPTIONS = [
    "Recently added",
    "Alphabetical",
    "Creator",
    "Recently played",
]


# ==========================================================
# Helpers
# ==========================================================

def get_image_for_type(
    item_type: str,
):

    if item_type == "playlist":

        return (
            get_random_playlist_cover()
            or get_random_album_cover()
        )

    if item_type == "artist":

        return (
            get_random_artist_image()
            or get_random_album_cover()
        )

    if item_type == "album":

        return (
            get_random_album_cover()
        )

    if item_type == "podcast":

        return (
            get_random_podcast_cover()
            or get_random_album_cover()
        )

    return (
        get_random_album_cover()
    )


# ==========================================================
# Playlist
# ==========================================================

def generate_playlist_item() -> dict:

    song_count = random.randint(
        12,
        120,
    )

    return {

        "type":
            "playlist",

        "title":
            random.choice(
                PLAYLIST_NAMES
            ),

        "subtitle":
            random.choice(
                [
                    f"Playlist • {song_count} songs",
                    "Playlist",
                    "Playlist • Spotify",
                ]
            ),

        "image":
            get_image_for_type(
                "playlist"
            ),

        "pinned":
            random.random() < 0.25,

        "downloaded":
            random.random() < 0.15,
    }


# ==========================================================
# Artist
# ==========================================================

def generate_artist_item() -> dict:

    return {

        "type":
            "artist",

        "title":
            random.choice(
                ARTIST_NAMES
            ),

        "subtitle":
            "Artist",

        "image":
            get_image_for_type(
                "artist"
            ),

        "pinned":
            random.random() < 0.20,

        "downloaded":
            False,
    }


# ==========================================================
# Album
# ==========================================================

def generate_album_item() -> dict:

    artist = random.choice(
        ARTIST_NAMES
    )

    return {

        "type":
            "album",

        "title":
            random.choice(
                ALBUM_NAMES
            ),

        "subtitle":
            f"Album • {artist}",

        "image":
            get_image_for_type(
                "album"
            ),

        "pinned":
            random.random() < 0.15,

        "downloaded":
            random.random() < 0.12,
    }


# ==========================================================
# Podcast
# ==========================================================

def generate_podcast_item() -> dict:

    return {

        "type":
            "podcast",

        "title":
            random.choice(
                PODCAST_NAMES
            ),

        "subtitle":
            random.choice(
                [
                    "Podcast",
                    "Podcast • New episodes",
                    "Show",
                ]
            ),

        "image":
            get_image_for_type(
                "podcast"
            ),

        "pinned":
            random.random() < 0.15,

        "downloaded":
            random.random() < 0.10,
    }


# ==========================================================
# Generic Library Item
# ==========================================================

def generate_library_item(
    item_type: str,
) -> dict:

    if item_type == "playlist":

        return (
            generate_playlist_item()
        )

    if item_type == "artist":

        return (
            generate_artist_item()
        )

    if item_type == "album":

        return (
            generate_album_item()
        )

    if item_type == "podcast":

        return (
            generate_podcast_item()
        )

    raise ValueError(
        f"Unknown library item type: "
        f"{item_type}"
    )


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> list[dict]:

    filter_count = random.randint(
        2,
        len(
            LIBRARY_FILTERS
        ),
    )

    selected_filters = random.sample(
        LIBRARY_FILTERS,
        k=filter_count,
    )

    active_filter = random.choice(
        [
            None,
            *[
                item["semantic"]
                for item
                in selected_filters
            ],
        ]
    )

    result = []

    for item in selected_filters:

        result.append(
            {
                **item,
                "selected":
                    (
                        item["semantic"]
                        == active_filter
                    ),
            }
        )

    return result


# ==========================================================
# Page Generator
# ==========================================================

def generate_library_page() -> dict:

    filters = (
        generate_filters()
    )

    active_filter = next(
        (
            item["semantic"]
            for item
            in filters
            if item["selected"]
        ),
        None,
    )


    # ------------------------------------------------------
    # Decide item population
    # ------------------------------------------------------

    if active_filter:

        type_mapping = {

            "playlists":
                "playlist",

            "artists":
                "artist",

            "albums":
                "album",

            "podcasts":
                "podcast",
        }

        allowed_types = [
            type_mapping[
                active_filter
            ]
        ]

    else:

        allowed_types = [
            "playlist",
            "artist",
            "album",
            "podcast",
        ]


    item_count = random.randint(
        12,
        24,
    )


    items = [

        generate_library_item(
            random.choice(
                allowed_types
            )
        )

        for _
        in range(
            item_count
        )
    ]


    # ------------------------------------------------------
    # Put pinned items toward the top
    # ------------------------------------------------------

    items.sort(
        key=lambda item:
            not item[
                "pinned"
            ]
    )


    return {

        "navigation":
            generate_navigation(
                selected="library"
            ),

        "title":
            "Your Library",

        "filters":
            filters,

        "sort":
            random.choice(
                SORT_OPTIONS
            ),

        "view_mode":
            random.choice(
                [
                    "list",
                    "list",
                    "list",
                    "grid",
                ]
            ),

        "items":
            items,

        "player":
            generate_player(),
    }