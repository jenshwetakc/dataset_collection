from __future__ import annotations

import random


# ==========================================================
# App Pools
# ==========================================================

APP_POOL = [

    {
        "name": "Phone",
        "icon": "mdi:phone",
        "color": "#2E7D32",
    },

    {
        "name": "Messages",
        "icon": "mdi:message-text",
        "color": "#1976D2",
    },

    {
        "name": "Camera",
        "icon": "mdi:camera",
        "color": "#424242",
    },

    {
        "name": "Chrome",
        "icon": "mdi:google-chrome",
        "color": "#F9A825",
    },

    {
        "name": "Gmail",
        "icon": "mdi:gmail",
        "color": "#D32F2F",
    },

    {
        "name": "Maps",
        "icon": "mdi:google-maps",
        "color": "#388E3C",
    },

    {
        "name": "Photos",
        "icon": "mdi:image-multiple",
        "color": "#8E24AA",
    },

    {
        "name": "YouTube",
        "icon": "mdi:youtube",
        "color": "#D50000",
    },

    {
        "name": "Drive",
        "icon": "mdi:google-drive",
        "color": "#2E7D32",
    },

    {
        "name": "Calendar",
        "icon": "mdi:calendar",
        "color": "#1565C0",
    },

    {
        "name": "Clock",
        "icon": "mdi:clock-outline",
        "color": "#455A64",
    },

    {
        "name": "Calculator",
        "icon": "mdi:calculator",
        "color": "#5E35B1",
    },

    {
        "name": "Files",
        "icon": "mdi:folder-outline",
        "color": "#F9A825",
    },

    {
        "name": "Contacts",
        "icon": "mdi:account-box",
        "color": "#00897B",
    },

    {
        "name": "Settings",
        "icon": "mdi:cog",
        "color": "#546E7A",
    },

    {
        "name": "Weather",
        "icon": "mdi:weather-partly-cloudy",
        "color": "#0288D1",
    },

    {
        "name": "Music",
        "icon": "mdi:music",
        "color": "#7B1FA2",
    },

    {
        "name": "Play Store",
        "icon": "mdi:google-play",
        "color": "#00897B",
    },

    {
        "name": "Keep Notes",
        "icon": "mdi:lightbulb-outline",
        "color": "#FBC02D",
    },

    {
        "name": "Meet",
        "icon": "mdi:video-outline",
        "color": "#00796B",
    },
]


# ==========================================================
# Dock
# ==========================================================

DOCK_APPS = [
    {
        "name": "Phone",
        "icon": "mdi:phone",
    },
    {
        "name": "Messages",
        "icon": "mdi:message-text",
    },
    {
        "name": "Chrome",
        "icon": "mdi:google-chrome",
    },
    {
        "name": "Camera",
        "icon": "mdi:camera",
    },
]


# ==========================================================
# Wallpapers
# ==========================================================

WALLPAPERS = [

    {
        "name": "blue_wave",
        "css": (
            "linear-gradient("
            "145deg,"
            "#163A5F 0%,"
            "#2E6F95 45%,"
            "#8BC6EC 100%"
            ")"
        ),
    },

    {
        "name": "purple_haze",
        "css": (
            "linear-gradient("
            "145deg,"
            "#271739 0%,"
            "#673AB7 48%,"
            "#CE93D8 100%"
            ")"
        ),
    },

    {
        "name": "green_mist",
        "css": (
            "linear-gradient("
            "145deg,"
            "#143128 0%,"
            "#2E7D32 50%,"
            "#81C784 100%"
            ")"
        ),
    },

    {
        "name": "sunrise",
        "css": (
            "linear-gradient("
            "145deg,"
            "#4A2C2A 0%,"
            "#D2695E 45%,"
            "#FFD3A5 100%"
            ")"
        ),
    },
]


# ==========================================================
# Widgets
# ==========================================================

WEATHER_WIDGETS = [
    {
        "city": "Seoul",
        "temperature": "22°",
        "condition": "Partly cloudy",
        "icon": "mdi:weather-partly-cloudy",
    },
    {
        "city": "Seoul",
        "temperature": "19°",
        "condition": "Cloudy",
        "icon": "mdi:weather-cloudy",
    },
    {
        "city": "Seoul",
        "temperature": "25°",
        "condition": "Sunny",
        "icon": "mdi:weather-sunny",
    },
]


# ==========================================================
# Build App
# ==========================================================

def build_app(
    app: dict,
    index: int,
) -> dict:

    return {
        "semantic":
            f"home_app_{index}",

        "name":
            app["name"],

        "icon":
            app["icon"],

        "color":
            app["color"],

        "notification_dot":
            random.random() < 0.22,

        "work_profile":
            random.random() < 0.08,
    }


# ==========================================================
# Main
# ==========================================================

def generate_home_screen_data() -> dict:

    # ======================================================
    # Layout
    # ======================================================

    columns = random.choice([
        4,
        5,
    ])

    app_count = random.randint(
        12,
        min(
            20,
            len(APP_POOL),
        ),
    )

    selected_apps = random.sample(
        APP_POOL,
        k=app_count,
    )

    apps = [
        build_app(
            app,
            index,
        )
        for index, app
        in enumerate(
            selected_apps
        )
    ]


    # ======================================================
    # State
    # ======================================================

    show_search = (
        random.random() < 0.88
    )

    show_widget = (
        random.random() < 0.58
    )

    show_folder = (
        random.random() < 0.35
    )

    show_page_indicator = (
        random.random() < 0.75
    )

    show_app_drawer_hint = (
        random.random() < 0.55
    )


    # ======================================================
    # Folder
    # ======================================================

    folder = None

    if show_folder:

        folder_apps = random.sample(
            APP_POOL,
            k=random.randint(
                4,
                6,
            ),
        )

        folder = {
            "name":
                random.choice([
                    "Google",
                    "Tools",
                    "Work",
                    "Media",
                ]),

            "apps":
                folder_apps,
        }


    # ======================================================
    # Widget
    # ======================================================

    weather = random.choice(
        WEATHER_WIDGETS
    )


    # ======================================================
    # Wallpaper
    # ======================================================

    wallpaper = random.choice(
        WALLPAPERS
    )


    # ======================================================
    # Page State
    # ======================================================

    page_count = random.choice([
        2,
        3,
    ])

    active_page = random.randint(
        0,
        page_count - 1,
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "columns":
            columns,

        "apps":
            apps,

        "show_search":
            show_search,

        "show_widget":
            show_widget,

        "show_folder":
            show_folder,

        "folder":
            folder,

        "show_page_indicator":
            show_page_indicator,

        "show_app_drawer_hint":
            show_app_drawer_hint,

        "page_count":
            page_count,

        "active_page":
            active_page,

        "wallpaper":
            wallpaper,

        "weather":
            weather,

        "dock_apps":
            DOCK_APPS,
    }