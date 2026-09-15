from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_avatar,
    get_random_banner,
    get_random_card_image,
    get_random_merchant_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Constants
# ==========================================================

CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "KRW",
    "CAD",
    "AUD",
]


CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "KRW": "₩",
    "CAD": "$",
    "AUD": "$",
}


TRANSACTION_TYPES = [
    "payment",
    "received",
    "sent",
    "refund",
    "subscription",
    "purchase",
]


TRANSACTION_STATUSES = [
    "completed",
    "completed",
    "completed",
    "completed",
    "pending",
    "refunded",
]


MERCHANT_CATEGORIES = [
    "Shopping",
    "Food & Drink",
    "Entertainment",
    "Transportation",
    "Bills",
    "Subscription",
    "Services",
    "Transfer",
]


MERCHANT_NAMES = [
    "Netflix",
    "Spotify",
    "Adobe",
    "Uber",
    "Airbnb",
    "Apple",
    "Google",
    "Amazon",
    "Starbucks",
    "Steam",
    "Dropbox",
    "Canva",
    "Notion",
    "Microsoft",
]


QUICK_ACTIONS = [
    {
        "label": "Send",
        "icon": "arrow_upward",
        "semantic": "send_money",
    },
    {
        "label": "Request",
        "icon": "arrow_downward",
        "semantic": "request_money",
    },
    {
        "label": "Scan",
        "icon": "qr_code_scanner",
        "semantic": "scan_qr",
    },
    {
        "label": "More",
        "icon": "more_horiz",
        "semantic": "more_actions",
    },
]


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


# ==========================================================
# Helpers
# ==========================================================

def format_money(
    amount: float,
    currency: str,
) -> str:

    symbol = CURRENCY_SYMBOLS.get(
        currency,
        "$",
    )

    if currency == "KRW":

        return (
            f"{symbol}"
            f"{amount:,.0f}"
        )

    return (
        f"{symbol}"
        f"{amount:,.2f}"
    )


def generate_balance() -> dict:

    currency = random.choice(
        CURRENCIES
    )

    if currency == "KRW":

        amount = random.randint(
            10000,
            8500000,
        )

    else:

        amount = round(
            random.uniform(
                20,
                12000,
            ),
            2,
        )

    return {
        "amount": amount,
        "currency": currency,
        "formatted": format_money(
            amount,
            currency,
        ),
        "available_text": random.choice([
            "Available balance",
            "PayPal balance",
            "Money available",
        ]),
    }


def generate_transaction(
    index: int,
) -> dict:

    transaction_type = random.choice(
        TRANSACTION_TYPES
    )

    status = random.choice(
        TRANSACTION_STATUSES
    )

    currency = random.choice(
        CURRENCIES
    )

    amount = round(
        random.uniform(
            2,
            750,
        ),
        2,
    )

    merchant = random.choice(
        MERCHANT_NAMES
        + [
            fake.company(),
            fake.name(),
        ]
    )

    category = random.choice(
        MERCHANT_CATEGORIES
    )

    days_ago = random.randint(
        0,
        30,
    )

    hours_ago = random.randint(
        0,
        23,
    )

    timestamp = (
        datetime.now()
        - timedelta(
            days=days_ago,
            hours=hours_ago,
        )
    )

    positive = (
        transaction_type
        in {
            "received",
            "refund",
        }
    )

    signed_amount = (
        amount
        if positive
        else -amount
    )

    if transaction_type == "received":

        description = random.choice([
            "Money received",
            "Payment received",
            "Transfer received",
        ])

        icon = "south_west"

    elif transaction_type == "sent":

        description = random.choice([
            "Money sent",
            "Payment sent",
            "Transfer sent",
        ])

        icon = "north_east"

    elif transaction_type == "refund":

        description = "Refund"

        icon = "undo"

    elif transaction_type == "subscription":

        description = "Automatic payment"

        icon = "autorenew"

    elif transaction_type == "purchase":

        description = random.choice([
            "Purchase",
            "Online purchase",
            "Payment",
        ])

        icon = "shopping_bag"

    else:

        description = "Payment"

        icon = "payments"

    merchant_image = (
        get_random_merchant_image()
    )

    avatar = (
        get_random_avatar()
    )

    return {
        "id": index,

        "merchant":
            merchant,

        "description":
            description,

        "category":
            category,

        "transaction_type":
            transaction_type,

        "status":
            status,

        "amount":
            amount,

        "signed_amount":
            signed_amount,

        "formatted_amount":
            (
                "+"
                if positive
                else "-"
            )
            + format_money(
                amount,
                currency,
            ),

        "currency":
            currency,

        "date":
            timestamp.strftime(
                "%b %d"
            ),

        "time":
            timestamp.strftime(
                "%I:%M %p"
            ).lstrip("0"),

        "icon":
            icon,

        "image":
            (
                merchant_image
                or avatar
            ),

        "positive":
            positive,
    }


def generate_payment_method(
    index: int,
) -> dict:

    method_type = random.choice([
        "visa",
        "mastercard",
        "bank",
    ])

    last_four = (
        str(
            random.randint(
                0,
                9999,
            )
        )
        .zfill(4)
    )

    if method_type == "bank":

        institution = random.choice([
            "Chase Bank",
            "Bank of America",
            "Wells Fargo",
            "Citibank",
            "KB Bank",
            "Shinhan Bank",
            "Woori Bank",
        ])

        label = institution

        icon = "account_balance"

    elif method_type == "mastercard":

        label = "Mastercard"

        icon = "credit_card"

    else:

        label = "Visa"

        icon = "credit_card"

    return {
        "id": index,
        "type": method_type,
        "label": label,
        "last_four": last_four,
        "icon": icon,
        "preferred": index == 0,
        "image": get_random_card_image(),
    }


def generate_promo() -> dict:

    promos = [
        {
            "title": "Shop and earn rewards",
            "description":
                "Explore personalized deals from brands you love.",
            "button": "Explore deals",
            "icon": "redeem",
        },
        {
            "title": "Pay in 4",
            "description":
                "Split eligible purchases into four payments.",
            "button": "Learn more",
            "icon": "calendar_month",
        },
        {
            "title": "Send money in seconds",
            "description":
                "Pay friends and family quickly and securely.",
            "button": "Send now",
            "icon": "send",
        },
        {
            "title": "Your money, your way",
            "description":
                "Manage cards, banks and your PayPal balance.",
            "button": "View wallet",
            "icon": "account_balance_wallet",
        },
    ]

    promo = dict(
        random.choice(
            promos
        )
    )

    promo[
        "image"
    ] = get_random_banner()

    return promo


# ==========================================================
# Main Generator
# ==========================================================

def generate_home_data() -> dict:

    first_name = fake.first_name()

    transaction_count = random.randint(
        7,
        18,
    )

    payment_method_count = random.randint(
        2,
        4,
    )

    return {

        # ------------------------------------------------------
        # User
        # ------------------------------------------------------

        "user": {
            "first_name":
                first_name,

            "full_name":
                fake.name(),

            "avatar":
                get_random_avatar(),

            "greeting":
                random.choice([
                    f"Hi, {first_name}",
                    f"Hello, {first_name}",
                    f"Good to see you, {first_name}",
                ]),
        },


        # ------------------------------------------------------
        # Balance
        # ------------------------------------------------------

        "balance":
            generate_balance(),


        # ------------------------------------------------------
        # Quick actions
        # ------------------------------------------------------

        "quick_actions":
            QUICK_ACTIONS,


        # ------------------------------------------------------
        # Activity
        # ------------------------------------------------------

        "transactions": [
            generate_transaction(
                index
            )
            for index
            in range(
                transaction_count
            )
        ],


        # ------------------------------------------------------
        # Wallet
        # ------------------------------------------------------

        "payment_methods": [
            generate_payment_method(
                index
            )
            for index
            in range(
                payment_method_count
            )
        ],


        # ------------------------------------------------------
        # Promotion
        # ------------------------------------------------------

        "promo":
            generate_promo(),


        # ------------------------------------------------------
        # Navigation
        # ------------------------------------------------------

        "navigation":
            NAVIGATION_ITEMS,


        # ------------------------------------------------------
        # Misc
        # ------------------------------------------------------

        "notification_count":
            random.randint(
                0,
                6,
            ),

        "search_placeholder":
            random.choice([
                "Search transactions",
                "Search activity",
                "Search PayPal",
            ]),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_home_data()
    )