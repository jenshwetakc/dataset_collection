from __future__ import annotations

import random

from copy import deepcopy
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


HOME_STATES = [
    "default",
    "search_suggestions",
    "recent_searches",
    "empty_history",
    "specialty_dialog",
    "clear_history_dialog",
]

SPECIALTIES = [
    "All specialties",
    "Internal medicine",
    "Family medicine",
    "Emergency medicine",
    "Pediatrics",
    "Cardiology",
    "Neurology",
    "Gastroenterology",
    "Endocrinology",
    "Pulmonology",
    "Infectious diseases",
    "Nephrology",
]

TOPICS = [
    ("Evaluation of headache in adults", "Neurology"),
    ("Overview of hypertension", "Cardiology"),
    ("Approach to abdominal pain", "Gastroenterology"),
    ("Evaluation of dizziness", "Internal medicine"),
    ("Overview of asthma", "Pulmonology"),
    ("Approach to fever in adults", "Infectious diseases"),
    ("Overview of type 2 diabetes", "Endocrinology"),
    ("Evaluation of fatigue", "Family medicine"),
    ("Approach to acute kidney injury", "Nephrology"),
    ("Evaluation of chest discomfort", "Emergency medicine"),
    ("Overview of preventive care", "Family medicine"),
    ("Approach to cough in children", "Pediatrics"),
]

SEARCH_GROUPS = [
    {
        "query": "head",
        "suggestions": [
            "Headache in adults",
            "Headache in children",
            "Head injury",
            "Headache evaluation",
        ],
    },
    {
        "query": "diab",
        "suggestions": [
            "Diabetes mellitus",
            "Diabetes screening",
            "Diabetic neuropathy",
            "Diabetes patient education",
        ],
    },
    {
        "query": "asth",
        "suggestions": [
            "Asthma in adults",
            "Asthma in children",
            "Asthma evaluation",
            "Asthma patient education",
        ],
    },
]

QUICK_TOOLS = [
    {
        "id": "calculators",
        "label": "Calculators",
        "description": "Browse clinical calculation tools",
        "icon": "calculate",
    },
    {
        "id": "drug_information",
        "label": "Drug information",
        "description": "Browse reference topics",
        "icon": "medication",
    },
    {
        "id": "patient_education",
        "label": "Patient education",
        "description": "Explore patient resources",
        "icon": "school",
    },
    {
        "id": "whats_new",
        "label": "What's new",
        "description": "Explore recently updated topics",
        "icon": "new_releases",
    },
]


def optional_image(
    directory: Path | None,
) -> str | None:
    # Avoid repeatedly warning when optional assets are absent.
    if directory is None or not directory.is_dir():
        return None

    if not get_image_files(str(directory)):
        return None

    return get_random_image(directory)


def generate_home_data(
    sample_index: int,
    avatars_dir: Path | None = None,
) -> dict:
    first_name = random.choice([
        "Alex", "Jordan", "Morgan", "Taylor", "Sam", "Casey",
    ])
    last_name = random.choice([
        "Lee", "Kim", "Patel", "Chen", "Park", "Singh",
    ])

    selected_topics = random.sample(
        TOPICS,
        k=random.randint(7, 10),
    )

    topic_records = [
        {
            "id": f"topic_{index}",
            "title": title,
            "specialty": specialty,
            "updated": random.choice([
                "Updated this week",
                "Updated this month",
                "Recently reviewed",
            ]),
            "saved": random.random() < 0.35,
        }
        for index, (title, specialty) in enumerate(selected_topics)
    ]

    recent = [
        {
            "id": f"recent_{index}",
            "title": title,
            "when": random.choice([
                "Today", "Yesterday", "Earlier this week",
            ]),
        }
        for index, (title, _) in enumerate(
            random.sample(TOPICS, k=random.randint(3, 6))
        )
    ]

    return {
        "sample_index": sample_index,
        "state": "default",
        "popup_visible": False,
        "popup_kind": None,
        "query": "",
        "suggestions": [],
        "show_history": False,
        "user": {
            "name": f"Dr. {first_name} {last_name}",
            "initials": first_name[0] + last_name[0],
            "avatar": optional_image(avatars_dir),
        },
        "specialty": random.choice(SPECIALTIES[:6]),
        "specialties": list(SPECIALTIES),
        "recent_searches": recent,
        "topics": topic_records,
        "quick_tools": deepcopy(QUICK_TOOLS),
        "saved_count": random.randint(3, 24),
        "layout_variant": random.choice([
            "standard", "compact", "comfortable",
        ]),
    }


def apply_home_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in HOME_STATES:
        raise ValueError(
            f"Unknown home state: {state!r}. "
            f"Available states: {HOME_STATES}"
        )

    data = deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": False,
        "popup_kind": None,
        "query": "",
        "suggestions": [],
        "show_history": False,
    })

    if state == "search_suggestions":
        group = random.choice(SEARCH_GROUPS)
        data["query"] = group["query"]
        data["suggestions"] = list(group["suggestions"])

    elif state == "recent_searches":
        data["show_history"] = True

    elif state == "empty_history":
        data["show_history"] = True
        data["recent_searches"] = []

    elif state == "specialty_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "specialty"

    elif state == "clear_history_dialog":
        data["show_history"] = True
        data["popup_visible"] = True
        data["popup_kind"] = "clear_history"

    return data