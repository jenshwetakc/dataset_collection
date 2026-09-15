from __future__ import annotations

import random


# ==========================================================
# Settings States
# ==========================================================

SETTINGS_STATES = [
    "system",
    "display",
    "bluetooth",
    "network",
    "personalization",
    "apps",
    "accounts",
    "accessibility",
    "storage",
    "windows_update",
    "update_downloading",
    "update_restart_required",
]


# ==========================================================
# Navigation
# ==========================================================

SETTINGS_NAVIGATION = [
    {
        "id": "system",
        "title": "System",
        "icon": "computer",
    },
    {
        "id": "bluetooth",
        "title": "Bluetooth & devices",
        "icon": "bluetooth",
    },
    {
        "id": "network",
        "title": "Network & internet",
        "icon": "wifi",
    },
    {
        "id": "personalization",
        "title": "Personalization",
        "icon": "palette",
    },
    {
        "id": "apps",
        "title": "Apps",
        "icon": "apps",
    },
    {
        "id": "accounts",
        "title": "Accounts",
        "icon": "person",
    },
    {
        "id": "accessibility",
        "title": "Accessibility",
        "icon": "accessibility_new",
    },
    {
        "id": "windows_update",
        "title": "Windows Update",
        "icon": "update",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def random_toggle(
    enabled_probability: float = 0.65,
) -> bool:

    return (
        random.random()
        < enabled_probability
    )


def random_storage_value() -> dict:

    total = random.choice(
        [
            256,
            512,
            1024,
        ]
    )

    used = random.randint(
        int(total * 0.30),
        int(total * 0.82),
    )

    return {
        "total": total,
        "used": used,
        "free": total - used,
        "percent": round(
            used / total * 100
        ),
    }


# ==========================================================
# System
# ==========================================================

def generate_system_settings() -> dict:

    return {
        "title": "System",
        "subtitle": "Display, sound, notifications, power",

        "cards": [
            {
                "title": "Display",
                "subtitle": "Monitors, brightness, night light",
                "icon": "desktop_windows",
                "value": random.choice(
                    [
                        "1920 × 1080",
                        "2560 × 1440",
                        "3840 × 2160",
                    ]
                ),
            },
            {
                "title": "Sound",
                "subtitle": "Volume levels, output, input devices",
                "icon": "volume_up",
                "value": f"{random.randint(20, 95)}%",
            },
            {
                "title": "Notifications",
                "subtitle": "Alerts from apps and system",
                "icon": "notifications",
                "value": random.choice(
                    [
                        "On",
                        "Off",
                    ]
                ),
            },
            {
                "title": "Power & battery",
                "subtitle": "Sleep, battery usage, power mode",
                "icon": "battery_full",
                "value": random.choice(
                    [
                        "Balanced",
                        "Best performance",
                        "Best power efficiency",
                    ]
                ),
            },
        ],
    }


# ==========================================================
# Display
# ==========================================================

def generate_display_settings() -> dict:

    brightness = random.randint(
        25,
        100,
    )

    return {
        "title": "Display",
        "subtitle": "Brightness, scale and display resolution",

        "brightness":
            brightness,

        "night_light":
            random_toggle(),

        "hdr":
            random_toggle(
                0.35
            ),

        "scale":
            random.choice(
                [
                    "100%",
                    "125%",
                    "150%",
                    "175%",
                ]
            ),

        "resolution":
            random.choice(
                [
                    "1920 × 1080",
                    "2560 × 1440",
                    "3840 × 2160",
                ]
            ),

        "orientation":
            random.choice(
                [
                    "Landscape",
                    "Portrait",
                ]
            ),
    }


# ==========================================================
# Bluetooth
# ==========================================================

def generate_bluetooth_settings() -> dict:

    bluetooth_enabled = (
        random_toggle(
            0.80
        )
    )

    devices = [
        {
            "name": "Wireless Mouse",
            "icon": "mouse",
            "status": "Connected",
        },
        {
            "name": "Bluetooth Headphones",
            "icon": "headphones",
            "status": random.choice(
                [
                    "Connected",
                    "Paired",
                ]
            ),
        },
        {
            "name": "Keyboard",
            "icon": "keyboard",
            "status": "Paired",
        },
    ]

    return {
        "title": "Bluetooth & devices",
        "subtitle": "Devices, printers, mouse",

        "bluetooth_enabled":
            bluetooth_enabled,

        "devices":
            random.sample(
                devices,
                k=random.randint(
                    1,
                    len(devices),
                ),
            ),

        "show_add_device":
            random.random() < 0.75,
    }


# ==========================================================
# Network
# ==========================================================

def generate_network_settings() -> dict:

    wifi_enabled = random_toggle(
        0.90
    )

    connected = (
        wifi_enabled
        and random.random()
        < 0.88
    )

    return {
        "title": "Network & internet",
        "subtitle": "Wi-Fi, VPN, proxy, mobile hotspot",

        "wifi_enabled":
            wifi_enabled,

        "connected":
            connected,

        "network_name":
            (
                random.choice(
                    [
                        "Home WiFi",
                        "CampusNet",
                        "KT_GiGA_5G",
                        "Office WiFi",
                    ]
                )
                if connected
                else None
            ),

        "properties": [
            {
                "title": "Wi-Fi",
                "icon": "wifi",
            },
            {
                "title": "VPN",
                "icon": "vpn_lock",
            },
            {
                "title": "Mobile hotspot",
                "icon": "portable_wifi_off",
            },
            {
                "title": "Proxy",
                "icon": "lan",
            },
        ],
    }


# ==========================================================
# Personalization
# ==========================================================

def generate_personalization_settings() -> dict:

    return {
        "title": "Personalization",
        "subtitle": "Background, colors, themes, lock screen",

        "theme":
            random.choice(
                [
                    "Light",
                    "Dark",
                    "Custom",
                ]
            ),

        "accent":
            random.choice(
                [
                    "Blue",
                    "Purple",
                    "Green",
                    "Orange",
                ]
            ),

        "items": [
            {
                "title": "Background",
                "icon": "wallpaper",
            },
            {
                "title": "Colors",
                "icon": "palette",
            },
            {
                "title": "Themes",
                "icon": "brush",
            },
            {
                "title": "Lock screen",
                "icon": "lock",
            },
            {
                "title": "Start",
                "icon": "window",
            },
            {
                "title": "Taskbar",
                "icon": "dock_to_bottom",
            },
        ],
    }


# ==========================================================
# Apps
# ==========================================================

def generate_apps_settings() -> dict:

    return {
        "title": "Apps",
        "subtitle": "Installed apps, defaults, optional features",

        "installed_count":
            random.randint(
                42,
                186,
            ),

        "items": [
            {
                "title": "Installed apps",
                "icon": "apps",
            },
            {
                "title": "Advanced app settings",
                "icon": "tune",
            },
            {
                "title": "Default apps",
                "icon": "task_alt",
            },
            {
                "title": "Optional features",
                "icon": "extension",
            },
            {
                "title": "Startup",
                "icon": "rocket_launch",
            },
        ],
    }


# ==========================================================
# Accounts
# ==========================================================

def generate_accounts_settings() -> dict:

    return {
        "title": "Accounts",
        "subtitle": "Your accounts, email, sync, work access",

        "user": {
            "name":
                random.choice(
                    [
                        "Shweta",
                        "Alex Kim",
                        "Jordan Lee",
                        "Taylor Park",
                    ]
                ),

            "email":
                random.choice(
                    [
                        "user@example.com",
                        "alex@example.com",
                        "jordan@example.com",
                    ]
                ),
        },

        "items": [
            {
                "title": "Your info",
                "icon": "person",
            },
            {
                "title": "Sign-in options",
                "icon": "password",
            },
            {
                "title": "Email & accounts",
                "icon": "mail",
            },
            {
                "title": "Access work or school",
                "icon": "business_center",
            },
            {
                "title": "Windows backup",
                "icon": "cloud",
            },
        ],
    }


# ==========================================================
# Accessibility
# ==========================================================

def generate_accessibility_settings() -> dict:

    return {
        "title": "Accessibility",
        "subtitle": "Vision, hearing, interaction",

        "text_size":
            random.randint(
                100,
                160,
            ),

        "contrast_themes":
            random_toggle(
                0.15
            ),

        "narrator":
            random_toggle(
                0.10
            ),

        "items": [
            {
                "title": "Text size",
                "icon": "text_fields",
            },
            {
                "title": "Visual effects",
                "icon": "animation",
            },
            {
                "title": "Mouse pointer and touch",
                "icon": "mouse",
            },
            {
                "title": "Text cursor",
                "icon": "edit",
            },
            {
                "title": "Magnifier",
                "icon": "zoom_in",
            },
            {
                "title": "Narrator",
                "icon": "record_voice_over",
            },
        ],
    }


# ==========================================================
# Storage
# ==========================================================

def generate_storage_settings() -> dict:

    storage = (
        random_storage_value()
    )

    return {
        "title": "Storage",
        "subtitle": "Storage space, drives, configuration",

        "storage":
            storage,

        "categories": [
            {
                "title": "Installed apps",
                "icon": "apps",
                "size": random.randint(
                    40,
                    180,
                ),
            },
            {
                "title": "Temporary files",
                "icon": "delete_sweep",
                "size": random.randint(
                    2,
                    38,
                ),
            },
            {
                "title": "Documents",
                "icon": "description",
                "size": random.randint(
                    8,
                    92,
                ),
            },
            {
                "title": "Other",
                "icon": "folder",
                "size": random.randint(
                    6,
                    75,
                ),
            },
        ],
    }


# ==========================================================
# Windows Update
# ==========================================================

def generate_windows_update(
    state: str,
) -> dict:

    if state == "update_downloading":

        progress = random.randint(
            8,
            92,
        )

        status = (
            f"Downloading – {progress}%"
        )

    elif state == "update_restart_required":

        progress = 100

        status = (
            "Restart required"
        )

    else:

        progress = None

        status = random.choice(
            [
                "You're up to date",
                "Updates available",
                "Last checked: Today",
            ]
        )


    return {
        "title": "Windows Update",
        "subtitle": "Updates, security and optional updates",

        "status":
            status,

        "progress":
            progress,

        "restart_required":
            (
                state
                == "update_restart_required"
            ),

        "updates": [
            {
                "name":
                    "Security Intelligence Update",

                "status":
                    random.choice(
                        [
                            "Pending install",
                            "Installed",
                            "Downloading",
                        ]
                    ),
            },
            {
                "name":
                    "Cumulative Update for Windows",

                "status":
                    random.choice(
                        [
                            "Pending restart",
                            "Installed",
                            "Downloading",
                        ]
                    ),
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_settings_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SETTINGS_STATES
        )


    if state not in SETTINGS_STATES:

        raise ValueError(
            f"Unknown Settings state: "
            f"{state}"
        )


    if state == "system":

        content = (
            generate_system_settings()
        )

    elif state == "display":

        content = (
            generate_display_settings()
        )

    elif state == "bluetooth":

        content = (
            generate_bluetooth_settings()
        )

    elif state == "network":

        content = (
            generate_network_settings()
        )

    elif state == "personalization":

        content = (
            generate_personalization_settings()
        )

    elif state == "apps":

        content = (
            generate_apps_settings()
        )

    elif state == "accounts":

        content = (
            generate_accounts_settings()
        )

    elif state == "accessibility":

        content = (
            generate_accessibility_settings()
        )

    elif state == "storage":

        content = (
            generate_storage_settings()
        )

    else:

        content = (
            generate_windows_update(
                state
            )
        )


    return {
        "state":
            state,

        "navigation":
            SETTINGS_NAVIGATION,

        "content":
            content,

        "search_placeholder":
            "Find a setting",
    }