from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


SPACES_STATES = [
    "overview",
    "shared_projects",
    "empty_space",
    "uploading",
    "create_folder_dialog",
    "invite_dialog",
]

PROJECT_NAMES = [
    "Travel highlights",
    "Brand campaign",
    "Weekend vlog",
    "Product launch",
    "Summer collection",
    "Studio session",
    "Daily moments",
    "City stories",
]

MEMBER_NAMES = ["Alex Morgan", "Jamie Lee", "Taylor Kim", "Sam Park"]


def resolve_directory(preferred: Path) -> Path | None:
    for directory in (preferred, ASSETS_ROOT):
        if get_image_files(str(directory)):
            return directory

    return None


def generate_spaces_data(
    sample_index: int,
    thumbnails_dir: Path | None = None,
    avatars_dir: Path | None = None,
) -> dict:
    thumbnails = resolve_directory(
        thumbnails_dir or ASSETS_ROOT / "capcut" / "spaces"
    )
    avatars = resolve_directory(
        avatars_dir or ASSETS_ROOT / "capcut" / "avatars"
    )

    members = [
        {
            "id": f"member_{index}",
            "name": name,
            "avatar": get_random_image(avatars) if avatars else None,
            "role": "Owner" if index == 0 else "Editor",
        }
        for index, name in enumerate(MEMBER_NAMES)
    ]

    projects = []

    for index in range(random.randint(12, 20)):
        projects.append({
            "id": f"cloud_{sample_index}_{index}",
            "title": f"{random.choice(PROJECT_NAMES)} {index + 1:02d}",
            "image": get_random_image(thumbnails) if thumbnails else None,
            "updated": random.choice([
                "Updated today",
                "Updated yesterday",
                "Updated 3 days ago",
            ]),
            "size": f"{random.randint(25, 350)} MB",
            "duration": f"00:{random.randint(10, 59):02d}",
            "shared": index % 3 == 0,
            "owner": random.choice(MEMBER_NAMES),
        })

    used = round(random.uniform(1.5, 8.5), 1)

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "space_name": random.choice([
            "Creative Studio",
            "My Workspace",
            "Video Team",
        ]),
        "active_tab": "all",
        "projects": projects,
        "members": members,
        "folders": [
            {"id": "campaigns", "name": "Campaigns", "count": 8},
            {"id": "personal", "name": "Personal", "count": 5},
            {"id": "archive", "name": "Archive", "count": 12},
        ],
        "storage_used": used,
        "storage_total": 10,
        "storage_percent": round(used / 10 * 100),
        "upload_percent": random.randint(25, 85),
        "upload_name": "Weekend highlights.mp4",
        "folder_name": "New collection",
        "invite_email": "creator@example.com",
        "invite_role": "Editor",
        "notify_member": True,
    }


def apply_spaces_state(base_data: dict, state: str) -> dict:
    if state not in SPACES_STATES:
        raise ValueError(f"Unknown Spaces state: {state}")

    data = dict(base_data)
    data["projects"] = [dict(item) for item in base_data["projects"]]
    data["state"] = state
    data["popup_visible"] = state in {
        "create_folder_dialog",
        "invite_dialog",
    }
    data["active_tab"] = "shared" if state == "shared_projects" else "all"

    if state == "shared_projects":
        data["projects"] = [
            item for item in data["projects"] if item["shared"]
        ]

    elif state == "empty_space":
        data["projects"] = []
        data["folders"] = []

    return data