from __future__ import annotations

import random
from copy import deepcopy


PACKING_STATES = (
    "packing",
    "all_packed",
    "empty_list",
    "add_item",
    "trip_picker",
    "reset_dialog",
)


def generate_packing_data(
    sample_index: int,
) -> dict:
    trips = [
        {
            "id": "park",
            "title": "Afternoon at the park",
            "subtitle": "A few hours away",
            "icon": "park",
        },
        {
            "id": "family_visit",
            "title": "Family visit",
            "subtitle": "An overnight stay",
            "icon": "home",
        },
        {
            "id": "weekend",
            "title": "Weekend away",
            "subtitle": "Two nights together",
            "icon": "luggage",
        },
    ]

    selected_trip = deepcopy(
        trips[sample_index % len(trips)]
    )

    specifications = [
        ("Essentials", "Diapers", "6 items", "inventory_2"),
        ("Essentials", "Wipes", "1 pack", "inventory_2"),
        ("Essentials", "Changing mat", "1 item", "checkroom"),
        ("Clothing", "Spare outfit", "2 sets", "checkroom"),
        ("Clothing", "Light jacket", "1 item", "checkroom"),
        ("Food & drinks", "Water bottle", "1 item", "water_drop"),
        ("Food & drinks", "Snack container", "1 item", "lunch_dining"),
        ("Comfort & play", "Favorite toy", "1 item", "toys"),
        ("Comfort & play", "Picture book", "1 item", "menu_book"),
        ("Comfort & play", "Small blanket", "1 item", "bed"),
    ]

    packed_indices = set(
        random.sample(
            range(len(specifications)),
            k=random.randint(2, 5),
        )
    )

    items = [
        {
            "id": f"packing_item_{index}",
            "category": category,
            "title": title,
            "quantity": quantity,
            "icon": item_icon,
            "packed": index in packed_indices,
        }
        for index, (
            category,
            title,
            quantity,
            item_icon,
        ) in enumerate(specifications)
    ]

    return {
        "state": "packing",
        "popup_visible": False,
        "sample_index": sample_index,
        "trips": trips,
        "selected_trip": selected_trip,
        "items": items,
        "groups": [],
        "total": 0,
        "packed_count": 0,
        "remaining_count": 0,
        "progress_percent": 0,
        "categories": [
            "Essentials",
            "Clothing",
            "Food & drinks",
            "Comfort & play",
        ],
        "form": {
            "title": "",
            "quantity": "1",
            "category": "Essentials",
        },
        "navigation": [
            {"label": "Today", "icon": "today", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": True},
        ],
    }


def apply_packing_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in PACKING_STATES:
        raise ValueError(
            f"Unknown packing state: {state}"
        )

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "add_item",
        "trip_picker",
        "reset_dialog",
    }

    if state == "all_packed":
        for item in data["items"]:
            item["packed"] = True

    elif state == "empty_list":
        data["items"] = []

    groups = []

    for category in data["categories"]:
        category_items = [
            item
            for item in data["items"]
            if item["category"] == category
        ]

        if category_items:
            groups.append({
                "id": f"group_{len(groups)}",
                "title": category,
                "items": category_items,
                "packed_count": sum(
                    item["packed"]
                    for item in category_items
                ),
            })

    data["groups"] = groups
    data["total"] = len(data["items"])
    data["packed_count"] = sum(
        item["packed"]
        for item in data["items"]
    )
    data["remaining_count"] = (
        data["total"] - data["packed_count"]
    )
    data["progress_percent"] = (
        round(
            100
            * data["packed_count"]
            / data["total"]
        )
        if data["total"]
        else 0
    )

    return data