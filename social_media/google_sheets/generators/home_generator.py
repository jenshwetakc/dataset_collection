from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker


# ==========================================================
# Home States
# ==========================================================

HOME_STATES = [
    "recent_grid",
    "recent_list",
    "starred",
    "shared",
    "offline",
    "search_results",
    "template_gallery",
    "file_context_menu",
    "sort_menu",
    "new_sheet_dialog",
    "empty",
]


POPUP_STATES = {
    "file_context_menu",
    "sort_menu",
    "new_sheet_dialog",
}


FILE_TITLES = [
    "Annual Budget",
    "Project Timeline",
    "Marketing Campaign",
    "Quarterly Sales",
    "Team Directory",
    "Research Results",
    "Inventory Tracker",
    "Customer Feedback",
    "Expense Report",
    "Weekly Schedule",
    "Product Roadmap",
    "Website Analytics",
    "Hiring Pipeline",
    "Content Calendar",
    "Event Planning",
]


TEMPLATE_NAMES = [
    "Blank spreadsheet",
    "To-do list",
    "Annual budget",
    "Monthly budget",
    "Schedule",
    "Travel planner",
    "Invoice",
    "Project timeline",
]


TEMPLATE_COLORS = [
    "#0F9D58",
    "#4285F4",
    "#F9AB00",
    "#A142F4",
    "#D93025",
    "#00ACC1",
]


# ==========================================================
# Spreadsheet Preview Data
# ==========================================================

def generate_preview_cells() -> list[list[str]]:

    headers = random.choice(
        [
            [
                "Date",
                "Owner",
                "Status",
                "Total",
            ],
            [
                "Task",
                "Priority",
                "Due",
                "Progress",
            ],
            [
                "Region",
                "Revenue",
                "Cost",
                "Profit",
            ],
            [
                "Item",
                "Quantity",
                "Price",
                "Stock",
            ],
        ]
    )

    rows = [
        headers,
    ]

    for _ in range(5):

        rows.append(
            [
                str(
                    random.randint(
                        10,
                        999,
                    )
                )
                for _ in range(4)
            ]
        )

    return rows


# ==========================================================
# Spreadsheet Files
# ==========================================================

def generate_files(
    fake: Faker,
    count: int,
) -> list[dict]:

    titles = random.sample(
        FILE_TITLES,
        k=min(
            count,
            len(FILE_TITLES),
        ),
    )

    files = []

    now = datetime.now()

    for index, title in enumerate(
        titles
    ):

        modified_time = (
            now
            - timedelta(
                hours=random.randint(
                    1,
                    500,
                )
            )
        )

        owner = (
            "Me"
            if random.random() < 0.65
            else fake.name()
        )

        files.append(
            {
                "id":
                    f"sheet_{index}",

                "title":
                    title,

                "owner":
                    owner,

                "modified":
                    modified_time.strftime(
                        "%b %d, %Y"
                    ),

                "modified_short":
                    modified_time.strftime(
                        "%b %d"
                    ),

                "starred":
                    random.random() < 0.35,

                "shared":
                    owner != "Me"
                    or random.random() < 0.35,

                "offline":
                    random.random() < 0.25,

                "preview_cells":
                    generate_preview_cells(),

                "accent":
                    random.choice(
                        TEMPLATE_COLORS
                    ),
            }
        )

    return files


# ==========================================================
# Template Gallery
# ==========================================================

def generate_templates() -> list[dict]:

    templates = []

    for index, name in enumerate(
        TEMPLATE_NAMES
    ):

        templates.append(
            {
                "id":
                    f"template_{index}",

                "name":
                    name,

                "color":
                    TEMPLATE_COLORS[
                        index
                        % len(
                            TEMPLATE_COLORS
                        )
                    ],

                "preview_cells":
                    generate_preview_cells(),
            }
        )

    return templates


# ==========================================================
# Home Generator
# ==========================================================

def generate_home_data(
    state: str | None = None,
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
            HOME_STATES
        )
    )

    if state not in HOME_STATES:

        raise ValueError(
            f"Unknown Sheets home state: {state}. "
            f"Available states: {HOME_STATES}"
        )

    all_files = generate_files(
        fake=fake,
        count=12,
    )

    if state == "starred":

        visible_files = [
            file
            for file in all_files
            if file["starred"]
        ]

    elif state == "shared":

        visible_files = [
            file
            for file in all_files
            if file["shared"]
        ]

    elif state == "offline":

        visible_files = [
            file
            for file in all_files
            if file["offline"]
        ]

    elif state == "empty":

        visible_files = []

    elif state == "search_results":

        # Keep several matching results.
        visible_files = all_files[
            :random.randint(
                3,
                7,
            )
        ]

    else:

        visible_files = all_files

    selected_file = (
        visible_files[0]
        if visible_files
        else all_files[0]
    )

    user_name = fake.name()

    navigation = [
        {
            "id": "recent",
            "label": "Recent",
            "icon": "schedule",
        },
        {
            "id": "starred",
            "label": "Starred",
            "icon": "star",
        },
        {
            "id": "shared",
            "label": "Shared with me",
            "icon": "group",
        },
        {
            "id": "offline",
            "label": "Offline",
            "icon": "offline_pin",
        },
    ]

    if state == "starred":

        active_navigation = "starred"

    elif state == "shared":

        active_navigation = "shared"

    elif state == "offline":

        active_navigation = "offline"

    else:

        active_navigation = "recent"

    return {
        "state":
            state,

        "is_popup":
            state in POPUP_STATES,

        "user": {
            "name":
                user_name,

            "initial":
                user_name[0],

            "email":
                fake.email(),
        },

        "navigation":
            navigation,

        "active_navigation":
            active_navigation,

        "files":
            visible_files,

        "selected_file":
            selected_file,

        "templates":
            generate_templates(),

        "search_query":
            random.choice(
                [
                    "budget",
                    "report",
                    "project",
                    "sales",
                ]
            ),

        "view_mode":
            (
                "list"
                if state == "recent_list"
                else "grid"
            ),

        "section_title": {
            "starred":
                "Starred",

            "shared":
                "Shared with me",

            "offline":
                "Offline",

            "search_results":
                "Search results",

            "template_gallery":
                "Template gallery",

            "empty":
                "Recent spreadsheets",
        }.get(
            state,
            "Recent spreadsheets",
        ),

        "sort_label":
            random.choice(
                [
                    "Last opened by me",
                    "Last modified",
                    "Title",
                ]
            ),

        "storage_used":
            random.randint(
                20,
                84,
            ),
    }