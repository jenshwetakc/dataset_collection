from __future__ import annotations

import random

from copy import deepcopy


# ==========================================================
# App Definitions
# ==========================================================

APP_LIBRARY = [

    {
        "name": "Messages",
        "symbol": "●",
        "style": "green",
    },

    {
        "name": "Calendar",
        "symbol": "17",
        "style": "calendar",
    },

    {
        "name": "Photos",
        "symbol": "✿",
        "style": "photos",
    },

    {
        "name": "Camera",
        "symbol": "◉",
        "style": "dark",
    },

    {
        "name": "Weather",
        "symbol": "☀",
        "style": "blue",
    },

    {
        "name": "Clock",
        "symbol": "◷",
        "style": "dark",
    },

    {
        "name": "Maps",
        "symbol": "↗",
        "style": "maps",
    },

    {
        "name": "Wallet",
        "symbol": "▰",
        "style": "wallet",
    },

    {
        "name": "Notes",
        "symbol": "≡",
        "style": "notes",
    },

    {
        "name": "Reminders",
        "symbol": "✓",
        "style": "white",
    },

    {
        "name": "Stocks",
        "symbol": "⌁",
        "style": "black",
    },

    {
        "name": "Books",
        "symbol": "▥",
        "style": "orange",
    },

    {
        "name": "App Store",
        "symbol": "A",
        "style": "blue",
    },

    {
        "name": "Podcasts",
        "symbol": "◉",
        "style": "purple",
    },

    {
        "name": "TV",
        "symbol": "TV",
        "style": "black",
    },

    {
        "name": "Health",
        "symbol": "♥",
        "style": "white",
    },

    {
        "name": "Home",
        "symbol": "⌂",
        "style": "orange",
    },

    {
        "name": "Settings",
        "symbol": "⚙",
        "style": "gray",
    },

    {
        "name": "Files",
        "symbol": "⌑",
        "style": "blue",
    },

    {
        "name": "Find My",
        "symbol": "●",
        "style": "findmy",
    },

    {
        "name": "Music",
        "symbol": "♫",
        "style": "music",
    },

    {
        "name": "News",
        "symbol": "N",
        "style": "red",
    },

    {
        "name": "FaceTime",
        "symbol": "▶",
        "style": "green",
    },

    {
        "name": "Mail",
        "symbol": "✉",
        "style": "blue",
    },

    {
        "name": "Safari",
        "symbol": "⌖",
        "style": "safari",
    },

    {
        "name": "Contacts",
        "symbol": "●",
        "style": "gray",
    },

    {
        "name": "Translate",
        "symbol": "文",
        "style": "black",
    },

    {
        "name": "Shortcuts",
        "symbol": "◆",
        "style": "shortcuts",
    },
]


# ==========================================================
# Dock Applications
# ==========================================================

DEFAULT_DOCK_NAMES = [
    "Phone",
    "Safari",
    "Messages",
    "Music",
]


DOCK_APP_LIBRARY = {

    "Phone": {
        "name": "Phone",
        "symbol": "☎",
        "style": "green",
    },

    "Safari": {
        "name": "Safari",
        "symbol": "⌖",
        "style": "safari",
    },

    "Messages": {
        "name": "Messages",
        "symbol": "●",
        "style": "green",
    },

    "Music": {
        "name": "Music",
        "symbol": "♫",
        "style": "music",
    },

    "Mail": {
        "name": "Mail",
        "symbol": "✉",
        "style": "blue",
    },

    "Camera": {
        "name": "Camera",
        "symbol": "◉",
        "style": "dark",
    },
}


# ==========================================================
# Home Screen States
# ==========================================================

HOME_STATES = [
    "normal",
    "folder_open",
    "context_menu",
    "edit_mode",
    "spotlight",
    "widget_edit",
]


HOME_STATE_WEIGHTS = [
    34,
    14,
    14,
    14,
    14,
    10,
]


# ==========================================================
# Wallpaper Definitions
# ==========================================================

WALLPAPERS = [

    {
        "name": "midnight",
        "background": (
            "linear-gradient("
            "145deg,"
            "#101C34 0%,"
            "#24355A 45%,"
            "#512C56 100%"
            ")"
        ),
    },

    {
        "name": "deep_blue",
        "background": (
            "radial-gradient("
            "circle at 25% 20%,"
            "#385C91 0%,"
            "#182844 38%,"
            "#0C1425 100%"
            ")"
        ),
    },

    {
        "name": "purple",
        "background": (
            "linear-gradient("
            "160deg,"
            "#493C72 0%,"
            "#2E3155 45%,"
            "#161D32 100%"
            ")"
        ),
    },

    {
        "name": "ocean",
        "background": (
            "radial-gradient("
            "circle at 70% 25%,"
            "#337C8C 0%,"
            "#24526D 35%,"
            "#14233B 100%"
            ")"
        ),
    },

    {
        "name": "sunset",
        "background": (
            "linear-gradient("
            "160deg,"
            "#7A4255 0%,"
            "#423451 45%,"
            "#18233A 100%"
            ")"
        ),
    },
]


# ==========================================================
# Widget Definitions
# ==========================================================

WIDGET_LIBRARY = [

    {
        "type": "weather",
        "title": "Weather",
        "headline": "22°",
        "subtitle": "Partly Cloudy",
        "footer": "H:25°  L:17°",
    },

    {
        "type": "calendar",
        "title": "Calendar",
        "headline": "Today",
        "subtitle": "Project meeting",
        "footer": "2:30 PM",
    },

    {
        "type": "battery",
        "title": "Batteries",
        "headline": "82%",
        "subtitle": "iPhone",
        "footer": "Connected",
    },

    {
        "type": "activity",
        "title": "Activity",
        "headline": "6,428",
        "subtitle": "steps",
        "footer": "4.7 km",
    },

    {
        "type": "music",
        "title": "Music",
        "headline": "Recently Played",
        "subtitle": "Daily Mix",
        "footer": "Playing",
    },
]


# ==========================================================
# Spotlight Suggestions
# ==========================================================

SPOTLIGHT_SUGGESTIONS = [
    "Settings",
    "Photos",
    "Messages",
    "Calendar",
    "Weather",
    "Notes",
    "Maps",
    "Mail",
    "Music",
]


# ==========================================================
# Clone App
# ==========================================================

def clone_app(
    app: dict,
) -> dict:

    return deepcopy(
        app
    )


# ==========================================================
# Find App
# ==========================================================

def find_app(
    name: str,
) -> dict | None:

    for app in APP_LIBRARY:

        if app["name"] == name:

            return clone_app(
                app
            )

    if name in DOCK_APP_LIBRARY:

        return clone_app(
            DOCK_APP_LIBRARY[
                name
            ]
        )

    return None


# ==========================================================
# Generate Badge
# ==========================================================

def generate_badge() -> int | None:

    if random.random() >= 0.24:

        return None

    return random.choice([
        1,
        2,
        3,
        4,
        5,
        8,
        12,
        17,
        24,
        36,
        99,
    ])


# ==========================================================
# Generate Applications
# ==========================================================

def generate_apps(
    count: int,
) -> list[dict]:

    count = min(
        count,
        len(
            APP_LIBRARY
        ),
    )

    selected = random.sample(
        APP_LIBRARY,
        k=count,
    )

    apps = []

    for index, source in enumerate(
        selected
    ):

        app = clone_app(
            source
        )

        app["id"] = (
            f"app_{index}"
        )

        app["badge"] = (
            generate_badge()
        )

        apps.append(
            app
        )

    return apps


# ==========================================================
# Generate Dock
# ==========================================================

def generate_dock() -> list[dict]:

    available_names = list(
        DOCK_APP_LIBRARY.keys()
    )

    if random.random() < 0.72:

        selected_names = (
            DEFAULT_DOCK_NAMES.copy()
        )

    else:

        selected_names = random.sample(
            available_names,
            k=4,
        )

    result = []

    for index, name in enumerate(
        selected_names
    ):

        app = clone_app(
            DOCK_APP_LIBRARY[
                name
            ]
        )

        app["id"] = (
            f"dock_{index}"
        )

        app["badge"] = (
            generate_badge()
        )

        result.append(
            app
        )

    return result


# ==========================================================
# Generate Widgets
# ==========================================================

def generate_widgets() -> list[dict]:

    count = random.choices(
        [
            0,
            1,
            2,
        ],
        weights=[
            28,
            52,
            20,
        ],
        k=1,
    )[0]

    if count == 0:

        return []

    selected = random.sample(
        WIDGET_LIBRARY,
        k=count,
    )

    widgets = []

    for index, widget in enumerate(
        selected
    ):

        value = deepcopy(
            widget
        )

        value["id"] = (
            f"widget_{index}"
        )

        value["size"] = random.choice([
            "small",
            "medium",
        ])

        widgets.append(
            value
        )

    return widgets


# ==========================================================
# Generate Folder
# ==========================================================

def generate_folder() -> dict:

    apps = generate_apps(
        random.randint(
            6,
            9,
        )
    )

    return {

        "name":
            random.choice([
                "Utilities",
                "Productivity",
                "Social",
                "Extras",
                "Work",
                "Travel",
            ]),

        "apps":
            apps,
    }


# ==========================================================
# Generate Context Menu
# ==========================================================

def generate_context_menu(
    apps: list[dict],
) -> dict:

    target_app = random.choice(
        apps
    )

    actions = [

        {
            "label": "Edit Home Screen",
            "symbol": "✎",
            "destructive": False,
        },

        {
            "label": "Share App",
            "symbol": "↗",
            "destructive": False,
        },

        {
            "label": "Remove App",
            "symbol": "−",
            "destructive": True,
        },
    ]

    if random.random() < 0.5:

        actions.insert(
            0,
            {
                "label": "Search",
                "symbol": "⌕",
                "destructive": False,
            },
        )

    return {

        "target_app":
            target_app,

        "actions":
            actions,
    }


# ==========================================================
# Generate Spotlight
# ==========================================================

def generate_spotlight() -> dict:

    query = random.choice([
        "",
        "",
        "",
        "set",
        "photo",
        "music",
        "map",
    ])

    suggestion_names = random.sample(
        SPOTLIGHT_SUGGESTIONS,
        k=random.randint(
            4,
            6,
        ),
    )

    suggestions = []

    for name in suggestion_names:

        app = find_app(
            name
        )

        if app is not None:

            suggestions.append(
                app
            )

    return {

        "query":
            query,

        "suggestions":
            suggestions,
    }


# ==========================================================
# Generate Widget Edit State
# ==========================================================

def generate_widget_edit() -> dict:

    widgets = random.sample(
        WIDGET_LIBRARY,
        k=min(
            4,
            len(
                WIDGET_LIBRARY
            ),
        ),
    )

    return {

        "title":
            "Add Widgets",

        "widgets": [
            deepcopy(
                widget
            )
            for widget in widgets
        ],
    }


# ==========================================================
# Resolve App Count
# ==========================================================

def get_app_count_for_viewport(
    viewport: dict | None,
) -> int:

    if not viewport:

        return 20

    category = viewport.get(
        "category"
    )

    orientation = viewport.get(
        "orientation"
    )

    if category == "tablet":

        if orientation == "landscape":

            return 28

        return 24

    if orientation == "landscape":

        return 16

    return 20


# ==========================================================
# Generate Home Screen
# ==========================================================

def generate_home_data(
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:
    """
    Generate one synthetic iOS home screen.

    Supported states:
        normal
        folder_open
        context_menu
        edit_mode
        spotlight
        widget_edit
    """

    if state is None:

        state = random.choices(
            HOME_STATES,
            weights=
                HOME_STATE_WEIGHTS,
            k=1,
        )[0]

    if state not in HOME_STATES:

        raise ValueError(
            f"Unknown iOS home state: {state}. "
            f"Available states: {HOME_STATES}"
        )

    app_count = (
        get_app_count_for_viewport(
            viewport
        )
    )

    apps = generate_apps(
        app_count
    )

    widgets = (
        generate_widgets()
    )

    dock = generate_dock()

    wallpaper = random.choice(
        WALLPAPERS
    )

    page_count = random.randint(
        2,
        4,
    )

    selected_page = random.randint(
        0,
        page_count - 1,
    )

    data = {

        "state":
            state,

        "wallpaper":
            deepcopy(
                wallpaper
            ),

        "apps":
            apps,

        "widgets":
            widgets,

        "dock":
            dock,

        "pages": {
            "count":
                page_count,

            "selected":
                selected_page,
        },

        "folder":
            None,

        "context_menu":
            None,

        "spotlight":
            None,

        "widget_edit":
            None,

        "is_overlay_state":
            state in {
                "folder_open",
                "context_menu",
                "spotlight",
                "widget_edit",
            },
    }


    # ======================================================
    # State-Specific Data
    # ======================================================

    if state == "folder_open":

        data["folder"] = (
            generate_folder()
        )


    elif state == "context_menu":

        data["context_menu"] = (
            generate_context_menu(
                apps
            )
        )


    elif state == "spotlight":

        data["spotlight"] = (
            generate_spotlight()
        )


    elif state == "widget_edit":

        data["widget_edit"] = (
            generate_widget_edit()
        )


    return data


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    example_viewport = {

        "name":
            "standard_iphone",

        "category":
            "mobile",

        "orientation":
            "portrait",

        "size_class":
            "compact",

        "width":
            390,

        "height":
            844,

        "dpr":
            3,
    }

    for state in HOME_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state.upper()
        )

        print(
            "=========================================="
        )

        pprint(
            generate_home_data(
                viewport=
                    example_viewport,

                state=
                    state,
            ),
            sort_dicts=False,
        )