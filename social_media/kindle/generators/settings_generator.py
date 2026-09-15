from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

SETTINGS_STATES = [
    "settings_home",
    "reading_preferences",
    "notifications",
    "storage",
    "device_management",
    "theme_sheet",
    "device_details",
    "clear_downloads",
    "sign_out_confirmation",
]


# ==========================================================
# Devices
# ==========================================================

DEVICE_NAMES = [
    "Shweta's Kindle",
    "Kindle Paperwhite",
    "Kindle Oasis",
    "Android Phone",
    "iPhone",
    "Tablet",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_device(
    index: int,
) -> dict:

    device_type = random.choice(
        [
            "kindle",
            "phone",
            "tablet",
        ]
    )

    icon = {
        "kindle": "menu_book",
        "phone": "smartphone",
        "tablet": "tablet_android",
    }[
        device_type
    ]

    return {

        "id":
            f"device_{index:03d}",

        "name":
            random.choice(
                DEVICE_NAMES
            ),

        "type":
            device_type,

        "icon":
            icon,

        "active":
            index == 0,

        "last_sync":
            random.choice(
                [
                    "Just now",
                    "5 min ago",
                    "1 hour ago",
                    "Yesterday",
                    "3 days ago",
                ]
            ),

        "storage_used":
            random.randint(
                10,
                92,
            ),
    }


# ==========================================================
# Generator
# ==========================================================

def generate_settings_page() -> dict:

    state = random.choice(
        SETTINGS_STATES
    )

    devices = [
        generate_device(
            index
        )
        for index in range(
            random.randint(
                2,
                5,
            )
        )
    ]


    # ======================================================
    # Popup States
    # ======================================================

    show_theme_sheet = (
        state
        == "theme_sheet"
    )

    show_device_details = (
        state
        == "device_details"
    )

    show_clear_downloads = (
        state
        == "clear_downloads"
    )

    show_sign_out = (
        state
        == "sign_out_confirmation"
    )

    popup_open = any(
        [
            show_theme_sheet,
            show_device_details,
            show_clear_downloads,
            show_sign_out,
        ]
    )


    # ======================================================
    # Settings
    # ======================================================

    selected_theme = random.choice(
        [
            "System",
            "Light",
            "Dark",
            "Sepia",
        ]
    )

    font_size = random.choice(
        [
            "Small",
            "Medium",
            "Large",
        ]
    )

    line_spacing = random.choice(
        [
            "Compact",
            "Normal",
            "Relaxed",
        ]
    )


    # ======================================================
    # Storage
    # ======================================================

    total_storage_gb = random.choice(
        [
            8,
            16,
            32,
        ]
    )

    used_storage_gb = round(
        random.uniform(
            1.2,
            total_storage_gb * 0.82,
        ),
        1,
    )

    storage_percentage = round(
        (
            used_storage_gb
            / total_storage_gb
        )
        * 100
    )


    # ======================================================
    # Active Device
    # ======================================================

    active_device = (
        random.choice(
            devices
        )
        if devices
        else None
    )


    return {

        "state":
            state,

        "popup_open":
            popup_open,

        "show_theme_sheet":
            show_theme_sheet,

        "show_device_details":
            show_device_details,

        "show_clear_downloads":
            show_clear_downloads,

        "show_sign_out":
            show_sign_out,


        # ==================================================
        # Account
        # ==================================================

        "profile_name":
            random.choice(
                [
                    "Shweta",
                    "Kindle Reader",
                    "Book Lover",
                ]
            ),

        "email":
            random.choice(
                [
                    "reader@example.com",
                    "kindle@example.com",
                    "books@example.com",
                ]
            ),

        "membership":
            random.choice(
                [
                    "Kindle Unlimited",
                    "Prime Reading",
                    "Standard Account",
                ]
            ),


        # ==================================================
        # Reading Preferences
        # ==================================================

        "theme":
            selected_theme,

        "font_size":
            font_size,

        "line_spacing":
            line_spacing,

        "page_animation":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "show_reading_progress":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "auto_brightness":
            random.choice(
                [
                    True,
                    False,
                ]
            ),


        # ==================================================
        # Notifications
        # ==================================================

        "book_recommendations":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "reading_reminders":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "deal_alerts":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "achievement_notifications":
            random.choice(
                [
                    True,
                    False,
                ]
            ),


        # ==================================================
        # Sync
        # ==================================================

        "whispersync":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "auto_download":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "wifi_only":
            random.choice(
                [
                    True,
                    False,
                ]
            ),


        # ==================================================
        # Storage
        # ==================================================

        "total_storage_gb":
            total_storage_gb,

        "used_storage_gb":
            used_storage_gb,

        "storage_percentage":
            storage_percentage,

        "downloaded_books":
            random.randint(
                8,
                120,
            ),

        "download_size":
            round(
                random.uniform(
                    0.8,
                    8.0,
                ),
                1,
            ),


        # ==================================================
        # Devices
        # ==================================================

        "devices":
            devices,

        "active_device":
            active_device,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_settings_page()
    )

    print(
        "\n=============================="
    )

    print(
        "KINDLE SETTINGS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page["state"],
    )

    print(
        "Popup:",
        page["popup_open"],
    )

    print(
        "Theme:",
        page["theme"],
    )