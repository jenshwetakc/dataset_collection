from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# States
# ==========================================================

HEART_RATE_STATES = [
    "live",
    "history",
    "measuring",
    "no_data",
    "high_alert",
    "permission_required",
]


# ==========================================================
# Time Ranges
# ==========================================================

TIME_RANGES = [
    {
        "label": "Day",
        "active": True,
    },
    {
        "label": "Week",
        "active": False,
    },
    {
        "label": "Month",
        "active": False,
    },
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "active": False,
    },
    {
        "label": "Journal",
        "icon": "view_timeline",
        "active": False,
    },
    {
        "label": "Browse",
        "icon": "explore",
        "active": True,
    },
    {
        "label": "Profile",
        "icon": "person",
        "active": False,
    },
]


# ==========================================================
# Heart Zone
# ==========================================================

def get_heart_zone(
    bpm: int,
) -> dict:

    if bpm < 60:

        return {
            "label": "Low",
            "icon": "arrow_downward",
        }

    if bpm < 100:

        return {
            "label": "Resting",
            "icon": "favorite",
        }

    if bpm < 130:

        return {
            "label": "Light",
            "icon": "directions_walk",
        }

    if bpm < 160:

        return {
            "label": "Cardio",
            "icon": "directions_run",
        }

    return {
        "label": "Peak",
        "icon": "local_fire_department",
    }


# ==========================================================
# History Points
# ==========================================================

def generate_history_points(
    count: int = 24,
) -> list[dict]:

    result = []

    current = (
        datetime.now()
        - timedelta(
            hours=count - 1
        )
    )

    for index in range(
        count
    ):

        bpm = random.randint(
            58,
            138,
        )

        result.append(
            {
                "index":
                    index,

                "time":
                    current.strftime(
                        "%H:%M"
                    ),

                "bpm":
                    bpm,

                "height":
                    max(
                        15,
                        min(
                            100,
                            int(
                                (
                                    bpm - 45
                                )
                                / 120
                                * 100
                            ),
                        ),
                    ),
            }
        )

        current += timedelta(
            hours=1
        )

    return result


# ==========================================================
# Recent Readings
# ==========================================================

def generate_recent_readings(
    count: int = 5,
) -> list[dict]:

    now = datetime.now()

    result = []

    for index in range(
        count
    ):

        timestamp = (
            now
            - timedelta(
                minutes=
                    index
                    * random.randint(
                        18,
                        48,
                    )
            )
        )

        bpm = random.randint(
            58,
            115,
        )

        zone = get_heart_zone(
            bpm
        )

        result.append(
            {
                "time":
                    timestamp.strftime(
                        "%H:%M"
                    ),

                "bpm":
                    bpm,

                "zone":
                    zone["label"],

                "icon":
                    zone["icon"],
            }
        )

    return result


# ==========================================================
# Summary
# ==========================================================

def generate_summary() -> dict:

    resting = random.randint(
        55,
        78,
    )

    low = random.randint(
        48,
        resting,
    )

    high = random.randint(
        105,
        172,
    )

    return {

        "resting":
            resting,

        "low":
            low,

        "high":
            high,

        "average":
            random.randint(
                resting,
                min(
                    high,
                    110,
                ),
            ),
    }


# ==========================================================
# Live
# ==========================================================

def generate_live_state() -> dict:

    bpm = random.randint(
        58,
        138,
    )

    zone = get_heart_zone(
        bpm
    )

    return {

        "current_bpm":
            bpm,

        "zone":
            zone,

        "last_updated":
            "Just now",

        "summary":
            generate_summary(),

        "history_points":
            generate_history_points(),

        "recent_readings":
            generate_recent_readings(),

        "progress":
            None,

        "message":
            None,

        "description":
            None,
    }


# ==========================================================
# History
# ==========================================================

def generate_history_state() -> dict:

    return {

        "current_bpm":
            None,

        "zone":
            None,

        "last_updated":
            None,

        "summary":
            generate_summary(),

        "history_points":
            generate_history_points(),

        "recent_readings":
            generate_recent_readings(
                count=7
            ),

        "progress":
            None,

        "message":
            None,

        "description":
            None,
    }


# ==========================================================
# Measuring
# ==========================================================

def generate_measuring_state() -> dict:

    return {

        "current_bpm":
            None,

        "zone":
            None,

        "last_updated":
            None,

        "summary":
            None,

        "history_points":
            [],

        "recent_readings":
            [],

        "progress":
            random.randint(
                15,
                85,
            ),

        "message":
            "Measuring heart rate",

        "description":
            (
                "Stay still while your connected sensor "
                "measures your heart rate."
            ),
    }


# ==========================================================
# No Data
# ==========================================================

def generate_no_data_state() -> dict:

    return {

        "current_bpm":
            None,

        "zone":
            None,

        "last_updated":
            None,

        "summary":
            None,

        "history_points":
            [],

        "recent_readings":
            [],

        "progress":
            None,

        "message":
            "No heart-rate data",

        "description":
            (
                "Connect a compatible watch or heart-rate "
                "sensor to start recording readings."
            ),
    }


# ==========================================================
# High Alert
# ==========================================================

def generate_high_alert_state() -> dict:

    bpm = random.randint(
        145,
        188,
    )

    return {

        "current_bpm":
            bpm,

        "zone":
            {
                "label":
                    "High",

                "icon":
                    "warning",
            },

        "last_updated":
            "Just now",

        "summary":
            generate_summary(),

        "history_points":
            generate_history_points(),

        "recent_readings":
            generate_recent_readings(),

        "progress":
            None,

        "message":
            "High heart rate detected",

        "description":
            (
                "Your latest reading is above your recent "
                "resting range."
            ),
    }


# ==========================================================
# Permission
# ==========================================================

def generate_permission_state() -> dict:

    return {

        "current_bpm":
            None,

        "zone":
            None,

        "last_updated":
            None,

        "summary":
            None,

        "history_points":
            [],

        "recent_readings":
            [],

        "progress":
            None,

        "message":
            "Allow heart-rate access",

        "description":
            (
                "Fit needs permission to read heart-rate "
                "measurements from connected health services."
            ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_heart_rate_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            HEART_RATE_STATES
        )


    if state not in HEART_RATE_STATES:

        raise ValueError(
            f"Unknown heart rate state: "
            f"{state}. "
            f"Available states: "
            f"{HEART_RATE_STATES}"
        )


    if state == "live":

        state_data = (
            generate_live_state()
        )

    elif state == "history":

        state_data = (
            generate_history_state()
        )

    elif state == "measuring":

        state_data = (
            generate_measuring_state()
        )

    elif state == "no_data":

        state_data = (
            generate_no_data_state()
        )

    elif state == "high_alert":

        state_data = (
            generate_high_alert_state()
        )

    else:

        state_data = (
            generate_permission_state()
        )


    return {

        "state":
            state,

        "title":
            "Heart rate",

        "time_ranges": [
            dict(item)
            for item
            in TIME_RANGES
        ],

        "navigation_items": [
            dict(item)
            for item
            in NAVIGATION_ITEMS
        ],

        **state_data,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in HEART_RATE_STATES:

        print(
            "\n"
            "===================================="
        )

        print(
            state.upper()
        )

        print(
            "===================================="
        )

        pprint(
            generate_heart_rate_data(
                state=state
            )
        )