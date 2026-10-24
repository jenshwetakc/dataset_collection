from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


CREATE_PIN_STATES = [
    "empty",
    "image_uploaded",
    "validation_error",
    "board_picker",
    "schedule",
    "advanced_settings",
    "discard_dialog",
]

POPUP_STATES = {
    "board_picker",
    "discard_dialog",
}


def generate_create_pin_data(seed: int | None = None) -> dict:
    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    image = get_random_image(ASSETS_ROOT)

    if not image:
        raise FileNotFoundError(
            f"No image assets were found under {ASSETS_ROOT}."
        )

    board_names = [
        "Home inspiration",
        "Creative projects",
        "Everyday ideas",
        "Places to visit",
        "Weekend plans",
        "Style inspiration",
    ]

    schedule_time = (
        datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(days=2)
    ).replace(hour=10, minute=0, second=0, microsecond=0)

    return {
        "state": "empty",
        "popup_visible": False,
        "has_image": False,
        "image": image,
        "title": fake.sentence(nb_words=6).rstrip("."),
        "description": fake.paragraph(nb_sentences=3),
        "link": f"https://{fake.domain_name()}/ideas",
        "link_error": "",
        "selected_board": board_names[0],
        "boards": [
            {
                "name": name,
                "cover": get_random_image(ASSETS_ROOT),
                "secret": index == 3,
            }
            for index, name in enumerate(board_names)
        ],
        "topics": ["Home decor", "DIY projects", "Creative inspiration"],
        "schedule_date": schedule_time.strftime("%Y-%m-%d"),
        "schedule_time": schedule_time.strftime("%H:%M"),
        "timezone": "Asia/Seoul",
        "allow_comments": True,
        "show_similar_products": False,
    }


def create_pin_state(base_data: dict, state: str) -> dict:
    if state not in CREATE_PIN_STATES:
        raise ValueError(f"Unknown Create Pin state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES
    data["has_image"] = state != "empty"

    if state == "empty":
        data["title"] = ""
        data["description"] = ""
        data["link"] = ""
        data["selected_board"] = ""
        data["topics"] = []

    if state == "validation_error":
        data["link"] = "my inspiration page"
        data["link_error"] = (
            "Enter a valid link, such as https://example.com."
        )

    return data