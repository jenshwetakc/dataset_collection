from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Static Pools
# ==========================================================

DEVICE_NAMES = [
    "Pixel 9",
    "Pixel 9 Pro",
    "Pixel Fold",
    "Android Device",
    "Galaxy S25",
    "Galaxy A56",
]


WIFI_NAMES = [
    "Home Wi-Fi",
    "Office Network",
    "KU-WiFi",
    "Android_AP",
    "CoffeeShop_5G",
    "Studio Network",
]


STORAGE_TOTALS = [
    64,
    128,
    256,
    512,
]


# ==========================================================
# Settings Entries
# ==========================================================

NETWORK_ENTRIES = [
    {
        "semantic": "network_internet",
        "title": "Network & internet",
        "icon": "mdi:wifi",
    },
    {
        "semantic": "connected_devices",
        "title": "Connected devices",
        "icon": "mdi:devices",
    },
]


APP_ENTRIES = [
    {
        "semantic": "apps",
        "title": "Apps",
        "icon": "mdi:apps",
    },
    {
        "semantic": "notifications",
        "title": "Notifications",
        "icon": "mdi:bell-outline",
    },
]


PERSONAL_ENTRIES = [
    {
        "semantic": "battery",
        "title": "Battery",
        "icon": "mdi:battery",
    },
    {
        "semantic": "storage",
        "title": "Storage",
        "icon": "mdi:database-outline",
    },
    {
        "semantic": "sound_vibration",
        "title": "Sound & vibration",
        "icon": "mdi:volume-high",
    },
    {
        "semantic": "display",
        "title": "Display",
        "icon": "mdi:brightness-6",
    },
]


SECURITY_ENTRIES = [
    {
        "semantic": "wallpaper_style",
        "title": "Wallpaper & style",
        "icon": "mdi:palette-outline",
    },
    {
        "semantic": "accessibility",
        "title": "Accessibility",
        "icon": "mdi:human",
    },
    {
        "semantic": "security_privacy",
        "title": "Security & privacy",
        "icon": "mdi:shield-lock-outline",
    },
    {
        "semantic": "location",
        "title": "Location",
        "icon": "mdi:map-marker-outline",
    },
]


SYSTEM_ENTRIES = [
    {
        "semantic": "safety_emergency",
        "title": "Safety & emergency",
        "icon": "mdi:alert-circle-outline",
    },
    {
        "semantic": "passwords_accounts",
        "title": "Passwords & accounts",
        "icon": "mdi:account-key-outline",
    },
    {
        "semantic": "digital_wellbeing",
        "title": "Digital Wellbeing & parental controls",
        "icon": "mdi:heart-pulse",
    },
    {
        "semantic": "google",
        "title": "Google",
        "icon": "mdi:google",
    },
    {
        "semantic": "system",
        "title": "System",
        "icon": "mdi:cog-outline",
    },
    {
        "semantic": "about_phone",
        "title": "About phone",
        "icon": "mdi:information-outline",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def make_entry(
    entry: dict,
    *,
    subtitle: str | None = None,
    badge: str | None = None,
    trailing: str = "mdi:chevron-right",
) -> dict:

    return {
        "semantic":
            entry["semantic"],

        "title":
            entry["title"],

        "icon":
            entry["icon"],

        "subtitle":
            subtitle,

        "badge":
            badge,

        "trailing":
            trailing,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_settings_data() -> dict:

    # ======================================================
    # Core State
    # ======================================================

    wifi_enabled = (
        random.random() < 0.85
    )

    bluetooth_enabled = (
        random.random() < 0.65
    )

    mobile_data_enabled = (
        random.random() < 0.90
    )

    account_present = (
        random.random() < 0.85
    )

    search_expanded = (
        random.random() < 0.25
    )

    update_available = (
        random.random() < 0.25
    )

    security_warning = (
        random.random() < 0.15
    )

    battery_saver = (
        random.random() < 0.20
    )


    # ======================================================
    # Account
    # ======================================================

    if account_present:

        account_name = fake.name()

        account_email = (
            fake.user_name()
            + "@gmail.com"
        )

    else:

        account_name = "Sign in"

        account_email = (
            "Sign in to your Google Account"
        )


    # ======================================================
    # Device
    # ======================================================

    device_name = random.choice(
        DEVICE_NAMES
    )

    wifi_name = random.choice(
        WIFI_NAMES
    )

    total_storage = random.choice(
        STORAGE_TOTALS
    )

    used_storage = random.randint(
        int(total_storage * 0.20),
        int(total_storage * 0.88),
    )

    battery_percent = random.randint(
        18,
        98,
    )


    # ======================================================
    # Quick Controls
    # ======================================================

    quick_controls = [
        {
            "semantic":
                "wifi_toggle",

            "title":
                "Wi-Fi",

            "subtitle":
                (
                    wifi_name
                    if wifi_enabled
                    else "Off"
                ),

            "icon":
                (
                    "mdi:wifi"
                    if wifi_enabled
                    else "mdi:wifi-off"
                ),

            "enabled":
                wifi_enabled,
        },

        {
            "semantic":
                "bluetooth_toggle",

            "title":
                "Bluetooth",

            "subtitle":
                (
                    "On"
                    if bluetooth_enabled
                    else "Off"
                ),

            "icon":
                (
                    "mdi:bluetooth"
                    if bluetooth_enabled
                    else "mdi:bluetooth-off"
                ),

            "enabled":
                bluetooth_enabled,
        },

        {
            "semantic":
                "mobile_data_toggle",

            "title":
                "Mobile data",

            "subtitle":
                (
                    "On"
                    if mobile_data_enabled
                    else "Off"
                ),

            "icon":
                (
                    "mdi:signal"
                    if mobile_data_enabled
                    else "mdi:signal-off"
                ),

            "enabled":
                mobile_data_enabled,
        },
    ]


    # ======================================================
    # Groups
    #
    # IMPORTANT:
    # Use "entries", not "items".
    #
    # This avoids Jinja collisions with dict.items.
    # ======================================================

    groups = []


    # ------------------------------------------------------
    # Connections
    # ------------------------------------------------------

    groups.append({
        "semantic":
            "connections_group",

        "title":
            "Connections",

        "entries": [

            make_entry(
                NETWORK_ENTRIES[0],

                subtitle=(
                    wifi_name
                    if wifi_enabled
                    else "Wi-Fi off"
                ),
            ),

            make_entry(
                NETWORK_ENTRIES[1],

                subtitle=(
                    "Bluetooth on"
                    if bluetooth_enabled
                    else "Bluetooth off"
                ),
            ),
        ],
    })


    # ------------------------------------------------------
    # Apps
    # ------------------------------------------------------

    groups.append({
        "semantic":
            "apps_group",

        "title":
            "Apps & notifications",

        "entries": [

            make_entry(
                APP_ENTRIES[0],
                subtitle="Default apps, permissions",
            ),

            make_entry(
                APP_ENTRIES[1],
                subtitle="Notification history, conversations",
            ),
        ],
    })


    # ------------------------------------------------------
    # Device
    # ------------------------------------------------------

    groups.append({
        "semantic":
            "device_group",

        "title":
            "Device",

        "entries": [

            make_entry(
                PERSONAL_ENTRIES[0],

                subtitle=(
                    f"{battery_percent}%"
                    + (
                        " · Battery Saver on"
                        if battery_saver
                        else ""
                    )
                ),
            ),

            make_entry(
                PERSONAL_ENTRIES[1],

                subtitle=(
                    f"{used_storage} GB used "
                    f"of {total_storage} GB"
                ),
            ),

            make_entry(
                PERSONAL_ENTRIES[2],
                subtitle="Media, call, alarm volume",
            ),

            make_entry(
                PERSONAL_ENTRIES[3],
                subtitle="Brightness, dark theme",
            ),
        ],
    })


    # ------------------------------------------------------
    # Personalization & Privacy
    # ------------------------------------------------------

    security_entries = [

        make_entry(
            SECURITY_ENTRIES[0],
            subtitle="Colors, wallpaper, themed icons",
        ),

        make_entry(
            SECURITY_ENTRIES[1],
            subtitle="Display, interaction, audio",
        ),

        make_entry(
            SECURITY_ENTRIES[2],

            subtitle=(
                "Action recommended"
                if security_warning
                else "App security, device lock"
            ),

            badge=(
                "Check"
                if security_warning
                else None
            ),
        ),

        make_entry(
            SECURITY_ENTRIES[3],
            subtitle="Location permissions",
        ),
    ]


    groups.append({
        "semantic":
            "privacy_group",

        "title":
            "Privacy & personalization",

        "entries":
            security_entries,
    })


    # ------------------------------------------------------
    # System
    # ------------------------------------------------------

    system_entries = [

        make_entry(
            SYSTEM_ENTRIES[0],
            subtitle="Emergency SOS, alerts",
        ),

        make_entry(
            SYSTEM_ENTRIES[1],
            subtitle=(
                account_email
                if account_present
                else "Add account"
            ),
        ),

        make_entry(
            SYSTEM_ENTRIES[2],
            subtitle="Screen time, app timers",
        ),

        make_entry(
            SYSTEM_ENTRIES[3],
            subtitle="Services & preferences",
        ),

        make_entry(
            SYSTEM_ENTRIES[4],

            subtitle=(
                "Software update available"
                if update_available
                else "Languages, gestures, backup"
            ),

            badge=(
                "Update"
                if update_available
                else None
            ),
        ),

        make_entry(
            SYSTEM_ENTRIES[5],
            subtitle=device_name,
        ),
    ]


    groups.append({
        "semantic":
            "system_group",

        "title":
            "System",

        "entries":
            system_entries,
    })


    # ======================================================
    # Result
    # ======================================================

    return {

        "title":
            "Settings",

        "search_expanded":
            search_expanded,

        "search_placeholder":
            "Search settings",

        "account": {

            "visible":
                True,

            "signed_in":
                account_present,

            "name":
                account_name,

            "email":
                account_email,

            "icon":
                (
                    "mdi:account-circle"
                    if account_present
                    else "mdi:account-plus-outline"
                ),
        },

        "quick_controls":
            quick_controls,

        "groups":
            groups,

        "state": {

            "wifi_enabled":
                wifi_enabled,

            "bluetooth_enabled":
                bluetooth_enabled,

            "mobile_data_enabled":
                mobile_data_enabled,

            "account_present":
                account_present,

            "search_expanded":
                search_expanded,

            "update_available":
                update_available,

            "security_warning":
                security_warning,

            "battery_saver":
                battery_saver,
        },
    }