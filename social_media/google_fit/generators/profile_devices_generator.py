from __future__ import annotations

import random

from faker import Faker

from social_media.google_fit.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

PROFILE_DEVICE_STATES = [
    "connected",
    "no_devices",
    "searching",
    "syncing",
    "permission_blocked",
    "connection_error",
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "active": False,
    },
    {
        "label": "Journal",
        "icon": "view_timeline",
        "active": False,
    },
    {
        "label": "Browse",
        "icon": "explore",
        "active": False,
    },
    {
        "label": "Profile",
        "icon": "person",
        "active": True,
    },
]


# ==========================================================
# Devices
# ==========================================================

DEVICE_TYPES = [
    {
        "name": "Pixel Watch",
        "icon": "watch",
        "type": "Smartwatch",
    },
    {
        "name": "Fitness Band",
        "icon": "watch",
        "type": "Activity tracker",
    },
    {
        "name": "Smart Scale",
        "icon": "monitor_weight",
        "type": "Scale",
    },
    {
        "name": "Heart Sensor",
        "icon": "monitor_heart",
        "type": "Heart-rate sensor",
    },
]


# ==========================================================
# Connected Apps
# ==========================================================

CONNECTED_APPS = [
    {
        "name": "Health Connect",
        "icon": "health_and_safety",
        "category": "Health data",
    },
    {
        "name": "Sleep Tracker",
        "icon": "bedtime",
        "category": "Sleep",
    },
    {
        "name": "Workout Sync",
        "icon": "fitness_center",
        "category": "Activity",
    },
    {
        "name": "Nutrition Log",
        "icon": "restaurant",
        "category": "Nutrition",
    },
]


# ==========================================================
# Settings
# ==========================================================

SETTINGS = [
    {
        "label": "Activity tracking",
        "icon": "directions_run",
        "enabled": True,
    },
    {
        "label": "Location tracking",
        "icon": "location_on",
        "enabled": True,
    },
    {
        "label": "Background sync",
        "icon": "sync",
        "enabled": True,
    },
    {
        "label": "Workout reminders",
        "icon": "notifications",
        "enabled": False,
    },
]


# ==========================================================
# Device Generator
# ==========================================================

def generate_connected_devices() -> list[dict]:

    count = random.randint(
        1,
        3,
    )

    selected = random.sample(
        DEVICE_TYPES,
        k=count,
    )

    result = []

    for index, device in enumerate(
        selected
    ):

        battery = random.randint(
            18,
            100,
        )

        result.append(
            {
                **device,

                "id":
                    index,

                "battery":
                    battery,

                "battery_label":
                    f"{battery}%",

                "connected":
                    True,

                "last_sync":
                    random.choice(
                        [
                            "Just now",
                            "2 min ago",
                            "12 min ago",
                            "1 hour ago",
                        ]
                    ),
            }
        )

    return result


# ==========================================================
# Connected State
# ==========================================================

def generate_connected_state() -> dict:

    devices = (
        generate_connected_devices()
    )

    apps = random.sample(
        CONNECTED_APPS,
        k=random.randint(
            2,
            len(CONNECTED_APPS),
        ),
    )

    return {

        "devices":
            devices,

        "connected_apps":
            apps,

        "settings": [
            dict(item)
            for item
            in SETTINGS
        ],

        "sync_progress":
            None,

        "message":
            None,

        "description":
            None,
    }


# ==========================================================
# No Devices
# ==========================================================

def generate_no_devices_state() -> dict:

    return {

        "devices":
            [],

        "connected_apps":
            random.sample(
                CONNECTED_APPS,
                k=random.randint(
                    1,
                    2,
                ),
            ),

        "settings": [
            dict(item)
            for item
            in SETTINGS
        ],

        "sync_progress":
            None,

        "message":
            "No devices connected",

        "description":
            (
                "Connect a watch, fitness tracker, scale, "
                "or compatible health device to sync activity data."
            ),
    }


# ==========================================================
# Searching
# ==========================================================

def generate_searching_state() -> dict:

    return {

        "devices":
            [],

        "connected_apps":
            [],

        "settings":
            [],

        "sync_progress":
            random.randint(
                20,
                75,
            ),

        "message":
            "Looking for devices",

        "description":
            (
                "Keep your nearby fitness device turned on "
                "and ready to pair."
            ),
    }


# ==========================================================
# Syncing
# ==========================================================

def generate_syncing_state() -> dict:

    devices = (
        generate_connected_devices()
    )

    return {

        "devices":
            devices,

        "connected_apps":
            random.sample(
                CONNECTED_APPS,
                k=2,
            ),

        "settings": [
            dict(item)
            for item
            in SETTINGS
        ],

        "sync_progress":
            random.randint(
                25,
                92,
            ),

        "message":
            "Syncing health data",

        "description":
            (
                "Fit is updating activity, sleep, heart rate, "
                "and other recent measurements."
            ),
    }


# ==========================================================
# Permission Blocked
# ==========================================================

def generate_permission_blocked_state() -> dict:

    return {

        "devices":
            [],

        "connected_apps":
            [],

        "settings":
            [],

        "sync_progress":
            None,

        "message":
            "Permission required",

        "description":
            (
                "Fit needs nearby-device and health-data "
                "permissions before it can connect and sync."
            ),
    }


# ==========================================================
# Connection Error
# ==========================================================

def generate_connection_error_state() -> dict:

    failed_device = (
        random.choice(
            DEVICE_TYPES
        )
    )

    return {

        "devices": [
            {
                **failed_device,

                "id":
                    0,

                "battery":
                    None,

                "battery_label":
                    None,

                "connected":
                    False,

                "last_sync":
                    "Connection failed",
            }
        ],

        "connected_apps":
            [],

        "settings":
            [],

        "sync_progress":
            None,

        "message":
            "Couldn't connect",

        "description":
            (
                f"Fit couldn't connect to "
                f"{failed_device['name']}. "
                "Check Bluetooth and try again."
            ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_profile_devices_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            PROFILE_DEVICE_STATES
        )


    if state not in (
        PROFILE_DEVICE_STATES
    ):

        raise ValueError(
            f"Unknown profile/device state: "
            f"{state}. "
            f"Available states: "
            f"{PROFILE_DEVICE_STATES}"
        )


    if state == "connected":

        state_data = (
            generate_connected_state()
        )

    elif state == "no_devices":

        state_data = (
            generate_no_devices_state()
        )

    elif state == "searching":

        state_data = (
            generate_searching_state()
        )

    elif state == "syncing":

        state_data = (
            generate_syncing_state()
        )

    elif state == "permission_blocked":

        state_data = (
            generate_permission_blocked_state()
        )

    else:

        state_data = (
            generate_connection_error_state()
        )


    user_name = (
        fake.name()
    )


    return {

        "state":
            state,

        "user": {
            "name":
                user_name,

            "email":
                fake.email(),

            "avatar":
                get_random_avatar(),

            "initial":
                user_name[0].upper(),
        },

        "navigation_items": [
            dict(item)
            for item
            in NAVIGATION_ITEMS
        ],

        **state_data,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in PROFILE_DEVICE_STATES:

        print(
            "\n"
            "===================================="
        )

        print(
            state.upper()
        )

        print(
            "===================================="
        )

        pprint(
            generate_profile_devices_data(
                state=state
            )
        )