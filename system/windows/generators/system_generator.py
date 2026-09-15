from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from system.windows.generators.media_generator import (
    get_random_wallpaper,
)


# ==========================================================
# Constants
# ==========================================================

INPUT_LANGUAGES = [
    "ENG",
    "KOR",
]


TASKBAR_APP_POOL = [

    {
        "name": "File Explorer",
        "icon": "folder",
    },

    {
        "name": "Browser",
        "icon": "public",
    },

    {
        "name": "Mail",
        "icon": "mail",
    },

    {
        "name": "Photos",
        "icon": "image",
    },

    {
        "name": "Settings",
        "icon": "settings",
    },

    {
        "name": "Terminal",
        "icon": "terminal",
    },

    {
        "name": "Store",
        "icon": "shopping_bag",
    },

    {
        "name": "Calendar",
        "icon": "calendar_month",
    },
]


# ==========================================================
# Time
# ==========================================================

def generate_datetime() -> datetime:

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


def format_time(
    value: datetime,
) -> str:

    return value.strftime(
        "%I:%M %p"
    ).lstrip("0")


def format_date(
    value: datetime,
) -> str:

    return (
        f"{value.month}/"
        f"{value.day}/"
        f"{value.year}"
    )


# ==========================================================
# Wi-Fi
# ==========================================================

def generate_wifi() -> dict:

    connected = (
        random.random()
        < 0.88
    )

    return {

        "connected":
            connected,

        "level":
            (
                random.randint(
                    1,
                    3,
                )
                if connected
                else 0
            ),

        "network_name":
            (
                random.choice(
                    [
                        "Home WiFi",
                        "KT_GiGA_5G",
                        "SK_WiFi",
                        "CampusNet",
                        "Office WiFi",
                    ]
                )
                if connected
                else None
            ),
    }


# ==========================================================
# Ethernet
# ==========================================================

def generate_ethernet() -> dict:

    connected = (
        random.random()
        < 0.24
    )

    return {

        "connected":
            connected,

        "network_name":
            (
                "Ethernet"
                if connected
                else None
            ),
    }


# ==========================================================
# Volume
# ==========================================================

def generate_volume() -> dict:

    muted = (
        random.random()
        < 0.12
    )

    return {

        "level":
            (
                0
                if muted
                else random.randint(
                    5,
                    100,
                )
            ),

        "muted":
            muted,
    }


# ==========================================================
# Battery
# ==========================================================

def generate_battery(
    device_category: str | None = None,
) -> dict:

    if device_category in {
        "desktop",
        "ultrawide",
    }:

        available = (
            random.random()
            < 0.12
        )

    else:

        available = (
            random.random()
            < 0.94
        )


    if not available:

        return {

            "available":
                False,

            "level":
                None,

            "charging":
                False,

            "battery_saver":
                False,
        }


    level = random.randint(
        8,
        100,
    )


    charging = (
        random.random()
        < 0.28
    )


    battery_saver = (
        not charging
        and level <= 25
        and random.random() < 0.55
    )


    return {

        "available":
            True,

        "level":
            level,

        "charging":
            charging,

        "battery_saver":
            battery_saver,
    }


# ==========================================================
# Notifications
# ==========================================================

def generate_notifications() -> dict:

    count = random.choices(

        [
            0,
            1,
            2,
            3,
            4,
            5,
        ],

        weights=[
            45,
            22,
            14,
            9,
            6,
            4,
        ],

        k=1,

    )[0]


    return {

        "count":
            count,

        "do_not_disturb":
            random.random()
            < 0.10,
    }


# ==========================================================
# Taskbar Apps
# ==========================================================

def generate_taskbar_apps() -> list[dict]:

    app_count = random.randint(
        3,
        7,
    )


    selected_apps = random.sample(

        TASKBAR_APP_POOL,

        k=min(
            app_count,
            len(
                TASKBAR_APP_POOL
            ),
        ),
    )


    active_index = (
        random.randrange(
            len(
                selected_apps
            )
        )
        if (
            selected_apps
            and random.random()
            < 0.80
        )
        else None
    )


    result = []


    for index, app in enumerate(
        selected_apps
    ):

        badge = None


        if (
            app["name"]
            in {
                "Mail",
                "Calendar",
            }
            and random.random() < 0.30
        ):

            badge = random.randint(
                1,
                9,
            )


        result.append({

            "name":
                app["name"],

            "icon":
                app["icon"],

            "active":
                index
                == active_index,

            "badge":
                badge,
        })


    return result


# ==========================================================
# Taskbar
# ==========================================================

def generate_taskbar() -> dict:

    return {

        "alignment":
            random.choices(
                [
                    "center",
                    "left",
                ],
                weights=[
                    90,
                    10,
                ],
                k=1,
            )[0],

        "search_mode":
            random.choices(
                [
                    "icon",
                    "box",
                    "hidden",
                ],
                weights=[
                    70,
                    22,
                    8,
                ],
                k=1,
            )[0],

        "apps":
            generate_taskbar_apps(),
    }


# ==========================================================
# System Generator
# ==========================================================

def generate_system_data(
    viewport: dict | None = None,
) -> dict:

    value = generate_datetime()


    category = (
        viewport.get(
            "category"
        )
        if viewport
        else None
    )


    wifi = generate_wifi()

    ethernet = generate_ethernet()


    network_type = (
        "ethernet"
        if ethernet["connected"]
        else "wifi"
    )


    return {

        "wallpaper":
            get_random_wallpaper(),

        "time_text":
            format_time(
                value
            ),

        "date_text":
            format_date(
                value
            ),

        "input_language":
            random.choices(
                INPUT_LANGUAGES,
                weights=[
                    75,
                    25,
                ],
                k=1,
            )[0],

        "network_type":
            network_type,

        "wifi":
            wifi,

        "ethernet":
            ethernet,

        "volume":
            generate_volume(),

        "battery":
            generate_battery(
                category
            ),

        "notifications":
            generate_notifications(),

        "taskbar":
            generate_taskbar(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    pprint(

        generate_system_data(

            viewport={

                "name":
                    "laptop",

                "category":
                    "laptop",
            }
        ),

        sort_dicts=False,
    )