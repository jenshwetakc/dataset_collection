from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Shared Asset Directories
# ==========================================================

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

TECHNOLOGY_DIR = (
    ASSETS_ROOT
    / "technology"
)

THUMBNAIL_DIR = (
    ASSETS_ROOT
    / "thumbnails"
)


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


# ==========================================================
# Technology Image
# ==========================================================

def get_random_technology_image() -> str | None:

    return get_random_image(
        TECHNOLOGY_DIR
    )


# ==========================================================
# Thumbnail
# ==========================================================

def get_random_thumbnail() -> str | None:

    return get_random_image(
        THUMBNAIL_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "PYCHARM MEDIA DEBUG"
    )

    print(
        "=============================="
    )

    print(
        "Assets root:",
        ASSETS_ROOT,
    )

    print(
        "Avatar directory:",
        AVATAR_DIR,
    )

    print(
        "Technology directory:",
        TECHNOLOGY_DIR,
    )

    print(
        "Thumbnail directory:",
        THUMBNAIL_DIR,
    )