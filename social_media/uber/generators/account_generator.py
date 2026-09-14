from __future__ import annotations

import random

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_driver_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_profile() -> dict:

    return {
        "name":
            fake.name(),

        "email":
            fake.email(),

        "rating":
            round(
                random.uniform(
                    4.6,
                    5.0,
                ),
                2,
            ),

        "ride_count":
            random.randint(
                42,
                3200,
            ),

        "avatar":
            get_random_driver_image(),
    }


def generate_wallet() -> dict:

    return {
        "balance":
            f"${random.uniform(0, 180):.2f}",

        "reward_points":
            random.randint(
                0,
                4800,
            ),
    }


def generate_account_data() -> dict:

    profile = generate_profile()
    wallet = generate_wallet()

    return {

        "title":
            "Account",

        "profile":
            profile,

        "wallet":
            wallet,

        "quick_actions": [
            {
                "label":
                    "Wallet",
                "subtitle":
                    wallet["balance"],
                "icon":
                    "account_balance_wallet",
                "badge":
                    None,
            },
            {
                "label":
                    "Payment methods",
                "subtitle":
                    "Manage cards and payment",
                "icon":
                    "credit_card",
                "badge":
                    None,
            },
            {
                "label":
                    "Saved places",
                "subtitle":
                    "Home, Work and more",
                "icon":
                    "bookmark",
                "badge":
                    random.choice(
                        [
                            None,
                            None,
                            "New",
                        ]
                    ),
            },
        ],

        "preferences": [
            {
                "type":
                    "switch",
                "label":
                    "Notifications",
                "subtitle":
                    "Trip updates and offers",
                "icon":
                    "notifications",
                "value":
                    random.choice(
                        [
                            True,
                            True,
                            False,
                        ]
                    ),
            },
            {
                "type":
                    "switch",
                "label":
                    "Ride updates",
                "subtitle":
                    "Pickup and arrival alerts",
                "icon":
                    "directions_car",
                "value":
                    random.choice(
                        [
                            True,
                            True,
                            False,
                        ]
                    ),
            },
            {
                "type":
                    "navigation",
                "label":
                    "Accessibility",
                "subtitle":
                    "Display and interaction settings",
                "icon":
                    "accessibility_new",
            },
        ],

        "safety": [
            {
                "label":
                    "Privacy",
                "subtitle":
                    "Control your data and permissions",
                "icon":
                    "lock",
            },
            {
                "label":
                    "Safety center",
                "subtitle":
                    "Safety tools and resources",
                "icon":
                    "shield",
                "badge":
                    random.choice(
                        [
                            None,
                            "Updated",
                            None,
                        ]
                    ),
            },
            {
                "label":
                    "Emergency contacts",
                "subtitle":
                    "Manage trusted contacts",
                "icon":
                    "emergency",
            },
        ],

        "support": [
            {
                "label":
                    "Help center",
                "subtitle":
                    "Get help with a trip or account",
                "icon":
                    "help",
            },
            {
                "label":
                    "About",
                "subtitle":
                    "App information and policies",
                "icon":
                    "info",
            },
        ],

        "navigation": [
            {
                "label":
                    "Home",
                "icon":
                    "home",
                "selected":
                    False,
            },
            {
                "label":
                    "Activity",
                "icon":
                    "receipt_long",
                "selected":
                    False,
            },
            {
                "label":
                    "Account",
                "icon":
                    "person",
                "selected":
                    True,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_account_data()
    )