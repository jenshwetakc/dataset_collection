from __future__ import annotations

import random
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

AVATARS_DIR = ASSETS_ROOT / "luma" / "avatars"

BLAST_STATES = [
    "feed",
    "composer",
    "validation_errors",
    "preview",
    "schedule_dialog",
    "scheduled",
    "empty",
    "delete_dialog",
]

RECIPIENT_STATUSES = [
    "Going",
    "Checked In",
    "Pending",
    "Waitlist",
    "Invited",
]

MESSAGE_EXAMPLES = [
    (
        "Getting ready for tomorrow",
        "We’re looking forward to seeing you!",
        "Doors open 20 minutes before the event. "
        "Please have your ticket ready when you arrive.",
    ),
    (
        "A quick venue update",
        "Here’s everything you need to know.",
        "We’ll meet at the main entrance. "
        "Our team will be there to welcome you and help you check in.",
    ),
    (
        "Thank you for joining us",
        "It was lovely bringing everyone together.",
        "Thank you for sharing your time and ideas. "
        "We hope to see you at another gathering soon.",
    ),
    (
        "Meet our special guest",
        "We have something exciting to share.",
        "A special guest will join our conversation. "
        "Bring your questions and get ready for an inspiring evening.",
    ),
]


def generate_blasts_data(
    sample_index: int = 0,
    *,
    avatars_dir: Path | None = None,
) -> dict:
    avatar_folder = (
        Path(avatars_dir)
        if avatars_dir is not None
        else AVATARS_DIR
    )

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    scheduled_at = now + timedelta(days=1)

    host_name = fake.name()
    initials = "".join(
        part[0]
        for part in host_name.split()[:2]
    ).upper()

    subject, introduction, body = random.choice(
        MESSAGE_EXAMPLES
    )

    messages = []

    for index in range(random.randint(3, 7)):
        title, opening, content = random.choice(
            MESSAGE_EXAMPLES
        )
        sent_at = now - timedelta(
            days=index + 1,
            hours=random.randint(0, 8),
        )

        messages.append({
            "id": f"blast_{sample_index}_{index}",
            "subject": title,
            "introduction": opening,
            "body": content,
            "status": "Sent",
            "timestamp": sent_at.strftime(
                "%b %d, %Y · %I:%M %p"
            ),
            "recipients": random.choice([
                "Going",
                "Going, Checked In",
                "Waitlist",
            ]),
        })

    return {
        "state": "feed",
        "popup_visible": False,
        "editor_visible": False,
        "event_title": random.choice([
            "Creative Community Night",
            "Builders & Ideas",
            "Weekend Coffee Club",
        ]),
        "host_name": host_name,
        "host_initials": initials,
        "host_avatar": get_random_image(
            avatar_folder
        ),
        "recipient_statuses": list(
            RECIPIENT_STATUSES
        ),
        "selected_recipients": ["Going"],
        "recipient_count": random.randint(25, 180),
        "quick_message": "",
        "subject": subject,
        "introduction": introduction,
        "body": body,
        "errors": {},
        "messages": messages,
        "selected_message": messages[0],
        "schedule_date": scheduled_at.strftime(
            "%Y-%m-%d"
        ),
        "schedule_time": "09:00",
        "timezone": "Asia/Seoul",
        "scheduled_label": scheduled_at.strftime(
            "%b %d, %Y"
        ) + " · 9:00 AM",
    }


def apply_blasts_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in BLAST_STATES:
        raise ValueError(
            f"Unknown Blasts state: {state}"
        )

    data = deepcopy(page_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "preview",
        "schedule_dialog",
        "delete_dialog",
    }
    data["editor_visible"] = state in {
        "composer",
        "validation_errors",
        "preview",
        "schedule_dialog",
    }
    data["errors"] = {}

    if state == "validation_errors":
        data["subject"] = ""
        data["introduction"] = ""
        data["body"] = ""
        data["errors"] = {
            "subject": "Add a subject line.",
            "body": "Write a message before continuing.",
        }

    elif state == "empty":
        data["messages"] = []

    elif state in {
        "scheduled",
        "delete_dialog",
    }:
        scheduled_message = {
            "id": "scheduled_blast",
            "subject": data["subject"],
            "introduction": data["introduction"],
            "body": data["body"],
            "status": "Scheduled",
            "timestamp": (
                data["scheduled_label"]
                + " · "
                + data["timezone"]
            ),
            "recipients": ", ".join(
                data["selected_recipients"]
            ),
        }

        data["messages"].insert(
            0,
            scheduled_message,
        )
        data["selected_message"] = (
            scheduled_message
        )

    return data