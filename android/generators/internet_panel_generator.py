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
# Wi-Fi Names
# ==========================================================

WIFI_NETWORKS = [
    "Home Wi-Fi",
    "KU-WiFi",
    "Office Network",
    "Android_AP",
    "Cafe 5G",
    "Guest Network",
    "Studio Wi-Fi",
    "Library",
    "Campus Secure",
    "Pixel Hotspot",
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
# Wi-Fi Icon
# ==========================================================

def get_wifi_icon(
    level: int,
    connected: bool = False,
) -> str:

    if level <= 1:
        return "mdi:wifi-strength-1"

    if level == 2:
        return "mdi:wifi-strength-2"

    if level == 3:
        return "mdi:wifi-strength-3"

    return "mdi:wifi"


# ==========================================================
# Network Builder
# ==========================================================

def build_network(
    name: str,
    index: int,
    *,
    connected: bool = False,
) -> dict:

    level = random.randint(
        1,
        4,
    )

    secured = (
        random.random()
        < 0.82
    )

    saved = (
        random.random()
        < 0.34
    )

    return {

        "semantic":
            f"wifi_network_{index}",

        "name":
            name,

        "signal_level":
            level,

        "icon":
            get_wifi_icon(
                level,
                connected=connected,
            ),

        "secured":
            secured,

        "saved":
            saved,

        "connected":
            connected,

        "subtitle":
            (
                "Connected"
                if connected
                else (
                    "Saved"
                    if saved
                    else (
                        "Tap to connect"
                        if secured
                        else "Open network"
                    )
                )
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_internet_panel_data() -> dict:

    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choices(
        [
            "bottom_sheet",
            "full_page",
        ],
        weights=[
            0.72,
            0.28,
        ],
        k=1,
    )[0]


    # ======================================================
    # Main State
    # ======================================================

    panel_state = random.choices(
        [
            "normal",
            "wifi_off",
            "no_internet",
            "details",
            "captive_portal",
        ],
        weights=[
            0.52,
            0.12,
            0.12,
            0.16,
            0.08,
        ],
        k=1,
    )[0]


    # ======================================================
    # Connectivity
    # ======================================================

    wifi_enabled = (
        panel_state
        != "wifi_off"
    )

    mobile_data_enabled = (
        random.random()
        < 0.82
    )

    airplane_mode = (
        random.random()
        < 0.12
    )


    # ======================================================
    # Connected Network
    # ======================================================

    connected_network = None

    if (
        wifi_enabled
        and panel_state
        not in {
            "no_internet",
        }
    ):

        connected_name = random.choice(
            WIFI_NETWORKS
        )

        connected_network = build_network(
            connected_name,
            0,
            connected=True,
        )


    # ======================================================
    # Nearby Networks
    # ======================================================

    nearby_names = [
        name
        for name in WIFI_NETWORKS
        if (
            not connected_network
            or name
            != connected_network[
                "name"
            ]
        )
    ]

    nearby_count = random.randint(
        3,
        min(
            7,
            len(
                nearby_names
            ),
        ),
    )

    selected_names = random.sample(
        nearby_names,
        nearby_count,
    )

    nearby_networks = [

        build_network(
            name,
            index + 1,
        )

        for index, name
        in enumerate(
            selected_names
        )
    ]


    # ======================================================
    # Details
    # ======================================================

    auto_connect = (
        random.random()
        < 0.76
    )

    metered = (
        random.random()
        < 0.18
    )

    randomized_mac = (
        random.random()
        < 0.84
    )

    ip_address = (
        f"192.168.1."
        f"{random.randint(2, 220)}"
    )


    # ======================================================
    # Mobile Data
    # ======================================================

    carrier = random.choice([
        "SKT",
        "KT",
        "LG U+",
        "5G",
    ])


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

        "wifi_enabled":
            wifi_enabled,

        "mobile_data_enabled":
            mobile_data_enabled,

        "airplane_mode":
            airplane_mode,

        "carrier":
            carrier,

        "connected_network":
            connected_network,

        "nearby_networks":
            nearby_networks,

        "show_network_details":
            (
                panel_state
                == "details"
                and connected_network
                is not None
            ),

        "captive_portal":
            (
                panel_state
                == "captive_portal"
            ),

        "no_internet":
            (
                panel_state
                == "no_internet"
            ),

        "auto_connect":
            auto_connect,

        "metered":
            metered,

        "randomized_mac":
            randomized_mac,

        "ip_address":
            ip_address,
    }