from __future__ import annotations

import random
from copy import deepcopy


ACCOUNT_STATES = [
    "overview",
    "profile_editing",
    "profile_error",
    "notifications",
    "appearance",
    "sessions",
    "specialty_dialog",
    "sign_out_dialog",
]

ACCOUNT_SECTIONS = [
    {"id": "overview", "label": "Overview", "icon": "account_circle"},
    {"id": "profile", "label": "Profile", "icon": "person"},
    {"id": "notifications", "label": "Notifications", "icon": "notifications"},
    {"id": "appearance", "label": "Appearance", "icon": "palette"},
    {"id": "sessions", "label": "Devices", "icon": "devices"},
]


def generate_account_data(sample_index: int) -> dict:
    first = random.choice(["Alex", "Jordan", "Morgan", "Taylor"])
    last = random.choice(["Lee", "Patel", "Kim", "Chen"])

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "popup_kind": None,
        "active_section": "overview",
        "sections": deepcopy(ACCOUNT_SECTIONS),
        "user": {
            "name": f"{first} {last}",
            "initials": first[0] + last[0],
            "email": f"{first.lower()}.{last.lower()}@example.com",
            "organization": random.choice([
                "University Medical Center",
                "Community Health Center",
                "Teaching Hospital",
            ]),
        },
        "specialty": random.choice([
            "Internal medicine", "Family medicine", "Pediatrics",
        ]),
        "specialties": [
            "Internal medicine",
            "Family medicine",
            "Pediatrics",
            "Emergency medicine",
            "Cardiology",
            "Neurology",
        ],
        "errors": {},
        "notifications": [
            {
                "id": "topic_updates",
                "label": "Topic updates",
                "description": "Updates for saved reference topics.",
                "enabled": True,
            },
            {
                "id": "product_news",
                "label": "Product news",
                "description": "Information about workspace features.",
                "enabled": False,
            },
            {
                "id": "download_alerts",
                "label": "Download alerts",
                "description": "Offline resource download status.",
                "enabled": True,
            },
            {
                "id": "reading_reminders",
                "label": "Reading reminders",
                "description": "Reminders to revisit your reading list.",
                "enabled": random.choice([True, False]),
            },
        ],
        "appearance_choice": "system",
        "appearance_options": [
            {"id": "system", "label": "System default", "icon": "devices"},
            {"id": "light", "label": "Light", "icon": "light_mode"},
            {"id": "dark", "label": "Dark", "icon": "dark_mode"},
        ],
        "text_size": 16,
        "text_sizes": [14, 16, 18, 20],
        "sessions": [
            {
                "id": "current",
                "name": "Current device",
                "description": "This browser",
                "icon": "laptop",
                "current": True,
            },
            {
                "id": "phone",
                "name": "Mobile device",
                "description": "Last active yesterday",
                "icon": "smartphone",
                "current": False,
            },
            {
                "id": "tablet",
                "name": "Tablet",
                "description": "Last active this week",
                "icon": "tablet",
                "current": False,
            },
        ],
    }


def apply_account_state(base_data: dict, state: str) -> dict:
    if state not in ACCOUNT_STATES:
        raise ValueError(f"Unknown account state: {state!r}")

    data = deepcopy(base_data)
    data.update({
        "state": state,
        "popup_visible": False,
        "popup_kind": None,
        "active_section": "overview",
        "errors": {},
    })

    if state in {"profile_editing", "profile_error", "specialty_dialog"}:
        data["active_section"] = "profile"

    elif state in {"notifications", "appearance", "sessions"}:
        data["active_section"] = state

    if state == "profile_error":
        data["user"]["email"] = "alex.example"
        data["errors"]["email"] = "Enter a valid email address."

    elif state == "specialty_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "specialty"

    elif state == "sign_out_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "sign_out"

    return data