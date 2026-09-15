from __future__ import annotations

from pathlib import Path

from system.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


# ==========================================================
# iOS Asset Root
# ==========================================================
#
# IOS_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "ios"
# )


# ==========================================================
# Asset Directories
# ==========================================================

WALLPAPER_DIR = (
    ASSETS_ROOT
    / "wallpapers"
)

PHOTO_DIR = (
    ASSETS_ROOT
    / "photos"
)

AVATAR_DIR = (
    ASSETS_ROOT
    / "avatars"
)

WIDGET_IMAGE_DIR = (
    ASSETS_ROOT
    / "widgets"
)

MESSAGE_IMAGE_DIR = (
    ASSETS_ROOT
    / "messages"
)

APP_ICON_DIR = (
    ASSETS_ROOT
    / "app_icons"
)


# ==========================================================
# Wallpapers
# ==========================================================

def get_random_wallpaper() -> str | None:
    """
    Return one random iOS wallpaper as a base64 data URI.

    Wallpapers may be placed directly inside:

        assets/ios/wallpapers/

    or inside nested directories such as:

        wallpapers/abstract/
        wallpapers/nature/
        wallpapers/city/
        wallpapers/dark/
        wallpapers/light/

    The common media generator searches recursively.
    """

    return get_random_image(
        WALLPAPER_DIR
    )


# ==========================================================
# Photos
# ==========================================================

def get_random_photo() -> str | None:

    return get_random_image(
        PHOTO_DIR
    )


# ==========================================================
# Avatars
# ==========================================================

def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


# ==========================================================
# Widget Images
# ==========================================================

def get_random_widget_image() -> str | None:

    return get_random_image(
        WIDGET_IMAGE_DIR
    )


# ==========================================================
# Message Images
# ==========================================================

def get_random_message_image() -> str | None:

    return get_random_image(
        MESSAGE_IMAGE_DIR
    )


# ==========================================================
# App Icons
# ==========================================================

def get_random_app_icon() -> str | None:

    return get_random_image(
        APP_ICON_DIR
    )


# ==========================================================
# Asset Count Helper
# ==========================================================

def get_asset_count(
    directory: Path,
) -> int:

    return len(
        get_image_files(
            str(
                directory
            )
        )
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS MEDIA GENERATOR"
    )

    print(
        "=========================================="
    )

    print(
        "\niOS assets root:",
        IOS_ASSETS_ROOT,
    )


    print(
        "\nWallpaper directory:",
        WALLPAPER_DIR,
    )

    print(
        "Wallpaper exists:",
        WALLPAPER_DIR.exists(),
    )

    print(
        "Wallpaper count:",
        get_asset_count(
            WALLPAPER_DIR
        ),
    )


    print(
        "\nPhoto count:",
        get_asset_count(
            PHOTO_DIR
        ),
    )

    print(
        "Avatar count:",
        get_asset_count(
            AVATAR_DIR
        ),
    )

    print(
        "Widget image count:",
        get_asset_count(
            WIDGET_IMAGE_DIR
        ),
    )

    print(
        "Message image count:",
        get_asset_count(
            MESSAGE_IMAGE_DIR
        ),
    )

    print(
        "App icon count:",
        get_asset_count(
            APP_ICON_DIR
        ),
    )


    wallpaper = (
        get_random_wallpaper()
    )

    print(
        "\nRandom wallpaper loaded:",
        wallpaper is not None,
    )

    if wallpaper:

        print(
            "Wallpaper data URI prefix:",
            wallpaper[:60],
        )