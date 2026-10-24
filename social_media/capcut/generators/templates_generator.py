from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


TEMPLATE_STATES = [
    "discover",
    "search_results",
    "category_selected",
    "saved_templates",
    "empty_saved",
    "template_preview",
]

CATEGORIES = [
    "For you",
    "Travel",
    "Lifestyle",
    "Fashion",
    "Food",
    "Celebration",
]

TITLES = [
    "Weekend memories",
    "Golden hour",
    "My daily story",
    "City adventure",
    "Simple moments",
    "Photo collection",
    "Summer highlights",
    "Before and after",
    "Mini vlog",
    "Favorite places",
    "A beautiful day",
    "Creative transition",
]

CREATORS = [
    "Frame Studio",
    "Daily Edits",
    "Motion Lab",
    "Creative Alex",
    "Visual Stories",
    "Dream Frames",
]


def resolve_directory(
    preferred: Path,
) -> Path | None:
    for directory in (preferred, ASSETS_ROOT):
        if get_image_files(str(directory)):
            return directory

    return None


def generate_templates_data(
    sample_index: int,
    thumbnails_dir: Path | None = None,
    avatars_dir: Path | None = None,
) -> dict:
    thumbnails = resolve_directory(
        thumbnails_dir or ASSETS_ROOT / "capcut" / "templates"
    )

    avatars = resolve_directory(
        avatars_dir or ASSETS_ROOT / "capcut" / "avatars"
    )

    templates = []

    for index in range(random.randint(18, 30)):
        seconds = random.randint(8, 45)

        templates.append({
            "id": f"template_{sample_index}_{index}",
            "title": random.choice(TITLES),
            "category": CATEGORIES[1 + index % (len(CATEGORIES) - 1)],
            "creator": random.choice(CREATORS),
            "thumbnail": (
                get_random_image(thumbnails)
                if thumbnails is not None
                else None
            ),
            "avatar": (
                get_random_image(avatars)
                if avatars is not None
                else None
            ),
            "duration": f"00:{seconds:02d}",
            "clips": random.randint(3, 14),
            "uses": f"{random.uniform(1, 950):.1f}K",
            "likes": f"{random.uniform(1, 80):.1f}K",
            "saved": random.random() < 0.35,
            "premium": random.random() < 0.2,
            "aspect_ratio": random.choice(["9:16", "1:1", "16:9"]),
            "description": (
                "Bring your favorite moments together with "
                "smooth transitions and a ready-made rhythm."
            ),
        })

    return {
        "sample_index": sample_index,
        "state": "discover",
        "popup_visible": False,
        "query": "",
        "active_category": "For you",
        "active_collection": "discover",
        "categories": list(CATEGORIES),
        "templates": templates,
        "target_template": dict(templates[0]),
        "sort": "Popular",
        "show_featured": True,
    }


def apply_templates_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in TEMPLATE_STATES:
        raise ValueError(f"Unknown templates state: {state}")

    data = dict(base_data)
    data["templates"] = [
        dict(item)
        for item in base_data["templates"]
    ]
    data["target_template"] = dict(base_data["target_template"])
    data["state"] = state
    data["popup_visible"] = state == "template_preview"
    data["query"] = ""
    data["active_category"] = "For you"
    data["active_collection"] = "discover"
    data["show_featured"] = state == "discover"

    if state == "search_results":
        data["query"] = data["templates"][0]["title"].split()[0]
        data["templates"] = [
            item
            for item in data["templates"]
            if data["query"].casefold() in item["title"].casefold()
        ]

    elif state == "category_selected":
        data["active_category"] = random.choice(CATEGORIES[1:])
        data["templates"] = [
            item
            for item in data["templates"]
            if item["category"] == data["active_category"]
        ]

    elif state == "saved_templates":
        data["active_collection"] = "saved"

        # Ensure this state contains at least one saved template.
        data["templates"][0]["saved"] = True
        data["templates"] = [
            item
            for item in data["templates"]
            if item["saved"]
        ]

    elif state == "empty_saved":
        data["active_collection"] = "saved"
        data["templates"] = []

    return data