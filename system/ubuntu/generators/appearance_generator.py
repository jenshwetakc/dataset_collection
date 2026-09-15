from __future__ import annotations

import random

from system.ubuntu.generators.media_generator import (
    get_random_wallpaper,
    get_wallpaper_gallery,
)


# ==========================================================
# Appearance States
# ==========================================================

APPEARANCE_STATES = [

    "default",

    "wallpaper_grid",

    "wallpaper_selected",

    "light_style",

    "dark_style",

    "accent_picker",

    "dock_settings",

    "dock_left",

    "dock_bottom",

    "compact_dock",

    "wallpaper_preview",

    "reset_dialog",
]


# ==========================================================
# Sidebar
# ==========================================================

SETTINGS_SECTIONS = [

    {
        "name": "Wi-Fi",
        "icon": "wifi",
    },

    {
        "name": "Network",
        "icon": "language",
    },

    {
        "name": "Bluetooth",
        "icon": "bluetooth",
    },

    {
        "name": "Background",
        "icon": "wallpaper",
    },

    {
        "name": "Appearance",
        "icon": "palette",
    },

    {
        "name": "Notifications",
        "icon": "notifications",
    },

    {
        "name": "Search",
        "icon": "search",
    },

    {
        "name": "Applications",
        "icon": "apps",
    },

    {
        "name": "Privacy",
        "icon": "lock",
    },

    {
        "name": "Online Accounts",
        "icon": "account_circle",
    },

    {
        "name": "Sharing",
        "icon": "share",
    },

    {
        "name": "Sound",
        "icon": "volume_up",
    },

    {
        "name": "Power",
        "icon": "battery_full",
    },

    {
        "name": "Displays",
        "icon": "monitor",
    },
]


# ==========================================================
# Accent Choices
# ==========================================================

ACCENT_CHOICES = [

    {
        "name": "Orange",
        "value": "#E95420",
    },

    {
        "name": "Blue",
        "value": "#3584E4",
    },

    {
        "name": "Purple",
        "value": "#9141AC",
    },

    {
        "name": "Green",
        "value": "#2EC27E",
    },

    {
        "name": "Red",
        "value": "#E01B24",
    },

    {
        "name": "Yellow",
        "value": "#F5C211",
    },
]


# ==========================================================
# Dock Positions
# ==========================================================

DOCK_POSITIONS = [
    "left",
    "bottom",
]


# ==========================================================
# Generator
# ==========================================================

def generate_appearance_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            APPEARANCE_STATES
        )


    if state not in APPEARANCE_STATES:

        raise ValueError(
            f"Unknown appearance state: "
            f"{state}"
        )


    # ======================================================
    # Wallpapers
    # ======================================================

    wallpapers = (
        get_wallpaper_gallery(
            count=random.randint(
                6,
                12,
            )
        )
    )


    if wallpapers:

        selected_wallpaper_index = (
            random.randrange(
                len(
                    wallpapers
                )
            )
        )

        selected_wallpaper = (
            wallpapers[
                selected_wallpaper_index
            ]
        )

    else:

        selected_wallpaper_index = 0

        selected_wallpaper = (
            get_random_wallpaper()
        )


    # ======================================================
    # Style
    # ======================================================

    if state == "dark_style":

        color_scheme = "dark"

    elif state == "light_style":

        color_scheme = "light"

    else:

        color_scheme = random.choice(
            [
                "light",
                "dark",
                "automatic",
            ]
        )


    # ======================================================
    # Dock Position
    # ======================================================

    if state == "dock_bottom":

        dock_position = "bottom"

    else:

        dock_position = "left"


    # ======================================================
    # Dock Size
    # ======================================================

    if state == "compact_dock":

        dock_size = random.randint(
            24,
            34,
        )

    else:

        dock_size = random.randint(
            36,
            54,
        )


    # ======================================================
    # Accent
    # ======================================================

    selected_accent_index = random.randrange(
        len(
            ACCENT_CHOICES
        )
    )


    accent_choices = []

    for index, accent in enumerate(
        ACCENT_CHOICES
    ):

        value = dict(
            accent
        )

        value[
            "selected"
        ] = (
            index
            == selected_accent_index
        )

        accent_choices.append(
            value
        )


    # ======================================================
    # Sidebar
    # ======================================================

    sidebar_entries = []

    for section in SETTINGS_SECTIONS:

        entry = dict(
            section
        )

        entry["active"] = (
            section["name"]
            == "Appearance"
        )

        sidebar_entries.append(
            entry
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "sidebar_entries":
            sidebar_entries,

        "wallpapers":
            wallpapers,

        "selected_wallpaper_index":
            selected_wallpaper_index,

        "selected_wallpaper":
            selected_wallpaper,

        "color_scheme":
            color_scheme,

        "accent_choices":
            accent_choices,

        "dock_position":
            dock_position,

        "dock_size":
            dock_size,

        "auto_hide":
            random.random()
            < 0.45,

        "panel_mode":
            random.random()
            < 0.35,

        "show_volumes":
            random.random()
            < 0.80,

        "show_trash":
            random.random()
            < 0.70,

        "show_home":
            random.random()
            < 0.55,

        "desktop_icons":
            random.random()
            < 0.65,
    }