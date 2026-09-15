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


SCREENSHOT_DIR = (
    ANDROID_ROOT
    / "assets"
    / "app_screenshots"
)


# ==========================================================
# Applications
# ==========================================================

APP_POOL = [

    {
        "name":
            "Chrome",

        "icon":
            "mdi:google-chrome",
    },

    {
        "name":
            "Messages",

        "icon":
            "mdi:message-text",
    },

    {
        "name":
            "Gmail",

        "icon":
            "mdi:gmail",
    },

    {
        "name":
            "Maps",

        "icon":
            "mdi:google-maps",
    },

    {
        "name":
            "YouTube",

        "icon":
            "mdi:youtube",
    },

    {
        "name":
            "Photos",

        "icon":
            "mdi:image-multiple-outline",
    },

    {
        "name":
            "Settings",

        "icon":
            "mdi:cog-outline",
    },

    {
        "name":
            "Calendar",

        "icon":
            "mdi:calendar-outline",
    },

    {
        "name":
            "Files",

        "icon":
            "mdi:folder-outline",
    },

    {
        "name":
            "Play Store",

        "icon":
            "mdi:google-play",
    },
]


# ==========================================================
# Fallback Screens
# ==========================================================

FALLBACK_SCREENS = [

    {
        "type":
            "browser",

        "title":
            "New tab",

        "lines":
            5,
    },

    {
        "type":
            "messages",

        "title":
            "Messages",

        "lines":
            6,
    },

    {
        "type":
            "mail",

        "title":
            "Inbox",

        "lines":
            7,
    },

    {
        "type":
            "settings",

        "title":
            "Settings",

        "lines":
            8,
    },

    {
        "type":
            "feed",

        "title":
            "Home",

        "lines":
            5,
    },
]


# ==========================================================
# Assets
# ==========================================================

def get_random_asset(
    directory: Path,
) -> str | None:

    if not directory.exists():

        return None


    try:

        return get_random_image(
            directory
        )

    except Exception:

        return None


# ==========================================================
# Build Recent App
# ==========================================================

def build_recent_app(
    app: dict,
    index: int,
) -> dict:

    screenshot = get_random_asset(
        SCREENSHOT_DIR
    )


    fallback = random.choice(
        FALLBACK_SCREENS
    )


    return {

        "semantic":
            f"recent_app_{index}",

        "name":
            app["name"],

        "icon":
            app["icon"],

        "screenshot":
            screenshot,

        "fallback":
            fallback,

        "locked":
            random.random()
            < 0.10,

        "split_supported":
            random.random()
            < 0.78,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_recent_apps_data() -> dict:

    # ======================================================
    # Overview State
    # ======================================================

    overview_state = random.choices(

        [
            "normal",
            "single",
            "empty",
            "menu",
            "split_suggestion",
        ],

        weights=[
            0.46,
            0.16,
            0.10,
            0.14,
            0.14,
        ],

        k=1,

    )[0]


    # ======================================================
    # Recent Count
    # ======================================================

    if overview_state == "empty":

        recent_count = 0

    elif overview_state == "single":

        recent_count = 1

    else:

        recent_count = random.randint(
            2,
            5,
        )


    selected_apps = random.sample(
        APP_POOL,
        k=recent_count,
    )


    recent_apps = [

        build_recent_app(
            app,
            index,
        )

        for index, app
        in enumerate(
            selected_apps
        )
    ]


    # ======================================================
    # Focus
    # ======================================================

    focused_index = (

        random.randrange(
            len(recent_apps)
        )

        if recent_apps

        else 0
    )


    # ======================================================
    # Menu
    # ======================================================

    show_menu = (
        overview_state
        == "menu"

        and bool(
            recent_apps
        )
    )


    # ======================================================
    # Split
    # ======================================================

    show_split_suggestion = (
        overview_state
        == "split_suggestion"

        and bool(
            recent_apps
        )
    )


    # ======================================================
    # Bottom Actions
    # ======================================================

    show_screenshot_action = (
        bool(
            recent_apps
        )
        and random.random()
        < 0.72
    )


    show_select_action = (
        bool(
            recent_apps
        )
        and random.random()
        < 0.52
    )


    show_clear_all = (
        len(
            recent_apps
        )
        >= 2

        and random.random()
        < 0.80
    )


    # ======================================================
    # Wallpaper
    # ======================================================

    wallpaper = get_random_asset(
        WALLPAPER_DIR
    )


    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choice([
        "stacked",
        "spread",
    ])


    # ======================================================
    # Result
    # ======================================================

    return {

        "overview_state":
            overview_state,

        "wallpaper":
            wallpaper,

        "recent_apps":
            recent_apps,

        "recent_count":
            len(
                recent_apps
            ),

        "focused_index":
            focused_index,

        "show_menu":
            show_menu,

        "show_split_suggestion":
            show_split_suggestion,

        "show_screenshot_action":
            show_screenshot_action,

        "show_select_action":
            show_select_action,

        "show_clear_all":
            show_clear_all,

        "layout_variant":
            layout_variant,
    }