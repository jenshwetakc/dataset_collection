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
# Device Controls
# ==========================================================

DEVICE_CONTROLS = [

    {
        "name":
            "Living room",

        "subtitle":
            "Light",

        "icon":
            "mdi:lightbulb-outline",
    },

    {
        "name":
            "Bedroom",

        "subtitle":
            "Light",

        "icon":
            "mdi:lightbulb-outline",
    },

    {
        "name":
            "Thermostat",

        "subtitle":
            "22°",

        "icon":
            "mdi:thermostat",
    },

    {
        "name":
            "Front door",

        "subtitle":
            "Locked",

        "icon":
            "mdi:lock-outline",
    },
]


# ==========================================================
# Wallet Cards
# ==========================================================

WALLET_CARDS = [

    {
        "name":
            "Visa",

        "last_four":
            "4821",

        "icon":
            "mdi:credit-card-outline",
    },

    {
        "name":
            "Mastercard",

        "last_four":
            "7712",

        "icon":
            "mdi:credit-card-outline",
    },

    {
        "name":
            "Transit card",

        "last_four":
            "Metro",

        "icon":
            "mdi:train",
    },
]


# ==========================================================
# Main Generator
# ==========================================================

def generate_power_menu_data() -> dict:

    # ======================================================
    # Main State
    # ======================================================

    menu_state = random.choices(
        [
            "normal",
            "restart_confirm",
            "poweroff_confirm",
            "emergency",
            "lockdown",
        ],
        weights=[
            0.56,
            0.12,
            0.12,
            0.10,
            0.10,
        ],
        k=1,
    )[0]


    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choice([
        "compact",
        "expanded",
    ])


    # ======================================================
    # Airplane
    # ======================================================

    airplane_mode = (
        random.random()
        < 0.20
    )


    # ======================================================
    # Wallet
    # ======================================================

    show_wallet = (
        menu_state == "normal"
        and random.random()
        < 0.48
    )

    wallet = random.choice(
        WALLET_CARDS
    )


    # ======================================================
    # Device Controls
    # ======================================================

    show_device_controls = (
        menu_state == "normal"
        and random.random()
        < 0.52
    )

    control_count = random.randint(
        2,
        min(
            4,
            len(
                DEVICE_CONTROLS
            ),
        ),
    )

    selected_controls = random.sample(
        DEVICE_CONTROLS,
        control_count,
    )

    controls = []

    for index, control in enumerate(
        selected_controls
    ):

        controls.append({

            "semantic":
                f"device_control_{index}",

            "name":
                control[
                    "name"
                ],

            "subtitle":
                control[
                    "subtitle"
                ],

            "icon":
                control[
                    "icon"
                ],

            "active":
                random.random()
                < 0.55,
        })


    # ======================================================
    # Emergency State
    # ======================================================

    emergency_message = random.choice([
        "Emergency services",
        "Emergency information",
        "Call emergency services",
    ])


    # ======================================================
    # Result
    # ======================================================

    return {

        "menu_state":
            menu_state,

        "layout_variant":
            layout_variant,

        "wallpaper":
            get_wallpaper(),

        "airplane_mode":
            airplane_mode,

        "show_wallet":
            show_wallet,

        "wallet":
            wallet,

        "show_device_controls":
            show_device_controls,

        "device_controls":
            controls,

        "emergency_message":
            emergency_message,
    }