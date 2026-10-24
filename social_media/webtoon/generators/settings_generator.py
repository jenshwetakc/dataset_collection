from __future__ import annotations

from copy import deepcopy

from faker import Faker

from social_media.webtoon.generators.reader_generator import (
    generate_footer_data,
)


fake = Faker()

SETTINGS_STATES = [
    "profile",
    "profile_editing",
    "profile_validation",
    "profile_saved",
    "notifications",
    "notifications_disabled",
    "language_menu",
    "delete_dialog",
]

LANGUAGES = [
    "English",
    "Français",
    "Deutsch",
    "Español",
    "Indonesia",
]


def generate_settings_data() -> dict:
    data = {
        "nickname": fake.user_name(),
        "email": fake.safe_email(),
        "languages": list(LANGUAGES),
        "language": "English",
        "preferences": [
            {
                "id": "episode_updates",
                "title": "New episode updates",
                "description": "Updates from your subscribed series.",
                "checked": True,
            },
            {
                "id": "creator_posts",
                "title": "Creator posts",
                "description": "News from creators you follow.",
                "checked": True,
            },
            {
                "id": "events",
                "title": "Events and announcements",
                "description": "Community events and product news.",
                "checked": False,
            },
            {
                "id": "recommendations",
                "title": "Reading recommendations",
                "description": "Suggestions for your next series.",
                "checked": True,
            },
        ],
    }

    data.update(generate_footer_data())
    return data


def apply_settings_state(base_data: dict, state: str) -> dict:
    if state not in SETTINGS_STATES:
        raise ValueError(f"Unknown settings state: {state}")

    data = deepcopy(base_data)

    data.update(
        {
            "state": state,
            "popup": state == "delete_dialog",
            "active_tab": (
                "notifications"
                if state in {"notifications", "notifications_disabled"}
                else "profile"
            ),
            "editing": state in {
                "profile_editing",
                "profile_validation",
            },
            "validation_error": state == "profile_validation",
            "saved": state == "profile_saved",
            "language_open": state == "language_menu",
        }
    )

    if state == "profile_editing":
        data["nickname"] = fake.user_name()

    if state == "profile_validation":
        data["nickname"] = ""

    if state == "notifications_disabled":
        for preference in data["preferences"]:
            preference["checked"] = False

    return data