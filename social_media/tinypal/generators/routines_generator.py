from __future__ import annotations

import random
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path

from social_media.tinypal.generators.home_generator import optional_image


ROUTINE_STATES = [
    "day_plan",
    "completed_day",
    "empty_day",
    "add_routine",
    "edit_routine",
    "repeat_sheet",
    "delete_dialog",
]


def generate_routines_data(
    sample_index: int,
    avatars_dir: Path,
) -> dict:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    week_days = [
        {
            "id": index,
            "label": (week_start + timedelta(days=index)).strftime("%a"),
            "number": (week_start + timedelta(days=index)).day,
            "date": (week_start + timedelta(days=index)).isoformat(),
            "selected": index == today.weekday(),
        }
        for index in range(7)
    ]

    name = random.choice(["Mia", "Noah", "Ava", "Leo"])

    child = {
        "id": "routine_child",
        "name": name,
        "initial": name[0],
        "age": f"{random.randint(4, 18)} months",
        "avatar": optional_image(avatars_dir),
    }

    specifications = [
        ("Morning feed", "water_drop", "07:30", "Morning"),
        ("Family walk", "park", "09:00", "Morning"),
        ("Quiet play", "toys", "10:30", "Morning"),
        ("Story time", "menu_book", "14:00", "Afternoon"),
        ("Evening bath", "bathtub", "18:00", "Evening"),
        ("Bedtime routine", "bedtime", "19:30", "Evening"),
    ]

    routines = [
        {
            "id": f"routine_plan_{index}",
            "title": title,
            "icon": icon,
            "time": time,
            "period": period,
            "duration": random.choice([15, 20, 30]),
            "completed": index < 2,
            "reminder": random.choice([True, False]),
            "repeat_label": "Every day",
            "note": random.choice([
                "",
                "Keep everything ready beforehand.",
                "A little time together.",
            ]),
        }
        for index, (title, icon, time, period)
        in enumerate(specifications)
    ]

    return {
        "sample_index": sample_index,
        "state": "day_plan",
        "popup_visible": False,
        "popup_kind": None,
        "selected_child": child,
        "date_label": today.strftime("%A, %B %d"),
        "month_label": today.strftime("%B %Y"),
        "week_days": week_days,
        "routines": routines,
        "groups": [],
        "total_count": 0,
        "completed_count": 0,
        "progress": 0,
        "selected_routine": deepcopy(routines[0]),
        "form": {
            "title": "Outdoor play",
            "time": "15:00",
            "duration": "20",
            "note": "",
            "reminder": True,
            "repeat_label": "Every day",
        },
        "repeat_days": [
            {"id": index, "label": label, "selected": True}
            for index, label in enumerate([
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday",
            ])
        ],
        "navigation": [
            {"label": "Today", "icon": "home", "active": False},
            {"label": "Track", "icon": "monitoring", "active": True},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": False},
        ],
    }


def apply_routines_state(base_data: dict, state: str) -> dict:
    if state not in ROUTINE_STATES:
        raise ValueError(f"Unknown routine state: {state}")

    data = deepcopy(base_data)
    data["state"] = state

    popup_states = {
        "add_routine",
        "edit_routine",
        "repeat_sheet",
        "delete_dialog",
    }

    data["popup_visible"] = state in popup_states
    data["popup_kind"] = state if state in popup_states else None

    if state == "completed_day":
        for routine in data["routines"]:
            routine["completed"] = True

    elif state == "empty_day":
        data["routines"] = []

    elif state == "edit_routine":
        selected = data["selected_routine"]

        data["form"] = {
            "title": selected["title"],
            "time": selected["time"],
            "duration": str(selected["duration"]),
            "note": selected["note"],
            "reminder": selected["reminder"],
            "repeat_label": selected["repeat_label"],
        }

    elif state == "repeat_sheet":
        for day in data["repeat_days"]:
            day["selected"] = day["id"] < 5

    data["total_count"] = len(data["routines"])
    data["completed_count"] = sum(
        routine["completed"] for routine in data["routines"]
    )

    data["progress"] = (
        round(100 * data["completed_count"] / data["total_count"])
        if data["total_count"]
        else 0
    )

    data["groups"] = [
        {
            "label": period,
            "routines": [
                routine for routine in data["routines"]
                if routine["period"] == period
            ],
        }
        for period in ["Morning", "Afternoon", "Evening"]
        if any(
            routine["period"] == period
            for routine in data["routines"]
        )
    ]

    return data