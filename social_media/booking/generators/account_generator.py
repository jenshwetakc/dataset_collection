from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_avatar,
)


# ==========================================================
# States
# ==========================================================

ACCOUNT_STATES = [
    "overview",
    "edit_profile",
    "payment_methods",
    "security",
    "notifications",
    "signout_confirm",
]


FIRST_NAMES = [
    "Alex",
    "Emma",
    "Daniel",
    "Mina",
    "Sophie",
    "Lucas",
]


LAST_NAMES = [
    "Kim",
    "Park",
    "Lee",
    "Smith",
    "Martin",
    "Brown",
]


COUNTRIES = [
    "South Korea",
    "Japan",
    "United States",
    "United Kingdom",
    "France",
    "Germany",
]


CARD_BRANDS = [
    "Visa",
    "Mastercard",
    "American Express",
]


# ==========================================================
# Payment Method
# ==========================================================

def generate_payment_method() -> dict:

    brand = random.choice(
        CARD_BRANDS
    )

    return {
        "brand":
            brand,

        "last_four":
            f"{random.randint(1000, 9999)}",

        "expiry":
            random.choice(
                [
                    "08/27",
                    "11/27",
                    "03/28",
                    "06/29",
                ]
            ),

        "default":
            random.random() < 0.40,
    }


# ==========================================================
# Notification Setting
# ==========================================================

def generate_notification_settings() -> list[dict]:

    return [
        {
            "title":
                "Booking confirmations",

            "description":
                "Receive confirmation and important booking updates.",

            "enabled":
                True,
        },
        {
            "title":
                "Price alerts",

            "description":
                "Get alerts when prices change for saved trips.",

            "enabled":
                random.random() < 0.65,
        },
        {
            "title":
                "Travel offers",

            "description":
                "Receive occasional deals and recommendations.",

            "enabled":
                random.random() < 0.50,
        },
        {
            "title":
                "Trip reminders",

            "description":
                "Receive reminders before your upcoming stay.",

            "enabled":
                random.random() < 0.75,
        },
    ]


# ==========================================================
# Main
# ==========================================================

def generate_account_data() -> dict:

    state = random.choice(
        ACCOUNT_STATES
    )

    first_name = random.choice(
        FIRST_NAMES
    )

    last_name = random.choice(
        LAST_NAMES
    )

    payment_methods = [
        generate_payment_method()
        for _ in range(
            random.randint(
                2,
                3,
            )
        )
    ]

    if payment_methods:

        payment_methods[0][
            "default"
        ] = True

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "overview":
            state == "overview",

        "edit_profile":
            state == "edit_profile",

        "payment_methods_open":
            state == "payment_methods",

        "security_open":
            state == "security",

        "notifications_open":
            state == "notifications",

        "signout_confirm":
            state == "signout_confirm",

        # ------------------------------------------
        # User
        # ------------------------------------------

        "user": {

            "first_name":
                first_name,

            "last_name":
                last_name,

            "full_name":
                (
                    f"{first_name} "
                    f"{last_name}"
                ),

            "email":
                "traveler@example.com",

            "phone":
                "+82 10 1234 5678",

            "country":
                random.choice(
                    COUNTRIES
                ),

            "avatar":
                get_random_avatar(),

            "member_since":
                random.choice(
                    [
                        "2022",
                        "2023",
                        "2024",
                        "2025",
                    ]
                ),
        },

        # ------------------------------------------
        # Stats
        # ------------------------------------------

        "stats": {

            "bookings":
                random.randint(
                    3,
                    24,
                ),

            "saved":
                random.randint(
                    2,
                    18,
                ),

            "reviews":
                random.randint(
                    0,
                    12,
                ),
        },

        # ------------------------------------------
        # Payment
        # ------------------------------------------

        "payment_methods":
            payment_methods,

        # ------------------------------------------
        # Notifications
        # ------------------------------------------

        "notifications":
            generate_notification_settings(),

        # ------------------------------------------
        # Security
        # ------------------------------------------

        "security": {

            "two_factor":
                random.random()
                < 0.45,

            "last_password_change":
                random.choice(
                    [
                        "2 weeks ago",
                        "1 month ago",
                        "3 months ago",
                    ]
                ),

            "sessions":
                random.randint(
                    1,
                    4,
                ),
        },

        # ------------------------------------------
        # Navigation
        # ------------------------------------------

        "sections": [
            {
                "label":
                    "Overview",

                "icon":
                    "person",

                "state":
                    "overview",
            },
            {
                "label":
                    "Personal details",

                "icon":
                    "badge",

                "state":
                    "edit_profile",
            },
            {
                "label":
                    "Payment methods",

                "icon":
                    "credit_card",

                "state":
                    "payment_methods",
            },
            {
                "label":
                    "Security",

                "icon":
                    "shield",

                "state":
                    "security",
            },
            {
                "label":
                    "Notifications",

                "icon":
                    "notifications",

                "state":
                    "notifications",
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_account_data()
    )

    print(
        "State:",
        data[
            "state"
        ],
    )

    print(
        "User:",
        data[
            "user"
        ][
            "full_name"
        ],
    )