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
# Apps
# ==========================================================

APP_POOL = [

    {
        "name": "Bank",
        "icon": "mdi:bank-outline",
    },

    {
        "name": "Wallet",
        "icon": "mdi:wallet-outline",
    },

    {
        "name": "Photos",
        "icon": "mdi:image-multiple-outline",
    },

    {
        "name": "Password Manager",
        "icon": "mdi:shield-key-outline",
    },

    {
        "name": "Drive",
        "icon": "mdi:google-drive",
    },

    {
        "name": "Settings",
        "icon": "mdi:cog-outline",
    },
]


# ==========================================================
# Helper
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
# Main Generator
# ==========================================================

def generate_biometric_prompt_data() -> dict:

    # ======================================================
    # Biometric Type
    # ======================================================

    biometric_type = random.choices(
        [
            "fingerprint",
            "face",
        ],
        weights=[
            0.66,
            0.34,
        ],
        k=1,
    )[0]


    # ======================================================
    # Main State
    # ======================================================

    prompt_state = random.choices(
        [
            "ready",
            "scanning",
            "failed",
            "retry",
            "success",
            "locked_out",
            "pin_fallback",
            "pattern_fallback",
        ],
        weights=[
            0.20,
            0.20,
            0.13,
            0.10,
            0.10,
            0.08,
            0.11,
            0.08,
        ],
        k=1,
    )[0]


    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choices(
        [
            "dialog",
            "bottom_sheet",
        ],
        weights=[
            0.72,
            0.28,
        ],
        k=1,
    )[0]


    # ======================================================
    # Authentication Context
    # ======================================================

    auth_context = random.choice([
        "app",
        "payment",
        "settings",
        "unlock",
    ])


    app = random.choice(
        APP_POOL
    )


    # ======================================================
    # Titles
    # ======================================================

    if auth_context == "payment":

        title = (
            "Confirm payment"
        )

        subtitle = (
            "Use your biometric to continue"
        )

    elif auth_context == "settings":

        title = (
            "Verify it's you"
        )

        subtitle = (
            "Authentication is required to change this setting"
        )

    elif auth_context == "unlock":

        title = (
            "Unlock"
        )

        subtitle = (
            "Verify your identity"
        )

    else:

        title = (
            f"Sign in to {app['name']}"
        )

        subtitle = (
            "Use your biometric to continue"
        )


    # ======================================================
    # Status
    # ======================================================

    if biometric_type == "fingerprint":

        main_icon = (
            "mdi:fingerprint"
        )

        ready_text = (
            "Touch the fingerprint sensor"
        )

        scanning_text = (
            "Checking fingerprint…"
        )

    else:

        main_icon = (
            "mdi:face-recognition"
        )

        ready_text = (
            "Look at your phone"
        )

        scanning_text = (
            "Looking for your face…"
        )


    if prompt_state == "ready":

        status_text = (
            ready_text
        )

    elif prompt_state == "scanning":

        status_text = (
            scanning_text
        )

    elif prompt_state == "failed":

        status_text = random.choice([
            "Not recognized",
            "Try again",
            "Couldn't verify",
        ])

    elif prompt_state == "retry":

        status_text = (
            "Try again"
        )

    elif prompt_state == "success":

        status_text = (
            "Verified"
        )

    elif prompt_state == "locked_out":

        status_text = (
            "Too many attempts"
        )

    elif prompt_state == "pin_fallback":

        status_text = (
            "Enter your PIN"
        )

    else:

        status_text = (
            "Draw your pattern"
        )


    # ======================================================
    # Confirmation Requirement
    # ======================================================

    require_confirmation = (
        prompt_state == "success"
        and random.random() < 0.42
    )


    # ======================================================
    # PIN
    # ======================================================

    pin_length = random.choice([
        4,
        6,
    ])

    entered_pin_length = (
        random.randint(
            0,
            pin_length - 1,
        )
        if prompt_state
        == "pin_fallback"
        else 0
    )


    # ======================================================
    # Pattern
    # ======================================================

    pattern_selected = []

    if prompt_state == "pattern_fallback":

        count = random.randint(
            0,
            5,
        )

        if count > 0:

            pattern_selected = random.sample(
                list(
                    range(
                        9
                    )
                ),
                count,
            )


    # ======================================================
    # Remaining Attempts
    # ======================================================

    remaining_attempts = (
        random.choice([
            1,
            2,
            3,
        ])
        if prompt_state
        in {
            "failed",
            "retry",
        }
        else None
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "biometric_type":
            biometric_type,

        "prompt_state":
            prompt_state,

        "layout_variant":
            layout_variant,

        "auth_context":
            auth_context,

        "app":
            app,

        "wallpaper":
            get_wallpaper(),

        "title":
            title,

        "subtitle":
            subtitle,

        "main_icon":
            main_icon,

        "status_text":
            status_text,

        "require_confirmation":
            require_confirmation,

        "pin_length":
            pin_length,

        "entered_pin_length":
            entered_pin_length,

        "pattern_selected":
            pattern_selected,

        "remaining_attempts":
            remaining_attempts,

        "show_cancel":
            (
                prompt_state
                not in {
                    "success",
                }
            ),

        "show_fallback":
            (
                prompt_state
                in {
                    "ready",
                    "scanning",
                    "failed",
                    "retry",
                    "locked_out",
                }
            ),
    }