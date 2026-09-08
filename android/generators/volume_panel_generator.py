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
# Audio Outputs
# ==========================================================

AUDIO_OUTPUTS = [
    {
        "name": "This phone",
        "icon": "mdi:cellphone",
        "type": "phone",
    },
    {
        "name": "Phone speaker",
        "icon": "mdi:volume-high",
        "type": "speaker",
    },
    {
        "name": "Pixel Buds Pro",
        "icon": "mdi:headphones",
        "type": "bluetooth",
    },
    {
        "name": "Bluetooth speaker",
        "icon": "mdi:speaker-wireless",
        "type": "bluetooth",
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
# Volume State
# ==========================================================

def volume_icon(
    stream: str,
    level: int,
    muted: bool,
) -> str:

    if muted or level == 0:

        if stream == "ring":
            return "mdi:volume-off"

        return "mdi:volume-mute"


    if stream == "alarm":
        return "mdi:alarm"


    if stream == "call":
        return "mdi:phone"


    if level <= 30:
        return "mdi:volume-low"


    if level <= 70:
        return "mdi:volume-medium"


    return "mdi:volume-high"


# ==========================================================
# Stream Builder
# ==========================================================

def build_stream(
    semantic: str,
    title: str,
) -> dict:

    level = random.randint(
        0,
        100,
    )

    muted = (
        level == 0
        or random.random() < 0.08
    )

    return {
        "semantic":
            semantic,

        "title":
            title,

        "level":
            0 if muted else level,

        "muted":
            muted,

        "icon":
            volume_icon(
                semantic,
                level,
                muted,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_volume_panel_data() -> dict:

    # ======================================================
    # Main Panel State
    # ======================================================

    panel_state = random.choices(
        [
            "collapsed",
            "expanded",
        ],
        weights=[
            0.55,
            0.45,
        ],
        k=1,
    )[0]


    # ======================================================
    # Ring Mode
    # ======================================================

    ring_mode = random.choices(
        [
            "normal",
            "vibrate",
            "silent",
        ],
        weights=[
            0.62,
            0.23,
            0.15,
        ],
        k=1,
    )[0]


    if ring_mode == "normal":

        ring_mode_icon = (
            "mdi:bell"
        )

        ring_mode_label = (
            "Ring"
        )

    elif ring_mode == "vibrate":

        ring_mode_icon = (
            "mdi:vibrate"
        )

        ring_mode_label = (
            "Vibrate"
        )

    else:

        ring_mode_icon = (
            "mdi:bell-off"
        )

        ring_mode_label = (
            "Silent"
        )


    # ======================================================
    # Volume Streams
    # ======================================================

    media = build_stream(
        "media",
        "Media",
    )

    ring = build_stream(
        "ring",
        "Ring",
    )

    alarm = build_stream(
        "alarm",
        "Alarm",
    )

    call = build_stream(
        "call",
        "Call",
    )


    # ======================================================
    # Output
    # ======================================================

    audio_output = random.choice(
        AUDIO_OUTPUTS
    )


    # ======================================================
    # Extra Features
    # ======================================================

    live_caption = (
        random.random()
        < 0.28
    )

    show_output_selector = (
        random.random()
        < 0.52
    )

    show_live_caption = (
        random.random()
        < 0.68
    )

    show_settings = (
        random.random()
        < 0.82
    )


    # ======================================================
    # Position
    # ======================================================

    panel_side = random.choices(
        [
            "right",
            "left",
        ],
        weights=[
            0.90,
            0.10,
        ],
        k=1,
    )[0]


    # ======================================================
    # Result
    # ======================================================

    return {
        "panel_state":
            panel_state,

        "panel_side":
            panel_side,

        "wallpaper":
            get_wallpaper(),

        "ring_mode":
            ring_mode,

        "ring_mode_icon":
            ring_mode_icon,

        "ring_mode_label":
            ring_mode_label,

        "media":
            media,

        "ring":
            ring,

        "alarm":
            alarm,

        "call":
            call,

        "audio_output":
            audio_output,

        "show_output_selector":
            show_output_selector,

        "show_live_caption":
            show_live_caption,

        "live_caption":
            live_caption,

        "show_settings":
            show_settings,
    }