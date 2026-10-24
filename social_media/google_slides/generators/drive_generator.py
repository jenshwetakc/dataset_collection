from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

DRIVE_STATES = [
    "my_drive_grid",
    "my_drive_list",
    "folder_open",
    "search_results",
    "file_selected",
    "file_context_menu",
    "upload_progress",
    "share_dialog",
    "storage_warning",
]

FILE_TYPES = [
    ("document", "Document", "#4285F4"),
    ("spreadsheet", "Spreadsheet", "#0F9D58"),
    ("presentation", "Presentation", "#F4B400"),
    ("pdf", "PDF", "#DB4437"),
    ("image", "Image", "#9C27B0"),
]


def initials(name: str) -> str:
    return "".join(
        word[0].upper()
        for word in name.split()[:2]
    ) or "U"


def random_image() -> str | None:
    for directory in [
        ASSETS_ROOT / "photos",
        ASSETS_ROOT / "images",
        ASSETS_ROOT,
    ]:
        if directory.exists():
            value = get_random_image(directory)
            if value:
                return value
    return None


def generate_files() -> list[dict]:
    entries = []

    for index in range(random.randint(9, 14)):
        kind, label, color = random.choice(FILE_TYPES)
        owner = fake.name()

        entries.append(
            {
                "id": f"file_{index}",
                "name": (
                    fake.sentence(
                        nb_words=random.randint(2, 5),
                    ).rstrip(".")
                    + (
                        ".pdf"
                        if kind == "pdf"
                        else ""
                    )
                ),
                "kind": kind,
                "kind_label": label,
                "color": color,
                "modified": fake.date_between(
                    start_date="-90d",
                    end_date="today",
                ).strftime("%b %d, %Y"),
                "owner": owner,
                "owner_initials": initials(owner),
                "image_src": (
                    random_image()
                    if kind == "image"
                    else None
                ),
                "shared": random.random() < 0.38,
                "starred": random.random() < 0.25,
            }
        )

    return entries


def generate_folders() -> list[dict]:
    return [
        {
            "id": f"folder_{index}",
            "name": name,
            "color": random.choice(
                ["#1A73E8", "#0F9D58", "#9334E6"]
            ),
        }
        for index, name in enumerate(
            random.sample(
                [
                    "Research",
                    "Coursework",
                    "Product planning",
                    "Design assets",
                    "Team projects",
                    "Archive",
                ],
                k=3,
            )
        )
    ]


def generate_people() -> list[dict]:
    people = []

    for index in range(random.randint(2, 4)):
        name = fake.name()

        people.append(
            {
                "name": name,
                "initials": initials(name),
                "email": fake.email(),
                "color": random.choice(
                    ["#1A73E8", "#0F9D58", "#9334E6", "#E37400"]
                ),
            }
        )

    return people


def generate_drive_data(
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:
    del viewport

    state = state or random.choice(DRIVE_STATES)

    if state not in DRIVE_STATES:
        raise ValueError(
            f"Unsupported Drive state: {state}"
        )

    files = generate_files()
    folders = generate_folders()
    selected_file = random.choice(files)
    people = generate_people()

    folder_name = random.choice(
        [
            "Research",
            "Coursework",
            "Product planning",
        ]
    )

    return {
        "app_name": "Google Drive",
        "state": state,
        "view_mode": (
            "list"
            if state == "my_drive_list"
            else "grid"
        ),
        "folders": folders,
        "files": files,
        "selected_file": selected_file,
        "people": people,
        "active_navigation": (
            "Recent"
            if state == "search_results"
            else "My Drive"
        ),
        "breadcrumb": (
            ["My Drive", folder_name]
            if state == "folder_open"
            else ["My Drive"]
        ),
        "search": {
            "visible": state == "search_results",
            "query": random.choice(
                ["research", "project", "report", "design"]
            ),
        },
        "context_menu": {
            "visible": state == "file_context_menu",
            "menu_entries": [
                "Open",
                "Share",
                "Get link",
                "Organize",
                "Download",
                "Rename",
                "Remove",
            ],
        },
        "upload": {
            "visible": state == "upload_progress",
            "file_name": (
                fake.file_name(
                    extension="pdf",
                )
            ),
            "progress": random.randint(18, 92),
        },
        "share_dialog": {
            "visible": state == "share_dialog",
            "link_access": random.choice(
                ["Restricted", "Anyone with the link"]
            ),
        },
        "storage": {
            "used": random.randint(12, 14),
            "total": 15,
            "warning_visible": state == "storage_warning",
        },
    }