from __future__ import annotations

import random

from social_media.canva.generators.media_generator import (
    get_random_design_thumbnail,
    get_random_photo,
)


# ==========================================================
# Pools
# ==========================================================

FILE_TYPES = [
    {
        "label": "PNG",
        "description": "High quality image",
        "icon": "image",
    },
    {
        "label": "JPG",
        "description": "Small file size image",
        "icon": "photo",
    },
    {
        "label": "PDF Standard",
        "description": "Best for documents and email",
        "icon": "picture_as_pdf",
    },
    {
        "label": "PDF Print",
        "description": "Best for professional printing",
        "icon": "print",
    },
    {
        "label": "MP4 Video",
        "description": "High quality video",
        "icon": "movie",
    },
]


PAGE_OPTIONS = [
    "All pages",
    "Current page",
    "Custom pages",
]


# ==========================================================
# Pages
# ==========================================================

def generate_pages() -> list[dict]:

    count = random.randint(
        3,
        8,
    )

    selected_count = random.randint(
        1,
        count,
    )

    selected_indices = set(
        random.sample(
            range(count),
            selected_count,
        )
    )

    return [
        {
            "number":
                index + 1,

            "selected":
                index
                in selected_indices,

            "thumbnail":
                get_random_design_thumbnail(),
        }
        for index
        in range(
            count
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_download_data() -> dict:

    selected_type = random.choice(
        FILE_TYPES
    )

    selected_page_mode = random.choice(
        PAGE_OPTIONS
    )

    quality = random.choice(
        [
            70,
            80,
            90,
            100,
        ]
    )

    size_scale = random.choice(
        [
            1,
            1.5,
            2,
            3,
        ]
    )

    return {

        "document": {
            "name":
                random.choice(
                    [
                        "Summer Campaign",
                        "Marketing Presentation",
                        "Brand Strategy",
                        "Product Launch",
                        "Social Media Kit",
                    ]
                ),

            "preview":
                get_random_photo(),
        },


        "file_types":
            FILE_TYPES,


        "selected_file_type":
            selected_type,


        "page_mode":
            selected_page_mode,


        "page_options":
            PAGE_OPTIONS,


        "pages":
            generate_pages(),


        "quality":
            quality,


        "size": {
            "scale":
                size_scale,

            "width":
                int(
                    1920
                    * size_scale
                ),

            "height":
                int(
                    1080
                    * size_scale
                ),
        },


        "options": {

            "transparent_background":
                random.random()
                < 0.35,

            "compress_file":
                random.random()
                < 0.55,

            "save_settings":
                random.random()
                < 0.40,
        },


        "estimated_size":
            random.choice(
                [
                    "1.8 MB",
                    "3.2 MB",
                    "5.6 MB",
                    "8.4 MB",
                    "12.1 MB",
                ]
            ),


        "exporting":
            random.random()
            < 0.20,


        "progress":
            random.randint(
                20,
                85,
            ),


        "actions": {

            "download":
                "Download",

            "cancel":
                "Cancel",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_download_data()
    )