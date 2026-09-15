from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

CLOCKS_STATES = [

    "world_clocks",

    "world_clock_selected",

    "add_world_clock",

    "alarms",

    "alarm_enabled",

    "alarm_disabled",

    "add_alarm",

    "edit_alarm",

    "alarm_ringing",

    "stopwatch_idle",

    "stopwatch_running",

    "stopwatch_laps",

    "timer_idle",

    "timer_running",

    "timer_paused",

    "timer_finished",
]


# ==========================================================
# Cities
# ==========================================================

WORLD_CITIES = [

    {
        "city": "Seoul",
        "country": "South Korea",
        "offset": 9,
    },

    {
        "city": "Tokyo",
        "country": "Japan",
        "offset": 9,
    },

    {
        "city": "London",
        "country": "United Kingdom",
        "offset": 0,
    },

    {
        "city": "Paris",
        "country": "France",
        "offset": 1,
    },

    {
        "city": "Berlin",
        "country": "Germany",
        "offset": 1,
    },

    {
        "city": "New York",
        "country": "United States",
        "offset": -5,
    },

    {
        "city": "Los Angeles",
        "country": "United States",
        "offset": -8,
    },

    {
        "city": "Sydney",
        "country": "Australia",
        "offset": 10,
    },

    {
        "city": "Singapore",
        "country": "Singapore",
        "offset": 8,
    },

    {
        "city": "Kathmandu",
        "country": "Nepal",
        "offset": 5.75,
    },
]


# ==========================================================
# Alarm Labels
# ==========================================================

ALARM_LABELS = [

    "Wake Up",

    "Morning Class",

    "Gym",

    "Study Time",

    "Meeting",

    "Medication",

    "Project Work",

    "Call Home",

    "Evening Reminder",
]


# ==========================================================
# Helpers
# ==========================================================

def format_offset(
    offset: float,
) -> str:

    sign = "+" if offset >= 0 else "-"

    absolute = abs(
        offset
    )

    hours = int(
        absolute
    )

    minutes = int(
        round(
            (
                absolute
                - hours
            )
            * 60
        )
    )

    return (
        f"UTC{sign}"
        f"{hours:02d}:"
        f"{minutes:02d}"
    )


def generate_world_clock(
    index: int,
) -> dict:

    city = dict(
        random.choice(
            WORLD_CITIES
        )
    )

    now = (
        datetime.utcnow()
        + timedelta(
            hours=city[
                "offset"
            ]
        )
    )

    return {

        "id":
            index,

        "city":
            city[
                "city"
            ],

        "country":
            city[
                "country"
            ],

        "offset":
            city[
                "offset"
            ],

        "offset_text":
            format_offset(
                city[
                    "offset"
                ]
            ),

        "time_text":
            now.strftime(
                "%H:%M"
            ),

        "date_text":
            now.strftime(
                "%a, %b %d"
            ),

        "day_period":
            (
                "Day"
                if 7
                <=
                now.hour
                <
                19
                else
                "Night"
            ),

        "selected":
            False,
    }


def generate_world_clocks() -> list[dict]:

    count = random.randint(
        4,
        7,
    )

    choices = random.sample(
        WORLD_CITIES,
        k=min(
            count,
            len(
                WORLD_CITIES
            ),
        ),
    )

    clocks = []

    for index, city in enumerate(
        choices
    ):

        now = (
            datetime.utcnow()
            + timedelta(
                hours=city[
                    "offset"
                ]
            )
        )

        clocks.append(
            {
                "id":
                    index,

                "city":
                    city[
                        "city"
                    ],

                "country":
                    city[
                        "country"
                    ],

                "offset":
                    city[
                        "offset"
                    ],

                "offset_text":
                    format_offset(
                        city[
                            "offset"
                        ]
                    ),

                "time_text":
                    now.strftime(
                        "%H:%M"
                    ),

                "date_text":
                    now.strftime(
                        "%a, %b %d"
                    ),

                "day_period":
                    (
                        "Day"
                        if 7
                        <=
                        now.hour
                        <
                        19
                        else
                        "Night"
                    ),

                "selected":
                    False,
            }
        )

    return clocks


# ==========================================================
# Alarms
# ==========================================================

def generate_alarm(
    index: int,
) -> dict:

    hour = random.randint(
        5,
        23,
    )

    minute = random.choice(
        [
            0,
            5,
            10,
            15,
            20,
            30,
            45,
            50,
        ]
    )

    days = random.choice(
        [
            "Every day",
            "Weekdays",
            "Weekends",
            "Mon, Wed, Fri",
            "Tomorrow",
        ]
    )

    return {

        "id":
            index,

        "time":
            f"{hour:02d}:{minute:02d}",

        "label":
            random.choice(
                ALARM_LABELS
            ),

        "days":
            days,

        "enabled":
            random.random()
            < 0.70,

        "selected":
            False,
    }


def generate_alarms() -> list[dict]:

    return [

        generate_alarm(
            index
        )

        for index in range(
            random.randint(
                3,
                6,
            )
        )
    ]


# ==========================================================
# Stopwatch
# ==========================================================

def generate_laps() -> list[dict]:

    lap_count = random.randint(
        4,
        9,
    )

    laps = []

    elapsed = 0.0

    for index in range(
        lap_count
    ):

        lap_time = random.uniform(
            24.0,
            92.0,
        )

        elapsed += lap_time

        lap_minutes = int(
            lap_time
            // 60
        )

        lap_seconds = (
            lap_time
            %
            60
        )

        total_minutes = int(
            elapsed
            // 60
        )

        total_seconds = (
            elapsed
            %
            60
        )

        laps.append(
            {
                "number":
                    index + 1,

                "lap_time":
                    (
                        f"{lap_minutes:02d}:"
                        f"{lap_seconds:05.2f}"
                    ),

                "total_time":
                    (
                        f"{total_minutes:02d}:"
                        f"{total_seconds:05.2f}"
                    ),
            }
        )

    return list(
        reversed(
            laps
        )
    )


# ==========================================================
# Timer
# ==========================================================

def generate_timer_values() -> dict:

    total_seconds = random.choice(
        [
            60,
            180,
            300,
            600,
            900,
            1200,
            1800,
            2700,
        ]
    )

    remaining = random.randint(
        10,
        total_seconds,
    )

    progress = int(
        (
            total_seconds
            - remaining
        )
        /
        total_seconds
        *
        100
    )

    return {

        "total_seconds":
            total_seconds,

        "remaining_seconds":
            remaining,

        "progress":
            progress,

        "hours":
            remaining
            // 3600,

        "minutes":
            (
                remaining
                % 3600
            )
            // 60,

        "seconds":
            remaining
            % 60,
    }


# ==========================================================
# Main
# ==========================================================

def generate_clocks_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CLOCKS_STATES
        )


    if state not in CLOCKS_STATES:

        raise ValueError(
            f"Unknown Clocks state: "
            f"{state}"
        )


    # ======================================================
    # Main Tab
    # ======================================================

    if state in {
        "world_clocks",
        "world_clock_selected",
        "add_world_clock",
    }:

        active_tab = "world"

    elif state in {
        "alarms",
        "alarm_enabled",
        "alarm_disabled",
        "add_alarm",
        "edit_alarm",
        "alarm_ringing",
    }:

        active_tab = "alarms"

    elif state in {
        "stopwatch_idle",
        "stopwatch_running",
        "stopwatch_laps",
    }:

        active_tab = "stopwatch"

    else:

        active_tab = "timer"


    # ======================================================
    # World Clocks
    # ======================================================

    world_clocks = (
        generate_world_clocks()
    )

    selected_clock = None

    if state == "world_clock_selected":

        selected_clock = random.choice(
            world_clocks
        )

        selected_clock[
            "selected"
        ] = True


    # ======================================================
    # Alarms
    # ======================================================

    alarms = (
        generate_alarms()
    )

    selected_alarm = None

    if state in {
        "alarm_enabled",
        "alarm_disabled",
        "edit_alarm",
        "alarm_ringing",
    }:

        selected_alarm = random.choice(
            alarms
        )

        selected_alarm[
            "selected"
        ] = True


    if state == "alarm_enabled":

        selected_alarm[
            "enabled"
        ] = True


    if state == "alarm_disabled":

        selected_alarm[
            "enabled"
        ] = False


    if state == "alarm_ringing":

        selected_alarm[
            "enabled"
        ] = True


    # ======================================================
    # Alarm Form
    # ======================================================

    if (
        state
        == "edit_alarm"
        and
        selected_alarm
    ):

        alarm_form = {

            "time":
                selected_alarm[
                    "time"
                ],

            "label":
                selected_alarm[
                    "label"
                ],

            "days":
                selected_alarm[
                    "days"
                ],

            "enabled":
                selected_alarm[
                    "enabled"
                ],
        }

    else:

        hour = random.randint(
            5,
            23,
        )

        minute = random.choice(
            [
                0,
                15,
                30,
                45,
            ]
        )

        alarm_form = {

            "time":
                f"{hour:02d}:{minute:02d}",

            "label":
                random.choice(
                    ALARM_LABELS
                ),

            "days":
                random.choice(
                    [
                        "Every day",
                        "Weekdays",
                        "Tomorrow",
                    ]
                ),

            "enabled":
                True,
        }


    # ======================================================
    # Stopwatch
    # ======================================================

    stopwatch_minutes = random.randint(
        0,
        12,
    )

    stopwatch_seconds = random.randint(
        0,
        59,
    )

    stopwatch_centiseconds = random.randint(
        0,
        99,
    )


    # ======================================================
    # Timer
    # ======================================================

    timer = generate_timer_values()


    if state == "timer_finished":

        timer[
            "remaining_seconds"
        ] = 0

        timer[
            "hours"
        ] = 0

        timer[
            "minutes"
        ] = 0

        timer[
            "seconds"
        ] = 0

        timer[
            "progress"
        ] = 100


    # ======================================================
    # Add World Clock Search
    # ======================================================

    location_query = ""

    location_results = []

    if state == "add_world_clock":

        city = random.choice(
            WORLD_CITIES
        )

        location_query = (
            city[
                "city"
            ][
                :random.randint(
                    2,
                    max(
                        2,
                        len(
                            city[
                                "city"
                            ]
                        )
                    ),
                )
            ]
        )

        location_results = random.sample(
            WORLD_CITIES,
            k=min(
                5,
                len(
                    WORLD_CITIES
                ),
            ),
        )


    return {

        "state":
            state,

        "active_tab":
            active_tab,

        "world_clocks":
            world_clocks,

        "selected_clock":
            selected_clock,

        "location_query":
            location_query,

        "location_results":
            location_results,

        "alarms":
            alarms,

        "selected_alarm":
            selected_alarm,

        "alarm_form":
            alarm_form,

        "laps":
            generate_laps(),

        "stopwatch_minutes":
            stopwatch_minutes,

        "stopwatch_seconds":
            stopwatch_seconds,

        "stopwatch_centiseconds":
            stopwatch_centiseconds,

        "timer":
            timer,

        "timer_running":
            state
            == "timer_running",

        "timer_paused":
            state
            == "timer_paused",

        "timer_finished":
            state
            == "timer_finished",
    }