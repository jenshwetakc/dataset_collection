from __future__ import annotations

from pathlib import Path

from system.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Windows Asset Root
# ==========================================================

# WINDOWS_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "windows"
# )


# ==========================================================
# Asset Directories
# ==========================================================

WALLPAPER_DIR = (
    ASSETS_ROOT
    / "wallpapers"
)

PROFILE_DIR = (
    ASSETS_ROOT
    / "albums"
)

PHOTO_DIR = (
    ASSETS_ROOT
    / "photos"
)

THUMBNAIL_DIR = (
    ASSETS_ROOT
    / "thumbnails"
)


# ==========================================================
# Media Helpers
# ==========================================================

def get_random_wallpaper() -> str | None:

    return get_random_image(
        WALLPAPER_DIR
    )


def get_random_profile_image() -> str | None:

    return get_random_image(
        PROFILE_DIR
    )


def get_random_photo() -> str | None:

    return get_random_image(
        PHOTO_DIR
    )


def get_random_thumbnail() -> str | None:

    return get_random_image(
        THUMBNAIL_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "Windows assets:",
        WINDOWS_ASSETS_ROOT,
    )

    print(
        "Wallpaper:",
        bool(
            get_random_wallpaper()
        ),
    )