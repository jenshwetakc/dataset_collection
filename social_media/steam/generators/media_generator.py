from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Steam Asset Paths
# ==========================================================

GAME_COVER_DIR = (
    ASSETS_ROOT
    / "game_covers"
)

GAME_BANNER_DIR = (
    ASSETS_ROOT
    / "game_banners"
)

GAME_SCREENSHOT_DIR = (
    ASSETS_ROOT
    / "game_screenshots"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)


# ==========================================================
# Media Helpers
# ==========================================================

def get_random_game_cover() -> str | None:

    return get_random_image(
        GAME_COVER_DIR
    )


def get_random_game_banner() -> str | None:

    return get_random_image(
        GAME_BANNER_DIR
    )


def get_random_game_screenshot() -> str | None:

    return get_random_image(
        GAME_SCREENSHOT_DIR
    )


def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )