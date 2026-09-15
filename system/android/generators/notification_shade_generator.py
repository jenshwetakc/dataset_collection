from __future__ import annotations

import random


# ==========================================================
# Quick Settings Tiles
# ==========================================================

QUICK_SETTING_TILES = [

    {
        "semantic":
            "wifi",

        "title":
            "Internet",

        "icon_on":
            "mdi:wifi",

        "icon_off":
            "mdi:wifi-off",
    },

    {
        "semantic":
            "bluetooth",

        "title":
            "Bluetooth",

        "icon_on":
            "mdi:bluetooth",

        "icon_off":
            "mdi:bluetooth-off",
    },

    {
        "semantic":
            "flashlight",

        "title":
            "Flashlight",

        "icon_on":
            "mdi:flashlight",

        "icon_off":
            "mdi:flashlight-off",
    },

    {
        "semantic":
            "airplane_mode",

        "title":
            "Airplane mode",

        "icon_on":
            "mdi:airplane",

        "icon_off":
            "mdi:airplane-off",
    },

    {
        "semantic":
            "battery_saver",

        "title":
            "Battery Saver",

        "icon_on":
            "mdi:battery-heart-variant",

        "icon_off":
            "mdi:battery",
    },

    {
        "semantic":
            "do_not_disturb",

        "title":
            "Do Not Disturb",

        "icon_on":
            "mdi:minus-circle",

        "icon_off":
            "mdi:bell",
    },

    {
        "semantic":
            "auto_rotate",

        "title":
            "Auto-rotate",

        "icon_on":
            "mdi:screen-rotation",

        "icon_off":
            "mdi:phone-lock",
    },

    {
        "semantic":
            "location",

        "title":
            "Location",

        "icon_on":
            "mdi:map-marker",

        "icon_off":
            "mdi:map-marker-off",
    },
]


# ==========================================================
# Notification Apps
# ==========================================================

NOTIFICATION_APPS = [

    {
        "app":
            "Messages",

        "icon":
            "mdi:message-text",
    },

    {
        "app":
            "Gmail",

        "icon":
            "mdi:email",
    },

    {
        "app":
            "Calendar",

        "icon":
            "mdi:calendar",
    },

    {
        "app":
            "Downloads",

        "icon":
            "mdi:download",
    },

    {
        "app":
            "Photos",

        "icon":
            "mdi:image",
    },

    {
        "app":
            "System",

        "icon":
            "mdi:cog",
    },
]


NOTIFICATION_TITLES = [
    "New message",
    "Meeting reminder",
    "Download complete",
    "Backup finished",
    "New activity",
    "Security update available",
    "Photo memories",
    "Connected device",
]


NOTIFICATION_BODIES = [
    "Tap to view more details.",
    "You have a new notification.",
    "This item is ready.",
    "Your device has finished syncing.",
    "There is new activity waiting for you.",
    "Open to review the latest information.",
]


# ==========================================================
# Generate Notification
# ==========================================================

def generate_notification(
    index: int,
) -> dict:

    app = random.choice(
        NOTIFICATION_APPS
    )

    action_count = random.choice([
        0,
        1,
        2,
    ])

    actions = random.sample(
        [
            "Reply",
            "Open",
            "Mark read",
            "Snooze",
        ],
        k=action_count,
    )

    return {

        "semantic":
            f"notification_{index}",

        "app":
            app["app"],

        "icon":
            app["icon"],

        "title":
            random.choice(
                NOTIFICATION_TITLES
            ),

        "body":
            random.choice(
                NOTIFICATION_BODIES
            ),

        "time":
            random.choice([
                "now",
                "1m",
                "5m",
                "12m",
                "1h",
                "2h",
            ]),

        "silent":
            random.random()
            < 0.22,

        "expanded":
            random.random()
            < 0.28,

        "actions":
            actions,
    }


# ==========================================================
# Notification Shade
# ==========================================================

def generate_notification_shade_data() -> dict:

    # ======================================================
    # Shade State
    # ======================================================

    shade_state = random.choices(

        [
            "collapsed",
            "partial",
            "expanded",
        ],

        weights=[
            0.20,
            0.35,
            0.45,
        ],

        k=1,

    )[0]


    # ======================================================
    # Quick Setting State
    # ======================================================

    control_state = {

        "wifi":
            random.random()
            < 0.85,

        "bluetooth":
            random.random()
            < 0.65,

        "flashlight":
            random.random()
            < 0.18,

        "airplane_mode":
            random.random()
            < 0.07,

        "battery_saver":
            random.random()
            < 0.22,

        "do_not_disturb":
            random.random()
            < 0.14,

        "auto_rotate":
            random.random()
            < 0.70,

        "location":
            random.random()
            < 0.80,
    }


    # ======================================================
    # Tile Count
    # ======================================================

    tile_count = {

        "collapsed":
            4,

        "partial":
            6,

        "expanded":
            8,

    }[
        shade_state
    ]


    selected_tiles = (
        QUICK_SETTING_TILES[
            :tile_count
        ]
    )


    # ======================================================
    # Build Tiles
    # ======================================================

    quick_settings = []


    for tile in selected_tiles:

        enabled = (
            control_state[
                tile["semantic"]
            ]
        )


        quick_settings.append({

            **tile,

            "enabled":
                enabled,

            "icon":
                (
                    tile["icon_on"]
                    if enabled
                    else tile["icon_off"]
                ),
        })


    # ======================================================
    # Notifications
    # ======================================================

    notification_count = (
        random.randint(
            1,
            5,
        )
    )


    notifications = [

        generate_notification(
            index
        )

        for index in range(
            notification_count
        )
    ]


    # ======================================================
    # Optional Components
    # ======================================================

    show_media = (

        shade_state != "collapsed"

        and random.random()
        < 0.45
    )


    show_brightness = (

        shade_state == "expanded"

        or (

            shade_state == "partial"

            and random.random()
            < 0.40
        )
    )


    # ======================================================
    # Media State
    # ======================================================

    media_playing = (
        random.random()
        < 0.60
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "shade_state":
            shade_state,

        "quick_settings":
            quick_settings,

        "brightness":
            random.randint(
                15,
                95,
            ),

        "show_brightness":
            show_brightness,

        "show_media":
            show_media,

        "media": {

            "title":
                random.choice([
                    "Midnight Drive",
                    "Daily Mix",
                    "Focus Playlist",
                    "Morning News",
                ]),

            "artist":
                random.choice([
                    "Various Artists",
                    "Spotify",
                    "Podcast",
                    "Music Player",
                ]),

            "playing":
                media_playing,

            "play_pause_icon":
                (
                    "mdi:pause"
                    if media_playing
                    else "mdi:play"
                ),
        },

        "notifications":
            notifications,

        "notification_count":
            notification_count,

        "show_clear_all":
            notification_count > 1,

        "controls":
            control_state,
    }