from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Shared Asset Directories
# ==========================================================

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

DOCUMENT_DIR = (
    ASSETS_ROOT
    / "documents"
)

PHOTOS_DIR = (
    ASSETS_ROOT
    / "photos"
)

PRODUCTS_DIR = (
    ASSETS_ROOT
    / "products"
)

TRAVEL_DIR = (
    ASSETS_ROOT
    / "travel"
)

print(ASSETS_ROOT)
print(PHOTOS_DIR)
print(DOCUMENT_DIR)
print(PRODUCTS_DIR)
print(TRAVEL_DIR)

# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


# ==========================================================
# Email Attachment Image
# ==========================================================

def get_random_attachment_image() -> str | None:

    directories = [
        PHOTOS_DIR,
        PRODUCTS_DIR,
        TRAVEL_DIR,
    ]

    import random

    directory = random.choice(
        directories
    )

    return get_random_image(
        directory
    )