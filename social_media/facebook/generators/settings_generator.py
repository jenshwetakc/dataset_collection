from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

SETTINGS_STATES = [
    "default",
    "default",
    "privacy_checkup",
    "notifications",
    "blocking",
    "language",
    "appearance",
    "account_center",
    "confirm_dialog",
]


LANGUAGES = [
    "English (US)",
    "한국어",
    "日本語",
    "Español",
    "Français",
    "Deutsch",
]


# ==========================================================
# Navigation
# ==========================================================

def generate_settings_navigation() -> list[dict]:

    return [
        {
            "name": "Settings home",
            "icon": "settings",
            "key": "default",
        },
        {
            "name": "Privacy",
            "icon": "shield",
            "key": "privacy_checkup",
        },
        {
            "name": "Notifications",
            "icon": "notifications",
            "key": "notifications",
        },
        {
            "name": "Blocking",
            "icon": "block",
            "key": "blocking",
        },
        {
            "name": "Language",
            "icon": "language",
            "key": "language",
        },
        {
            "name": "Appearance",
            "icon": "dark_mode",
            "key": "appearance",
        },
        {
            "name": "Accounts Center",
            "icon": "manage_accounts",
            "key": "account_center",
        },
    ]


# ==========================================================
# Privacy
# ==========================================================

def generate_privacy_options() -> list[dict]:

    return [
        {
            "title": "Who can see your future posts?",
            "value": random.choice(
                [
                    "Friends",
                    "Public",
                    "Only me",
                ]
            ),
            "icon": "public",
        },
        {
            "title": "Who can see your friends list?",
            "value": random.choice(
                [
                    "Friends",
                    "Only me",
                    "Public",
                ]
            ),
            "icon": "group",
        },
        {
            "title": "Who can look you up using your email?",
            "value": random.choice(
                [
                    "Friends",
                    "Friends of friends",
                    "Everyone",
                ]
            ),
            "icon": "mail",
        },
        {
            "title": "Allow search engines outside Facebook",
            "value": random.choice(
                [
                    "Allowed",
                    "Not allowed",
                ]
            ),
            "icon": "search",
        },
    ]


# ==========================================================
# Notification Settings
# ==========================================================

def generate_notification_settings() -> list[dict]:

    names = [
        (
            "Push notifications",
            "notifications_active",
        ),
        (
            "Email notifications",
            "mail",
        ),
        (
            "SMS notifications",
            "sms",
        ),
        (
            "Friend requests",
            "person_add",
        ),
        (
            "Comments",
            "chat_bubble",
        ),
        (
            "Tags",
            "sell",
        ),
        (
            "Birthdays",
            "cake",
        ),
    ]

    return [
        {
            "name": name,
            "icon": icon,
            "enabled":
                random.random() < 0.65,
        }
        for name, icon in names
    ]


# ==========================================================
# Blocking
# ==========================================================

def generate_blocked_people(
    count: int = 5,
) -> list[dict]:

    return [
        {
            "id":
                index,

            "name":
                fake.name(),

            "reason":
                random.choice(
                    [
                        "Blocked profile",
                        "Restricted interaction",
                    ]
                ),
        }
        for index in range(
            count
        )
    ]


# ==========================================================
# Appearance
# ==========================================================

def generate_appearance_settings() -> dict:

    return {
        "theme":
            random.choice(
                [
                    "System",
                    "Light",
                    "Dark",
                ]
            ),

        "compact_mode":
            random.random() < 0.5,

        "reduce_motion":
            random.random() < 0.35,

        "high_contrast":
            random.random() < 0.2,
    }


# ==========================================================
# Accounts
# ==========================================================

def generate_accounts() -> list[dict]:

    return [
        {
            "name":
                "Facebook",

            "username":
                fake.user_name(),

            "icon":
                "facebook",
        },
        {
            "name":
                "Messenger",

            "username":
                fake.user_name(),

            "icon":
                "chat",
        },
        {
            "name":
                "Instagram",

            "username":
                fake.user_name(),

            "icon":
                "photo_camera",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_settings_state() -> dict:

    name = random.choice(
        SETTINGS_STATES
    )

    selected_language = None

    if name == "language":

        selected_language = (
            random.choice(
                LANGUAGES
            )
        )

    confirm_action = None

    if name == "confirm_dialog":

        confirm_action = random.choice(
            [
                "Deactivate account",
                "Remove blocked profile",
                "Reset notification settings",
            ]
        )

    return {
        "name":
            name,

        "selected_language":
            selected_language,

        "confirm_action":
            confirm_action,
    }


# ==========================================================
# Complete Data
# ==========================================================

def generate_settings_data() -> dict:

    return {
        "navigation":
            generate_settings_navigation(),

        "privacy":
            generate_privacy_options(),

        "notifications":
            generate_notification_settings(),

        "blocked_people":
            generate_blocked_people(
                count=random.randint(
                    4,
                    7,
                )
            ),

        "languages":
            LANGUAGES,

        "appearance":
            generate_appearance_settings(),

        "accounts":
            generate_accounts(),

        "state":
            generate_settings_state(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_settings_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK SETTINGS GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Privacy options:",
        len(
            data["privacy"]
        ),
    )

    print(
        "Notification settings:",
        len(
            data["notifications"]
        ),
    )

    print(
        "Blocked people:",
        len(
            data["blocked_people"]
        ),
    )