from __future__ import annotations

import random
from pathlib import Path

from common.media_generator import (
    get_random_image,
)


# ==========================================================
# Paths
# ==========================================================

ANDROID_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

IMAGE_DIR = (
    ANDROID_ROOT
    / "assets"
    / "file_picker"
    / "images"
)


# ==========================================================
# File Pools
# ==========================================================

FILE_POOL = [

    {
        "name": "Project proposal.pdf",
        "type": "pdf",
        "icon": "mdi:file-pdf-box",
        "size": "2.4 MB",
    },

    {
        "name": "Meeting notes.docx",
        "type": "document",
        "icon": "mdi:file-word-outline",
        "size": "824 KB",
    },

    {
        "name": "Budget.xlsx",
        "type": "spreadsheet",
        "icon": "mdi:file-excel-outline",
        "size": "1.1 MB",
    },

    {
        "name": "Presentation.pptx",
        "type": "presentation",
        "icon": "mdi:file-powerpoint-outline",
        "size": "4.6 MB",
    },

    {
        "name": "archive.zip",
        "type": "archive",
        "icon": "mdi:folder-zip-outline",
        "size": "17 MB",
    },

    {
        "name": "voice_note.m4a",
        "type": "audio",
        "icon": "mdi:file-music-outline",
        "size": "3.7 MB",
    },

    {
        "name": "README.txt",
        "type": "text",
        "icon": "mdi:file-document-outline",
        "size": "18 KB",
    },

    {
        "name": "invoice.pdf",
        "type": "pdf",
        "icon": "mdi:file-pdf-box",
        "size": "696 KB",
    },

    {
        "name": "research_notes.txt",
        "type": "text",
        "icon": "mdi:file-document-outline",
        "size": "42 KB",
    },

    {
        "name": "dataset.csv",
        "type": "spreadsheet",
        "icon": "mdi:file-delimited-outline",
        "size": "8.3 MB",
    },
]


FOLDERS = [
    {
        "name": "Documents",
        "icon": "mdi:folder-outline",
    },
    {
        "name": "Downloads",
        "icon": "mdi:folder-download-outline",
    },
    {
        "name": "Screenshots",
        "icon": "mdi:folder-image",
    },
    {
        "name": "Projects",
        "icon": "mdi:folder-code-outline",
    },
]


LOCATIONS = [
    {
        "semantic": "recent",
        "label": "Recent",
        "icon": "mdi:history",
    },
    {
        "semantic": "images",
        "label": "Images",
        "icon": "mdi:image-multiple-outline",
    },
    {
        "semantic": "downloads",
        "label": "Downloads",
        "icon": "mdi:download-outline",
    },
    {
        "semantic": "documents",
        "label": "Documents",
        "icon": "mdi:file-document-outline",
    },
    {
        "semantic": "device",
        "label": "This device",
        "icon": "mdi:cellphone",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def get_random_image_asset() -> str | None:

    if not IMAGE_DIR.exists():
        return None

    try:

        return get_random_image(
            IMAGE_DIR
        )

    except Exception:

        return None


# ==========================================================
# Item Builders
# ==========================================================

def build_file(
    source: dict,
    index: int,
) -> dict:

    modified = random.choice([
        "Today",
        "Yesterday",
        "Sep 5",
        "Sep 3",
        "Aug 29",
        "Aug 21",
    ])

    return {

        "semantic":
            f"file_{index}",

        "name":
            source["name"],

        "type":
            source["type"],

        "icon":
            source["icon"],

        "size":
            source["size"],

        "modified":
            modified,

        "selected":
            False,

        "thumbnail":
            None,
    }


def build_image_file(
    index: int,
) -> dict:

    return {

        "semantic":
            f"image_file_{index}",

        "name":
            random.choice([
                "IMG_2026.jpg",
                "Screenshot.png",
                "Camera_001.jpg",
                "Photo.jpg",
                "Wallpaper.png",
            ]),

        "type":
            "image",

        "icon":
            "mdi:image-outline",

        "size":
            random.choice([
                "1.2 MB",
                "2.8 MB",
                "4.1 MB",
                "860 KB",
            ]),

        "modified":
            random.choice([
                "Today",
                "Yesterday",
                "Sep 4",
                "Aug 31",
            ]),

        "selected":
            False,

        "thumbnail":
            get_random_image_asset(),
    }


def build_folder(
    source: dict,
    index: int,
) -> dict:

    return {

        "semantic":
            f"folder_{index}",

        "name":
            source["name"],

        "type":
            "folder",

        "icon":
            source["icon"],

        "size":
            "",

        "modified":
            random.choice([
                "Today",
                "Yesterday",
                "Sep 1",
                "Aug 25",
            ]),

        "selected":
            False,

        "thumbnail":
            None,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_file_picker_data() -> dict:

    # ======================================================
    # Main State
    # ======================================================

    picker_state = random.choices(
        [
            "normal",
            "search",
            "search_results",
            "multi_select",
            "drawer_open",
            "sort_menu",
            "empty",
            "no_results",
        ],
        weights=[
            0.30,
            0.10,
            0.14,
            0.14,
            0.10,
            0.08,
            0.07,
            0.07,
        ],
        k=1,
    )[0]


    # ======================================================
    # Location
    # ======================================================

    location = random.choice(
        LOCATIONS
    )


    # ======================================================
    # View
    # ======================================================

    view_mode = random.choice([
        "grid",
        "list",
    ])


    # ======================================================
    # Selection Mode
    # ======================================================

    selection_mode = random.choice([
        "single",
        "multiple",
    ])

    if picker_state == "multi_select":
        selection_mode = "multiple"


    # ======================================================
    # Sort
    # ======================================================

    sort_by = random.choice([
        "Name",
        "Date modified",
        "Size",
    ])


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    if picker_state in {
        "search",
        "search_results",
        "no_results",
    }:

        search_query = random.choice([
            "report",
            "photo",
            "pdf",
            "project",
            "notes",
        ])


    # ======================================================
    # Build Items
    # ======================================================

    items = []

    if picker_state not in {
        "empty",
        "no_results",
    }:

        folder_count = random.randint(
            1,
            3,
        )

        selected_folders = random.sample(
            FOLDERS,
            folder_count,
        )

        for index, folder in enumerate(
            selected_folders
        ):

            items.append(
                build_folder(
                    folder,
                    index,
                )
            )


        file_count = random.randint(
            6,
            12,
        )

        selected_files = random.sample(
            FILE_POOL,
            min(
                file_count,
                len(
                    FILE_POOL
                ),
            ),
        )

        base_index = len(items)

        for offset, source in enumerate(
            selected_files
        ):

            items.append(
                build_file(
                    source,
                    base_index + offset,
                )
            )


        image_count = random.randint(
            2,
            5,
        )

        for image_index in range(
            image_count
        ):

            items.append(
                build_image_file(
                    len(items)
                )
            )


    # ======================================================
    # Search Filtering
    # ======================================================

    if picker_state == "search_results":

        query = search_query.lower()

        filtered = [
            item
            for item in items
            if (
                query
                in item["name"].lower()
                or query
                in item["type"].lower()
            )
        ]

        if filtered:

            items = filtered

        else:

            items = random.sample(
                items,
                min(
                    3,
                    len(items),
                ),
            )


    # ======================================================
    # Multi Selection
    # ======================================================

    selected_count = 0

    if (
        picker_state == "multi_select"
        and items
    ):

        selectable = [
            item
            for item in items
            if item["type"]
            != "folder"
        ]

        if selectable:

            count = random.randint(
                1,
                min(
                    4,
                    len(selectable),
                ),
            )

            selected_items = random.sample(
                selectable,
                count,
            )

            selected_semantics = {
                item["semantic"]
                for item in selected_items
            }

            for item in items:

                if (
                    item["semantic"]
                    in selected_semantics
                ):

                    item["selected"] = True

            selected_count = count


    # ======================================================
    # Filter
    # ======================================================

    file_filter = random.choice([
        "All files",
        "Images",
        "Documents",
        "PDFs",
    ])


    # ======================================================
    # Storage
    # ======================================================

    storage_used = random.randint(
        24,
        112,
    )

    storage_total = random.choice([
        128,
        256,
        512,
    ])

    storage_percentage = min(
        100,
        int(
            storage_used
            / storage_total
            * 100
        ),
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "picker_state":
            picker_state,

        "location":
            location,

        "view_mode":
            view_mode,

        "selection_mode":
            selection_mode,

        "selected_count":
            selected_count,

        "sort_by":
            sort_by,

        "search_query":
            search_query,

        "file_filter":
            file_filter,

        "items":
            items,

        "locations":
            LOCATIONS,

        "storage_used":
            storage_used,

        "storage_total":
            storage_total,

        "storage_percentage":
            storage_percentage,

        "show_search":
            picker_state
            in {
                "search",
                "search_results",
                "no_results",
            },

        "drawer_open":
            picker_state
            == "drawer_open",

        "sort_menu_open":
            picker_state
            == "sort_menu",
    }