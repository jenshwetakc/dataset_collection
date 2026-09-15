from __future__ import annotations

import random


# ==========================================================
# Search States
# ==========================================================

SEARCH_STATES = [
    "default",
    "typing",
    "apps_results",
    "documents_results",
    "web_results",
    "recent_searches",
    "no_results",
    "search_filters",
    "search_settings",
]


# ==========================================================
# App Pool
# ==========================================================

APP_POOL = [
    {
        "name": "Settings",
        "icon": "settings",
        "category": "App",
    },
    {
        "name": "File Explorer",
        "icon": "folder",
        "category": "App",
    },
    {
        "name": "Photos",
        "icon": "photo_library",
        "category": "App",
    },
    {
        "name": "Calculator",
        "icon": "calculate",
        "category": "App",
    },
    {
        "name": "Terminal",
        "icon": "terminal",
        "category": "App",
    },
    {
        "name": "Notepad",
        "icon": "description",
        "category": "App",
    },
]


# ==========================================================
# Documents
# ==========================================================

DOCUMENT_POOL = [
    {
        "name": "Research Notes.docx",
        "icon": "description",
        "location": "Documents",
        "modified": "Today",
    },
    {
        "name": "Presentation.pptx",
        "icon": "slideshow",
        "location": "Documents",
        "modified": "Yesterday",
    },
    {
        "name": "Dataset Results.xlsx",
        "icon": "table_chart",
        "location": "Projects",
        "modified": "2 days ago",
    },
    {
        "name": "architecture.pdf",
        "icon": "picture_as_pdf",
        "location": "Downloads",
        "modified": "Last week",
    },
]


# ==========================================================
# Web Results
# ==========================================================

WEB_POOL = [
    {
        "title": "Windows help and support",
        "subtitle": "Find help with Windows features and settings.",
        "icon": "language",
    },
    {
        "title": "System settings overview",
        "subtitle": "Learn about display, sound, and power.",
        "icon": "public",
    },
    {
        "title": "File Explorer tips",
        "subtitle": "Organize and find files quickly.",
        "icon": "language",
    },
]


# ==========================================================
# Recent Searches
# ==========================================================

RECENT_SEARCHES = [
    "settings",
    "downloads",
    "display",
    "bluetooth",
    "terminal",
    "photos",
]


# ==========================================================
# Suggested Categories
# ==========================================================

SEARCH_CATEGORIES = [
    {
        "id": "all",
        "label": "All",
        "icon": "search",
    },
    {
        "id": "apps",
        "label": "Apps",
        "icon": "apps",
    },
    {
        "id": "documents",
        "label": "Documents",
        "icon": "description",
    },
    {
        "id": "web",
        "label": "Web",
        "icon": "language",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_query() -> str:

    return random.choice(
        [
            "settings",
            "display",
            "files",
            "photos",
            "terminal",
            "research",
        ]
    )


def generate_apps() -> list[dict]:

    return random.sample(
        APP_POOL,
        k=random.randint(
            3,
            min(
                5,
                len(APP_POOL),
            ),
        ),
    )


def generate_documents() -> list[dict]:

    return random.sample(
        DOCUMENT_POOL,
        k=random.randint(
            2,
            min(
                4,
                len(DOCUMENT_POOL),
            ),
        ),
    )


def generate_web_results() -> list[dict]:

    return random.sample(
        WEB_POOL,
        k=random.randint(
            2,
            len(WEB_POOL),
        ),
    )


# ==========================================================
# Main Generator
# ==========================================================

def generate_search_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SEARCH_STATES
        )


    if state not in SEARCH_STATES:

        raise ValueError(
            f"Unknown Search state: {state}"
        )


    query = ""

    if state in {
        "typing",
        "apps_results",
        "documents_results",
        "web_results",
        "no_results",
        "search_filters",
    }:

        query = generate_query()


    if state == "no_results":

        query = random.choice(
            [
                "xyz123",
                "unknown setting",
                "missing file",
                "nonexistent app",
            ]
        )


    return {
        "state":
            state,

        "query":
            query,

        "categories":
            SEARCH_CATEGORIES,

        "selected_category":
            (
                "apps"
                if state == "apps_results"
                else
                "documents"
                if state == "documents_results"
                else
                "web"
                if state == "web_results"
                else
                "all"
            ),

        "apps":
            (
                generate_apps()
                if state in {
                    "default",
                    "typing",
                    "apps_results",
                    "search_filters",
                }
                else []
            ),

        "documents":
            (
                generate_documents()
                if state in {
                    "typing",
                    "documents_results",
                    "search_filters",
                }
                else []
            ),

        "web":
            (
                generate_web_results()
                if state in {
                    "web_results",
                    "search_filters",
                }
                else []
            ),

        "recent":
            (
                random.sample(
                    RECENT_SEARCHES,
                    k=random.randint(
                        3,
                        len(RECENT_SEARCHES),
                    ),
                )
                if state
                in {
                    "default",
                    "recent_searches",
                }
                else []
            ),

        "settings": {
            "safe_search":
                random.choice(
                    [
                        "Moderate",
                        "Strict",
                        "Off",
                    ]
                ),

            "cloud_search":
                random.random()
                < 0.70,

            "history":
                random.random()
                < 0.75,
        },
    }