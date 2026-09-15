from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Shared Asset Directories
# ==========================================================

PROPERTY_DIR = (
    ASSETS_ROOT
    / "home"
)

INTERIOR_DIR = (
    ASSETS_ROOT
    / "interiors"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

BANNER_DIR = (
    ASSETS_ROOT
    / "banners"
)

MAP_DIR = (
    ASSETS_ROOT
    / "maps"
)


# ==========================================================
# Zillow Media Helpers
# ==========================================================

def get_random_property_image() -> str | None:

    return get_random_image(
        PROPERTY_DIR
    )


def get_random_interior_image() -> str | None:

    return get_random_image(
        INTERIOR_DIR
    )


def get_random_agent_image() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


def get_random_hero_image() -> str | None:

    # For the home hero, house/property images work well.
    return get_random_image(
        PROPERTY_DIR
    )


def get_random_map_image() -> str | None:

    return get_random_image(
        MAP_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "ZILLOW MEDIA GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "Property directory:",
        PROPERTY_DIR,
    )

    print(
        "Interior directory:",
        INTERIOR_DIR,
    )

    print(
        "Avatar directory:",
        AVATAR_DIR,
    )

    print(
        "Map directory:",
        MAP_DIR,
    )

    print(
        "Property image loaded:",
        get_random_property_image()
        is not None,
    )

    print(
        "Agent image loaded:",
        get_random_agent_image()
        is not None,
    )