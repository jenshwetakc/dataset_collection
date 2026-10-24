from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from social_media.tinypal.generators.home_generator import optional_image


FAMILY_STATES = [
    "overview",
    "pending_invites",
    "empty_caregivers",
    "invite_dialog",
    "permissions_sheet",
    "edit_child",
    "remove_dialog",
]


def generate_family_data(
    sample_index: int,
    avatars_dir: Path,
) -> dict:
    child_names = random.sample(
        ["Mia", "Noah", "Ava", "Leo", "Ella", "Lily"],
        k=2,
    )

    children = [
        {
            "id": f"family_child_{index}",
            "name": name,
            "initial": name[0],
            "age": f"{random.randint(4, 18)} months",
            "birth_date": random.choice([
                "2025-04-12",
                "2025-09-08",
                "2026-02-19",
            ]),
            "avatar": optional_image(avatars_dir),
            "note": random.choice([
                "Loves story time",
                "Enjoys family walks",
                "Favorite toy: soft blocks",
            ]),
        }
        for index, name in enumerate(child_names)
    ]

    caregivers = [
        {
            "id": "caregiver_owner",
            "name": "You",
            "initial": "Y",
            "email": "parent@example.com",
            "role": "Owner",
            "avatar": optional_image(avatars_dir),
            "owner": True,
        },
        {
            "id": "caregiver_sam",
            "name": "Sam Taylor",
            "initial": "S",
            "email": "sam@example.com",
            "role": "Caregiver",
            "avatar": optional_image(avatars_dir),
            "owner": False,
        },
        {
            "id": "caregiver_alex",
            "name": "Alex Morgan",
            "initial": "A",
            "email": "alex@example.com",
            "role": "Viewer",
            "avatar": optional_image(avatars_dir),
            "owner": False,
        },
    ]

    invitations = [
        {
            "id": "invite_0",
            "name": "Jordan",
            "email": "jordan@example.com",
            "role": "Caregiver",
            "status": "Pending",
        },
        {
            "id": "invite_1",
            "name": "Casey",
            "email": "casey@example.com",
            "role": "Viewer",
            "status": "Pending",
        },
    ]

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "popup_kind": None,
        "active_tab": "members",
        "family_name": random.choice([
            "Our little family",
            "The Taylor family",
            "Home together",
        ]),
        "children": children,
        "caregivers": caregivers,
        "invitations": invitations,
        "selected_child": deepcopy(children[0]),
        "selected_caregiver": deepcopy(caregivers[1]),
        "invite_name": "",
        "invite_email": "",
        "invite_role": "Caregiver",
        "roles": [
            {
                "id": "Caregiver",
                "description": "View and add daily records",
            },
            {
                "id": "Viewer",
                "description": "View shared records",
            },
        ],
        "permissions": [
            {
                "id": "view_records",
                "title": "View activity records",
                "description": "Read the shared activity history",
                "enabled": True,
            },
            {
                "id": "add_records",
                "title": "Add activity records",
                "description": "Record new daily activities",
                "enabled": True,
            },
            {
                "id": "edit_routines",
                "title": "Edit routines",
                "description": "Update planned family activities",
                "enabled": False,
            },
            {
                "id": "receive_updates",
                "title": "Receive updates",
                "description": "Get notifications for shared records",
                "enabled": random.choice([True, False]),
            },
        ],
        "navigation": [
            {"label": "Today", "icon": "home", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": True},
        ],
    }


def apply_family_state(base_data: dict, state: str) -> dict:
    if state not in FAMILY_STATES:
        raise ValueError(f"Unknown family state: {state}")

    data = deepcopy(base_data)
    data["state"] = state

    popup_states = {
        "invite_dialog",
        "permissions_sheet",
        "edit_child",
        "remove_dialog",
    }

    data["popup_visible"] = state in popup_states
    data["popup_kind"] = state if state in popup_states else None

    if state == "pending_invites":
        data["active_tab"] = "invites"

    elif state == "empty_caregivers":
        data["caregivers"] = [
            person for person in data["caregivers"]
            if person["owner"]
        ]
        data["invitations"] = []

    data["additional_caregivers"] = sum(
        not person["owner"]
        for person in data["caregivers"]
    )

    data["member_count"] = len(data["caregivers"])
    data["invite_count"] = len(data["invitations"])

    return data