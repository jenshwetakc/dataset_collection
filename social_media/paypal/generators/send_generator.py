from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_avatar,
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


SUGGESTED_LABELS = [
    "Recent",
    "Frequent",
    "Suggested",
]


# ==========================================================
# Contact
# ==========================================================

def generate_contact(
    index: int,
) -> dict:

    name = fake.name()

    username_type = random.choice([
        "email",
        "username",
        "phone",
    ])

    if username_type == "email":

        secondary = fake.email()

    elif username_type == "phone":

        secondary = fake.phone_number()

    else:

        secondary = (
            "@"
            + fake.user_name()
        )

    return {
        "id":
            index,

        "name":
            name,

        "secondary":
            secondary,

        "avatar":
            get_random_avatar(),

        "initial":
            name[0].upper(),

        "is_recent":
            random.choice([
                True,
                False,
            ]),

        "favorite":
            random.random() < 0.25,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_send_data() -> dict:

    contacts = [
        generate_contact(index)
        for index in range(
            random.randint(
                10,
                20,
            )
        )
    ]

    recent_contacts = (
        contacts[:random.randint(
            4,
            min(
                7,
                len(contacts),
            ),
        )]
    )

    return {

        "title":
            random.choice([
                "Send money",
                "Who do you want to pay?",
                "Send to someone",
            ]),

        "subtitle":
            random.choice([
                "Search by name, email, or username.",
                "Find someone to send money to.",
                "Choose a person to continue.",
            ]),

        "search_placeholder":
            random.choice([
                "Name, email, or username",
                "Search people",
                "Find a recipient",
            ]),

        "recent_title":
            random.choice(
                SUGGESTED_LABELS
            ),

        "recent_contacts":
            recent_contacts,

        "contacts":
            contacts,

        "navigation":
            NAVIGATION_ITEMS,

        "notification_count":
            random.randint(
                0,
                5,
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_send_data()
    )