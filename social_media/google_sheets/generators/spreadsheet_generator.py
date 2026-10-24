from __future__ import annotations

import random

from datetime import (
    date,
    timedelta,
)

from faker import Faker


# ==========================================================
# Spreadsheet States
# ==========================================================

SPREADSHEET_STATES = [
    "blank",
    "populated",
    "cell_selected",
    "range_selected",
    "formula_editing",
    "column_selected",
    "row_selected",
    "filter_enabled",
    "filter_menu",
    "context_menu",
    "format_menu",
    "sheet_tab_menu",
    "find_replace",
    "share_dialog",
    "comment_panel",
    "protected_range_warning",
    "chart_inserted",
]


# States where background annotations must be skipped.
POPUP_STATES = {
    "filter_menu",
    "context_menu",
    "format_menu",
    "sheet_tab_menu",
    "find_replace",
    "share_dialog",
    "protected_range_warning",
}


DOCUMENT_TITLES = [
    "Quarterly Sales Overview",
    "Marketing Campaign Tracker",
    "Project Resource Plan",
    "Inventory and Orders",
    "Research Dataset Review",
    "Team Budget Forecast",
]


SHEET_NAMES = [
    "Overview",
    "Revenue",
    "Expenses",
    "Forecast",
    "Notes",
]


# ==========================================================
# Column Name
# ==========================================================

def column_name(
    index: int,
) -> str:
    """
    Convert zero-based index to spreadsheet column name.

    0 -> A
    1 -> B
    25 -> Z
    26 -> AA
    """

    value = index + 1
    result = ""

    while value:

        value, remainder = divmod(
            value - 1,
            26,
        )

        result = (
            chr(65 + remainder)
            + result
        )

    return result


# ==========================================================
# Table Data
# ==========================================================

def generate_table(
    fake: Faker,
    row_count: int,
    column_count: int,
) -> tuple[list[str], list[dict]]:

    headings = [
        "Date",
        "Owner",
        "Region",
        "Category",
        "Units",
        "Revenue",
        "Cost",
        "Status",
        "Variance",
        "Notes",
        "Priority",
        "Updated",
    ][:column_count]

    regions = [
        "North",
        "South",
        "East",
        "West",
        "Central",
    ]

    categories = [
        "Software",
        "Services",
        "Hardware",
        "Support",
    ]

    statuses = [
        "Complete",
        "In progress",
        "At risk",
        "Planned",
    ]

    start_date = (
        date.today()
        - timedelta(days=120)
    )

    rows = []

    for row_index in range(
        row_count
    ):

        units = random.randint(
            8,
            180,
        )

        revenue = (
            units
            * random.randint(
                45,
                260,
            )
        )

        cost = round(
            revenue
            * random.uniform(
                0.35,
                0.78,
            )
        )

        values = [
            (
                start_date
                + timedelta(
                    days=row_index * 3
                )
            ).isoformat(),

            fake.name(),

            random.choice(
                regions
            ),

            random.choice(
                categories
            ),

            str(
                units
            ),

            f"${revenue:,}",

            f"${cost:,}",

            random.choice(
                statuses
            ),

            (
                f"{random.randint(-18, 32)}%"
            ),

            fake.sentence(
                nb_words=4
            ).rstrip("."),

            random.choice(
                [
                    "High",
                    "Medium",
                    "Low",
                ]
            ),

            fake.date_this_year().isoformat(),
        ][:column_count]

        cells = []

        for column_index, value in enumerate(
            values
        ):

            cells.append(
                {
                    "column":
                        column_name(
                            column_index
                        ),

                    "column_index":
                        column_index,

                    "value":
                        value,
                }
            )

        rows.append(
            {
                "number":
                    row_index + 2,

                "cells":
                    cells,
            }
        )

    return (
        headings,
        rows,
    )


# ==========================================================
# Spreadsheet Generator
# ==========================================================

def generate_spreadsheet_data(
    state: str | None = None,
    viewport: dict | None = None,
    seed: int | None = None,
) -> dict:

    if seed is not None:

        random.seed(
            seed
        )

        Faker.seed(
            seed
        )

    fake = Faker()

    state = (
        state
        or random.choice(
            SPREADSHEET_STATES
        )
    )

    if state not in SPREADSHEET_STATES:

        raise ValueError(
            f"Unknown spreadsheet state: {state}. "
            f"Available states: {SPREADSHEET_STATES}"
        )

    viewport = (
        viewport
        or {}
    )

    viewport_width = viewport.get(
        "width",
        1366,
    )

    compact = (
        viewport_width < 600
    )

    medium = (
        600
        <= viewport_width
        < 1024
    )

    if compact:

        column_count = 6
        row_count = 24

    elif medium:

        column_count = 9
        row_count = 30

    else:

        column_count = 12
        row_count = 36

    headings, rows = generate_table(
        fake=fake,
        row_count=row_count,
        column_count=column_count,
    )

    if state == "blank":

        headings = [
            ""
            for _ in range(
                column_count
            )
        ]

        for row in rows:

            for cell in row["cells"]:

                cell["value"] = ""

    selected_row = random.randint(
        3,
        min(
            row_count,
            12,
        ),
    )

    selected_column_index = random.randint(
        1,
        min(
            column_count - 1,
            5,
        ),
    )

    selected_column = column_name(
        selected_column_index
    )

    selected_cell = (
        f"{selected_column}"
        f"{selected_row}"
    )

    selected_value = (
        rows[
            selected_row - 2
        ][
            "cells"
        ][
            selected_column_index
        ][
            "value"
        ]
    )

    range_end_column_index = min(
        selected_column_index + 2,
        column_count - 1,
    )

    range_end_column = column_name(
        range_end_column_index
    )

    collaborators = []

    for color in [
        "#7C4DFF",
        "#D93025",
        "#0288D1",
    ]:

        name = fake.name()

        collaborators.append(
            {
                "name":
                    name,

                "initial":
                    name[0],

                "color":
                    color,
            }
        )

    sheet_count = random.randint(
        3,
        5,
    )

    selected_sheet_names = random.sample(
        SHEET_NAMES,
        k=sheet_count,
    )

    sheet_tabs = []

    for index, name in enumerate(
        selected_sheet_names
    ):

        sheet_tabs.append(
            {
                "name":
                    name,

                "active":
                    index == 0,
            }
        )

    return {
        "state":
            state,

        "is_popup":
            state in POPUP_STATES,

        "is_compact":
            compact,

        "is_medium":
            medium,

        "title":
            random.choice(
                DOCUMENT_TITLES
            ),

        "starred":
            random.random() < 0.45,

        "saved_text":
            random.choice(
                [
                    "Saved to Drive",
                    "Saving…",
                    "All changes saved",
                ]
            ),

        "menus": [
            "File",
            "Edit",
            "View",
            "Insert",
            "Format",
            "Data",
            "Tools",
            "Extensions",
            "Help",
        ],

        "toolbar_controls": [
            {
                "icon": "undo",
                "label": "Undo",
            },
            {
                "icon": "redo",
                "label": "Redo",
            },
            {
                "icon": "print",
                "label": "Print",
            },
            {
                "icon": "format_paint",
                "label": "Paint format",
            },
            {
                "icon": "attach_money",
                "label": "Currency",
            },
            {
                "icon": "percent",
                "label": "Percent",
            },
            {
                "icon": "format_bold",
                "label": "Bold",
            },
            {
                "icon": "format_italic",
                "label": "Italic",
            },
            {
                "icon": "format_align_left",
                "label": "Alignment",
            },
            {
                "icon": "format_color_fill",
                "label": "Fill color",
            },
            {
                "icon": "borders",
                "label": "Borders",
            },
        ],

        "column_letters": [
            column_name(index)
            for index in range(
                column_count
            )
        ],

        "headings":
            headings,

        "rows":
            rows,

        "selected_cell":
            selected_cell,

        "selected_row":
            selected_row,

        "selected_column":
            selected_column,

        "selected_column_index":
            selected_column_index,

        "range_end_column_index":
            range_end_column_index,

        "selected_value":
            selected_value,

        "formula":
            (
                f"=SUM(F2:F"
                f"{min(row_count, 18)})"
            ),

        "range_label":
            (
                f"{selected_column}"
                f"{selected_row}:"
                f"{range_end_column}"
                f"{selected_row + 4}"
            ),

        "filter_values": [
            "Complete",
            "In progress",
            "At risk",
            "Planned",
        ],

        "sheet_tabs":
            sheet_tabs,

        "collaborators":
            collaborators,

        "comments": [
            {
                "author":
                    fake.name(),

                "initial":
                    fake.first_name()[0],

                "body":
                    fake.sentence(
                        nb_words=9
                    ),

                "time":
                    "2h",
            },
            {
                "author":
                    fake.name(),

                "initial":
                    fake.first_name()[0],

                "body":
                    fake.sentence(
                        nb_words=7
                    ),

                "time":
                    "Yesterday",
            },
        ],

        "find_text":
            random.choice(
                [
                    "Complete",
                    "North",
                    "Software",
                    "High",
                ]
            ),

        "chart": {
            "title":
                "Revenue by region",

            "bars": [
                random.randint(
                    35,
                    94,
                )
                for _ in range(5)
            ],

            "labels": [
                "North",
                "South",
                "East",
                "West",
                "Central",
            ],
        },
    }