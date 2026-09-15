from __future__ import annotations

import random

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Shared Asset Directories
# ==========================================================

PRODUCTS_DIR = (
    ASSETS_ROOT
    / "products"
)

ELECTRONICS_DIR = (
    ASSETS_ROOT
    / "electronics"
)

FASHION_DIR = (
    ASSETS_ROOT
    / "products"
)

HOME_DIR = (
    ASSETS_ROOT
    / "home"
)

BOOKS_DIR = (
    ASSETS_ROOT
    / "books"
)

FOOD_DIR = (
    ASSETS_ROOT
    / "food"
)

BANNERS_DIR = (
    ASSETS_ROOT
    / "banners"
)

AVATARS_DIR = (
    ASSETS_ROOT
    / "avatars"
)

LIFESTYLE_DIR = (
    ASSETS_ROOT
    / "lifestyle"
)


# ==========================================================
# Helpers
# ==========================================================

def get_image_with_fallback(
    *directories: Path,
) -> str | None:
    """
    Try the supplied asset directories in random order.

    The first directory that returns a valid image wins.
    """

    candidates = list(
        directories
    )

    random.shuffle(
        candidates
    )

    for directory in candidates:

        image = get_random_image(
            directory
        )

        if image is not None:
            return image

    return None


# ==========================================================
# Product
# ==========================================================

def get_random_product_image() -> str | None:

    return get_image_with_fallback(
        PRODUCTS_DIR,
        ELECTRONICS_DIR,
        FASHION_DIR,
        HOME_DIR,
        BOOKS_DIR,
        FOOD_DIR,
        LIFESTYLE_DIR,
    )


# ==========================================================
# Electronics
# ==========================================================

def get_random_electronics_image() -> str | None:

    return get_image_with_fallback(
        ELECTRONICS_DIR,
        PRODUCTS_DIR,
        LIFESTYLE_DIR,
    )


# ==========================================================
# Fashion
# ==========================================================

def get_random_fashion_image() -> str | None:

    return get_image_with_fallback(
        FASHION_DIR,
        PRODUCTS_DIR,
        LIFESTYLE_DIR,
    )


# ==========================================================
# Home
# ==========================================================

def get_random_home_image() -> str | None:

    return get_image_with_fallback(
        HOME_DIR,
        PRODUCTS_DIR,
        LIFESTYLE_DIR,
    )


# ==========================================================
# Books
# ==========================================================

def get_random_book_image() -> str | None:

    return get_image_with_fallback(
        BOOKS_DIR,
        PRODUCTS_DIR,
    )


# ==========================================================
# Food
# ==========================================================

def get_random_food_image() -> str | None:

    return get_image_with_fallback(
        FOOD_DIR,
        PRODUCTS_DIR,
        LIFESTYLE_DIR,
    )


# ==========================================================
# Banner
# ==========================================================

def get_random_banner_image() -> str | None:

    return get_image_with_fallback(
        BANNERS_DIR,
        LIFESTYLE_DIR,
        HOME_DIR,
        PRODUCTS_DIR,
    )


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:

    return get_image_with_fallback(
        AVATARS_DIR,
        LIFESTYLE_DIR,
    )


# ==========================================================
# Category Image
# ==========================================================

def get_category_image(
    category: str,
) -> str | None:

    category = (
        category
        .strip()
        .lower()
    )

    if category == "electronics":

        return (
            get_random_electronics_image()
        )

    if category == "fashion":

        return (
            get_random_fashion_image()
        )

    if category == "home":

        return (
            get_random_home_image()
        )

    if category == "books":

        return (
            get_random_book_image()
        )

    if category in {
        "food",
        "grocery",
    }:

        return (
            get_random_food_image()
        )

    return get_random_product_image()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "AMAZON MEDIA DEBUG"
    )

    print(
        "=============================="
    )

    print(
        "Assets root:",
        ASSETS_ROOT,
    )

    print(
        "Product image:",
        get_random_product_image()
        is not None,
    )

    print(
        "Electronics image:",
        get_random_electronics_image()
        is not None,
    )

    print(
        "Fashion image:",
        get_random_fashion_image()
        is not None,
    )

    print(
        "Banner image:",
        get_random_banner_image()
        is not None,
    )