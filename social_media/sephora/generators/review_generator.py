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

REVIEW_STATES = [
    "empty",
    "rated",
    "draft",
    "photos_added",
    "skin_type_open",
    "validation_error",
    "preview_dialog",
    "submitted",
]


def generate_review_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:
    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    return {
        "sample_index": sample_index,
        "state": "empty",
        "popup_visible": False,
        "brand": fake.company(),
        "product_name": random.choice([
            "Daily Hydrating Face Cream",
            "Lightweight Moisture Gel",
            "Gentle Facial Cleanser",
        ]),
        "product_image": get_random_image(directory),
        "rating": 4,
        "nickname": fake.user_name(),
        "title": "Comfortable texture for everyday use",
        "body": (
            "I enjoyed the lightweight texture and simple packaging. "
            "It fits comfortably into my daily routine. "
            "I would prefer a smaller travel size as another option."
        ),
        "skin_types": [
            "Normal",
            "Dry",
            "Oily",
            "Combination",
        ],
        "skin_type": random.choice([
            "Normal", "Dry", "Oily", "Combination",
        ]),
        "recommend": "yes",
        "photos": [
            image
            for _ in range(2)
            if (image := get_random_image(directory))
        ],
        "accepted_terms": True,
    }


def apply_review_state(base_data: dict, state: str) -> dict:
    if state not in REVIEW_STATES:
        raise ValueError(f"Unknown review state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state == "preview_dialog"

    if state in ["empty", "rated"]:
        data["title"] = ""
        data["body"] = ""
        data["nickname"] = ""
        data["accepted_terms"] = False

    if state == "empty":
        data["rating"] = 0

    if state == "validation_error":
        data["title"] = ""
        data["body"] = ""
        data["accepted_terms"] = False

    if state not in [
        "photos_added",
        "preview_dialog",
        "submitted",
    ]:
        data["photos"] = []

    return data