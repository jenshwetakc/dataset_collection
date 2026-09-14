from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
)

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)


# ==========================================================
# Data Pools
# ==========================================================

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


LYRIC_LINES = [
    "City lights are fading slowly",
    "I can hear the midnight calling",
    "Every road leads somewhere new",
    "I keep thinking back to you",
    "Underneath the open sky",
    "We were learning how to fly",
    "Every moment felt like gold",
    "Stories waiting to be told",
    "Keep the windows open wide",
    "Let the evening air inside",
    "Maybe we can stay awhile",
    "Watch the distance turn to miles",
    "Nothing here can stay the same",
    "Still I remember every name",
    "Another morning starts again",
    "Sunlight falling through the rain",
    "Take the long way through the town",
    "Never let the silence down",
    "Somewhere past the city line",
    "Everything will turn out fine",
    "We were moving without plans",
    "Holding futures in our hands",
    "Time was running through the night",
    "Still the road was full of light",
]


# ==========================================================
# Helpers
# ==========================================================

def format_time(
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
# Lyrics
# ==========================================================

def generate_lyrics_lines(
    count: int,
) -> list[dict]:

    selected_lines = random.choices(
        LYRIC_LINES,
        k=count,
    )


    active_index = random.randint(
        max(
            1,
            count // 4,
        ),
        max(
            1,
            count - 4,
        ),
    )


    result = []


    for index, text in enumerate(
        selected_lines
    ):

        if index < active_index:

            state = "past"

        elif index == active_index:

            state = "active"

        else:

            state = "future"


        result.append(
            {
                "index":
                    index,

                "text":
                    text,

                "state":
                    state,
            }
        )


    return result


# ==========================================================
# Page Generator
# ==========================================================

def generate_lyrics_page() -> dict:

    duration_seconds = random.randint(
        170,
        320,
    )

    progress = random.uniform(
        0.15,
        0.85,
    )

    elapsed_seconds = int(
        duration_seconds
        * progress
    )


    return {

        # ==================================================
        # Navigation
        # ==================================================

        "navigation":
            generate_navigation(
                selected="home"
            ),


        # ==================================================
        # Track
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

            "liked":
                random.random() < 0.45,

            "duration":
                format_time(
                    duration_seconds
                ),

            "elapsed":
                format_time(
                    elapsed_seconds
                ),

            "progress":
                progress,
        },


        # ==================================================
        # Playback
        # ==================================================

        "playing":
            random.random() < 0.75,

        "shuffle":
            random.random() < 0.30,

        "repeat":
            random.random() < 0.30,


        # ==================================================
        # Lyrics
        # ==================================================

        "lyrics": generate_lyrics_lines(
            count=random.randint(
                14,
                24,
            )
        ),


        # ==================================================
        # Display
        # ==================================================

        "show_background_art":
            random.random() < 0.65,

        "show_translation":
            random.random() < 0.20,

        "fullscreen":
            True,
    }