from __future__ import annotations

import random

from faker import Faker


fake = Faker()


TEMPLATE_GALLERY_STATES = [
    "all_templates",
    "category_filtered",
    "search_results",
    "favorites",
    "preview_dialog",
    "no_results",
]


TEMPLATE_CATEGORIES = [
    {
        "id": "all",
        "label": "All templates",
        "icon": "dashboard",
    },
    {
        "id": "personal",
        "label": "Personal",
        "icon": "person",
    },
    {
        "id": "work",
        "label": "Work",
        "icon": "business_center",
    },
    {
        "id": "project_management",
        "label": "Project management",
        "icon": "task_alt",
    },
    {
        "id": "education",
        "label": "Education",
        "icon": "school",
    },
]


TEMPLATE_DEFINITIONS = [
    {
        "id": "annual_budget",
        "name": "Annual budget",
        "category": "personal",
        "description": "Track income, spending, savings, and monthly totals.",
        "accent": "#188038",
        "columns": [
            "Category",
            "Jan",
            "Feb",
            "Mar",
        ],
    },
    {
        "id": "monthly_budget",
        "name": "Monthly budget",
        "category": "personal",
        "description": "Plan recurring expenses and compare planned costs.",
        "accent": "#0F9D58",
        "columns": [
            "Expense",
            "Planned",
            "Actual",
            "Difference",
        ],
    },
    {
        "id": "to_do_list",
        "name": "To-do list",
        "category": "personal",
        "description": "Organize tasks, priorities, owners, and deadlines.",
        "accent": "#4285F4",
        "columns": [
            "Task",
            "Owner",
            "Due",
            "Status",
        ],
    },
    {
        "id": "investment_tracker",
        "name": "Investment tracker",
        "category": "personal",
        "description": "Monitor investments and portfolio performance.",
        "accent": "#9334E6",
        "columns": [
            "Asset",
            "Units",
            "Price",
            "Value",
        ],
    },
    {
        "id": "project_timeline",
        "name": "Project timeline",
        "category": "project_management",
        "description": "Coordinate milestones, dependencies, and delivery.",
        "accent": "#1A73E8",
        "columns": [
            "Milestone",
            "Start",
            "Finish",
            "Progress",
        ],
    },
    {
        "id": "project_tracker",
        "name": "Project tracker",
        "category": "project_management",
        "description": "Track project tasks, owners, risks, and status.",
        "accent": "#185ABC",
        "columns": [
            "Project",
            "Owner",
            "Status",
            "Risk",
        ],
    },
    {
        "id": "gantt_chart",
        "name": "Gantt chart",
        "category": "project_management",
        "description": "Visualize a schedule across multiple workstreams.",
        "accent": "#D93025",
        "columns": [
            "Phase",
            "Week 1",
            "Week 2",
            "Week 3",
        ],
    },
    {
        "id": "employee_schedule",
        "name": "Employee schedule",
        "category": "work",
        "description": "Plan shifts, employee assignments, and availability.",
        "accent": "#F9AB00",
        "columns": [
            "Employee",
            "Monday",
            "Tuesday",
            "Wednesday",
        ],
    },
    {
        "id": "expense_report",
        "name": "Expense report",
        "category": "work",
        "description": "Record business expenses and reimbursement status.",
        "accent": "#E37400",
        "columns": [
            "Date",
            "Vendor",
            "Amount",
            "Status",
        ],
    },
    {
        "id": "sales_dashboard",
        "name": "Sales dashboard",
        "category": "work",
        "description": "Summarize sales performance and monthly targets.",
        "accent": "#A142F4",
        "columns": [
            "Region",
            "Target",
            "Sales",
            "Growth",
        ],
    },
    {
        "id": "attendance",
        "name": "Attendance",
        "category": "education",
        "description": "Record student attendance and participation.",
        "accent": "#12B5CB",
        "columns": [
            "Student",
            "Present",
            "Absent",
            "Rate",
        ],
    },
    {
        "id": "grade_book",
        "name": "Grade book",
        "category": "education",
        "description": "Calculate grades and monitor student progress.",
        "accent": "#C5221F",
        "columns": [
            "Student",
            "Quiz",
            "Exam",
            "Grade",
        ],
    },
]


POPUP_STATES = {
    "preview_dialog",
}


def generate_preview_rows(
    columns: list[str],
) -> list[list[str]]:

    rows = [
        columns,
    ]

    for _ in range(4):

        row = []

        for column_index, column in enumerate(
            columns
        ):

            if column_index == 0:

                value = random.choice(
                    [
                        fake.first_name(),
                        fake.word().title(),
                        fake.company(),
                        fake.job(),
                    ]
                )

            elif any(
                keyword in column.lower()
                for keyword in [
                    "amount",
                    "sales",
                    "target",
                    "price",
                    "value",
                    "planned",
                    "actual",
                ]
            ):

                value = (
                    f"${random.randint(5, 95):,}K"
                )

            elif any(
                keyword in column.lower()
                for keyword in [
                    "status",
                    "risk",
                    "grade",
                ]
            ):

                value = random.choice(
                    [
                        "Complete",
                        "Active",
                        "Pending",
                        "Low",
                        "A",
                    ]
                )

            elif any(
                keyword in column.lower()
                for keyword in [
                    "progress",
                    "growth",
                    "rate",
                ]
            ):

                value = (
                    f"{random.randint(10, 100)}%"
                )

            else:

                value = random.choice(
                    [
                        "Yes",
                        "No",
                        "May 12",
                        "Jun 24",
                        "Week 2",
                    ]
                )

            row.append(
                value
            )

        rows.append(
            row
        )

    return rows


def build_template(
    definition: dict,
    favorite_ids: set[str],
) -> dict:

    return {
        **definition,
        "favorite":
            definition["id"] in favorite_ids,
        "usage_count":
            random.randint(
                120,
                9800,
            ),
        "preview_rows":
            generate_preview_rows(
                definition["columns"]
            ),
    }


def generate_template_gallery_data(
    state: str | None = None,
) -> dict:

    state = (
        state
        or random.choice(
            TEMPLATE_GALLERY_STATES
        )
    )

    if state not in TEMPLATE_GALLERY_STATES:

        raise ValueError(
            f"Unknown template gallery state: {state}. "
            f"Available states: {TEMPLATE_GALLERY_STATES}"
        )

    favorite_count = random.randint(
        2,
        5,
    )

    favorite_ids = {
        definition["id"]
        for definition in random.sample(
            TEMPLATE_DEFINITIONS,
            k=favorite_count,
        )
    }

    templates = [
        build_template(
            definition,
            favorite_ids,
        )
        for definition in TEMPLATE_DEFINITIONS
    ]

    selected_category = "all"
    search_query = ""
    section_title = "All templates"
    visible_templates = templates

    if state == "category_filtered":

        selected_category = random.choice(
            [
                "personal",
                "work",
                "project_management",
                "education",
            ]
        )

        category = next(
            category
            for category in TEMPLATE_CATEGORIES
            if category["id"] == selected_category
        )

        section_title = category["label"]

        visible_templates = [
            template_item
            for template_item in templates
            if (
                template_item["category"]
                == selected_category
            )
        ]

    elif state == "search_results":

        selected_template = random.choice(
            templates
        )

        search_query = random.choice(
            selected_template["name"].split()
        )

        section_title = (
            f'Results for "{search_query}"'
        )

        visible_templates = [
            template_item
            for template_item in templates
            if (
                search_query.lower()
                in template_item["name"].lower()
                or search_query.lower()
                in template_item["description"].lower()
            )
        ]

    elif state == "favorites":

        section_title = "Favorite templates"

        visible_templates = [
            template_item
            for template_item in templates
            if template_item["favorite"]
        ]

    elif state == "no_results":

        search_query = random.choice(
            [
                "Cryptocurrency mining ledger",
                "Underwater research station",
                "Interplanetary delivery plan",
            ]
        )

        section_title = (
            f'Results for "{search_query}"'
        )

        visible_templates = []

    featured_templates = random.sample(
        templates,
        k=min(
            4,
            len(templates),
        ),
    )

    preview_template = (
        random.choice(
            templates
        )
        if state == "preview_dialog"
        else None
    )

    return {
        "app_name":
            "Google Sheets",
        "state":
            state,
        "is_popup":
            state in POPUP_STATES,
        "categories":
            TEMPLATE_CATEGORIES,
        "selected_category":
            selected_category,
        "search_query":
            search_query,
        "section_title":
            section_title,
        "templates":
            visible_templates,
        "all_templates":
            templates,
        "featured_templates":
            featured_templates,
        "preview_template":
            preview_template,
        "sort_label":
            random.choice(
                [
                    "Recommended",
                    "Most popular",
                    "Recently added",
                    "Alphabetical",
                ]
            ),
        "user": {
            "name":
                fake.name(),
            "email":
                fake.email(),
            "initial":
                fake.first_name()[0].upper(),
        },
    }