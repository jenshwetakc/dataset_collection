from __future__ import annotations

import random

from faker import Faker


CHART_EDITOR_STATES = [
    "chart_selected",
    "setup_tab",
    "customize_tab",
    "chart_type_menu",
    "data_range_dialog",
    "series_settings",
    "legend_settings",
    "loading",
    "error",
    "delete_dialog",
]

POPUP_STATES = {
    "chart_type_menu",
    "data_range_dialog",
    "delete_dialog",
}

CHART_TYPES = [
    {"name": "Column chart", "icon": "bar_chart"},
    {"name": "Line chart", "icon": "show_chart"},
    {"name": "Area chart", "icon": "area_chart"},
    {"name": "Pie chart", "icon": "pie_chart"},
    {"name": "Scatter chart", "icon": "scatter_plot"},
    {"name": "Combo chart", "icon": "stacked_line_chart"},
]


def generate_chart_editor_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(CHART_EDITOR_STATES)
    if state not in CHART_EDITOR_STATES:
        raise ValueError(
            f"Unknown chart editor state: {state}. Expected one of {CHART_EDITOR_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    compact = width < 600
    categories = random.sample(
        ["North", "South", "East", "West", "Central", "Online"],
        k=5,
    )
    values = [random.randint(34, 96) for _ in categories]
    secondary_values = [random.randint(22, 82) for _ in categories]
    selected_type = random.choice(CHART_TYPES)
    title = random.choice(
        ["Revenue by region", "Quarterly performance", "Campaign conversions", "Orders by channel"]
    )

    table_rows = []
    for index, category in enumerate(categories):
        value = random.randint(12000, 82000)
        target = random.randint(15000, 76000)
        table_rows.append(
            {
                "category": category,
                "value": value,
                "value_text": f"${value:,}",
                "target": target,
                "target_text": f"${target:,}",
                "owner": fake.name(),
                "status": random.choice(["Complete", "In progress", "Planned"]),
            }
        )

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": compact,
        "document_title": random.choice(
            ["Quarterly Sales Overview", "Marketing Dashboard", "Operations Metrics"]
        ),
        "chart_title": title,
        "chart_types": CHART_TYPES,
        "selected_type": selected_type,
        "categories": categories,
        "values": values,
        "secondary_values": secondary_values,
        "data_range": random.choice(["Overview!A1:C6", "Revenue!B2:D7", "Dashboard!A3:C8"]),
        "x_axis": "Region",
        "series": ["Revenue", "Target"],
        "colors": ["#1A73E8", "#0F9D58"],
        "table_rows": table_rows,
        "headers": ["Region", "Revenue", "Target", "Owner", "Status"],
        "legend_position": random.choice(["Right", "Bottom", "Top", "Inside"]),
        "account_initial": fake.first_name()[0].upper(),
    }
