from __future__ import annotations

import random
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


HOME_STATES = [
    "overview",
    "empty_day",
    "sleep_active",
    "child_switcher",
    "quick_log",
    "reminder_settings",
]


def optional_image(directory: Path) -> str | None:
    # Avoid repeated warnings when an optional directory is empty.
    if not get_image_files(str(directory)):
        return None

    return get_random_image(directory)


def generate_home_data(
    sample_index: int,
    avatars_dir: Path,
    articles_dir: Path,
) -> dict:
    names = random.sample(
        ["Mia", "Noah", "Ava", "Leo", "Ella", "Oliver", "Lily"],
        k=3,
    )

    children = [
        {
            "id": f"child_{index}",
            "name": name,
            "initial": name[0],
            "age": f"{random.randint(3, 18)} months",
            "avatar": optional_image(avatars_dir),
        }
        for index, name in enumerate(names)
    ]

    activities = [
        {
            "id": "feeding",
            "title": "Feeding",
            "icon": "water_drop",
            "value": f"{random.randint(3, 7)} feeds",
            "detail": "Last recorded at 10:15",
        },
        {
            "id": "sleep",
            "title": "Sleep",
            "icon": "bedtime",
            "value": f"{random.randint(6, 10)}h 25m",
            "detail": "Total recorded today",
        },
        {
            "id": "diaper",
            "title": "Diapers",
            "icon": "baby_changing_station",
            "value": f"{random.randint(2, 6)} changes",
            "detail": "Last recorded at 11:05",
        },
    ]

    routine_options = [
        ("Morning feed", "water_drop", "08:00"),
        ("Outdoor time", "park", "09:30"),
        ("Nap time", "bedtime", "11:00"),
        ("Story time", "menu_book", "14:00"),
        ("Evening bath", "bathtub", "18:30"),
    ]

    routines = [
        {
            "id": f"routine_{index}",
            "title": title,
            "icon": icon,
            "time": time,
            "completed": index < random.randint(1, 3),
        }
        for index, (title, icon, time) in enumerate(routine_options)
    ]

    article_options = [
        ("Making room for quiet play", "Play & learning", "5 min"),
        ("Building a gentle bedtime routine", "Daily routines", "4 min"),
        ("Small moments of connection", "Family life", "6 min"),
        ("Ideas for your next family walk", "Activities", "3 min"),
    ]

    articles = [
        {
            "id": f"article_{index}",
            "title": title,
            "category": category,
            "duration": duration,
            "image": optional_image(articles_dir),
            "saved": random.choice([True, False]),
        }
        for index, (title, category, duration) in enumerate(
            random.sample(article_options, k=3)
        )
    ]

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "popup_kind": None,
        "greeting": random.choice(
            ["Hello", "Welcome back", "Good morning"]
        ),
        "parent_name": random.choice(["Alex", "Sam", "Taylor", "Jordan"]),
        "date_label": datetime.now().strftime("%A, %B %d"),
        "children": children,
        "selected_child": children[0],
        "activities": activities,
        "routines": routines,
        "articles": articles,
        "notification_count": random.randint(1, 5),
        "empty_day": False,
        "sleep_active": False,
        "sleep_elapsed": f"00:{random.randint(10, 59):02d}:24",
        "log_types": [
            {"id": "feeding", "label": "Feeding", "icon": "water_drop"},
            {"id": "sleep", "label": "Sleep", "icon": "bedtime"},
            {
                "id": "diaper",
                "label": "Diaper",
                "icon": "baby_changing_station",
            },
        ],
        "selected_log_type": "feeding",
        "log_time": "11:30",
        "log_amount": str(random.choice([90, 120, 150, 180])),
        "log_note": "",
        "reminders": [
            {
                "id": "routine",
                "title": "Routine reminders",
                "description": "A reminder for planned activities",
                "enabled": True,
            },
            {
                "id": "daily",
                "title": "Daily recap",
                "description": "Review your recorded day",
                "enabled": random.choice([True, False]),
            },
            {
                "id": "articles",
                "title": "New reading",
                "description": "Updates from your saved topics",
                "enabled": False,
            },
        ],
        "navigation": [
            {"label": "Today", "icon": "home", "active": True},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": False},
        ],
    }


def apply_home_state(base_data: dict, state: str) -> dict:
    if state not in HOME_STATES:
        raise ValueError(f"Unknown home state: {state}")

    data = deepcopy(base_data)
    data["state"] = state

    data["popup_visible"] = state in {
        "child_switcher",
        "quick_log",
        "reminder_settings",
    }

    data["popup_kind"] = state if data["popup_visible"] else None

    if state == "empty_day":
        data["empty_day"] = True

        for activity in data["activities"]:
            activity["value"] = "No records"
            activity["detail"] = "Start with your first activity"

        for routine in data["routines"]:
            routine["completed"] = False

    elif state == "sleep_active":
        data["sleep_active"] = True

    return data