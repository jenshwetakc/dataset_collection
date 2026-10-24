from __future__ import annotations

from copy import deepcopy

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


MESSAGES_STATES = [
    "inbox",
    "conversation",
    "message_composed",
    "empty_inbox",
    "new_message_dialog",
    "share_pin_dialog",
]

POPUP_STATES = {
    "new_message_dialog",
    "share_pin_dialog",
}


def generate_messages_data(seed: int | None = None) -> dict:
    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    avatar_root = ASSETS_ROOT / "pinterest" / "avatars"

    if not avatar_root.is_dir():
        avatar_root = ASSETS_ROOT

    contacts = [
        {
            "id": index,
            "name": fake.name(),
            "avatar": get_random_image(avatar_root),
            "preview": fake.sentence(nb_words=6),
            "time": f"{index + 1}h",
            "unread": index in {0, 2},
        }
        for index in range(8)
    ]

    pins = [
        {
            "image": get_random_image(ASSETS_ROOT),
            "title": fake.sentence(nb_words=5).rstrip("."),
        }
        for _ in range(6)
    ]

    return {
        "state": "inbox",
        "popup_visible": False,
        "show_thread": False,
        "contacts": contacts,
        "active_contact": contacts[0],
        "pins": pins,
        "selected_contact_id": contacts[1]["id"],
        "draft": "",
        "messages": [
            {
                "kind": "text",
                "outgoing": False,
                "text": "I found some ideas for our next project!",
            },
            {
                "kind": "pin",
                "outgoing": False,
                "pin": pins[0],
            },
            {
                "kind": "text",
                "outgoing": True,
                "text": "Love this. The colors work so well together.",
            },
            {
                "kind": "text",
                "outgoing": False,
                "text": "Should we save a few more ideas?",
            },
        ],
    }


def create_messages_state(base_data: dict, state: str) -> dict:
    if state not in MESSAGES_STATES:
        raise ValueError(f"Unknown Messages state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES
    data["show_thread"] = state in {
        "conversation",
        "message_composed",
        "share_pin_dialog",
    }

    if state == "message_composed":
        data["draft"] = "Yes! Let me send you another idea."

    if state == "empty_inbox":
        data["contacts"] = []

    return data