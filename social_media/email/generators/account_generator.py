from __future__ import annotations

import random

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

ACCOUNT_STATES = [
    "account_overview",
    "storage_usage",
    "connected_accounts",
    "security",
    "recovery_email",
    "account_switcher_popup",
    "sign_out_confirm",
    "mobile_profile_sheet",
]


# ==========================================================
# Helpers
# ==========================================================

def _account(
    index: int = 0,
) -> dict:

    name = fake.name()

    return {
        "id":
            f"account_{index}",

        "name":
            name,

        "email":
            fake.email(),

        "avatar":
            get_random_avatar(),

        "organization":
            random.choice([
                "Example University",
                "Research Lab",
                "Mail Studio",
                "Design Team",
            ]),

        "role":
            random.choice([
                "Graduate Student",
                "Research Assistant",
                "Software Engineer",
                "Product Designer",
            ]),
    }


def _connected_account(
    index: int,
) -> dict:

    return {
        "id":
            f"connected_account_{index}",

        "service":
            random.choice([
                "Google Drive",
                "Dropbox",
                "OneDrive",
                "Calendar",
                "Contacts",
            ]),

        "email":
            fake.email(),

        "connected":
            random.random() < 0.8,
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_account_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            ACCOUNT_STATES
        )
    )

    if selected_state not in ACCOUNT_STATES:

        raise ValueError(
            f"Unknown account state: "
            f"{selected_state}"
        )

    current_account = _account()

    alternative_accounts = [
        _account(
            index=index + 1
        )
        for index in range(
            random.randint(
                2,
                4,
            )
        )
    ]

    storage_total = random.choice([
        15,
        30,
        100,
    ])

    storage_used = round(
        random.uniform(
            2.0,
            storage_total * 0.92,
        ),
        1,
    )

    storage_percent = int(
        (
            storage_used
            / storage_total
        )
        * 100
    )

    connected_accounts = [
        _connected_account(
            index
        )
        for index in range(
            random.randint(
                3,
                6,
            )
        )
    ]

    if selected_state == "storage_usage":

        selected_section = "storage"

    elif selected_state == "connected_accounts":

        selected_section = "connected"

    elif selected_state == "security":

        selected_section = "security"

    elif selected_state == "recovery_email":

        selected_section = "recovery"

    else:

        selected_section = "overview"

    return {
        "state":
            selected_state,

        "title":
            "Account",

        "selected_section":
            selected_section,

        "account":
            current_account,

        "alternative_accounts":
            alternative_accounts,

        "sections": [
            {
                "key":
                    "overview",

                "label":
                    "Overview",

                "icon":
                    "person",
            },
            {
                "key":
                    "storage",

                "label":
                    "Storage",

                "icon":
                    "cloud",
            },
            {
                "key":
                    "connected",

                "label":
                    "Connected accounts",

                "icon":
                    "link",
            },
            {
                "key":
                    "security",

                "label":
                    "Security",

                "icon":
                    "security",
            },
            {
                "key":
                    "recovery",

                "label":
                    "Recovery",

                "icon":
                    "shield",
            },
        ],

        "storage": {
            "used":
                storage_used,

            "total":
                storage_total,

            "percent":
                storage_percent,

            "mail":
                random.randint(
                    20,
                    65,
                ),

            "attachments":
                random.randint(
                    10,
                    40,
                ),

            "other":
                random.randint(
                    5,
                    25,
                ),
        },

        "connected_accounts":
            connected_accounts,

        "security": {
            "two_factor":
                random.random() < 0.65,

            "login_alerts":
                random.random() < 0.8,

            "remember_devices":
                random.random() < 0.6,

            "last_password_change":
                random.choice([
                    "2 weeks ago",
                    "1 month ago",
                    "3 months ago",
                ]),

            "recent_device":
                random.choice([
                    "Chrome on macOS",
                    "Chrome on Windows",
                    "Safari on iPhone",
                    "Android device",
                ]),

            "recent_location":
                random.choice([
                    "Seoul, South Korea",
                    "Busan, South Korea",
                    "Tokyo, Japan",
                    "Singapore",
                ]),
        },

        "recovery": {
            "email":
                fake.email(),

            "phone":
                fake.phone_number(),

            "verified":
                random.random() < 0.8,
        },

        "account_switcher_open":
            selected_state
            == "account_switcher_popup",

        "sign_out_confirm_open":
            selected_state
            == "sign_out_confirm",

        "mobile_profile_sheet_open":
            selected_state
            == "mobile_profile_sheet",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_account_data()

    print(
        "State:",
        data["state"],
    )

    print(
        "Section:",
        data["selected_section"],
    )