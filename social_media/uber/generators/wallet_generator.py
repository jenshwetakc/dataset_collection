from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_payment_methods() -> list[dict]:

    methods = [
        {
            "type": "card",
            "label": "Visa",
            "subtitle": f"•••• {random.randint(1000, 9999)}",
            "icon": "credit_card",
        },
        {
            "type": "card",
            "label": "Mastercard",
            "subtitle": f"•••• {random.randint(1000, 9999)}",
            "icon": "credit_card",
        },
        {
            "type": "cash",
            "label": "Uber Cash",
            "subtitle": "Use your Uber Cash balance",
            "icon": "account_balance_wallet",
        },
    ]

    selected_index = random.randint(
        0,
        len(methods) - 1,
    )

    for index, method in enumerate(methods):

        method["selected"] = (
            index == selected_index
        )

    return methods


def generate_transactions() -> list[dict]:

    transaction_count = random.randint(
        6,
        11,
    )

    transactions = []

    now = datetime.now()


    for index in range(
        transaction_count
    ):

        transaction_type = random.choice(
            [
                "ride",
                "ride",
                "top_up",
                "refund",
                "promotion",
            ]
        )

        date = (
            now
            - timedelta(
                days=random.randint(
                    0,
                    28,
                )
            )
        )

        if transaction_type == "ride":

            amount = random.uniform(
                8,
                42,
            )

            transactions.append(
                {
                    "title":
                        random.choice(
                            [
                                "UberX trip",
                                "Comfort trip",
                                "Uber Green trip",
                                "UberXL trip",
                            ]
                        ),

                    "subtitle":
                        fake.street_name(),

                    "date":
                        date.strftime(
                            "%b %d"
                        ),

                    "amount":
                        f"-${amount:.2f}",

                    "positive":
                        False,

                    "icon":
                        "directions_car",
                }
            )

        elif transaction_type == "top_up":

            amount = random.choice(
                [
                    10,
                    20,
                    25,
                    50,
                ]
            )

            transactions.append(
                {
                    "title":
                        "Uber Cash top up",

                    "subtitle":
                        "Added to balance",

                    "date":
                        date.strftime(
                            "%b %d"
                        ),

                    "amount":
                        f"+${amount:.2f}",

                    "positive":
                        True,

                    "icon":
                        "add_card",
                }
            )

        elif transaction_type == "refund":

            amount = random.uniform(
                4,
                22,
            )

            transactions.append(
                {
                    "title":
                        "Trip refund",

                    "subtitle":
                        "Refund completed",

                    "date":
                        date.strftime(
                            "%b %d"
                        ),

                    "amount":
                        f"+${amount:.2f}",

                    "positive":
                        True,

                    "icon":
                        "undo",
                }
            )

        else:

            amount = random.uniform(
                3,
                12,
            )

            transactions.append(
                {
                    "title":
                        "Promotion credit",

                    "subtitle":
                        "Uber promotion",

                    "date":
                        date.strftime(
                            "%b %d"
                        ),

                    "amount":
                        f"+${amount:.2f}",

                    "positive":
                        True,

                    "icon":
                        "redeem",
                }
            )


    return transactions


# ==========================================================
# Main Generator
# ==========================================================

def generate_wallet_data() -> dict:

    balance = random.uniform(
        4,
        180,
    )

    selected_top_up = random.choice(
        [
            10,
            20,
            25,
            50,
        ]
    )


    return {

        "title":
            "Wallet",

        "balance": {

            "label":
                "Uber Cash",

            "amount":
                f"${balance:.2f}",

            "subtitle":
                random.choice(
                    [
                        "Available for rides",
                        "Your Uber Cash balance",
                        "Ready to use",
                    ]
                ),
        },

        "top_up_options": [

            {
                "value":
                    value,

                "label":
                    f"${value}",

                "selected":
                    value
                    == selected_top_up,
            }

            for value
            in [
                10,
                20,
                25,
                50,
            ]
        ],

        "payment_methods":
            generate_payment_methods(),

        "transactions":
            generate_transactions(),

        "promo": {

            "title":
                random.choice(
                    [
                        "Add promo code",
                        "Promotions",
                        "Uber credits",
                    ]
                ),

            "subtitle":
                random.choice(
                    [
                        "Enter a promo or gift code",
                        "Save on your next ride",
                        "Manage promotions and credits",
                    ]
                ),

            "icon":
                "redeem",

            "badge":
                random.choice(
                    [
                        None,
                        "New",
                        None,
                    ]
                ),
        },

        "auto_reload": {

            "enabled":
                random.choice(
                    [
                        True,
                        False,
                    ]
                ),

            "title":
                "Auto reload",

            "subtitle":
                "Automatically add Uber Cash when your balance gets low",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_wallet_data()
    )