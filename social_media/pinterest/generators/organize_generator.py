from __future__ import annotations

import random
from copy import deepcopy

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


ORGANIZE_STATES = [
    "organize",
    "selected",
    "all_selected",
    "move_dialog",
    "delete_dialog",
    "empty",
]

POPUP_STATES = {"move_dialog", "delete_dialog"}


def generate_organize_data(seed: int | None = None) -> dict:
    fake = Faker()
    rng = random.Random(seed)

    if seed is not None:
        fake.seed_instance(seed)

    pins = []

    for index in range(36):
        image = get_random_image(ASSETS_ROOT)

        if not image:
            raise FileNotFoundError(
                f"No image assets found under {ASSETS_ROOT}."
            )

        pins.append({
            "id": index,
            "image": image,
            "title": fake.sentence(nb_words=5).rstrip("."),
            "ratio": rng.choice(["3 / 4", "2 / 3", "1 / 1"]),
            "selected": False,
        })

    return {
        "state": "organize",
        "popup_visible": False,
        "board_name": rng.choice([
            "Ideas for my home",
            "Creative projects",
            "Weekend inspiration",
            "Everyday style",
        ]),
        "pins": pins,
        "selected_count": 0,
        "destinations": [
            {
                "name": name,
                "cover": get_random_image(ASSETS_ROOT),
                "secret": index == 2,
            }
            for index, name in enumerate([
                "New project",
                "Favorites",
                "Private inspiration",
                "Ideas to try",
                "Things to make",
            ])
        ],
    }


def create_organize_state(base_data: dict, state: str) -> dict:
    if state not in ORGANIZE_STATES:
        raise ValueError(f"Unknown Organize state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES

    if state == "empty":
        data["pins"] = []

    selected_ids = set()

    if state in {"selected", "move_dialog", "delete_dialog"}:
        selected_ids = {0, 2, 4, 6}
    elif state == "all_selected":
        selected_ids = {pin["id"] for pin in data["pins"]}

    for pin in data["pins"]:
        pin["selected"] = pin["id"] in selected_ids

    data["selected_count"] = sum(
        pin["selected"] for pin in data["pins"]
    )

    return data