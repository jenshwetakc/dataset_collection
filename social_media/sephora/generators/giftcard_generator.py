from __future__ import annotations

import calendar
import random

from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

GIFTCARD_STATES = [
    "design_selected",
    "custom_amount",
    "recipient_filled",
    "scheduled_delivery",
    "date_picker",
    "validation_error",
    "preview_dialog",
    "added",
]


def generate_giftcard_data(sample_index: int = 0, media_dir: Path | None = None,) -> dict:
    delivery_date = date.today() + timedelta(
        days=random.randint(2, 20)
    )
    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    return {
        "sample_index": sample_index,
        "state": "design_selected",
        "popup_visible": False,
        "designs": [
            {"id": "classic", "name": "Classic", "symbol": "redeem"},
            {"id": "birthday", "name": "Birthday", "symbol": "cake"},
            {"id": "thanks", "name": "Thank You", "symbol": "favorite"},
            {"id": "celebrate", "name": "Celebrate", "symbol": "celebration"},
        ],
        "selected_design": random.choice([
            "classic", "birthday", "thanks", "celebrate",
        ]),
        "amounts": [25, 50, 75, 100, 150],
        "amount": 50,
        "image": get_random_image(directory),
        "custom_amount": "",
        "recipient_name": fake.first_name(),
        "recipient_email": fake.safe_email(),
        "sender_name": fake.first_name(),
        "message": random.choice([
            "A little something to brighten your day!",
            "Celebrate yourself with something you love.",
            "Thank you for everything!",
        ]),
        "delivery_mode": "now",
        "date_label": delivery_date.strftime("%B %d, %Y"),
        "month_label": delivery_date.strftime("%B %Y"),
        "selected_day": delivery_date.day,
        "weeks": calendar.Calendar(
            firstweekday=6
        ).monthdayscalendar(
            delivery_date.year,
            delivery_date.month,
        ),
    }


def apply_giftcard_state(base_data: dict, state: str) -> dict:
    if state not in GIFTCARD_STATES:
        raise ValueError(f"Unknown gift-card state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state == "preview_dialog"

    if state == "custom_amount":
        data["amount"] = 125
        data["custom_amount"] = "125"

    if state in ["scheduled_delivery", "date_picker"]:
        data["delivery_mode"] = "scheduled"

    if state == "design_selected":
        data["recipient_name"] = ""
        data["recipient_email"] = ""
        data["sender_name"] = ""
        data["message"] = ""

    if state == "validation_error":
        data["recipient_email"] = "invalid-email"

    return data