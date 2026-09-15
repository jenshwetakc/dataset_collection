from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_background,
    get_random_design_thumbnail,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

BRAND_STATES = [
    "overview",
    "colors",
    "fonts",
    "logos",
    "locked_premium",
]


# ==========================================================
# Color Pools
# ==========================================================

COLOR_PALETTES = [
    [
        "#0F172A",
        "#2563EB",
        "#38BDF8",
        "#F8FAFC",
        "#F97316",
    ],
    [
        "#18181B",
        "#7C3AED",
        "#EC4899",
        "#FACC15",
        "#FAFAFA",
    ],
    [
        "#052E16",
        "#16A34A",
        "#86EFAC",
        "#FEFCE8",
        "#EA580C",
    ],
    [
        "#312E81",
        "#6366F1",
        "#A5B4FC",
        "#F5F3FF",
        "#DB2777",
    ],
]


FONT_NAMES = [
    "Inter",
    "Poppins",
    "Montserrat",
    "DM Sans",
    "Playfair Display",
    "Lora",
    "Nunito Sans",
    "Roboto",
]


# ==========================================================
# Brand Colors
# ==========================================================

def generate_brand_colors() -> list[dict]:

    palette = random.choice(
        COLOR_PALETTES
    )

    return [
        {
            "value":
                color,

            "name":
                random.choice(
                    [
                        "Primary",
                        "Secondary",
                        "Accent",
                        "Surface",
                        "Highlight",
                    ]
                ),

            "selected":
                index == 0,
        }
        for index, color
        in enumerate(palette)
    ]


# ==========================================================
# Fonts
# ==========================================================

def generate_brand_fonts() -> list[dict]:

    selected = random.sample(
        FONT_NAMES,
        3,
    )

    roles = [
        "Heading",
        "Subheading",
        "Body",
    ]

    return [
        {
            "role":
                role,

            "font":
                font_name,

            "size":
                random.choice(
                    [
                        16,
                        18,
                        20,
                        24,
                        32,
                        40,
                    ]
                ),

            "weight":
                random.choice(
                    [
                        "Regular",
                        "Medium",
                        "Semi Bold",
                        "Bold",
                    ]
                ),
        }
        for role, font_name
        in zip(
            roles,
            selected,
        )
    ]


# ==========================================================
# Logos
# ==========================================================

def generate_logos() -> list[dict]:

    count = random.randint(
        4,
        8,
    )

    logos = []

    for index in range(
        count
    ):

        logos.append(
            {
                "name":
                    random.choice(
                        [
                            "Primary logo",
                            "Horizontal logo",
                            "Icon mark",
                            "White logo",
                            "Dark logo",
                            "Campaign logo",
                        ]
                    ),

                "image":
                    (
                        get_random_design_thumbnail()
                        or get_random_background()
                    ),

                "favorite":
                    random.random()
                    < 0.20,

                "selected":
                    index == 0,
            }
        )

    return logos


# ==========================================================
# Guidelines
# ==========================================================

def generate_guidelines() -> list[dict]:

    return [
        {
            "title":
                "Brand voice",

            "description":
                random.choice(
                    [
                        "Clear, confident, and approachable.",
                        "Friendly, modern, and energetic.",
                        "Professional with a human tone.",
                    ]
                ),

            "icon":
                "campaign",
        },
        {
            "title":
                "Photography",

            "description":
                random.choice(
                    [
                        "Natural lighting and authentic moments.",
                        "Bold contrast with simple compositions.",
                        "Bright editorial-style photography.",
                    ]
                ),

            "icon":
                "photo_camera",
        },
        {
            "title":
                "Visual style",

            "description":
                random.choice(
                    [
                        "Minimal layouts with generous spacing.",
                        "Bold typography and vibrant accents.",
                        "Clean grids with soft neutral surfaces.",
                    ]
                ),

            "icon":
                "palette",
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_brand_kit_data(
    forced_state: str | None = None,
) -> dict:

    if forced_state is not None:

        if forced_state not in BRAND_STATES:

            raise ValueError(
                f"Unknown brand state: "
                f"{forced_state}"
            )

        state = forced_state

    else:

        state = random.choice(
            BRAND_STATES
        )

    brand_name = random.choice(
        [
            "Nova Studio",
            "Orbit Creative",
            "Northstar",
            "Luma Labs",
            "Aster & Co.",
            "Studio Bloom",
        ]
    )

    return {

        "state":
            state,


        "brand": {

            "name":
                brand_name,

            "description":
                fake.catch_phrase(),

            "owner":
                fake.name(),

            "avatar":
                get_random_avatar(),

            "cover":
                get_random_background(),
        },


        "colors":
            generate_brand_colors(),


        "fonts":
            generate_brand_fonts(),


        "logos":
            generate_logos(),


        "guidelines":
            generate_guidelines(),


        "usage": {

            "designs":
                random.randint(
                    18,
                    240,
                ),

            "members":
                random.randint(
                    2,
                    18,
                ),

            "assets":
                random.randint(
                    12,
                    96,
                ),
        },


        "premium": {

            "title":
                "Unlock your full Brand Kit",

            "description":
                (
                    "Add unlimited logos, fonts, colors, "
                    "and brand controls for your team."
                ),

            "features": [
                "Unlimited brand palettes",
                "Upload custom fonts",
                "Brand templates",
                "Team brand controls",
            ],
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_brand_kit_data()
    )