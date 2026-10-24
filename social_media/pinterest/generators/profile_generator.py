from __future__ import annotations

import random

from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


PROFILE_STATES = [
    "saved",
    "created",
    "empty_saved",
    "sort_menu",
    "create_board_dialog",
    "share_dialog",
]

POPUP_STATES = {
    "sort_menu",
    "create_board_dialog",
    "share_dialog",
}

BOARD_NAMES = [
    "Home inspiration",
    "Things to make",
    "Weekend recipes",
    "Places to visit",
    "Everyday style",
    "Garden ideas",
    "Creative workspace",
    "Beautiful typography",
    "Photography",
    "Small spaces",
    "Color inspiration",
    "Dream kitchen",
]

SORT_OPTIONS = [
    "Last saved to",
    "A to Z",
    "Custom",
]


def generate_profile_data(
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)

    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    root = Path(ASSETS_ROOT)

    # Optional portrait directory. Without it, use the
    # existing shared image collection.
    avatar_directory = root / "pinterest" / "avatars"

    avatar_root = (
        avatar_directory
        if avatar_directory.is_dir()
        else root
    )

    profile_name = fake.name()

    username = (
        fake.user_name()
        .replace(" ", "")
        .lower()
    )

    boards = []

    for index, title in enumerate(BOARD_NAMES):
        boards.append(
            {
                "id": index,
                "name": title,
                "pin_count": rng.randint(12, 450),
                "updated": rng.choice(
                    ["1d", "3d", "1w", "2w", "1mo"]
                ),
                "covers": [
                    get_random_image(root)
                    for _ in range(3)
                ],
                "private": index == 4,
            }
        )

    created_pins = []

    for index in range(36):
        created_pins.append(
            {
                "id": index,
                "image": get_random_image(root),
                "title": rng.choice(
                    [
                        "A little everyday inspiration",
                        "Fresh ideas for the weekend",
                        "Details worth saving",
                        "Something beautiful to try",
                    ]
                ),
                "aspect_ratio": rng.choice(
                    [
                        "2 / 3",
                        "3 / 4",
                        "4 / 5",
                        "1 / 1",
                    ]
                ),
            }
        )

    return {
        "state": "saved",
        "popup_visible": False,
        "active_tab": "Saved",

        "profile": {
            "name": profile_name,
            "username": username,
            "avatar": get_random_image(avatar_root),
            "bio": rng.choice(
                [
                    "Collecting thoughtful spaces, good food, "
                    "and ideas for everyday life.",
                    "Design, travel, and little things "
                    "that inspire me.",
                    "A place for creative projects "
                    "and things I want to try.",
                ]
            ),
            "website": fake.domain_name(),
            "followers": rng.randint(100, 9500),
            "following": rng.randint(20, 900),
        },

        "boards": boards,
        "created_pins": created_pins,

        "sort_options": SORT_OPTIONS,
        "selected_sort": "Last saved to",

        "share_url": (
            f"https://www.pinterest.com/{username}/"
        ),

        "share_options": [
            {"name": "Copy link", "icon": "link"},
            {"name": "Email", "icon": "mail"},
            {"name": "Message", "icon": "chat"},
            {"name": "More", "icon": "more_horiz"},
        ],
    }


def create_profile_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in PROFILE_STATES:
        raise ValueError(
            f"Unknown profile state: {state!r}"
        )

    # Reuse the same media and person across states.
    return {
        **base_data,
        "state": state,
        "popup_visible": state in POPUP_STATES,
        "active_tab": (
            "Created"
            if state == "created"
            else "Saved"
        ),
        "boards": (
            []
            if state == "empty_saved"
            else base_data["boards"]
        ),
    }