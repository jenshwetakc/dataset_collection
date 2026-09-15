from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_avatar,
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


QR_TABS = [
    {
        "label": "Scan",
        "semantic": "scan",
    },
    {
        "label": "My code",
        "semantic": "my_code",
    },
]


# ==========================================================
# QR Pattern
# ==========================================================

def generate_qr_cells(
    size: int = 13,
) -> list[list[int]]:

    cells = []

    for row in range(size):

        current_row = []

        for column in range(size):

            value = random.choice([
                0,
                1,
            ])

            current_row.append(
                value
            )

        cells.append(
            current_row
        )

    return cells


# ==========================================================
# Recent Recipient
# ==========================================================

def generate_recent_recipient(
    index: int,
) -> dict:

    name = fake.name()

    return {
        "id":
            index,

        "name":
            name,

        "username":
            "@"
            + fake.user_name(),

        "avatar":
            get_random_avatar(),

        "initial":
            name[0].upper(),
    }


# ==========================================================
# Main
# ==========================================================

def generate_qr_pay_data() -> dict:

    active_mode = random.choice([
        "scan",
        "scan",
        "my_code",
    ])

    recent_count = random.randint(
        4,
        7,
    )

    return {

        "title":
            random.choice([
                "Pay with QR",
                "Scan & pay",
                "QR payments",
            ]),

        "subtitle":
            random.choice([
                "Scan a PayPal QR code to pay.",
                "Point your camera at a payment code.",
                "Scan or share your personal QR code.",
            ]),

        "active_mode":
            active_mode,

        "tabs":
            QR_TABS,

        "flash_enabled":
            random.random()
            < 0.25,

        "camera_message":
            random.choice([
                "Position the QR code inside the frame",
                "Hold steady to scan",
                "Align the code with the square",
            ]),

        "user": {
            "name":
                fake.name(),

            "username":
                "@"
                + fake.user_name(),

            "avatar":
                get_random_avatar(),
        },

        "qr_cells":
            generate_qr_cells(),

        "recent_recipients": [
            generate_recent_recipient(
                index
            )
            for index in range(
                recent_count
            )
        ],

        "navigation":
            NAVIGATION_ITEMS,

        "show_permission_dialog":
            random.random()
            < 0.25,

        "permission_type":
            random.choice([
                "camera",
                "photos",
            ]),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_qr_pay_data()
    )