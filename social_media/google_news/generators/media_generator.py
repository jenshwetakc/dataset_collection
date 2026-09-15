from __future__ import annotations

import random

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    image_to_data_uri,
)


# ==========================================================
# Google News Media Directories
# ==========================================================

NEWS_DIR = (
    ASSETS_ROOT
    / "news"
)

THUMBNAIL_DIR = (
    ASSETS_ROOT
    / "news_banners"
)

PHOTO_DIR = (
    ASSETS_ROOT
    / "photos"
)

BANNER_DIR = (
    ASSETS_ROOT
    / "news_banners"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

LOGO_DIR = (
    ASSETS_ROOT
    / "logos"
)


# ==========================================================
# Candidate Directories
# ==========================================================

ARTICLE_IMAGE_DIRECTORIES = [
    NEWS_DIR,
    THUMBNAIL_DIR,
    PHOTO_DIR,
    BANNER_DIR,
]

PUBLISHER_IMAGE_DIRECTORIES = [
    LOGO_DIR,
    AVATAR_DIR,
]

AVATAR_IMAGE_DIRECTORIES = [
    AVATAR_DIR,
    LOGO_DIR,
]


# ==========================================================
# Generic Candidate Image Helper
# ==========================================================

def get_random_image_from_directories(
    directories: list[Path],
) -> str | None:
    """
    Pick a random image from the first available collection
    across multiple candidate directories.
    """

    available_images = []

    for directory in directories:

        images = get_image_files(
            str(directory)
        )

        available_images.extend(
            images
        )

    if not available_images:

        print(
            "[GOOGLE NEWS MEDIA WARNING] "
            "No images found in candidate directories:"
        )

        for directory in directories:
            print(
                " -",
                directory,
            )

        return None

    selected = random.choice(
        available_images
    )

    return image_to_data_uri(
        selected
    )


# ==========================================================
# Public Helpers
# ==========================================================

def get_random_article_image() -> str | None:

    return get_random_image_from_directories(
        ARTICLE_IMAGE_DIRECTORIES
    )


def get_random_hero_image() -> str | None:

    return get_random_image_from_directories(
        ARTICLE_IMAGE_DIRECTORIES
    )


def get_random_publisher_logo() -> str | None:

    return get_random_image_from_directories(
        PUBLISHER_IMAGE_DIRECTORIES
    )


def get_random_avatar() -> str | None:

    return get_random_image_from_directories(
        AVATAR_IMAGE_DIRECTORIES
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "GOOGLE NEWS MEDIA"
    )

    print(
        "=============================="
    )

    print(
        "Assets root:",
        ASSETS_ROOT,
    )

    print(
        "Article image:",
        get_random_article_image()
        is not None,
    )

    print(
        "Publisher logo:",
        get_random_publisher_logo()
        is not None,
    )