from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_avatar,
    get_random_merchant_image,
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


TRANSACTION_TYPES = [
    "purchase",
    "sent",
    "received",
    "refund",
    "subscription",
]


STATUSES = [
    "Completed",
    "Completed",
    "Completed",
    "Pending",
    "Refunded",
]


MERCHANTS = [
    "Netflix",
    "Spotify",
    "Amazon",
    "Apple",
    "Adobe",
    "Uber",
    "Airbnb",
    "Starbucks",
    "Canva",
    "Dropbox",
]


CURRENCIES = [
    ("USD", "$"),
    ("EUR", "€"),
    ("GBP", "£"),
    ("KRW", "₩"),
]


# ==========================================================
# Amount
# ==========================================================

def generate_amount(
    currency_code: str,
    symbol: str,
) -> dict:

    if currency_code == "KRW":

        amount = random.randint(
            5000,
            500000,
        )

        formatted = (
            f"{symbol}{amount:,.0f}"
        )

    else:

        amount = round(
            random.uniform(
                5,
                900,
            ),
            2,
        )

        formatted = (
            f"{symbol}{amount:,.2f}"
        )

    return {
        "value": amount,
        "formatted": formatted,
    }


# ==========================================================
# Timeline
# ==========================================================

def generate_timeline(
    status: str,
) -> list[dict]:

    now = datetime.now()

    timeline = [
        {
            "title": "Payment created",
            "time": (
                now
                - timedelta(
                    minutes=15
                )
            ).strftime(
                "%I:%M %p"
            ).lstrip("0"),
            "complete": True,
        },
        {
            "title": "Payment authorized",
            "time": (
                now
                - timedelta(
                    minutes=10
                )
            ).strftime(
                "%I:%M %p"
            ).lstrip("0"),
            "complete": True,
        },
    ]

    if status == "Pending":

        timeline.append({
            "title": "Waiting for completion",
            "time": "Pending",
            "complete": False,
        })

    elif status == "Refunded":

        timeline.append({
            "title": "Payment completed",
            "time": (
                now
                - timedelta(
                    minutes=5
                )
            ).strftime(
                "%I:%M %p"
            ).lstrip("0"),
            "complete": True,
        })

        timeline.append({
            "title": "Refund issued",
            "time": now.strftime(
                "%I:%M %p"
            ).lstrip("0"),
            "complete": True,
        })

    else:

        timeline.append({
            "title": "Payment completed",
            "time": now.strftime(
                "%I:%M %p"
            ).lstrip("0"),
            "complete": True,
        })

    return timeline


# ==========================================================
# Main Generator
# ==========================================================

def generate_transaction_detail_data() -> dict:

    transaction_type = random.choice(
        TRANSACTION_TYPES
    )

    status = random.choice(
        STATUSES
    )

    currency_code, symbol = random.choice(
        CURRENCIES
    )

    amount = generate_amount(
        currency_code,
        symbol,
    )

    positive = (
        transaction_type
        in {
            "received",
            "refund",
        }
    )

    if transaction_type in {
        "sent",
        "received",
    }:

        counterparty = fake.name()

        image = get_random_avatar()

    else:

        counterparty = random.choice(
            MERCHANTS
            + [
                fake.company(),
            ]
        )

        image = get_random_merchant_image()

    if transaction_type == "received":

        description = "Money received"

        icon = "south_west"

    elif transaction_type == "sent":

        description = "Money sent"

        icon = "north_east"

    elif transaction_type == "refund":

        description = "Refund"

        icon = "undo"

    elif transaction_type == "subscription":

        description = "Automatic payment"

        icon = "autorenew"

    else:

        description = "Purchase"

        icon = "shopping_bag"

    timestamp = (
        datetime.now()
        - timedelta(
            days=random.randint(
                0,
                10,
            ),
            hours=random.randint(
                0,
                10,
            ),
        )
    )

    fee = random.choice([
        0.0,
        0.0,
        0.0,
        1.99,
        2.49,
    ])

    if positive:

        signed_amount = (
            "+"
            + amount["formatted"]
        )

    else:

        signed_amount = (
            "-"
            + amount["formatted"]
        )

    return {

        "transaction_type":
            transaction_type,

        "status":
            status,

        "positive":
            positive,

        "status_icon":
            (
                "schedule"
                if status == "Pending"
                else
                "undo"
                if status == "Refunded"
                else
                "check"
            ),

        "title":
            description,

        "counterparty":
            counterparty,

        "counterparty_image":
            image,

        "counterparty_initial":
            counterparty[0].upper(),

        "transaction_icon":
            icon,

        "amount":
            amount,

        "signed_amount":
            signed_amount,

        "currency":
            currency_code,

        "date":
            timestamp.strftime(
                "%B %d, %Y"
            ),

        "time":
            timestamp.strftime(
                "%I:%M %p"
            ).lstrip("0"),

        "transaction_id":
            fake.uuid4(),

        "note":
            random.choice([
                "",
                "Thanks!",
                "Dinner",
                "Subscription payment",
                "Online purchase",
                "Weekend trip",
            ]),

        "fee":
            (
                "No fee"
                if fee == 0
                else f"${fee:.2f}"
            ),

        "payment_method":
            random.choice([
                "PayPal balance",
                "Visa •••• 4821",
                "Mastercard •••• 7745",
                "Chase Bank •••• 2710",
                "KB Bank •••• 5192",
            ]),

        "timeline":
            generate_timeline(
                status
            ),

        "show_dialog":
            random.random()
            < 0.30,

        "dialog_type":
            random.choice([
                "report",
                "refund",
            ]),

        "navigation":
            NAVIGATION_ITEMS,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_transaction_detail_data()
    )