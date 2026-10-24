from __future__ import annotations

import random
from copy import deepcopy


DRUG_REFERENCE_STATES = [
    "directory",
    "search_results",
    "reference_detail",
    "saved_only",
    "comparison",
    "empty_results",
    "filters_dialog",
    "save_dialog",
]


REFERENCE_ITEMS = [
    ("Amoxicillin", "Anti-infectives"),
    ("Azithromycin", "Anti-infectives"),
    ("Doxycycline", "Anti-infectives"),
    ("Metformin", "Endocrinology"),
    ("Insulin glargine", "Endocrinology"),
    ("Levothyroxine", "Endocrinology"),
    ("Amlodipine", "Cardiovascular"),
    ("Lisinopril", "Cardiovascular"),
    ("Losartan", "Cardiovascular"),
    ("Atorvastatin", "Cardiovascular"),
    ("Omeprazole", "Gastrointestinal"),
    ("Famotidine", "Gastrointestinal"),
    ("Ondansetron", "Gastrointestinal"),
    ("Albuterol", "Respiratory"),
    ("Budesonide", "Respiratory"),
    ("Montelukast", "Respiratory"),
    ("Cetirizine", "Allergy"),
    ("Loratadine", "Allergy"),
    ("Acetaminophen", "Pain and inflammation"),
    ("Ibuprofen", "Pain and inflammation"),
    ("Naproxen", "Pain and inflammation"),
    ("Sertraline", "Mental health"),
    ("Escitalopram", "Mental health"),
    ("Fluoxetine", "Mental health"),
]


CATEGORIES = [
    "All categories",
    "Anti-infectives",
    "Cardiovascular",
    "Endocrinology",
    "Gastrointestinal",
    "Respiratory",
    "Allergy",
    "Pain and inflammation",
    "Mental health",
]


def generate_drug_reference_data(
    *,
    sample_index: int,
) -> dict:
    entries = []

    for index, (name, category) in enumerate(
        sorted(REFERENCE_ITEMS)
    ):
        entries.append({
            "id": f"reference_{index}",
            "name": name,
            "category": category,
            "saved": index % 4 == 0,
            "updated": random.choice([
                "Sep 2026",
                "Aug 2026",
                "Jul 2026",
            ]),
            "sections": random.randint(8, 15),
            "selected": False,
        })

    reference = deepcopy(
        next(
            entry
            for entry in entries
            if entry["name"] == "Amoxicillin"
        )
    )

    reference["sections_data"] = [
        {
            "key": "overview",
            "title": "Reference overview",
            "expanded": True,
            "text": (
                "This synthetic panel demonstrates the organization "
                "of a drug reference. Use the section navigation to "
                "browse the sample content."
            ),
            "rows": [
                ("Record type", "Drug reference"),
                ("Reference category", reference["category"]),
                ("Content version", "Demonstration edition"),
            ],
        },
        {
            "key": "formulations",
            "title": "Formulation information",
            "expanded": False,
            "text": (
                "A populated reference section can contain structured "
                "tables, explanatory notes, and links to related records."
            ),
            "rows": [
                ("Table", "Formulation overview"),
                ("Related content", "Product reference records"),
            ],
        },
        {
            "key": "administration",
            "title": "Administration reference",
            "expanded": False,
            "text": (
                "Sample text for testing an expanded reference section. "
                "No administration instructions are provided."
            ),
            "rows": [
                ("Section type", "Structured reference"),
                ("Related content", "Supporting documentation"),
            ],
        },
        {
            "key": "safety",
            "title": "Safety reference",
            "expanded": False,
            "text": (
                "This sample section represents where reviewed safety "
                "information would appear in a reference application."
            ),
            "rows": [
                ("Content status", "Synthetic demonstration"),
                ("Supporting material", "Reference bibliography"),
            ],
        },
        {
            "key": "references",
            "title": "References and related content",
            "expanded": False,
            "text": (
                "Related records and bibliography entries can be "
                "displayed here."
            ),
            "rows": [
                ("Related records", "3 demonstration entries"),
                ("Bibliography", "Placeholder reference list"),
            ],
        },
    ]

    category_counts = {
        category: sum(
            entry["category"] == category
            for entry in entries
        )
        for category in CATEGORIES
        if category != "All categories"
    }

    return {
        "sample_index": sample_index,
        "state": "directory",
        "popup_visible": False,
        "query": "",
        "active_category": "All categories",
        "saved_only": False,
        "entries": entries,
        "total_count": len(entries),
        "saved_count": sum(
            entry["saved"]
            for entry in entries
        ),
        "categories": CATEGORIES,
        "category_counts": category_counts,
        "reference": reference,
        "comparison_entries": [],
        "filter_categories": ["Cardiovascular", "Endocrinology"],
        "filter_saved_only": False,
        "collections": [
            {
                "id": "clinical",
                "name": "Clinical references",
                "count": 18,
                "selected": True,
            },
            {
                "id": "reading",
                "name": "Reading list",
                "count": 12,
                "selected": False,
            },
            {
                "id": "teaching",
                "name": "Teaching resources",
                "count": 9,
                "selected": False,
            },
            {
                "id": "review",
                "name": "For later review",
                "count": 7,
                "selected": True,
            },
        ],
        "recent_names": [
            "Metformin",
            "Amoxicillin",
            "Amlodipine",
            "Omeprazole",
            "Cetirizine",
        ],
        "updates": [
            {
                "title": "Reference organization refreshed",
                "text": "Updated section navigation and related links.",
            },
            {
                "title": "New collection tools",
                "text": "Organize references into multiple collections.",
            },
            {
                "title": "Comparison workspace",
                "text": "Review reference metadata side by side.",
            },
        ],
    }


def apply_drug_reference_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in DRUG_REFERENCE_STATES:
        raise ValueError(
            f"Unknown drug reference state: {state}"
        )

    data = deepcopy(base_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "filters_dialog",
        "save_dialog",
    }

    if state == "search_results":
        data["query"] = "Anti-infectives"
        data["active_category"] = "Anti-infectives"

        data["entries"] = [
            entry
            for entry in data["entries"]
            if entry["category"] == "Anti-infectives"
        ]

    elif state == "saved_only":
        data["saved_only"] = True

        data["entries"] = [
            entry
            for entry in data["entries"]
            if entry["saved"]
        ]

    elif state == "reference_detail":
        data["reference"]["sections_data"][1]["expanded"] = True

        for entry in data["entries"]:
            entry["selected"] = (
                entry["id"] == data["reference"]["id"]
            )

    elif state == "comparison":
        names = {"Amoxicillin", "Azithromycin", "Doxycycline"}

        data["comparison_entries"] = [
            deepcopy(entry)
            for entry in data["entries"]
            if entry["name"] in names
        ]

        for entry in data["entries"]:
            entry["selected"] = entry["name"] in names

    elif state == "empty_results":
        data["query"] = "Unmatched reference"
        data["entries"] = []

    return data