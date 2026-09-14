from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_artist_image,
    get_random_music_cover,
    get_random_playlist_cover,
)


# ==========================================================
# Content Pools
# ==========================================================

TRACK_TITLES = [

    "Midnight Drive",
    "Golden Hour",
    "Lost in the City",
    "Afterglow",
    "Stay With Me",
    "Northern Lights",
    "Dream Again",
    "Slow Motion",
    "Falling Stars",
    "Ocean Eyes",
    "Summer Rain",
    "Electric Heart",
    "Blue Skies",
    "Into the Night",
    "Parallel Lines",
    "Another Morning",
    "Paper Moon",
    "City Lights",
    "Last Goodbye",
    "Open Roads",
]


ARTIST_NAMES = [

    "Lena Harper",
    "Nova Lane",
    "The Wild Hours",
    "Eli Morgan",
    "June Parker",
    "Arden Grey",
    "Maya Rivers",
    "Velvet Coast",
    "Theo Miles",
    "Luna Vale",
    "Echo Garden",
    "Sofia Reed",
    "Northbound",
    "Avery Stone",
    "Neon Harbor",
    "Willow June",
]


ALBUM_NAMES = [

    "Midnight Stories",
    "Open Skies",
    "Neon Dreams",
    "After Hours",
    "Golden Days",
    "Blue Horizon",
    "Quiet Places",
    "Northern Lights",
    "Paper Hearts",
    "Endless Summer",
    "Parallel",
    "Dream State",
]


PLAYLIST_NAMES = [

    "Daily Mix 1",
    "Daily Mix 2",
    "Chill Mix",
    "Discover Weekly",
    "Release Radar",
    "Morning Acoustic",
    "Late Night Vibes",
    "Focus Flow",
    "Road Trip",
    "Soft Pop",
    "Indie Favorites",
    "Weekend Mood",
    "Peaceful Piano",
    "Energy Boost",
    "Fresh Finds",
]


SECTION_TITLES = [

    "Recently played",
    "Made for you",
    "Your top mixes",
    "Jump back in",
    "Popular right now",
    "Recommended for today",
    "More of what you like",
    "Based on your recent listening",
    "Episodes for you",
    "New releases for you",
]


GREETING_OPTIONS = [

    "Good morning",
    "Good afternoon",
    "Good evening",
    "Welcome back",
]


# ==========================================================
# Utility
# ==========================================================

def random_duration() -> str:

    minutes = random.randint(
        2,
        5
    )

    seconds = random.randint(
        0,
        59
    )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


def random_progress() -> float:

    return round(
        random.uniform(
            0.05,
            0.90
        ),
        3,
    )


# ==========================================================
# Track
# ==========================================================

def generate_track() -> dict:

    return {

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
            get_random_album_cover()
            or get_random_music_cover(),

        "duration":
            random_duration(),

        "liked":
            random.random()
            < 0.30,

        "explicit":
            random.random()
            < 0.15,
    }


# ==========================================================
# Media Card
# ==========================================================

def generate_media_card(
    card_type: str | None = None,
) -> dict:

    card_type = (
        card_type
        or random.choice(
            [
                "album",
                "playlist",
                "artist",
            ]
        )
    )

    if card_type == "artist":

        artist = random.choice(
            ARTIST_NAMES
        )

        return {

            "type":
                "artist",

            "title":
                artist,

            "subtitle":
                "Artist",

            "image":
                get_random_artist_image()
                or get_random_music_cover(),

            "circular":
                True,
        }

    if card_type == "playlist":

        return {

            "type":
                "playlist",

            "title":
                random.choice(
                    PLAYLIST_NAMES
                ),

            "subtitle":
                (
                    "Playlist • "
                    + random.choice(
                        ARTIST_NAMES
                    )
                ),

            "image":
                get_random_playlist_cover()
                or get_random_music_cover(),

            "circular":
                False,
        }

    album = random.choice(
        ALBUM_NAMES
    )

    artist = random.choice(
        ARTIST_NAMES
    )

    return {

        "type":
            "album",

        "title":
            album,

        "subtitle":
            artist,

        "image":
            get_random_album_cover()
            or get_random_music_cover(),

        "circular":
            False,
    }


# ==========================================================
# Quick Access Card
# ==========================================================

def generate_quick_access_item() -> dict:

    if random.random() < 0.5:

        title = random.choice(
            PLAYLIST_NAMES
        )

        image = (
            get_random_playlist_cover()
            or get_random_music_cover()
        )

        item_type = "playlist"

    else:

        title = random.choice(
            ALBUM_NAMES
        )

        image = (
            get_random_album_cover()
            or get_random_music_cover()
        )

        item_type = "album"

    return {

        "type":
            item_type,

        "title":
            title,

        "image":
            image,
    }


# ==========================================================
# Section
# ==========================================================

def generate_section(
    title: str | None = None,
    item_count: int | None = None,
) -> dict:

    item_count = (
        item_count
        or random.randint(
            6,
            10
        )
    )

    return {

        "title":
            title
            or random.choice(
                SECTION_TITLES
            ),

        "show_all":
            random.random()
            < 0.80,

        "items": [

            generate_media_card()

            for _ in range(
                item_count
            )
        ],
    }


# ==========================================================
# Player
# ==========================================================

def generate_player() -> dict:

    track = (
        generate_track()
    )

    return {

        "track":
            track,

        "playing":
            random.random()
            < 0.55,

        "shuffle":
            random.random()
            < 0.25,

        "repeat":
            random.random()
            < 0.20,

        "progress":
            random_progress(),

        "volume":
            round(
                random.uniform(
                    0.20,
                    1.0
                ),
                2,
            ),
    }


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> dict:

    return {

        "selected":
            "home",

        "items": [

            {
                "name":
                    "Home",

                "icon":
                    "home",

                "semantic":
                    "home",
            },

            {
                "name":
                    "Search",

                "icon":
                    "search",

                "semantic":
                    "search",
            },

            {
                "name":
                    "Your Library",

                "icon":
                    "library_music",

                "semantic":
                    "library",
            },
        ],
    }


# ==========================================================
# Home Page
# ==========================================================

def generate_home_page() -> dict:

    section_titles = (
        random.sample(
            SECTION_TITLES,
            k=random.randint(
                3,
                min(
                    6,
                    len(
                        SECTION_TITLES
                    )
                ),
            ),
        )
    )

    quick_access_count = (
        random.choice(
            [
                4,
                6,
                8,
            ]
        )
    )

    return {

        "greeting":
            random.choice(
                GREETING_OPTIONS
            ),

        "quick_access": [

            generate_quick_access_item()

            for _ in range(
                quick_access_count
            )
        ],

        "sections": [

            generate_section(
                title=title
            )

            for title in (
                section_titles
            )
        ],

        "navigation":
            generate_navigation(),

        "player":
            generate_player(),

        "profile": {

            "name":
                random.choice(
                    [
                        "Alex",
                        "Taylor",
                        "Jordan",
                        "Sam",
                        "Jamie",
                        "Morgan",
                    ]
                ),

            "avatar":
                get_random_artist_image()
                or get_random_music_cover(),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_home_page()
    )