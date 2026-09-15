from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

GOAL_STATES = [
    "overview",
    "editing",
    "completed",
    "no_goals",
    "saving",
    "validation_error",
]


# ==========================================================
# Goal Definitions
# ==========================================================

GOAL_TYPES = [
    {
        "key": "steps",
        "title": "Daily steps",
        "icon": "directions_walk",
        "unit": "steps",
        "targets": [
            5000,
            7000,
            8000,
            10000,
            12000,
        ],
    },
    {
        "key": "heart_points",
        "title": "Heart Points",
        "icon": "favorite",
        "unit": "points",
        "targets": [
            20,
            30,
            40,
            50,
            60,
        ],
    },
    {
        "key": "move_minutes",
        "title": "Move minutes",
        "icon": "timer",
        "unit": "min",
        "targets": [
            30,
            45,
            60,
            75,
            90,
        ],
    },
    {
        "key": "sleep",
        "title": "Sleep",
        "icon": "bedtime",
        "unit": "hr",
        "targets": [
            7,
            8,
            9,
        ],
    },
]


# ==========================================================
# Suggestions
# ==========================================================

SUGGESTIONS = [
    {
        "title": "Walk more",
        "description":
            "Try increasing your daily step goal gradually.",
        "icon": "directions_walk",
    },
    {
        "title": "Stay consistent",
        "description":
            "Small daily goals are easier to maintain over time.",
        "icon": "calendar_month",
    },
    {
        "title": "Add active minutes",
        "description":
            "Short movement breaks can help you reach your goal.",
        "icon": "timer",
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
        "active": False,
    },
    {
        "label": "Profile",
        "icon": "person",
        "active": True,
    },
]


# ==========================================================
# Generate One Goal
# ==========================================================

def generate_goal(
    definition: dict,
    force_complete: bool = False,
) -> dict:

    target = random.choice(
        definition[
            "targets"
        ]
    )

    if force_complete:

        current = random.randint(
            target,
            int(
                target * 1.25
            ),
        )

    else:

        current = random.randint(
            max(
                1,
                int(
                    target * 0.25
                ),
            ),
            int(
                target * 1.05
            ),
        )

    progress = min(
        1.0,
        current / target,
    )

    return {
        "key":
            definition[
                "key"
            ],

        "title":
            definition[
                "title"
            ],

        "icon":
            definition[
                "icon"
            ],

        "unit":
            definition[
                "unit"
            ],

        "current":
            current,

        "target":
            target,

        "current_formatted":
            (
                f"{current:,}"
                if isinstance(
                    current,
                    int,
                )
                else str(
                    current
                )
            ),

        "target_formatted":
            (
                f"{target:,}"
                if isinstance(
                    target,
                    int,
                )
                else str(
                    target
                )
            ),

        "progress":
            progress,

        "completed":
            current >= target,

        "enabled":
            True,
    }


# ==========================================================
# Goal Collection
# ==========================================================

def generate_goals(
    *,
    force_complete: bool = False,
) -> list[dict]:

    selected = random.sample(
        GOAL_TYPES,
        k=random.randint(
            2,
            4,
        ),
    )

    return [
        generate_goal(
            definition,
            force_complete=
                force_complete,
        )
        for definition
        in selected
    ]


# ==========================================================
# Overview
# ==========================================================

def generate_overview_state() -> dict:

    return {
        "goals":
            generate_goals(),

        "message":
            None,

        "description":
            None,

        "saving_progress":
            None,

        "selected_goal":
            None,
    }


# ==========================================================
# Editing
# ==========================================================

def generate_editing_state() -> dict:

    goals = (
        generate_goals()
    )

    selected_goal = random.choice(
        goals
    )

    return {
        "goals":
            goals,

        "message":
            "Edit goal",

        "description":
            (
                "Adjust your target and choose whether "
                "this goal should stay active."
            ),

        "saving_progress":
            None,

        "selected_goal":
            selected_goal,
    }


# ==========================================================
# Completed
# ==========================================================

def generate_completed_state() -> dict:

    return {
        "goals":
            generate_goals(
                force_complete=True
            ),

        "message":
            "Goals completed",

        "description":
            (
                "You've reached your activity targets today."
            ),

        "saving_progress":
            None,

        "selected_goal":
            None,
    }


# ==========================================================
# No Goals
# ==========================================================

def generate_no_goals_state() -> dict:

    return {
        "goals":
            [],

        "message":
            "No goals yet",

        "description":
            (
                "Set an activity, sleep, or movement goal "
                "to start tracking your progress."
            ),

        "saving_progress":
            None,

        "selected_goal":
            None,
    }


# ==========================================================
# Saving
# ==========================================================

def generate_saving_state() -> dict:

    goals = (
        generate_goals()
    )

    return {
        "goals":
            goals,

        "message":
            "Saving your goals",

        "description":
            (
                "Fit is updating your activity targets."
            ),

        "saving_progress":
            random.randint(
                25,
                88,
            ),

        "selected_goal":
            None,
    }


# ==========================================================
# Validation Error
# ==========================================================

def generate_validation_error_state() -> dict:

    goals = (
        generate_goals()
    )

    selected_goal = random.choice(
        goals
    )

    return {
        "goals":
            goals,

        "message":
            "Check your goal",

        "description":
            (
                "Enter a valid target greater than zero."
            ),

        "saving_progress":
            None,

        "selected_goal":
            {
                **selected_goal,
                "target":
                    0,
                "target_formatted":
                    "0",
            },
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_goals_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            GOAL_STATES
        )


    if state not in GOAL_STATES:

        raise ValueError(
            f"Unknown goal state: "
            f"{state}. "
            f"Available states: "
            f"{GOAL_STATES}"
        )


    if state == "overview":

        state_data = (
            generate_overview_state()
        )

    elif state == "editing":

        state_data = (
            generate_editing_state()
        )

    elif state == "completed":

        state_data = (
            generate_completed_state()
        )

    elif state == "no_goals":

        state_data = (
            generate_no_goals_state()
        )

    elif state == "saving":

        state_data = (
            generate_saving_state()
        )

    else:

        state_data = (
            generate_validation_error_state()
        )


    return {
        "state":
            state,

        "title":
            "Goals",

        "suggestions":
            random.sample(
                SUGGESTIONS,
                k=2,
            ),

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

    for state in GOAL_STATES:

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
            generate_goals_data(
                state=state
            )
        )