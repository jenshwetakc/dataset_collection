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

EVENT_COVERS_DIR = ASSETS_ROOT / "luma"
HOST_AVATARS_DIR = ASSETS_ROOT / "luma"

EVENT_STATES = [
    "available",
    "registered",
    "pending_approval",
    "sold_out",
    "registration_dialog",
    "share_dialog",
    "cancel_dialog",
]

EVENT_TITLES = [
    "Creative Community Evening",
    "Builders and Ideas Meetup",
    "Weekend Photography Walk",
    "Design Together Workshop",
    "Community Coffee Club",
    "Independent Film Night",
]


def generate_event_page(
    sample_index: int = 0,
    *,
    event_covers_dir: str | Path | None = None,
    host_avatars_dir: str | Path | None = None,
) -> dict:
    covers_dir = Path(
        event_covers_dir
        if event_covers_dir is not None
        else EVENT_COVERS_DIR
    ).expanduser()

    avatars_dir = Path(
        host_avatars_dir
        if host_avatars_dir is not None
        else HOST_AVATARS_DIR
    ).expanduser()

    starts_at = (
        datetime.now().replace(
            hour=random.randint(10, 19),
            minute=random.choice([0, 30]),
            second=0,
            microsecond=0,
        )
        + timedelta(days=random.randint(2, 30))
    )

    duration = random.choice([90, 120, 180])
    ends_at = starts_at + timedelta(minutes=duration)

    host_name = fake.name()
    guest_name = fake.name()
    online = random.random() < 0.25
    price = random.choice([0, 10, 15, 25])
    attendee_count = random.randint(15, 150)

    hosts = []
    for index in range(random.randint(1, 3)):
        name = host_name if index == 0 else fake.name()
        hosts.append({
            "name": name,
            "initials": "".join(
                part[0] for part in name.split()[:2]
            ).upper(),
            "avatar": get_random_image(avatars_dir),
        })

    return {
        "state": "available",
        "popup_visible": False,
        "sample_index": sample_index,
        "title": random.choice(EVENT_TITLES),
        "cover": get_random_image(covers_dir),
        "category": random.choice([
            "Community", "Technology", "Arts", "Design",
        ]),
        "calendar_name": f"{fake.word().title()} Collective",
        "date": starts_at.strftime("%A, %B %d"),
        "month": starts_at.strftime("%b").upper(),
        "day": starts_at.strftime("%d"),
        "start_time": starts_at.strftime("%I:%M %p").lstrip("0"),
        "end_time": ends_at.strftime("%I:%M %p").lstrip("0"),
        "timezone": "Local time",
        "online": online,
        "venue": "Online Event" if online else f"{fake.street_name()} Studio",
        "address": (
            "Join link provided after registration"
            if online else fake.address()
        ),
        "hosts": hosts,
        "attendee_count": attendee_count,
        "capacity": attendee_count + random.randint(10, 50),
        "price": price,
        "price_text": "Free" if price == 0 else f"${price}",
        "guest_name": guest_name,
        "guest_email": fake.safe_email(),
        "share_url": f"https://example.com/events/event-{sample_index:06d}",
        "description": [
            "Join a welcoming gathering of curious people, "
            "share ideas, and make new connections.",
            "The event includes guided activities, informal "
            "conversation, and time to explore together.",
            "Everyone is welcome. Bring your curiosity and "
            "arrive a few minutes before the event begins.",
        ],
        "agenda": [
            {"time": "First 15 minutes", "title": "Welcome and introductions"},
            {"time": "Next 45 minutes", "title": "Main session"},
            {"time": "Final 30 minutes", "title": "Conversation and networking"},
        ],
        "questions": [
            "What should I bring?",
            "Can I attend on my own?",
            "How do I contact the host?",
        ],
        "status_title": "You're invited",
        "status_message": "Reserve your place to join this event.",
        "action_label": "Register",
    }


def apply_event_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in EVENT_STATES:
        raise ValueError(f"Unknown event state: {state}")

    data = deepcopy(page_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "registration_dialog",
        "share_dialog",
        "cancel_dialog",
    }

    if state in {"registered", "cancel_dialog"}:
        data["status_title"] = "You're going!"
        data["status_message"] = (
            "Your registration is confirmed. "
            "We look forward to seeing you."
        )
        data["action_label"] = "View Ticket"

    elif state == "pending_approval":
        data["status_title"] = "Registration pending"
        data["status_message"] = (
            "The host will review your request "
            "and notify you when it is approved."
        )
        data["action_label"] = "Request Submitted"

    elif state == "sold_out":
        data["attendee_count"] = data["capacity"]
        data["status_title"] = "This event is full"
        data["status_message"] = (
            "Join the waitlist to hear if a place becomes available."
        )
        data["action_label"] = "Join Waitlist"

    return data