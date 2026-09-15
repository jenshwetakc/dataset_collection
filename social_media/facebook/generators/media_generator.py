# # social_media/facebook/media_generator.py
#
# from __future__ import annotations
#
# import random
#
# from social_media.common.media_generator import (
#     ASSETS_ROOT,
#     get_random_image,
#     get_image_files,
# )
#
#
# # ==========================================================
# # Facebook Asset Directories
# # ==========================================================
#
# AVATAR_DIR = (
#     ASSETS_ROOT
#     / "avatars"
# )
#
# PROFILE_DIR = (
#     ASSETS_ROOT
#     / "profiles"
# )
#
# POST_DIR = (
#     ASSETS_ROOT
#     / "photos"
# )
#
# LIFESTYLE_DIR = (
#     ASSETS_ROOT
#     / "lifestyle"
# )
#
# TRAVEL_DIR = (
#     ASSETS_ROOT
#     / "travel"
# )
#
# PETS_DIR = (
#     ASSETS_ROOT
#     / "pets"
# )
#
# FOOD_DIR = (
#     ASSETS_ROOT
#     / "food"
# )
#
# PRODUCT_DIR = (
#     ASSETS_ROOT
#     / "products"
# )
#
# BANNER_DIR = (
#     ASSETS_ROOT
#     / "banners"
# )
#
# NOTO_EMOJI_DIR = (
#     ASSETS_ROOT
#     / "notoemoji"
# )
#
# TWEMOJI_DIR = (
#     ASSETS_ROOT
#     / "twemoji"
# )
#
#
#
# def get_random_noto_emoji() -> str | None:
#
#     return get_random_image(
#         NOTO_EMOJI_DIR
#     )
#
#
# def get_random_twemoji() -> str | None:
#
#     return get_random_image(
#         TWEMOJI_DIR
#     )
#
#
# def get_random_emoji() -> str | None:
#
#     directories = [
#         NOTO_EMOJI_DIR,
#         TWEMOJI_DIR,
#     ]
#
#     random.shuffle(
#         directories
#     )
#
#     for directory in directories:
#
#         image = get_random_image(
#             directory
#         )
#
#         if image is not None:
#             return image
#
#     return None
# # ==========================================================
# # Avatar
# # ==========================================================
#
# def get_random_avatar() -> str | None:
#
#     image = get_random_image(
#         AVATAR_DIR
#     )
#
#     if image is None:
#
#         image = get_random_image(
#             PROFILE_DIR
#         )
#
#     return image
#
#
# # ==========================================================
# # Profile Image
# # ==========================================================
#
# def get_random_profile_image() -> str | None:
#
#     return get_random_image(
#         PROFILE_DIR
#     )
#
#
# # ==========================================================
# # Post Image
# # ==========================================================
#
# def get_random_post_image() -> str | None:
#
#     directories = [
#         POST_DIR,
#         LIFESTYLE_DIR,
#         TRAVEL_DIR,
#         PETS_DIR,
#         FOOD_DIR,
#     ]
#
#     directory = random.choice(
#         directories
#     )
#
#     return get_random_image(
#         directory
#     )
#
#
# # ==========================================================
# # Story Images
# # ==========================================================
#
# def get_random_story_images(
#     count: int = 6,
# ) -> list[str]:
#
#     directories = [
#         PROFILE_DIR,
#         LIFESTYLE_DIR,
#         TRAVEL_DIR,
#         PETS_DIR,
#     ]
#
#     images = []
#
#     for _ in range(count):
#
#         directory = random.choice(
#             directories
#         )
#
#         image = get_random_image(
#             directory
#         )
#
#         if image is not None:
#             images.append(
#                 image
#             )
#
#     return images
#
#
# # ==========================================================
# # Marketplace Product
# # ==========================================================
#
# def get_random_product_image() -> str | None:
#
#     return get_random_image(
#         PRODUCT_DIR
#     )
#
#
# # ==========================================================
# # Cover / Banner
# # ==========================================================
#
# def get_random_cover_image() -> str | None:
#
#     image = get_random_image(
#         BANNER_DIR
#     )
#
#     if image is None:
#
#         image = get_random_image(
#             TRAVEL_DIR
#         )
#
#     return image
#
#
# # ==========================================================
# # Debug Helper
# # ==========================================================
#
# def debug_directory(
#     name: str,
#     directory,
# ) -> None:
#
#     print(
#         "\n"
#         "------------------------------------------"
#     )
#
#     print(
#         f"Directory: {name}"
#     )
#
#     print(
#         "Path:",
#         directory,
#     )
#
#     print(
#         "Exists:",
#         directory.exists(),
#     )
#
#     images = get_image_files(
#         str(directory)
#     )
#
#     print(
#         "Image count:",
#         len(images),
#     )
#
#     if images:
#
#         print(
#             "Sample file:",
#             images[0],
#         )
#
#
# # ==========================================================
# # Debug
# # ==========================================================
#
# if __name__ == "__main__":
#
#     print(
#         "\n"
#         "=========================================="
#     )
#
#     print(
#         "FACEBOOK MEDIA GENERATOR DEBUG"
#     )
#
#     print(
#         "=========================================="
#     )
#
#     print(
#         "\nAssets root:"
#     )
#
#     print(
#         ASSETS_ROOT
#     )
#
#     print(
#         "\nAssets root exists:",
#         ASSETS_ROOT.exists(),
#     )
#
#
#     # ======================================================
#     # Directory Debug
#     # ======================================================
#
#     directories = {
#
#         "AVATAR_DIR":
#             AVATAR_DIR,
#
#         "PROFILE_DIR":
#             PROFILE_DIR,
#
#         "POST_DIR":
#             POST_DIR,
#
#         "LIFESTYLE_DIR":
#             LIFESTYLE_DIR,
#
#         "TRAVEL_DIR":
#             TRAVEL_DIR,
#
#         "PETS_DIR":
#             PETS_DIR,
#
#         "FOOD_DIR":
#             FOOD_DIR,
#
#         "PRODUCT_DIR":
#             PRODUCT_DIR,
#
#         "BANNER_DIR":
#             BANNER_DIR,
#     }
#
#     for (
#         name,
#         directory,
#     ) in directories.items():
#
#         debug_directory(
#             name,
#             directory,
#         )
#
#
#     # ======================================================
#     # Generator Debug
#     # ======================================================
#
#     print(
#         "\n"
#         "=========================================="
#     )
#
#     print(
#         "GENERATOR TESTS"
#     )
#
#     print(
#         "=========================================="
#     )
#
#
#     avatar = get_random_avatar()
#
#     print(
#         "\nRandom avatar loaded:",
#         avatar is not None,
#     )
#
#     if avatar:
#
#         print(
#             "Avatar data URI prefix:",
#             avatar[:50],
#         )
#
#
#     profile_image = (
#         get_random_profile_image()
#     )
#
#     print(
#         "\nRandom profile image loaded:",
#         profile_image is not None,
#     )
#
#     if profile_image:
#
#         print(
#             "Profile data URI prefix:",
#             profile_image[:50],
#         )
#
#
#     post_image = (
#         get_random_post_image()
#     )
#
#     print(
#         "\nRandom post image loaded:",
#         post_image is not None,
#     )
#
#     if post_image:
#
#         print(
#             "Post data URI prefix:",
#             post_image[:50],
#         )
#
#
#     story_images = (
#         get_random_story_images(
#             count=6,
#         )
#     )
#
#     print(
#         "\nStory images requested:",
#         6,
#     )
#
#     print(
#         "Story images returned:",
#         len(story_images),
#     )
#
#     if story_images:
#
#         print(
#             "Story data URI prefix:",
#             story_images[0][:50],
#         )
#
#
#     product_image = (
#         get_random_product_image()
#     )
#
#     print(
#         "\nRandom product image loaded:",
#         product_image is not None,
#     )
#
#     if product_image:
#
#         print(
#             "Product data URI prefix:",
#             product_image[:50],
#         )
#
#
#     cover_image = (
#         get_random_cover_image()
#     )
#
#     print(
#         "\nRandom cover image loaded:",
#         cover_image is not None,
#     )
#
#     if cover_image:
#
#         print(
#             "Cover data URI prefix:",
#             cover_image[:50],
#         )
#
#
#     print(
#         "\n"
#         "=========================================="
#     )
#
#     print(
#         "FACEBOOK MEDIA DEBUG COMPLETE"
#     )
#
#     print(
#         "=========================================="
#     )

from __future__ import annotations

import random

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


# ==========================================================
# Facebook Asset Directories
# ==========================================================

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

PROFILE_DIR = (
    ASSETS_ROOT
    / "profiles"
)

POST_DIR = (
    ASSETS_ROOT
    / "photos"
)

LIFESTYLE_DIR = (
    ASSETS_ROOT
    / "lifestyle"
)

TRAVEL_DIR = (
    ASSETS_ROOT
    / "travel"
)

PETS_DIR = (
    ASSETS_ROOT
    / "pets"
)

FOOD_DIR = (
    ASSETS_ROOT
    / "food"
)

PRODUCT_DIR = (
    ASSETS_ROOT
    / "products"
)

BANNER_DIR = (
    ASSETS_ROOT
    / "banners"
)


# ==========================================================
# Emoji Asset Directories
# ==========================================================

NOTO_EMOJI_DIR = (
    ASSETS_ROOT
    / "notoemoji"
)

TWEMOJI_DIR = (
    ASSETS_ROOT
    / "twemoji"
)


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar() -> str | None:

    image = get_random_image(
        AVATAR_DIR
    )

    if image is None:

        image = get_random_image(
            PROFILE_DIR
        )

    return image


# ==========================================================
# Profile
# ==========================================================

def get_random_profile_image() -> str | None:

    return get_random_image(
        PROFILE_DIR
    )


# ==========================================================
# Posts
# ==========================================================

def get_random_post_image() -> str | None:

    directories = [
        POST_DIR,
        LIFESTYLE_DIR,
        TRAVEL_DIR,
        PETS_DIR,
        FOOD_DIR,
    ]

    random.shuffle(
        directories
    )

    for directory in directories:

        image = get_random_image(
            directory
        )

        if image is not None:

            return image

    return None


# ==========================================================
# Story Images
# ==========================================================

def get_random_story_images(
    count: int = 6,
) -> list[str]:

    directories = [
        PROFILE_DIR,
        LIFESTYLE_DIR,
        TRAVEL_DIR,
        PETS_DIR,
    ]

    images = []

    for _ in range(
        count
    ):

        shuffled_directories = (
            directories.copy()
        )

        random.shuffle(
            shuffled_directories
        )

        selected_image = None

        for directory in shuffled_directories:

            selected_image = (
                get_random_image(
                    directory
                )
            )

            if selected_image is not None:
                break

        if selected_image is not None:

            images.append(
                selected_image
            )

    return images


# ==========================================================
# Product
# ==========================================================

def get_random_product_image() -> str | None:

    return get_random_image(
        PRODUCT_DIR
    )


# ==========================================================
# Cover / Banner
# ==========================================================

def get_random_cover_image() -> str | None:

    image = get_random_image(
        BANNER_DIR
    )

    if image is None:

        image = get_random_image(
            TRAVEL_DIR
        )

    if image is None:

        image = get_random_post_image()

    return image


# ==========================================================
# Noto Emoji
# ==========================================================

def get_random_noto_emoji() -> str | None:

    return get_random_image(
        NOTO_EMOJI_DIR
    )


# ==========================================================
# Twemoji
# ==========================================================

def get_random_twemoji() -> str | None:

    return get_random_image(
        TWEMOJI_DIR
    )


# ==========================================================
# Random Emoji
# ==========================================================

def get_random_emoji() -> str | None:

    directories = [
        NOTO_EMOJI_DIR,
        TWEMOJI_DIR,
    ]

    random.shuffle(
        directories
    )

    for directory in directories:

        emoji = get_random_image(
            directory
        )

        if emoji is not None:

            return emoji

    return None


# ==========================================================
# Multiple Random Emojis
# ==========================================================

def get_random_emojis(
    count: int = 24,
) -> list[str]:

    images = []

    attempts = 0

    max_attempts = max(
        count * 5,
        30,
    )

    while (
        len(images) < count
        and
        attempts < max_attempts
    ):

        attempts += 1

        image = get_random_emoji()

        if image is None:
            continue

        images.append(
            image
        )

    return images


# ==========================================================
# Emoji Source Variant
# ==========================================================

def get_random_emoji_with_source() -> dict | None:

    source = random.choice(
        [
            "noto",
            "twemoji",
        ]
    )

    if source == "noto":

        image = get_random_noto_emoji()

    else:

        image = get_random_twemoji()

    # Fallback to other source
    if image is None:

        image = get_random_emoji()

    if image is None:

        return None

    return {
        "image":
            image,

        "source":
            source,
    }


# ==========================================================
# Debug Helpers
# ==========================================================

def debug_directory(
    name: str,
    directory,
):

    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "DIRECTORY:",
        name,
    )

    print(
        "Path:",
        directory,
    )

    print(
        "Exists:",
        directory.exists(),
    )

    if not directory.exists():

        print(
            "Count:",
            0,
        )

        return

    files = get_image_files(
        str(
            directory
        )
    )

    print(
        "Count:",
        len(
            files
        ),
    )

    if files:

        print(
            "First file:",
            files[0],
        )


# ==========================================================
# Debug Main
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK MEDIA GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "ASSETS ROOT:",
        ASSETS_ROOT,
    )


    directories = [
        (
            "avatars",
            AVATAR_DIR,
        ),
        (
            "profiles",
            PROFILE_DIR,
        ),
        (
            "posts",
            POST_DIR,
        ),
        (
            "lifestyle",
            LIFESTYLE_DIR,
        ),
        (
            "travel",
            TRAVEL_DIR,
        ),
        (
            "pets",
            PETS_DIR,
        ),
        (
            "food",
            FOOD_DIR,
        ),
        (
            "products",
            PRODUCT_DIR,
        ),
        (
            "banners",
            BANNER_DIR,
        ),
        (
            "notoemoji",
            NOTO_EMOJI_DIR,
        ),
        (
            "twemoji",
            TWEMOJI_DIR,
        ),
    ]


    for name, directory in directories:

        debug_directory(
            name,
            directory,
        )


    print(
        "\n"
        "=========================================="
    )

    print(
        "SAMPLE LOAD TEST"
    )

    print(
        "=========================================="
    )


    avatar = get_random_avatar()

    print(
        "Avatar loaded:",
        avatar is not None,
    )

    if avatar:

        print(
            "Avatar prefix:",
            avatar[:40],
        )


    profile = get_random_profile_image()

    print(
        "Profile loaded:",
        profile is not None,
    )


    post = get_random_post_image()

    print(
        "Post loaded:",
        post is not None,
    )


    product = get_random_product_image()

    print(
        "Product loaded:",
        product is not None,
    )


    cover = get_random_cover_image()

    print(
        "Cover loaded:",
        cover is not None,
    )


    noto = get_random_noto_emoji()

    print(
        "Noto Emoji loaded:",
        noto is not None,
    )


    twemoji = get_random_twemoji()

    print(
        "Twemoji loaded:",
        twemoji is not None,
    )


    random_emoji = get_random_emoji()

    print(
        "Random emoji loaded:",
        random_emoji is not None,
    )

    if random_emoji:

        print(
            "Emoji prefix:",
            random_emoji[:40],
        )


    emojis = get_random_emojis(
        count=12
    )

    print(
        "Generated emoji count:",
        len(
            emojis
        ),
    )


    stories = get_random_story_images(
        count=6
    )

    print(
        "Generated story images:",
        len(
            stories
        ),
    )