from __future__ import annotations

import random

from faker import Faker


CONDITIONAL_FORMATTING_STATES = [
    "rules_list",
    "single_color_editor",
    "color_scale_editor",
    "custom_formula",
    "invalid_formula",
    "range_dialog",
    "rule_menu",
    "delete_dialog",
    "empty_state",
    "loading",
]

POPUP_STATES = {
    "range_dialog",
    "rule_menu",
    "delete_dialog",
}


def generate_conditional_formatting_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(CONDITIONAL_FORMATTING_STATES)
    if state not in CONDITIONAL_FORMATTING_STATES:
        raise ValueError(
            f"Unknown conditional-formatting state: {state}. "
            f"Expected one of {CONDITIONAL_FORMATTING_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    departments = ["Engineering", "Design", "Marketing", "Sales", "Support"]
    statuses = ["On track", "At risk", "Blocked", "Complete"]
    rows = []
    total_budget = 0

    for index in range(18):
        budget = random.randint(4500, 48000)
        completion = random.randint(18, 100)
        total_budget += budget
        rows.append(
            {
                "row_number": index + 2,
                "project": fake.catch_phrase(),
                "owner": fake.name(),
                "department": random.choice(departments),
                "budget_text": f"${budget:,}",
                "completion_text": f"{completion}%",
                "completion": completion,
                "status": random.choice(statuses),
            }
        )

    rules = [
        {
            "rule_id": "high_completion",
            "range": "E2:E250",
            "description": "Greater than or equal to 80%",
            "preview_text": "80%",
            "preview_background": "#b7e1cd",
            "preview_color": "#0d652d",
        },
        {
            "rule_id": "blocked_status",
            "range": "F2:F250",
            "description": "Text is exactly “Blocked”",
            "preview_text": "Blocked",
            "preview_background": "#f4c7c3",
            "preview_color": "#8c1d18",
        },
        {
            "rule_id": "large_budget",
            "range": "D2:D250",
            "description": "Greater than $25,000",
            "preview_text": "$25,000",
            "preview_background": "#fce8b2",
            "preview_color": "#7a4f01",
        },
    ]

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": width < 600,
        "document_title": random.choice(
            ["Project Portfolio", "Quarterly Planning", "Team Operations"]
        ),
        "account_initial": fake.first_name()[0].upper(),
        "sheet_name": "Projects",
        "headers": ["Project", "Owner", "Department", "Budget", "Completion", "Status"],
        "rows": rows,
        "total_budget_text": f"${total_budget:,}",
        "rules": [] if state == "empty_state" else rules,
        "selected_rule": rules[0],
        "apply_range": "E2:E250",
        "format_condition": "Greater than or equal to",
        "condition_value": "80%",
        "custom_formula": "=$E2>=80%",
        "invalid_formula": "=$E2=>80%",
        "range_suggestions": ["Projects!E2:E250", "Projects!D2:D250", "Projects!F2:F250"],
        "color_scale_points": [
            {"label": "Minpoint", "type": "Min value", "value": "", "color": "#f8696b"},
            {"label": "Midpoint", "type": "Percentile", "value": "50", "color": "#ffeb84"},
            {"label": "Maxpoint", "type": "Max value", "value": "", "color": "#63be7b"},
        ],
    }
