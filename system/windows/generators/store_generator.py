from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

STORE_STATES = [
    "home",
    "search_results",
    "app_detail",
    "installing",
    "installed",
    "library",
    "updates_available",
    "updating",
    "categories",
    "wishlist",
    "offline",
    "install_dialog",
]


# ==========================================================
# Navigation
# ==========================================================

STORE_NAVIGATION = [
    {
        "id": "home",
        "label": "Home",
        "icon": "home",
    },
    {
        "id": "apps",
        "label": "Apps",
        "icon": "apps",
    },
    {
        "id": "gaming",
        "label": "Gaming",
        "icon": "sports_esports",
    },
    {
        "id": "library",
        "label": "Library",
        "icon": "video_library",
    },
]


# ==========================================================
# App Pool
# ==========================================================

APP_POOL = [
    {
        "name": "Photo Studio",
        "category": "Photo & video",
        "icon": "photo_camera",
        "publisher": "Creative Labs",
        "rating": 4.7,
        "price": "Free",
    },
    {
        "name": "Focus Notes",
        "category": "Productivity",
        "icon": "note_alt",
        "publisher": "Focus Apps",
        "rating": 4.6,
        "price": "Free",
    },
    {
        "name": "Code Editor",
        "category": "Developer tools",
        "icon": "code",
        "publisher": "Dev Tools",
        "rating": 4.8,
        "price": "Free",
    },
    {
        "name": "Music Player",
        "category": "Music",
        "icon": "music_note",
        "publisher": "Sound Labs",
        "rating": 4.4,
        "price": "$4.99",
    },
    {
        "name": "Weather Plus",
        "category": "News & weather",
        "icon": "partly_cloudy_day",
        "publisher": "Weather Works",
        "rating": 4.5,
        "price": "Free",
    },
    {
        "name": "Sketch Board",
        "category": "Creativity",
        "icon": "draw",
        "publisher": "Design Studio",
        "rating": 4.3,
        "price": "$8.99",
    },
    {
        "name": "Game Hub",
        "category": "Gaming",
        "icon": "sports_esports",
        "publisher": "Arcade Labs",
        "rating": 4.2,
        "price": "Free",
    },
    {
        "name": "PDF Reader",
        "category": "Productivity",
        "icon": "picture_as_pdf",
        "publisher": "Office Tools",
        "rating": 4.6,
        "price": "Free",
    },
]


# ==========================================================
# Categories
# ==========================================================

CATEGORY_POOL = [
    {
        "name": "Productivity",
        "icon": "work",
    },
    {
        "name": "Photo & video",
        "icon": "photo_library",
    },
    {
        "name": "Entertainment",
        "icon": "movie",
    },
    {
        "name": "Developer tools",
        "icon": "terminal",
    },
    {
        "name": "Education",
        "icon": "school",
    },
    {
        "name": "Music",
        "icon": "music_note",
    },
    {
        "name": "Gaming",
        "icon": "sports_esports",
    },
    {
        "name": "Utilities",
        "icon": "build",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_apps(
    minimum: int = 4,
    maximum: int = 8,
) -> list[dict]:

    count = random.randint(
        minimum,
        min(
            maximum,
            len(APP_POOL),
        ),
    )

    result = []

    for app in random.sample(
        APP_POOL,
        k=count,
    ):

        result.append(
            {
                **app,

                "installed":
                    random.random()
                    < 0.30,

                "progress":
                    None,

                "update_available":
                    random.random()
                    < 0.35,
            }
        )

    return result


def generate_featured_app() -> dict:

    app = random.choice(
        APP_POOL
    )

    return {
        **app,

        "headline":
            random.choice(
                [
                    "Featured app",
                    "Editor's choice",
                    "Popular this week",
                ]
            ),

        "description":
            random.choice(
                [
                    "Discover powerful tools designed for everyday work.",
                    "A simple and modern experience for Windows.",
                    "Explore one of this week's most popular downloads.",
                ]
            ),
    }


def generate_search() -> dict:

    query = random.choice(
        [
            "photo",
            "music",
            "code",
            "notes",
            "reader",
            "weather",
        ]
    )

    return {
        "query":
            query,

        "results":
            generate_apps(
                minimum=3,
                maximum=6,
            ),
    }


def generate_library() -> list[dict]:

    apps = generate_apps(
        minimum=5,
        maximum=8,
    )

    for app in apps:

        app["installed"] = True

    return apps


def generate_updates() -> list[dict]:

    apps = generate_library()

    selected = random.sample(
        apps,
        k=random.randint(
            2,
            min(
                5,
                len(apps),
            ),
        ),
    )

    for app in selected:

        app["update_available"] = True

    return selected


# ==========================================================
# Main Generator
# ==========================================================

def generate_store_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            STORE_STATES
        )


    if state not in STORE_STATES:

        raise ValueError(
            f"Unknown Store state: {state}"
        )


    selected_app = (
        random.choice(
            APP_POOL
        )
    )


    progress = None


    if state in {
        "installing",
        "updating",
    }:

        progress = random.randint(
            8,
            92,
        )


    return {

        "state":
            state,

        "navigation":
            STORE_NAVIGATION,

        "featured":
            generate_featured_app(),

        "apps":
            generate_apps(),

        "categories":
            CATEGORY_POOL,

        "search":
            generate_search(),

        "selected_app": {
            **selected_app,

            "installed":
                state
                == "installed",

            "progress":
                progress,

            "description":
                random.choice(
                    [
                        "A modern Windows app designed for fast everyday workflows.",
                        "Simple tools, a clean interface, and useful features.",
                        "Built to help you work more efficiently on your PC.",
                    ]
                ),

            "reviews":
                random.randint(
                    120,
                    12000,
                ),
        },

        "library":
            generate_library(),

        "updates":
            generate_updates(),

        "wishlist":
            random.sample(
                APP_POOL,
                k=random.randint(
                    3,
                    6,
                ),
            ),
    }