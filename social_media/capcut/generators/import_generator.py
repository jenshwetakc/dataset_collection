from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


IMPORT_STATES = [
    "all_media",
    "videos",
    "photos",
    "selected_media",
    "preview_dialog",
    "importing",
]


def generate_import_data(
    sample_index: int,
    media_dir: Path | None = None,
) -> dict:
    preferred = media_dir or ASSETS_ROOT / "capcut" / "import"

    directory = next(
        (
            candidate
            for candidate in (preferred, ASSETS_ROOT)
            if get_image_files(str(candidate))
        ),
        None,
    )

    media = []

    for index in range(random.randint(24, 36)):
        kind = "video" if index % 2 == 0 else "photo"

        media.append({
            "id": f"import_{sample_index}_{index}",
            "name": (
                f"VID_{index + 1:04d}.mp4"
                if kind == "video"
                else f"IMG_{index + 1:04d}.jpg"
            ),
            "kind": kind,
            "image": (
                get_random_image(directory)
                if directory is not None
                else None
            ),
            "duration": f"00:{random.randint(5, 59):02d}",
            "size": f"{random.randint(4, 95)} MB",
            "selected": False,
            "selection_order": None,
        })

    return {
        "sample_index": sample_index,
        "state": "all_media",
        "popup_visible": False,
        "active_tab": "all",
        "album": "Recent",
        "albums": ["Recent", "Camera", "Downloads", "Favorites"],
        "media": media,
        "selected_media": [],
        "selected_count": 0,
        "target_media": dict(media[0]),
        "progress": random.randint(25, 85),
        "imported_count": 0,
        "import_total": 4,
    }


def apply_import_state(base_data: dict, state: str) -> dict:
    if state not in IMPORT_STATES:
        raise ValueError(f"Unknown import state: {state}")

    data = dict(base_data)
    data["media"] = [dict(item) for item in base_data["media"]]
    data["target_media"] = dict(base_data["target_media"])
    data["state"] = state
    data["popup_visible"] = state in {"preview_dialog", "importing"}
    data["active_tab"] = {
        "videos": "video",
        "photos": "photo",
    }.get(state, "all")

    if state in {"videos", "photos"}:
        data["media"] = [
            item
            for item in data["media"]
            if item["kind"] == data["active_tab"]
        ]

    if state in {"selected_media", "importing"}:
        selected = random.sample(data["media"], k=4)

        for order, item in enumerate(selected, start=1):
            item["selected"] = True
            item["selection_order"] = order

        data["selected_media"] = sorted(
            selected,
            key=lambda item: item["selection_order"],
        )
        data["selected_count"] = len(selected)
        data["import_total"] = len(selected)
        data["imported_count"] = min(
            len(selected) - 1,
            int(data["progress"] / 100 * len(selected)),
        )

    return data