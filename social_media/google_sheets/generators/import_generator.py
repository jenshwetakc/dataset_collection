from __future__ import annotations

import random

from faker import Faker


IMPORT_STATES = [
    "upload_idle",
    "drag_active",
    "uploading",
    "processing",
    "import_options",
    "preview",
    "success",
    "file_error",
    "overwrite_dialog",
    "cancel_dialog",
]

POPUP_STATES = {
    "import_options",
    "preview",
    "overwrite_dialog",
    "cancel_dialog",
}

FILE_NAMES = [
    "quarterly_sales.csv",
    "customer_feedback.xlsx",
    "inventory_export.csv",
    "research_results.tsv",
    "campaign_metrics.xlsx",
    "team_budget.csv",
]


def generate_import_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    state = state or random.choice(IMPORT_STATES)
    if state not in IMPORT_STATES:
        raise ValueError(
            f"Unknown import state: {state}. Expected one of {IMPORT_STATES}."
        )

    width = (viewport or {}).get("width", 1366)
    compact = width < 600
    file_name = random.choice(FILE_NAMES)
    file_size = round(random.uniform(0.4, 18.0), 1)
    progress = random.randint(28, 82)
    row_count = random.randint(420, 12800)
    column_count = random.randint(6, 18)
    selected_import_location = random.choice(
        ["Create new spreadsheet", "Insert new sheet(s)", "Replace spreadsheet"]
    )

    headers = ["Date", "Owner", "Region", "Category", "Revenue", "Status"]
    preview_rows = []
    for index in range(6):
        preview_rows.append(
            [
                fake.date_this_year().isoformat(),
                fake.name(),
                random.choice(["North", "South", "East", "West"]),
                random.choice(["Software", "Services", "Support"]),
                f"${random.randint(800, 28000):,}",
                random.choice(["Complete", "In progress", "Planned"]),
            ]
        )

    return {
        "state": state,
        "is_popup": state in POPUP_STATES,
        "is_compact": compact,
        "file_name": file_name,
        "file_size": file_size,
        "progress": progress,
        "row_count": row_count,
        "column_count": column_count,
        "selected_import_location": selected_import_location,
        "import_locations": [
            "Create new spreadsheet",
            "Insert new sheet(s)",
            "Replace spreadsheet",
            "Replace current sheet",
            "Append to current sheet",
        ],
        "separator_types": ["Detect automatically", "Comma", "Tab", "Semicolon", "Custom"],
        "selected_separator": random.choice(["Detect automatically", "Comma", "Tab"]),
        "convert_text": random.random() < 0.8,
        "headers": headers,
        "preview_rows": preview_rows,
        "error_title": random.choice(
            ["This file could not be imported", "Unsupported file format", "The file is too large"]
        ),
        "error_message": random.choice(
            [
                "Some rows contain inconsistent column counts. Correct the file and try again.",
                "Google Sheets cannot open this file. Upload a CSV, TSV, XLS, or XLSX file.",
                "The uploaded file exceeds the supported size for this import.",
            ]
        ),
        "account_initial": fake.first_name()[0].upper(),
    }
