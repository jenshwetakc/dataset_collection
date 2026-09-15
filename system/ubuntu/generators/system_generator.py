from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# Constants
# ==========================================================

WIFI_NETWORKS = [
    "Home Wi-Fi",
    "KU-Campus",
    "Office Network",
    "Public Wi-Fi",
    "Studio",
    "Workspace",
]

POWER_MODES = [
    "performance",
    "balanced",
    "power_saver",
]

NOTIFICATION_APPS = [
    "Software Updater",
    "Files",
    "Calendar",
    "Firefox",
    "Terminal",
    "Settings",
]

NOTIFICATION_MESSAGES = [
    "Updates are available",
    "Download completed",
    "Meeting starts in 10 minutes",
    "File copied successfully",
    "New system notification",
    "Backup completed",
]


# ==========================================================
# Time
# ==========================================================

def generate_datetime():

    base = datetime.now()

    offset = timedelta(
        minutes=random.randint(
            -720,
            720,
        )
    )

    return (
        base
        + offset
    )


# ==========================================================
# Notifications
# ==========================================================

def generate_notifications():

    count = random.randint(
        0,
        3,
    )

    notifications = []

    for index in range(
        count
    ):

        app = random.choice(
            NOTIFICATION_APPS
        )

        message = random.choice(
            NOTIFICATION_MESSAGES
        )

        notifications.append(
            {
                "id":
                    index,

                "app":
                    app,

                "message":
                    message,

                "minutes_ago":
                    random.randint(
                        1,
                        90,
                    ),
            }
        )

    return notifications


# ==========================================================
# Ubuntu System Data
# ==========================================================

def generate_system_data(
    viewport: dict | None = None,
) -> dict:

    now = generate_datetime()

    # ------------------------------------------------------
    # Determine whether this is probably a laptop
    # ------------------------------------------------------

    viewport_category = (
        viewport.get(
            "category"
        )
        if viewport
        else None
    )

    is_laptop = (
        viewport_category
        == "laptop"
    )

    # Desktop displays can still occasionally show UPS /
    # battery-like state, but normally do not.
    if is_laptop:

        battery_available = (
            random.random()
            < 0.95
        )

    else:

        battery_available = (
            random.random()
            < 0.20
        )

    # ------------------------------------------------------
    # Wi-Fi
    # ------------------------------------------------------

    wifi_connected = (
        random.random()
        < 0.88
    )

    wifi = {

        "enabled":
            True,

        "connected":
            wifi_connected,

        "level":
            (
                random.randint(
                    1,
                    3,
                )
                if wifi_connected
                else 0
            ),

        "network_name":
            (
                random.choice(
                    WIFI_NETWORKS
                )
                if wifi_connected
                else None
            ),
    }

    # ------------------------------------------------------
    # Bluetooth
    # ------------------------------------------------------

    bluetooth_enabled = (
        random.random()
        < 0.65
    )

    bluetooth = {

        "enabled":
            bluetooth_enabled,

        "connected":
            (
                bluetooth_enabled
                and random.random()
                < 0.35
            ),
    }

    # ------------------------------------------------------
    # Audio
    # ------------------------------------------------------

    muted = (
        random.random()
        < 0.10
    )

    audio = {

        "muted":
            muted,

        "volume":
            (
                0
                if muted
                else random.randint(
                    15,
                    100,
                )
            ),
    }

    # ------------------------------------------------------
    # Battery
    # ------------------------------------------------------

    battery_level = random.randint(
        8,
        100,
    )

    charging = (
        battery_available
        and random.random()
        < 0.20
    )

    battery = {

        "available":
            battery_available,

        "level":
            battery_level,

        "charging":
            charging,

        "low":
            (
                battery_available
                and not charging
                and battery_level
                <= 20
            ),
    }

    # ------------------------------------------------------
    # Notifications
    # ------------------------------------------------------

    notifications = (
        generate_notifications()
    )

    # ------------------------------------------------------
    # Result
    # ------------------------------------------------------

    return {

        "time_text":
            now.strftime(
                "%H:%M"
            ),

        "date_text":
            now.strftime(
                "%b %-d"
            ),

        "weekday_text":
            now.strftime(
                "%A"
            ),

        "full_date_text":
            now.strftime(
                "%A, %B %-d"
            ),

        "wifi":
            wifi,

        "bluetooth":
            bluetooth,

        "audio":
            audio,

        "battery":
            battery,

        "power_mode":
            random.choice(
                POWER_MODES
            ),

        "night_light":
            (
                random.random()
                < 0.25
            ),

        "dark_mode":
            (
                random.random()
                < 0.50
            ),

        "airplane_mode":
            False,

        "notifications": {

            "count":
                len(
                    notifications
                ),

            "entries":
                notifications,
        },
    }