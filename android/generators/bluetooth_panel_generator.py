from __future__ import annotations

import random
from pathlib import Path

from common.media_generator import (
    get_random_image,
)


# ==========================================================
# Paths
# ==========================================================

ANDROID_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

WALLPAPER_DIR = (
    ANDROID_ROOT
    / "assets"
    / "wallpapers"
)


# ==========================================================
# Device Pool
# ==========================================================

DEVICE_POOL = [

    {
        "name": "Pixel Buds Pro",
        "type": "headphones",
        "icon": "mdi:headphones",
    },

    {
        "name": "Galaxy Buds",
        "type": "headphones",
        "icon": "mdi:earbuds",
    },

    {
        "name": "Wireless Speaker",
        "type": "speaker",
        "icon": "mdi:speaker-wireless",
    },

    {
        "name": "Smart Watch",
        "type": "watch",
        "icon": "mdi:watch-variant",
    },

    {
        "name": "Keyboard",
        "type": "keyboard",
        "icon": "mdi:keyboard-outline",
    },

    {
        "name": "Mouse",
        "type": "mouse",
        "icon": "mdi:mouse",
    },

    {
        "name": "Car Audio",
        "type": "car",
        "icon": "mdi:car-connected",
    },

    {
        "name": "Laptop",
        "type": "computer",
        "icon": "mdi:laptop",
    },
]


# ==========================================================
# Wallpaper
# ==========================================================

def get_wallpaper() -> str | None:

    if not WALLPAPER_DIR.exists():
        return None

    try:

        return get_random_image(
            WALLPAPER_DIR
        )

    except Exception:

        return None


# ==========================================================
# Build Device
# ==========================================================

def build_device(
    device: dict,
    index: int,
    *,
    connected: bool = False,
) -> dict:

    battery_supported = (
        device["type"]
        in {
            "headphones",
            "watch",
            "keyboard",
            "mouse",
        }
    )

    battery = (
        random.randint(
            18,
            100,
        )
        if battery_supported
        else None
    )

    return {

        "semantic":
            f"bluetooth_device_{index}",

        "name":
            device["name"],

        "type":
            device["type"],

        "icon":
            device["icon"],

        "connected":
            connected,

        "battery":
            battery,

        "saved":
            (
                connected
                or random.random() < 0.35
            ),

        "subtitle":
            (
                "Connected"
                if connected
                else "Available"
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_bluetooth_panel_data() -> dict:

    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choices(
        [
            "bottom_sheet",
            "full_page",
        ],
        weights=[
            0.70,
            0.30,
        ],
        k=1,
    )[0]


    # ======================================================
    # Main State
    # ======================================================

    panel_state = random.choices(
        [
            "normal",
            "bluetooth_off",
            "scanning",
            "pairing",
            "pair_confirm",
            "details",
            "empty",
        ],
        weights=[
            0.38,
            0.10,
            0.12,
            0.10,
            0.10,
            0.12,
            0.08,
        ],
        k=1,
    )[0]


    # ======================================================
    # Bluetooth
    # ======================================================

    bluetooth_enabled = (
        panel_state
        != "bluetooth_off"
    )


    # ======================================================
    # Connected Devices
    # ======================================================

    connected_devices = []

    if bluetooth_enabled and panel_state != "empty":

        connected_count = random.randint(
            0,
            2,
        )

        if panel_state in {
            "details",
            "normal",
        }:

            connected_count = max(
                connected_count,
                1,
            )


        if connected_count > 0:

            selected_connected = random.sample(
                DEVICE_POOL,
                connected_count,
            )

            connected_devices = [

                build_device(
                    device,
                    index,
                    connected=True,
                )

                for index, device
                in enumerate(
                    selected_connected
                )
            ]


    # ======================================================
    # Nearby Devices
    # ======================================================

    used_names = {
        device["name"]
        for device
        in connected_devices
    }

    available_pool = [
        device
        for device
        in DEVICE_POOL
        if device["name"]
        not in used_names
    ]


    nearby_devices = []

    if (
        bluetooth_enabled
        and panel_state != "empty"
    ):

        nearby_count = random.randint(
            2,
            min(
                6,
                len(
                    available_pool
                ),
            ),
        )

        selected_nearby = random.sample(
            available_pool,
            nearby_count,
        )

        nearby_devices = [

            build_device(
                device,
                index + 10,
                connected=False,
            )

            for index, device
            in enumerate(
                selected_nearby
            )
        ]


    # ======================================================
    # Pairing Target
    # ======================================================

    pairing_target = None

    if (
        panel_state
        in {
            "pairing",
            "pair_confirm",
        }
        and nearby_devices
    ):

        pairing_target = random.choice(
            nearby_devices
        )


    # ======================================================
    # Details Target
    # ======================================================

    details_device = None

    if (
        panel_state
        == "details"
        and connected_devices
    ):

        details_device = random.choice(
            connected_devices
        )


    # ======================================================
    # Pairing Code
    # ======================================================

    pairing_code = (
        str(
            random.randint(
                100000,
                999999,
            )
        )
        if panel_state
        == "pair_confirm"
        else None
    )


    # ======================================================
    # Device Details
    # ======================================================

    media_audio = (
        random.random()
        < 0.88
    )

    phone_calls = (
        random.random()
        < 0.62
    )

    contact_sharing = (
        random.random()
        < 0.36
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "layout_variant":
            layout_variant,

        "panel_state":
            panel_state,

        "wallpaper":
            get_wallpaper(),

        "bluetooth_enabled":
            bluetooth_enabled,

        "connected_devices":
            connected_devices,

        "nearby_devices":
            nearby_devices,

        "pairing_target":
            pairing_target,

        "pairing_code":
            pairing_code,

        "details_device":
            details_device,

        "media_audio":
            media_audio,

        "phone_calls":
            phone_calls,

        "contact_sharing":
            contact_sharing,

        "show_scan_indicator":
            (
                panel_state
                == "scanning"
            ),
    }