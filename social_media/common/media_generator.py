from __future__ import annotations

import base64
import mimetypes
import random

from functools import lru_cache
from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

SOCIAL_MEDIA_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

ASSETS_ROOT = (
    SOCIAL_MEDIA_ROOT
    / "assets"
)

# ASSETS_ROOT = (
#     COMMON_ROOT
#     / "photos"
# )


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

@lru_cache(maxsize=None)
def get_image_files(
    directory: str,
) -> tuple[Path, ...]:
    """
    Return all supported image files inside a directory.

    Results are cached so the directory is scanned only once
    per process.
    """

    path = Path(directory)

    if not path.exists():

        print(
            f"[MEDIA WARNING] "
            f"Directory does not exist: "
            f"{path}"
        )

        return tuple()

    return tuple(
        file
        for file in path.rglob("*")
        if (
            file.is_file()
            and file.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    )


# ==========================================================
# Image -> Data URI
# ==========================================================

def image_to_data_uri(
    image_path: Path,
) -> str:
    """
    Convert an image file to a base64 data URI.
    """

    mime_type, _ = (
        mimetypes.guess_type(
            image_path
        )
    )

    if mime_type is None:
        mime_type = "image/jpeg"

    encoded = (
        base64.b64encode(
            image_path.read_bytes()
        )
        .decode("utf-8")
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
    """
    Return one random image from a directory
    as a base64 data URI.
    """

    images = get_image_files(
        str(directory)
    )

    if not images:

        print(
            f"[MEDIA WARNING] "
            f"No images found in: "
            f"{directory}"
        )

        return None

    selected_image = random.choice(
        images
    )

    return image_to_data_uri(
        selected_image
    )


# ==========================================================
# Optional Cache Utilities
# ==========================================================

def clear_media_cache() -> None:
    """
    Clear cached directory listings.

    Useful if new images are added while the same Python
    process is still running.
    """

    get_image_files.cache_clear()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "COMMON MEDIA DEBUG"
    )

    print(
        "=============================="
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

    images = get_image_files(
        str(ASSETS_ROOT)
    )

    print(
        "Image count:",
        len(images)
    )

    if images:

        image = get_random_image(
            ASSETS_ROOT
        )

        print(
            "Random image loaded:",
            image is not None
        )

        if image:

            print(
                "Data URI prefix:",
                image[:50]
            )