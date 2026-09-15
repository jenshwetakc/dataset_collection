from __future__ import annotations

import random

from system.windows.generators.media_generator import (
    get_random_photo,
)


# ==========================================================
# States
# ==========================================================

PAINT_STATES = [
    "blank_canvas",
    "drawing",
    "text_tool",
    "shape_tool",
    "selection",
    "crop",
    "color_picker",
    "eraser",
    "image_open",
    "resize_dialog",
    "save_dialog",
    "unsaved_close_dialog",
]


# ==========================================================
# Tools
# ==========================================================

PAINT_TOOLS = [
    {
        "id": "select",
        "label": "Select",
        "icon": "select_all",
    },
    {
        "id": "crop",
        "label": "Crop",
        "icon": "crop",
    },
    {
        "id": "resize",
        "label": "Resize",
        "icon": "aspect_ratio",
    },
    {
        "id": "rotate",
        "label": "Rotate",
        "icon": "rotate_right",
    },
    {
        "id": "brush",
        "label": "Brushes",
        "icon": "brush",
    },
    {
        "id": "eraser",
        "label": "Eraser",
        "icon": "ink_eraser",
    },
    {
        "id": "fill",
        "label": "Fill",
        "icon": "format_color_fill",
    },
    {
        "id": "text",
        "label": "Text",
        "icon": "text_fields",
    },
    {
        "id": "picker",
        "label": "Color picker",
        "icon": "colorize",
    },
]


# ==========================================================
# Shapes
# ==========================================================

SHAPES = [
    "rectangle",
    "circle",
    "line",
    "arrow_right_alt",
    "star",
    "favorite",
]


# ==========================================================
# Colors
# ==========================================================

PALETTE = [
    "#000000",
    "#FFFFFF",
    "#808080",
    "#C00000",
    "#FF0000",
    "#FF8000",
    "#FFFF00",
    "#00B050",
    "#00B0F0",
    "#0070C0",
    "#7030A0",
    "#FF66CC",
]


# ==========================================================
# Helpers
# ==========================================================

def choose_active_tool(
    state: str,
) -> str:

    mapping = {
        "drawing":
            "brush",

        "text_tool":
            "text",

        "shape_tool":
            "shape",

        "selection":
            "select",

        "crop":
            "crop",

        "color_picker":
            "picker",

        "eraser":
            "eraser",
    }

    return mapping.get(
        state,
        "brush",
    )


def generate_canvas_marks(
    state: str,
) -> list[dict]:

    marks = []


    if state == "drawing":

        for _ in range(
            random.randint(
                2,
                5,
            )
        ):

            marks.append(
                {
                    "type":
                        "stroke",

                    "x":
                        random.randint(
                            60,
                            520,
                        ),

                    "y":
                        random.randint(
                            60,
                            340,
                        ),

                    "width":
                        random.randint(
                            60,
                            220,
                        ),

                    "height":
                        random.randint(
                            12,
                            40,
                        ),

                    "rotation":
                        random.randint(
                            -18,
                            18,
                        ),

                    "color":
                        random.choice(
                            PALETTE[3:]
                        ),
                }
            )


    elif state == "shape_tool":

        marks.append(
            {
                "type":
                    "shape",

                "shape":
                    random.choice(
                        [
                            "rectangle",
                            "circle",
                        ]
                    ),

                "x":
                    random.randint(
                        120,
                        320,
                    ),

                "y":
                    random.randint(
                        90,
                        220,
                    ),

                "width":
                    random.randint(
                        160,
                        260,
                    ),

                "height":
                    random.randint(
                        100,
                        200,
                    ),

                "color":
                    random.choice(
                        PALETTE[3:]
                    ),
            }
        )


    elif state == "text_tool":

        marks.append(
            {
                "type":
                    "text",

                "x":
                    random.randint(
                        120,
                        260,
                    ),

                "y":
                    random.randint(
                        120,
                        230,
                    ),

                "text":
                    random.choice(
                        [
                            "Synthetic UI",
                            "Research Notes",
                            "Windows Paint",
                            "Dataset Sample",
                        ]
                    ),

                "color":
                    random.choice(
                        PALETTE
                    ),
            }
        )


    return marks


# ==========================================================
# Main Generator
# ==========================================================

def generate_paint_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            PAINT_STATES
        )


    if state not in PAINT_STATES:

        raise ValueError(
            f"Unknown Paint state: "
            f"{state}"
        )


    image_src = None


    if state in {
        "image_open",
        "selection",
        "crop",
        "resize_dialog",
        "save_dialog",
        "unsaved_close_dialog",
    }:

        image_src = get_random_photo()


    return {
        "state":
            state,

        "tools":
            PAINT_TOOLS,

        "active_tool":
            choose_active_tool(
                state
            ),

        "shapes":
            SHAPES,

        "palette":
            PALETTE,

        "primary_color":
            random.choice(
                PALETTE
            ),

        "secondary_color":
            random.choice(
                PALETTE
            ),

        "canvas": {
            "width":
                random.choice(
                    [
                        800,
                        1024,
                        1200,
                    ]
                ),

            "height":
                random.choice(
                    [
                        600,
                        768,
                        900,
                    ]
                ),

            "zoom":
                random.choice(
                    [
                        75,
                        100,
                        125,
                        150,
                    ]
                ),

            "image":
                image_src,

            "marks":
                generate_canvas_marks(
                    state
                ),
        },

        "selection": {
            "x":
                random.randint(
                    120,
                    260,
                ),

            "y":
                random.randint(
                    90,
                    180,
                ),

            "width":
                random.randint(
                    180,
                    320,
                ),

            "height":
                random.randint(
                    120,
                    240,
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
                    150,
                ),

            "width":
                random.randint(
                    280,
                    440,
                ),

            "height":
                random.randint(
                    200,
                    320,
                ),
        },

        "resize": {
            "width":
                random.choice(
                    [
                        640,
                        800,
                        1024,
                        1280,
                    ]
                ),

            "height":
                random.choice(
                    [
                        480,
                        600,
                        768,
                        960,
                    ]
                ),

            "maintain_aspect":
                random.random()
                < 0.75,
        },

        "save": {
            "filename":
                random.choice(
                    [
                        "drawing.png",
                        "image_edit.png",
                        "paint_sample.jpg",
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
                        "BMP",
                    ]
                ),
        },
    }