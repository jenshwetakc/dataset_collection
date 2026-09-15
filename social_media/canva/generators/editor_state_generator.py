from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_design_thumbnail,
    get_random_photo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

EDITOR_STATES = [
    "comments",
    "layers",
    "color_picker",
    "image_edit",
    "present",
]


# ==========================================================
# Tool Rail
# ==========================================================

TOOLS = [
    {
        "label": "Design",
        "icon": "dashboard_customize",
    },
    {
        "label": "Elements",
        "icon": "shapes",
    },
    {
        "label": "Text",
        "icon": "title",
    },
    {
        "label": "Uploads",
        "icon": "cloud_upload",
    },
    {
        "label": "Draw",
        "icon": "draw",
    },
]


# ==========================================================
# Comments
# ==========================================================

def generate_comments() -> list[dict]:

    count = random.randint(
        3,
        6,
    )

    comments = []

    for index in range(count):

        comments.append(
            {
                "id":
                    index,

                "name":
                    fake.name(),

                "avatar":
                    get_random_avatar(),

                "time":
                    random.choice(
                        [
                            "Just now",
                            "3m",
                            "12m",
                            "1h",
                            "Yesterday",
                        ]
                    ),

                "text":
                    random.choice(
                        [
                            "Can we make this title slightly larger?",
                            "I like this version.",
                            "Maybe use another photo here.",
                            "Let's keep the spacing consistent.",
                            "Could we try a lighter background?",
                            "This section looks great.",
                        ]
                    ),

                "resolved":
                    random.random()
                    < 0.15,
            }
        )

    return comments


# ==========================================================
# Layers
# ==========================================================

def generate_layers() -> list[dict]:

    base_layers = [
        {
            "name": "Headline",
            "icon": "title",
            "type": "text",
        },
        {
            "name": "Subtitle",
            "icon": "subject",
            "type": "text",
        },
        {
            "name": "Portrait photo",
            "icon": "image",
            "type": "image",
        },
        {
            "name": "Accent shape",
            "icon": "shapes",
            "type": "shape",
        },
        {
            "name": "Background",
            "icon": "wallpaper",
            "type": "background",
        },
    ]

    selected_index = random.randrange(
        len(base_layers)
    )

    return [
        {
            **item,

            "selected":
                index == selected_index,

            "visible":
                random.random() > 0.12,

            "locked":
                random.random() < 0.20,
        }
        for index, item
        in enumerate(base_layers)
    ]


# ==========================================================
# Colors
# ==========================================================

def generate_colors() -> list[dict]:

    colors = [
        "#111827",
        "#FFFFFF",
        "#FF6B6B",
        "#FFD166",
        "#06D6A0",
        "#118AB2",
        "#7C3AED",
        "#EC4899",
        "#F97316",
        "#64748B",
        "#2563EB",
        "#16A34A",
    ]

    selected = random.choice(
        colors
    )

    return [
        {
            "value":
                color,

            "selected":
                color == selected,
        }
        for color
        in colors
    ]


# ==========================================================
# Image Adjustments
# ==========================================================

def generate_image_adjustments() -> list[dict]:

    return [
        {
            "label": "Brightness",
            "semantic": "brightness",
            "value": random.randint(
                25,
                85,
            ),
        },
        {
            "label": "Contrast",
            "semantic": "contrast",
            "value": random.randint(
                25,
                85,
            ),
        },
        {
            "label": "Saturation",
            "semantic": "saturation",
            "value": random.randint(
                25,
                85,
            ),
        },
        {
            "label": "Warmth",
            "semantic": "warmth",
            "value": random.randint(
                25,
                85,
            ),
        },
    ]


# ==========================================================
# Pages
# ==========================================================

def generate_pages() -> list[dict]:

    count = random.randint(
        3,
        6,
    )

    return [
        {
            "number":
                index + 1,

            "selected":
                index == 0,

            "image":
                get_random_design_thumbnail(),
        }
        for index in range(count)
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_editor_state_data(
    forced_state: str | None = None,
) -> dict:

    if forced_state is not None:

        if forced_state not in EDITOR_STATES:

            raise ValueError(
                f"Unknown editor state: "
                f"{forced_state}"
            )

        state = forced_state

    else:

        state = random.choice(
            EDITOR_STATES
        )

    return {

        "state":
            state,


        "document": {

            "name":
                random.choice(
                    [
                        "Summer Campaign",
                        "Product Launch",
                        "Brand Presentation",
                        "Marketing Strategy",
                        "Creative Portfolio",
                    ]
                ),
        },


        "canvas": {

            "image":
                get_random_photo(),

            "headline":
                random.choice(
                    [
                        "Design your next idea",
                        "Make something remarkable",
                        "Create with confidence",
                        "Ideas worth sharing",
                        "Bring your vision to life",
                    ]
                ),

            "subtitle":
                random.choice(
                    [
                        "Turn simple ideas into powerful stories.",
                        "Create beautiful content for every moment.",
                        "Great ideas deserve great design.",
                    ]
                ),
        },


        "tools":
            TOOLS,


        "comments":
            generate_comments(),


        "layers":
            generate_layers(),


        "colors":
            generate_colors(),


        "adjustments":
            generate_image_adjustments(),


        "pages":
            generate_pages(),


        "zoom":
            random.choice(
                [
                    50,
                    60,
                    75,
                    85,
                ]
            ),


        "present": {

            "page":
                random.randint(
                    1,
                    4,
                ),

            "total":
                random.randint(
                    4,
                    8,
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_editor_state_data()
    )