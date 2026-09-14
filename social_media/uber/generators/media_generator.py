from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Uber Media Directories
# ==========================================================

DRIVER_DIR = (
    ASSETS_ROOT
    / "avatars"
)

VEHICLE_DIR = (
    ASSETS_ROOT
    / "vehicles"
)

PLACE_DIR = (
    ASSETS_ROOT
    / "places"
)

PROMOTION_DIR = (
    ASSETS_ROOT
    / "banners"
)


# ==========================================================
# Uber Media Helpers
# ==========================================================

def get_random_driver_image() -> str | None:

    return get_random_image(
        DRIVER_DIR
    )


def get_random_vehicle_image() -> str | None:

    return get_random_image(
        VEHICLE_DIR
    )


def get_random_place_image() -> str | None:

    return get_random_image(
        PLACE_DIR
    )


def get_random_promotion_image() -> str | None:

    return get_random_image(
        PROMOTION_DIR
    )


# ==========================================================
# Generic Ride / Transport Artwork
#
# Useful if a specific asset directory is empty.
# ==========================================================

def get_random_transport_image() -> str | None:

    image = (
        get_random_vehicle_image()
    )

    if image:
        return image


    image = (
        get_random_place_image()
    )

    if image:
        return image


    return get_random_driver_image()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "UBER MEDIA"
    )

    print(
        "=============================="
    )


    print(
        "Driver:",
        DRIVER_DIR
    )

    print(
        "Vehicle:",
        VEHICLE_DIR
    )

    print(
        "Place:",
        PLACE_DIR
    )

    print(
        "Promotion:",
        PROMOTION_DIR
    )


    image = (
        get_random_transport_image()
    )


    print(
        "Random transport image loaded:",
        image is not None
    )