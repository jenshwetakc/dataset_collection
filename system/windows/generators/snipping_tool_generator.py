from __future__ import annotations

import random

from system.windows.generators.media_generator import (
    get_random_photo,
)


# ==========================================================
# States
# ==========================================================

SNIPPING_TOOL_STATES = [
    "capture_ready",
    "rectangle_snip",
    "window_snip",
    "fullscreen_snip",
    "captured_image",
    "markup",
    "crop",
    "screen_record",
    "recording",
    "delay_menu",
    "settings",
    "save_dialog",
]


# ==========================================================
# Capture Modes
# ==========================================================

CAPTURE_MODES = [
    {
        "id": "rectangle",
        "label": "Rectangle",
        "icon": "crop_square",
    },
    {
        "id": "window",
        "label": "Window",
        "icon": "window",
    },
    {
        "id": "fullscreen",
        "label": "Full screen",
        "icon": "fullscreen",
    },
    {
        "id": "freeform",
        "label": "Freeform",
        "icon": "gesture",
    },
]


# ==========================================================
# Markup Tools
# ==========================================================

MARKUP_TOOLS = [
    {
        "id": "pen",
        "label": "Pen",
        "icon": "edit",
    },
    {
        "id": "highlighter",
        "label": "Highlighter",
        "icon": "border_color",
    },
    {
        "id": "eraser",
        "label": "Eraser",
        "icon": "ink_eraser",
    },
    {
        "id": "ruler",
        "label": "Ruler",
        "icon": "straighten",
    },
    {
        "id": "crop",
        "label": "Crop",
        "icon": "crop",
    },
]


# ==========================================================
# Delay Options
# ==========================================================

DELAY_OPTIONS = [
    "No delay",
    "3 seconds",
    "5 seconds",
    "10 seconds",
]


# ==========================================================
# Helpers
# ==========================================================

def choose_mode(
    state: str,
) -> str:

    mapping = {
        "rectangle_snip":
            "rectangle",

        "window_snip":
            "window",

        "fullscreen_snip":
            "fullscreen",
    }

    return mapping.get(
        state,
        random.choice(
            CAPTURE_MODES
        )["id"],
    )


def generate_selection() -> dict:

    return {
        "x":
            random.randint(
                140,
                340,
            ),

        "y":
            random.randint(
                90,
                220,
            ),

        "width":
            random.randint(
                380,
                700,
            ),

        "height":
            random.randint(
                240,
                480,
            ),
    }


def generate_markup_marks() -> list[dict]:

    marks = []

    for _ in range(
        random.randint(
            2,
            5,
        )
    ):

        marks.append(
            {
                "x":
                    random.randint(
                        100,
                        620,
                    ),

                "y":
                    random.randint(
                        80,
                        380,
                    ),

                "width":
                    random.randint(
                        60,
                        220,
                    ),

                "height":
                    random.randint(
                        5,
                        14,
                    ),

                "rotation":
                    random.randint(
                        -18,
                        18,
                    ),

                "kind":
                    random.choice(
                        [
                            "pen",
                            "highlighter",
                        ]
                    ),
            }
        )

    return marks


# ==========================================================
# Main Generator
# ==========================================================

def generate_snipping_tool_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SNIPPING_TOOL_STATES
        )


    if state not in SNIPPING_TOOL_STATES:

        raise ValueError(
            f"Unknown Snipping Tool state: "
            f"{state}"
        )


    image = None


    if state in {
        "captured_image",
        "markup",
        "crop",
        "save_dialog",
    }:

        image = get_random_photo()


    return {
        "state":
            state,

        "capture_modes":
            CAPTURE_MODES,

        "selected_mode":
            choose_mode(
                state
            ),

        "markup_tools":
            MARKUP_TOOLS,

        "delay":
            random.choice(
                DELAY_OPTIONS
            ),

        "delay_options":
            DELAY_OPTIONS,

        "selection":
            generate_selection(),

        "capture": {
            "image":
                image,

            "width":
                random.choice(
                    [
                        1280,
                        1440,
                        1920,
                    ]
                ),

            "height":
                random.choice(
                    [
                        720,
                        900,
                        1080,
                    ]
                ),

            "filename":
                random.choice(
                    [
                        "Screenshot 2026-09-05 221500.png",
                        "Screenshot 2026-09-05 222018.png",
                        "Snip_2026-09-05.png",
                    ]
                ),
        },

        "markup": {
            "active_tool":
                random.choice(
                    [
                        "pen",
                        "highlighter",
                        "eraser",
                    ]
                ),

            "marks":
                generate_markup_marks(),

            "thickness":
                random.randint(
                    2,
                    8,
                ),
        },

        "crop": {
            "x":
                random.randint(
                    80,
                    180,
                ),

            "y":
                random.randint(
                    70,
                    160,
                ),

            "width":
                random.randint(
                    420,
                    700,
                ),

            "height":
                random.randint(
                    280,
                    480,
                ),
        },

        "recording": {
            "duration":
                random.choice(
                    [
                        "00:08",
                        "00:17",
                        "00:35",
                        "01:12",
                    ]
                ),

            "audio":
                random.random()
                < 0.65,

            "microphone":
                random.random()
                < 0.55,
        },

        "settings": {
            "auto_save":
                random.random()
                < 0.75,

            "clipboard":
                random.random()
                < 0.90,

            "multiple_windows":
                random.random()
                < 0.35,

            "border":
                random.random()
                < 0.55,
        },

        "save": {
            "filename":
                random.choice(
                    [
                        "Screenshot.png",
                        "Snip.png",
                        "Capture.png",
                    ]
                ),

            "folder":
                random.choice(
                    [
                        "Pictures",
                        "Desktop",
                        "Documents",
                    ]
                ),

            "format":
                random.choice(
                    [
                        "PNG",
                        "JPEG",
                    ]
                ),
        },
    }