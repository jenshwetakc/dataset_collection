from __future__ import annotations

import random

from faker import Faker

from social_media.baemin.generators.media_generator import (
    get_random_avatar,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Pools
# ==========================================================

MEMBERSHIP_LEVELS = [
    "Basic",
    "Silver",
    "Gold",
    "VIP",
]


PAYMENT_METHODS = [
    {
        "name": "Baemin Pay",
        "icon": "account_balance_wallet",
    },
    {
        "name": "Credit card",
        "icon": "credit_card",
    },
    {
        "name": "Kakao Pay",
        "icon": "payments",
    },
    {
        "name": "Naver Pay",
        "icon": "account_balance",
    },
]


QUICK_ACTIONS = [
    {
        "title": "Orders",
        "icon": "receipt_long",
        "semantic": "profile_orders",
    },
    {
        "title": "Favorites",
        "icon": "favorite",
        "semantic": "profile_favorites",
    },
    {
        "title": "Coupons",
        "icon": "confirmation_number",
        "semantic": "profile_coupons",
    },
    {
        "title": "Reviews",
        "icon": "rate_review",
        "semantic": "profile_reviews",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_phone() -> str:

    return (
        f"010-"
        f"{random.randint(1000, 9999)}-"
        f"{random.randint(1000, 9999)}"
    )


def generate_address() -> str:

    district = random.choice(
        [
            "Gangnam-gu",
            "Mapo-gu",
            "Songpa-gu",
            "Jongno-gu",
            "Seocho-gu",
            "Yongsan-gu",
        ]
    )

    return (
        f"{random.randint(1, 250)} "
        f"{fake.street_name()}, "
        f"{district}, Seoul"
    )


# ==========================================================
# Main Generator
# ==========================================================

def generate_profile_data() -> dict:

    membership = random.choice(
        MEMBERSHIP_LEVELS
    )

    points = random.randint(
        200,
        18000,
    )

    coupons = random.randint(
        0,
        14,
    )

    user_name = fake.name()

    return {

        # ==================================================
        # User
        # ==================================================

        "user": {

            "name":
                user_name,

            "avatar":
                (
                    get_random_avatar()
                    if random.random() < 0.85
                    else None
                ),

            "email":
                fake.email(),

            "phone":
                generate_phone(),

            "member_since":
                fake.date_between(
                    start_date="-5y",
                    end_date="-2M",
                ).strftime(
                    "%b %Y"
                ),

            "membership":
                membership,
        },


        # ==================================================
        # Rewards
        # ==================================================

        "rewards": {

            "points":
                points,

            "points_text":
                f"{points:,} P",

            "coupons":
                coupons,

            "coupon_text":
                f"{coupons} coupons",

            "progress":
                random.randint(
                    15,
                    90,
                ),

            "next_level":
                random.choice(
                    [
                        "Silver",
                        "Gold",
                        "VIP",
                    ]
                ),
        },


        # ==================================================
        # Quick Actions
        # ==================================================

        "quick_actions":
            QUICK_ACTIONS,


        # ==================================================
        # Payment
        # ==================================================

        "payment": {

            **random.choice(
                PAYMENT_METHODS
            ),

            "detail":
                random.choice(
                    [
                        "•••• 4821",
                        "Default payment",
                        "Connected",
                        "Ready to use",
                    ]
                ),
        },


        # ==================================================
        # Address
        # ==================================================

        "address": {

            "label":
                random.choice(
                    [
                        "Home",
                        "Work",
                        "Apartment",
                    ]
                ),

            "address":
                generate_address(),

            "detail":
                random.choice(
                    [
                        "Apartment 1204",
                        "Building B, Room 302",
                        "Leave at front door",
                    ]
                ),
        },


        # ==================================================
        # Preferences
        # ==================================================

        "preferences": {

            "notifications":
                random.random()
                < 0.75,

            "marketing":
                random.random()
                < 0.35,

            "dark_mode":
                random.random()
                < 0.45,

            "location":
                random.random()
                < 0.80,
        },


        # ==================================================
        # Misc
        # ==================================================

        "notification_count":
            random.randint(
                0,
                12,
            ),

        "new_feature":
            random.random()
            < 0.5,

        "version":
            f"{random.randint(6, 8)}."
            f"{random.randint(0, 9)}."
            f"{random.randint(0, 9)}",
    }