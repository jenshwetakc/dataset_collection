from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

ACCOUNT_STATES = [
    "overview",
    "profile_edit",
    "address_manager",
    "payment_manager",
    "security",
    "prime_member",
    "non_prime",
    "notifications",
    "signout_dialog",
    "delete_account_dialog",
]


# ==========================================================
# Main Generator
# ==========================================================

def generate_account_data() -> dict:

    state = random.choice(
        ACCOUNT_STATES
    )

    prime_member = (
        state == "prime_member"
        or (
            state != "non_prime"
            and random.random() < 0.65
        )
    )

    addresses = [
        {
            "label": "Home",
            "name": "Alex Morgan",
            "line1": "24 Maple Street",
            "line2": "Apartment 302",
            "city": "Seoul",
            "postal_code": "02841",
            "default": True,
        },
        {
            "label": "Office",
            "name": "Alex Morgan",
            "line1": "101 Central Avenue",
            "line2": "Office 8F",
            "city": "Seoul",
            "postal_code": "04524",
            "default": False,
        },
    ]

    payment_methods = [
        {
            "type": "Visa",
            "ending": "4242",
            "icon": "credit_card",
            "default": True,
        },
        {
            "type": "Mastercard",
            "ending": "7311",
            "icon": "credit_card",
            "default": False,
        },
    ]

    notification_settings = [
        {
            "label": "Order updates",
            "enabled": True,
        },
        {
            "label": "Delivery notifications",
            "enabled": True,
        },
        {
            "label": "Recommendations",
            "enabled": random.random() < 0.5,
        },
        {
            "label": "Deals and promotions",
            "enabled": random.random() < 0.5,
        },
    ]

    return {

        "state":
            state,

        "name":
            random.choice(
                [
                    "Alex Morgan",
                    "Jamie Lee",
                    "Taylor Kim",
                    "Morgan Park",
                ]
            ),

        "email":
            random.choice(
                [
                    "alex@example.com",
                    "jamie@example.com",
                    "taylor@example.com",
                ]
            ),

        "phone":
            random.choice(
                [
                    "+82 10-1234-5678",
                    "+82 10-8241-7293",
                    "+82 10-4432-1188",
                ]
            ),

        "prime_member":
            prime_member,

        "prime_renewal":
            random.choice(
                [
                    "Renews October 18",
                    "Renews November 5",
                    "Renews December 12",
                ]
            ),

        "addresses":
            addresses,

        "payment_methods":
            payment_methods,

        "notification_settings":
            notification_settings,

        "show_profile_dialog":
            (
                state == "profile_edit"
            ),

        "show_addresses":
            (
                state == "address_manager"
            ),

        "show_payments":
            (
                state == "payment_manager"
            ),

        "show_security":
            (
                state == "security"
            ),

        "show_notifications":
            (
                state == "notifications"
            ),

        "show_signout_dialog":
            (
                state == "signout_dialog"
            ),

        "show_delete_dialog":
            (
                state == "delete_account_dialog"
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_account_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON ACCOUNT GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Prime:",
        data["prime_member"],
    )

    print(
        "Addresses:",
        len(
            data["addresses"]
        ),
    )

    print(
        "Payments:",
        len(
            data["payment_methods"]
        ),
    )