from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


VERSION_HISTORY_STATES = [
    "timeline",
    "version_selected",
    "named_versions",
    "expanded_group",
    "loading",
    "empty",
    "error",
    "restore_dialog",
    "rename_dialog",
    "make_copy_dialog",
]

POPUP_STATES = {
    "restore_dialog",
    "rename_dialog",
    "make_copy_dialog",
}


def _cell_rows(fake: Faker) -> list[list[dict]]:
    regions = ["North", "South", "East", "West", "Central"]
    statuses = ["Complete", "In progress", "At risk", "Planned"]
    rows = []
    for row_index in range(12):
        rows.append(
            [
                {"value": (datetime.now() - timedelta(days=row_index * 3)).strftime("%b %d"), "changed": row_index in {1, 4}},
                {"value": fake.name(), "changed": row_index in {2, 7}},
                {"value": random.choice(regions), "changed": row_index in {3, 8}},
                {"value": f"${random.randint(1200, 28000):,}", "changed": row_index in {1, 5, 9}},
                {"value": random.choice(statuses), "changed": row_index in {0, 6}},
                {"value": f"{random.randint(-12, 30)}%", "changed": row_index in {4, 10}},
            ]
        )
    return rows


def generate_version_history_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(VERSION_HISTORY_STATES)
    if state not in VERSION_HISTORY_STATES:
        raise ValueError(
            f"Unknown version history state: {state}. "
            f"Expected one of {VERSION_HISTORY_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    compact = width < 600
    people = []
    colors = ["#1A73E8", "#D93025", "#0F9D58", "#A142F4", "#F29900"]
    for color in colors:
        name = fake.name()
        people.append({"name": name, "initial": name[0].upper(), "color": color})

    now = datetime.now()
    groups = []
    for group_index, label in enumerate(["Today", "Yesterday", "September 26", "September 22"]):
        versions = []
        for version_index in range(random.randint(2, 4)):
            person = random.choice(people)
            version_time = now - timedelta(hours=group_index * 18 + version_index * 3)
            versions.append(
                {
                    "id": f"v{group_index}_{version_index}",
                    "time": version_time.strftime("%I:%M %p").lstrip("0"),
                    "author": person["name"],
                    "initial": person["initial"],
                    "color": person["color"],
                    "changes": random.randint(2, 24),
                    "named": group_index == 1 and version_index == 0,
                    "name": "Approved quarterly plan" if group_index == 1 and version_index == 0 else None,
                }
            )
        groups.append(
            {
                "label": label,
                "expanded": state == "expanded_group" or group_index < 2,
                "versions": versions,
            }
        )

    all_versions = [version for group in groups for version in group["versions"]]
    selected_version = random.choice(all_versions)
    if state == "named_versions":
        selected_version = next((v for v in all_versions if v["named"]), selected_version)

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": compact,
        "document_title": random.choice(
            ["Quarterly Sales Overview", "Team Budget Forecast", "Campaign Performance"]
        ),
        "groups": groups,
        "selected_version": selected_version,
        "contributors": people[: random.randint(3, 5)],
        "headers": ["Date", "Owner", "Region", "Revenue", "Status", "Variance"],
        "rows": _cell_rows(fake),
        "sheet_tabs": ["Overview", "Revenue", "Expenses"],
        "named_only": state == "named_versions",
        "copy_name": f"Copy of {random.choice(['Quarterly Sales Overview', 'Team Budget Forecast'])}",
        "account_initial": fake.first_name()[0].upper(),
    }
