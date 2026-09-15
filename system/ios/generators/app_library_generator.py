from __future__ import annotations

import random

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


# ==========================================================
# States
# ==========================================================

APP_LIBRARY_STATES = [

    "normal",

    "search_active",

    "category_open",

    "app_context_menu",

    "suggestions_expanded",

    "recently_added",
]


APP_LIBRARY_STATE_WEIGHTS = [

    32,

    16,

    16,

    12,

    12,

    12,
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

    if (
        icon is None
        and fallback
    ):

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Apps
# ==========================================================

APP_POOL = [

    {
        "name": "Messages",
        "style": "green",
        "icon": resolve_icon(
            "message",
            "message-circle",
        ),
    },

    {
        "name": "Mail",
        "style": "blue",
        "icon": resolve_icon(
            "mail",
            "mail",
        ),
    },

    {
        "name": "Calendar",
        "style": "red",
        "icon": resolve_icon(
            "calendar",
            "calendar",
        ),
    },

    {
        "name": "Photos",
        "style": "multicolor",
        "icon": resolve_icon(
            "image",
            "image",
        ),
    },

    {
        "name": "Camera",
        "style": "gray",
        "icon": resolve_icon(
            "camera"
        ),
    },

    {
        "name": "Maps",
        "style": "green",
        "icon": resolve_icon(
            "map",
            "map",
        ),
    },

    {
        "name": "Weather",
        "style": "blue",
        "icon": get_lucide_icon(
            "cloud-sun"
        ),
    },

    {
        "name": "Clock",
        "style": "dark",
        "icon": get_lucide_icon(
            "clock-3"
        ),
    },

    {
        "name": "Notes",
        "style": "yellow",
        "icon": get_lucide_icon(
            "notebook"
        ),
    },

    {
        "name": "Reminders",
        "style": "white",
        "icon": get_lucide_icon(
            "list-checks"
        ),
    },

    {
        "name": "Music",
        "style": "red",
        "icon": resolve_icon(
            "music",
            "music"
        ),
    },

    {
        "name": "Podcasts",
        "style": "purple",
        "icon": get_lucide_icon(
            "podcast"
        ),
    },

    {
        "name": "Books",
        "style": "orange",
        "icon": get_lucide_icon(
            "book-open"
        ),
    },

    {
        "name": "Files",
        "style": "blue",
        "icon": resolve_icon(
            "folder",
            "folder"
        ),
    },

    {
        "name": "Wallet",
        "style": "dark",
        "icon": get_lucide_icon(
            "wallet-cards"
        ),
    },

    {
        "name": "Health",
        "style": "white",
        "icon": get_lucide_icon(
            "heart-pulse"
        ),
    },

    {
        "name": "Home",
        "style": "orange",
        "icon": resolve_icon(
            "home",
            "house"
        ),
    },

    {
        "name": "Settings",
        "style": "gray",
        "icon": resolve_icon(
            "settings",
            "settings"
        ),
    },

    {
        "name": "Safari",
        "style": "blue",
        "icon": get_lucide_icon(
            "compass"
        ),
    },

    {
        "name": "Shortcuts",
        "style": "purple",
        "icon": get_lucide_icon(
            "workflow"
        ),
    },
]


# ==========================================================
# Categories
# ==========================================================

CATEGORY_DEFINITIONS = [

    {
        "id":
            "suggestions",

        "title":
            "Suggestions",
    },

    {
        "id":
            "recently_added",

        "title":
            "Recently Added",
    },

    {
        "id":
            "social",

        "title":
            "Social",
    },

    {
        "id":
            "utilities",

        "title":
            "Utilities",
    },

    {
        "id":
            "productivity",

        "title":
            "Productivity",
    },

    {
        "id":
            "creativity",

        "title":
            "Creativity",
    },

    {
        "id":
            "information",

        "title":
            "Information & Reading",
    },

    {
        "id":
            "entertainment",

        "title":
            "Entertainment",
    },
]


# ==========================================================
# App Copy
# ==========================================================

def copy_app(
    app: dict,
) -> dict:

    return {
        **app,
        "badge":
            (
                random.randint(
                    1,
                    28,
                )
                if random.random() < 0.22
                else None
            ),
    }


# ==========================================================
# Category
# ==========================================================

def generate_category(
    definition: dict,
) -> dict:

    apps = random.sample(
        APP_POOL,
        k=4,
    )


    return {

        "id":
            definition["id"],

        "title":
            definition["title"],

        "apps":
            [
                copy_app(
                    app
                )
                for app
                in apps
            ],
    }


# ==========================================================
# Search
# ==========================================================

def generate_search_data() -> dict:

    query = random.choice([

        "m",

        "photo",

        "map",

        "music",

        "mail",

        "s",
    ])


    results = [

        copy_app(
            app
        )

        for app
        in APP_POOL

        if query.lower()
        in app["name"].lower()
    ]


    if not results:

        results = [

            copy_app(
                app
            )

            for app
            in random.sample(
                APP_POOL,
                k=5,
            )
        ]


    return {

        "query":
            query,

        "results":
            results[:8],
    }


# ==========================================================
# Context Menu
# ==========================================================

def generate_context_menu() -> dict:

    target = copy_app(
        random.choice(
            APP_POOL
        )
    )


    return {

        "target":
            target,

        "actions": [

            {
                "id":
                    "search",

                "label":
                    "Search",

                "icon":
                    resolve_icon(
                        "search"
                    ),

                "destructive":
                    False,
            },

            {
                "id":
                    "share",

                "label":
                    "Share App",

                "icon":
                    resolve_icon(
                        "share",
                        "share"
                    ),

                "destructive":
                    False,
            },

            {
                "id":
                    "delete",

                "label":
                    "Delete App",

                "icon":
                    get_lucide_icon(
                        "trash-2"
                    ),

                "destructive":
                    True,
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_app_library_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choices(

            APP_LIBRARY_STATES,

            weights=
                APP_LIBRARY_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in APP_LIBRARY_STATES:

        raise ValueError(
            f"Unknown App Library state: {state}"
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


    categories = [

        generate_category(
            definition
        )

        for definition
        in CATEGORY_DEFINITIONS
    ]


    selected_category = random.choice(
        categories
    )


    overlay_states = {

        "category_open",

        "app_context_menu",

        "suggestions_expanded",
    }


    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            state
            in overlay_states,


        "title":
            "App Library",


        "categories":
            categories,


        "selected_category":
            selected_category,


        "search":
            generate_search_data(),


        "context_menu":
            generate_context_menu(),


        "recent_apps":

            [
                copy_app(
                    app
                )

                for app
                in random.sample(
                    APP_POOL,
                    k=8,
                )
            ],


        "suggestions":

            [
                copy_app(
                    app
                )

                for app
                in random.sample(
                    APP_POOL,
                    k=8,
                )
            ],


        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "back":
                resolve_icon(
                    "back"
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


    for state in APP_LIBRARY_STATES:

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

            generate_app_library_data(
                state=
                    state
            ),

            sort_dicts=False,
        )