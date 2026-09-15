# social_media/youtube/generators/media_generator.py

from __future__ import annotations

import base64
import mimetypes
import random

from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================



SOCIAL_MEDIA_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)


COMMON_ROOT = (
    SOCIAL_MEDIA_ROOT
    / "aimg"
)


ASSETS_ROOT = (
    COMMON_ROOT
    / "assets"
)


THUMBNAIL_DIR = (
    COMMON_ROOT
    / "thumbnails"
)


AVATAR_DIR = (
    COMMON_ROOT
    / "avatars"
)


BANNER_DIR = (
    COMMON_ROOT
    / "banners"
)


SHORTS_DIR = (
    COMMON_ROOT
    / "shorts"
)


# ==========================================================
# Supported Extensions
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# ==========================================================
# Find Image Files
# ==========================================================

def get_image_files(
    directory: Path,
) -> list[Path]:

    if not directory.exists():

        print(
            f"[MEDIA WARNING] "
            f"Directory does not exist: "
            f"{directory}"
        )

        return []


    return [
        file
        for file in directory.rglob("*")
        if (
            file.is_file()
            and file.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    ]


# ==========================================================
# Image -> Data URI
# ==========================================================

def image_to_data_uri(
    image_path: Path,
) -> str:

    mime_type, _ = (
        mimetypes.guess_type(
            image_path
        )
    )


    if mime_type is None:

        mime_type = (
            "image/jpeg"
        )


    encoded = (
        base64.b64encode(
            image_path.read_bytes()
        )
        .decode(
            "utf-8"
        )
    )


    return (
        f"data:{mime_type};"
        f"base64,{encoded}"
    )


# ==========================================================
# Random Image
# ==========================================================

def get_random_image(
    directory: Path,
) -> str | None:

    images = (
        get_image_files(
            directory
        )
    )


    if not images:

        print(
            f"[MEDIA WARNING] "
            f"No images found in: "
            f"{directory}"
        )

        return None


    selected_image = (
        random.choice(
            images
        )
    )


    return (
        image_to_data_uri(
            selected_image
        )
    )


# ==========================================================
# YouTube Media Helpers
# ==========================================================

def get_random_thumbnail() -> str | None:

    return get_random_image(
        THUMBNAIL_DIR
    )


def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


def get_random_banner() -> str | None:

    return get_random_image(
        BANNER_DIR
    )


def get_random_short_image() -> str | None:

    return get_random_image(
        SHORTS_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "MEDIA PATH DEBUG"
    )

    print(
        "=============================="
    )


    print(
        "Current file:",
        Path(__file__).resolve()
    )

    print(
        "Social media root:",
        SOCIAL_MEDIA_ROOT
    )

    print(
        "Common root:",
        COMMON_ROOT
    )

    print(
        "Assets root:",
        ASSETS_ROOT
    )

    print(
        "Assets exists:",
        ASSETS_ROOT.exists()
    )


    print(
        "\nThumbnail directory:",
        THUMBNAIL_DIR
    )

    print(
        "Thumbnail exists:",
        THUMBNAIL_DIR.exists()
    )

    print(
        "Thumbnail count:",
        len(
            get_image_files(
                THUMBNAIL_DIR
            )
        )
    )


    print(
        "\nAvatar directory:",
        AVATAR_DIR
    )

    print(
        "Avatar exists:",
        AVATAR_DIR.exists()
    )

    print(
        "Avatar count:",
        len(
            get_image_files(
                AVATAR_DIR
            )
        )
    )


    print(
        "\nBanner count:",
        len(
            get_image_files(
                BANNER_DIR
            )
        )
    )


    print(
        "Shorts count:",
        len(
            get_image_files(
                SHORTS_DIR
            )
        )
    )


    thumbnail = (
        get_random_thumbnail()
    )


    if thumbnail:

        print(
            "\nThumbnail loaded successfully."
        )

        print(
            "Thumbnail prefix:",
            thumbnail[:50]
        )

    else:

        print(
            "\nNo thumbnail loaded."
        )