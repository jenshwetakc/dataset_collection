from __future__ import annotations

import random
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

COVERS_DIR = ASSETS_ROOT / "luma"

CREATE_STATES = [
    "blank",
    "filled",
    "online",
    "validation_errors",
    "cover_picker",
    "theme_picker",
    "visibility_dialog",
]


def generate_create_data(
    sample_index: int = 0,
    *,
    covers_dir: str | Path | None = None,
) -> dict:
    directory = Path(
        covers_dir if covers_dir is not None else COVERS_DIR
    ).expanduser()

    start = (
        datetime.now().replace(
            hour=18, minute=0, second=0, microsecond=0,
        )
        + timedelta(days=random.randint(3, 21))
    )
    end = start + timedelta(hours=2)

    covers = [
        {
            "id": f"cover_{index}",
            "image": get_random_image(directory),
        }
        for index in range(9)
    ]

    return {
        "state": "filled",
        "popup_visible": False,
        "title": random.choice([
            "Creative Coffee Evening",
            "Builders and Ideas",
            "Community Design Workshop",
            "Weekend Photography Walk",
        ]),
        "calendar": f"{fake.word().title()} Collective",
        "cover": covers[0]["image"],
        "covers": covers,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "start_time": start.strftime("%H:%M"),
        "end_time": end.strftime("%H:%M"),
        "timezone": "Asia/Seoul",
        "online": False,
        "location": f"{fake.street_name()} Studio",
        "meeting_url": "https://example.com/meeting",
        "description": (
            "Join us for an evening of ideas and conversation.\n\n"
            "Meet the community, explore something new, "
            "and connect with other curious people."
        ),
        "visibility": random.choice(["Public", "Private"]),
        "themes": [
            {"name": "Minimal", "style": "minimal"},
            {"name": "Ambient", "style": "ambient"},
            {"name": "Pattern", "style": "pattern"},
            {"name": "Playful", "style": "playful"},
        ],
        "selected_theme": "Minimal",
        "errors": {},
    }


def apply_create_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in CREATE_STATES:
        raise ValueError(f"Unknown Create Event state: {state}")

    data = deepcopy(page_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "cover_picker",
        "theme_picker",
        "visibility_dialog",
    }

    if state in {"blank", "validation_errors"}:
        data["title"] = ""
        data["location"] = ""
        data["description"] = ""
        data["cover"] = None

    if state == "online":
        data["online"] = True

    if state == "validation_errors":
        data["errors"] = {
            "title": "Enter an event name.",
            "location": "Choose a location or an online event.",
        }

    return data