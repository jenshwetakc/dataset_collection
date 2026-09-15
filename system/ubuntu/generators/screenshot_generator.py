from __future__ import annotations

import random

from system.ubuntu.generators.media_generator import (
    get_random_photo,
)


# ==========================================================
# States
# ==========================================================

SCREENSHOT_STATES = [

    "screen_mode",

    "window_mode",

    "area_mode",

    "area_selected",

    "window_selected",

    "delay_menu",

    "options_open",

    "capture_countdown",

    "capture_preview",

    "recording_ready",

    "recording_active",

    "save_dialog",
]


# ==========================================================
# Modes
# ==========================================================

CAPTURE_MODES = [

    {
        "name":
            "Screen",

        "semantic":
            "screen",

        "icon":
            "desktop_windows",
    },

    {
        "name":
            "Window",

        "semantic":
            "window",

        "icon":
            "select_window",
    },

    {
        "name":
            "Selection",

        "semantic":
            "area",

        "icon":
            "crop_free",
    },
]


# ==========================================================
# Windows
# ==========================================================

WINDOWS = [

    {
        "title":
            "Files",

        "icon":
            "folder",

        "x":
            17,

        "y":
            18,

        "width":
            42,

        "height":
            58,
    },

    {
        "title":
            "Terminal",

        "icon":
            "terminal",

        "x":
            44,

        "y":
            28,

        "width":
            39,

        "height":
            48,
    },

    {
        "title":
            "Text Editor",

        "icon":
            "edit_note",

        "x":
            28,

        "y":
            14,

        "width":
            48,

        "height":
            67,
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_selection() -> dict:

    width = random.randint(
        34,
        62,
    )

    height = random.randint(
        30,
        58,
    )

    x = random.randint(
        8,
        90 - width,
    )

    y = random.randint(
        10,
        88 - height,
    )


    return {

        "x":
            x,

        "y":
            y,

        "width":
            width,

        "height":
            height,
    }


def generate_windows() -> list[dict]:

    entries = [

        dict(
            window
        )

        for window in WINDOWS
    ]


    random.shuffle(
        entries
    )


    selected_index = random.randrange(
        len(
            entries
        )
    )


    for index, entry in enumerate(
        entries
    ):

        entry[
            "selected"
        ] = (
            index
            == selected_index
        )


    return entries


# ==========================================================
# Main
# ==========================================================

def generate_screenshot_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SCREENSHOT_STATES
        )


    if state not in SCREENSHOT_STATES:

        raise ValueError(
            f"Unknown Screenshot state: "
            f"{state}"
        )


    # ======================================================
    # Mode
    # ======================================================

    if state in {
        "window_mode",
        "window_selected",
    }:

        mode = "window"

    elif state in {
        "area_mode",
        "area_selected",
    }:

        mode = "area"

    else:

        mode = "screen"


    # ======================================================
    # Recording
    # ======================================================

    recording = state in {
        "recording_ready",
        "recording_active",
    }


    # ======================================================
    # Delay
    # ======================================================

    delay = random.choice(
        [
            0,
            3,
            5,
            10,
        ]
    )


    # ======================================================
    # Countdown
    # ======================================================

    countdown = random.choice(
        [
            1,
            2,
            3,
        ]
    )


    return {

        "state":
            state,

        "mode":
            mode,

        "recording":
            recording,

        "capture_modes":
            [
                dict(
                    entry
                )
                for entry
                in CAPTURE_MODES
            ],

        "selection":
            generate_selection(),

        "windows":
            generate_windows(),

        "delay":
            delay,

        "countdown":
            countdown,

        "include_pointer":
            random.random()
            < 0.55,

        "include_border":
            random.random()
            < 0.65,

        "record_audio":
            random.random()
            < 0.45,

        "recording_seconds":
            random.randint(
                3,
                240,
            ),

        "preview_image":
            get_random_photo(),

        "filename":
            random.choice(
                [
                    "Screenshot from 2026-09-05.png",
                    "Screenshot_2026-09-05_2146.png",
                    "screen-capture.png",
                    "desktop-screenshot.png",
                ]
            ),
    }