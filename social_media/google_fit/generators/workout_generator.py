from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# Supported States
# ==========================================================

WORKOUT_STATES = [
    "ready",
    "countdown",
    "active",
    "paused",
    "completed",
    "gps_error",
]


# ==========================================================
# Workout Types
# ==========================================================

WORKOUT_TYPES = [
    {
        "name": "Walking",
        "icon": "directions_walk",
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "name": "Running",
        "icon": "directions_run",
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "name": "Cycling",
        "icon": "directions_bike",
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "name": "Hiking",
        "icon": "hiking",
        "supports_distance": True,
        "supports_route": True,
    },
    {
        "name": "Strength training",
        "icon": "fitness_center",
        "supports_distance": False,
        "supports_route": False,
    },
    {
        "name": "Yoga",
        "icon": "self_improvement",
        "supports_distance": False,
        "supports_route": False,
    },
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
    },
    {
        "label": "Journal",
        "icon": "view_timeline",
    },
    {
        "label": "Browse",
        "icon": "explore",
    },
    {
        "label": "Profile",
        "icon": "person",
    },
]


# ==========================================================
# Duration
# ==========================================================

def format_duration(
    seconds: int,
) -> str:

    hours = (
        seconds // 3600
    )

    minutes = (
        seconds % 3600
    ) // 60

    remaining_seconds = (
        seconds % 60
    )

    if hours:

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{remaining_seconds:02d}"
        )

    return (
        f"{minutes:02d}:"
        f"{remaining_seconds:02d}"
    )


# ==========================================================
# Live Metrics
# ==========================================================

def generate_metrics(
    workout: dict,
) -> dict:

    duration_seconds = random.randint(
        280,
        5400,
    )

    distance = (
        round(
            random.uniform(
                0.8,
                14.5,
            ),
            2,
        )
        if workout[
            "supports_distance"
        ]
        else None
    )

    calories = random.randint(
        45,
        720,
    )

    heart_rate = random.randint(
        92,
        168,
    )

    steps = (
        random.randint(
            600,
            14500,
        )
        if workout["name"]
        in {
            "Walking",
            "Running",
            "Hiking",
        }
        else None
    )

    pace = None

    if distance:

        duration_minutes = (
            duration_seconds
            / 60
        )

        pace_value = (
            duration_minutes
            / distance
        )

        pace_minutes = int(
            pace_value
        )

        pace_seconds = int(
            (
                pace_value
                - pace_minutes
            )
            * 60
        )

        pace = (
            f"{pace_minutes}:"
            f"{pace_seconds:02d}"
        )

    return {

        "duration_seconds":
            duration_seconds,

        "duration":
            format_duration(
                duration_seconds
            ),

        "distance":
            (
                f"{distance:.2f}"
                if distance is not None
                else None
            ),

        "distance_unit":
            "km",

        "calories":
            calories,

        "heart_rate":
            heart_rate,

        "heart_zone":
            random.choice(
                [
                    "Light",
                    "Moderate",
                    "Cardio",
                    "Peak",
                ]
            ),

        "steps":
            (
                f"{steps:,}"
                if steps is not None
                else None
            ),

        "pace":
            pace,

        "pace_unit":
            "/km",
    }


# ==========================================================
# Completed Summary
# ==========================================================

def generate_completed_data(
    workout: dict,
    metrics: dict,
) -> dict:

    start = (
        datetime.now()
        - timedelta(
            seconds=
                metrics[
                    "duration_seconds"
                ]
        )
    )

    return {

        "start_time":
            start.strftime(
                "%H:%M"
            ),

        "end_time":
            datetime.now().strftime(
                "%H:%M"
            ),

        "heart_points":
            random.randint(
                5,
                45,
            ),

        "average_heart_rate":
            random.randint(
                85,
                148,
            ),

        "max_heart_rate":
            random.randint(
                130,
                188,
            ),

        "elevation":
            (
                random.randint(
                    10,
                    390,
                )
                if workout[
                    "supports_route"
                ]
                else None
            ),
    }


# ==========================================================
# Ready State
# ==========================================================

def generate_ready_state(
    workout: dict,
) -> dict:

    return {

        "headline":
            f"Ready for {workout['name'].lower()}?",

        "message":
            "Your workout will begin when you tap Start.",

        "countdown":
            None,

        "metrics":
            None,

        "completed":
            None,
    }


# ==========================================================
# Countdown
# ==========================================================

def generate_countdown_state(
    workout: dict,
) -> dict:

    return {

        "headline":
            "Get ready",

        "message":
            workout["name"],

        "countdown":
            random.choice(
                [
                    3,
                    2,
                    1,
                ]
            ),

        "metrics":
            None,

        "completed":
            None,
    }


# ==========================================================
# Active / Paused
# ==========================================================

def generate_live_state(
    workout: dict,
    paused: bool = False,
) -> dict:

    metrics = (
        generate_metrics(
            workout
        )
    )

    return {

        "headline":
            (
                "Workout paused"
                if paused
                else workout[
                    "name"
                ]
            ),

        "message":
            (
                "Your activity is paused"
                if paused
                else "Workout in progress"
            ),

        "countdown":
            None,

        "metrics":
            metrics,

        "completed":
            None,
    }


# ==========================================================
# Completed
# ==========================================================

def generate_completed_state(
    workout: dict,
) -> dict:

    metrics = (
        generate_metrics(
            workout
        )
    )

    return {

        "headline":
            "Workout complete",

        "message":
            f"Great job on your {workout['name'].lower()}.",

        "countdown":
            None,

        "metrics":
            metrics,

        "completed":
            generate_completed_data(
                workout,
                metrics,
            ),
    }


# ==========================================================
# GPS Error
# ==========================================================

def generate_gps_error_state(
    workout: dict,
) -> dict:

    return {

        "headline":
            "Location unavailable",

        "message":
            (
                "Fit can't get a reliable GPS signal. "
                "Move to an open area or continue without a route."
            ),

        "countdown":
            None,

        "metrics":
            None,

        "completed":
            None,
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_workout_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            WORKOUT_STATES
        )

    if state not in (
        WORKOUT_STATES
    ):

        raise ValueError(
            f"Unknown workout state: "
            f"{state}. "
            f"Available states: "
            f"{WORKOUT_STATES}"
        )


    workout = random.choice(
        WORKOUT_TYPES
    )


    if state == "ready":

        state_data = (
            generate_ready_state(
                workout
            )
        )

    elif state == "countdown":

        state_data = (
            generate_countdown_state(
                workout
            )
        )

    elif state == "active":

        state_data = (
            generate_live_state(
                workout,
                paused=False,
            )
        )

    elif state == "paused":

        state_data = (
            generate_live_state(
                workout,
                paused=True,
            )
        )

    elif state == "completed":

        state_data = (
            generate_completed_state(
                workout
            )
        )

    else:

        state_data = (
            generate_gps_error_state(
                workout
            )
        )


    return {

        "state":
            state,

        "workout":
            workout,

        "navigation_items": [
            dict(
                item
            )
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

    for state in WORKOUT_STATES:

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
            generate_workout_data(
                state=state
            )
        )