from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Baemin Media Directories
# ==========================================================

FOOD_DIR = (
    ASSETS_ROOT
    / "food"
)

print(FOOD_DIR)
RESTAURANT_DIR = (
    ASSETS_ROOT
    / "restaurants"
)



BANNER_DIR = (
    ASSETS_ROOT
    / "banners"
)

# CATEGORY_DIR = (
#     ASSETS_ROOT
#     / "categories"
# )

CATEGORY_DIR = (
    ASSETS_ROOT
    / "food"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)


# ==========================================================
# Baemin Media Helpers
# ==========================================================

def get_random_food_image() -> str | None:

    return get_random_image(
        FOOD_DIR
    )


def get_random_restaurant_image() -> str | None:

    return get_random_image(
        RESTAURANT_DIR
    )


def get_random_banner() -> str | None:

    return get_random_image(
        BANNER_DIR
    )


def get_random_category_image() -> str | None:

    return get_random_image(
        CATEGORY_DIR
    )


def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )