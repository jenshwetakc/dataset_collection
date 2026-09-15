from __future__ import annotations

import random

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


# ==========================================================
# States
# ==========================================================

CONTROL_CENTER_STATES = [

    "normal",

    "connectivity_expanded",

    "media_expanded",

    "brightness_expanded",

    "volume_expanded",

    "focus_picker",

    "screen_mirroring",

    "recording_active",
]


CONTROL_CENTER_STATE_WEIGHTS = [

    30,  # normal
    14,  # connectivity
    12,  # media
    10,  # brightness
    10,  # volume
    10,  # focus
    8,   # screen mirroring
    6,   # recording
]


# ==========================================================
# Safe Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if (
        icon is None
        and fallback
    ):

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Connectivity
# ==========================================================

def generate_connectivity() -> dict:

    airplane = (
        random.random()
        < 0.12
    )

    cellular = (
        not airplane
        and random.random() < 0.95
    )

    wifi = (
        not airplane
        and random.random() < 0.88
    )

    bluetooth = (
        random.random()
        < 0.82
    )


    return {

        "airplane": {

            "enabled":
                airplane,

            "title":
                "Airplane Mode",

            "icon":
                resolve_icon(
                    "airplane",
                    "plane",
                ),
        },


        "cellular": {

            "enabled":
                cellular,

            "title":
                "Cellular Data",

            "subtitle":
                random.choice([
                    "5G",
                    "5G+",
                    "LTE",
                ]),

            "icon":
                resolve_icon(
                    "cellular",
                    "signal",
                ),
        },


        "wifi": {

            "enabled":
                wifi,

            "title":
                "Wi-Fi",

            "subtitle":
                (
                    random.choice([
                        "Home Network",
                        "KU-WiFi",
                        "Campus WiFi",
                    ])
                    if wifi
                    else "Off"
                ),

            "icon":
                resolve_icon(
                    "wifi"
                ),
        },


        "bluetooth": {

            "enabled":
                bluetooth,

            "title":
                "Bluetooth",

            "subtitle":
                (
                    "On"
                    if bluetooth
                    else "Off"
                ),

            "icon":
                resolve_icon(
                    "bluetooth"
                ),
        },


        "airdrop": {

            "enabled":
                random.random() < 0.55,

            "title":
                "AirDrop",

            "subtitle":
                random.choice([
                    "Contacts Only",
                    "Everyone for 10 Minutes",
                    "Receiving Off",
                ]),

            "icon":
                get_lucide_icon(
                    "radio-tower"
                ),
        },


        "hotspot": {

            "enabled":
                random.random() < 0.18,

            "title":
                "Personal Hotspot",

            "subtitle":
                random.choice([
                    "Off",
                    "Discoverable",
                ]),

            "icon":
                resolve_icon(
                    "hotspot",
                    "radio",
                ),
        },
    }


# ==========================================================
# Media
# ==========================================================

def generate_media() -> dict:

    playing = (
        random.random()
        < 0.72
    )


    return {

        "playing":
            playing,

        "title":
            random.choice([
                "Midnight Drive",
                "Afterglow",
                "City Lights",
                "Morning Focus",
                "Quiet Hours",
            ]),

        "artist":
            random.choice([
                "Nova",
                "Ocean Avenue",
                "Night Radio",
                "Studio Sessions",
                "Aurora",
            ]),

        "progress":
            random.randint(
                8,
                91,
            ),

        "icons": {

            "play":
                resolve_icon(
                    "play"
                ),

            "pause":
                resolve_icon(
                    "pause"
                ),

            "skip_back":
                resolve_icon(
                    "skip_back"
                ),

            "skip_forward":
                resolve_icon(
                    "skip_forward"
                ),

            "airplay":
                get_lucide_icon(
                    "cast"
                ),
        },
    }


# ==========================================================
# Focus
# ==========================================================

def generate_focus() -> dict:

    modes = [

        {
            "id":
                "do_not_disturb",

            "title":
                "Do Not Disturb",

            "icon":
                resolve_icon(
                    "moon"
                ),
        },

        {
            "id":
                "personal",

            "title":
                "Personal",

            "icon":
                resolve_icon(
                    "user"
                ),
        },

        {
            "id":
                "work",

            "title":
                "Work",

            "icon":
                get_lucide_icon(
                    "briefcase"
                ),
        },

        {
            "id":
                "sleep",

            "title":
                "Sleep",

            "icon":
                get_lucide_icon(
                    "bed"
                ),
        },
    ]


    active = (
        random.choice(
            [
                None,
                None,
                None,
                "do_not_disturb",
                "personal",
                "work",
                "sleep",
            ]
        )
    )


    return {

        "active":
            active,

        "modes":
            modes,

        "main_icon":
            (
                next(
                    (
                        item["icon"]
                        for item in modes
                        if item["id"] == active
                    ),
                    None,
                )
                if active
                else resolve_icon(
                    "moon"
                )
            ),
    }


# ==========================================================
# Screen Mirroring
# ==========================================================

def generate_mirroring_devices() -> list[dict]:

    candidates = [

        "Living Room TV",

        "Bedroom TV",

        "Studio Display",

        "Meeting Room",

        "Apple TV",

        "Office Display",
    ]

    random.shuffle(
        candidates
    )


    return [

        {
            "name":
                name,

            "connected":
                (
                    index == 0
                    and random.random() < 0.35
                ),

            "icon":
                get_lucide_icon(
                    "monitor"
                ),
        }

        for index, name
        in enumerate(
            candidates[:4]
        )
    ]


# ==========================================================
# Utility Controls
# ==========================================================

def generate_utilities() -> list[dict]:

    return [

        {
            "id":
                "flashlight",

            "title":
                "Flashlight",

            "enabled":
                random.random() < 0.20,

            "icon":
                resolve_icon(
                    "flashlight"
                ),
        },

        {
            "id":
                "timer",

            "title":
                "Timer",

            "enabled":
                False,

            "icon":
                get_lucide_icon(
                    "timer"
                ),
        },

        {
            "id":
                "calculator",

            "title":
                "Calculator",

            "enabled":
                False,

            "icon":
                get_lucide_icon(
                    "calculator"
                ),
        },

        {
            "id":
                "camera",

            "title":
                "Camera",

            "enabled":
                False,

            "icon":
                resolve_icon(
                    "camera"
                ),
        },

        {
            "id":
                "orientation_lock",

            "title":
                "Orientation Lock",

            "enabled":
                random.random() < 0.18,

            "icon":
                get_lucide_icon(
                    "rotate-ccw"
                ),
        },

        {
            "id":
                "screen_recording",

            "title":
                "Screen Recording",

            "enabled":
                False,

            "icon":
                get_lucide_icon(
                    "circle-dot"
                ),
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_control_center_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choices(

            CONTROL_CENTER_STATES,

            weights=
                CONTROL_CENTER_STATE_WEIGHTS,

            k=1,

        )[0]


    if (
        state
        not in CONTROL_CENTER_STATES
    ):

        raise ValueError(
            f"Unknown Control Center state: {state}"
        )


    category = (
        viewport.get(
            "category",
            ""
        )
        if viewport
        else ""
    )


    device_family = (
        "ipad"
        if category == "tablet"
        else "iphone"
    )


    recording = (
        state
        == "recording_active"
    )


    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            state
            in {
                "connectivity_expanded",
                "media_expanded",
                "brightness_expanded",
                "volume_expanded",
                "focus_picker",
                "screen_mirroring",
            },


        "connectivity":
            generate_connectivity(),


        "media":
            generate_media(),


        "focus":
            generate_focus(),


        "brightness":
            random.randint(
                20,
                95,
            ),


        "volume":
            random.randint(
                5,
                90,
            ),


        "recording": {

            "active":
                recording,

            "duration":
                random.choice([
                    "00:08",
                    "00:21",
                    "01:04",
                    "02:18",
                ]),

            "icon":
                get_lucide_icon(
                    "circle-dot"
                ),
        },


        "mirroring": {

            "icon":
                get_lucide_icon(
                    "screen-share"
                ),

            "devices":
                generate_mirroring_devices(),
        },


        "utilities":
            generate_utilities(),


        "icons": {

            "brightness":
                resolve_icon(
                    "brightness",
                    "sun",
                ),

            "volume":
                resolve_icon(
                    "volume",
                    "volume-2",
                ),

            "lock":
                resolve_icon(
                    "lock"
                ),

            "screen_mirroring":
                get_lucide_icon(
                    "screen-share"
                ),

            "focus":
                resolve_icon(
                    "moon"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "check":
                resolve_icon(
                    "check"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in CONTROL_CENTER_STATES:

        print(
            "\n=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_control_center_data(
                state=state
            ),

            sort_dicts=False,
        )