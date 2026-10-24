from __future__ import annotations

import random
from copy import deepcopy


DOWNLOAD_STATES = [
    "downloaded",
    "downloading",
    "paused",
    "download_error",
    "empty",
    "selection_mode",
    "download_settings_dialog",
    "remove_dialog",
]

RESOURCE_TITLES = [
    "Internal medicine reference collection",
    "Patient education resources",
    "Clinical topic summaries",
    "General reference graphics",
    "Family medicine resources",
    "Pediatric reference collection",
    "Laboratory reference topics",
    "Clinical calculator resources",
]


def generate_downloads_data(sample_index: int) -> dict:
    resources = [
        {
            "id": f"download_{index}",
            "title": title,
            "size_mb": random.randint(20, 160),
            "status": "ready",
            "progress": 100,
            "selected": False,
            "updated": random.choice([
                "Updated today",
                "Updated yesterday",
                "Updated this week",
            ]),
            "icon": random.choice([
                "article", "menu_book", "image", "school",
            ]),
        }
        for index, title in enumerate(RESOURCE_TITLES)
    ]

    return {
        "sample_index": sample_index,
        "state": "downloaded",
        "popup_visible": False,
        "popup_kind": None,
        "resources": resources,
        "selection_mode": False,
        "selected_count": 0,
        "wifi_only": True,
        "automatic_updates": random.choice([True, False]),
        "include_graphics": True,
        "storage_limit_mb": 2000,
        "used_mb": 0,
        "storage_percent": 0,
        "resource_count": len(resources),
        "active_tab": "all",
        "status_labels": {
            "ready": "Available offline",
            "downloading": "Downloading",
            "paused": "Paused",
            "error": "Download failed",
        },
    }


def apply_downloads_state(base_data: dict, state: str) -> dict:
    if state not in DOWNLOAD_STATES:
        raise ValueError(f"Unknown download state: {state!r}")

    data = deepcopy(base_data)
    data.update({
        "state": state,
        "popup_visible": False,
        "popup_kind": None,
        "selection_mode": False,
        "selected_count": 0,
    })

    if state in {"downloading", "paused"}:
        for resource in data["resources"][:3]:
            resource["status"] = state
            resource["progress"] = random.randint(12, 88)

    elif state == "download_error":
        data["resources"][0]["status"] = "error"
        data["resources"][0]["progress"] = 34

    elif state == "empty":
        data["resources"] = []

    elif state in {"selection_mode", "remove_dialog"}:
        data["selection_mode"] = True
        for resource in data["resources"][:2]:
            resource["selected"] = True

        if state == "remove_dialog":
            data["popup_visible"] = True
            data["popup_kind"] = "remove"

    elif state == "download_settings_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "settings"

    data["selected_count"] = sum(
        resource["selected"] for resource in data["resources"]
    )
    data["resource_count"] = len(data["resources"])

    data["used_mb"] = round(sum(
        resource["size_mb"] * resource["progress"] / 100
        for resource in data["resources"]
    ))
    data["storage_percent"] = min(
        100,
        round(data["used_mb"] / data["storage_limit_mb"] * 100),
    )

    return data