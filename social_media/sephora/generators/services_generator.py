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

SERVICES_STATES = [
    "overview",
    "store_dialog",
    "date_selected",
    "time_selected",
    "no_availability",
    "details_form",
    "validation_error",
    "confirmed",
]


def generate_services_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:

    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    services = [
        {
            "name": "Full Face",
            "duration": "60 minutes",
            "price": "$60",
            "description": "A complete makeup look for your occasion.",
        },
        {
            "name": "Beauty Lesson",
            "duration": "75 minutes",
            "price": "$75",
            "description": "Explore makeup techniques in a personal lesson.",
        },
        {
            "name": "Brow Wax",
            "duration": "20 minutes",
            "price": "$22",
            "description": "Brow shaping with a licensed Beauty Advisor.",
        },
    ]

    appointment_date = date.today() + timedelta(
        days=random.randint(3, 18)
    )

    weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(
        appointment_date.year,
        appointment_date.month,
    )

    stores = [
        {
            "id": index,
            "name": f"{fake.city()} Beauty Center",
            "address": fake.street_address(),
            "distance": f"{random.uniform(0.5, 12):.1f} miles",
        }
        for index in range(3)
    ]

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "service": random.choice(services),
        "hero_image": get_random_image(directory),
        "stores": stores,
        "store": stores[0],
        "month_label": appointment_date.strftime("%B %Y"),
        "weeks": weeks,
        "selected_day": appointment_date.day,
        "date_label": appointment_date.strftime("%B %d, %Y"),
        "times": [
            "10:00 AM",
            "11:30 AM",
            "1:00 PM",
            "2:30 PM",
            "4:00 PM",
            "5:30 PM",
        ],
        "selected_time": "1:00 PM",
        "customer": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.safe_email(),
            "phone": fake.numerify("202-555-01##"),
        },
        "confirmation_code": fake.bothify("DEMO-????-####").upper(),
        "faqs": [
            {
                "title": "Before your appointment",
                "body": (
                    "Review the service information and contact "
                    "your chosen store with preparation questions."
                ),
            },
            {
                "title": "Changing your reservation",
                "body": (
                    "Review the applicable reservation policies "
                    "before changing your appointment."
                ),
            },
        ],
    }


def apply_services_state(
    base_data: dict,
    state: str,
) -> dict:

    if state not in SERVICES_STATES:
        raise ValueError(f"Unknown services state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state == "store_dialog"

    if state == "validation_error":
        data["customer"]["email"] = ""
        data["customer"]["phone"] = ""

    return data