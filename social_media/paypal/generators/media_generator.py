from __future__ import annotations

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# PayPal Media Directories
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

AVATAR_DIR = (
    ASSET_DIR
    / "avatars"
)


MERCHANT_DIR = (
    ASSET_DIR
    / "merchants"
)


CARD_DIR = (
    ASSET_DIR
    / "cards"
)


# OFFER_DIR = (
#     ASSET_DIR
#     / "offers"
# )
OFFER_DIR = (
    ASSET_DIR
    / "banners"
)

BANNER_DIR = (
    ASSET_DIR
    / "banners"
)


# ==========================================================
# PayPal Media Helpers
# ==========================================================

def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


def get_random_merchant_image() -> str | None:

    return get_random_image(
        MERCHANT_DIR
    )


def get_random_card_image() -> str | None:

    return get_random_image(
        CARD_DIR
    )


def get_random_offer_image() -> str | None:

    return get_random_image(
        OFFER_DIR
    )


def get_random_banner() -> str | None:

    return get_random_image(
        BANNER_DIR
    )


# ==========================================================
# Debug Helper
# ==========================================================

def debug_media(
    name: str,
    directory: Path,
    loader,
) -> None:

    print(
        "\n--------------------------------"
    )

    print(
        name
    )

    print(
        "--------------------------------"
    )

    print(
        "Directory:",
        directory
    )

    print(
        "Exists:",
        directory.exists()
    )

    if directory.exists():

        files = [
            path
            for path in directory.rglob("*")
            if path.is_file()
        ]

        print(
            "Total files:",
            len(files)
        )

    media = loader()

    print(
        "Media loaded:",
        media is not None
    )

    if media:

        print(
            "Is data URI:",
            media.startswith(
                "data:"
            )
        )

        print(
            "Data URI prefix:",
            media[:80]
        )

        print(
            "Encoded length:",
            len(media)
        )


# ==========================================================
# Debug / Test
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "========================================"
    )

    print(
        "PAYPAL MEDIA GENERATOR TEST"
    )

    print(
        "========================================"
    )


    print(
        "\nAssets root:",
        ASSETS_ROOT
    )

    # print(
    #     "PayPal assets root:",
    #     PAYPAL_ASSETS_ROOT
    # )
    #
    # print(
    #     "PayPal assets exist:",
    #     PAYPAL_ASSETS_ROOT.exists()
    # )


    # ------------------------------------------------------
    # Avatar
    # ------------------------------------------------------

    debug_media(
        name="Avatar",
        directory=AVATAR_DIR,
        loader=get_random_avatar,
    )


    # ------------------------------------------------------
    # Merchant
    # ------------------------------------------------------

    debug_media(
        name="Merchant",
        directory=MERCHANT_DIR,
        loader=get_random_merchant_image,
    )


    # ------------------------------------------------------
    # Card
    # ------------------------------------------------------

    debug_media(
        name="Card",
        directory=CARD_DIR,
        loader=get_random_card_image,
    )


    # ------------------------------------------------------
    # Offer
    # ------------------------------------------------------

    debug_media(
        name="Offer",
        directory=OFFER_DIR,
        loader=get_random_offer_image,
    )


    # ------------------------------------------------------
    # Banner
    # ------------------------------------------------------

    debug_media(
        name="Banner",
        directory=BANNER_DIR,
        loader=get_random_banner,
    )


    print(
        "\n"
        "========================================"
    )

    print(
        "TEST COMPLETE"
    )

    print(
        "========================================"
    )