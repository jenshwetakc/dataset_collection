from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)
from pathlib import Path

# ==========================================================
# Google Maps Asset Root
# ==========================================================


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

# GOOGLE_MAPS_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "google_maps"
# )


# ==========================================================
# Media Directories
# ==========================================================

PLACE_DIR = (
    ASSET_DIR
    / "places"
)


RESTAURANT_DIR = (
    ASSET_DIR
    / "restaurants"
)


CAFE_DIR = (
    ASSET_DIR
    / "cafes"
)


HOTEL_DIR = (
    ASSET_DIR
    / "hotels"
)


AVATAR_DIR = (
    ASSET_DIR
    / "avatars"
)


STREET_VIEW_DIR = (
    ASSET_DIR
    / "street_view"
)


# ==========================================================
# Random Media
# ==========================================================

def get_random_place_image() -> str | None:

    return get_random_image(
        PLACE_DIR
    )


def get_random_restaurant_image() -> str | None:

    return get_random_image(
        RESTAURANT_DIR
    )


def get_random_cafe_image() -> str | None:

    return get_random_image(
        CAFE_DIR
    )


def get_random_hotel_image() -> str | None:

    return get_random_image(
        HOTEL_DIR
    )


def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


def get_random_street_view_image() -> str | None:

    return get_random_image(
        STREET_VIEW_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "GOOGLE MAPS MEDIA"
    )

    print(
        "=============================="
    )

    print(
        "Root:",
        ASSET_DIR,
    )

    print(
        "Place image:",
        get_random_place_image()
        is not None,
    )

    print(
        "Avatar:",
        get_random_avatar()
        is not None,
    )