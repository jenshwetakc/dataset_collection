from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_card_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "semantic": "home",
    },
    {
        "label": "Activity",
        "icon": "receipt_long",
        "semantic": "activity",
    },
    {
        "label": "Send",
        "icon": "send",
        "semantic": "send",
    },
    {
        "label": "Wallet",
        "icon": "account_balance_wallet",
        "semantic": "wallet",
    },
]


TABS = [
    {
        "label": "Payment methods",
        "semantic": "payment_methods",
    },
    {
        "label": "Banks",
        "semantic": "banks",
    },
]


CARD_BRANDS = [
    "Visa",
    "Mastercard",
    "American Express",
]


BANKS = [
    "Chase Bank",
    "Bank of America",
    "Citibank",
    "Wells Fargo",
    "KB Bank",
    "Shinhan Bank",
    "Woori Bank",
]


# ==========================================================
# Card
# ==========================================================

def generate_card(
    index: int,
) -> dict:

    brand = random.choice(
        CARD_BRANDS
    )

    last_four = (
        str(
            random.randint(
                0,
                9999,
            )
        )
        .zfill(4)
    )

    month = random.randint(
        1,
        12,
    )

    year = random.randint(
        27,
        32,
    )

    return {
        "id":
            index,

        "brand":
            brand,

        "last_four":
            last_four,

        "expiry":
            f"{month:02d}/{year}",

        "preferred":
            index == 0,

        "image":
            get_random_card_image(),

        "color_variant":
            random.choice([
                "primary",
                "surface",
                "dark",
            ]),
    }


# ==========================================================
# Bank
# ==========================================================

def generate_bank(
    index: int,
) -> dict:

    name = random.choice(
        BANKS
    )

    last_four = (
        str(
            random.randint(
                0,
                9999,
            )
        )
        .zfill(4)
    )

    return {
        "id":
            index,

        "name":
            name,

        "last_four":
            last_four,

        "verified":
            random.random()
            < 0.85,

        "preferred":
            index == 0,
    }


# ==========================================================
# Main
# ==========================================================

def generate_wallet_data() -> dict:

    card_count = random.randint(
        2,
        4,
    )

    bank_count = random.randint(
        1,
        3,
    )

    return {

        "title":
            random.choice([
                "Wallet",
                "Payment methods",
                "Your wallet",
            ]),

        "subtitle":
            random.choice([
                "Manage how you pay with PayPal.",
                "Cards, banks, and your PayPal balance.",
                "Choose and manage your payment methods.",
            ]),

        "balance":
            f"${random.uniform(100, 5000):,.2f}",

        "cards": [
            generate_card(index)
            for index in range(
                card_count
            )
        ],

        "banks": [
            generate_bank(index)
            for index in range(
                bank_count
            )
        ],

        "tabs":
            TABS,

        "navigation":
            NAVIGATION_ITEMS,

        "show_add_sheet":
            random.random()
            < 0.35,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_wallet_data()
    )