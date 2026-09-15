from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# Constants
# ==========================================================

NOTIFICATION_ICONS = [
    "notifications",
    "chat",
    "mail",
    "event",
    "download",
]

SYSTEM_STATE_ICONS = [
    "alarm",
    "bluetooth",
    "do_not_disturb_on",
]

CELLULAR_TYPES = [
    "5G",
    "LTE",
    "4G",
]

STATUS_BAR_VARIANTS = [
    "default",
    "compact",
]


# ==========================================================
# Generate Time
# ==========================================================

def generate_time_text() -> str:

    base = datetime.now()

    offset = timedelta(
        minutes=random.randint(
            -600,
            600,
        )
    )

    value = (
        base
        + offset
    )

    return value.strftime(
        "%H:%M"
    )


# ==========================================================
# System Generator
# ==========================================================

def generate_system_data() -> dict:

    notification_count = random.randint(
        0,
        3,
    )

    notifications = random.sample(
        NOTIFICATION_ICONS,
        k=min(
            notification_count,
            len(
                NOTIFICATION_ICONS
            ),
        ),
    )

    system_state_count = random.randint(
        0,
        2,
    )

    system_states = random.sample(
        SYSTEM_STATE_ICONS,
        k=min(
            system_state_count,
            len(
                SYSTEM_STATE_ICONS
            ),
        ),
    )

    cellular_available = random.random() < 0.95

    wifi_connected = random.random() < 0.85

    battery_level = random.randint(
        8,
        100,
    )

    charging = random.random() < 0.18

    battery_saver = (
        not charging
        and battery_level <= 25
        and random.random() < 0.45
    )

    return {

        "status_bar_variant":
            random.choice(
                STATUS_BAR_VARIANTS
            ),

        "time_text":
            generate_time_text(),

        "notifications": {
            "icons":
                notifications,
        },

        "system_states":
            system_states,

        "cellular": {

            "available":
                cellular_available,

            "level":
                random.randint(
                    1,
                    4,
                ),

            "type":
                (
                    random.choice(
                        CELLULAR_TYPES
                    )
                    if cellular_available
                    else None
                ),
        },

        "wifi": {

            "connected":
                wifi_connected,

            "level":
                random.randint(
                    1,
                    3,
                ),
        },

        "battery": {

            "level":
                battery_level,

            "charging":
                charging,

            "battery_saver":
                battery_saver,
        },
    }