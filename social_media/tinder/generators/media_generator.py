# from __future__ import annotations
#
# from social_media.common.media_generator import (
#     ASSETS_ROOT,
#     get_random_image,
# )
#
#
# # ==========================================================
# # Tinder Assets
# # ==========================================================
#
# # TINDER_ASSETS_ROOT = (
# #     ASSETS_ROOT
# #     / "tinder"
# # )
#
# PROFILE_DIR = (
#     ASSETS_ROOT
#     / "profiles"
# )
#
# AVATAR_DIR = (
#     ASSETS_ROOT
#     / "avatars"
# )
#
# LIFESTYLE_DIR = (
#     ASSETS_ROOT
#     / "lifestyle"
# )
#
# TRAVEL_DIR = (
#     ASSETS_ROOT
#     / "travel"
# )
#
# PETS_DIR = (
#     ASSETS_ROOT
#     / "pets"
# )
#
#
# # ==========================================================
# # Profile Images
# # ==========================================================
#
# def get_random_profile_image() -> str | None:
#
#     return get_random_image(
#         PROFILE_DIR
#     )
#
#
# # ==========================================================
# # Avatar
# # ==========================================================
#
# def get_random_avatar() -> str | None:
#
#     image = get_random_image(
#         AVATAR_DIR
#     )
#
#     if image is None:
#
#         image = get_random_profile_image()
#
#     return image
#
#
# # ==========================================================
# # Lifestyle
# # ==========================================================
#
# def get_random_lifestyle_image() -> str | None:
#
#     return get_random_image(
#         LIFESTYLE_DIR
#     )
#
#
# # ==========================================================
# # Travel
# # ==========================================================
#
# def get_random_travel_image() -> str | None:
#
#     return get_random_image(
#         TRAVEL_DIR
#     )
#
#
# # ==========================================================
# # Pets
# # ==========================================================
#
# def get_random_pet_image() -> str | None:
#
#     return get_random_image(
#         PETS_DIR
#     )
#
#
# # ==========================================================
# # Any Tinder Image
# # ==========================================================
#
# def get_random_tinder_image() -> str | None:
#
#     directories = [
#
#         PROFILE_DIR,
#         AVATAR_DIR,
#         LIFESTYLE_DIR,
#         TRAVEL_DIR,
#         PETS_DIR,
#
#     ]
#
#     import random
#
#     random.shuffle(
#         directories
#     )
#
#     for directory in directories:
#
#         image = get_random_image(
#             directory
#         )
#
#         if image:
#
#             return image
#
#     return None

from __future__ import annotations

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Tinder Assets
# ==========================================================

PROFILE_DIR = (
    ASSETS_ROOT
    / "profiles"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

LIFESTYLE_DIR = (
    ASSETS_ROOT
    / "lifestyle"
)

TRAVEL_DIR = (
    ASSETS_ROOT
    / "travel"
)

PETS_DIR = (
    ASSETS_ROOT
    / "pets"
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
# Debug Helpers
# ==========================================================

def get_image_count(
    directory: Path,
) -> int:

    if not directory.exists():
        return 0

    if not directory.is_dir():
        return 0

    return sum(

        1

        for file_path
        in directory.rglob("*")

        if (
            file_path.is_file()
            and file_path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    )


def debug_directory(
    name: str,
    directory: Path,
) -> None:

    exists = (
        directory.exists()
    )

    is_dir = (
        directory.is_dir()
        if exists
        else False
    )

    image_count = (
        get_image_count(
            directory
        )
    )

    print(
        "\n"
        "========================================"
    )

    print(
        f"[TINDER MEDIA] {name}"
    )

    print(
        "========================================"
    )

    print(
        "Path:"
    )

    print(
        directory
    )

    print(
        "Exists:",
        exists,
    )

    print(
        "Is directory:",
        is_dir,
    )

    print(
        "Image count:",
        image_count,
    )


def debug_all_directories() -> None:

    print(
        "\n\n"
        "========================================"
    )

    print(
        "TINDER MEDIA DEBUG"
    )

    print(
        "========================================"
    )

    print(
        "ASSETS_ROOT:"
    )

    print(
        ASSETS_ROOT
    )

    directories = {

        "PROFILE_DIR":
            PROFILE_DIR,

        "AVATAR_DIR":
            AVATAR_DIR,

        "LIFESTYLE_DIR":
            LIFESTYLE_DIR,

        "TRAVEL_DIR":
            TRAVEL_DIR,

        "PETS_DIR":
            PETS_DIR,
    }

    total_images = 0

    for name, directory in directories.items():

        debug_directory(
            name,
            directory,
        )

        total_images += (
            get_image_count(
                directory
            )
        )

    print(
        "\n"
        "========================================"
    )

    print(
        "SUMMARY"
    )

    print(
        "========================================"
    )

    print(
        "Total directories:",
        len(
            directories
        ),
    )

    print(
        "Total images:",
        total_images,
    )

    print(
        "========================================"
        "\n"
    )


# ==========================================================
# Profile Images
# ==========================================================

def get_random_profile_image() -> str | None:

    return get_random_image(
        PROFILE_DIR
    )


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:

    image = (
        get_random_image(
            AVATAR_DIR
        )
    )

    if image is None:

        image = (
            get_random_profile_image()
        )

    return image


# ==========================================================
# Lifestyle
# ==========================================================

def get_random_lifestyle_image() -> str | None:

    return get_random_image(
        LIFESTYLE_DIR
    )


# ==========================================================
# Travel
# ==========================================================

def get_random_travel_image() -> str | None:

    return get_random_image(
        TRAVEL_DIR
    )


# ==========================================================
# Pets
# ==========================================================

def get_random_pet_image() -> str | None:

    return get_random_image(
        PETS_DIR
    )


# ==========================================================
# Any Tinder Image
# ==========================================================

def get_random_tinder_image() -> str | None:

    import random

    directories = [

        PROFILE_DIR,
        AVATAR_DIR,
        LIFESTYLE_DIR,
        TRAVEL_DIR,
        PETS_DIR,

    ]

    random.shuffle(
        directories
    )

    for directory in directories:

        image = (
            get_random_image(
                directory
            )
        )

        if image:

            return image

    return None


# ==========================================================
# Debug Entry Point
# ==========================================================

if __name__ == "__main__":

    debug_all_directories()