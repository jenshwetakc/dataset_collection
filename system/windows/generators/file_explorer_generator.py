from __future__ import annotations

import random


# ==========================================================
# Explorer States
# ==========================================================

FILE_EXPLORER_STATES = [
    "home",
    "folder_grid",
    "details_view",
    "selected_file",
    "multi_select",
    "rename",
    "search_results",
    "context_menu",
    "empty_folder",
    "copy_progress",
    "properties_dialog",
]


# ==========================================================
# Locations
# ==========================================================

LOCATION_POOL = [
    {
        "name": "Home",
        "icon": "home",
    },
    {
        "name": "Desktop",
        "icon": "desktop_windows",
    },
    {
        "name": "Documents",
        "icon": "description",
    },
    {
        "name": "Downloads",
        "icon": "download",
    },
    {
        "name": "Pictures",
        "icon": "image",
    },
    {
        "name": "Music",
        "icon": "music_note",
    },
    {
        "name": "Videos",
        "icon": "movie",
    },
]


# ==========================================================
# File / Folder Pool
# ==========================================================

ITEM_POOL = [
    {
        "name": "Research",
        "type": "File folder",
        "icon": "folder",
        "kind": "folder",
        "size": "",
    },
    {
        "name": "Projects",
        "type": "File folder",
        "icon": "folder",
        "kind": "folder",
        "size": "",
    },
    {
        "name": "Dataset",
        "type": "File folder",
        "icon": "folder",
        "kind": "folder",
        "size": "",
    },
    {
        "name": "Screenshots",
        "type": "File folder",
        "icon": "folder",
        "kind": "folder",
        "size": "",
    },
    {
        "name": "Thesis.docx",
        "type": "Microsoft Word Document",
        "icon": "description",
        "kind": "document",
        "size": "2.4 MB",
    },
    {
        "name": "Presentation.pptx",
        "type": "Microsoft PowerPoint Presentation",
        "icon": "slideshow",
        "kind": "document",
        "size": "8.7 MB",
    },
    {
        "name": "Results.xlsx",
        "type": "Microsoft Excel Worksheet",
        "icon": "table_chart",
        "kind": "document",
        "size": "1.2 MB",
    },
    {
        "name": "architecture.pdf",
        "type": "PDF File",
        "icon": "picture_as_pdf",
        "kind": "document",
        "size": "6.3 MB",
    },
    {
        "name": "notes.txt",
        "type": "Text Document",
        "icon": "note",
        "kind": "document",
        "size": "18 KB",
    },
    {
        "name": "screenshot_01.png",
        "type": "PNG File",
        "icon": "image",
        "kind": "image",
        "size": "1.8 MB",
    },
    {
        "name": "photo.jpg",
        "type": "JPEG File",
        "icon": "image",
        "kind": "image",
        "size": "3.5 MB",
    },
    {
        "name": "demo.mp4",
        "type": "MP4 Video",
        "icon": "movie",
        "kind": "video",
        "size": "24.2 MB",
    },
]


# ==========================================================
# Quick Access
# ==========================================================

QUICK_ACCESS_POOL = [
    {
        "name": "Desktop",
        "icon": "desktop_windows",
    },
    {
        "name": "Downloads",
        "icon": "download",
    },
    {
        "name": "Documents",
        "icon": "description",
    },
    {
        "name": "Pictures",
        "icon": "image",
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
        "label": "Open with",
        "icon": "apps",
    },
    {
        "divider": True,
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
        "label": "Share",
        "icon": "share",
    },
    {
        "label": "Delete",
        "icon": "delete",
    },
    {
        "divider": True,
    },
    {
        "label": "Properties",
        "icon": "info",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_modified_date() -> str:

    return random.choice(
        [
            "9/5/2026 3:42 PM",
            "9/5/2026 10:18 AM",
            "9/4/2026 7:32 PM",
            "9/3/2026 11:08 AM",
            "8/31/2026 4:21 PM",
            "8/28/2026 9:05 AM",
        ]
    )


def generate_items(
    minimum: int = 6,
    maximum: int = 11,
) -> list[dict]:

    count = random.randint(
        minimum,
        min(
            maximum,
            len(ITEM_POOL),
        ),
    )

    items = random.sample(
        ITEM_POOL,
        k=count,
    )

    result = []

    for item in items:

        result.append(
            {
                **item,

                "modified":
                    generate_modified_date(),

                "selected":
                    False,

                "renaming":
                    False,
            }
        )

    return result


# ==========================================================
# Selection
# ==========================================================

def apply_single_selection(
    items: list[dict],
) -> int | None:

    if not items:
        return None

    index = random.randrange(
        len(items)
    )

    items[index]["selected"] = True

    return index


def apply_multi_selection(
    items: list[dict],
) -> list[int]:

    if len(items) < 2:
        return []

    count = random.randint(
        2,
        min(
            4,
            len(items),
        ),
    )

    indices = random.sample(
        range(
            len(items)
        ),
        k=count,
    )

    for index in indices:

        items[index]["selected"] = True

    return indices


# ==========================================================
# Search
# ==========================================================

def generate_search_data() -> dict:

    query = random.choice(
        [
            "report",
            "project",
            "image",
            "notes",
            "presentation",
        ]
    )

    items = generate_items(
        minimum=3,
        maximum=6,
    )

    return {
        "query": query,
        "results": items,
    }


# ==========================================================
# Copy Progress
# ==========================================================

def generate_copy_progress() -> dict:

    progress = random.randint(
        12,
        92,
    )

    total = random.choice(
        [
            18,
            32,
            47,
            81,
            126,
        ]
    )

    copied = max(
        1,
        round(
            total
            * progress
            / 100
        ),
    )

    return {
        "progress": progress,
        "total_items": total,
        "copied_items": copied,
        "speed": random.choice(
            [
                "12.8 MB/s",
                "25.4 MB/s",
                "48.1 MB/s",
                "76.5 MB/s",
            ]
        ),
        "source": random.choice(
            [
                "Downloads",
                "Pictures",
                "Research",
            ]
        ),
        "destination": random.choice(
            [
                "Documents",
                "Projects",
                "Desktop",
            ]
        ),
    }


# ==========================================================
# Properties
# ==========================================================

def generate_properties(
    item: dict,
) -> dict:

    return {
        "name":
            item["name"],

        "icon":
            item["icon"],

        "type":
            item["type"],

        "location":
            random.choice(
                [
                    "C:\\Users\\User\\Documents",
                    "C:\\Users\\User\\Downloads",
                    "C:\\Users\\User\\Desktop",
                ]
            ),

        "size":
            item["size"]
            or random.choice(
                [
                    "42.3 MB",
                    "128 MB",
                    "680 MB",
                ]
            ),

        "created":
            "August 28, 2026, 10:22 AM",

        "modified":
            "September 5, 2026, 3:42 PM",

        "read_only":
            random.random() < 0.25,

        "hidden":
            random.random() < 0.08,
    }


# ==========================================================
# File Explorer Generator
# ==========================================================

def generate_file_explorer_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            FILE_EXPLORER_STATES
        )


    if state not in FILE_EXPLORER_STATES:

        raise ValueError(
            f"Unknown File Explorer state: {state}"
        )


    location = random.choice(
        LOCATION_POOL
    )


    items = generate_items()


    selected_index = None

    selected_indices = []


    if state in {
        "selected_file",
        "context_menu",
        "properties_dialog",
    }:

        selected_index = (
            apply_single_selection(
                items
            )
        )


    elif state == "multi_select":

        selected_indices = (
            apply_multi_selection(
                items
            )
        )


    elif state == "rename":

        selected_index = (
            apply_single_selection(
                items
            )
        )

        if selected_index is not None:

            items[
                selected_index
            ]["renaming"] = True


    search = (
        generate_search_data()
        if state == "search_results"
        else {
            "query": "",
            "results": [],
        }
    )


    if state == "search_results":

        visible_items = (
            search["results"]
        )

    elif state == "empty_folder":

        visible_items = []

    else:

        visible_items = items


    selected_item = None

    if selected_index is not None:

        selected_item = (
            items[
                selected_index
            ]
        )


    return {

        "state":
            state,

        "window_mode":
            random.choice(
                [
                    "maximized",
                    "maximized",
                    "windowed",
                ]
            ),

        "location":
            location,

        "breadcrumbs": [
            {
                "name": "This PC",
            },
            {
                "name": location["name"],
            },
        ],

        "sidebar": {
            "quick_access":
                QUICK_ACCESS_POOL,

            "locations":
                LOCATION_POOL,
        },

        "view_mode":
            (
                "details"
                if state
                in {
                    "details_view",
                    "selected_file",
                    "multi_select",
                    "rename",
                    "context_menu",
                    "search_results",
                }
                else "grid"
            ),

        "items":
            visible_items,

        "selected_item":
            selected_item,

        "selected_indices":
            selected_indices,

        "search":
            search,

        "context_menu":
            (
                CONTEXT_MENU_ITEMS
                if state
                == "context_menu"
                else []
            ),

        "copy_progress":
            (
                generate_copy_progress()
                if state
                == "copy_progress"
                else None
            ),

        "properties":
            (
                generate_properties(
                    selected_item
                )
                if (
                    state
                    == "properties_dialog"
                    and selected_item
                    is not None
                )
                else None
            ),
    }