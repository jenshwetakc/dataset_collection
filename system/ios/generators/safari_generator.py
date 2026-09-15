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

SAFARI_STATES = [

    "start_page",

    "webpage",

    "tab_overview",

    "reader_mode",

    "history",

    "downloads",

    "private_browsing",

    "share_sheet",
]


SAFARI_STATE_WEIGHTS = [

    20,

    24,

    14,

    10,

    10,

    8,

    8,

    6,
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
# Websites
# ==========================================================

WEBSITES = [

    {
        "title": "Research Portal",
        "domain": "research.example.com",
        "style": "blue",
    },

    {
        "title": "Daily News",
        "domain": "news.example.com",
        "style": "red",
    },

    {
        "title": "Developer Docs",
        "domain": "docs.example.com",
        "style": "dark",
    },

    {
        "title": "University",
        "domain": "university.example.com",
        "style": "purple",
    },

    {
        "title": "Cloud Drive",
        "domain": "drive.example.com",
        "style": "blue",
    },

    {
        "title": "Travel",
        "domain": "travel.example.com",
        "style": "green",
    },

    {
        "title": "Weather",
        "domain": "weather.example.com",
        "style": "cyan",
    },

    {
        "title": "Shopping",
        "domain": "shop.example.com",
        "style": "orange",
    },
]


# ==========================================================
# Favorite
# ==========================================================

def generate_favorites() -> list[dict]:

    chosen = random.sample(
        WEBSITES,
        k=6,
    )

    icons = [
        "book-open",
        "newspaper",
        "code-2",
        "graduation-cap",
        "cloud",
        "plane",
    ]

    result = []

    for index, site in enumerate(
        chosen
    ):

        result.append({

            "id":
                f"favorite_{index}",

            "title":
                site["title"],

            "domain":
                site["domain"],

            "style":
                site["style"],

            "icon":
                get_lucide_icon(
                    icons[
                        index
                        % len(
                            icons
                        )
                    ]
                ),
        })

    return result


# ==========================================================
# Reading List
# ==========================================================

def generate_reading_list() -> list[dict]:

    titles = [

        "Improving Interface Accessibility",

        "Design Systems at Scale",

        "Modern Browser Rendering",

        "Synthetic Dataset Generation",

        "User Interface Evaluation",
    ]

    return [

        {
            "id":
                f"reading_{index}",

            "title":
                title,

            "domain":
                random.choice(
                    WEBSITES
                )["domain"],

            "time":
                random.choice([
                    "Today",
                    "Yesterday",
                    "Friday",
                ]),
        }

        for index, title
        in enumerate(
            titles
        )
    ]


# ==========================================================
# Tabs
# ==========================================================

def generate_tabs() -> list[dict]:

    selected = random.sample(
        WEBSITES,
        k=6,
    )

    tabs = []

    for index, site in enumerate(
        selected
    ):

        tabs.append({

            "id":
                f"tab_{index}",

            "title":
                site["title"],

            "domain":
                site["domain"],

            "style":
                site["style"],

            "active":
                index == 0,

            "progress":
                random.randint(
                    20,
                    95,
                ),
        })

    return tabs


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    result = []

    for index in range(
        10
    ):

        site = random.choice(
            WEBSITES
        )

        result.append({

            "id":
                f"history_{index}",

            "title":
                site["title"],

            "domain":
                site["domain"],

            "time":
                random.choice([
                    "9:42 AM",
                    "10:17 AM",
                    "11:34 AM",
                    "Yesterday",
                    "Friday",
                ]),
        })

    return result


# ==========================================================
# Downloads
# ==========================================================

def generate_downloads() -> list[dict]:

    file_names = [

        "report.pdf",

        "dataset.zip",

        "slides.pptx",

        "results.csv",

        "paper.pdf",

        "screenshots.zip",
    ]

    result = []

    for index, name in enumerate(
        file_names
    ):

        downloading = (
            random.random()
            < 0.35
        )

        result.append({

            "id":
                f"download_{index}",

            "name":
                name,

            "size":
                random.choice([
                    "320 KB",
                    "1.8 MB",
                    "8.4 MB",
                    "24 MB",
                ]),

            "downloading":
                downloading,

            "progress":
                (
                    random.randint(
                        12,
                        88,
                    )
                    if downloading
                    else 100
                ),

            "icon":
                get_lucide_icon(
                    "file-down"
                ),
        })

    return result


# ==========================================================
# Current Web Page
# ==========================================================

def generate_webpage() -> dict:

    site = random.choice(
        WEBSITES
    )

    headline = random.choice([

        "Understanding Modern Interface Design",

        "A Practical Guide to Better User Experiences",

        "New Methods for Evaluating Software Interfaces",

        "Building Reliable Visual Datasets",

        "Recent Developments in Human-Computer Interaction",
    ])

    return {

        "title":
            site["title"],

        "domain":
            site["domain"],

        "headline":
            headline,

        "author":
            fake.name(),

        "date":
            random.choice([
                "September 5, 2026",
                "September 4, 2026",
                "August 30, 2026",
            ]),

        "paragraphs": [

            (
                "Modern interfaces combine typography, layout, "
                "color, imagery, and interaction to guide users "
                "through complex information."
            ),

            (
                "Consistent structure is important, but real "
                "applications also contain a wide range of states "
                "such as menus, dialogs, loading views, and forms."
            ),

            (
                "Evaluating these interfaces requires examples "
                "that capture both ordinary layouts and less "
                "frequent interaction states."
            ),

            (
                "Responsive behavior further changes geometry "
                "across compact phones, tablets, and landscape "
                "orientations."
            ),
        ],
    }


# ==========================================================
# Share Sheet
# ==========================================================

def generate_share_sheet() -> dict:

    return {

        "apps": [

            {
                "id": "messages",
                "title": "Messages",
                "icon": resolve_icon(
                    "message",
                    "message-circle",
                ),
                "style": "green",
            },

            {
                "id": "mail",
                "title": "Mail",
                "icon": resolve_icon(
                    "mail",
                    "mail",
                ),
                "style": "blue",
            },

            {
                "id": "notes",
                "title": "Notes",
                "icon": get_lucide_icon(
                    "notebook"
                ),
                "style": "yellow",
            },

            {
                "id": "files",
                "title": "Files",
                "icon": get_lucide_icon(
                    "folder"
                ),
                "style": "blue",
            },
        ],

        "actions": [

            {
                "id": "copy",
                "title": "Copy",
                "icon": get_lucide_icon(
                    "copy"
                ),
            },

            {
                "id": "reading_list",
                "title": "Add to Reading List",
                "icon": get_lucide_icon(
                    "glasses"
                ),
            },

            {
                "id": "bookmark",
                "title": "Add Bookmark",
                "icon": get_lucide_icon(
                    "bookmark"
                ),
            },

            {
                "id": "print",
                "title": "Print",
                "icon": get_lucide_icon(
                    "printer"
                ),
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_safari_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choices(

            SAFARI_STATES,

            weights=
                SAFARI_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in SAFARI_STATES:

        raise ValueError(
            f"Unknown Safari state: {state}"
        )


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


    webpage = generate_webpage()


    is_overlay_state = (
        state == "share_sheet"
    )


    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "webpage":
            webpage,

        "favorites":
            generate_favorites(),

        "reading_list":
            generate_reading_list(),

        "tabs":
            generate_tabs(),

        "history":
            generate_history(),

        "downloads":
            generate_downloads(),

        "share_sheet":
            generate_share_sheet(),


        "search": {

            "query":
                random.choice([
                    "",
                    "interface design",
                    "synthetic dataset",
                    "research",
                ]),
        },


        "icons": {

            "back":
                resolve_icon(
                    "back",
                    "chevron-left",
                ),

            "forward":
                resolve_icon(
                    "forward",
                    "chevron-right",
                ),

            "share":
                resolve_icon(
                    "share",
                    "share"
                ),

            "tabs":
                get_lucide_icon(
                    "copy"
                ),

            "bookmark":
                get_lucide_icon(
                    "bookmark"
                ),

            "reader":
                get_lucide_icon(
                    "align-left"
                ),

            "refresh":
                get_lucide_icon(
                    "rotate-cw"
                ),

            "search":
                resolve_icon(
                    "search"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "history":
                get_lucide_icon(
                    "history"
                ),

            "download":
                get_lucide_icon(
                    "download"
                ),

            "private":
                get_lucide_icon(
                    "glasses"
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in SAFARI_STATES:

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

            generate_safari_data(
                state=state
            ),

            sort_dicts=False,
        )