from __future__ import annotations

import random
from copy import deepcopy


SAVED_STATES = [
    "all_saved",
    "collection_view",
    "search_results",
    "empty_collection",
    "selection_mode",
    "create_collection_dialog",
    "move_resources_dialog",
    "delete_collection_dialog",
]

RESOURCE_TYPES = {
    "topic": ("Clinical topic", "article"),
    "graphic": ("Graphic", "image"),
    "education": ("Patient education", "school"),
    "calculator": ("Calculator", "calculate"),
}

SUBJECTS = [
    "Headache",
    "Asthma",
    "Diabetes",
    "Hypertension",
    "Dizziness",
    "Preventive care",
]


def generate_saved_data(
    sample_index: int,
) -> dict:
    collections = [
        {"id": "favorites", "name": "Favorites"},
        {"id": "reading", "name": "Reading list"},
        {"id": "teaching", "name": "Teaching resources"},
        {"id": "review", "name": "Weekly review"},
        {"id": "empty", "name": "New collection"},
    ]

    resources = []

    for index in range(random.randint(14, 20)):
        resource_type = list(RESOURCE_TYPES)[index % 4]
        type_label, glyph = RESOURCE_TYPES[resource_type]
        subject = SUBJECTS[index % len(SUBJECTS)]

        # Cycling guarantees each populated collection has resources.
        collection_id = collections[index % 4]["id"]

        resources.append({
            "id": f"saved_{index}",
            "title": f"{subject}: {type_label.lower()}",
            "type": resource_type,
            "type_label": type_label,
            "icon": glyph,
            "collection_id": collection_id,
            "collection_name": next(
                collection["name"]
                for collection in collections
                if collection["id"] == collection_id
            ),
            "saved_label": random.choice([
                "Saved today",
                "Saved yesterday",
                "Saved this week",
            ]),
            "description": (
                "A saved reference resource in your personal workspace."
            ),
            "selected": False,
        })

    for collection in collections:
        collection["count"] = sum(
            resource["collection_id"] == collection["id"]
            for resource in resources
        )

    return {
        "sample_index": sample_index,
        "state": "all_saved",
        "popup_visible": False,
        "popup_kind": None,
        "collections": collections,
        "all_resources": resources,
        "resources": deepcopy(resources),
        "active_collection": "all",
        "page_title": "Saved resources",
        "query": "",
        "search_visible": False,
        "selection_mode": False,
        "selected_count": 0,
        "resource_count": len(resources),
        "total_count": len(resources),
        "sort_label": "Recently saved",
        "new_collection_name": "Clinical notes",
        "destination_collection": "teaching",
        "delete_collection": deepcopy(collections[1]),
        "layout_variant": random.choice(["list", "cards"]),
    }


def apply_saved_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in SAVED_STATES:
        raise ValueError(f"Unknown saved state: {state!r}")

    data = deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": False,
        "popup_kind": None,
        "active_collection": "all",
        "page_title": "Saved resources",
        "query": "",
        "search_visible": False,
        "selection_mode": False,
        "selected_count": 0,
        "resources": deepcopy(data["all_resources"]),
    })

    if state == "collection_view":
        collection = random.choice(data["collections"][:4])

        data["active_collection"] = collection["id"]
        data["page_title"] = collection["name"]
        data["resources"] = [
            resource
            for resource in data["resources"]
            if resource["collection_id"] == collection["id"]
        ]

    elif state == "search_results":
        data["query"] = "Headache"
        data["search_visible"] = True
        data["resources"] = [
            resource
            for resource in data["resources"]
            if data["query"].casefold()
            in resource["title"].casefold()
        ]

    elif state == "empty_collection":
        data["active_collection"] = "empty"
        data["page_title"] = "New collection"
        data["resources"] = []

    elif state in {"selection_mode", "move_resources_dialog"}:
        data["selection_mode"] = True

        for resource in data["resources"][:3]:
            resource["selected"] = True

        if state == "move_resources_dialog":
            data["popup_visible"] = True
            data["popup_kind"] = "move"

    elif state == "create_collection_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "create"

    elif state == "delete_collection_dialog":
        collection = data["delete_collection"]

        data["active_collection"] = collection["id"]
        data["page_title"] = collection["name"]
        data["resources"] = [
            resource
            for resource in data["resources"]
            if resource["collection_id"] == collection["id"]
        ]

        data["popup_visible"] = True
        data["popup_kind"] = "delete"

    data["selected_count"] = sum(
        resource["selected"]
        for resource in data["resources"]
    )
    data["resource_count"] = len(data["resources"])

    return data