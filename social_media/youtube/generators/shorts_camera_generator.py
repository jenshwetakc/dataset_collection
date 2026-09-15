
from __future__ import annotations

import random
from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_thumbnail,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Camera States
# ==========================================================

SHORTS_CAMERA_STATES = [
    "idle",
    "recording",
    "paused",
    "countdown",
    "recorded",
    "effects_open",
]


# ==========================================================
# Utility
# ==========================================================

def format_duration(
    seconds: float,
) -> str:

    whole_seconds = int(seconds)

    minutes = (
        whole_seconds
        // 60
    )

    seconds = (
        whole_seconds
        % 60
    )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


# ==========================================================
# Camera Preview
# ==========================================================

def generate_camera_preview() -> dict[str, Any]:

    return {
        # We use a local image as a synthetic camera frame.
        "image":
            get_random_thumbnail(),

        "camera":
            random.choice(
                [
                    "front",
                    "rear",
                ]
            ),

        "flash":
            random.choice(
                [
                    "off",
                    "off",
                    "auto",
                    "on",
                ]
            ),

        "orientation":
            "portrait",
    }


# ==========================================================
# Recording Duration
# ==========================================================

def generate_duration() -> dict[str, Any]:

    max_seconds = random.choice(
        [
            15,
            30,
            60,
        ]
    )

    return {
        "max_seconds":
            max_seconds,

        "max_text":
            f"{max_seconds}s",
    }


# ==========================================================
# Recording Segments
# ==========================================================

def generate_recording_segments(
    state: str,
    max_seconds: int,
) -> dict[str, Any]:

    # ------------------------------------------------------
    # Idle / countdown have no completed segments yet.
    # ------------------------------------------------------

    if state in {
        "idle",
        "countdown",
        "effects_open",
    }:

        return {
            "segments": [],
            "recorded_seconds": 0.0,
            "recorded_percent": 0.0,
        }


    # ------------------------------------------------------
    # Generate total recorded amount.
    # ------------------------------------------------------

    total_recorded = random.uniform(
        max_seconds * 0.12,
        max_seconds * 0.85,
    )


    if state == "recorded":

        total_recorded = random.uniform(
            max_seconds * 0.55,
            max_seconds * 0.98,
        )


    segment_count = random.randint(
        1,
        4,
    )


    raw_parts = [
        random.uniform(
            0.5,
            1.5,
        )
        for _ in range(
            segment_count
        )
    ]

    raw_total = sum(
        raw_parts
    )


    segments = []

    running_seconds = 0.0


    for index, part in enumerate(
        raw_parts
    ):

        seconds = (
            total_recorded
            * part
            / raw_total
        )

        start_seconds = (
            running_seconds
        )

        end_seconds = (
            running_seconds
            + seconds
        )

        start_percent = (
            start_seconds
            / max_seconds
            * 100
        )

        width_percent = (
            seconds
            / max_seconds
            * 100
        )


        segments.append(
            {
                "id":
                    f"segment_{index}",

                "seconds":
                    round(
                        seconds,
                        2,
                    ),

                "start_percent":
                    round(
                        start_percent,
                        2,
                    ),

                "width_percent":
                    round(
                        width_percent,
                        2,
                    ),
            }
        )


        running_seconds = (
            end_seconds
        )


    recorded_percent = (
        total_recorded
        / max_seconds
        * 100
    )


    return {
        "segments":
            segments,

        "recorded_seconds":
            round(
                total_recorded,
                2,
            ),

        "recorded_text":
            format_duration(
                total_recorded
            ),

        "recorded_percent":
            round(
                recorded_percent,
                2,
            ),
    }


# ==========================================================
# Playback / Recording
# ==========================================================

def generate_recording_state(
    state: str,
) -> dict[str, Any]:

    return {
        "is_recording":
            state
            == "recording",

        "is_paused":
            state
            == "paused",

        "has_recording":
            state
            in {
                "recording",
                "paused",
                "recorded",
            },

        "record_button_icon":
            (
                "stop"
                if state == "recording"
                else None
            ),

        "record_button_label":
            (
                "Stop recording"
                if state == "recording"
                else "Start recording"
            ),
    }


# ==========================================================
# Countdown
# ==========================================================

def generate_countdown(
    state: str,
) -> dict[str, Any]:

    enabled = (
        state == "countdown"
    )

    return {
        "enabled":
            enabled,

        "number":
            (
                random.choice(
                    [
                        3,
                        2,
                        1,
                    ]
                )
                if enabled
                else None
            ),

        "label":
            (
                "Get ready"
                if enabled
                else None
            ),
    }


# ==========================================================
# Speed
# ==========================================================

def generate_speed() -> dict[str, Any]:

    selected = random.choice(
        [
            "0.3x",
            "0.5x",
            "1x",
            "1x",
            "2x",
            "3x",
        ]
    )

    return {
        "selected":
            selected,

        "options": [
            "0.3x",
            "0.5x",
            "1x",
            "2x",
            "3x",
        ],
    }


# ==========================================================
# Timer
# ==========================================================

def generate_timer() -> dict[str, Any]:

    enabled = (
        random.random()
        < 0.35
    )

    return {
        "enabled":
            enabled,

        "seconds":
            (
                random.choice(
                    [
                        3,
                        10,
                        20,
                    ]
                )
                if enabled
                else None
            ),
    }


# ==========================================================
# Sound
# ==========================================================

def generate_sound() -> dict[str, Any]:

    selected = (
        random.random()
        < 0.55
    )

    return {
        "selected":
            selected,

        "title":
            (
                random.choice(
                    [
                        "Original sound",
                        "Summer Beat",
                        "Daily Vibes",
                        "Trending Audio",
                        "City Nights",
                    ]
                )
                if selected
                else "Add sound"
            ),

        "artist":
            (
                fake.name()
                if selected
                else None
            ),
    }


# ==========================================================
# Effects
# ==========================================================

def generate_effects(
    state: str,
) -> dict[str, Any]:

    effect_names = [
        "None",
        "Glow",
        "Retro",
        "Warm",
        "Cool",
        "Dream",
        "Mono",
        "Pop",
    ]


    selected_index = (
        random.randint(
            0,
            len(effect_names) - 1,
        )
    )


    return {
        "open":
            state
            == "effects_open",

        "items": [
            {
                "id":
                    f"effect_{index}",

                "label":
                    label,

                "selected":
                    index
                    == selected_index,

                "preview":
                    get_random_thumbnail(),
            }

            for index, label in enumerate(
                effect_names
            )
        ],
    }


# ==========================================================
# Right Tool Rail
# ==========================================================

def generate_tools(
    preview: dict[str, Any],
    timer: dict[str, Any],
    speed: dict[str, Any],
) -> list[dict[str, Any]]:

    return [
        {
            "label":
                "Flip",

            "icon":
                "flip_camera_android",

            "semantic":
                "flip_camera_button",

            "value":
                preview["camera"],

            "selected":
                False,
        },

        {
            "label":
                "Speed",

            "icon":
                "speed",

            "semantic":
                "speed_button",

            "value":
                speed["selected"],

            "selected":
                speed["selected"]
                != "1x",
        },

        {
            "label":
                "Timer",

            "icon":
                "timer",

            "semantic":
                "timer_button",

            "value":
                (
                    f"{timer['seconds']}s"
                    if timer["enabled"]
                    else None
                ),

            "selected":
                timer["enabled"],
        },

        {
            "label":
                "Effects",

            "icon":
                "auto_awesome",

            "semantic":
                "effects_button",

            "value":
                None,

            "selected":
                False,
        },

        {
            "label":
                "Flash",

            "icon":
                (
                    "flash_on"
                    if preview["flash"]
                    == "on"
                    else "flash_off"
                ),

            "semantic":
                "flash_button",

            "value":
                preview["flash"],

            "selected":
                preview["flash"]
                != "off",
        },
    ]


# ==========================================================
# Top Bar
# ==========================================================

def generate_top_bar() -> dict[str, Any]:

    return {
        "show_close":
            True,

        "show_settings":
            random.random()
            < 0.45,

        "title":
            "Create a Short",
    }


# ==========================================================
# Bottom Actions
# ==========================================================

def generate_bottom_actions(
    state: str,
) -> dict[str, Any]:

    has_recording = (
        state
        in {
            "recording",
            "paused",
            "recorded",
        }
    )

    return {
        "show_gallery":
            state
            not in {
                "recording",
                "countdown",
            },

        "show_record":
            True,

        "show_undo":
            has_recording
            and state
            != "recording",

        "show_next":
            state
            in {
                "paused",
                "recorded",
            },

        "next_label":
            "Next",

        "gallery_label":
            "Gallery",
    }


# ==========================================================
# Camera Page
# ==========================================================

def generate_shorts_camera_page(
    state: str | None = None,
) -> dict[str, Any]:

    if state is None:

        state = random.choice(
            SHORTS_CAMERA_STATES
        )


    if state not in SHORTS_CAMERA_STATES:

        raise ValueError(
            f"Unknown Shorts camera state: "
            f"{state}. "
            f"Expected one of: "
            f"{SHORTS_CAMERA_STATES}"
        )


    preview = (
        generate_camera_preview()
    )


    duration = (
        generate_duration()
    )


    timer = (
        generate_timer()
    )


    speed = (
        generate_speed()
    )


    recording_segments = (
        generate_recording_segments(
            state=state,
            max_seconds=(
                duration[
                    "max_seconds"
                ]
            ),
        )
    )


    return {
        "page_type":
            "shorts_camera",

        "state":
            state,

        "preview":
            preview,

        "duration":
            duration,

        "recording":
            generate_recording_state(
                state
            ),

        "segments":
            recording_segments,

        "countdown":
            generate_countdown(
                state
            ),

        "timer":
            timer,

        "speed":
            speed,

        "sound":
            generate_sound(),

        "effects":
            generate_effects(
                state
            ),

        "tools":
            generate_tools(
                preview=preview,
                timer=timer,
                speed=speed,
            ),

        "top_bar":
            generate_top_bar(),

        "bottom_actions":
            generate_bottom_actions(
                state
            ),

        "layout": {
            "show_progress":
                True,

            "show_sound":
                state
                not in {
                    "recording",
                    "countdown",
                },

            "show_tools":
                state
                != "countdown",

            "show_effects_panel":
                state
                == "effects_open",

            "show_countdown":
                state
                == "countdown",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE SHORTS CAMERA"
    )

    print(
        "=========================================="
    )


    for state in SHORTS_CAMERA_STATES:

        page = (
            generate_shorts_camera_page(
                state=state
            )
        )


        print(
            "\n"
            "------------------------------------------"
        )

        print(
            "State:",
            page["state"]
        )

        print(
            "Camera:",
            page["preview"]["camera"]
        )

        print(
            "Duration:",
            page["duration"]["max_text"]
        )

        print(
            "Recorded:",
            page["segments"].get(
                "recorded_text",
                "0:00",
            )
        )

        print(
            "Segments:",
            len(
                page["segments"][
                    "segments"
                ]
            )
        )

        print(
            "Recording:",
            page["recording"][
                "is_recording"
            ]
        )

        print(
            "Countdown:",
            page["countdown"][
                "enabled"
            ]
        )

        print(
            "Effects open:",
            page["effects"][
                "open"
            ]
        )

        print(
            "Sound:",
            page["sound"][
                "title"
            ]
        )