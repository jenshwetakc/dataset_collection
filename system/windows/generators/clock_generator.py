from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

CLOCK_STATES = [
    "clock_home",
    "alarms",
    "alarm_enabled",
    "alarm_disabled",
    "timer_setup",
    "timer_running",
    "stopwatch_idle",
    "stopwatch_running",
    "focus_session",
    "world_clock",
    "add_alarm_dialog",
    "add_timer_dialog",
]


# ==========================================================
# Navigation
# ==========================================================

CLOCK_NAVIGATION = [
    {
        "id": "focus_session",
        "label": "Focus sessions",
        "icon": "center_focus_strong",
    },
    {
        "id": "timer",
        "label": "Timer",
        "icon": "timer",
    },
    {
        "id": "alarms",
        "label": "Alarm",
        "icon": "alarm",
    },
    {
        "id": "stopwatch",
        "label": "Stopwatch",
        "icon": "speed",
    },
    {
        "id": "world_clock",
        "label": "World clock",
        "icon": "public",
    },
]


# ==========================================================
# Alarm Pool
# ==========================================================

ALARM_LABELS = [
    "Wake up",
    "Morning meeting",
    "Research session",
    "Gym",
    "Class",
    "Reminder",
]


ALARM_SOUNDS = [
    "Chimes",
    "Morning",
    "Digital",
    "Echo",
]


# ==========================================================
# World Clock
# ==========================================================

CITY_POOL = [
    {
        "city": "Seoul",
        "country": "South Korea",
        "offset": "+0h",
    },
    {
        "city": "Tokyo",
        "country": "Japan",
        "offset": "+0h",
    },
    {
        "city": "London",
        "country": "United Kingdom",
        "offset": "-8h",
    },
    {
        "city": "New York",
        "country": "United States",
        "offset": "-13h",
    },
    {
        "city": "San Francisco",
        "country": "United States",
        "offset": "-16h",
    },
    {
        "city": "Sydney",
        "country": "Australia",
        "offset": "+1h",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_alarms() -> list[dict]:

    result = []

    for index in range(
        random.randint(
            3,
            6,
        )
    ):

        hour = random.randint(
            5,
            22,
        )

        minute = random.choice(
            [
                0,
                10,
                15,
                20,
                30,
                45,
                50,
            ]
        )

        result.append(
            {
                "id":
                    f"alarm_{index}",

                "hour":
                    hour,

                "minute":
                    minute,

                "time":
                    f"{hour:02d}:{minute:02d}",

                "label":
                    random.choice(
                        ALARM_LABELS
                    ),

                "enabled":
                    random.random()
                    < 0.70,

                "repeat":
                    random.choice(
                        [
                            "Every day",
                            "Weekdays",
                            "Mon, Wed, Fri",
                            "Once",
                        ]
                    ),

                "sound":
                    random.choice(
                        ALARM_SOUNDS
                    ),
            }
        )

    return result


def generate_timers() -> list[dict]:

    result = []

    for index in range(
        random.randint(
            2,
            4,
        )
    ):

        total_seconds = random.choice(
            [
                60,
                300,
                600,
                900,
                1500,
                1800,
                3600,
            ]
        )

        result.append(
            {
                "id":
                    f"timer_{index}",

                "label":
                    random.choice(
                        [
                            "Tea",
                            "Break",
                            "Focus",
                            "Exercise",
                            "Reading",
                        ]
                    ),

                "total_seconds":
                    total_seconds,

                "hours":
                    total_seconds
                    // 3600,

                "minutes":
                    (
                        total_seconds
                        % 3600
                    )
                    // 60,

                "seconds":
                    total_seconds
                    % 60,
            }
        )

    return result


def generate_world_clocks() -> list[dict]:

    count = random.randint(
        3,
        min(
            5,
            len(
                CITY_POOL
            ),
        ),
    )

    selected = random.sample(
        CITY_POOL,
        k=count,
    )

    result = []

    for city in selected:

        hour = random.randint(
            0,
            23,
        )

        minute = random.randint(
            0,
            59,
        )

        result.append(
            {
                **city,

                "time":
                    f"{hour:02d}:{minute:02d}",

                "day":
                    random.choice(
                        [
                            "Today",
                            "Yesterday",
                            "Tomorrow",
                        ]
                    ),
            }
        )

    return result


def generate_laps() -> list[dict]:

    count = random.randint(
        2,
        6,
    )

    laps = []

    elapsed = 0.0

    for index in range(
        count
    ):

        lap_time = round(
            random.uniform(
                20,
                95,
            ),
            2,
        )

        elapsed += lap_time

        laps.append(
            {
                "lap":
                    index + 1,

                "lap_time":
                    f"{lap_time:.2f}s",

                "total":
                    f"{elapsed:.2f}s",
            }
        )

    return laps


# ==========================================================
# Main Generator
# ==========================================================

def generate_clock_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CLOCK_STATES
        )


    if state not in CLOCK_STATES:

        raise ValueError(
            f"Unknown Clock state: {state}"
        )


    alarms = generate_alarms()


    if state == "alarm_enabled":

        alarms[0][
            "enabled"
        ] = True


    if state == "alarm_disabled":

        alarms[0][
            "enabled"
        ] = False


    active_nav = (
        "focus_session"
    )


    if state in {
        "alarms",
        "alarm_enabled",
        "alarm_disabled",
        "add_alarm_dialog",
    }:

        active_nav = (
            "alarms"
        )


    elif state in {
        "timer_setup",
        "timer_running",
        "add_timer_dialog",
    }:

        active_nav = (
            "timer"
        )


    elif state in {
        "stopwatch_idle",
        "stopwatch_running",
    }:

        active_nav = (
            "stopwatch"
        )


    elif state == "world_clock":

        active_nav = (
            "world_clock"
        )


    focus_minutes = random.choice(
        [
            15,
            25,
            30,
            45,
            60,
        ]
    )


    timer_total = random.choice(
        [
            300,
            600,
            900,
            1500,
        ]
    )


    timer_remaining = (
        random.randint(
            30,
            timer_total - 1,
        )
        if state
        == "timer_running"
        else timer_total
    )


    return {
        "state":
            state,

        "active_nav":
            active_nav,

        "navigation":
            CLOCK_NAVIGATION,

        "alarms":
            alarms,

        "timers":
            generate_timers(),

        "world_clocks":
            generate_world_clocks(),

        "timer_running": {
            "total":
                timer_total,

            "remaining":
                timer_remaining,

            "minutes":
                timer_remaining
                // 60,

            "seconds":
                timer_remaining
                % 60,

            "progress":
                round(
                    (
                        1
                        -
                        timer_remaining
                        /
                        timer_total
                    )
                    *
                    100
                ),
        },

        "stopwatch": {
            "elapsed":
                random.choice(
                    [
                        "00:00.00",
                        "00:42.18",
                        "01:18.54",
                        "03:26.91",
                    ]
                ),

            "laps":
                (
                    generate_laps()
                    if state
                    == "stopwatch_running"
                    else []
                ),
        },

        "focus": {
            "minutes":
                focus_minutes,

            "completed":
                random.randint(
                    0,
                    4,
                ),

            "daily_goal":
                random.choice(
                    [
                        3,
                        4,
                        5,
                    ]
                ),

            "progress":
                random.randint(
                    12,
                    85,
                ),

            "task":
                random.choice(
                    [
                        "Review research notes",
                        "Prepare slides",
                        "Read paper",
                        "Inspect dataset",
                    ]
                ),
        },

        "new_alarm": {
            "time":
                random.choice(
                    [
                        "07:30",
                        "08:00",
                        "09:15",
                        "18:00",
                    ]
                ),

            "label":
                random.choice(
                    ALARM_LABELS
                ),

            "repeat":
                random.choice(
                    [
                        "Every day",
                        "Weekdays",
                        "Once",
                    ]
                ),

            "sound":
                random.choice(
                    ALARM_SOUNDS
                ),
        },

        "new_timer": {
            "hours":
                random.randint(
                    0,
                    2,
                ),

            "minutes":
                random.choice(
                    [
                        5,
                        10,
                        15,
                        25,
                        30,
                        45,
                    ]
                ),

            "seconds":
                random.choice(
                    [
                        0,
                        15,
                        30,
                        45,
                    ]
                ),

            "label":
                random.choice(
                    [
                        "New timer",
                        "Focus",
                        "Break",
                        "Exercise",
                    ]
                ),
        },
    }