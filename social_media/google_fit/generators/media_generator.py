from __future__ import annotations

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Google Fit Asset Paths
# ==========================================================
#
# GOOGLE_FIT_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "google_fit"
# )


AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)


WORKOUT_DIR = (
    ASSETS_ROOT
    / "workouts"
)


HEALTH_DIR = (
    ASSETS_ROOT
    / "health"
)


# ==========================================================
# Generic Fallback Directories
# ==========================================================
#
# COMMON_AVATAR_DIR = (
#     ASSETS_ROOT
#     / "avatars"
# )


COMMON_PHOTO_DIR = (
    ASSETS_ROOT
    / "wallpapers"
)


# ==========================================================
# Helpers
# ==========================================================

def _first_available_image(
    *directories: Path,
) -> str | None:
    """
    Try directories in order and return the first
    successfully loaded image.
    """

    for directory in directories:

        image = get_random_image(
            directory
        )

        if image:
            return image

    return None


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:

    return _first_available_image(
        AVATAR_DIR,
        COMMON_PHOTO_DIR,
    )


# ==========================================================
# Workout Image
# ==========================================================

def get_random_workout_image() -> str | None:

    return _first_available_image(
        WORKOUT_DIR,
        # COMMON_PHOTO_DIR,
    )


# ==========================================================
# Health Image
# ==========================================================

def get_random_health_image() -> str | None:

    return _first_available_image(
        HEALTH_DIR,
        # COMMON_PHOTO_DIR,
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "GOOGLE FIT MEDIA"
    )

    print(
        "=============================="
    )

    print(
        "Assets root:",
        # GOOGLE_FIT_ASSETS_ROOT,
    )

    print(
        "Avatar:",
        bool(
            get_random_avatar()
        ),
    )

    print(
        "Workout:",
        bool(
            get_random_workout_image()
        ),
    )

    print(
        "Health:",
        bool(
            get_random_health_image()
        ),
    )