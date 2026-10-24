from __future__ import annotations

import random

from faker import Faker


PIVOT_TABLE_STATES = [
    "pivot_default",
    "rows_configured",
    "columns_configured",
    "metrics_configured",
    "filter_configured",
    "field_menu",
    "range_dialog",
    "suggestion",
    "loading",
    "delete_dialog",
]

POPUP_STATES = {
    "field_menu",
    "range_dialog",
    "delete_dialog",
}

AVAILABLE_FIELDS = [
    "Date",
    "Owner",
    "Region",
    "Category",
    "Revenue",
    "Units",
    "Status",
]


def generate_pivot_table_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(PIVOT_TABLE_STATES)
    if state not in PIVOT_TABLE_STATES:
        raise ValueError(
            f"Unknown pivot-table state: {state}. "
            f"Expected one of {PIVOT_TABLE_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    regions = ["North", "South", "East", "West"]
    categories = ["Software", "Services", "Hardware"]

    source_rows = []
    for index in range(12):
        revenue = random.randint(2500, 28000)
        units = random.randint(8, 160)
        source_rows.append(
            {
                "date": fake.date_this_year().isoformat(),
                "owner": fake.name(),
                "region": random.choice(regions),
                "category": random.choice(categories),
                "revenue_text": f"${revenue:,}",
                "units_text": str(units),
                "status": random.choice(["Complete", "In progress", "Planned"]),
            }
        )

    pivot_rows = []
    grand_total = 0
    for region in regions:
        software = random.randint(18000, 76000)
        services = random.randint(16000, 68000)
        hardware = random.randint(12000, 62000)
        total = software + services + hardware
        grand_total += total
        pivot_rows.append(
            {
                "label": region,
                "software_text": f"${software:,}",
                "services_text": f"${services:,}",
                "hardware_text": f"${hardware:,}",
                "total_text": f"${total:,}",
            }
        )

    rows = ["Region"]
    columns = []
    metrics = ["SUM of Revenue"]
    filters = []

    if state in {"columns_configured", "metrics_configured", "filter_configured"}:
        columns = ["Category"]
    if state == "metrics_configured":
        metrics = ["SUM of Revenue", "SUM of Units"]
    if state == "filter_configured":
        filters = ["Status is Complete"]

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": width < 600,
        "document_title": random.choice(
            ["Regional Sales Analysis", "Operations Summary", "Campaign Results"]
        ),
        "source_range": random.choice(["Data!A1:G250", "Sales!A1:G480", "Orders!A1:G320"]),
        "source_headers": AVAILABLE_FIELDS,
        "source_rows": source_rows,
        "pivot_rows": pivot_rows,
        "grand_total_text": f"${grand_total:,}",
        "available_fields": AVAILABLE_FIELDS,
        "row_fields": rows,
        "column_fields": columns,
        "metric_fields": metrics,
        "filter_fields": filters,
        "selected_field": random.choice(AVAILABLE_FIELDS),
        "suggestion_title": "Revenue by region and category",
        "suggestion_description": "Summarize total revenue across regions with categories as columns.",
        "account_initial": fake.first_name()[0].upper(),
    }
