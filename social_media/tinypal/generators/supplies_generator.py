from __future__ import annotations

from copy import deepcopy
import random


SUPPLIES_STATES = (
    "inventory",
    "low_stock",
    "shopping_list",
    "empty_inventory",
    "add_supply",
    "supply_details",
    "restock_dialog",
)


def generate_supplies_data(sample_index: int) -> dict:
    specifications = [
        ("Diapers", "Care", "inventory_2", "packs", 2),
        ("Wipes", "Care", "cleaning_services", "packs", 2),
        ("Changing mats", "Care", "layers", "items", 1),
        ("Storage bags", "Home", "shopping_bag", "boxes", 1),
        ("Laundry detergent", "Home", "local_laundry_service", "bottles", 1),
        ("Washcloths", "Care", "dry_cleaning", "items", 3),
        ("Spare outfits", "Clothing", "checkroom", "sets", 2),
        ("Socks", "Clothing", "checkroom", "pairs", 3),
        ("Light jackets", "Clothing", "checkroom", "items", 1),
        ("Drawing paper", "Play", "description", "packs", 1),
        ("Crayons", "Play", "draw", "boxes", 1),
        ("Craft supplies", "Play", "interests", "boxes", 1),
        ("Snack containers", "Outings", "lunch_dining", "items", 2),
        ("Water bottles", "Outings", "water_drop", "items", 1),
        ("Travel pouches", "Outings", "luggage", "items", 2),
    ]

    entries = []

    for index, (name, category, symbol, unit, minimum) in enumerate(
        specifications
    ):
        quantity = (
            random.randint(0, minimum)
            if index in {0, 1, 3, 9}
            else random.randint(minimum + 1, minimum + 5)
        )

        entries.append({
            "id": f"supply_{index}",
            "name": name,
            "category": category,
            "icon": symbol,
            "unit": unit,
            "quantity": quantity,
            "minimum": minimum,
            "location": ["Hall cupboard", "Bedroom shelf", "Storage basket"][
                index % 3
            ],
            "note": "Keep the spare items together for easy access.",
            "updated": ["Today", "Yesterday", "This week"][index % 3],
            "low": quantity <= minimum,
        })

    return {
        "sample_index": sample_index,
        "state": "inventory",
        "popup_visible": False,
        "active_view": "inventory",
        "entries": entries,
        "visible_entries": [],
        "shopping": [],
        "selected_supply": deepcopy(entries[0]),
        "total": 0,
        "low_count": 0,
        "shopping_count": 0,
        "categories": ["Care", "Home", "Clothing", "Play", "Outings"],
        "form": {
            "name": "",
            "quantity": "1",
            "minimum": "1",
            "category": "Care",
            "location": "",
        },
        "restock_quantity": 3,
        "navigation": [
            {"label": "Today", "icon": "today", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": True},
        ],
    }


def apply_supplies_state(base_data: dict, state: str) -> dict:
    if state not in SUPPLIES_STATES:
        raise ValueError(f"Unknown supplies state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "add_supply", "supply_details", "restock_dialog",
    }

    if state == "empty_inventory":
        data["entries"] = []

    if state == "low_stock":
        data["active_view"] = "low"
    elif state == "shopping_list":
        data["active_view"] = "shopping"

    entries = data["entries"]
    low_entries = [entry for entry in entries if entry["low"]]

    data["total"] = len(entries)
    data["low_count"] = len(low_entries)
    data["visible_entries"] = (
        low_entries if data["active_view"] == "low" else entries
    )

    data["shopping"] = [
        {
            "id": f"shopping_{entry['id']}",
            "name": entry["name"],
            "icon": entry["icon"],
            "amount": max(1, entry["minimum"] + 2 - entry["quantity"]),
            "unit": entry["unit"],
            "checked": index == 0,
        }
        for index, entry in enumerate(low_entries)
    ]

    data["shopping_count"] = len(data["shopping"])
    return data