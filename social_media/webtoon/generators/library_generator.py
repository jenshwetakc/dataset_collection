from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)
from social_media.webtoon.generators.reader_generator import (
    generate_footer_data,
)


fake = Faker()

LIBRARY_STATES = [
    "subscribed",
    "recent",
    "updates_only",
    "edit_mode",
    "selected",
    "remove_dialog",
    "removed",
    "empty_subscriptions",
    "empty_history",
]

COVERS_ROOT = Path(ASSETS_ROOT) / "webtoon"


def load_cover() -> str:
    if (
        not COVERS_ROOT.is_dir()
        or not get_image_files(str(COVERS_ROOT))
    ):
        raise FileNotFoundError(
            f"No supported cover images in: {COVERS_ROOT}"
        )

    image = get_random_image(COVERS_ROOT)

    if not image:
        raise RuntimeError(f"Could not load cover: {COVERS_ROOT}")

    return image


def generate_library_data() -> dict:
    series = []

    for index in range(18):
        available_episode = random.randint(20, 180)
        last_read = random.randint(1, available_episode)

        series.append(
            {
                "id": f"library_{index}",
                "title": fake.sentence(
                    nb_words=random.randint(2, 5)
                ).rstrip("."),
                "creator": fake.name(),
                "genre": random.choice(
                    ["Romance", "Fantasy", "Drama", "Action", "Comedy"]
                ),
                "cover": load_cover(),
                "available_episode": available_episode,
                "last_read": last_read,
                "unread_count": available_episode - last_read,
                "subscribed": index % 3 != 0,
                "read_hours_ago": index * 4 + random.randint(1, 3),
            }
        )

    data = {
        "account_name": fake.first_name(),
        "series": series,
    }

    data.update(generate_footer_data())

    return data


def apply_library_state(base_data: dict, state: str) -> dict:
    if state not in LIBRARY_STATES:
        raise ValueError(f"Unknown library state: {state}")

    data = deepcopy(base_data)

    active_tab = (
        "recent"
        if state in {"recent", "empty_history"}
        else "subscribed"
    )

    subscriptions = [
        item for item in data["series"] if item["subscribed"]
    ]

    history = sorted(
        data["series"],
        key=lambda item: item["read_hours_ago"],
    )

    selected_ids = (
        [item["id"] for item in subscriptions[:2]]
        if state in {"selected", "remove_dialog", "removed"}
        else []
    )

    removed_count = 0

    if state == "removed":
        subscriptions = [
            item for item in subscriptions
            if item["id"] not in selected_ids
        ]
        removed_count = len(selected_ids)
        selected_ids = []

    if state == "empty_subscriptions":
        subscriptions = []

    if state == "empty_history":
        history = []

    results = (
        history if active_tab == "recent" else subscriptions
    )

    if state == "updates_only":
        results = [
            item for item in results
            if item["unread_count"] > 0
        ]

    for item in results:
        item["selected"] = item["id"] in selected_ids

    data.update(
        {
            "state": state,
            "popup": state == "remove_dialog",
            "active_tab": active_tab,
            "edit_mode": state in {
                "edit_mode", "selected", "remove_dialog"
            },
            "updates_only": state == "updates_only",
            "selected_count": len(selected_ids),
            "subscription_count": len(subscriptions),
            "history_count": len(history),
            "results": results,
            "removed_count": removed_count,
        }
    )

    return data