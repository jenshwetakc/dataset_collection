from __future__ import annotations

import random
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

EVENT_IMAGES_DIR = ASSETS_ROOT / "luma"
AVATARS_DIR = ASSETS_ROOT / "luma"

MY_EVENTS_STATES = [
    "upcoming",
    "past",
    "hosting",
    "invitations",
    "search_results",
    "empty",
    "cancel_dialog",
]

EVENT_TITLES = [
    "Creative Coffee Club",
    "Builders and Ideas",
    "Community Supper",
    "Photography Walk",
    "Design Conversations",
    "Weekend Social",
    "AI Demo Evening",
    "Independent Film Night",
]


def generate_my_events_data(
    sample_index: int = 0,
    *,
    event_images_dir: str | Path | None = None,
    avatars_dir: str | Path | None = None,
) -> dict:
    images_dir = Path(
        event_images_dir
        if event_images_dir is not None
        else EVENT_IMAGES_DIR
    ).expanduser()

    avatar_dir = Path(
        avatars_dir
        if avatars_dir is not None
        else AVATARS_DIR
    ).expanduser()

    name = fake.name()
    city = fake.city()

    now = datetime.now().replace(
        hour=18, minute=0, second=0, microsecond=0,
    )

    def make_events(kind: str) -> list[dict]:
        records = []

        for index in range(random.randint(8, 13)):
            offset = index * 2 + 1
            date = now + timedelta(
                days=-offset if kind == "past" else offset
            )
            online = random.random() < 0.25

            status = (
                "Attended" if kind == "past"
                else "Hosting" if kind == "hosting"
                else "Invited" if kind == "invitations"
                else random.choice(["Going", "Going", "Pending"])
            )

            records.append({
                "id": f"my_events_{sample_index}_{kind}_{index}",
                "title": random.choice(EVENT_TITLES),
                "date": date.strftime("%A, %B %d"),
                "month": date.strftime("%b").upper(),
                "day": date.strftime("%d"),
                "time": date.strftime("%I:%M %p").lstrip("0"),
                "host": fake.name(),
                "location": (
                    "Online Event"
                    if online else f"{fake.street_name()} Studio"
                ),
                "online": online,
                "image": get_random_image(images_dir),
                "status": status,
                "attendees": random.randint(12, 160),
                "kind": kind,
            })

        return records

    upcoming = make_events("upcoming")
    past = make_events("past")
    hosting = make_events("hosting")
    invitations = make_events("invitations")

    # Ensure the cancellation target is a confirmed registration.
    upcoming[0]["status"] = "Going"

    return {
        "state": "upcoming",
        "popup_visible": False,
        "active_tab": "upcoming",
        "active_filter": "all",
        "search_query": "",
        "name": name,
        "initials": "".join(
            part[0] for part in name.split()[:2]
        ).upper(),
        "avatar": get_random_image(avatar_dir),
        "city": city,
        "upcoming_events": upcoming,
        "past_events": past,
        "hosting_events": hosting,
        "invitation_events": invitations,
        "visible_events": upcoming,
        "selected_event": upcoming[0],
        "invitation_count": len(invitations),
    }


def apply_my_events_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in MY_EVENTS_STATES:
        raise ValueError(f"Unknown My Events state: {state}")

    data = deepcopy(page_data)
    data["state"] = state
    data["popup_visible"] = state == "cancel_dialog"

    if state == "past":
        data["active_tab"] = "past"
        data["visible_events"] = data["past_events"]

    elif state == "hosting":
        data["active_filter"] = "hosting"
        data["visible_events"] = data["hosting_events"]

    elif state == "invitations":
        data["active_filter"] = "invitations"
        data["visible_events"] = data["invitation_events"]

    elif state == "search_results":
        query = data["upcoming_events"][0]["title"].split()[0]
        data["search_query"] = query
        data["visible_events"] = [
            event
            for event in data["upcoming_events"]
            if query.casefold() in event["title"].casefold()
        ]

    elif state == "empty":
        data["visible_events"] = []

    return data