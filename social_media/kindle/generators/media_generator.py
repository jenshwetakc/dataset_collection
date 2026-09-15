from __future__ import annotations

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Shared Kindle Assets
# ==========================================================

BOOKS_DIR = (
    ASSETS_ROOT
    / "books"
)

PEOPLE_DIR = (
    ASSETS_ROOT
    / "characters"
)


# ==========================================================
# Book Cover
# ==========================================================

def get_random_book_cover() -> str | None:

    return get_random_image(
        BOOKS_DIR
    )


# ==========================================================
# Author / Profile Image
# ==========================================================

def get_random_author_image() -> str | None:

    return get_random_image(
        PEOPLE_DIR
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "KINDLE MEDIA DEBUG"
    )

    print(
        "=============================="
    )

    print(
        "Books directory:",
        BOOKS_DIR,
    )

    print(
        "People directory:",
        PEOPLE_DIR,
    )

    print(
        "Book loaded:",
        get_random_book_cover()
        is not None,
    )

    print(
        "Author loaded:",
        get_random_author_image()
        is not None,
    )