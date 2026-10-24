from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


BACKGROUND_STATES = [
    "original",
    "processing",
    "removed",
    "background_selected",
    "manual_refine",
    "reset_dialog",
]


def generate_background_data(
    sample_index: int,
    media_dir: Path | None = None,
) -> dict:
    preferred = media_dir or ASSETS_ROOT / "capcut" / "background"

    directory = next(
        (
            candidate
            for candidate in (preferred, ASSETS_ROOT)
            if get_image_files(str(candidate))
        ),
        None,
    )

    return {
        "sample_index": sample_index,
        "state": "original",
        "popup_visible": False,
        "image": (
            get_random_image(directory)
            if directory is not None
            else None
        ),
        "project_name": random.choice([
            "Portrait edit",
            "Product story",
            "Creative composition",
        ]),
        "progress": random.randint(25, 85),
        "show_removed": False,
        "active_tab": "remove",
        "selected_background": "transparent",
        "backgrounds": [
            {"id": "transparent", "label": "Transparent", "icon": "grid_on"},
            {"id": "studio", "label": "Studio", "icon": "photo_camera"},
            {"id": "brand", "label": "Brand", "icon": "palette"},
            {"id": "soft", "label": "Soft", "icon": "blur_on"},
        ],
        "brush_mode": "erase",
        "brush_size": random.randint(20, 45),
        "feather": random.randint(10, 30),
        "apply_all": random.choice([True, False]),
    }


def apply_background_state(base_data: dict, state: str) -> dict:
    if state not in BACKGROUND_STATES:
        raise ValueError(f"Unknown background state: {state}")

    data = dict(base_data)
    data["state"] = state
    data["popup_visible"] = state == "reset_dialog"
    data["show_removed"] = state not in {"original", "processing"}
    data["active_tab"] = (
        "background"
        if state == "background_selected"
        else "refine"
        if state == "manual_refine"
        else "remove"
    )
    data["selected_background"] = (
        random.choice(["studio", "brand", "soft"])
        if state == "background_selected"
        else "transparent"
    )

    return data