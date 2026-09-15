from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

START_MENU_STATES = [
    "default",
    "all_apps",
    "search_active",
    "recommended_expanded",
    "account_menu",
    "power_menu",
    "folder_open",
]


# ==========================================================
# Pinned Apps
# ==========================================================

PINNED_APP_POOL = [

    {
        "name": "Edge",
        "icon": "public",
    },

    {
        "name": "Mail",
        "icon": "mail",
    },

    {
        "name": "Calendar",
        "icon": "calendar_month",
    },

    {
        "name": "Photos",
        "icon": "photo_library",
    },

    {
        "name": "Settings",
        "icon": "settings",
    },

    {
        "name": "Store",
        "icon": "shopping_bag",
    },

    {
        "name": "Calculator",
        "icon": "calculate",
    },

    {
        "name": "Terminal",
        "icon": "terminal",
    },

    {
        "name": "Notepad",
        "icon": "description",
    },

    {
        "name": "Camera",
        "icon": "photo_camera",
    },

    {
        "name": "Clock",
        "icon": "schedule",
    },

    {
        "name": "Maps",
        "icon": "map",
    },

    {
        "name": "Music",
        "icon": "music_note",
    },

    {
        "name": "Movies",
        "icon": "movie",
    },

    {
        "name": "Teams",
        "icon": "groups",
    },

    {
        "name": "Xbox",
        "icon": "sports_esports",
    },
]


# ==========================================================
# Recommended Items
# ==========================================================

RECOMMENDED_POOL = [

    {
        "name": "Research Notes.docx",
        "subtitle": "2h ago",
        "icon": "description",
    },

    {
        "name": "Presentation.pptx",
        "subtitle": "Yesterday",
        "icon": "slideshow",
    },

    {
        "name": "Dataset",
        "subtitle": "Recently added",
        "icon": "folder",
    },

    {
        "name": "Screenshot.png",
        "subtitle": "3h ago",
        "icon": "image",
    },

    {
        "name": "Meeting Notes.txt",
        "subtitle": "Yesterday",
        "icon": "note",
    },

    {
        "name": "Downloads",
        "subtitle": "Frequently used",
        "icon": "download",
    },
]


# ==========================================================
# All Apps
# ==========================================================

ALL_APPS = [

    {
        "letter": "A",
        "apps": [
            {
                "name": "Alarms & Clock",
                "icon": "schedule",
            },
        ],
    },

    {
        "letter": "C",
        "apps": [
            {
                "name": "Calculator",
                "icon": "calculate",
            },
            {
                "name": "Camera",
                "icon": "photo_camera",
            },
        ],
    },

    {
        "letter": "F",
        "apps": [
            {
                "name": "File Explorer",
                "icon": "folder",
            },
        ],
    },

    {
        "letter": "M",
        "apps": [
            {
                "name": "Mail",
                "icon": "mail",
            },
            {
                "name": "Maps",
                "icon": "map",
            },
            {
                "name": "Microsoft Store",
                "icon": "shopping_bag",
            },
        ],
    },

    {
        "letter": "N",
        "apps": [
            {
                "name": "Notepad",
                "icon": "description",
            },
        ],
    },

    {
        "letter": "P",
        "apps": [
            {
                "name": "Photos",
                "icon": "photo_library",
            },
        ],
    },

    {
        "letter": "S",
        "apps": [
            {
                "name": "Settings",
                "icon": "settings",
            },
        ],
    },

    {
        "letter": "T",
        "apps": [
            {
                "name": "Terminal",
                "icon": "terminal",
            },
        ],
    },
]


# ==========================================================
# Search
# ==========================================================

SEARCH_RESULT_POOL = [

    {
        "name": "Settings",
        "category": "App",
        "icon": "settings",
    },

    {
        "name": "File Explorer",
        "category": "App",
        "icon": "folder",
    },

    {
        "name": "Display settings",
        "category": "System settings",
        "icon": "display_settings",
    },

    {
        "name": "Bluetooth & devices",
        "category": "System settings",
        "icon": "bluetooth",
    },

    {
        "name": "Downloads",
        "category": "Folder",
        "icon": "download",
    },
]


SEARCH_QUERIES = [
    "settings",
    "file",
    "display",
    "bluetooth",
    "downloads",
]


# ==========================================================
# Account Menu
# ==========================================================

ACCOUNT_MENU_ITEMS = [

    {
        "label": "Change account settings",
        "icon": "manage_accounts",
    },

    {
        "label": "Lock",
        "icon": "lock",
    },

    {
        "label": "Sign out",
        "icon": "logout",
    },
]


# ==========================================================
# Power Menu
# ==========================================================

POWER_MENU_ITEMS = [

    {
        "label": "Sleep",
        "icon": "bedtime",
    },

    {
        "label": "Shut down",
        "icon": "power_settings_new",
    },

    {
        "label": "Restart",
        "icon": "restart_alt",
    },
]


# ==========================================================
# Folder Contents
# ==========================================================

FOLDER_APP_POOL = [

    {
        "name": "Word",
        "icon": "description",
    },

    {
        "name": "Excel",
        "icon": "table_chart",
    },

    {
        "name": "PowerPoint",
        "icon": "slideshow",
    },

    {
        "name": "OneNote",
        "icon": "note",
    },
]


# ==========================================================
# Generate Pinned Apps
# ==========================================================

def generate_pinned_apps() -> list[dict]:

    count = random.randint(
        10,
        16,
    )

    selected = random.sample(
        PINNED_APP_POOL,
        k=min(
            count,
            len(PINNED_APP_POOL),
        ),
    )

    return selected


# ==========================================================
# Recommended
# ==========================================================

def generate_recommended_items(
    expanded: bool = False,
) -> list[dict]:

    count = (
        min(
            len(RECOMMENDED_POOL),
            random.randint(5, 6),
        )
        if expanded
        else random.randint(
            3,
            4,
        )
    )

    return random.sample(
        RECOMMENDED_POOL,
        k=count,
    )


# ==========================================================
# Search Results
# ==========================================================

def generate_search_results() -> dict:

    query = random.choice(
        SEARCH_QUERIES
    )

    count = random.randint(
        3,
        min(
            5,
            len(SEARCH_RESULT_POOL),
        ),
    )

    return {

        "query":
            query,

        "results":
            random.sample(
                SEARCH_RESULT_POOL,
                k=count,
            ),
    }


# ==========================================================
# Generator
# ==========================================================

def generate_start_menu_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            START_MENU_STATES
        )


    if state not in START_MENU_STATES:

        raise ValueError(
            f"Unknown Start menu state: {state}"
        )


    search = (
        generate_search_results()
        if state == "search_active"
        else {
            "query": "",
            "results": [],
        }
    )


    return {

        "state":
            state,

        "pinned_apps":
            generate_pinned_apps(),

        "recommended":
            generate_recommended_items(
                expanded=(
                    state
                    == "recommended_expanded"
                )
            ),

        "all_apps":
            ALL_APPS,

        "search":
            search,

        "profile": {
            "name":
                random.choice(
                    [
                        "Shweta",
                        "Alex",
                        "Jordan",
                        "Taylor",
                        "Sam",
                    ]
                ),

            "initial":
                random.choice(
                    [
                        "S",
                        "A",
                        "J",
                        "T",
                    ]
                ),
        },

        "account_menu":
            (
                ACCOUNT_MENU_ITEMS
                if state
                == "account_menu"
                else []
            ),

        "power_menu":
            (
                POWER_MENU_ITEMS
                if state
                == "power_menu"
                else []
            ),

        "folder": {
            "name":
                "Productivity",

            "apps":
                FOLDER_APP_POOL,
        } if state == "folder_open"
        else None,
    }