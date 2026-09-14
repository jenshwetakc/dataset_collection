from __future__ import annotations

import random


# ==========================================================
# Notification Icons
# ==========================================================

NOTIFICATION_ICONS = [
    "notifications",
    "chat",
    "sms",
    "mail",
    "alternate_email",
    "call",
    "missed_video_call",
    "download",
    "upload",
    "cloud",
    "cloud_download",
    "sync",
    "event",
    "calendar_month",
    "alarm",
    "schedule",
    "music_note",
    "headphones",
    "play_circle",
    "photo_camera",
    "image",
    "location_on",
    "navigation",
    "directions_car",
    "shopping_cart",
    "shopping_bag",
    "payments",
    "account_balance",
    "sports_esports",
    "favorite",
    "star",
    "person",
    "group",
    "public",
    "language",
]


# ==========================================================
# Optional System-State Icons
# ==========================================================

SYSTEM_STATE_ICONS = [
    "alarm",
    "bluetooth",
    "bluetooth_connected",
    "do_not_disturb_on",
    "vpn_key",
    "location_on",
    "sync",
]


# ==========================================================
# Time
# ==========================================================

def generate_time(
    use_24_hour: bool = True,
) -> dict:

    hour = random.randint(
        0,
        23,
    )

    minute = random.randint(
        0,
        59,
    )

    if use_24_hour:

        text = (
            f"{hour:02d}:"
            f"{minute:02d}"
        )

    else:

        hour_12 = (
            hour % 12
        )

        if hour_12 == 0:
            hour_12 = 12

        text = (
            f"{hour_12}:"
            f"{minute:02d}"
        )

    return {
        "hour": hour,
        "minute": minute,
        "text": text,
        "format":
            "24h"
            if use_24_hour
            else "12h",
    }


# ==========================================================
# Battery
# ==========================================================

def generate_battery() -> dict:

    level = random.randint(
        1,
        100,
    )

    charging = (
        random.random()
        < 0.15
    )

    battery_saver = (
        level <= 20
        and random.random() < 0.35
    )

    return {
        "level": level,
        "charging": charging,
        "battery_saver":
            battery_saver,
    }


# ==========================================================
# Cellular
# ==========================================================

def generate_cellular() -> dict:

    available = (
        random.random()
        < 0.96
    )

    if not available:

        return {
            "available": False,
            "level": 0,
            "type": None,
        }

    return {
        "available": True,

        "level":
            random.randint(
                1,
                4,
            ),

        "type":
            random.choice(
                [
                    "4G",
                    "LTE",
                    "5G",
                    "5G+",
                ]
            ),
    }


# ==========================================================
# Wi-Fi
# ==========================================================

def generate_wifi() -> dict:

    connected = (
        random.random()
        < 0.85
    )

    if not connected:

        return {
            "connected": False,
            "level": 0,
        }

    return {
        "connected": True,

        "level":
            random.randint(
                1,
                4,
            ),
    }


# ==========================================================
# Notifications
# ==========================================================

def generate_notifications() -> dict:

    # ------------------------------------------
    # Clean status bar vs notification bar
    # ------------------------------------------

    has_notifications = (
        random.random()
        < 0.60
    )

    if not has_notifications:

        return {
            "count": 0,
            "icons": [],
        }

    count = random.randint(
        1,
        4,
    )

    icons = random.sample(
        NOTIFICATION_ICONS,
        k=min(
            count,
            len(
                NOTIFICATION_ICONS
            ),
        ),
    )

    return {
        "count": len(
            icons
        ),

        "icons":
            icons,
    }


# ==========================================================
# Additional System States
# ==========================================================

def generate_system_states() -> list[str]:

    # Most screenshots should not be overloaded.
    if random.random() < 0.65:
        return []

    count = random.randint(
        1,
        2,
    )

    return random.sample(
        SYSTEM_STATE_ICONS,
        k=min(
            count,
            len(
                SYSTEM_STATE_ICONS
            ),
        ),
    )


# ==========================================================
# Status Bar Variant
# ==========================================================

def choose_status_bar_variant(
    notification_count: int,
) -> str:

    if notification_count == 0:

        return "normal"

    if notification_count <= 2:

        return "notifications_light"

    return "notifications_dense"


# ==========================================================
# Complete System Data
# ==========================================================

def generate_system_data() -> dict:

    # ------------------------------------------
    # Time format diversity
    # ------------------------------------------

    use_24_hour = (
        random.random()
        < 0.65
    )

    time = generate_time(
        use_24_hour=
            use_24_hour
    )

    battery = (
        generate_battery()
    )

    wifi = (
        generate_wifi()
    )

    cellular = (
        generate_cellular()
    )

    notifications = (
        generate_notifications()
    )

    system_states = (
        generate_system_states()
    )


    return {

        # --------------------------------------
        # Time
        # --------------------------------------

        "time":
            time,

        # Convenient direct value for HTML
        "time_text":
            time["text"],

        # --------------------------------------
        # Connectivity
        # --------------------------------------

        "wifi":
            wifi,

        "cellular":
            cellular,

        # --------------------------------------
        # Battery
        # --------------------------------------

        "battery":
            battery,

        # --------------------------------------
        # Notifications
        # --------------------------------------

        "notifications":
            notifications,

        # --------------------------------------
        # Other icons
        # --------------------------------------

        "system_states":
            system_states,

        # --------------------------------------
        # Status-bar layout
        # --------------------------------------

        "status_bar_variant":
            choose_status_bar_variant(
                notifications[
                    "count"
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for _ in range(10):

        pprint.pp(
            generate_system_data()
        )

        print(
            "-" * 60
        )