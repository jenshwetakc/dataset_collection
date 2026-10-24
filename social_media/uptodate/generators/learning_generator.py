from __future__ import annotations

import random
from copy import deepcopy


LEARNING_STATES = [
    "dashboard",
    "filtered",
    "activity_detail",
    "selection_mode",
    "empty_results",
    "export_dialog",
    "claim_dialog",
    "claim_success",
]


SUBJECTS = [
    ("Evaluation of persistent cough", "Pulmonary"),
    ("Approach to abnormal liver tests", "Gastroenterology"),
    ("Review of thyroid function testing", "Endocrinology"),
    ("Assessment of joint symptoms", "Rheumatology"),
    ("Overview of headache evaluation", "Neurology"),
    ("Review of blood pressure measurement", "Cardiology"),
    ("Approach to anemia evaluation", "Hematology"),
    ("Overview of sleep assessment", "Primary care"),
    ("Review of kidney function testing", "Nephrology"),
    ("Assessment of common skin findings", "Dermatology"),
    ("Overview of preventive care visits", "Primary care"),
    ("Review of respiratory testing", "Pulmonary"),
    ("Approach to fatigue assessment", "Primary care"),
    ("Overview of medication reconciliation", "Primary care"),
    ("Review of cardiovascular risk assessment", "Cardiology"),
    ("Approach to electrolyte abnormalities", "Nephrology"),
    ("Review of gastrointestinal symptoms", "Gastroenterology"),
    ("Overview of musculoskeletal examination", "Rheumatology"),
]


def generate_learning_data(
    *,
    sample_index: int,
) -> dict:
    subjects = random.sample(
        SUBJECTS,
        k=len(SUBJECTS),
    )

    activities = []

    for index, (title, specialty) in enumerate(subjects):
        status = (
            "available"
            if index % 3 != 2
            else "claimed"
        )

        activities.append({
            "id": f"activity_{index}",
            "title": title,
            "specialty": specialty,
            "date": f"Sep {28 - index}, 2026",
            "duration": random.choice([6, 8, 10, 12, 15]),
            "credits": random.choice([0.25, 0.5, 0.75]),
            "status": status,
            "selected": False,
            "expanded": False,
            "notes": [
                "Reviewed the topic overview.",
                "Compared related reference sections.",
                "Recorded a question for further reading.",
            ],
        })

    claimed = sum(
        activity["credits"]
        for activity in activities
        if activity["status"] == "claimed"
    )

    available = sum(
        activity["credits"]
        for activity in activities
        if activity["status"] == "available"
    )

    return {
        "sample_index": sample_index,
        "state": "dashboard",
        "popup_visible": False,
        "query": "",
        "active_tab": "all",
        "active_specialty": "All specialties",
        "period": "Last 30 days",
        "activities": activities,
        "total_activity_count": len(activities),
        "claimed_credits": claimed,
        "available_credits": available,
        "learning_minutes": sum(
            item["duration"]
            for item in activities
        ),
        "goal": 12,
        "goal_progress": min(
            100,
            round(claimed / 12 * 100),
        ),
        "selected_count": 0,
        "selected_credits": 0,
        "claim_confirmed": True,
        "claimed_now": 0,
        "export_format": "pdf",
        "export_include": {
            "summary": True,
            "activities": True,
            "notes": False,
        },
        "specialties": [
            "All specialties",
            "Primary care",
            "Cardiology",
            "Pulmonary",
            "Nephrology",
        ],
        "recommendations": [
            {
                "title": "Continue your recent reading",
                "description": "Revisit topics from your activity history.",
                "icon": "history",
            },
            {
                "title": "Explore another specialty",
                "description": "Browse a different collection of topics.",
                "icon": "explore",
            },
            {
                "title": "Review saved resources",
                "description": "Return to items in your collections.",
                "icon": "bookmark",
            },
        ],
        "monthly_history": [
            {"month": "September", "credits": claimed},
            {"month": "August", "credits": 4.5},
            {"month": "July", "credits": 3.75},
            {"month": "June", "credits": 5.0},
        ],
    }


def apply_learning_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in LEARNING_STATES:
        raise ValueError(
            f"Unknown learning state: {state}"
        )

    data = deepcopy(base_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "export_dialog",
        "claim_dialog",
    }

    if state == "filtered":
        data["active_tab"] = "available"
        data["active_specialty"] = "Primary care"

        data["activities"] = [
            item
            for item in data["activities"]
            if (
                item["status"] == "available"
                and item["specialty"] == "Primary care"
            )
        ]

    elif state == "activity_detail":
        data["activities"][0]["expanded"] = True

    elif state in {
        "selection_mode",
        "claim_dialog",
        "claim_success",
    }:
        selected = [
            item
            for item in data["activities"]
            if item["status"] == "available"
        ][:4]

        for item in selected:
            item["selected"] = True

        data["selected_count"] = len(selected)

        data["selected_credits"] = sum(
            item["credits"]
            for item in selected
        )

        if state == "claim_success":
            for item in selected:
                item["status"] = "claimed"
                item["selected"] = False

            data["claimed_now"] = data["selected_credits"]

            data["claimed_credits"] += (
                data["selected_credits"]
            )

            data["available_credits"] -= (
                data["selected_credits"]
            )

            data["selected_count"] = 0
            data["selected_credits"] = 0

            data["goal_progress"] = min(
                100,
                round(
                    data["claimed_credits"]
                    / data["goal"]
                    * 100
                ),
            )

    elif state == "empty_results":
        data["query"] = "Unmatched learning activity"
        data["active_specialty"] = "Cardiology"
        data["activities"] = []

    return data