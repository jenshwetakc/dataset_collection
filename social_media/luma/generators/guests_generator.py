from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

AVATARS_DIR = ASSETS_ROOT / "avatars"

GUEST_STATES = [
    "all",
    "pending",
    "waitlist",
    "checked_in",
    "search_results",
    "bulk_selected",
    "guest_details",
    "invite_dialog",
    "empty",
]

STATUSES = ["Going", "Pending", "Waitlist", "Not Going"]


def generate_guests_data(
    sample_index: int = 0,
    *,
    avatars_dir: str | Path | None = None,
) -> dict:
    directory = Path(
        avatars_dir if avatars_dir is not None else AVATARS_DIR
    ).expanduser()

    guests = []

    for index in range(random.randint(24, 38)):
        name = fake.name()

        # Ensure each status is represented.
        status = (
            STATUSES[index]
            if index < len(STATUSES)
            else random.choice(STATUSES)
        )

        checked_in = (
            status == "Going"
            and (index == 0 or random.random() < 0.45)
        )

        guests.append({
            "id": f"guest_{sample_index}_{index}",
            "name": name,
            "email": fake.safe_email(),
            "avatar": get_random_image(directory),
            "initials": "".join(
                part[0] for part in name.split()[:2]
            ).upper(),
            "status": status,
            "ticket": random.choice([
                "General Admission",
                "Early Bird",
                "Community Ticket",
            ]),
            "registered": fake.date_between(
                start_date="-30d",
                end_date="today",
            ).strftime("%b %d"),
            "checked_in": checked_in,
            "selected": False,
        })

    return {
        "state": "all",
        "popup_visible": False,
        "event_title": random.choice([
            "Creative Community Evening",
            "Builders and Ideas Meetup",
            "Design Conversations",
        ]),
        "active_filter": "All",
        "search_query": "",
        "guests": guests,
        "visible_guests": guests,
        "selected_guest": guests[0],
        "selected_count": 0,
        "counts": {
            "All": len(guests),
            "Going": sum(g["status"] == "Going" for g in guests),
            "Pending": sum(g["status"] == "Pending" for g in guests),
            "Waitlist": sum(g["status"] == "Waitlist" for g in guests),
            "Checked In": sum(g["checked_in"] for g in guests),
        },
        "invitation_emails": "\n".join(
            fake.safe_email() for _ in range(3)
        ),
        "invitation_message": (
            "You’re invited! Join us for an evening "
            "of conversation and new connections."
        ),
    }


def apply_guests_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in GUEST_STATES:
        raise ValueError(f"Unknown guest state: {state}")

    data = deepcopy(page_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "guest_details",
        "invite_dialog",
    }

    if state in {"pending", "waitlist"}:
        status = "Pending" if state == "pending" else "Waitlist"
        data["active_filter"] = status
        data["visible_guests"] = [
            guest
            for guest in data["guests"]
            if guest["status"] == status
        ]

    elif state == "checked_in":
        data["active_filter"] = "Checked In"
        data["visible_guests"] = [
            guest for guest in data["guests"]
            if guest["checked_in"]
        ]

    elif state == "search_results":
        query = data["guests"][0]["name"].split()[0]
        data["search_query"] = query
        data["visible_guests"] = [
            guest for guest in data["guests"]
            if query.casefold() in guest["name"].casefold()
        ]

    elif state == "bulk_selected":
        for guest in data["visible_guests"][:3]:
            guest["selected"] = True
        data["selected_count"] = 3

    elif state == "empty":
        data["guests"] = []
        data["visible_guests"] = []
        data["counts"] = {
            key: 0 for key in data["counts"]
        }

    return data