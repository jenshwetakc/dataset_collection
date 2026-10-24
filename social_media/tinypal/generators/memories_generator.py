from __future__ import annotations

import random
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path

from social_media.tinypal.generators.home_generator import optional_image


MEMORY_STATES = [
    "all_memories",
    "milestones_only",
    "empty_album",
    "memory_viewer",
    "add_memory",
    "edit_memory",
    "delete_dialog",
]


def generate_memories_data(
    sample_index: int,
    photos_dir: Path,
) -> dict:
    today = date.today()

    specifications = [
        ("A sunny family walk", "photo", "park"),
        ("Our first picture book", "milestone", "menu_book"),
        ("An afternoon of little discoveries", "photo", "explore"),
        ("A new favorite game", "milestone", "toys"),
        ("Together at the park", "photo", "nature_people"),
        ("A special family visit", "milestone", "group"),
        ("A cozy morning at home", "photo", "home"),
        ("A moment worth remembering", "photo", "favorite"),
    ]

    memories = [
        {
            "id": f"memory_{index}",
            "title": title,
            "kind": kind,
            "icon": icon_name,
            "date": (today - timedelta(days=index * 3)).isoformat(),
            "date_label": (
                today - timedelta(days=index * 3)
            ).strftime("%b %d, %Y"),
            "photo": optional_image(photos_dir),
            "note": random.choice([
                "A small moment we wanted to keep.",
                "We enjoyed this time together.",
                "One for the family album.",
            ]),
            "favorite": index in {0, 2, 5},
            "author": random.choice(["You", "Sam", "Alex"]),
        }
        for index, (title, kind, icon_name) in enumerate(specifications)
    ]

    return {
        "sample_index": sample_index,
        "state": "all_memories",
        "popup_visible": False,
        "popup_kind": None,
        "active_filter": "all",
        "memories": memories,
        "visible_memories": [],
        "selected_memory": deepcopy(memories[0]),
        "count": 0,
        "milestone_count": 0,
        "filters": [
            {"id": "all", "label": "All memories", "icon": "photo_library"},
            {"id": "milestone", "label": "Milestones", "icon": "auto_awesome"},
        ],
        "form": {
            "title": "",
            "date": today.isoformat(),
            "note": "",
            "photo": None,
            "milestone": False,
        },
        "navigation": [
            {"label": "Today", "icon": "home", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": True},
        ],
    }


def apply_memories_state(base_data: dict, state: str) -> dict:
    if state not in MEMORY_STATES:
        raise ValueError(f"Unknown memory state: {state}")

    data = deepcopy(base_data)
    data["state"] = state

    popup_states = {
        "memory_viewer",
        "add_memory",
        "edit_memory",
        "delete_dialog",
    }

    data["popup_visible"] = state in popup_states
    data["popup_kind"] = state if state in popup_states else None

    if state == "milestones_only":
        data["active_filter"] = "milestone"

    elif state == "empty_album":
        data["memories"] = []

    elif state == "edit_memory":
        memory = data["selected_memory"]

        data["form"] = {
            "title": memory["title"],
            "date": memory["date"],
            "note": memory["note"],
            "photo": memory["photo"],
            "milestone": memory["kind"] == "milestone",
        }

    data["visible_memories"] = [
        memory for memory in data["memories"]
        if (
            data["active_filter"] == "all"
            or memory["kind"] == data["active_filter"]
        )
    ]

    data["count"] = len(data["visible_memories"])
    data["milestone_count"] = sum(
        memory["kind"] == "milestone"
        for memory in data["memories"]
    )

    return data