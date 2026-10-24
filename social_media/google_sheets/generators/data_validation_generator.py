from __future__ import annotations

import random

from faker import Faker


DATA_VALIDATION_STATES = [
    "rules_list",
    "dropdown_editor",
    "checkbox_editor",
    "number_editor",
    "date_editor",
    "invalid_rule",
    "advanced_options",
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


def generate_data_validation_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(DATA_VALIDATION_STATES)
    if state not in DATA_VALIDATION_STATES:
        raise ValueError(
            f"Unknown data-validation state: {state}. "
            f"Expected one of {DATA_VALIDATION_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    priorities = ["Low", "Medium", "High", "Urgent"]
    statuses = ["Not started", "In progress", "In review", "Done"]
    departments = ["Product", "Engineering", "Design", "Marketing"]

    rows = []
    for index in range(18):
        progress = random.randint(5, 100)
        rows.append(
            {
                "row_number": index + 2,
                "task": fake.bs().capitalize(),
                "owner": fake.name(),
                "department": random.choice(departments),
                "priority": random.choice(priorities),
                "status": random.choice(statuses),
                "progress": progress,
                "progress_text": f"{progress}%",
                "approved": random.choice([True, False]),
                "due_date": fake.date_this_year().strftime("%b %d, %Y"),
            }
        )

    dropdown_options = [
        {"label": "Not started", "color": "#d2e3fc"},
        {"label": "In progress", "color": "#fce8b2"},
        {"label": "In review", "color": "#e8d7f1"},
        {"label": "Done", "color": "#b7e1cd"},
    ]

    rules = [
        {"range": "E2:E250", "criterion": "Dropdown", "summary": "4 status options", "icon": "arrow_drop_down_circle"},
        {"range": "G2:G250", "criterion": "Checkbox", "summary": "Checked / unchecked", "icon": "check_box"},
        {"range": "F2:F250", "criterion": "Number", "summary": "Between 0 and 100", "icon": "pin"},
        {"range": "H2:H250", "criterion": "Date", "summary": "Valid date", "icon": "calendar_today"},
    ]

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": width < 600,
        "document_title": random.choice(["Launch Tracker", "Team Workboard", "Delivery Plan"]),
        "account_initial": fake.first_name()[0].upper(),
        "sheet_name": "Tasks",
        "headers": ["Task", "Owner", "Department", "Priority", "Status", "Progress", "Approved", "Due date"],
        "rows": rows,
        "rules": [] if state == "empty_state" else rules,
        "selected_rule": rules[0],
        "apply_range": "E2:E250",
        "criterion": "Dropdown",
        "dropdown_options": dropdown_options,
        "range_suggestions": ["Tasks!E2:E250", "Tasks!G2:G250", "Tasks!H2:H250"],
        "help_text": "Choose the current workflow status.",
        "invalid_value": "",
        "number_min": "0",
        "number_max": "100",
        "date_condition": "is valid date",
    }
