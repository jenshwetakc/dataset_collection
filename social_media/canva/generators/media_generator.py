from __future__ import annotations

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Canva Asset Directories
# ==========================================================

PHOTO_DIR = (
    ASSETS_ROOT
    / "photos"
)

TEMPLATE_DIR = (
    ASSETS_ROOT
    / "templates"
)

THUMBNAIL_DIR = (
    ASSETS_ROOT
    / "thumbnails"
)

ILLUSTRATION_DIR = (
    ASSETS_ROOT
    / "illustrations"
)

BACKGROUND_DIR = (
    ASSETS_ROOT
    / "backgrounds"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)


# ==========================================================
# Generic Fallback Loader
# ==========================================================

def _get_with_fallback(
    *directories: Path,
) -> str | None:
    """
    Try directories in order until an image is found.
    """

    for directory in directories:

        image = get_random_image(
            directory
        )

        if image:
            return image

    return None


# ==========================================================
# Canva Media Helpers
# ==========================================================

def get_random_template_image() -> str | None:

    return _get_with_fallback(
        TEMPLATE_DIR,
        THUMBNAIL_DIR,
        PHOTO_DIR,
    )


def get_random_design_thumbnail() -> str | None:

    return _get_with_fallback(
        THUMBNAIL_DIR,
        TEMPLATE_DIR,
        PHOTO_DIR,
    )


def get_random_photo() -> str | None:

    return _get_with_fallback(
        PHOTO_DIR,
        THUMBNAIL_DIR,
    )


def get_random_background() -> str | None:

    return _get_with_fallback(
        BACKGROUND_DIR,
        PHOTO_DIR,
        TEMPLATE_DIR,
    )


def get_random_illustration() -> str | None:

    return _get_with_fallback(
        ILLUSTRATION_DIR,
        TEMPLATE_DIR,
        PHOTO_DIR,
    )


def get_random_avatar() -> str | None:

    return _get_with_fallback(
        AVATAR_DIR,
        PHOTO_DIR,
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "CANVA MEDIA DEBUG"
    )

    print(
        "=============================="
    )

    print(
        "Assets root:",
        ASSETS_ROOT,
    )

    print(
        "Template:",
        get_random_template_image()
        is not None,
    )

    print(
        "Thumbnail:",
        get_random_design_thumbnail()
        is not None,
    )

    print(
        "Avatar:",
        get_random_avatar()
        is not None,
    )