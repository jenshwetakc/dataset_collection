from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

FILES_STATES = [

    "home_grid",

    "home_list",

    "documents_grid",

    "downloads_list",

    "recent",

    "starred",

    "trash",

    "item_selected",

    "multiple_selected",

    "search_open",

    "search_results",

    "context_menu_open",

    "rename_open",

    "properties_dialog",

    "delete_dialog",

    "new_folder_dialog",

    "sidebar_collapsed",
]


# ==========================================================
# Sidebar
# ==========================================================

SIDEBAR_ITEMS = [

    {
        "label": "Recent",
        "icon": "schedule",
        "location": "recent",
    },

    {
        "label": "Starred",
        "icon": "star",
        "location": "starred",
    },

    {
        "label": "Home",
        "icon": "home",
        "location": "home",
    },

    {
        "label": "Desktop",
        "icon": "desktop_windows",
        "location": "desktop",
    },

    {
        "label": "Documents",
        "icon": "description",
        "location": "documents",
    },

    {
        "label": "Downloads",
        "icon": "download",
        "location": "downloads",
    },

    {
        "label": "Music",
        "icon": "music_note",
        "location": "music",
    },

    {
        "label": "Pictures",
        "icon": "image",
        "location": "pictures",
    },

    {
        "label": "Videos",
        "icon": "movie",
        "location": "videos",
    },

    {
        "label": "Trash",
        "icon": "delete",
        "location": "trash",
    },
]


# ==========================================================
# Folder Names
# ==========================================================

FOLDER_NAMES = [
    "Desktop",
    "Documents",
    "Downloads",
    "Music",
    "Pictures",
    "Projects",
    "Public",
    "Templates",
    "Videos",
    "Research",
    "Screenshots",
    "Archive",
]


# ==========================================================
# Files
# ==========================================================

FILE_DEFINITIONS = [

    {
        "extension": ".pdf",
        "icon": "picture_as_pdf",
        "kind": "PDF document",
    },

    {
        "extension": ".txt",
        "icon": "description",
        "kind": "Plain text document",
    },

    {
        "extension": ".docx",
        "icon": "article",
        "kind": "Document",
    },

    {
        "extension": ".pptx",
        "icon": "slideshow",
        "kind": "Presentation",
    },

    {
        "extension": ".xlsx",
        "icon": "table_chart",
        "kind": "Spreadsheet",
    },

    {
        "extension": ".png",
        "icon": "image",
        "kind": "PNG image",
    },

    {
        "extension": ".jpg",
        "icon": "image",
        "kind": "JPEG image",
    },

    {
        "extension": ".zip",
        "icon": "folder_zip",
        "kind": "Archive",
    },

    {
        "extension": ".py",
        "icon": "code",
        "kind": "Python source",
    },
]


# ==========================================================
# Context Menu
# ==========================================================

CONTEXT_MENU_ITEMS = [

    {
        "label": "Open",
        "icon": "open_in_new",
    },

    {
        "label": "Open With",
        "icon": "apps",
    },

    {
        "label": "Cut",
        "icon": "content_cut",
    },

    {
        "label": "Copy",
        "icon": "content_copy",
    },

    {
        "label": "Rename",
        "icon": "edit",
    },

    {
        "label": "Move to Trash",
        "icon": "delete",
    },

    {
        "label": "Properties",
        "icon": "info",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_modified_text() -> str:

    value = (
        datetime.now()
        - timedelta(
            days=random.randint(
                0,
                120,
            ),
            hours=random.randint(
                0,
                23,
            ),
        )
    )

    if value.date() == datetime.now().date():

        return value.strftime(
            "Today %H:%M"
        )

    return value.strftime(
        "%b %d"
    )


def generate_size() -> str:

    kind = random.choice(
        [
            "KB",
            "MB",
            "GB",
        ]
    )

    if kind == "KB":

        value = random.randint(
            8,
            900,
        )

    elif kind == "MB":

        value = round(
            random.uniform(
                1,
                900,
            ),
            1,
        )

    else:

        value = round(
            random.uniform(
                1,
                8,
            ),
            1,
        )

    return (
        f"{value} {kind}"
    )


def generate_file_name(
    extension: str,
) -> str:

    stems = [
        "report",
        "notes",
        "meeting",
        "presentation",
        "dataset",
        "budget",
        "results",
        "analysis",
        "design",
        "project",
        "paper",
        "summary",
        "draft",
        "schedule",
        "figure",
    ]

    return (
        random.choice(
            stems
        )
        + (
            f"_{random.randint(1, 99)}"
            if random.random() < 0.45
            else ""
        )
        + extension
    )


# ==========================================================
# Generate One Item
# ==========================================================

def generate_folder(
    index: int,
) -> dict:

    return {

        "id":
            f"folder_{index}",

        "name":
            random.choice(
                FOLDER_NAMES
            ),

        "type":
            "folder",

        "kind":
            "Folder",

        "icon":
            "folder",

        "size":
            "—",

        "modified":
            generate_modified_text(),

        "starred":
            random.random() < 0.14,

        "selected":
            False,
    }


def generate_file(
    index: int,
) -> dict:

    definition = random.choice(
        FILE_DEFINITIONS
    )

    return {

        "id":
            f"file_{index}",

        "name":
            generate_file_name(
                definition[
                    "extension"
                ]
            ),

        "type":
            "file",

        "kind":
            definition[
                "kind"
            ],

        "icon":
            definition[
                "icon"
            ],

        "size":
            generate_size(),

        "modified":
            generate_modified_text(),

        "starred":
            random.random() < 0.16,

        "selected":
            False,
    }


# ==========================================================
# Item Collection
# ==========================================================

def generate_items(
    minimum: int = 10,
    maximum: int = 22,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    folder_count = random.randint(
        3,
        min(
            7,
            count,
        ),
    )

    items = []

    for index in range(
        folder_count
    ):

        items.append(
            generate_folder(
                index
            )
        )

    for index in range(
        count
        - folder_count
    ):

        items.append(
            generate_file(
                index
            )
        )

    return items


# ==========================================================
# State Resolver
# ==========================================================

def resolve_location(
    state: str,
) -> str:

    if state == "documents_grid":
        return "documents"

    if state == "downloads_list":
        return "downloads"

    if state == "recent":
        return "recent"

    if state == "starred":
        return "starred"

    if state == "trash":
        return "trash"

    return "home"


def resolve_view_mode(
    state: str,
) -> str:

    if state in {
        "home_list",
        "downloads_list",
        "recent",
        "starred",
        "trash",
        "search_results",
    }:

        return "list"

    return "grid"


# ==========================================================
# Main Generator
# ==========================================================

def generate_files_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            FILES_STATES
        )


    if state not in FILES_STATES:

        raise ValueError(
            f"Unknown Files state: "
            f"{state}"
        )


    location = resolve_location(
        state
    )


    view_mode = resolve_view_mode(
        state
    )


    items = generate_items()


    # ======================================================
    # Starred State
    # ======================================================

    if state == "starred":

        for item in items:

            item["starred"] = (
                random.random()
                < 0.75
            )

        items = [
            item
            for item in items
            if item["starred"]
        ]


    # ======================================================
    # Trash
    # ======================================================

    if state == "trash":

        items = [

            generate_file(
                index
            )

            for index in range(
                random.randint(
                    4,
                    12,
                )
            )
        ]


    # ======================================================
    # Selection
    # ======================================================

    selected_ids = []


    if state in {
        "item_selected",
        "context_menu_open",
        "rename_open",
        "properties_dialog",
        "delete_dialog",
    }:

        selected_item = random.choice(
            items
        )

        selected_item[
            "selected"
        ] = True

        selected_ids = [
            selected_item[
                "id"
            ]
        ]


    elif state == "multiple_selected":

        selected_items = random.sample(

            items,

            k=min(
                random.randint(
                    2,
                    5,
                ),
                len(
                    items
                ),
            ),
        )

        for item in selected_items:

            item[
                "selected"
            ] = True

            selected_ids.append(
                item[
                    "id"
                ]
            )


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    if state in {
        "search_open",
        "search_results",
    }:

        search_query = random.choice(
            [
                "report",
                "project",
                "image",
                "notes",
                "presentation",
            ]
        )


    if state == "search_results":

        result_count = random.randint(
            4,
            min(
                10,
                len(
                    items
                ),
            ),
        )

        items = random.sample(
            items,
            k=result_count,
        )


    # ======================================================
    # Current Item
    # ======================================================

    selected_item = next(
        (
            item
            for item in items
            if item[
                "selected"
            ]
        ),
        None,
    )


    if (
        selected_item is None
        and state in {
            "rename_open",
            "properties_dialog",
            "delete_dialog",
            "context_menu_open",
        }
    ):

        selected_item = random.choice(
            items
        )

        selected_item[
            "selected"
        ] = True

        selected_ids = [
            selected_item[
                "id"
            ]
        ]


    # ======================================================
    # Sidebar
    # ======================================================

    sidebar_items = [
        dict(
            item
        )
        for item in SIDEBAR_ITEMS
    ]

    for item in sidebar_items:

        item[
            "active"
        ] = (
            item[
                "location"
            ]
            == location
        )


    # ======================================================
    # Location Title
    # ======================================================

    location_titles = {

        "home":
            "Home",

        "documents":
            "Documents",

        "downloads":
            "Downloads",

        "recent":
            "Recent",

        "starred":
            "Starred",

        "trash":
            "Trash",
    }


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "location":
            location,

        "location_title":
            location_titles[
                location
            ],

        "view_mode":
            view_mode,

        "sidebar_collapsed":
            state
            == "sidebar_collapsed",

        "search_visible":
            state
            in {
                "search_open",
                "search_results",
            },

        "search_query":
            search_query,

        "items":
            items,

        "selected_ids":
            selected_ids,

        "selected_count":
            len(
                selected_ids
            ),

        "selected_item":
            selected_item,

        "context_menu_items":
            [
                dict(
                    item
                )
                for item in CONTEXT_MENU_ITEMS
            ],

        "new_folder_name":
            random.choice(
                [
                    "New Folder",
                    "Research",
                    "Project Files",
                    "Archive",
                ]
            ),

        "rename_value":
            (
                selected_item[
                    "name"
                ]
                if selected_item
                else ""
            ),

        "user_name":
            fake.first_name(),

        "computer_name":
            fake.user_name(),
    }