from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

WALLET_STATES = [

    "wallet_home",

    "card_detail",

    "transactions",

    "passes",

    "add_card",

    "apple_pay_sheet",

    "payment_success",

    "payment_declined",
]


WALLET_STATE_WEIGHTS = [

    24,

    14,

    14,

    12,

    10,

    12,

    8,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Card Definitions
# ==========================================================

CARD_STYLES = [

    {
        "style":
            "blue",

        "brand":
            "VISA",
    },

    {
        "style":
            "dark",

        "brand":
            "Mastercard",
    },

    {
        "style":
            "gold",

        "brand":
            "VISA",
    },

    {
        "style":
            "purple",

        "brand":
            "AMEX",
    },
]


# ==========================================================
# Payment Card
# ==========================================================

def generate_payment_card(
    index: int,
) -> dict:

    definition = random.choice(
        CARD_STYLES
    )


    return {

        "id":
            f"card_{index}",

        "name":
            random.choice([
                "Everyday Card",
                "Travel Card",
                "Rewards Card",
                "Student Card",
            ]),

        "bank":
            random.choice([
                "Korea Bank",
                "Global Bank",
                "City Bank",
                "Prime Financial",
            ]),

        "last4":
            f"{random.randint(0, 9999):04d}",

        "brand":
            definition["brand"],

        "style":
            definition["style"],

        "balance":
            random.randint(
                120,
                5200,
            ),

        "default":
            index == 0,

        "contactless":
            True,
    }


# ==========================================================
# Cards
# ==========================================================

def generate_cards() -> list[dict]:

    return [

        generate_payment_card(
            index
        )

        for index
        in range(
            3
        )
    ]


# ==========================================================
# Transaction
# ==========================================================

def generate_transaction(
    index: int,
) -> dict:

    merchants = [

        (
            "Coffee House",
            "coffee",
        ),

        (
            "Metro",
            "train",
        ),

        (
            "App Store",
            "smartphone",
        ),

        (
            "Grocery Market",
            "shopping-basket",
        ),

        (
            "Restaurant",
            "utensils",
        ),

        (
            "Book Store",
            "book-open",
        ),

        (
            "Taxi",
            "car",
        ),

        (
            "Online Shop",
            "shopping-bag",
        ),
    ]


    merchant, icon_name = random.choice(
        merchants
    )


    amount = random.uniform(
        3.0,
        180.0,
    )


    return {

        "id":
            f"transaction_{index}",

        "merchant":
            merchant,

        "icon":
            get_lucide_icon(
                icon_name
            ),

        "amount":
            f"${amount:.2f}",

        "time":
            random.choice([
                "Today, 9:41 AM",
                "Today, 11:18 AM",
                "Yesterday",
                "Friday",
                "Sep 3",
            ]),

        "status":
            random.choice([
                "Completed",
                "Completed",
                "Completed",
                "Pending",
            ]),

        "location":
            random.choice([
                "Seoul",
                "Online",
                "Campus",
                "Downtown",
            ]),
    }


# ==========================================================
# Transactions
# ==========================================================

def generate_transactions() -> list[dict]:

    return [

        generate_transaction(
            index
        )

        for index
        in range(
            10
        )
    ]


# ==========================================================
# Passes
# ==========================================================

def generate_passes() -> list[dict]:

    return [

        {
            "id":
                "boarding_pass",

            "title":
                "Boarding Pass",

            "subtitle":
                "Seoul → Tokyo",

            "detail":
                "Gate 18 · 14:35",

            "style":
                "blue",

            "icon":
                get_lucide_icon(
                    "plane"
                ),
        },

        {
            "id":
                "transit",

            "title":
                "Transit Card",

            "subtitle":
                "Metro",

            "detail":
                "Balance ₩24,500",

            "style":
                "green",

            "icon":
                get_lucide_icon(
                    "train"
                ),
        },

        {
            "id":
                "event",

            "title":
                "Conference",

            "subtitle":
                "Technology Summit",

            "detail":
                "Sep 18 · Hall B",

            "style":
                "purple",

            "icon":
                get_lucide_icon(
                    "ticket"
                ),
        },

        {
            "id":
                "membership",

            "title":
                "Membership",

            "subtitle":
                "Fitness Club",

            "detail":
                "Member #48291",

            "style":
                "orange",

            "icon":
                get_lucide_icon(
                    "badge"
                ),
        },
    ]


# ==========================================================
# Add Card
# ==========================================================

def generate_add_card() -> dict:

    return {

        "card_number":
            random.choice([
                "",
                "•••• •••• •••• 3482",
            ]),

        "name":
            random.choice([
                "",
                fake.name(),
            ]),

        "expiration":
            random.choice([
                "",
                "09/30",
            ]),

        "security_code":
            "",
    }


# ==========================================================
# Apple Pay
# ==========================================================

def generate_payment_sheet(
    card: dict,
) -> dict:

    merchants = [

        "Coffee House",

        "Online Store",

        "Transit",

        "Restaurant",
    ]


    amount = random.uniform(
        6,
        120,
    )


    return {

        "merchant":
            random.choice(
                merchants
            ),

        "amount":
            f"${amount:.2f}",

        "card":
            card,

        "shipping":
            random.choice([
                None,
                "Home",
                "Campus",
            ]),

        "requires_side_button":
            True,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_wallet_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choices(

            WALLET_STATES,

            weights=
                WALLET_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in WALLET_STATES:

        raise ValueError(
            f"Unknown Wallet state: {state}"
        )


    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    cards = generate_cards()


    active_card = random.choice(
        cards
    )


    transactions = (
        generate_transactions()
    )


    is_overlay_state = (
        state
        in {
            "add_card",
            "apple_pay_sheet",
            "payment_success",
            "payment_declined",
        }
    )


    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "cards":
            cards,

        "active_card":
            active_card,

        "transactions":
            transactions,

        "passes":
            generate_passes(),


        "add_card":
            generate_add_card(),


        "payment":
            generate_payment_sheet(
                active_card
            ),


        "payment_success": {

            "title":
                "Done",

            "message":
                "Payment Complete",
        },


        "payment_declined": {

            "title":
                "Payment Not Completed",

            "message":
                (
                    "Your card issuer declined "
                    "this transaction."
                ),

            "action":
                "Try Another Card",
        },


        "icons": {

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis"
                ),

            "back":
                resolve_icon(
                    "back",
                    "chevron-left"
                ),

            "card":
                get_lucide_icon(
                    "credit-card"
                ),

            "wallet":
                get_lucide_icon(
                    "wallet-cards"
                ),

            "contactless":
                get_lucide_icon(
                    "contactless"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "lock":
                resolve_icon(
                    "lock"
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right"
                ),

            "info":
                resolve_icon(
                    "info"
                ),

            "history":
                get_lucide_icon(
                    "history"
                ),

            "ticket":
                get_lucide_icon(
                    "ticket"
                ),

            "scan":
                get_lucide_icon(
                    "scan-line"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in WALLET_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_wallet_data(
                state=
                    state
            ),

            sort_dicts=False,
        )