from __future__ import annotations

import random
from copy import deepcopy


CALCULATOR_STATES = [
    "directory",
    "search_results",
    "empty_search",
    "calculator_form",
    "filled_form",
    "validation_error",
    "result",
    "units_dialog",
    "reset_dialog",
]

CALCULATORS = [
    ("bmi", "Body mass index", "General", "monitor_weight"),
    ("bsa", "Body surface area", "General", "straighten"),
    ("conversion", "Unit conversion", "General", "swap_horiz"),
    ("renal", "Renal function tools", "Renal", "calculate"),
    ("electrolytes", "Electrolyte tools", "Laboratory", "science"),
    ("cardiology", "Cardiology tools", "Cardiology", "favorite"),
    ("respiratory", "Respiratory tools", "Respiratory", "air"),
    ("nutrition", "Nutrition tools", "General", "restaurant"),
    ("pediatrics", "Pediatric tools", "Pediatrics", "child_care"),
]


def generate_calculators_data(sample_index: int) -> dict:
    entries = [
        {
            "id": key,
            "title": title,
            "category": category,
            "icon": glyph,
            "saved": random.random() < 0.3,
        }
        for key, title, category, glyph in CALCULATORS
    ]

    return {
        "sample_index": sample_index,
        "state": "directory",
        "popup_visible": False,
        "popup_kind": None,
        "view": "directory",
        "query": "",
        "all_calculators": entries,
        "calculators": deepcopy(entries),
        "categories": [
            "All", "General", "Renal", "Laboratory",
            "Cardiology", "Respiratory", "Pediatrics",
        ],
        "active_category": "All",
        "units": "metric",
        "unit_options": [
            {
                "id": "metric",
                "label": "Metric",
                "description": "Height in cm, weight in kg",
            },
            {
                "id": "imperial",
                "label": "Imperial",
                "description": "Height in inches, weight in lb",
            },
        ],
        "height": "",
        "weight": "",
        "errors": {},
        "bmi": None,
        "saved": random.random() < 0.4,
        "formula_expanded": False,
    }


def apply_calculators_state(base_data: dict, state: str) -> dict:
    if state not in CALCULATOR_STATES:
        raise ValueError(f"Unknown calculator state: {state!r}")

    data = deepcopy(base_data)
    data.update({
        "state": state,
        "popup_visible": False,
        "popup_kind": None,
        "view": "directory",
        "query": "",
        "height": "",
        "weight": "",
        "errors": {},
        "bmi": None,
        "calculators": deepcopy(data["all_calculators"]),
    })

    if state == "search_results":
        data["query"] = "Body"
        data["calculators"] = [
            entry for entry in data["calculators"]
            if data["query"].casefold() in entry["title"].casefold()
        ]

    elif state == "empty_search":
        data["query"] = "unmatched calculator"
        data["calculators"] = []

    elif state not in {"directory", "search_results", "empty_search"}:
        data["view"] = "form"
        data["units"] = random.choice(["metric", "imperial"])

        if state != "calculator_form":
            if data["units"] == "metric":
                height = random.randint(150, 195)
                weight = random.randint(50, 100)
                height_m = height / 100
                weight_kg = weight
            else:
                height = random.randint(60, 76)
                weight = random.randint(110, 220)
                height_m = height * 0.0254
                weight_kg = weight * 0.45359237

            data["height"] = str(height)
            data["weight"] = str(weight)

            if state == "result":
                data["bmi"] = round(weight_kg / height_m ** 2, 1)
                data["formula_expanded"] = True

        if state == "validation_error":
            data["height"] = "0"
            data["errors"] = {
                "height": "Enter a height greater than zero.",
            }

        elif state in {"units_dialog", "reset_dialog"}:
            data["popup_visible"] = True
            data["popup_kind"] = (
                "units" if state == "units_dialog" else "reset"
            )

    return data