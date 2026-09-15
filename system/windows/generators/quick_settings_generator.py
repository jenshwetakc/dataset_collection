from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

QUICK_SETTINGS_STATES = [
    "quick_settings",
    "wifi_expanded",
    "bluetooth_expanded",
    "volume",
    "brightness",
    "airplane_mode",
    "battery_saver",
    "notification_center",
    "notification_expanded",
    "calendar",
    "do_not_disturb",
]


# ==========================================================
# Wi-Fi Networks
# ==========================================================

WIFI_NETWORKS = [
    "Home WiFi",
    "CampusNet",
    "KT_GiGA_5G",
    "Office WiFi",
    "Public WiFi",
    "Galaxy Hotspot",
]


# ==========================================================
# Bluetooth Devices
# ==========================================================

BLUETOOTH_DEVICES = [
    {
        "name": "Wireless Mouse",
        "icon": "mouse",
    },
    {
        "name": "Bluetooth Headphones",
        "icon": "headphones",
    },
    {
        "name": "Keyboard",
        "icon": "keyboard",
    },
    {
        "name": "Galaxy Buds",
        "icon": "earbuds",
    },
]


# ==========================================================
# Notification Pool
# ==========================================================

NOTIFICATION_POOL = [
    {
        "app": "Mail",
        "icon": "mail",
        "title": "New message",
        "message": "You received a new email.",
    },
    {
        "app": "Calendar",
        "icon": "event",
        "title": "Meeting soon",
        "message": "Research meeting starts in 15 minutes.",
    },
    {
        "app": "Windows Update",
        "icon": "update",
        "title": "Update available",
        "message": "A new system update is ready.",
    },
    {
        "app": "Photos",
        "icon": "photo_library",
        "title": "Import completed",
        "message": "12 photos were imported successfully.",
    },
    {
        "app": "System",
        "icon": "security",
        "title": "Security scan complete",
        "message": "No threats were found.",
    },
]


# ==========================================================
# Quick Toggle Generator
# ==========================================================

def generate_quick_toggles() -> list[dict]:

    return [
        {
            "id": "wifi",
            "label": "Wi-Fi",
            "icon": "wifi",
            "enabled": random.random() < 0.90,
        },
        {
            "id": "bluetooth",
            "label": "Bluetooth",
            "icon": "bluetooth",
            "enabled": random.random() < 0.72,
        },
        {
            "id": "airplane",
            "label": "Airplane mode",
            "icon": "airplanemode_active",
            "enabled": random.random() < 0.08,
        },
        {
            "id": "battery_saver",
            "label": "Battery saver",
            "icon": "battery_saver",
            "enabled": random.random() < 0.18,
        },
        {
            "id": "night_light",
            "label": "Night light",
            "icon": "nightlight",
            "enabled": random.random() < 0.38,
        },
        {
            "id": "accessibility",
            "label": "Accessibility",
            "icon": "accessibility_new",
            "enabled": False,
        },
    ]


# ==========================================================
# Wi-Fi
# ==========================================================

def generate_wifi_panel() -> dict:

    selected = random.choice(
        WIFI_NETWORKS
    )

    networks = []

    for network in random.sample(
        WIFI_NETWORKS,
        k=random.randint(
            3,
            len(WIFI_NETWORKS),
        ),
    ):

        networks.append(
            {
                "name": network,
                "connected": (
                    network == selected
                ),
                "secured": random.random() < 0.90,
                "strength": random.randint(
                    1,
                    3,
                ),
            }
        )

    return {
        "networks": networks,
        "selected": selected,
    }


# ==========================================================
# Bluetooth
# ==========================================================

def generate_bluetooth_panel() -> dict:

    count = random.randint(
        2,
        len(
            BLUETOOTH_DEVICES
        ),
    )

    devices = random.sample(
        BLUETOOTH_DEVICES,
        k=count,
    )

    result = []

    connected_index = random.randrange(
        len(devices)
    )

    for index, device in enumerate(
        devices
    ):

        result.append(
            {
                **device,
                "connected":
                    index
                    == connected_index,

                "battery":
                    (
                        random.randint(
                            30,
                            100,
                        )
                        if random.random()
                        < 0.60
                        else None
                    ),
            }
        )

    return {
        "devices": result,
    }


# ==========================================================
# Notifications
# ==========================================================

def generate_notifications() -> list[dict]:

    count = random.randint(
        2,
        5,
    )

    selected = random.sample(
        NOTIFICATION_POOL,
        k=min(
            count,
            len(
                NOTIFICATION_POOL
            ),
        ),
    )

    return [
        {
            **item,
            "time": random.choice(
                [
                    "Now",
                    "2 min",
                    "10 min",
                    "1 hr",
                    "Yesterday",
                ]
            ),
        }
        for item in selected
    ]


# ==========================================================
# Calendar
# ==========================================================

def generate_calendar() -> dict:

    days = list(
        range(
            1,
            31,
        )
    )

    return {
        "month":
            random.choice(
                [
                    "September 2026",
                    "October 2026",
                    "November 2026",
                ]
            ),

        "selected_day":
            random.choice(
                days
            ),

        "days":
            days,

        "events": [
            {
                "title":
                    "Research Meeting",

                "time":
                    "2:30 PM",
            },
            {
                "title":
                    "Project Review",

                "time":
                    "4:00 PM",
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_quick_settings_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            QUICK_SETTINGS_STATES
        )


    if state not in QUICK_SETTINGS_STATES:

        raise ValueError(
            f"Unknown quick settings state: "
            f"{state}"
        )


    return {
        "state":
            state,

        "toggles":
            generate_quick_toggles(),

        "volume":
            random.randint(
                0,
                100,
            ),

        "brightness":
            random.randint(
                15,
                100,
            ),

        "wifi":
            generate_wifi_panel(),

        "bluetooth":
            generate_bluetooth_panel(),

        "notifications":
            generate_notifications(),

        "calendar":
            generate_calendar(),

        "do_not_disturb":
            random.random() < 0.22,
    }