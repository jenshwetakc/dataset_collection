from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# States
# ==========================================================

BODY_MEASUREMENT_STATES = [
    "normal",
    "empty",
    "add_measurement",
    "validation_error",
    "goal_reached",
    "syncing",
]


# ==========================================================
# Time Ranges
# ==========================================================

TIME_RANGES = [
    {
        "label": "Week",
        "active": False,
    },
    {
        "label": "Month",
        "active": True,
    },
    {
        "label": "3 months",
        "active": False,
    },
    {
        "label": "Year",
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
# Helpers
# ==========================================================

def format_weight(
    value: float,
) -> str:

    return f"{value:.1f}"


def calculate_bmi(
    weight_kg: float,
    height_cm: int,
) -> float:

    height_m = (
        height_cm
        / 100
    )

    return round(
        weight_kg
        / (
            height_m
            * height_m
        ),
        1,
    )


def get_bmi_status(
    bmi: float,
) -> dict:

    if bmi < 18.5:

        return {
            "label": "Low range",
            "icon": "south",
        }

    if bmi < 25:

        return {
            "label": "Healthy range",
            "icon": "check_circle",
        }

    if bmi < 30:

        return {
            "label": "Above range",
            "icon": "north",
        }

    return {
        "label": "High range",
        "icon": "warning",
    }


# ==========================================================
# History
# ==========================================================

def generate_history(
    current_weight: float,
    count: int = 8,
) -> list[dict]:

    now = datetime.now()

    history = []

    weight = (
        current_weight
        + random.uniform(
            1.0,
            4.0,
        )
    )

    for index in range(
        count
    ):

        date = (
            now
            - timedelta(
                days=
                    (
                        count
                        - index
                        - 1
                    )
                    * random.randint(
                        3,
                        7,
                    )
            )
        )

        weight -= random.uniform(
            0.1,
            0.8,
        )

        history.append(
            {
                "id":
                    index,

                "date":
                    date.strftime(
                        "%b %d"
                    ),

                "time":
                    random.choice(
                        [
                            "07:15",
                            "08:10",
                            "18:30",
                            "21:05",
                        ]
                    ),

                "weight":
                    round(
                        weight,
                        1,
                    ),

                "weight_label":
                    format_weight(
                        weight
                    ),

                "source":
                    random.choice(
                        [
                            "Manual",
                            "Smart scale",
                            "Health Connect",
                        ]
                    ),
            }
        )

    return history


# ==========================================================
# Trend
# ==========================================================

def generate_trend(
    history: list[dict],
) -> list[dict]:

    if not history:

        return []

    values = [
        item["weight"]
        for item in history
    ]

    minimum = min(
        values
    )

    maximum = max(
        values
    )

    spread = max(
        0.5,
        maximum - minimum,
    )

    result = []

    for item in history:

        normalized = (
            (
                item["weight"]
                - minimum
            )
            / spread
        )

        result.append(
            {
                **item,

                "height":
                    int(
                        28
                        + normalized
                        * 68
                    ),
            }
        )

    return result


# ==========================================================
# Normal State
# ==========================================================

def generate_normal_state(
    goal_reached: bool = False,
) -> dict:

    height_cm = random.randint(
        155,
        188,
    )

    goal_weight = round(
        random.uniform(
            55.0,
            78.0,
        ),
        1,
    )

    if goal_reached:

        current_weight = round(
            goal_weight
            - random.uniform(
                0.0,
                1.0,
            ),
            1,
        )

    else:

        current_weight = round(
            goal_weight
            + random.uniform(
                1.5,
                8.0,
            ),
            1,
        )

    bmi = calculate_bmi(
        current_weight,
        height_cm,
    )

    bmi_status = (
        get_bmi_status(
            bmi
        )
    )

    history = generate_history(
        current_weight=
            current_weight,
    )

    difference = round(
        current_weight
        - goal_weight,
        1,
    )

    progress = (
        1.0
        if goal_reached
        else max(
            0.10,
            min(
                0.95,
                random.uniform(
                    0.35,
                    0.90,
                ),
            ),
        )
    )

    return {

        "current_weight":
            current_weight,

        "current_weight_label":
            format_weight(
                current_weight
            ),

        "goal_weight":
            goal_weight,

        "goal_weight_label":
            format_weight(
                goal_weight
            ),

        "height_cm":
            height_cm,

        "bmi":
            bmi,

        "bmi_status":
            bmi_status,

        "difference":
            difference,

        "difference_label":
            f"{abs(difference):.1f}",

        "goal_progress":
            progress,

        "history":
            history,

        "trend":
            generate_trend(
                history
            ),

        "selected_measurement":
            None,

        "sync_progress":
            None,

        "message":
            (
                "Weight goal reached"
                if goal_reached
                else None
            ),

        "description":
            (
                "You've reached your current weight target."
                if goal_reached
                else None
            ),
    }


# ==========================================================
# Empty
# ==========================================================

def generate_empty_state() -> dict:

    return {

        "current_weight":
            None,

        "current_weight_label":
            None,

        "goal_weight":
            None,

        "goal_weight_label":
            None,

        "height_cm":
            None,

        "bmi":
            None,

        "bmi_status":
            None,

        "difference":
            None,

        "difference_label":
            None,

        "goal_progress":
            0,

        "history":
            [],

        "trend":
            [],

        "selected_measurement":
            None,

        "sync_progress":
            None,

        "message":
            "No measurements yet",

        "description":
            (
                "Add your first weight measurement "
                "to start tracking trends over time."
            ),
    }


# ==========================================================
# Add Measurement
# ==========================================================

def generate_add_measurement_state(
    validation_error: bool = False,
) -> dict:

    data = (
        generate_normal_state()
    )

    measurement = {

        "weight":
            (
                0
                if validation_error
                else round(
                    random.uniform(
                        52.0,
                        95.0,
                    ),
                    1,
                )
            ),

        "unit":
            "kg",

        "date":
            datetime.now().strftime(
                "%Y-%m-%d"
            ),

        "time":
            datetime.now().strftime(
                "%H:%M"
            ),
    }

    data.update(
        {
            "selected_measurement":
                measurement,

            "message":
                (
                    "Check measurement"
                    if validation_error
                    else "Add measurement"
                ),

            "description":
                (
                    "Weight must be greater than zero."
                    if validation_error
                    else
                    "Record a new body-weight measurement."
                ),
        }
    )

    return data


# ==========================================================
# Syncing
# ==========================================================

def generate_syncing_state() -> dict:

    data = (
        generate_normal_state()
    )

    data.update(
        {
            "sync_progress":
                random.randint(
                    20,
                    88,
                ),

            "message":
                "Syncing measurements",

            "description":
                (
                    "Fit is checking connected health "
                    "services for recent measurements."
                ),
        }
    )

    return data


# ==========================================================
# Public Generator
# ==========================================================

def generate_body_measurements_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            BODY_MEASUREMENT_STATES
        )

    if state not in (
        BODY_MEASUREMENT_STATES
    ):

        raise ValueError(
            f"Unknown body measurement state: "
            f"{state}. "
            f"Available states: "
            f"{BODY_MEASUREMENT_STATES}"
        )


    if state == "normal":

        state_data = (
            generate_normal_state()
        )

    elif state == "empty":

        state_data = (
            generate_empty_state()
        )

    elif state == "add_measurement":

        state_data = (
            generate_add_measurement_state()
        )

    elif state == "validation_error":

        state_data = (
            generate_add_measurement_state(
                validation_error=True
            )
        )

    elif state == "goal_reached":

        state_data = (
            generate_normal_state(
                goal_reached=True
            )
        )

    else:

        state_data = (
            generate_syncing_state()
        )


    return {

        "state":
            state,

        "title":
            "Body measurements",

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

    for state in (
        BODY_MEASUREMENT_STATES
    ):

        print(
            "\n"
            "=================================="
        )

        print(
            state.upper()
        )

        print(
            "=================================="
        )

        pprint(
            generate_body_measurements_data(
                state=state
            )
        )