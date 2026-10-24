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

# Change these to your actual folders.
BANNERS_DIR = ASSETS_ROOT / "luma"
EVENT_IMAGES_DIR = ASSETS_ROOT / "luma"
AVATARS_DIR = ASSETS_ROOT / "avatars"

CALENDAR_STATES = [
    "upcoming",
    "past",
    "subscribed",
    "empty",
    "subscribe_dialog",
    "share_dialog",
]

EVENT_TITLES = [
    "Community Coffee Morning",
    "Creative Workshop",
    "Builders Meetup",
    "Photography Walk",
    "Design Conversations",
    "Weekend Social",
    "Book Club Evening",
    "Ideas and Inspiration",
]


def generate_calendar_data(
    sample_index: int = 0,
    *,
    banners_dir: str | Path | None = None,
    event_images_dir: str | Path | None = None,
    avatars_dir: str | Path | None = None,
) -> dict:
    banners = Path(
        banners_dir if banners_dir is not None else BANNERS_DIR
    ).expanduser()

    event_images = Path(
        event_images_dir
        if event_images_dir is not None
        else EVENT_IMAGES_DIR
    ).expanduser()

    avatars = Path(
        avatars_dir if avatars_dir is not None else AVATARS_DIR
    ).expanduser()

    city = fake.city()
    community_name = f"{fake.word().title()} Collective"

    now = datetime.now().replace(
        hour=18,
        minute=0,
        second=0,
        microsecond=0,
    )

    def make_events(past: bool) -> list[dict]:
        events = []

        for index in range(random.randint(10, 16)):
            offset = index * 3 + random.randint(1, 3)
            event_date = now + timedelta(
                days=-offset if past else offset
            )

            events.append({
                "id": (
                    f"calendar_{sample_index}_"
                    f"{'past' if past else 'upcoming'}_{index}"
                ),
                "title": random.choice(EVENT_TITLES),
                "month": event_date.strftime("%b").upper(),
                "day": event_date.strftime("%d"),
                "date": event_date.strftime("%A, %B %d"),
                "time": event_date.strftime("%I:%M %p").lstrip("0"),
                "host": fake.name(),
                "venue": f"{fake.street_name()} Studio",
                "image": get_random_image(event_images),
                "price": random.choice(["Free", "$10", "$15", "$25"]),
                "attendees": random.randint(12, 180),
                "past": past,
            })

        return sorted(
            events,
            key=lambda event: next(
                index
                for index, candidate in enumerate(events)
                if candidate is event
            ),
        )

    upcoming_events = make_events(False)
    past_events = make_events(True)

    hosts = []

    for _ in range(random.randint(2, 4)):
        name = fake.name()
        hosts.append({
            "name": name,
            "avatar": get_random_image(avatars),
            "initials": "".join(
                part[0] for part in name.split()[:2]
            ).upper(),
        })

    return {
        "state": "upcoming",
        "popup_visible": False,
        "active_tab": "upcoming",
        "subscribed": False,
        "community_name": community_name,
        "city": city,
        "banner": get_random_image(banners),
        "avatar": get_random_image(avatars),
        "initials": "".join(
            word[0] for word in community_name.split()[:2]
        ).upper(),
        "description": (
            "A welcoming community for curious people. "
            "Join our gatherings, meet new friends, "
            "and explore ideas together."
        ),
        "subscriber_count": random.randint(200, 8500),
        "hosts": hosts,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "visible_events": upcoming_events,
        "guest_name": fake.name(),
        "guest_email": fake.safe_email(),
        "email_updates": True,
        "share_url": (
            f"https://example.com/calendars/"
            f"community-{sample_index:06d}"
        ),
    }


def apply_calendar_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in CALENDAR_STATES:
        raise ValueError(f"Unknown calendar state: {state}")

    data = deepcopy(page_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "subscribe_dialog",
        "share_dialog",
    }
    data["subscribed"] = state == "subscribed"
    data["active_tab"] = "past" if state == "past" else "upcoming"

    data["visible_events"] = (
        data["past_events"]
        if state == "past"
        else data["upcoming_events"]
    )

    if state == "empty":
        data["visible_events"] = []

    return data