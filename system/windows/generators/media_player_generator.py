from __future__ import annotations

import random

from system.windows.generators.media_generator import (
    get_random_photo,
    get_random_thumbnail,
)


# ==========================================================
# States
# ==========================================================

MEDIA_PLAYER_STATES = [
    "library",
    "albums",
    "artists",
    "search",
    "now_playing",
    "queue",
    "mini_player",
    "video_playing",
    "fullscreen_video",
    "volume_open",
    "shuffle_repeat",
    "media_error",
]


# ==========================================================
# Navigation
# ==========================================================

MEDIA_PLAYER_NAVIGATION = [
    {
        "id": "library",
        "label": "Home",
        "icon": "home",
    },
    {
        "id": "albums",
        "label": "Albums",
        "icon": "album",
    },
    {
        "id": "artists",
        "label": "Artists",
        "icon": "person",
    },
    {
        "id": "videos",
        "label": "Videos",
        "icon": "movie",
    },
    {
        "id": "playlists",
        "label": "Playlists",
        "icon": "queue_music",
    },
]


# ==========================================================
# Tracks
# ==========================================================

TRACK_POOL = [
    {
        "title": "Midnight Drive",
        "artist": "Nova Lane",
        "album": "City Lights",
        "duration": "3:42",
    },
    {
        "title": "Ocean Lines",
        "artist": "Blue Harbor",
        "album": "Coastline",
        "duration": "4:18",
    },
    {
        "title": "Parallel",
        "artist": "Echo Frame",
        "album": "Signals",
        "duration": "3:27",
    },
    {
        "title": "Cloud Nine",
        "artist": "Mira",
        "album": "Open Sky",
        "duration": "2:58",
    },
    {
        "title": "Late Evening",
        "artist": "North Avenue",
        "album": "After Hours",
        "duration": "4:05",
    },
    {
        "title": "Static Hearts",
        "artist": "Vector Bloom",
        "album": "Pulse",
        "duration": "3:51",
    },
]


# ==========================================================
# Albums
# ==========================================================

ALBUM_POOL = [
    {
        "title": "City Lights",
        "artist": "Nova Lane",
        "year": "2026",
    },
    {
        "title": "Coastline",
        "artist": "Blue Harbor",
        "year": "2025",
    },
    {
        "title": "Signals",
        "artist": "Echo Frame",
        "year": "2026",
    },
    {
        "title": "Open Sky",
        "artist": "Mira",
        "year": "2024",
    },
    {
        "title": "After Hours",
        "artist": "North Avenue",
        "year": "2025",
    },
]


# ==========================================================
# Artists
# ==========================================================

ARTIST_POOL = [
    "Nova Lane",
    "Blue Harbor",
    "Echo Frame",
    "Mira",
    "North Avenue",
    "Vector Bloom",
]


# ==========================================================
# Videos
# ==========================================================

VIDEO_POOL = [
    {
        "title": "Sample Video",
        "duration": "05:24",
    },
    {
        "title": "Travel Clip",
        "duration": "02:48",
    },
    {
        "title": "Conference Recording",
        "duration": "12:16",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_track(
    index: int,
) -> dict:

    track = random.choice(
        TRACK_POOL
    )

    return {
        "id":
            f"track_{index}",

        **track,

        "cover":
            get_random_thumbnail()
            or get_random_photo(),

        "favorite":
            random.random()
            < 0.30,

        "playing":
            False,
    }


def generate_tracks(
    minimum: int = 4,
    maximum: int = 8,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    tracks = [
        generate_track(
            index
        )
        for index in range(
            count
        )
    ]

    return tracks


def generate_albums() -> list[dict]:

    result = []

    for index, album in enumerate(
        random.sample(
            ALBUM_POOL,
            k=random.randint(
                3,
                len(
                    ALBUM_POOL
                ),
            ),
        )
    ):

        result.append(
            {
                "id":
                    f"album_{index}",

                **album,

                "cover":
                    get_random_thumbnail()
                    or get_random_photo(),

                "tracks":
                    random.randint(
                        6,
                        14,
                    ),
            }
        )

    return result


def generate_artists() -> list[dict]:

    result = []

    for index, artist in enumerate(
        random.sample(
            ARTIST_POOL,
            k=random.randint(
                3,
                len(
                    ARTIST_POOL
                ),
            ),
        )
    ):

        result.append(
            {
                "id":
                    f"artist_{index}",

                "name":
                    artist,

                "image":
                    get_random_photo(),

                "albums":
                    random.randint(
                        1,
                        6,
                    ),
            }
        )

    return result


def generate_videos() -> list[dict]:

    result = []

    for index, video in enumerate(
        VIDEO_POOL
    ):

        result.append(
            {
                "id":
                    f"video_{index}",

                **video,

                "thumbnail":
                    get_random_thumbnail()
                    or get_random_photo(),
            }
        )

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_media_player_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            MEDIA_PLAYER_STATES
        )


    if state not in MEDIA_PLAYER_STATES:

        raise ValueError(
            f"Unknown Media Player state: "
            f"{state}"
        )


    tracks = generate_tracks()

    current_track = random.choice(
        tracks
    )

    current_track[
        "playing"
    ] = state not in {
        "library",
        "albums",
        "artists",
        "search",
        "media_error",
    }


    search_query = (
        random.choice(
            [
                "city",
                "nova",
                "signals",
                "video",
                "music",
            ]
        )
        if state
        == "search"
        else ""
    )


    search_results = (
        random.sample(
            tracks,
            k=random.randint(
                2,
                min(
                    5,
                    len(
                        tracks
                    ),
                ),
            ),
        )
        if state
        == "search"
        else []
    )


    progress = random.randint(
        8,
        90,
    )


    return {
        "state":
            state,

        "navigation":
            MEDIA_PLAYER_NAVIGATION,

        "tracks":
            tracks,

        "albums":
            generate_albums(),

        "artists":
            generate_artists(),

        "videos":
            generate_videos(),

        "current_track":
            current_track,

        "queue":
            random.sample(
                tracks,
                k=random.randint(
                    3,
                    min(
                        6,
                        len(
                            tracks
                        ),
                    ),
                ),
            ),

        "search_query":
            search_query,

        "search_results":
            search_results,

        "playback": {
            "progress":
                progress,

            "current_time":
                random.choice(
                    [
                        "0:42",
                        "1:18",
                        "2:03",
                        "2:54",
                    ]
                ),

            "duration":
                current_track[
                    "duration"
                ],

            "volume":
                random.randint(
                    10,
                    100,
                ),

            "muted":
                random.random()
                < 0.15,

            "shuffle":
                state
                == "shuffle_repeat"
                or random.random()
                < 0.30,

            "repeat":
                state
                == "shuffle_repeat"
                or random.random()
                < 0.25,
        },

        "video": {
            "title":
                random.choice(
                    VIDEO_POOL
                )[
                    "title"
                ],

            "thumbnail":
                get_random_thumbnail()
                or get_random_photo(),

            "progress":
                random.randint(
                    5,
                    95,
                ),

            "current_time":
                random.choice(
                    [
                        "00:41",
                        "01:32",
                        "03:08",
                    ]
                ),

            "duration":
                random.choice(
                    [
                        "05:24",
                        "08:42",
                        "12:16",
                    ]
                ),
        },

        "error": {
            "title":
                "We can't play this file",

            "message":
                random.choice(
                    [
                        "The file may be unsupported or damaged.",
                        "The media location is no longer available.",
                        "Media Player couldn't open this item.",
                    ]
                ),
        },
    }