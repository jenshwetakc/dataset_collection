from __future__ import annotations

import random

from system.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
    image_to_data_uri,
)


# ==========================================================
# Ubuntu Assets
# ==========================================================
#
# UBUNTU_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "ubuntu"
# )


WALLPAPER_DIR = (
    ASSETS_ROOT
    / "backgrounds"
)


PHOTO_DIR = (
    ASSETS_ROOT
    / "photos"
)


AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)


DOCUMENT_PREVIEW_DIR = (
    ASSETS_ROOT
    / "documents"
)


# ==========================================================
# Random Wallpaper
# ==========================================================

def get_random_wallpaper():

    return get_random_image(
        WALLPAPER_DIR
    )


# ==========================================================
# Wallpaper Gallery
# ==========================================================

def get_wallpaper_gallery(
    count: int = 8,
) -> list[str]:

    files = list(
        get_image_files(
            str(
                WALLPAPER_DIR
            )
        )
    )

    if not files:

        return []


    selected = random.sample(

        files,

        k=min(
            count,
            len(
                files
            ),
        ),
    )


    return [

        image_to_data_uri(
            file
        )

        for file in selected
    ]


# ==========================================================
# Other Media
# ==========================================================

def get_random_photo():

    return get_random_image(
        PHOTO_DIR
    )


def get_random_avatar():

    return get_random_image(
        AVATAR_DIR
    )


def get_random_document_preview():

    return get_random_image(
        DOCUMENT_PREVIEW_DIR
    )