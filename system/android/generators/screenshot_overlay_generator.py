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

SCREENSHOT_DIR = (
    ANDROID_ROOT
    / "assets"
    / "screenshots"
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
# Main Generator
# ==========================================================

def generate_screenshot_overlay_data() -> dict:

    # ======================================================
    # Overlay State
    # ======================================================

    overlay_state = random.choices(
        [
            "captured",
            "expanded_preview",
            "scroll_available",
            "scrolling",
            "saved",
            "failed",
        ],
        weights=[
            0.38,
            0.16,
            0.16,
            0.10,
            0.12,
            0.08,
        ],
        k=1,
    )[0]


    # ======================================================
    # Preview Orientation
    # ======================================================

    preview_orientation = random.choice([
        "portrait",
        "landscape",
    ])


    # ======================================================
    # Screenshot
    # ======================================================

    screenshot = get_random_asset(
        SCREENSHOT_DIR
    )


    # ======================================================
    # Actions
    # ======================================================

    show_share = (
        overlay_state
        not in {
            "failed",
            "scrolling",
        }
        and random.random() < 0.92
    )

    show_edit = (
        overlay_state
        not in {
            "failed",
            "scrolling",
        }
        and random.random() < 0.88
    )

    show_delete = (
        overlay_state
        not in {
            "failed",
            "scrolling",
        }
        and random.random() < 0.76
    )

    show_copy_text = (
        overlay_state
        not in {
            "failed",
            "scrolling",
        }
        and random.random() < 0.42
    )

    show_scroll_capture = (
        overlay_state
        in {
            "scroll_available",
            "scrolling",
        }
    )


    # ======================================================
    # Progress
    # ======================================================

    scroll_progress = (
        random.randint(
            20,
            88,
        )
        if overlay_state
        == "scrolling"
        else None
    )


    # ======================================================
    # Saved State
    # ======================================================

    show_saved_message = (
        overlay_state
        == "saved"
    )


    # ======================================================
    # Failed State
    # ======================================================

    failure_reason = None

    if overlay_state == "failed":

        failure_reason = random.choice([
            "Couldn't save screenshot",
            "Screenshot isn't available",
            "Couldn't capture this screen",
        ])


    # ======================================================
    # Position
    # ======================================================

    overlay_position = random.choices(
        [
            "bottom",
            "lower_left",
        ],
        weights=[
            0.72,
            0.28,
        ],
        k=1,
    )[0]


    # ======================================================
    # Result
    # ======================================================

    return {

        "overlay_state":
            overlay_state,

        "overlay_position":
            overlay_position,

        "preview_orientation":
            preview_orientation,

        "wallpaper":
            get_random_asset(
                WALLPAPER_DIR
            ),

        "screenshot":
            screenshot,

        "show_share":
            show_share,

        "show_edit":
            show_edit,

        "show_delete":
            show_delete,

        "show_copy_text":
            show_copy_text,

        "show_scroll_capture":
            show_scroll_capture,

        "scroll_progress":
            scroll_progress,

        "show_saved_message":
            show_saved_message,

        "failure_reason":
            failure_reason,
    }