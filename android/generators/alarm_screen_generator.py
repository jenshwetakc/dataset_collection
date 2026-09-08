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
# Helpers
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
# Alarm Labels
# ==========================================================

ALARM_LABELS = [
    "Morning alarm",
    "Wake up",
    "Work",
    "Gym",
    "Class",
    "Meeting",
    "Medication",
    "Nap",
    "Reminder",
]


# ==========================================================
# Alarm Sounds
# ==========================================================

ALARM_SOUNDS = [
    "Default",
    "Gentle",
    "Sunrise",
    "Bright Morning",
    "Classic Alarm",
    "Soft Bells",
]


# ==========================================================
# Main Generator
# ==========================================================

def generate_alarm_screen_data() -> dict:

    # ======================================================
    # Main State
    # ======================================================

    screen_state = random.choices(
        [
            "alarm_ringing",
            "alarm_snoozed",
            "alarm_dismissed",
            "upcoming_alarm",
            "timer_running",
            "timer_finished",
            "bedtime_alarm",
        ],
        weights=[
            0.30,
            0.10,
            0.08,
            0.12,
            0.16,
            0.14,
            0.10,
        ],
        k=1,
    )[0]


    # ======================================================
    # Layout
    # ======================================================

    layout_variant = random.choices(
        [
            "fullscreen",
            "compact_card",
        ],
        weights=[
            0.82,
            0.18,
        ],
        k=1,
    )[0]


    # ======================================================
    # Time
    # ======================================================

    hour = random.randint(
        1,
        12,
    )

    minute = random.choice([
        0,
        5,
        10,
        15,
        20,
        25,
        30,
        35,
        40,
        45,
        50,
        55,
    ])

    period = random.choice([
        "AM",
        "PM",
    ])

    alarm_time = (
        f"{hour}:{minute:02d}"
    )


    # ======================================================
    # Label
    # ======================================================

    label = random.choice(
        ALARM_LABELS
    )


    # ======================================================
    # Alarm Behavior
    # ======================================================

    vibration = (
        random.random()
        < 0.72
    )

    sound = random.choice(
        ALARM_SOUNDS
    )

    snooze_minutes = random.choice([
        5,
        10,
        15,
    ])


    # ======================================================
    # Timer
    # ======================================================

    timer_total = random.choice([
        60,
        120,
        180,
        300,
        600,
        900,
    ])

    timer_remaining = random.randint(
        0,
        timer_total,
    )

    if screen_state == "timer_finished":

        timer_remaining = 0


    timer_minutes = (
        timer_remaining
        // 60
    )

    timer_seconds = (
        timer_remaining
        % 60
    )

    timer_text = (
        f"{timer_minutes:02d}:"
        f"{timer_seconds:02d}"
    )


    timer_progress = (
        0
        if timer_total == 0
        else int(
            (
                timer_remaining
                / timer_total
            )
            * 100
        )
    )


    # ======================================================
    # Upcoming
    # ======================================================

    upcoming_minutes = random.choice([
        5,
        10,
        15,
        30,
        45,
    ])


    # ======================================================
    # Bedtime
    # ======================================================

    bedtime_message = random.choice([
        "Good morning",
        "Time to wake up",
        "Your day starts now",
    ])


    # ======================================================
    # Result
    # ======================================================

    return {

        "screen_state":
            screen_state,

        "layout_variant":
            layout_variant,

        "wallpaper":
            get_wallpaper(),

        "alarm_time":
            alarm_time,

        "period":
            period,

        "label":
            label,

        "vibration":
            vibration,

        "sound":
            sound,

        "snooze_minutes":
            snooze_minutes,

        "timer_text":
            timer_text,

        "timer_progress":
            timer_progress,

        "upcoming_minutes":
            upcoming_minutes,

        "bedtime_message":
            bedtime_message,
    }