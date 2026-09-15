from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Booking Asset Directories
# ==========================================================

HOTELS_DIR = (
    ASSETS_ROOT
    / "hotels"
)

ROOMS_DIR = (
    ASSETS_ROOT
    / "rooms"
)

TRAVEL_DIR = (
    ASSETS_ROOT
    / "travel"
)

CITY_DIR = (
    ASSETS_ROOT
    / "cities"
)

# LANDMARK_DIR = (
#     ASSETS_ROOT
#     / "landmarks"
# )
LANDMARK_DIR = (
    ASSETS_ROOT
    / "travel"
)


LIFESTYLE_DIR = (
    ASSETS_ROOT
    / "lifestyle"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)


# ==========================================================
# Hotel Image
# ==========================================================

def get_random_hotel_image() -> str | None:
    """
    Return a random hotel/property image.

    Falls back to travel/lifestyle images when
    a dedicated hotel directory is unavailable.
    """

    image = get_random_image(
        HOTELS_DIR
    )

    if image is None:

        image = get_random_image(
            TRAVEL_DIR
        )

    if image is None:

        image = get_random_image(
            LIFESTYLE_DIR
        )

    return image


# ==========================================================
# Room Image
# ==========================================================

def get_random_room_image() -> str | None:
    """
    Return a random room/interior image.
    """

    image = get_random_image(
        ROOMS_DIR
    )

    if image is None:

        image = get_random_hotel_image()

    return image


# ==========================================================
# Destination Image
# ==========================================================

def get_random_destination_image() -> str | None:
    """
    Return an image suitable for city/destination cards.
    """

    image = get_random_image(
        CITY_DIR
    )

    if image is None:

        image = get_random_image(
            TRAVEL_DIR
        )

    if image is None:

        image = get_random_image(
            LANDMARK_DIR
        )

    if image is None:

        image = get_random_hotel_image()

    return image


# ==========================================================
# Landmark Image
# ==========================================================

def get_random_landmark_image() -> str | None:
    """
    Return an image suitable for attractions/landmarks.
    """

    image = get_random_image(
        LANDMARK_DIR
    )

    if image is None:

        image = get_random_image(
            TRAVEL_DIR
        )

    if image is None:

        image = get_random_destination_image()

    return image


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:
    """
    Return a random avatar.
    """

    image = get_random_image(
        AVATAR_DIR
    )

    if image is None:

        image = get_random_image(
            LIFESTYLE_DIR
        )

    return image


# ==========================================================
# Generic Property Image
# ==========================================================

def get_random_property_image() -> str | None:
    """
    Generic property image helper.

    Useful for:
    - hotels
    - apartments
    - villas
    - resorts
    - guest houses
    """

    return get_random_hotel_image()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "BOOKING MEDIA DEBUG"
    )

    print(
        "=============================="
    )


    directories = {

        "hotels":
            HOTELS_DIR,

        "rooms":
            ROOMS_DIR,

        "travel":
            TRAVEL_DIR,

        "cities":
            CITY_DIR,

        "landmarks":
            LANDMARK_DIR,

        "lifestyle":
            LIFESTYLE_DIR,

        "avatars":
            AVATAR_DIR,
    }


    for name, directory in (
        directories.items()
    ):

        print(
            f"{name:12}",
            directory,
            "| exists:",
            directory.exists(),
        )


    print(
        "\nHotel image:",
        get_random_hotel_image()
        is not None,
    )

    print(
        "Room image:",
        get_random_room_image()
        is not None,
    )

    print(
        "Destination image:",
        get_random_destination_image()
        is not None,
    )

    print(
        "Landmark image:",
        get_random_landmark_image()
        is not None,
    )

    print(
        "Avatar:",
        get_random_avatar()
        is not None,
    )