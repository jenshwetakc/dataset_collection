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

EVENT_CHAT_STATES = [
    "conversation",
    "replying",
    "empty",
    "closed",
    "members_dialog",
    "mute_dialog",
    "delete_dialog",
    "close_dialog",
]

MESSAGE_TEXTS = [
    "Looking forward to meeting everyone!",
    "Is anyone coming from the city center?",
    "The entrance is on the first floor.",
    "Thanks for organizing this gathering.",
    "I’ll arrive about ten minutes early.",
    "Will there be time for questions?",
    "Yes, we’ll have an open discussion at the end.",
    "Happy to share my notes after the session.",
]


def generate_event_chat_data(
    sample_index: int = 0,
    *,
    avatars_dir: Path | None = None,
) -> dict:
    folder = (
        Path(avatars_dir)
        if avatars_dir is not None
        else AVATARS_DIR
    )

    members = []

    for index in range(random.randint(8, 14)):
        name = fake.name()

        members.append({
            "id": f"member_{sample_index}_{index}",
            "name": name,
            "initials": "".join(
                part[0]
                for part in name.split()[:2]
            ).upper(),
            "avatar": get_random_image(folder),
            "role": "Host" if index == 0 else "Guest",
        })

    messages = []

    for index in range(random.randint(12, 18)):
        sender = members[index % len(members)]
        own = index % 5 == 4

        messages.append({
            "id": f"message_{sample_index}_{index}",
            "sender": deepcopy(sender),
            "own": own,
            "text": random.choice(MESSAGE_TEXTS),
            "time": f"10:{index + 10:02d}",
            "reaction": index % 4 == 0,
            "reaction_count": random.randint(1, 5),
        })

    return {
        "state": "conversation",
        "popup_visible": False,
        "event_title": random.choice([
            "Creative Community Night",
            "Builders & Ideas",
            "Weekend Workshop",
        ]),
        "members": members,
        "member_count": len(members),
        "messages": messages,
        "selected_message": deepcopy(messages[0]),
        "draft": "",
        "reply_visible": False,
        "closed": False,
        "mute_options": [
            "1 hour",
            "8 hours",
            "1 week",
            "Forever",
        ],
        "selected_mute": "8 hours",
        "conversations": [
            {
                "title": "Creative Community Night",
                "preview": "Looking forward to meeting everyone!",
                "unread": 3,
            },
            {
                "title": "Weekend Coffee Club",
                "preview": "See you on Saturday.",
                "unread": 0,
            },
            {
                "title": "Design Workshop",
                "preview": "Thank you for joining us.",
                "unread": 0,
            },
        ],
    }


def apply_event_chat_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in EVENT_CHAT_STATES:
        raise ValueError(
            f"Unknown Event Chat state: {state}"
        )

    data = deepcopy(page_data)
    data["state"] = state

    data["popup_visible"] = state in {
        "members_dialog",
        "mute_dialog",
        "delete_dialog",
        "close_dialog",
    }
    data["reply_visible"] = state == "replying"
    data["closed"] = state == "closed"

    if state == "empty":
        data["messages"] = []

    elif state == "replying":
        data["draft"] = (
            "Thanks! I’ll meet everyone at the entrance."
        )

    return data