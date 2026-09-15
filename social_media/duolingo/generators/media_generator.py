from __future__ import annotations

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)



PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)


# ==========================================================
# Asset Paths
# ==========================================================

ASSET_DIR = (
    PROJECT_ROOT
    / "assets"
)
# ==========================================================
# Duolingo Asset Root
# ==========================================================
# 
# DUOLINGO_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "duolingo"
# )


# ==========================================================
# Asset Directories
# ==========================================================

CHARACTER_DIR = (
    ASSET_DIR
    / "characters"
)

ILLUSTRATION_DIR = (
    ASSET_DIR
    / "illustrations"
)

AVATAR_DIR = (
    ASSET_DIR
    / "avatars"
)

COURSE_DIR = (
    ASSET_DIR
    / "courses"
)

REWARD_DIR = (
    ASSET_DIR
    / "rewards"
)

ACHIEVEMENT_DIR = (
    ASSET_DIR
    / "achievements"
)


# ==========================================================
# Media Helpers
# ==========================================================

def get_random_character() -> str | None:

    return get_random_image(
        CHARACTER_DIR
    )


def get_random_illustration() -> str | None:

    return get_random_image(
        ILLUSTRATION_DIR
    )


def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


def get_random_course_image() -> str | None:

    return get_random_image(
        COURSE_DIR
    )


def get_random_reward() -> str | None:

    return get_random_image(
        REWARD_DIR
    )


def get_random_achievement() -> str | None:

    return get_random_image(
        ACHIEVEMENT_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "DUOLINGO MEDIA"
    )

    print(
        "=============================="
    )

    print(
        "Assets root:",
        ASSET_DIR
    )

    print(
        "Character:",
        get_random_character()
        is not None
    )

    print(
        "Illustration:",
        get_random_illustration()
        is not None
    )

    print(
        "Avatar:",
        get_random_avatar()
        is not None
    )