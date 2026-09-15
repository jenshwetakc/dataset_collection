from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

FILES_STATES = [

    "browse",

    "recents",

    "shared",

    "folder_open",

    "search_active",

    "file_preview",

    "context_menu",

    "move_sheet",
]


FILES_STATE_WEIGHTS = [

    22,

    14,

    10,

    16,

    12,

    10,

    8,

    8,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# File Types
# ==========================================================

FILE_TYPES = [

    {
        "extension": "pdf",
        "icon": "file-text",
        "style": "red",
    },

    {
        "extension": "docx",
        "icon": "file-text",
        "style": "blue",
    },

    {
        "extension": "pptx",
        "icon": "presentation",
        "style": "orange",
    },

    {
        "extension": "xlsx",
        "icon": "sheet",
        "style": "green",
    },

    {
        "extension": "png",
        "icon": "image",
        "style": "purple",
    },

    {
        "extension": "jpg",
        "icon": "image",
        "style": "purple",
    },

    {
        "extension": "zip",
        "icon": "archive",
        "style": "gray",
    },

    {
        "extension": "txt",
        "icon": "file-text",
        "style": "gray",
    },
]


# ==========================================================
# File
# ==========================================================

def generate_file(
    index: int,
) -> dict:

    file_type = random.choice(
        FILE_TYPES
    )


    names = [

        "Research Notes",

        "Experiment Results",

        "Presentation",

        "Dataset Summary",

        "Meeting Notes",

        "Screenshots",

        "Project Plan",

        "Report Draft",

        "References",

        "Evaluation",

        "Weekly Update",

        "Implementation Notes",
    ]


    return {

        "id":
            f"file_{index}",

        "name":
            random.choice(
                names
            ),

        "extension":
            file_type["extension"],

        "display_name":
            (
                f"{random.choice(names)}."
                f"{file_type['extension']}"
            ),

        "icon":
            get_lucide_icon(
                file_type["icon"]
            ),

        "style":
            file_type["style"],

        "size":
            random.choice([
                "84 KB",
                "215 KB",
                "1.2 MB",
                "3.8 MB",
                "12.4 MB",
                "48 MB",
            ]),

        "modified":
            random.choice([
                "Today",
                "Yesterday",
                "Sep 3",
                "Aug 30",
                "Aug 24",
            ]),

        "shared":
            random.random() < 0.22,

        "downloaded":
            random.random() < 0.72,

        "favorite":
            random.random() < 0.18,
    }


# ==========================================================
# Folder
# ==========================================================

def generate_folder(
    index: int,
) -> dict:

    titles = [

        "Research",

        "Documents",

        "Downloads",

        "Projects",

        "Screenshots",

        "Presentations",

        "Shared",

        "Archive",
    ]


    return {

        "id":
            f"folder_{index}",

        "title":
            random.choice(
                titles
            ),

        "count":
            random.randint(
                3,
                38,
            ),

        "shared":
            random.random() < 0.18,

        "favorite":
            random.random() < 0.15,

        "icon":
            get_lucide_icon(
                "folder"
            ),
    }


# ==========================================================
# Locations
# ==========================================================

def generate_locations() -> list[dict]:

    return [

        {
            "id": "icloud",
            "title": "iCloud Drive",
            "icon": get_lucide_icon(
                "cloud"
            ),
        },

        {
            "id": "on_my_iphone",
            "title": "On My iPhone",
            "icon": get_lucide_icon(
                "smartphone"
            ),
        },

        {
            "id": "downloads",
            "title": "Downloads",
            "icon": get_lucide_icon(
                "download"
            ),
        },

        {
            "id": "recently_deleted",
            "title": "Recently Deleted",
            "icon": get_lucide_icon(
                "trash-2"
            ),
        },
    ]


# ==========================================================
# Tags
# ==========================================================

def generate_tags() -> list[dict]:

    return [

        {
            "id": "red",
            "title": "Red",
            "color": "#FF453A",
        },

        {
            "id": "orange",
            "title": "Orange",
            "color": "#FF9F0A",
        },

        {
            "id": "green",
            "title": "Green",
            "color": "#30D158",
        },

        {
            "id": "blue",
            "title": "Blue",
            "color": "#0A84FF",
        },

        {
            "id": "purple",
            "title": "Purple",
            "color": "#BF5AF2",
        },
    ]


# ==========================================================
# Search
# ==========================================================

def generate_search_data(
    files: list[dict],
) -> dict:

    query = random.choice([

        "research",

        "report",

        "presentation",

        "notes",

        "project",
    ])


    results = [

        file

        for file
        in files

        if query.lower()
        in file["display_name"].lower()
    ]


    if not results:

        results = random.sample(

            files,

            k=min(
                6,
                len(
                    files
                ),
            ),
        )


    return {

        "query":
            query,

        "results":
            results,
    }


# ==========================================================
# Context Menu
# ==========================================================

def generate_context_menu() -> dict:

    return {

        "actions": [

            {
                "id": "open",
                "title": "Open",
                "icon": get_lucide_icon(
                    "external-link"
                ),
                "destructive": False,
            },

            {
                "id": "rename",
                "title": "Rename",
                "icon": get_lucide_icon(
                    "pencil"
                ),
                "destructive": False,
            },

            {
                "id": "move",
                "title": "Move",
                "icon": get_lucide_icon(
                    "folder-input"
                ),
                "destructive": False,
            },

            {
                "id": "duplicate",
                "title": "Duplicate",
                "icon": get_lucide_icon(
                    "copy"
                ),
                "destructive": False,
            },

            {
                "id": "share",
                "title": "Share",
                "icon": resolve_icon(
                    "share",
                    "share"
                ),
                "destructive": False,
            },

            {
                "id": "delete",
                "title": "Delete",
                "icon": get_lucide_icon(
                    "trash-2"
                ),
                "destructive": True,
            },
        ],
    }


# ==========================================================
# Move Destinations
# ==========================================================

def generate_move_destinations() -> list[dict]:

    return [

        {
            "id": "icloud_drive",
            "title": "iCloud Drive",
            "icon": get_lucide_icon(
                "cloud"
            ),
        },

        {
            "id": "documents",
            "title": "Documents",
            "icon": get_lucide_icon(
                "folder"
            ),
        },

        {
            "id": "downloads",
            "title": "Downloads",
            "icon": get_lucide_icon(
                "folder"
            ),
        },

        {
            "id": "research",
            "title": "Research",
            "icon": get_lucide_icon(
                "folder"
            ),
        },

        {
            "id": "projects",
            "title": "Projects",
            "icon": get_lucide_icon(
                "folder"
            ),
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_files_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            FILES_STATES,

            weights=
                FILES_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in FILES_STATES:

        raise ValueError(
            f"Unknown Files state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Files
    # ======================================================

    files = [

        generate_file(
            index
        )

        for index
        in range(
            16
        )
    ]


    folders = [

        generate_folder(
            index
        )

        for index
        in range(
            6
        )
    ]


    active_file = random.choice(
        files
    )


    active_folder = random.choice(
        folders
    )


    folder_files = random.sample(

        files,

        k=min(
            random.randint(
                7,
                12,
            ),
            len(
                files
            ),
        ),
    )


    shared_files = [

        file
        for file
        in files
        if file["shared"]
    ]


    if not shared_files:

        shared_files = files[:4]


    # ======================================================
    # Overlay
    # ======================================================

    is_overlay_state = (
        state
        in {
            "context_menu",
            "move_sheet",
        }
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "title":
            "Files",


        "files":
            files,

        "folders":
            folders,

        "locations":
            generate_locations(),

        "tags":
            generate_tags(),


        "active_file":
            active_file,

        "active_folder":
            active_folder,

        "folder_files":
            folder_files,

        "shared_files":
            shared_files,


        "search":
            generate_search_data(
                files
            ),


        "context_menu":
            generate_context_menu(),


        "move_destinations":
            generate_move_destinations(),


        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis"
                ),

            "back":
                resolve_icon(
                    "back"
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "folder":
                get_lucide_icon(
                    "folder"
                ),

            "folder_plus":
                get_lucide_icon(
                    "folder-plus"
                ),

            "cloud":
                get_lucide_icon(
                    "cloud"
                ),

            "download":
                get_lucide_icon(
                    "download"
                ),

            "share":
                resolve_icon(
                    "share",
                    "share"
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "grid":
                get_lucide_icon(
                    "grid-2x2"
                ),

            "list":
                get_lucide_icon(
                    "list"
                ),

            "info":
                resolve_icon(
                    "info"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in FILES_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_files_data(
                state=
                    state
            ),

            sort_dicts=False,
        )