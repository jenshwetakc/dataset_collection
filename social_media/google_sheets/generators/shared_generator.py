from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


SHARED_STATES = [
    "populated_grid",
    "populated_list",
    "empty",
    "loading",
    "search_results",
    "file_selected",
    "context_menu",
    "share_dialog",
    "access_request_dialog",
    "details_panel",
]

POPUP_STATES = {
    "context_menu",
    "share_dialog",
    "access_request_dialog",
}

FILE_TITLES = [
    "Quarterly revenue forecast",
    "Customer research notes",
    "Product launch checklist",
    "Campaign performance",
    "Hiring plan and budget",
    "Regional inventory",
    "Conference registrations",
    "Website experiment results",
    "Team capacity planner",
    "Operations dashboard",
]


def generate_shared_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(SHARED_STATES)
    if state not in SHARED_STATES:
        raise ValueError(
            f"Unknown shared page state: {state}. Expected one of {SHARED_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    compact = width < 600
    owners = [fake.name() for _ in range(6)]
    colors = ["#0F9D58", "#1A73E8", "#F9AB00", "#A142F4", "#D93025"]
    now = datetime.now()

    files = []
    for index, title in enumerate(random.sample(FILE_TITLES, k=8)):
        owner = random.choice(owners)
        files.append(
            {
                "id": index + 1,
                "title": title,
                "owner": owner,
                "owner_initial": owner[0].upper(),
                "owner_color": random.choice(colors),
                "modified": (now - timedelta(hours=random.randint(1, 240))).strftime("%b %d"),
                "shared_with": random.randint(2, 18),
                "starred": random.random() < 0.25,
                "preview_rows": [random.randint(20, 92) for _ in range(4)],
            }
        )

    selected_index = random.randrange(len(files))
    query = random.choice(["budget", "campaign", "team", "research"])
    display_files = files
    if state == "search_results":
        display_files = files[: random.randint(2, 4)]

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": compact,
        "view_mode": "list" if state == "populated_list" else "grid",
        "query": query if state == "search_results" else "",
        "files": display_files,
        "selected_id": files[selected_index]["id"],
        "selected_file": files[selected_index],
        "navigation": [
            {"icon": "home", "label": "Home", "active": False},
            {"icon": "schedule", "label": "Recent", "active": False},
            {"icon": "group", "label": "Shared with me", "active": True},
            {"icon": "star", "label": "Starred", "active": False},
            {"icon": "delete", "label": "Trash", "active": False},
        ],
        "filters": ["People", "Modified", "Type"],
        "context_actions": [
            {"icon": "open_in_new", "label": "Open"},
            {"icon": "person_add", "label": "Share"},
            {"icon": "link", "label": "Copy link"},
            {"icon": "drive_file_move", "label": "Organize"},
            {"icon": "info", "label": "File information"},
            {"icon": "block", "label": "Block owner"},
        ],
        "requester": fake.name(),
        "requester_email": fake.email(),
        "account_name": fake.name(),
        "account_initial": fake.first_name()[0].upper(),
    }
