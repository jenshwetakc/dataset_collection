from __future__ import annotations

import random

from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    # LUMA,
    get_random_image,
)

fake = Faker()


# ==========================================================
# Asset Directories
# ==========================================================

EVENT_COVERS_DIR = ASSETS_ROOT / "luma"
HOST_AVATARS_DIR = ASSETS_ROOT / "luma"
print(EVENT_COVERS_DIR)

# To use absolute paths instead:
#
# EVENT_COVERS_DIR = Path("/absolute/path/to/event/images")
# HOST_AVATARS_DIR = Path("/absolute/path/to/avatar/images")


# ==========================================================
# Page States
# ==========================================================

DISCOVER_STATES = [
    "browse",
    "search_results",
    "category_selected",
    "empty_results",
    "filter_dialog",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [
    {"name": "All", "icon": "explore"},
    {"name": "Technology", "icon": "memory"},
    {"name": "Arts", "icon": "palette"},
    {"name": "Wellness", "icon": "spa"},
    {"name": "Food", "icon": "restaurant"},
    {"name": "Community", "icon": "groups"},
]

EVENT_NAMES = {
    "Technology": [
        "Builders & Ideas",
        "AI Demo Night",
        "Creative Coding Workshop",
        "Startup Coffee Club",
        "Design and Technology Meetup",
    ],
    "Arts": [
        "Sketch Together",
        "Photography Walk",
        "Independent Film Evening",
        "Studio Open House",
        "Creative Community Night",
    ],
    "Wellness": [
        "Morning Movement",
        "Mindful Sunday",
        "Sunset Yoga",
        "Weekend Walking Club",
        "Breathe and Reset",
    ],
    "Food": [
        "Community Supper",
        "Coffee Tasting",
        "Weekend Brunch Club",
        "Cooking Together",
        "Neighborhood Food Walk",
    ],
    "Community": [
        "Meet Your Neighbors",
        "Book Club Evening",
        "Language Exchange",
        "Volunteer Together",
        "New Friends Social",
    ],
}


# ==========================================================
# Generate Discover Data
# ==========================================================

def generate_discover_page(
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

    city = fake.city()

    selected_category = random.choice(
        list(EVENT_NAMES)
    )

    events = []

    base_date = datetime.now() + timedelta(
        days=random.randint(1, 7)
    )

    for index in range(random.randint(15, 23)):
        category = random.choice(
            list(EVENT_NAMES)
        )

        starts_at = (
            base_date
            + timedelta(
                days=index // 3,
                hours=random.randint(9, 20),
            )
        )

        events.append({
            "id": f"event_{sample_index}_{index}",
            "title": random.choice(
                EVENT_NAMES[category]
            ),
            "category": category,
            "host": fake.name(),
            "venue": f"{fake.street_name()} Studio",
            "city": city,
            "date": starts_at.strftime("%a, %b %d"),
            "time": starts_at.strftime(
                "%I:%M %p"
            ).lstrip("0"),

            # Load images only from the configured folders.
            "cover": get_random_image(covers_dir),
            "avatar": get_random_image(avatars_dir),

            "initials": fake.lexify("??").upper(),
            "price": random.choice([
                "Free",
                "$10",
                "$15",
                "$25",
            ]),
            "attendees": random.randint(8, 180),
            "saved": random.random() < 0.25,
        })

    # Ensure the selected category has enough examples.
    for event in events[:5]:
        event["category"] = selected_category
        event["title"] = random.choice(
            EVENT_NAMES[selected_category]
        )

    return {
        "state": "browse",
        "popup_visible": False,
        "city": city,
        "heading": "Discover Events",
        "subtitle": "Find your next gathering.",
        "search_query": "",
        "selected_category": selected_category,
        "active_category": "All",
        "categories": deepcopy(CATEGORIES),
        "events": events,
        "visible_events": events,
        "date_options": [
            "Any time",
            "Today",
            "Tomorrow",
            "This weekend",
        ],
        "format_options": [
            "Any format",
            "In person",
            "Online",
        ],
        "date_filter": "Any time",
        "format_filter": "Any format",
        "free_only": random.choice([True, False]),
    }


# ==========================================================
# Apply Page State
# ==========================================================

def apply_discover_state(
    page_data: dict,
    state: str,
) -> dict:

    if state not in DISCOVER_STATES:
        raise ValueError(
            f"Unknown Discover state: {state}"
        )

    data = deepcopy(page_data)

    data["state"] = state
    data["popup_visible"] = (
        state == "filter_dialog"
    )

    if state == "category_selected":
        category = data["selected_category"]

        data["active_category"] = category
        data["heading"] = f"{category} Events"

        data["visible_events"] = [
            event
            for event in data["events"]
            if event["category"] == category
        ]

    elif state == "search_results":
        query = (
            data["events"][0]["title"].split()[0]
        )

        data["search_query"] = query
        data["heading"] = "Search Results"
        data["subtitle"] = (
            f'Events matching “{query}”'
        )

        data["visible_events"] = [
            event
            for event in data["events"]
            if (
                query.casefold()
                in event["title"].casefold()
            )
        ]

    elif state == "empty_results":
        data["search_query"] = (
            "Underwater astronomy club"
        )
        data["heading"] = "Search Results"
        data["subtitle"] = (
            "Try another search or location."
        )
        data["visible_events"] = []

    return data