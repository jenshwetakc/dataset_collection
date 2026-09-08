from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

from common.media_generator import (
    get_random_image,
)


fake = Faker()


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

AVATAR_DIR = (
    ANDROID_ROOT
    / "assets"
    / "avatars"
)


# ==========================================================
# Helpers
# ==========================================================

def get_random_asset(
    directory: Path,
) -> str | None:

    if not directory.exists():
        return None

    try:
        return get_random_image(
            directory
        )
    except Exception:
        return None


# ==========================================================
# Audio Routes
# ==========================================================

AUDIO_ROUTES = [
    {
        "name": "Phone",
        "icon": "mdi:cellphone",
        "semantic": "phone",
    },
    {
        "name": "Speaker",
        "icon": "mdi:volume-high",
        "semantic": "speaker",
    },
    {
        "name": "Bluetooth",
        "icon": "mdi:bluetooth",
        "semantic": "bluetooth",
    },
]


# ==========================================================
# Main Generator
# ==========================================================

def generate_call_screen_data() -> dict:

    # ======================================================
    # Main State
    # ======================================================

    call_state = random.choices(
        [
            "incoming",
            "active",
            "hold",
            "missed",
            "declined",
            "keypad",
            "video",
        ],
        weights=[
            0.30,
            0.28,
            0.10,
            0.08,
            0.06,
            0.10,
            0.08,
        ],
        k=1,
    )[0]


    # ======================================================
    # Caller
    # ======================================================

    known_contact = (
        random.random()
        < 0.82
    )

    if known_contact:

        caller_name = fake.first_name()

        caller_number = random.choice([
            "+82 10-4821-7754",
            "+82 10-2294-1188",
            "+82 10-7752-4801",
            "+1 415-555-0198",
        ])

    else:

        caller_name = random.choice([
            "Unknown caller",
            "Private number",
            "No caller ID",
        ])

        caller_number = ""


    caller_avatar = (
        get_random_asset(
            AVATAR_DIR
        )
        if known_contact
        else None
    )


    # ======================================================
    # Call Type
    # ======================================================

    call_type = (
        "video"
        if call_state == "video"
        else random.choices(
            [
                "voice",
                "video",
            ],
            weights=[
                0.86,
                0.14,
            ],
            k=1,
        )[0]
    )


    # ======================================================
    # Duration
    # ======================================================

    call_seconds = random.randint(
        4,
        3600,
    )

    minutes = (
        call_seconds
        // 60
    )

    seconds = (
        call_seconds
        % 60
    )

    duration = (
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


    # ======================================================
    # Audio State
    # ======================================================

    muted = (
        random.random()
        < 0.28
    )

    speaker_on = (
        random.random()
        < 0.24
    )

    audio_route = random.choice(
        AUDIO_ROUTES
    )

    if speaker_on:

        audio_route = {
            "name": "Speaker",
            "icon": "mdi:volume-high",
            "semantic": "speaker",
        }


    # ======================================================
    # Extra Controls
    # ======================================================

    show_add_call = (
        call_state
        in {
            "active",
            "hold",
        }
        and random.random() < 0.72
    )

    show_merge_call = (
        call_state == "hold"
        and random.random() < 0.66
    )

    show_hold = (
        call_state == "active"
        and random.random() < 0.68
    )


    # ======================================================
    # Keypad
    # ======================================================

    keypad_digits = ""

    if call_state == "keypad":

        count = random.randint(
            0,
            6,
        )

        keypad_digits = "".join(
            random.choice(
                "0123456789"
            )
            for _ in range(
                count
            )
        )


    # ======================================================
    # Compact Variant
    # ======================================================

    layout_variant = random.choices(
        [
            "fullscreen",
            "compact",
        ],
        weights=[
            0.82,
            0.18,
        ],
        k=1,
    )[0]


    # ======================================================
    # Emergency
    # ======================================================

    emergency = (
        random.random()
        < 0.04
    )

    if emergency:

        caller_name = random.choice([
            "Emergency services",
            "Emergency contact",
        ])


    # ======================================================
    # Result
    # ======================================================

    return {

        "call_state":
            call_state,

        "layout_variant":
            layout_variant,

        "call_type":
            call_type,

        "caller_name":
            caller_name,

        "caller_number":
            caller_number,

        "caller_avatar":
            caller_avatar,

        "known_contact":
            known_contact,

        "wallpaper":
            get_random_asset(
                WALLPAPER_DIR
            ),

        "duration":
            duration,

        "muted":
            muted,

        "speaker_on":
            speaker_on,

        "audio_route":
            audio_route,

        "show_add_call":
            show_add_call,

        "show_merge_call":
            show_merge_call,

        "show_hold":
            show_hold,

        "keypad_digits":
            keypad_digits,

        "emergency":
            emergency,
    }