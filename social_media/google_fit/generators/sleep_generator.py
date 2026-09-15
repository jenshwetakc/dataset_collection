from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# States
# ==========================================================

SLEEP_STATES = [
    "recorded",
    "no_data",
    "permission_required",
    "syncing",
    "irregular_sleep",
    "goal_achieved",
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

def format_minutes(
    total_minutes: int,
) -> str:

    hours = (
        total_minutes
        // 60
    )

    minutes = (
        total_minutes
        % 60
    )

    return (
        f"{hours}h "
        f"{minutes:02d}m"
    )


def random_time(
    hour_start: int,
    hour_end: int,
) -> str:

    hour = random.randint(
        hour_start,
        hour_end,
    )

    minute = random.choice(
        [
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
        ]
    )

    return (
        f"{hour:02d}:"
        f"{minute:02d}"
    )


# ==========================================================
# Sleep Stages
# ==========================================================

def generate_sleep_stages(
    total_minutes: int,
) -> list[dict]:

    awake = random.randint(
        10,
        35,
    )

    rem = int(
        total_minutes
        * random.uniform(
            0.18,
            0.24,
        )
    )

    deep = int(
        total_minutes
        * random.uniform(
            0.15,
            0.22,
        )
    )

    light = max(
        0,
        total_minutes
        - awake
        - rem
        - deep,
    )

    stages = [
        {
            "key": "awake",
            "label": "Awake",
            "minutes": awake,
            "value": format_minutes(
                awake
            ),
            "percent":
                round(
                    awake
                    / total_minutes
                    * 100
                ),
        },
        {
            "key": "rem",
            "label": "REM",
            "minutes": rem,
            "value": format_minutes(
                rem
            ),
            "percent":
                round(
                    rem
                    / total_minutes
                    * 100
                ),
        },
        {
            "key": "light",
            "label": "Light",
            "minutes": light,
            "value": format_minutes(
                light
            ),
            "percent":
                round(
                    light
                    / total_minutes
                    * 100
                ),
        },
        {
            "key": "deep",
            "label": "Deep",
            "minutes": deep,
            "value": format_minutes(
                deep
            ),
            "percent":
                round(
                    deep
                    / total_minutes
                    * 100
                ),
        },
    ]

    return stages


# ==========================================================
# Timeline
# ==========================================================

def generate_timeline(
    stages: list[dict],
) -> list[dict]:

    timeline = []

    stage_lookup = [
        "light",
        "deep",
        "light",
        "rem",
        "light",
        "awake",
        "light",
        "deep",
        "light",
        "rem",
    ]

    count = random.randint(
        10,
        16,
    )

    for index in range(
        count
    ):

        key = random.choice(
            stage_lookup
        )

        timeline.append(
            {
                "key":
                    key,

                "width":
                    random.randint(
                        6,
                        18,
                    ),
            }
        )

    return timeline


# ==========================================================
# Weekly Data
# ==========================================================

def generate_weekly_sleep() -> list[dict]:

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

        minutes = random.randint(
            330,
            530,
        )

        result.append(
            {
                "day":
                    date.strftime(
                        "%a"
                    )[0],

                "date":
                    date.strftime(
                        "%b %d"
                    ),

                "minutes":
                    minutes,

                "value":
                    format_minutes(
                        minutes
                    ),

                "height":
                    random.randint(
                        45,
                        100,
                    ),
            }
        )

    return result


# ==========================================================
# Recorded
# ==========================================================

def generate_recorded_state(
    goal_achieved: bool = False,
    irregular: bool = False,
) -> dict:

    if goal_achieved:

        total_minutes = random.randint(
            480,
            560,
        )

    elif irregular:

        total_minutes = random.randint(
            260,
            390,
        )

    else:

        total_minutes = random.randint(
            390,
            500,
        )

    stages = (
        generate_sleep_stages(
            total_minutes
        )
    )

    score = (
        random.randint(
            88,
            98,
        )
        if goal_achieved
        else random.randint(
            60,
            89,
        )
    )

    if irregular:

        score = random.randint(
            45,
            67,
        )

    bedtime = random_time(
        21,
        23,
    )

    wake_time = random_time(
        5,
        8,
    )

    if irregular:

        bedtime = random.choice(
            [
                "00:45",
                "01:10",
                "02:20",
            ]
        )

        wake_time = random.choice(
            [
                "05:20",
                "06:10",
                "07:05",
            ]
        )

    return {

        "total_minutes":
            total_minutes,

        "duration":
            format_minutes(
                total_minutes
            ),

        "score":
            score,

        "bedtime":
            bedtime,

        "wake_time":
            wake_time,

        "goal":
            "8h 00m",

        "goal_progress":
            min(
                1.0,
                total_minutes / 480,
            ),

        "stages":
            stages,

        "timeline":
            generate_timeline(
                stages
            ),

        "weekly":
            generate_weekly_sleep(),

        "insight":
            (
                {
                    "icon":
                        "check_circle",

                    "title":
                        "Sleep goal reached",

                    "description":
                        "You met your nightly sleep goal.",
                }
                if goal_achieved
                else (
                    {
                        "icon":
                            "schedule",

                        "title":
                            "Your schedule varied",

                        "description":
                            "Your bedtime was later than your recent average.",
                    }
                    if irregular
                    else {
                        "icon":
                            "bedtime",

                        "title":
                            "Good sleep consistency",

                        "description":
                            "Your sleep duration is close to your recent average.",
                    }
                )
            ),
    }


# ==========================================================
# No Data
# ==========================================================

def generate_no_data_state() -> dict:

    return {

        "message":
            "No sleep data was recorded for last night.",

        "description":
            (
                "Wear a connected device or add your sleep "
                "manually to start tracking your sleep history."
            ),
    }


# ==========================================================
# Permission
# ==========================================================

def generate_permission_state() -> dict:

    return {

        "message":
            "Allow sleep access",

        "description":
            (
                "Fit needs permission to read sleep information "
                "from connected health services."
            ),
    }


# ==========================================================
# Sync
# ==========================================================

def generate_sync_state() -> dict:

    return {

        "message":
            "Syncing sleep data",

        "description":
            (
                "Fit is checking connected devices for your "
                "latest sleep session."
            ),

        "progress":
            random.randint(
                25,
                85,
            ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_sleep_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SLEEP_STATES
        )

    if state not in SLEEP_STATES:

        raise ValueError(
            f"Unknown sleep state: "
            f"{state}. "
            f"Available states: "
            f"{SLEEP_STATES}"
        )


    result = {

        "state":
            state,

        "title":
            "Sleep",

        "navigation_items": [
            dict(
                item
            )
            for item
            in NAVIGATION_ITEMS
        ],
    }


    if state == "recorded":

        result.update(
            generate_recorded_state()
        )


    elif state == "goal_achieved":

        result.update(
            generate_recorded_state(
                goal_achieved=True
            )
        )


    elif state == "irregular_sleep":

        result.update(
            generate_recorded_state(
                irregular=True
            )
        )


    elif state == "no_data":

        result.update(
            generate_no_data_state()
        )


    elif state == "permission_required":

        result.update(
            generate_permission_state()
        )


    elif state == "syncing":

        result.update(
            generate_sync_state()
        )


    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in SLEEP_STATES:

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
            generate_sleep_data(
                state=state
            )
        )