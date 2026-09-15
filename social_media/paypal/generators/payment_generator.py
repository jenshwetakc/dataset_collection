from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_avatar,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Constants
# ==========================================================

CURRENCIES = [
    {
        "code": "USD",
        "symbol": "$",
        "label": "US Dollar",
    },
    {
        "code": "EUR",
        "symbol": "€",
        "label": "Euro",
    },
    {
        "code": "GBP",
        "symbol": "£",
        "label": "British Pound",
    },
    {
        "code": "KRW",
        "symbol": "₩",
        "label": "Korean Won",
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


PAYMENT_METHOD_TYPES = [
    "visa",
    "mastercard",
    "bank",
    "balance",
]


# ==========================================================
# Recipient
# ==========================================================

def generate_recipient() -> dict:

    name = fake.name()

    return {
        "name":
            name,

        "email":
            fake.email(),

        "avatar":
            get_random_avatar(),

        "initial":
            name[0].upper(),
    }


# ==========================================================
# Payment Method
# ==========================================================

def generate_payment_method(
    index: int,
) -> dict:

    method_type = random.choice(
        PAYMENT_METHOD_TYPES
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

    if method_type == "balance":

        label = "PayPal balance"

        subtitle = random.choice([
            "$1,284.62 available",
            "$640.15 available",
            "$3,420.90 available",
        ])

        icon = "account_balance_wallet"

    elif method_type == "bank":

        bank = random.choice([
            "Chase Bank",
            "KB Bank",
            "Shinhan Bank",
            "Citibank",
            "Woori Bank",
        ])

        label = bank

        subtitle = (
            "Bank •••• "
            + last_four
        )

        icon = "account_balance"

    elif method_type == "mastercard":

        label = "Mastercard"

        subtitle = (
            "•••• "
            + last_four
        )

        icon = "credit_card"

    else:

        label = "Visa"

        subtitle = (
            "•••• "
            + last_four
        )

        icon = "credit_card"

    return {
        "id":
            index,

        "type":
            method_type,

        "label":
            label,

        "subtitle":
            subtitle,

        "icon":
            icon,

        "selected":
            index == 0,
    }


# ==========================================================
# Amount
# ==========================================================

def generate_amount(
    currency: dict,
) -> dict:

    if currency["code"] == "KRW":

        value = random.choice([
            10000,
            25000,
            50000,
            75000,
            100000,
            250000,
        ])

        formatted = (
            f"{value:,.0f}"
        )

    else:

        value = round(
            random.uniform(
                5,
                500,
            ),
            2,
        )

        formatted = (
            f"{value:,.2f}"
        )

    return {
        "value":
            value,

        "formatted":
            formatted,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_payment_data() -> dict:

    currency = random.choice(
        CURRENCIES
    )

    amount = generate_amount(
        currency
    )

    payment_methods = [
        generate_payment_method(
            index
        )
        for index
        in range(
            random.randint(
                3,
                5,
            )
        )
    ]

    fee = random.choice([
        0.00,
        0.00,
        0.00,
        1.99,
        2.49,
    ])

    return {

        # ------------------------------------------------------
        # Recipient
        # ------------------------------------------------------

        "recipient":
            generate_recipient(),


        # ------------------------------------------------------
        # Amount
        # ------------------------------------------------------

        "currency":
            currency,

        "amount":
            amount,


        # ------------------------------------------------------
        # Note
        # ------------------------------------------------------

        "note_placeholder":
            random.choice([
                "Add a note",
                "What's this payment for?",
                "Write a message",
            ]),


        # ------------------------------------------------------
        # Funding
        # ------------------------------------------------------

        "payment_methods":
            payment_methods,


        # ------------------------------------------------------
        # Summary
        # ------------------------------------------------------

        "fee":
            fee,

        "fee_text":
            (
                "No fee"
                if fee == 0
                else f"${fee:.2f}"
            ),

        "total":
            (
                amount["value"]
                + fee
            ),


        # ------------------------------------------------------
        # UI Text
        # ------------------------------------------------------

        "title":
            random.choice([
                "Send money",
                "Review payment",
                "Send payment",
            ]),

        "continue_label":
            random.choice([
                "Continue",
                "Review",
                "Next",
            ]),

        "send_label":
            random.choice([
                "Send now",
                "Send payment",
                "Pay",
            ]),


        # ------------------------------------------------------
        # Optional Sheet
        # ------------------------------------------------------

        "show_payment_sheet":
            random.random()
            < 0.35,


        # ------------------------------------------------------
        # Navigation
        # ------------------------------------------------------

        "navigation":
            NAVIGATION_ITEMS,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_payment_data()
    )