from __future__ import annotations

from copy import deepcopy

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


UPDATES_STATES = [
    "updates",
    "all_read",
    "empty",
    "item_menu",
    "preferences_dialog",
]

POPUP_STATES = {"item_menu", "preferences_dialog"}


def generate_updates_data(seed: int | None = None) -> dict:
    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    avatar_root = ASSETS_ROOT / "pinterest" / "avatars"

    if not avatar_root.is_dir():
        avatar_root = ASSETS_ROOT

    kinds = [
        ("save", "saved an idea from your board.", "bookmark"),
        ("follow", "started following you.", "person_add"),
        ("board", "added new ideas to a shared board.", "dashboard"),
    ]

    groups = []

    for group_index, label in enumerate(["Today", "Yesterday", "Earlier"]):
        entries = []

        for index in range(4):
            kind, action, symbol = kinds[index % len(kinds)]

            entries.append({
                "id": group_index * 4 + index,
                "kind": kind,
                "name": fake.name(),
                "action": action,
                "symbol": symbol,
                "avatar": get_random_image(avatar_root),
                "preview": get_random_image(ASSETS_ROOT),
                "time": f"{index + 1}h" if group_index == 0 else f"{group_index + 1}d",
                "unread": group_index == 0 and index < 3,
            })

        groups.append({"label": label, "entries": entries})

    return {
        "state": "updates",
        "popup_visible": False,
        "groups": groups,
        "recommendations": [
            {
                "image": get_random_image(ASSETS_ROOT),
                "title": fake.sentence(nb_words=5).rstrip("."),
            }
            for _ in range(4)
        ],
        "preferences": [
            {
                "id": "push",
                "label": "Push notifications",
                "description": "Get updates on your device.",
                "enabled": True,
            },
            {
                "id": "email",
                "label": "Email notifications",
                "description": "Receive updates by email.",
                "enabled": False,
            },
            {
                "id": "in_app",
                "label": "In-app notifications",
                "description": "See updates while using Pinterest.",
                "enabled": True,
            },
        ],
    }


def create_updates_state(base_data: dict, state: str) -> dict:
    if state not in UPDATES_STATES:
        raise ValueError(f"Unknown Updates state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES

    if state == "all_read":
        for group in data["groups"]:
            for entry in group["entries"]:
                entry["unread"] = False

    if state == "empty":
        data["groups"] = []

    return data