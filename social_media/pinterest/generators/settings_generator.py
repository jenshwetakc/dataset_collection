from __future__ import annotations

from copy import deepcopy

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


SETTINGS_STATES = [
    "default",
    "edited",
    "validation_error",
    "saved",
    "change_photo_dialog",
    "discard_dialog",
]

POPUP_STATES = {
    "change_photo_dialog",
    "discard_dialog",
}


def generate_settings_data(seed: int | None = None) -> dict:
    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    avatar_directory = ASSETS_ROOT / "pinterest" / "avatars"

    if not avatar_directory.is_dir():
        avatar_directory = ASSETS_ROOT

    profile = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "about": (
            "Collecting ideas for cozy spaces, creative projects "
            "and everyday inspiration."
        ),
        "pronouns": "",
        "website": f"https://{fake.domain_name()}",
        "username": fake.user_name().replace(".", "_"),
    }

    return {
        "state": "default",
        "popup_visible": False,
        "dirty": False,
        "avatar": get_random_image(avatar_directory),
        "profile": profile,
        "original_profile": deepcopy(profile),
        "website_error": "",
        "navigation": [
            "Edit profile",
            "Account management",
            "Profile visibility",
            "Tune your home feed",
            "Claimed accounts",
            "Social permissions",
            "Notifications",
            "Privacy and data",
            "Security",
        ],
    }


def create_settings_state(base_data: dict, state: str) -> dict:
    if state not in SETTINGS_STATES:
        raise ValueError(f"Unknown settings state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES

    if state in {"edited", "validation_error", "saved", "discard_dialog"}:
        data["profile"]["about"] = (
            "Finding inspiration for my next home project. "
            "Currently saving small-space ideas and handmade details."
        )
        data["dirty"] = state != "saved"

    if state == "validation_error":
        data["profile"]["website"] = "my creative website"
        data["website_error"] = (
            "Enter a valid website address, such as https://example.com."
        )

    if state == "saved":
        data["original_profile"] = deepcopy(data["profile"])

    return data