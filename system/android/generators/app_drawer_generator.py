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

WALLPAPER_DIR = (
    ANDROID_ROOT
    / "assets"
    / "wallpapers"
)


# ==========================================================
# Application Pool
# ==========================================================

APP_POOL = [

    {
        "name": "Calculator",
        "icon": "mdi:calculator",
    },

    {
        "name": "Calendar",
        "icon": "mdi:calendar",
    },

    {
        "name": "Camera",
        "icon": "mdi:camera",
    },

    {
        "name": "Chrome",
        "icon": "mdi:google-chrome",
    },

    {
        "name": "Clock",
        "icon": "mdi:clock-outline",
    },

    {
        "name": "Contacts",
        "icon": "mdi:account-box-outline",
    },

    {
        "name": "Drive",
        "icon": "mdi:google-drive",
    },

    {
        "name": "Files",
        "icon": "mdi:folder-outline",
    },

    {
        "name": "Gmail",
        "icon": "mdi:gmail",
    },

    {
        "name": "Google",
        "icon": "mdi:google",
    },

    {
        "name": "Keep Notes",
        "icon": "mdi:lightbulb-outline",
    },

    {
        "name": "Maps",
        "icon": "mdi:google-maps",
    },

    {
        "name": "Meet",
        "icon": "mdi:video-outline",
    },

    {
        "name": "Messages",
        "icon": "mdi:message-text-outline",
    },

    {
        "name": "Photos",
        "icon": "mdi:image-multiple-outline",
    },

    {
        "name": "Phone",
        "icon": "mdi:phone-outline",
    },

    {
        "name": "Play Store",
        "icon": "mdi:google-play",
    },

    {
        "name": "Recorder",
        "icon": "mdi:microphone-outline",
    },

    {
        "name": "Settings",
        "icon": "mdi:cog-outline",
    },

    {
        "name": "Weather",
        "icon": "mdi:weather-partly-cloudy",
    },

    {
        "name": "YouTube",
        "icon": "mdi:youtube",
    },

    {
        "name": "YouTube Music",
        "icon": "mdi:music-circle-outline",
    },

    {
        "name": "Wallet",
        "icon": "mdi:wallet-outline",
    },

    {
        "name": "Translate",
        "icon": "mdi:translate",
    },
]


# ==========================================================
# Work Apps
# ==========================================================

WORK_APP_POOL = [

    {
        "name": "Calendar",
        "icon": "mdi:calendar-outline",
    },

    {
        "name": "Chrome",
        "icon": "mdi:google-chrome",
    },

    {
        "name": "Drive",
        "icon": "mdi:google-drive",
    },

    {
        "name": "Gmail",
        "icon": "mdi:gmail",
    },

    {
        "name": "Meet",
        "icon": "mdi:video-outline",
    },

    {
        "name": "Slack",
        "icon": "mdi:slack",
    },

    {
        "name": "Docs",
        "icon": "mdi:file-document-outline",
    },

    {
        "name": "Sheets",
        "icon": "mdi:table-large",
    },
]


# ==========================================================
# Icon Backgrounds
# ==========================================================

ICON_BACKGROUNDS = [
    "#1565C0",
    "#2E7D32",
    "#6A1B9A",
    "#C62828",
    "#EF6C00",
    "#00838F",
    "#455A64",
    "#283593",
    "#AD1457",
]


# ==========================================================
# Wallpaper
# ==========================================================

def get_wallpaper() -> str | None:

    if not WALLPAPER_DIR.exists():
        return None

    try:

        return get_random_image(
            WALLPAPER_DIR
        )

    except Exception:

        return None


# ==========================================================
# Build App
# ==========================================================

def build_app(
    app: dict,
    index: int,
    *,
    work_profile: bool = False,
) -> dict:

    return {

        "semantic":
            (
                f"work_app_{index}"
                if work_profile
                else f"app_{index}"
            ),

        "name":
            app["name"],

        "icon":
            app["icon"],

        "background":
            random.choice(
                ICON_BACKGROUNDS
            ),

        "notification_dot":
            random.random()
            < 0.14,

        "work_profile":
            work_profile,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_app_drawer_data() -> dict:

    # ======================================================
    # State
    # ======================================================

    drawer_state = random.choices(
        [
            "normal",
            "search",
            "search_results",
        ],
        weights=[
            0.60,
            0.18,
            0.22,
        ],
        k=1,
    )[0]


    # ======================================================
    # Tabs
    # ======================================================

    has_work_profile = (
        random.random()
        < 0.42
    )

    active_tab = (
        random.choice([
            "personal",
            "work",
        ])
        if has_work_profile
        else "personal"
    )


    # ======================================================
    # Grid
    # ======================================================

    columns = random.choice([
        4,
        5,
    ])


    # ======================================================
    # Apps
    # ======================================================

    personal_count = random.randint(
        16,
        len(APP_POOL),
    )

    selected_personal = random.sample(
        APP_POOL,
        personal_count,
    )

    personal_apps = [

        build_app(
            app,
            index,
        )

        for index, app
        in enumerate(
            selected_personal
        )
    ]


    work_apps = []

    if has_work_profile:

        work_count = random.randint(
            5,
            len(WORK_APP_POOL),
        )

        work_apps = [

            build_app(
                app,
                index,
                work_profile=True,
            )

            for index, app
            in enumerate(
                random.sample(
                    WORK_APP_POOL,
                    work_count,
                )
            )
        ]


    # ======================================================
    # Suggestions
    # ======================================================

    show_suggestions = (
        drawer_state == "normal"
        and random.random()
        < 0.72
    )

    suggestions = random.sample(
        personal_apps,
        k=min(
            random.choice([
                4,
                5,
            ]),
            len(personal_apps),
        ),
    )


    # ======================================================
    # Search
    # ======================================================

    query = ""

    search_results = []

    if drawer_state == "search":

        query = random.choice([
            "",
            "C",
            "Go",
            "Ma",
            "Set",
        ])


    elif drawer_state == "search_results":

        query = random.choice([
            "ca",
            "go",
            "ph",
            "you",
            "set",
            "map",
        ])

        search_results = [

            app
            for app
            in personal_apps

            if query.lower()
            in app["name"].lower()
        ]


        if not search_results:

            search_results = random.sample(
                personal_apps,
                k=min(
                    4,
                    len(personal_apps),
                ),
            )


    # ======================================================
    # Current Apps
    # ======================================================

    current_apps = (
        work_apps
        if active_tab == "work"
        else personal_apps
    )


    if drawer_state == "search_results":

        current_apps = search_results


    # ======================================================
    # Misc State
    # ======================================================

    show_alphabet_index = (
        drawer_state == "normal"
        and random.random()
        < 0.34
    )

    show_keyboard = (
        drawer_state
        in {
            "search",
            "search_results",
        }
        and random.random()
        < 0.55
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "drawer_state":
            drawer_state,

        "wallpaper":
            get_wallpaper(),

        "columns":
            columns,

        "has_work_profile":
            has_work_profile,

        "active_tab":
            active_tab,

        "personal_apps":
            personal_apps,

        "work_apps":
            work_apps,

        "apps":
            current_apps,

        "show_suggestions":
            show_suggestions,

        "suggestions":
            suggestions,

        "query":
            query,

        "show_alphabet_index":
            show_alphabet_index,

        "show_keyboard":
            show_keyboard,

        "result_count":
            len(
                search_results
            ),
    }