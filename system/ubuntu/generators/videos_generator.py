from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

VIDEO_STATES = [

    "library",

    "playing",

    "paused",

    "buffering",

    "playlist_open",

    "subtitles_menu",

    "playback_menu",

    "volume_open",

    "fullscreen",

    "video_info",

    "open_media_dialog",

    "end_screen",
]


# ==========================================================
# Video Titles
# ==========================================================

VIDEO_TITLES = [

    "Mountain Journey",

    "City Walk",

    "Ocean Waves",

    "Project Demo",

    "Conference Talk",

    "Travel Memories",

    "Nature Documentary",

    "Tutorial Recording",

    "Presentation Demo",

    "Campus Tour",

    "Night Drive",

    "Wildlife Highlights",
]


# ==========================================================
# Subtitle Options
# ==========================================================

SUBTITLE_OPTIONS = [

    "Off",

    "English",

    "English (CC)",

    "Korean",

    "Japanese",

    "Auto-generated",
]


# ==========================================================
# Playback Speeds
# ==========================================================

PLAYBACK_SPEEDS = [

    "0.5×",

    "0.75×",

    "1.0×",

    "1.25×",

    "1.5×",

    "1.75×",

    "2.0×",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_duration() -> int:

    return random.randint(
        180,
        7200,
    )


def format_duration(
    seconds: int,
) -> str:

    hours = seconds // 3600

    minutes = (
        seconds % 3600
    ) // 60

    secs = seconds % 60


    if hours:

        return (
            f"{hours}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )

    return (
        f"{minutes}:"
        f"{secs:02d}"
    )


def generate_video(
    index: int,
) -> dict:

    duration = (
        generate_duration()
    )

    progress = random.randint(
        0,
        duration
    )


    return {

        "id":
            index,

        "title":
            random.choice(
                VIDEO_TITLES
            ),

        "duration":
            duration,

        "duration_text":
            format_duration(
                duration
            ),

        "progress":
            progress,

        "progress_text":
            format_duration(
                progress
            ),

        "progress_percent":
            int(
                progress
                / duration
                * 100
            ),

        "resolution":
            random.choice(
                [
                    "720p",
                    "1080p",
                    "1440p",
                    "4K",
                ]
            ),

        "favorite":
            random.random()
            < 0.25,

        "selected":
            False,
    }


def generate_library() -> list[dict]:

    count = random.randint(
        6,
        12,
    )

    entries = [

        generate_video(
            index
        )

        for index in range(
            count
        )
    ]


    selected_index = random.randrange(
        len(
            entries
        )
    )

    entries[
        selected_index
    ][
        "selected"
    ] = True


    return entries


# ==========================================================
# Main
# ==========================================================

def generate_videos_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            VIDEO_STATES
        )


    if state not in VIDEO_STATES:

        raise ValueError(
            f"Unknown Videos state: "
            f"{state}"
        )


    library = (
        generate_library()
    )


    selected_video = next(
        video
        for video in library
        if video[
            "selected"
        ]
    )


    # ======================================================
    # Playback State
    # ======================================================

    playing = state in {
        "playing",
        "fullscreen",
        "playlist_open",
        "subtitles_menu",
        "playback_menu",
        "volume_open",
        "video_info",
    }


    paused = (
        state
        == "paused"
    )


    buffering = (
        state
        == "buffering"
    )


    # ======================================================
    # Playback Values
    # ======================================================

    volume = random.randint(
        15,
        100,
    )


    playback_speed = random.choice(
        PLAYBACK_SPEEDS
    )


    subtitle = random.choice(
        SUBTITLE_OPTIONS
    )


    # ======================================================
    # Video Info
    # ======================================================

    info_entries = [

        {
            "label":
                "Title",

            "value":
                selected_video[
                    "title"
                ],

            "icon":
                "movie",
        },

        {
            "label":
                "Duration",

            "value":
                selected_video[
                    "duration_text"
                ],

            "icon":
                "schedule",
        },

        {
            "label":
                "Resolution",

            "value":
                selected_video[
                    "resolution"
                ],

            "icon":
                "high_quality",
        },

        {
            "label":
                "File Type",

            "value":
                random.choice(
                    [
                        "MP4 Video",
                        "WebM Video",
                        "MKV Video",
                    ]
                ),

            "icon":
                "description",
        },

        {
            "label":
                "Location",

            "value":
                random.choice(
                    [
                        "~/Videos",
                        "~/Downloads",
                        "~/Desktop",
                    ]
                ),

            "icon":
                "folder",
        },
    ]


    return {

        "state":
            state,

        "library":
            library,

        "selected_video":
            selected_video,

        "playing":
            playing,

        "paused":
            paused,

        "buffering":
            buffering,

        "volume":
            volume,

        "playback_speed":
            playback_speed,

        "subtitle":
            subtitle,

        "subtitle_options":
            SUBTITLE_OPTIONS.copy(),

        "playback_speeds":
            PLAYBACK_SPEEDS.copy(),

        "info_entries":
            info_entries,

        "autoplay":
            random.random()
            < 0.6,

        "repeat":
            random.random()
            < 0.25,
    }