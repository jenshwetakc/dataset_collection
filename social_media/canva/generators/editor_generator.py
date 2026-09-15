from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_design_thumbnail,
    get_random_illustration,
    get_random_photo,
    get_random_template_image,
)


fake = Faker()


# ==========================================================
# Tool Rail
# ==========================================================

TOOL_ITEMS = [
    {
        "label": "Design",
        "icon": "dashboard_customize",
        "panel": "design",
    },
    {
        "label": "Elements",
        "icon": "shapes",
        "panel": "elements",
    },
    {
        "label": "Text",
        "icon": "title",
        "panel": "text",
    },
    {
        "label": "Brand",
        "icon": "diamond",
        "panel": "brand",
    },
    {
        "label": "Uploads",
        "icon": "cloud_upload",
        "panel": "uploads",
    },
    {
        "label": "Draw",
        "icon": "draw",
        "panel": "draw",
    },
    {
        "label": "Projects",
        "icon": "folder",
        "panel": "projects",
    },
]


ELEMENT_CATEGORIES = [
    {
        "label": "Shapes",
        "icon": "category",
    },
    {
        "label": "Graphics",
        "icon": "interests",
    },
    {
        "label": "Photos",
        "icon": "photo",
    },
    {
        "label": "Videos",
        "icon": "movie",
    },
    {
        "label": "Charts",
        "icon": "bar_chart",
    },
    {
        "label": "Frames",
        "icon": "crop_free",
    },
]


FONT_OPTIONS = [
    "Arial",
    "Montserrat",
    "Open Sans",
    "Roboto",
    "Poppins",
    "Playfair Display",
    "Lato",
    "Nunito",
]


DOCUMENT_NAMES = [
    "Summer Campaign",
    "Marketing Presentation",
    "Product Launch",
    "Creative Portfolio",
    "Company Proposal",
    "Social Media Kit",
    "Brand Presentation",
    "Quarterly Review",
]


CANVAS_HEADLINES = [
    "Create something amazing",
    "Design your next big idea",
    "Ideas worth sharing",
    "Make your story stand out",
    "Bring your vision to life",
    "Create. Share. Inspire.",
]


CANVAS_SUBTITLES = [
    "Simple ideas can make a big impact.",
    "Turn your ideas into beautiful visual stories.",
    "Designed for people who love creating.",
    "A fresh way to present your next idea.",
    "Make every moment look remarkable.",
]


# ==========================================================
# Tool Rail Generator
# ==========================================================

def generate_tools() -> list[dict]:

    selected_index = random.randrange(
        len(
            TOOL_ITEMS
        )
    )

    return [
        {
            **item,
            "selected":
                index
                == selected_index,
        }
        for index, item
        in enumerate(
            TOOL_ITEMS
        )
    ]


# ==========================================================
# Template Cards
# ==========================================================

def generate_template_cards(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            8,
            14,
        )

    cards = []

    for index in range(
        count
    ):

        cards.append(
            {
                "id":
                    index,

                "title":
                    random.choice(
                        [
                            "Modern",
                            "Minimal",
                            "Creative",
                            "Professional",
                            "Bold",
                            "Elegant",
                            "Bright",
                            "Simple",
                        ]
                    )
                    + " "
                    + random.choice(
                        [
                            "Presentation",
                            "Poster",
                            "Campaign",
                            "Story",
                            "Design",
                            "Layout",
                        ]
                    ),

                "image":
                    get_random_template_image(),

                "premium":
                    random.random()
                    < 0.18,
            }
        )

    return cards


# ==========================================================
# Element Cards
# ==========================================================

def generate_elements(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            8,
            16,
        )

    items = []

    for index in range(
        count
    ):

        element_type = random.choice(
            [
                "photo",
                "illustration",
                "shape",
            ]
        )

        if element_type == "photo":

            image = get_random_photo()

        elif element_type == "illustration":

            image = get_random_illustration()

        else:

            image = None

        items.append(
            {
                "id":
                    index,

                "type":
                    element_type,

                "image":
                    image,

                "shape":
                    random.choice(
                        [
                            "circle",
                            "square",
                            "triangle",
                            "star",
                        ]
                    ),
            }
        )

    return items


# ==========================================================
# Pages
# ==========================================================

def generate_pages() -> list[dict]:

    page_count = random.randint(
        2,
        5,
    )

    return [
        {
            "number":
                index + 1,

            "selected":
                index == 0,

            "thumbnail":
                get_random_design_thumbnail(),
        }
        for index
        in range(
            page_count
        )
    ]


# ==========================================================
# Main Editor Generator
# ==========================================================

def generate_editor_data() -> dict:

    selected_tool = random.choice(
        [
            "design",
            "elements",
            "text",
        ]
    )

    tools = []

    for item in TOOL_ITEMS:

        tools.append(
            {
                **item,
                "selected":
                    item["panel"]
                    == selected_tool,
            }
        )

    headline = random.choice(
        CANVAS_HEADLINES
    )

    subtitle = random.choice(
        CANVAS_SUBTITLES
    )

    return {

        "document": {

            "name":
                random.choice(
                    DOCUMENT_NAMES
                ),

            "saved":
                random.random()
                < 0.85,
        },


        "user": {

            "name":
                fake.name(),

            "avatar":
                get_random_avatar(),
        },


        "tools":
            tools,


        "active_panel":
            selected_tool,


        "search": {

            "placeholder":
                random.choice(
                    [
                        "Search templates",
                        "Search elements",
                        "Search Canva",
                        "Search graphics and photos",
                    ]
                ),
        },


        "categories":
            ELEMENT_CATEGORIES,


        "templates":
            generate_template_cards(),


        "elements":
            generate_elements(),


        "text_panel": {

            "font":
                random.choice(
                    FONT_OPTIONS
                ),

            "size":
                random.choice(
                    [
                        18,
                        24,
                        28,
                        32,
                        40,
                        48,
                    ]
                ),

            "alignment":
                random.choice(
                    [
                        "format_align_left",
                        "format_align_center",
                        "format_align_right",
                    ]
                ),
        },


        "canvas": {

            "headline":
                headline,

            "subtitle":
                subtitle,

            "background":
                get_random_template_image(),

            "photo":
                get_random_photo(),

            "accent_text":
                random.choice(
                    [
                        "EXPLORE",
                        "CREATE",
                        "INSPIRE",
                        "DESIGN",
                        "DISCOVER",
                    ]
                ),
        },


        "pages":
            generate_pages(),


        "zoom":
            random.choice(
                [
                    40,
                    50,
                    60,
                    75,
                    85,
                ]
            ),


        "toolbar": {

            "font":
                random.choice(
                    FONT_OPTIONS
                ),

            "font_size":
                random.choice(
                    [
                        18,
                        24,
                        28,
                        32,
                        40,
                    ]
                ),

            "bold":
                random.random()
                < 0.45,

            "italic":
                random.random()
                < 0.25,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_editor_data()
    )