from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_card_image,
    get_random_merchant_image,
)


fake = Faker()


# ==========================================================
# Navigation
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


CARD_BRANDS = [
    "Visa",
    "Mastercard",
]


MERCHANTS = [
    "Spotify",
    "Netflix",
    "Amazon",
    "Apple",
    "Uber",
    "Starbucks",
    "Airbnb",
    "Adobe",
    "Canva",
    "Dropbox",
    "Samsung",
]


# ==========================================================
# Card
# ==========================================================

def generate_card() -> dict:

    brand = random.choice(
        CARD_BRANDS
    )

    number = "".join(
        str(
            random.randint(
                0,
                9,
            )
        )
        for _ in range(
            16
        )
    )

    formatted_number = " ".join(
        number[index:index + 4]
        for index in range(
            0,
            16,
            4,
        )
    )

    expiry_month = random.randint(
        1,
        12,
    )

    expiry_year = random.randint(
        27,
        33,
    )

    cvv = str(
        random.randint(
            100,
            999,
        )
    )

    return {
        "brand":
            brand,

        "number":
            formatted_number,

        "masked_number":
            "•••• •••• •••• "
            + number[-4:],

        "last_four":
            number[-4:],

        "expiry":
            f"{expiry_month:02d}/{expiry_year}",

        "cvv":
            cvv,

        "holder":
            fake.name().upper(),

        "image":
            get_random_card_image(),

        "frozen":
            random.random()
            < 0.25,

        "status":
            random.choice([
                "Active",
                "Active",
                "Active",
                "Temporarily locked",
            ]),
    }


# ==========================================================
# Spending
# ==========================================================

def generate_spending_data() -> dict:

    limit = random.choice([
        500,
        1000,
        1500,
        2000,
        3000,
        5000,
    ])

    spent = round(
        random.uniform(
            50,
            limit * 0.85,
        ),
        2,
    )

    percent = round(
        spent
        / limit
        * 100
    )

    return {
        "limit":
            limit,

        "spent":
            spent,

        "remaining":
            limit - spent,

        "percent":
            percent,

        "formatted_limit":
            f"${limit:,.2f}",

        "formatted_spent":
            f"${spent:,.2f}",

        "formatted_remaining":
            f"${limit - spent:,.2f}",
    }


# ==========================================================
# Transaction
# ==========================================================

def generate_card_transaction(
    index: int,
) -> dict:

    merchant = random.choice(
        MERCHANTS
        + [
            fake.company(),
        ]
    )

    amount = round(
        random.uniform(
            2,
            350,
        ),
        2,
    )

    timestamp = (
        datetime.now()
        - timedelta(
            days=random.randint(
                0,
                10,
            ),
            hours=random.randint(
                0,
                22,
            ),
        )
    )

    status = random.choice([
        "Completed",
        "Completed",
        "Completed",
        "Pending",
        "Refunded",
    ])

    return {
        "id":
            index,

        "merchant":
            merchant,

        "amount":
            f"-${amount:,.2f}",

        "status":
            status,

        "date":
            timestamp.strftime(
                "%b %d"
            ),

        "time":
            timestamp.strftime(
                "%I:%M %p"
            ).lstrip("0"),

        "image":
            get_random_merchant_image(),

        "category_icon":
            random.choice([
                "shopping_bag",
                "restaurant",
                "local_taxi",
                "movie",
                "subscriptions",
            ]),
    }


# ==========================================================
# Main
# ==========================================================

def generate_card_detail_data() -> dict:

    card = generate_card()

    return {
        "title":
            random.choice([
                "Card details",
                "Manage card",
                "PayPal card",
            ]),

        "card":
            card,

        "spending":
            generate_spending_data(),

        "linked_account":
            random.choice([
                "PayPal balance",
                "Chase Bank •••• 2735",
                "KB Bank •••• 5121",
                "Citibank •••• 9044",
            ]),

        "transactions": [
            generate_card_transaction(
                index
            )
            for index in range(
                random.randint(
                    5,
                    9,
                )
            )
        ],

        "online_payments_enabled":
            random.choice([
                True,
                False,
            ]),

        "contactless_enabled":
            random.choice([
                True,
                True,
                False,
            ]),

        "international_enabled":
            random.choice([
                True,
                False,
            ]),

        "show_card_dialog":
            random.random()
            < 0.25,

        "navigation":
            NAVIGATION_ITEMS,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_card_detail_data()
    )