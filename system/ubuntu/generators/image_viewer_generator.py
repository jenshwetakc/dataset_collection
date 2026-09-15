from __future__ import annotations

import random

from faker import Faker

from system.ubuntu.generators.media_generator import (
    get_random_photo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

IMAGE_VIEWER_STATES = [

    "single_image",

    "gallery_strip",

    "zoomed_in",

    "zoomed_out",

    "fit_to_window",

    "fullscreen",

    "details_open",

    "edit_mode",

    "rotate_mode",

    "crop_mode",

    "slideshow",

    "image_menu",

    "open_file_dialog",

    "delete_dialog",
]


# ==========================================================
# Image Names
# ==========================================================

IMAGE_NAMES = [

    "IMG_1024.jpg",

    "mountains.jpg",

    "sunset.png",

    "city_view.jpg",

    "vacation_01.jpg",

    "workspace.png",

    "nature.jpg",

    "street_photo.jpg",

    "portrait.jpg",

    "landscape.jpg",

    "beach.jpg",

    "architecture.png",
]


# ==========================================================
# Image Menu
# ==========================================================

IMAGE_MENU_ENTRIES = [

    {
        "label":
            "Open With",

        "icon":
            "open_in_new",
    },

    {
        "label":
            "Set as Background",

        "icon":
            "wallpaper",
    },

    {
        "label":
            "Print",

        "icon":
            "print",
    },

    {
        "label":
            "Properties",

        "icon":
            "info",
    },

    {
        "label":
            "Move to Trash",

        "icon":
            "delete",
    },
]


# ==========================================================
# Edit Tools
# ==========================================================

EDIT_TOOLS = [

    {
        "label":
            "Crop",

        "icon":
            "crop",
    },

    {
        "label":
            "Rotate",

        "icon":
            "rotate_right",
    },

    {
        "label":
            "Flip",

        "icon":
            "flip",
    },

    {
        "label":
            "Brightness",

        "icon":
            "brightness_6",
    },

    {
        "label":
            "Contrast",

        "icon":
            "contrast",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_gallery(
    minimum: int = 5,
    maximum: int = 10,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    gallery = []

    for index in range(
        count
    ):

        gallery.append(
            {
                "id":
                    index,

                "name":
                    random.choice(
                        IMAGE_NAMES
                    ),

                "src":
                    get_random_photo(),

                "selected":
                    False,

                "favorite":
                    random.random()
                    < 0.22,
            }
        )


    selected_index = random.randrange(
        len(
            gallery
        )
    )

    gallery[
        selected_index
    ][
        "selected"
    ] = True


    return gallery


# ==========================================================
# Metadata
# ==========================================================

def generate_metadata(
    image_name: str,
) -> list[dict]:

    width = random.choice(
        [
            1920,
            2560,
            3024,
            4032,
            6000,
        ]
    )

    height = random.choice(
        [
            1080,
            1440,
            2268,
            3024,
            4000,
        ]
    )


    return [

        {
            "label":
                "File",

            "value":
                image_name,

            "icon":
                "description",
        },

        {
            "label":
                "Dimensions",

            "value":
                f"{width} × {height}",

            "icon":
                "aspect_ratio",
        },

        {
            "label":
                "Size",

            "value":
                f"{random.uniform(1.2, 18.0):.1f} MB",

            "icon":
                "hard_drive",
        },

        {
            "label":
                "Type",

            "value":
                random.choice(
                    [
                        "JPEG image",
                        "PNG image",
                        "WebP image",
                    ]
                ),

            "icon":
                "image",
        },

        {
            "label":
                "Modified",

            "value":
                random.choice(
                    [
                        "Today, 14:32",
                        "Yesterday, 19:20",
                        "Sep 4, 11:05",
                        "Sep 2, 08:46",
                    ]
                ),

            "icon":
                "schedule",
        },

        {
            "label":
                "Location",

            "value":
                random.choice(
                    [
                        "~/Pictures",
                        "~/Downloads",
                        "~/Desktop",
                        "~/Pictures/Photos",
                    ]
                ),

            "icon":
                "folder",
        },
    ]


# ==========================================================
# File Dialog
# ==========================================================

def generate_file_entries() -> list[dict]:

    count = random.randint(
        6,
        10,
    )

    entries = []

    for index in range(
        count
    ):

        entries.append(
            {
                "id":
                    index,

                "name":
                    random.choice(
                        IMAGE_NAMES
                    ),

                "src":
                    get_random_photo(),

                "modified":
                    random.choice(
                        [
                            "Today",
                            "Yesterday",
                            "Sep 3",
                            "Aug 30",
                        ]
                    ),
            }
        )

    return entries


# ==========================================================
# Main
# ==========================================================

def generate_image_viewer_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            IMAGE_VIEWER_STATES
        )


    if state not in IMAGE_VIEWER_STATES:

        raise ValueError(
            f"Unknown Image Viewer state: "
            f"{state}"
        )


    gallery = generate_gallery()


    selected_image = next(
        image
        for image in gallery
        if image[
            "selected"
        ]
    )


    # ======================================================
    # Zoom
    # ======================================================

    if state == "zoomed_in":

        zoom = random.choice(
            [
                150,
                175,
                200,
                250,
            ]
        )

    elif state == "zoomed_out":

        zoom = random.choice(
            [
                35,
                50,
                67,
            ]
        )

    elif state == "fit_to_window":

        zoom = 100

    else:

        zoom = random.choice(
            [
                75,
                100,
                110,
            ]
        )


    # ======================================================
    # Crop
    # ======================================================

    crop = {

        "x":
            random.randint(
                10,
                24,
            ),

        "y":
            random.randint(
                8,
                18,
            ),

        "width":
            random.randint(
                55,
                75,
            ),

        "height":
            random.randint(
                55,
                76,
            ),
    }


    # ======================================================
    # Edit Slider
    # ======================================================

    edit_value = random.randint(
        20,
        80,
    )


    return {

        "state":
            state,

        "gallery":
            gallery,

        "selected_image":
            selected_image,

        "zoom":
            zoom,

        "metadata_entries":
            generate_metadata(
                selected_image[
                    "name"
                ]
            ),

        "image_menu_entries":
            [
                dict(
                    entry
                )
                for entry
                in IMAGE_MENU_ENTRIES
            ],

        "edit_tools":
            [
                dict(
                    entry
                )
                for entry
                in EDIT_TOOLS
            ],

        "crop":
            crop,

        "edit_value":
            edit_value,

        "rotation":
            random.choice(
                [
                    0,
                    90,
                    180,
                    270,
                ]
            ),

        "file_entries":
            generate_file_entries(),

        "slideshow_index":
            random.randint(
                1,
                len(
                    gallery
                ),
            ),

        "favorite":
            selected_image[
                "favorite"
            ],
    }