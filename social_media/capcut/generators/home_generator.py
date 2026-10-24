from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


HOME_STATES = [
    "projects",
    "empty",
    "search_results",
    "selection_mode",
    "rename_dialog",
    "delete_dialog",
]

PROJECT_NAMES = [
    "Seoul weekend",
    "Morning coffee",
    "Travel diary",
    "City after dark",
    "Summer memories",
    "Studio session",
    "A day in my life",
    "Mountain escape",
    "Product showcase",
    "Birthday highlights",
    "Street food tour",
    "Behind the scenes",
]

TOOLS = [
    {"label": "Auto captions", "icon": "closed_caption"},
    {"label": "Remove background", "icon": "person_remove"},
    {"label": "AI video", "icon": "auto_awesome"},
    {"label": "Photo editor", "icon": "photo"},
    {"label": "Text to speech", "icon": "record_voice_over"},
    {"label": "Enhance video", "icon": "high_quality"},
]

NAVIGATION = [
    {"id": "home", "label": "Edit", "icon": "movie_edit"},
    {"id": "templates", "label": "Templates", "icon": "dashboard"},
    {"id": "spaces", "label": "Spaces", "icon": "cloud"},
    {"id": "profile", "label": "Me", "icon": "person"},
]


def resolve_media_directory(
    preferred: Path,
) -> Path | None:
    for directory in (preferred, ASSETS_ROOT):
        if get_image_files(str(directory)):
            return directory

    return None


def generate_home_data(
    sample_index: int,
    thumbnails_dir: Path | None = None,
    avatars_dir: Path | None = None,
) -> dict:
    thumbnails = resolve_media_directory(
        thumbnails_dir or ASSETS_ROOT / "capcut" / "thumbnails"
    )
    avatars = resolve_media_directory(
        avatars_dir or ASSETS_ROOT / "capcut" / "avatars"
    )

    project_count = random.randint(12, 24)
    projects = []

    for index in range(project_count):
        seconds = random.randint(12, 240)

        projects.append({
            "id": f"project_{sample_index}_{index}",
            "title": (
                f"{random.choice(PROJECT_NAMES)} "
                f"{index + 1:02d}"
            ),
            "thumbnail": (
                get_random_image(thumbnails)
                if thumbnails is not None
                else None
            ),
            "duration": f"{seconds // 60:02d}:{seconds % 60:02d}",
            "updated": random.choice([
                "Edited just now",
                "Edited 2 hours ago",
                "Edited yesterday",
                "Edited 3 days ago",
            ]),
            "aspect_ratio": random.choice(["9:16", "16:9", "1:1"]),
            "size": f"{random.randint(18, 480)} MB",
            "cloud_saved": random.random() < 0.45,
            "selected": False,
        })

    return {
        "sample_index": sample_index,
        "state": "projects",
        "popup_visible": False,
        "selection_mode": False,
        "selected_count": 0,
        "query": "",
        "sort_label": "Last edited",
        "view_mode": random.choice(["grid", "list"]),
        "active_tab": "local",
        "user_name": random.choice(["Alex", "Jamie", "Taylor", "Morgan"]),
        "avatar": (
            get_random_image(avatars)
            if avatars is not None
            else None
        ),
        "projects": projects,
        "tools": random.sample(TOOLS, k=random.randint(4, 6)),
        "navigation": [dict(item) for item in NAVIGATION],
        "target_project": dict(projects[0]),
        "rename_value": projects[0]["title"],
        "show_promotion": random.random() < 0.7,
    }


def apply_home_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in HOME_STATES:
        raise ValueError(f"Unknown CapCut home state: {state}")

    data = dict(base_data)
    data["projects"] = [
        dict(project)
        for project in base_data["projects"]
    ]
    data["target_project"] = dict(base_data["target_project"])
    data["state"] = state
    data["popup_visible"] = state in {
        "rename_dialog",
        "delete_dialog",
    }
    data["selection_mode"] = state == "selection_mode"
    data["selected_count"] = 0
    data["query"] = ""

    if state == "empty":
        data["projects"] = []

    elif state == "search_results":
        query = data["projects"][0]["title"].split()[0]
        data["query"] = query
        data["projects"] = [
            project
            for project in data["projects"]
            if query.casefold() in project["title"].casefold()
        ]

    elif state == "selection_mode":
        selected_ids = {
            project["id"]
            for project in random.sample(
                data["projects"],
                k=random.randint(1, min(4, len(data["projects"]))),
            )
        }

        for project in data["projects"]:
            project["selected"] = project["id"] in selected_ids

        data["selected_count"] = len(selected_ids)

    return data