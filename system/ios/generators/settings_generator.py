from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# Settings States
# ==========================================================

SETTINGS_STATES = [

    "main",

    "search_active",

    "wifi",

    "bluetooth",

    "notifications",

    "appearance",

    "storage",

    "confirmation_dialog",
]


SETTINGS_STATE_WEIGHTS = [

    24,  # main

    12,  # search_active

    14,  # wifi

    12,  # bluetooth

    12,  # notifications

    10,  # appearance

    10,  # storage

    6,   # confirmation_dialog
]


# ==========================================================
# Safe Lucide Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback_name: str | None = None,
) -> str | None:

    icon = (
        get_icon(
            semantic
        )
    )

    if (
        icon is None
        and fallback_name
    ):

        icon = (
            get_lucide_icon(
                fallback_name
            )
        )

    return icon


# ==========================================================
# Main Settings Sections
# ==========================================================

def generate_main_sections() -> list[dict]:

    return [

        # ==================================================
        # Connectivity
        # ==================================================

        {
            "id":
                "connectivity",

            "header":
                None,

            "footer":
                None,

            "items": [

                {
                    "id":
                        "airplane_mode",

                    "title":
                        "Airplane Mode",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "airplane",
                            "plane",
                        ),

                    "icon_style":
                        "orange",

                    "type":
                        "switch",

                    "enabled":
                        random.random() < 0.15,
                },

                {
                    "id":
                        "wifi",

                    "title":
                        "Wi-Fi",

                    "subtitle":
                        None,

                    "value":
                        random.choice([
                            "Home Network",
                            "KU-WiFi",
                            "Campus WiFi",
                            "MyNetwork",
                            "Connected",
                        ]),

                    "icon":
                        resolve_icon(
                            "wifi"
                        ),

                    "icon_style":
                        "blue",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "bluetooth",

                    "title":
                        "Bluetooth",

                    "subtitle":
                        None,

                    "value":
                        random.choice([
                            "On",
                            "Off",
                        ]),

                    "icon":
                        resolve_icon(
                            "bluetooth"
                        ),

                    "icon_style":
                        "blue",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "cellular",

                    "title":
                        "Cellular",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "cellular",
                            "signal",
                        ),

                    "icon_style":
                        "green",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "hotspot",

                    "title":
                        "Personal Hotspot",

                    "subtitle":
                        None,

                    "value":
                        random.choice([
                            "Off",
                            "Not Discoverable",
                        ]),

                    "icon":
                        resolve_icon(
                            "hotspot",
                            "radio",
                        ),

                    "icon_style":
                        "green",

                    "type":
                        "navigation",
                },
            ],
        },


        # ==================================================
        # Notifications / Focus
        # ==================================================

        {
            "id":
                "notifications_focus",

            "header":
                None,

            "footer":
                None,

            "items": [

                {
                    "id":
                        "notifications",

                    "title":
                        "Notifications",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "notifications",
                            "bell",
                        ),

                    "icon_style":
                        "red",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "sounds",

                    "title":
                        "Sounds & Haptics",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        get_lucide_icon(
                            "volume-2"
                        ),

                    "icon_style":
                        "pink",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "focus",

                    "title":
                        "Focus",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "focus",
                            "moon",
                        ),

                    "icon_style":
                        "purple",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "screen_time",

                    "title":
                        "Screen Time",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "screen_time",
                            "hourglass",
                        ),

                    "icon_style":
                        "purple",

                    "type":
                        "navigation",
                },
            ],
        },


        # ==================================================
        # General
        # ==================================================

        {
            "id":
                "general",

            "header":
                None,

            "footer":
                None,

            "items": [

                {
                    "id":
                        "general",

                    "title":
                        "General",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "general",
                            "settings",
                        ),

                    "icon_style":
                        "gray",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "control_center",

                    "title":
                        "Control Center",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "control_center",
                            "sliders-horizontal",
                        ),

                    "icon_style":
                        "gray",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "display",

                    "title":
                        "Display & Brightness",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "display",
                            "sun",
                        ),

                    "icon_style":
                        "blue",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "accessibility",

                    "title":
                        "Accessibility",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "accessibility",
                            "accessibility",
                        ),

                    "icon_style":
                        "blue",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "wallpaper",

                    "title":
                        "Wallpaper",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        get_lucide_icon(
                            "image"
                        ),

                    "icon_style":
                        "cyan",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "siri",

                    "title":
                        "Siri",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        get_lucide_icon(
                            "sparkles"
                        ),

                    "icon_style":
                        "purple",

                    "type":
                        "navigation",
                },
            ],
        },


        # ==================================================
        # Privacy
        # ==================================================

        {
            "id":
                "privacy",

            "header":
                None,

            "footer":
                None,

            "items": [

                {
                    "id":
                        "privacy_security",

                    "title":
                        "Privacy & Security",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "shield",
                            "shield",
                        ),

                    "icon_style":
                        "blue",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "battery",

                    "title":
                        "Battery",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        resolve_icon(
                            "battery",
                            "battery",
                        ),

                    "icon_style":
                        "green",

                    "type":
                        "navigation",
                },

                {
                    "id":
                        "storage",

                    "title":
                        "iPhone Storage",

                    "subtitle":
                        None,

                    "value":
                        None,

                    "icon":
                        get_lucide_icon(
                            "hard-drive"
                        ),

                    "icon_style":
                        "gray",

                    "type":
                        "navigation",
                },
            ],
        },
    ]


# ==========================================================
# Search Results
# ==========================================================

def generate_search_results() -> list[dict]:

    candidates = [

        {
            "title":
                "Wi-Fi",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "wifi"
                ),

            "icon_style":
                "blue",
        },

        {
            "title":
                "Bluetooth",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "bluetooth"
                ),

            "icon_style":
                "blue",
        },

        {
            "title":
                "Notifications",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "notifications"
                ),

            "icon_style":
                "red",
        },

        {
            "title":
                "Display & Brightness",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "display",
                    "sun",
                ),

            "icon_style":
                "blue",
        },

        {
            "title":
                "Privacy & Security",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "shield"
                ),

            "icon_style":
                "blue",
        },

        {
            "title":
                "Battery",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "battery"
                ),

            "icon_style":
                "green",
        },

        {
            "title":
                "Accessibility",

            "subtitle":
                "Settings",

            "icon":
                resolve_icon(
                    "accessibility",
                    "accessibility",
                ),

            "icon_style":
                "blue",
        },
    ]

    random.shuffle(
        candidates
    )

    return candidates[
        :random.randint(
            4,
            len(candidates),
        )
    ]


# ==========================================================
# Wi-Fi Networks
# ==========================================================

def generate_wifi_networks() -> list[dict]:

    names = [

        "Home Network",

        "KU-WiFi",

        "Campus Wireless",

        "CoffeeLab",

        "Galaxy",

        "Office WiFi",

        "Public Wi-Fi",

        "Studio Network",
    ]


    random.shuffle(
        names
    )


    networks = []


    for index, name in enumerate(
        names[
            :random.randint(
                5,
                8,
            )
        ]
    ):

        connected = (
            index == 0
        )


        networks.append({

            "name":
                name,

            "connected":
                connected,

            "secured":
                random.random() < 0.85,

            "signal_level":
                random.randint(
                    1,
                    3,
                ),

            "wifi_icon":
                (
                    resolve_icon(
                        "wifi_low"
                    )
                    if random.random() < 0.25
                    else
                    resolve_icon(
                        "wifi"
                    )
                ),

            "lock_icon":
                (
                    resolve_icon(
                        "lock"
                    )
                ),

            "info_icon":
                (
                    resolve_icon(
                        "info"
                    )
                ),

            "check_icon":
                (
                    resolve_icon(
                        "check"
                    )
                ),
        })


    return networks


# ==========================================================
# Bluetooth Devices
# ==========================================================

def generate_bluetooth_devices() -> list[dict]:

    device_names = [

        "AirPods",

        "Wireless Keyboard",

        "Magic Mouse",

        "Speaker",

        "Headphones",

        "Car Audio",

        "Game Controller",

        "Fitness Watch",
    ]


    random.shuffle(
        device_names
    )


    devices = []


    for index, name in enumerate(
        device_names[
            :random.randint(
                4,
                7,
            )
        ]
    ):

        if index == 0:

            state = (
                "Connected"
            )

        else:

            state = random.choice([
                "Not Connected",
                "Connected",
            ])


        devices.append({

            "name":
                name,

            "state":
                state,

            "icon":
                resolve_icon(
                    "bluetooth"
                ),

            "info_icon":
                resolve_icon(
                    "info"
                ),
        })


    return devices


# ==========================================================
# Notification Apps
# ==========================================================

def generate_notification_apps() -> list[dict]:

    apps = [

        (
            "Messages",
            "message",
            "green",
        ),

        (
            "Mail",
            "mail",
            "blue",
        ),

        (
            "Calendar",
            "calendar",
            "red",
        ),

        (
            "Photos",
            "image",
            "multicolor",
        ),

        (
            "Phone",
            "phone",
            "green",
        ),

        (
            "Music",
            "music",
            "red",
        ),
    ]


    items = []


    for (
        title,
        semantic,
        icon_style,
    ) in apps:

        items.append({

            "title":
                title,

            "icon":
                resolve_icon(
                    semantic
                ),

            "icon_style":
                icon_style,

            "status":
                random.choice([
                    "Banners, Sounds, Badges",
                    "Banners, Sounds",
                    "Badges",
                    "Off",
                ]),
        })


    return items


# ==========================================================
# Appearance Data
# ==========================================================

def generate_appearance_data() -> dict:

    selected_mode = (
        random.choice([
            "light",
            "dark",
        ])
    )


    return {

        "selected_mode":
            selected_mode,

        "automatic":
            random.random() < 0.35,

        "brightness":
            random.randint(
                25,
                95,
            ),

        "true_tone":
            random.random() < 0.75,

        "night_shift":
            random.choice([
                "Off",
                "Sunset to Sunrise",
                "Scheduled",
            ]),

        "icons": {

            "sun":
                resolve_icon(
                    "sun"
                ),

            "moon":
                resolve_icon(
                    "moon"
                ),

            "brightness":
                resolve_icon(
                    "brightness",
                    "sun-medium",
                ),
        },
    }


# ==========================================================
# Storage Data
# ==========================================================

def generate_storage_data() -> dict:

    capacities = [
        128,
        256,
        512,
    ]


    capacity = (
        random.choice(
            capacities
        )
    )


    usage_ratio = (
        random.uniform(
            0.38,
            0.92,
        )
    )


    used = round(
        capacity
        * usage_ratio,
        1,
    )


    categories = [

        {
            "name":
                "Apps",

            "size":
                round(
                    used
                    * random.uniform(
                        0.25,
                        0.40,
                    ),
                    1,
                ),

            "icon":
                get_lucide_icon(
                    "layout-grid"
                ),

            "icon_style":
                "blue",
        },

        {
            "name":
                "Photos",

            "size":
                round(
                    used
                    * random.uniform(
                        0.15,
                        0.28,
                    ),
                    1,
                ),

            "icon":
                resolve_icon(
                    "image"
                ),

            "icon_style":
                "red",
        },

        {
            "name":
                "Media",

            "size":
                round(
                    used
                    * random.uniform(
                        0.08,
                        0.18,
                    ),
                    1,
                ),

            "icon":
                resolve_icon(
                    "music"
                ),

            "icon_style":
                "purple",
        },

        {
            "name":
                "Messages",

            "size":
                round(
                    used
                    * random.uniform(
                        0.04,
                        0.12,
                    ),
                    1,
                ),

            "icon":
                resolve_icon(
                    "message"
                ),

            "icon_style":
                "green",
        },

        {
            "name":
                "System Data",

            "size":
                round(
                    used
                    * random.uniform(
                        0.07,
                        0.16,
                    ),
                    1,
                ),

            "icon":
                resolve_icon(
                    "settings"
                ),

            "icon_style":
                "gray",
        },
    ]


    return {

        "capacity":
            capacity,

        "used":
            used,

        "free":
            round(
                capacity
                - used,
                1,
            ),

        "usage_percent":
            round(
                usage_ratio
                * 100,
            ),

        "categories":
            categories,

        "storage_icon":
            get_lucide_icon(
                "hard-drive"
            ),
    }


# ==========================================================
# Confirmation Dialog
# ==========================================================

def generate_confirmation_dialog() -> dict:

    dialog_types = [

        {
            "title":
                "Turn Off Bluetooth?",

            "message":
                (
                    "Bluetooth accessories will be disconnected "
                    "until Bluetooth is turned on again."
                ),

            "confirm":
                "Turn Off",

            "cancel":
                "Cancel",
        },

        {
            "title":
                "Reset Settings?",

            "message":
                (
                    "This will reset your settings without "
                    "deleting your data or media."
                ),

            "confirm":
                "Reset",

            "cancel":
                "Cancel",
        },

        {
            "title":
                "Forget This Network?",

            "message":
                (
                    "Your device will no longer join this "
                    "Wi-Fi network automatically."
                ),

            "confirm":
                "Forget",

            "cancel":
                "Cancel",
        },
    ]


    return random.choice(
        dialog_types
    )


# ==========================================================
# Main Settings Generator
# ==========================================================

def generate_settings_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:
    """
    Generate synthetic iOS Settings data.

    Parameters
    ----------
    viewport:
        Optional common viewport dictionary.

        Used to determine whether the UI should behave
        like iPhone or iPad.

    state:
        Optional explicit Settings state.

        If None, a random state is selected.
    """

    # ======================================================
    # Resolve Device Family
    # ======================================================

    device_family = "iphone"


    if viewport:

        category = (
            viewport.get(
                "category",
                ""
            )
        )

        if category == "tablet":

            device_family = "ipad"


    # ======================================================
    # Resolve State
    # ======================================================

    if state is None:

        state = random.choices(

            SETTINGS_STATES,

            weights=
                SETTINGS_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in SETTINGS_STATES:

        raise ValueError(
            f"Unknown settings state: {state}"
        )


    # ======================================================
    # Device-Specific Labels
    # ======================================================

    storage_title = (
        "iPad Storage"
        if device_family == "ipad"
        else "iPhone Storage"
    )


    # ======================================================
    # Main Data
    # ======================================================

    data = {

        # --------------------------------------------------
        # Device
        # --------------------------------------------------

        "device_family":
            device_family,


        # --------------------------------------------------
        # State
        # --------------------------------------------------

        "state":
            state,

        "title":
            "Settings",

        "is_overlay_state":
            state
            == "confirmation_dialog",


        # --------------------------------------------------
        # Shared Icons
        # --------------------------------------------------

        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "back":
                resolve_icon(
                    "back"
                ),

            "forward":
                resolve_icon(
                    "forward"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "info":
                resolve_icon(
                    "info"
                ),

            "lock":
                resolve_icon(
                    "lock"
                ),

            "wifi":
                resolve_icon(
                    "wifi"
                ),

            "bluetooth":
                resolve_icon(
                    "bluetooth"
                ),
        },


        # --------------------------------------------------
        # Main Settings
        # --------------------------------------------------

        "sections":
            generate_main_sections(),


        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "search": {

            "query":
                random.choice([
                    "wifi",
                    "display",
                    "battery",
                    "privacy",
                    "notifications",
                ]),

            "results":
                generate_search_results(),
        },


        # --------------------------------------------------
        # Wi-Fi
        # --------------------------------------------------

        "wifi": {

            "enabled":
                True,

            "networks":
                generate_wifi_networks(),
        },


        # --------------------------------------------------
        # Bluetooth
        # --------------------------------------------------

        "bluetooth": {

            "enabled":
                True,

            "devices":
                generate_bluetooth_devices(),
        },


        # --------------------------------------------------
        # Notifications
        # --------------------------------------------------

        "notifications": {

            "apps":
                generate_notification_apps(),
        },


        # --------------------------------------------------
        # Appearance
        # --------------------------------------------------

        "appearance":
            generate_appearance_data(),


        # --------------------------------------------------
        # Storage
        # --------------------------------------------------

        "storage":
            generate_storage_data(),


        # --------------------------------------------------
        # Device-Specific Strings
        # --------------------------------------------------

        "labels": {

            "storage_title":
                storage_title,
        },


        # --------------------------------------------------
        # Dialog
        # --------------------------------------------------

        "confirmation_dialog":
            generate_confirmation_dialog(),
    }


    return data

# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in SETTINGS_STATES:

        print(
            "\n"
            "=================================================="
        )

        print(
            "STATE:",
            state,
        )

        print(
            "=================================================="
        )


        data = (
            generate_settings_data(
                state=state
            )
        )


        pprint(
            data,
            sort_dicts=False,
        )