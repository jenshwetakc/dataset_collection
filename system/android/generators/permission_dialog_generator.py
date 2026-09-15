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
# Apps
# ==========================================================

APP_POOL = [
    {
        "name": "Camera",
        "icon": "mdi:camera",
    },
    {
        "name": "Maps",
        "icon": "mdi:google-maps",
    },
    {
        "name": "Messages",
        "icon": "mdi:message-text",
    },
    {
        "name": "Recorder",
        "icon": "mdi:microphone",
    },
    {
        "name": "Photos",
        "icon": "mdi:image-multiple",
    },
    {
        "name": "Meet",
        "icon": "mdi:video",
    },
    {
        "name": "Weather",
        "icon": "mdi:weather-partly-cloudy",
    },
]


# ==========================================================
# Permission Types
# ==========================================================

PERMISSIONS = [

    {
        "type": "camera",
        "label": "camera",
        "icon": "mdi:camera-outline",
        "question": "Allow {app} to take pictures and record video?",
        "supports_one_time": True,
        "supports_location_accuracy": False,
    },

    {
        "type": "microphone",
        "label": "microphone",
        "icon": "mdi:microphone-outline",
        "question": "Allow {app} to record audio?",
        "supports_one_time": True,
        "supports_location_accuracy": False,
    },

    {
        "type": "location",
        "label": "location",
        "icon": "mdi:map-marker-outline",
        "question": "Allow {app} to access this device's location?",
        "supports_one_time": True,
        "supports_location_accuracy": True,
    },

    {
        "type": "notifications",
        "label": "notifications",
        "icon": "mdi:bell-outline",
        "question": "Allow {app} to send you notifications?",
        "supports_one_time": False,
        "supports_location_accuracy": False,
    },

    {
        "type": "contacts",
        "label": "contacts",
        "icon": "mdi:account-box-outline",
        "question": "Allow {app} to access your contacts?",
        "supports_one_time": False,
        "supports_location_accuracy": False,
    },

    {
        "type": "nearby_devices",
        "label": "nearby devices",
        "icon": "mdi:bluetooth",
        "question": "Allow {app} to find and connect to nearby devices?",
        "supports_one_time": False,
        "supports_location_accuracy": False,
    },
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
# Main Generator
# ==========================================================

def generate_permission_dialog_data() -> dict:

    # ======================================================
    # App + Permission
    # ======================================================

    app = random.choice(
        APP_POOL
    )

    permission = random.choice(
        PERMISSIONS
    )


    # ======================================================
    # Dialog State
    # ======================================================

    dialog_state = random.choices(
        [
            "request",
            "denied_retry",
            "settings_redirect",
        ],
        weights=[
            0.72,
            0.18,
            0.10,
        ],
        k=1,
    )[0]


    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choices(
        [
            "dialog",
            "bottom_sheet",
        ],
        weights=[
            0.78,
            0.22,
        ],
        k=1,
    )[0]


    # ======================================================
    # Location Accuracy
    # ======================================================

    show_location_accuracy = (
        permission[
            "supports_location_accuracy"
        ]
        and dialog_state == "request"
    )

    precise_location = (
        random.random()
        < 0.65
    )


    # ======================================================
    # One-time Permission
    # ======================================================

    show_one_time = (
        permission[
            "supports_one_time"
        ]
        and dialog_state == "request"
        and random.random() < 0.82
    )


    # ======================================================
    # While Using
    # ======================================================

    show_while_using = (
        permission["type"]
        in {
            "camera",
            "microphone",
            "location",
        }
        and dialog_state == "request"
    )


    # ======================================================
    # Background
    # ======================================================

    show_fake_app_content = (
        random.random()
        < 0.85
    )


    # ======================================================
    # Text
    # ======================================================

    question = (
        permission[
            "question"
        ].format(
            app=app["name"]
        )
    )


    if dialog_state == "denied_retry":

        title = (
            f"{app['name']} needs "
            f"{permission['label']} permission"
        )

        message = (
            "You previously denied this permission. "
            "You can allow it to continue."
        )

    elif dialog_state == "settings_redirect":

        title = (
            f"Permission required"
        )

        message = (
            f"To use this feature, allow "
            f"{permission['label']} access in Settings."
        )

    else:

        title = question

        message = None


    # ======================================================
    # Result
    # ======================================================

    return {

        "dialog_state":
            dialog_state,

        "layout_variant":
            layout_variant,

        "wallpaper":
            get_wallpaper(),

        "show_fake_app_content":
            show_fake_app_content,

        "app":
            app,

        "permission":
            permission,

        "title":
            title,

        "message":
            message,

        "show_location_accuracy":
            show_location_accuracy,

        "precise_location":
            precise_location,

        "show_one_time":
            show_one_time,

        "show_while_using":
            show_while_using,
    }