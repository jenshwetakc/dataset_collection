from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

TEXT_EDITOR_STATES = [

    "empty_document",

    "document_open",

    "multiple_tabs",

    "unsaved_changes",

    "find_open",

    "replace_open",

    "split_view",

    "recent_files_menu",

    "document_menu_open",

    "save_as_dialog",

    "open_file_dialog",

    "close_unsaved_dialog",
]


# ==========================================================
# File Names
# ==========================================================

FILE_NAMES = [

    "notes.txt",

    "README.md",

    "meeting_notes.txt",

    "project_plan.md",

    "ideas.txt",

    "todo.md",

    "research_notes.txt",

    "draft.txt",

    "config.ini",

    "requirements.txt",
]


# ==========================================================
# Recent Files
# ==========================================================

RECENT_FILE_LOCATIONS = [

    "~/Documents",

    "~/Desktop",

    "~/Projects",

    "~/Downloads",
]


# ==========================================================
# Document Menu
# ==========================================================

DOCUMENT_MENU_ENTRIES = [

    {
        "label":
            "New Document",

        "icon":
            "note_add",
    },

    {
        "label":
            "Open",

        "icon":
            "folder_open",
    },

    {
        "label":
            "Save",

        "icon":
            "save",
    },

    {
        "label":
            "Save As",

        "icon":
            "save_as",
    },

    {
        "label":
            "Print",

        "icon":
            "print",
    },

    {
        "label":
            "Preferences",

        "icon":
            "settings",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_document_lines(
    minimum: int = 10,
    maximum: int = 24,
) -> list[str]:

    count = random.randint(
        minimum,
        maximum,
    )

    lines = []

    for index in range(
        count
    ):

        if index == 0:

            lines.append(
                random.choice(
                    [
                        "# Project Notes",
                        "# Meeting Notes",
                        "# Research Ideas",
                        "# Tasks",
                        "# Draft",
                    ]
                )
            )

        elif random.random() < 0.18:

            lines.append(
                ""
            )

        elif random.random() < 0.25:

            lines.append(
                "- "
                + fake.sentence(
                    nb_words=random.randint(
                        4,
                        9,
                    )
                )
            )

        else:

            lines.append(
                fake.sentence(
                    nb_words=random.randint(
                        6,
                        14,
                    )
                )
            )

    return lines


def generate_tab(
    index: int,
    active: bool = False,
) -> dict:

    return {

        "id":
            index,

        "name":
            random.choice(
                FILE_NAMES
            ),

        "active":
            active,

        "modified":
            random.random()
            < 0.30,
    }


def generate_tabs(
    state: str,
) -> list[dict]:

    if state == "multiple_tabs":

        count = random.randint(
            3,
            5,
        )

    else:

        count = 1


    tabs = [

        generate_tab(
            index,
            active=index == 0,
        )

        for index in range(
            count
        )
    ]


    if state == "unsaved_changes":

        tabs[0][
            "modified"
        ] = True


    return tabs


def generate_recent_files() -> list[dict]:

    count = random.randint(
        4,
        7,
    )

    selected = random.sample(

        FILE_NAMES,

        k=min(
            count,
            len(
                FILE_NAMES
            ),
        ),
    )


    return [

        {

            "name":
                name,

            "location":
                random.choice(
                    RECENT_FILE_LOCATIONS
                ),

            "icon":
                (
                    "markdown"
                    if name.endswith(
                        ".md"
                    )
                    else "description"
                ),
        }

        for name in selected
    ]


def generate_open_files() -> list[dict]:

    names = random.sample(
        FILE_NAMES,
        k=random.randint(
            5,
            8,
        ),
    )

    return [

        {
            "name":
                name,

            "icon":
                (
                    "markdown"
                    if name.endswith(
                        ".md"
                    )
                    else "description"
                ),

            "modified":
                random.choice(
                    [
                        "Today",
                        "Yesterday",
                        "Sep 4",
                        "Sep 2",
                    ]
                ),
        }

        for name in names
    ]


# ==========================================================
# Main
# ==========================================================

def generate_text_editor_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            TEXT_EDITOR_STATES
        )


    if state not in TEXT_EDITOR_STATES:

        raise ValueError(
            f"Unknown Text Editor state: "
            f"{state}"
        )


    tabs = generate_tabs(
        state
    )


    active_tab = next(
        tab
        for tab in tabs
        if tab[
            "active"
        ]
    )


    if state == "empty_document":

        document_lines = []

    else:

        document_lines = (
            generate_document_lines()
        )


    # ======================================================
    # Find / Replace
    # ======================================================

    find_query = ""

    replace_value = ""


    if state in {
        "find_open",
        "replace_open",
    }:

        find_query = random.choice(
            [
                "project",
                "meeting",
                "task",
                "research",
                "draft",
            ]
        )


    if state == "replace_open":

        replace_value = random.choice(
            [
                "application",
                "updated",
                "completed",
                "reviewed",
            ]
        )


    # ======================================================
    # Split View
    # ======================================================

    split_lines = []

    if state == "split_view":

        split_lines = (
            generate_document_lines(
                minimum=8,
                maximum=16,
            )
        )


    return {

        "state":
            state,

        "tabs":
            tabs,

        "active_tab":
            active_tab,

        "document_lines":
            document_lines,

        "split_lines":
            split_lines,

        "find_query":
            find_query,

        "replace_value":
            replace_value,

        "recent_files":
            generate_recent_files(),

        "document_menu_entries":
            [
                dict(
                    entry
                )
                for entry
                in DOCUMENT_MENU_ENTRIES
            ],

        "open_files":
            generate_open_files(),

        "save_name":
            active_tab[
                "name"
            ],

        "save_location":
            random.choice(
                [
                    "Documents",
                    "Desktop",
                    "Projects",
                ]
            ),
    }