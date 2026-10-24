from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


SEARCH_STATES = [
    "all_results",
    "topics_only",
    "graphics_only",
    "patient_education",
    "no_results",
    "filters_dialog",
    "save_dialog",
]

CATEGORIES = [
    {"key": "all", "label": "All"},
    {"key": "topic", "label": "Topics"},
    {"key": "graphic", "label": "Graphics"},
    {"key": "education", "label": "Patient education"},
]

SPECIALTIES = [
    "All specialties",
    "Internal medicine",
    "Family medicine",
    "Emergency medicine",
    "Pediatrics",
]

SEARCH_SUBJECTS = [
    "Headache",
    "Asthma",
    "Diabetes",
    "Hypertension",
    "Dizziness",
]

TYPE_LABELS = {
    "topic": "Clinical topic",
    "graphic": "Graphic",
    "education": "Patient education",
}

TYPE_ICONS = {
    "topic": "article",
    "graphic": "image",
    "education": "school",
}


def generate_search_data(
    sample_index: int,
    graphics_dir: Path | None = None,
) -> dict:
    subject = random.choice(SEARCH_SUBJECTS)

    image_available = (
        graphics_dir is not None
        and graphics_dir.is_dir()
        and bool(get_image_files(str(graphics_dir)))
    )

    results = []

    for index in range(random.randint(12, 18)):
        resource_type = ["topic", "graphic", "education"][index % 3]

        if resource_type == "topic":
            title = random.choice([
                f"{subject}: overview",
                f"Approach to {subject.lower()}",
                f"{subject}: evaluation",
                f"{subject}: reference topic",
            ])
        elif resource_type == "graphic":
            title = random.choice([
                f"{subject}: reference illustration",
                f"{subject}: topic summary graphic",
                f"{subject}: overview figure",
            ])
        else:
            title = random.choice([
                f"Understanding {subject.lower()}",
                f"{subject}: patient information",
                f"Learning about {subject.lower()}",
            ])

        results.append({
            "id": f"result_{index}",
            "title": title,
            "type": resource_type,
            "type_label": TYPE_LABELS[resource_type],
            "icon": TYPE_ICONS[resource_type],
            "specialty": random.choice(SPECIALTIES[1:]),
            "summary": (
                f"Browse this synthetic {subject.lower()} resource, "
                "including its overview, related sections, "
                "and reference information."
            ),
            "updated": random.choice([
                "Recently reviewed",
                "Updated this month",
                "Updated this week",
            ]),
            "saved": random.random() < 0.25,
            "image": (
                get_random_image(graphics_dir)
                if resource_type == "graphic" and image_available
                else None
            ),
        })

    counts = {
        "all": len(results),
        **{
            category: sum(
                result["type"] == category
                for result in results
            )
            for category in TYPE_LABELS
        },
    }

    return {
        "sample_index": sample_index,
        "state": "all_results",
        "query": subject.lower(),
        "active_category": "all",
        "categories": deepcopy(CATEGORIES),
        "counts": counts,
        "all_results": results,
        "results": deepcopy(results),
        "result_count": len(results),
        "popup_visible": False,
        "popup_kind": None,
        "selected_result": deepcopy(results[0]),
        "specialties": list(SPECIALTIES),
        "selected_specialty": "All specialties",
        "sort_label": "Relevance",
        "include_archived": False,
        "collections": [
            {"id": "favorites", "name": "Favorites", "selected": True},
            {"id": "reading", "name": "Reading list", "selected": False},
            {"id": "teaching", "name": "Teaching resources", "selected": False},
        ],
        "related_queries": [
            f"{subject.lower()} overview",
            f"{subject.lower()} patient information",
            f"{subject.lower()} graphics",
        ],
    }


def apply_search_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in SEARCH_STATES:
        raise ValueError(f"Unknown search state: {state!r}")

    data = deepcopy(base_data)

    data.update({
        "state": state,
        "active_category": "all",
        "popup_visible": False,
        "popup_kind": None,
        "results": deepcopy(data["all_results"]),
    })

    category = {
        "topics_only": "topic",
        "graphics_only": "graphic",
        "patient_education": "education",
    }.get(state)

    if category:
        data["active_category"] = category
        data["results"] = [
            result
            for result in data["results"]
            if result["type"] == category
        ]

    elif state == "no_results":
        data["query"] = "unmatched reference keyword"
        data["results"] = []
        data["counts"] = {
            "all": 0,
            "topic": 0,
            "graphic": 0,
            "education": 0,
        }

    elif state == "filters_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "filters"

    elif state == "save_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "save"

    data["result_count"] = len(data["results"])

    return data