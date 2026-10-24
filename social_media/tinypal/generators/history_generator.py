from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from social_media.tinypal.generators.home_generator import (
    optional_image,
)


HISTORY_STATES = [
    "all_records",
    "feeding_only",
    "sleep_only",
    "empty_results",
    "filter_sheet",
    "record_details",
    "edit_record",
    "delete_dialog",
]


def generate_history_data(
    sample_index: int,
    avatars_dir: Path,
) -> dict:
    name = random.choice(["Mia", "Noah", "Ava", "Leo", "Ella"])

    child = {
        "id": "history_child",
        "name": name,
        "initial": name[0],
        "age": f"{random.randint(4, 18)} months",
        "avatar": optional_image(avatars_dir),
    }

    kinds = {
        "feeding": {
            "label": "Feeding",
            "icon": "water_drop",
        },
        "sleep": {
            "label": "Sleep",
            "icon": "bedtime",
        },
        "diaper": {
            "label": "Diaper change",
            "icon": "baby_changing_station",
        },
    }

    # Descending timestamps keep the timeline internally ordered.
    times = [
        ("Today", "2026-10-06", "16:20"),
        ("Today", "2026-10-06", "14:45"),
        ("Today", "2026-10-06", "13:10"),
        ("Today", "2026-10-06", "11:30"),
        ("Today", "2026-10-06", "09:15"),
        ("Today", "2026-10-06", "07:40"),
        ("Yesterday", "2026-10-05", "20:10"),
        ("Yesterday", "2026-10-05", "18:30"),
        ("Yesterday", "2026-10-05", "16:00"),
        ("Yesterday", "2026-10-05", "14:20"),
        ("Yesterday", "2026-10-05", "11:45"),
        ("Yesterday", "2026-10-05", "08:10"),
    ]

    records = []

    for index, (day, date, time) in enumerate(times):
        kind = ["feeding", "sleep", "diaper"][index % 3]
        minutes = random.choice([35, 45, 60, 75])
        amount = random.choice([90, 120, 150, 180])

        value = (
            f"{amount} ml"
            if kind == "feeding"
            else f"{minutes} min"
            if kind == "sleep"
            else random.choice(["Wet", "Dirty", "Mixed"])
        )

        records.append({
            "id": f"record_{index}",
            "kind": kind,
            "title": kinds[kind]["label"],
            "icon": kinds[kind]["icon"],
            "day": day,
            "date": date,
            "time": time,
            "value": value,
            "amount": str(amount),
            "minutes": str(minutes),
            "diaper_type": value if kind == "diaper" else "Wet",
            "caregiver": random.choice(["You", "Sam", "Alex"]),
            "note": random.choice([
                "",
                "Recorded after our afternoon routine.",
                "A calm moment at home.",
            ]),
        })

    return {
        "sample_index": sample_index,
        "state": "all_records",
        "popup_visible": False,
        "popup_kind": None,
        "selected_child": child,
        "selected_category": "all",
        "date_range": "Last 2 days",
        "query": "",
        "records": records,
        "visible_records": records,
        "groups": [],
        # Choose a feeding record so edit fields match its type.
        "selected_record": deepcopy(records[0]),
        "categories": [
            {"id": "all", "label": "All", "icon": "apps"},
            {"id": "feeding", "label": "Feeding", "icon": "water_drop"},
            {"id": "sleep", "label": "Sleep", "icon": "bedtime"},
            {
                "id": "diaper",
                "label": "Diapers",
                "icon": "baby_changing_station",
            },
        ],
        "filter_categories": ["feeding", "sleep", "diaper"],
        "caregiver_filter": "Everyone",
        "navigation": [
            {"label": "Today", "icon": "home", "active": False},
            {"label": "Track", "icon": "monitoring", "active": True},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": False},
        ],
    }


def apply_history_state(base_data: dict, state: str) -> dict:
    if state not in HISTORY_STATES:
        raise ValueError(f"Unknown history state: {state}")

    data = deepcopy(base_data)
    data["state"] = state

    popup_states = {
        "filter_sheet",
        "record_details",
        "edit_record",
        "delete_dialog",
    }

    data["popup_visible"] = state in popup_states
    data["popup_kind"] = state if state in popup_states else None

    if state == "feeding_only":
        data["selected_category"] = "feeding"
    elif state == "sleep_only":
        data["selected_category"] = "sleep"
    elif state == "empty_results":
        data["query"] = "Outdoor play"

    category = data["selected_category"]

    visible = [
        record
        for record in data["records"]
        if category == "all" or record["kind"] == category
    ]

    if state == "empty_results":
        visible = []

    data["visible_records"] = visible
    data["result_count"] = len(visible)

    groups = []

    for day in ["Today", "Yesterday"]:
        day_records = [
            record for record in visible if record["day"] == day
        ]

        if day_records:
            groups.append({
                "label": day,
                "records": day_records,
            })

    data["groups"] = groups

    # Summary values describe the displayed records.
    data["summary"] = [
        {
            "title": "Feeding",
            "icon": "water_drop",
            "value": str(sum(r["kind"] == "feeding" for r in visible)),
            "unit": "records",
        },
        {
            "title": "Sleep",
            "icon": "bedtime",
            "value": str(sum(
                int(r["minutes"])
                for r in visible
                if r["kind"] == "sleep"
            )),
            "unit": "minutes",
        },
        {
            "title": "Diapers",
            "icon": "baby_changing_station",
            "value": str(sum(r["kind"] == "diaper" for r in visible)),
            "unit": "changes",
        },
    ]

    return data