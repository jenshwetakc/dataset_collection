from __future__ import annotations

import random

from datetime import (
    date,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

TASK_STATES = [
    "all_tasks",
    "today",
    "upcoming",
    "important",
    "completed",
    "overdue",
    "board_view",
    "search_results",
    "task_details_dialog",
    "create_task_dialog",
    "filter_menu",
    "mobile_task_sheet",
]


TASK_TITLES = [
    "Review research paper",
    "Prepare presentation slides",
    "Submit progress report",
    "Update experiment results",
    "Schedule advisor meeting",
    "Review pull request",
    "Complete dataset validation",
    "Write literature review",
    "Prepare weekly summary",
    "Check annotation quality",
    "Update project documentation",
    "Run model evaluation",
    "Reply to project email",
    "Organize research notes",
]


LISTS = [
    {
        "id": "personal",
        "name": "Personal",
        "icon": "person",
        "color": "blue",
    },
    {
        "id": "work",
        "name": "Work",
        "icon": "work",
        "color": "purple",
    },
    {
        "id": "research",
        "name": "Research",
        "icon": "science",
        "color": "green",
    },
    {
        "id": "study",
        "name": "Study",
        "icon": "school",
        "color": "orange",
    },
]


# ==========================================================
# Subtask
# ==========================================================

def generate_subtask(
    index: int,
) -> dict:

    return {
        "id":
            f"subtask_{index}",

        "title":
            fake.sentence(
                nb_words=random.randint(
                    3,
                    7,
                )
            ).rstrip("."),

        "completed":
            random.random() < 0.35,
    }


# ==========================================================
# Task
# ==========================================================

def generate_task(
    index: int,
) -> dict:

    today = date.today()

    due_offset = random.randint(
        -5,
        20,
    )

    due_date = (
        today
        + timedelta(
            days=due_offset
        )
    )

    completed = (
        random.random() < 0.25
    )

    priority = random.choice(
        [
            "none",
            "low",
            "medium",
            "high",
        ]
    )

    list_data = random.choice(
        LISTS
    )

    subtask_count = random.randint(
        0,
        4,
    )

    subtasks = [
        generate_subtask(
            subtask_index
        )
        for subtask_index in range(
            subtask_count
        )
    ]

    completed_subtasks = sum(
        subtask["completed"]
        for subtask in subtasks
    )

    if completed:

        status = "completed"

    elif due_date < today:

        status = "overdue"

    elif due_date == today:

        status = "today"

    elif due_offset <= 7:

        status = "upcoming"

    else:

        status = "later"

    return {
        "id":
            f"task_{index}",

        "title":
            random.choice(
                TASK_TITLES
            ),

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    1,
                    3,
                )
            ),

        "completed":
            completed,

        "important":
            random.random() < 0.30,

        "priority":
            priority,

        "status":
            status,

        "due_date":
            due_date.isoformat(),

        "due_date_text":
            due_date.strftime(
                "%b %d"
            ),

        "due_time":
            random.choice(
                [
                    "09:00",
                    "10:30",
                    "13:00",
                    "15:30",
                    "18:00",
                    "",
                ]
            ),

        "list_id":
            list_data["id"],

        "list_name":
            list_data["name"],

        "list_color":
            list_data["color"],

        "assignee":
            fake.name(),

        "assignee_initials":
            "".join(
                part[0].upper()
                for part
                in fake.name().split()[:2]
            ),

        "subtasks":
            subtasks,

        "subtask_count":
            len(subtasks),

        "completed_subtasks":
            completed_subtasks,

        "progress":
            (
                int(
                    completed_subtasks
                    / len(subtasks)
                    * 100
                )
                if subtasks
                else 0
            ),

        "tags": random.sample(
            [
                "Research",
                "Urgent",
                "Review",
                "Writing",
                "Meeting",
                "Experiment",
            ],
            k=random.randint(
                0,
                3,
            ),
        ),

        "has_attachment":
            random.random() < 0.30,

        "comment_count":
            random.randint(
                0,
                6,
            ),
    }


# ==========================================================
# Sections
# ==========================================================

def create_task_sections(
    tasks: list[dict],
) -> list[dict]:

    section_definitions = [
        {
            "id": "overdue",
            "title": "Overdue",
        },
        {
            "id": "today",
            "title": "Today",
        },
        {
            "id": "upcoming",
            "title": "Upcoming",
        },
        {
            "id": "later",
            "title": "Later",
        },
        {
            "id": "completed",
            "title": "Completed",
        },
    ]

    sections = []

    for definition in section_definitions:

        section_tasks = [
            task
            for task in tasks
            if task["status"]
            == definition["id"]
        ]

        if not section_tasks:
            continue

        sections.append(
            {
                "id":
                    definition["id"],

                "title":
                    definition["title"],

                "tasks":
                    section_tasks,

                "count":
                    len(section_tasks),
            }
        )

    return sections


# ==========================================================
# Main Generator
# ==========================================================

def generate_tasks_data(
    state: str | None = None,
    seed: int | None = None,
    viewport: dict | None = None,
) -> dict:

    if seed is not None:

        random.seed(
            seed
        )

        Faker.seed(
            seed
        )

    if state is None:

        state = random.choice(
            TASK_STATES
        )

    if state not in TASK_STATES:

        raise ValueError(
            f"Unknown task state: {state}. "
            f"Available states: {TASK_STATES}"
        )

    tasks = [
        generate_task(
            index
        )
        for index in range(
            random.randint(
                16,
                28,
            )
        )
    ]

    selected_task = (
        random.choice(tasks)
        if tasks
        else None
    )

    if state == "today":

        visible_tasks = [
            task
            for task in tasks
            if task["status"] == "today"
        ]

    elif state == "upcoming":

        visible_tasks = [
            task
            for task in tasks
            if task["status"]
            in {
                "upcoming",
                "later",
            }
        ]

    elif state == "important":

        visible_tasks = [
            task
            for task in tasks
            if task["important"]
        ]

    elif state == "completed":

        visible_tasks = [
            task
            for task in tasks
            if task["completed"]
        ]

    elif state == "overdue":

        visible_tasks = [
            task
            for task in tasks
            if task["status"]
            == "overdue"
        ]

    elif state == "search_results":

        visible_tasks = [
            task
            for task in tasks
            if any(
                keyword
                in task["title"].lower()
                for keyword in [
                    "research",
                    "review",
                    "report",
                ]
            )
        ]

    else:

        visible_tasks = tasks

    popup_states = {
        "task_details_dialog",
        "create_task_dialog",
        "filter_menu",
        "mobile_task_sheet",
    }

    return {
        "state":
            state,

        "popup_open":
            state in popup_states,

        "is_mobile_sheet":
            state == "mobile_task_sheet",

        "board_view":
            state == "board_view",

        "page_title": {
            "all_tasks": "All tasks",
            "today": "Today",
            "upcoming": "Upcoming",
            "important": "Important",
            "completed": "Completed",
            "overdue": "Overdue",
            "board_view": "Task board",
            "search_results": "Search results",
            "task_details_dialog": "All tasks",
            "create_task_dialog": "All tasks",
            "filter_menu": "All tasks",
            "mobile_task_sheet": "All tasks",
        }[state],

        "search_query":
            (
                "research"
                if state == "search_results"
                else ""
            ),

        "tasks":
            tasks,

        "visible_tasks":
            visible_tasks,

        "sections":
            create_task_sections(
                visible_tasks
            ),

        "selected_task":
            selected_task,

        "lists":
            LISTS,

        "counts": {
            "all":
                len(tasks),

            "today":
                sum(
                    task["status"] == "today"
                    for task in tasks
                ),

            "important":
                sum(
                    task["important"]
                    for task in tasks
                ),

            "completed":
                sum(
                    task["completed"]
                    for task in tasks
                ),

            "overdue":
                sum(
                    task["status"] == "overdue"
                    for task in tasks
                ),
        },

        "board_columns": [
            {
                "id": "overdue",
                "title": "Overdue",
                "tasks": [
                    task
                    for task in visible_tasks
                    if task["status"]
                    == "overdue"
                ],
            },
            {
                "id": "today",
                "title": "Today",
                "tasks": [
                    task
                    for task in visible_tasks
                    if task["status"]
                    == "today"
                ],
            },
            {
                "id": "upcoming",
                "title": "Upcoming",
                "tasks": [
                    task
                    for task in visible_tasks
                    if task["status"]
                    in {
                        "upcoming",
                        "later",
                    }
                ],
            },
            {
                "id": "completed",
                "title": "Completed",
                "tasks": [
                    task
                    for task in visible_tasks
                    if task["completed"]
                ],
            },
        ],

        "filter_options": [
            {
                "id": "all",
                "label": "All tasks",
                "selected": True,
            },
            {
                "id": "due_date",
                "label": "Due date",
                "selected": False,
            },
            {
                "id": "priority",
                "label": "Priority",
                "selected": False,
            },
            {
                "id": "list",
                "label": "Task list",
                "selected": False,
            },
            {
                "id": "assignee",
                "label": "Assignee",
                "selected": False,
            },
        ],

        "viewport":
            viewport or {},
    }