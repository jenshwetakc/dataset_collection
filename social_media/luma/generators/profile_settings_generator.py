from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

AVATARS_DIR = ASSETS_ROOT / "luma" / "avatars"

PROFILE_SETTINGS_STATES = [
    "profile",
    "social_links",
    "account",
    "validation_errors",
    "saved",
    "photo_dialog",
    "username_dialog",
    "email_dialog",
    "verification_dialog",
]


def generate_profile_settings_data(
    sample_index: int = 0,
    *,
    avatars_dir: Path | None = None,
) -> dict:
    folder = (
        Path(avatars_dir)
        if avatars_dir is not None
        else AVATARS_DIR
    )

    first_name = fake.first_name()
    last_name = fake.last_name()

    # Fictional username; reserved example domains for links.
    username = f"community_host_{sample_index}"

    photo_choices = []

    for index in range(6):
        image = get_random_image(folder)

        if image is not None:
            photo_choices.append({
                "id": f"photo_{index}",
                "image": image,
                "selected": index == 0,
            })

    avatar = (
        photo_choices[0]["image"]
        if photo_choices
        else None
    )

    return {
        "state": "profile",
        "active_section": "Profile",
        "popup_visible": False,
        "first_name": first_name,
        "last_name": last_name,
        "display_name": f"{first_name} {last_name}",
        "initials": (
            first_name[0] + last_name[0]
        ).upper(),
        "avatar": avatar,
        "photo_choices": photo_choices,
        "bio": random.choice([
            "Bringing curious people together through "
            "workshops, conversations, and community gatherings.",
            "Designer, maker, and occasional meetup host. "
            "Always happy to meet people with new ideas.",
            "Creating welcoming spaces for learning "
            "and meaningful conversations.",
        ]),
        "username": username,
        "profile_url": (
            f"https://luma.com/user/{username}"
        ),
        "email": fake.safe_email(),
        "new_email": fake.safe_email(),
        "verification_code": "",
        "links": [
            {
                "name": "Website",
                "icon": "language",
                "value": f"https://{username}.example.com",
            },
            {
                "name": "Instagram",
                "icon": "photo_camera",
                "value": "https://example.com/instagram",
            },
            {
                "name": "X",
                "icon": "alternate_email",
                "value": "https://example.com/social",
            },
            {
                "name": "YouTube",
                "icon": "smart_display",
                "value": "",
            },
            {
                "name": "TikTok",
                "icon": "music_note",
                "value": "",
            },
            {
                "name": "LinkedIn",
                "icon": "work",
                "value": "https://example.com/linkedin",
            },
        ],
        "errors": {},
    }


def apply_profile_settings_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in PROFILE_SETTINGS_STATES:
        raise ValueError(
            f"Unknown Profile Settings state: {state}"
        )

    data = deepcopy(page_data)
    data["state"] = state
    data["errors"] = {}

    data["popup_visible"] = state in {
        "photo_dialog",
        "username_dialog",
        "email_dialog",
        "verification_dialog",
    }

    if state == "social_links":
        data["active_section"] = "Social Links"

    elif state in {
        "account",
        "username_dialog",
        "email_dialog",
        "verification_dialog",
    }:
        data["active_section"] = "Account"

    else:
        data["active_section"] = "Profile"

    if state == "validation_errors":
        data["first_name"] = ""
        data["bio"] = "A" * 320
        data["errors"] = {
            "first_name": "Enter your first name.",
            "bio": "Shorten your bio to 280 characters.",
        }

    return data