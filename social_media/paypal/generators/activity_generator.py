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


TABS = [
    {
        "label": "All",
        "semantic": "all",
    },
    {
        "label": "Money in",
        "semantic": "money_in",
    },
    {
        "label": "Money out",
        "semantic": "money_out",
    },
]


FILTERS = [
    {
        "label": "Date",
        "icon": "calendar_month",
        "semantic": "date",
    },
    {
        "label": "Status",
        "icon": "check_circle",
        "semantic": "status",
    },
    {
        "label": "Type",
        "icon": "tune",
        "semantic": "type",
    },
]


TRANSACTION_TYPES = [
    "payment",
    "received",
    "sent",
    "refund",
    "purchase",
    "subscription",
    "withdrawal",
    "deposit",
]


STATUSES = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Pending",
    "Refunded",
    "Cancelled",
]


MERCHANTS = [
    "Netflix",
    "Spotify",
    "Apple",
    "Amazon",
    "Adobe",
    "Uber",
    "Airbnb",
    "Starbucks",
    "Dropbox",
    "Canva",
    "Microsoft",
    "Steam",
]


CURRENCIES = [
    ("USD", "$"),
    ("EUR", "€"),
    ("GBP", "£"),
    ("KRW", "₩"),
]


# ==========================================================
# Transaction Helpers
# ==========================================================

def generate_transaction(
    index: int,
    day_offset: int,
) -> dict:

    transaction_type = random.choice(
        TRANSACTION_TYPES
    )

    status = random.choice(
        STATUSES
    )

    currency_code, symbol = random.choice(
        CURRENCIES
    )

    if currency_code == "KRW":

        amount = random.randint(
            1000,
            500000,
        )

        formatted_amount = (
            f"{symbol}{amount:,.0f}"
        )

    else:

        amount = round(
            random.uniform(
                2,
                900,
            ),
            2,
        )

        formatted_amount = (
            f"{symbol}{amount:,.2f}"
        )

    positive = (
        transaction_type
        in {
            "received",
            "refund",
            "deposit",
        }
    )

    if positive:

        formatted_amount = (
            "+"
            + formatted_amount
        )

    else:

        formatted_amount = (
            "-"
            + formatted_amount
        )

    timestamp = (
        datetime.now()
        - timedelta(
            days=day_offset,
            hours=random.randint(
                0,
                20,
            ),
            minutes=random.randint(
                0,
                59,
            ),
        )
    )

    if transaction_type == "received":

        title = fake.name()

        description = random.choice([
            "Money received",
            "Payment received",
            "Transfer received",
        ])

        icon = "south_west"

    elif transaction_type == "sent":

        title = fake.name()

        description = "Money sent"

        icon = "north_east"

    elif transaction_type == "refund":

        title = random.choice(
            MERCHANTS
        )

        description = "Refund"

        icon = "undo"

    elif transaction_type == "subscription":

        title = random.choice(
            MERCHANTS
        )

        description = "Automatic payment"

        icon = "autorenew"

    elif transaction_type == "withdrawal":

        title = random.choice([
            "Bank transfer",
            "Transfer to bank",
        ])

        description = "Withdrawal"

        icon = "account_balance"

    elif transaction_type == "deposit":

        title = random.choice([
            "Bank transfer",
            "Add money",
        ])

        description = "Deposit"

        icon = "account_balance"

    else:

        title = random.choice(
            MERCHANTS
            + [
                fake.company(),
            ]
        )

        description = random.choice([
            "Payment",
            "Purchase",
            "Online purchase",
        ])

        icon = "shopping_bag"

    image = (
        get_random_merchant_image()
        or (
            get_random_avatar()
            if transaction_type
            in {
                "received",
                "sent",
            }
            else None
        )
    )

    return {
        "id":
            index,

        "title":
            title,

        "description":
            description,

        "type":
            transaction_type,

        "status":
            status,

        "currency":
            currency_code,

        "amount":
            amount,

        "formatted_amount":
            formatted_amount,

        "positive":
            positive,

        "date":
            timestamp.strftime(
                "%b %d, %Y"
            ),

        "time":
            timestamp.strftime(
                "%I:%M %p"
            ).lstrip("0"),

        "icon":
            icon,

        "image":
            image,
    }


# ==========================================================
# Activity Groups
# ==========================================================

def generate_activity_groups() -> list[dict]:

    groups = []

    transaction_index = 0

    day_offsets = [
        0,
        1,
        2,
        random.randint(
            3,
            6,
        ),
        random.randint(
            7,
            14,
        ),
    ]

    for group_index, day_offset in enumerate(
        day_offsets
    ):

        if day_offset == 0:

            label = "Today"

        elif day_offset == 1:

            label = "Yesterday"

        else:

            date = (
                datetime.now()
                - timedelta(
                    days=day_offset
                )
            )

            label = date.strftime(
                "%B %d"
            )

        count = random.randint(
            2,
            5,
        )

        transactions = []

        for _ in range(
            count
        ):

            transactions.append(
                generate_transaction(
                    transaction_index,
                    day_offset,
                )
            )

            transaction_index += 1

        groups.append({
            "id":
                group_index,

            "label":
                label,

            "transactions":
                transactions,
        })

    return groups


# ==========================================================
# Summary
# ==========================================================

def generate_summary() -> dict:

    incoming = round(
        random.uniform(
            500,
            7500,
        ),
        2,
    )

    outgoing = round(
        random.uniform(
            300,
            6500,
        ),
        2,
    )

    return {
        "incoming":
            f"${incoming:,.2f}",

        "outgoing":
            f"${outgoing:,.2f}",

        "net":
            f"${incoming - outgoing:,.2f}",

        "transaction_count":
            random.randint(
                20,
                120,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_activity_data() -> dict:

    return {
        "title":
            random.choice([
                "Activity",
                "Recent activity",
                "Transactions",
            ]),

        "subtitle":
            random.choice([
                "Track your recent payments and transfers.",
                "See where your money has been going.",
                "Review your PayPal activity.",
            ]),

        "search_placeholder":
            random.choice([
                "Search transactions",
                "Search activity",
                "Search by name or amount",
            ]),

        "tabs":
            TABS,

        "filters":
            FILTERS,

        "summary":
            generate_summary(),

        "groups":
            generate_activity_groups(),

        "navigation":
            NAVIGATION_ITEMS,

        "show_summary":
            random.random()
            < 0.75,

        "active_filter_count":
            random.choice([
                0,
                0,
                1,
                2,
            ]),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_activity_data()
    )