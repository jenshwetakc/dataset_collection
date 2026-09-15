from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# States
# ==========================================================

HYDRATION_STATES = [
    "normal",
    "goal_reached",
    "empty",
    "quick_add",
    "custom_add",
    "reminders",
    "saving",
]


# ==========================================================
# Quick Add Options
# ==========================================================

QUICK_ADD_OPTIONS = [
    {
        "label": "Small",
        "amount": 150,
        "icon": "local_drink",
    },
    {
        "label": "Glass",
        "amount": 250,
        "icon": "water_full",
    },
    {
        "label": "Bottle",
        "amount": 500,
        "icon": "water_bottle",
    },
    {
        "label": "Large",
        "amount": 750,
        "icon": "water",
    },
]


# ==========================================================
# Reminder Options
# ==========================================================

REMINDER_OPTIONS = [
    {
        "label": "Morning reminder",
        "icon": "wb_sunny",
        "time": "08:30",
    },
    {
        "label": "Lunch reminder",
        "icon": "restaurant",
        "time": "12:30",
    },
    {
        "label": "Afternoon reminder",
        "icon": "schedule",
        "time": "15:30",
    },
    {
        "label": "Evening reminder",
        "icon": "dark_mode",
        "time": "19:00",
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
# Helper
# ==========================================================

def format_ml(
    amount: int,
) -> str:

    if amount >= 1000:

        liters = (
            amount / 1000
        )

        return (
            f"{liters:.1f} L"
        )

    return (
        f"{amount} ml"
    )


# ==========================================================
# History
# ==========================================================

def generate_history(
    count: int = 6,
) -> list[dict]:

    now = datetime.now()

    history = []

    for index in range(
        count
    ):

        amount = random.choice(
            [
                150,
                200,
                250,
                300,
                500,
            ]
        )

        time = (
            now
            - timedelta(
                minutes=
                    index
                    * random.randint(
                        50,
                        110,
                    )
            )
        )

        history.append(
            {
                "id":
                    index,

                "amount":
                    amount,

                "amount_label":
                    format_ml(
                        amount
                    ),

                "time":
                    time.strftime(
                        "%H:%M"
                    ),

                "icon":
                    random.choice(
                        [
                            "water_drop",
                            "local_drink",
                            "water_full",
                        ]
                    ),
            }
        )

    return history


# ==========================================================
# Weekly
# ==========================================================

def generate_weekly() -> list[dict]:

    today = datetime.now()

    result = []

    for offset in range(
        6,
        -1,
        -1,
    ):

        date = (
            today
            - timedelta(
                days=offset
            )
        )

        amount = random.randint(
            900,
            3200,
        )

        result.append(
            {
                "day":
                    date.strftime(
                        "%a"
                    )[0],

                "amount":
                    amount,

                "label":
                    format_ml(
                        amount
                    ),

                "height":
                    random.randint(
                        30,
                        100,
                    ),
            }
        )

    return result


# ==========================================================
# Normal
# ==========================================================

def generate_normal_state(
    goal_reached: bool = False,
) -> dict:

    goal = random.choice(
        [
            1800,
            2000,
            2200,
            2500,
            3000,
        ]
    )

    if goal_reached:

        current = random.randint(
            goal,
            int(
                goal * 1.3
            ),
        )

    else:

        current = random.randint(
            int(
                goal * 0.30
            ),
            int(
                goal * 0.95
            ),
        )

    progress = min(
        1.0,
        current / goal,
    )

    remaining = max(
        0,
        goal - current,
    )

    return {

        "goal":
            goal,

        "goal_label":
            format_ml(
                goal
            ),

        "current":
            current,

        "current_label":
            format_ml(
                current
            ),

        "remaining":
            remaining,

        "remaining_label":
            format_ml(
                remaining
            ),

        "progress":
            progress,

        "history":
            generate_history(),

        "weekly":
            generate_weekly(),

        "quick_add":
            [
                dict(item)
                for item
                in QUICK_ADD_OPTIONS
            ],

        "reminders":
            [],

        "message":
            (
                "Daily goal reached"
                if goal_reached
                else None
            ),

        "description":
            (
                "You've reached your hydration target for today."
                if goal_reached
                else None
            ),

        "selected_amount":
            None,

        "saving_progress":
            None,
    }


# ==========================================================
# Empty
# ==========================================================

def generate_empty_state() -> dict:

    return {

        "goal":
            2000,

        "goal_label":
            "2.0 L",

        "current":
            0,

        "current_label":
            "0 ml",

        "remaining":
            2000,

        "remaining_label":
            "2.0 L",

        "progress":
            0.0,

        "history":
            [],

        "weekly":
            [],

        "quick_add":
            [
                dict(item)
                for item
                in QUICK_ADD_OPTIONS
            ],

        "reminders":
            [],

        "message":
            "No water logged today",

        "description":
            (
                "Start logging drinks to track "
                "your hydration progress."
            ),

        "selected_amount":
            None,

        "saving_progress":
            None,
    }


# ==========================================================
# Quick Add
# ==========================================================

def generate_quick_add_state() -> dict:

    data = (
        generate_normal_state()
    )

    selected = random.choice(
        QUICK_ADD_OPTIONS
    )

    data.update(
        {
            "selected_amount":
                dict(selected),
        }
    )

    return data


# ==========================================================
# Custom Add
# ==========================================================

def generate_custom_add_state() -> dict:

    data = (
        generate_normal_state()
    )

    data.update(
        {
            "selected_amount": {
                "label":
                    "Custom",

                "amount":
                    random.choice(
                        [
                            300,
                            350,
                            400,
                            600,
                        ]
                    ),

                "icon":
                    "edit",
            },
        }
    )

    return data


# ==========================================================
# Reminders
# ==========================================================

def generate_reminders_state() -> dict:

    data = (
        generate_normal_state()
    )

    reminders = []

    for option in REMINDER_OPTIONS:

        reminders.append(
            {
                **option,

                "enabled":
                    random.choice(
                        [
                            True,
                            True,
                            False,
                        ]
                    ),
            }
        )

    data.update(
        {
            "reminders":
                reminders,
        }
    )

    return data


# ==========================================================
# Saving
# ==========================================================

def generate_saving_state() -> dict:

    data = (
        generate_normal_state()
    )

    data.update(
        {
            "message":
                "Saving hydration data",

            "description":
                "Updating today's water intake.",

            "saving_progress":
                random.randint(
                    25,
                    90,
                ),
        }
    )

    return data


# ==========================================================
# Public Generator
# ==========================================================

def generate_hydration_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            HYDRATION_STATES
        )


    if state not in (
        HYDRATION_STATES
    ):

        raise ValueError(
            f"Unknown hydration state: "
            f"{state}. "
            f"Available states: "
            f"{HYDRATION_STATES}"
        )


    if state == "normal":

        state_data = (
            generate_normal_state()
        )

    elif state == "goal_reached":

        state_data = (
            generate_normal_state(
                goal_reached=True
            )
        )

    elif state == "empty":

        state_data = (
            generate_empty_state()
        )

    elif state == "quick_add":

        state_data = (
            generate_quick_add_state()
        )

    elif state == "custom_add":

        state_data = (
            generate_custom_add_state()
        )

    elif state == "reminders":

        state_data = (
            generate_reminders_state()
        )

    else:

        state_data = (
            generate_saving_state()
        )


    return {

        "state":
            state,

        "title":
            "Hydration",

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

    for state in HYDRATION_STATES:

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
            generate_hydration_data(
                state=state
            )
        )