from __future__ import annotations

import random

from faker import Faker

from system.ubuntu.generators.media_generator import (
    get_random_wallpaper,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

DESKTOP_STATES = [

    "empty",

    "desktop_icons",

    "quick_settings_open",

    "calendar_open",

    "context_menu_open",

    "notification_open",

    "app_grid_open",

    "search_open",

    "single_window",

    "two_windows",

    "maximized_window",

    "half_screen_window",
]


# ==========================================================
# Dock Applications
# ==========================================================

DOCK_APPS = [

    {
        "name": "Firefox",
        "icon": "language",
    },

    {
        "name": "Files",
        "icon": "folder",
    },

    {
        "name": "Terminal",
        "icon": "terminal",
    },

    {
        "name": "Software",
        "icon": "shopping_bag",
    },

    {
        "name": "Settings",
        "icon": "settings",
    },
]


# ==========================================================
# App Grid
# ==========================================================

APP_GRID_APPS = [

    {
        "name": "Calculator",
        "icon": "calculate",
    },

    {
        "name": "Calendar",
        "icon": "calendar_month",
    },

    {
        "name": "Camera",
        "icon": "photo_camera",
    },

    {
        "name": "Files",
        "icon": "folder",
    },

    {
        "name": "Firefox",
        "icon": "language",
    },

    {
        "name": "Settings",
        "icon": "settings",
    },

    {
        "name": "Software",
        "icon": "shopping_bag",
    },

    {
        "name": "Terminal",
        "icon": "terminal",
    },

    {
        "name": "Text Editor",
        "icon": "edit_note",
    },

    {
        "name": "Videos",
        "icon": "movie",
    },

    {
        "name": "Weather",
        "icon": "partly_cloudy_day",
    },

    {
        "name": "Help",
        "icon": "help",
    },
]


# ==========================================================
# Desktop Icons
# ==========================================================

DESKTOP_ICON_CHOICES = [

    {
        "name": "Home",
        "icon": "home",
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
        "name": "Projects",
        "icon": "folder",
    },

    {
        "name": "Pictures",
        "icon": "image",
    },
]


# ==========================================================
# Window Generator
# ==========================================================

def generate_window(
    application: str | None = None,
):

    application = (
        application
        or random.choice(
            [
                "Files",
                "Terminal",
                "Settings",
            ]
        )
    )

    if application == "Files":

        return {

            "application":
                "Files",

            "title":
                random.choice(
                    [
                        "Home",
                        "Documents",
                        "Downloads",
                    ]
                ),

            "icon":
                "folder",

            "content_type":
                "files",
        }

    if application == "Settings":

        return {

            "application":
                "Settings",

            "title":
                random.choice(
                    [
                        "Settings",
                        "Network",
                        "Appearance",
                    ]
                ),

            "icon":
                "settings",

            "content_type":
                "settings",
        }

    return {

        "application":
            "Terminal",

        "title":
            "Terminal",

        "icon":
            "terminal",

        "content_type":
            "terminal",
    }


# ==========================================================
# Desktop Generator
# ==========================================================

def generate_desktop_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            DESKTOP_STATES
        )

    if state not in DESKTOP_STATES:

        raise ValueError(
            f"Unknown desktop state: {state}"
        )

    # ------------------------------------------------------
    # Dock
    # ------------------------------------------------------

    dock_apps = [
        dict(app)
        for app in DOCK_APPS
    ]

    running_count = random.randint(
        1,
        3,
    )

    running_indices = random.sample(
        range(
            len(dock_apps)
        ),
        k=running_count,
    )

    for index, app in enumerate(
        dock_apps
    ):

        app["running"] = (
            index
            in running_indices
        )

        app["active"] = False

    active_index = random.choice(
        running_indices
    )

    dock_apps[
        active_index
    ][
        "active"
    ] = True

    # ------------------------------------------------------
    # Desktop icons
    # ------------------------------------------------------

    desktop_icons = random.sample(
        DESKTOP_ICON_CHOICES,
        k=random.randint(
            2,
            min(
                5,
                len(
                    DESKTOP_ICON_CHOICES
                ),
            ),
        ),
    )

    # ------------------------------------------------------
    # Windows
    # ------------------------------------------------------

    windows = []

    if state in {
        "single_window",
        "maximized_window",
        "half_screen_window",
    }:

        windows = [
            generate_window()
        ]

    elif state == "two_windows":

        first_app = random.choice(
            [
                "Files",
                "Terminal",
                "Settings",
            ]
        )

        second_candidates = [
            value
            for value in [
                "Files",
                "Terminal",
                "Settings",
            ]
            if value != first_app
        ]

        windows = [

            generate_window(
                first_app
            ),

            generate_window(
                random.choice(
                    second_candidates
                )
            ),
        ]

    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    search_query = random.choice(
        [
            "",
            "settings",
            "terminal",
            "files",
            "calculator",
        ]
    )

    # ------------------------------------------------------
    # Result
    # ------------------------------------------------------

    return {

        "state":
            state,

        "wallpaper":
            get_random_wallpaper(),

        "dock_apps":
            dock_apps,

        "desktop_icons":
            desktop_icons,

        "app_grid_apps":
            APP_GRID_APPS,

        "windows":
            windows,

        "search_query":
            search_query,

        "search_results":
            random.sample(
                APP_GRID_APPS,
                k=4,
            ),

        "context_menu_entries": [

            {
                "label":
                    "New Folder",

                "icon":
                    "create_new_folder",
            },

            {
                "label":
                    "Paste",

                "icon":
                    "content_paste",
            },

            {
                "label":
                    "Open in Terminal",

                "icon":
                    "terminal",
            },

            {
                "label":
                    "Display Settings",

                "icon":
                    "monitor",
            },

            {
                "label":
                    "Change Background",

                "icon":
                    "wallpaper",
            },
        ],

        "calendar_days":
            list(
                range(
                    1,
                    31,
                )
            ),

        "user_name":
            fake.first_name(),

        "computer_name":
            fake.user_name(),
    }