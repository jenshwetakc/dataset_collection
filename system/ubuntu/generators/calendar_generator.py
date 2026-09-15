from __future__ import annotations

import calendar
import random

from datetime import (
    date,
    datetime,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

CALENDAR_STATES = [

    "month_view",

    "week_view",

    "day_view",

    "event_selected",

    "create_event",

    "edit_event",

    "reminder_menu",

    "calendar_menu",

    "search_open",

    "search_results",

    "overlapping_events",

    "all_day_events",

    "delete_event_dialog",
]


# ==========================================================
# Event Titles
# ==========================================================

EVENT_TITLES = [

    "Team Meeting",

    "Research Discussion",

    "Project Review",

    "Lunch with Alex",

    "Doctor Appointment",

    "Focus Time",

    "Weekly Planning",

    "Design Review",

    "Presentation",

    "Study Session",

    "Code Review",

    "Office Hours",

    "Client Call",

    "Gym",

    "Dinner",

    "Conference",

    "Workshop",
]


# ==========================================================
# Calendar Colors
# ==========================================================

CALENDARS = [

    {
        "name":
            "Personal",

        "color":
            "#3584E4",
    },

    {
        "name":
            "Work",

        "color":
            "#E95420",
    },

    {
        "name":
            "University",

        "color":
            "#9141AC",
    },

    {
        "name":
            "Birthdays",

        "color":
            "#2EC27E",
    },
]


# ==========================================================
# Reminder Options
# ==========================================================

REMINDER_OPTIONS = [

    "At event time",

    "5 minutes before",

    "10 minutes before",

    "30 minutes before",

    "1 hour before",

    "1 day before",
]


# ==========================================================
# Helpers
# ==========================================================

def random_time() -> tuple[int, int]:

    hour = random.randint(
        8,
        18,
    )

    minute = random.choice(
        [
            0,
            15,
            30,
            45,
        ]
    )

    return hour, minute


def generate_event(
    index: int,
    base_date: date,
) -> dict:

    offset = random.randint(
        -10,
        20,
    )

    event_date = (
        base_date
        + timedelta(
            days=offset
        )
    )


    hour, minute = random_time()


    duration = random.choice(
        [
            30,
            45,
            60,
            90,
            120,
        ]
    )


    start_dt = datetime.combine(
        event_date,
        datetime.min.time(),
    ).replace(
        hour=hour,
        minute=minute,
    )


    end_dt = (
        start_dt
        + timedelta(
            minutes=duration
        )
    )


    cal = random.choice(
        CALENDARS
    )


    all_day = (
        random.random()
        < 0.12
    )


    return {

        "id":
            index,

        "title":
            random.choice(
                EVENT_TITLES
            ),

        "date":
            event_date,

        "date_text":
            event_date.strftime(
                "%Y-%m-%d"
            ),

        "start":
            start_dt,

        "end":
            end_dt,

        "start_text":
            (
                "All day"
                if all_day
                else start_dt.strftime(
                    "%H:%M"
                )
            ),

        "end_text":
            (
                ""
                if all_day
                else end_dt.strftime(
                    "%H:%M"
                )
            ),

        "all_day":
            all_day,

        "calendar":
            cal[
                "name"
            ],

        "color":
            cal[
                "color"
            ],

        "location":
            random.choice(
                [
                    "",
                    "Room 301",
                    "Online",
                    "Conference Room",
                    "Library",
                    "Office",
                ]
            ),

        "description":
            fake.sentence(
                nb_words=random.randint(
                    6,
                    14,
                )
            ),

        "selected":
            False,
    }


def generate_events(
    base_date: date,
    count: int = 18,
) -> list[dict]:

    return [

        generate_event(
            index,
            base_date,
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Month Grid
# ==========================================================

def generate_month_days(
    year: int,
    month: int,
) -> list[dict]:

    first_weekday, days_in_month = (
        calendar.monthrange(
            year,
            month,
        )
    )


    previous_month = (
        month - 1
        if month > 1
        else 12
    )

    previous_year = (
        year
        if month > 1
        else year - 1
    )


    previous_days = (
        calendar.monthrange(
            previous_year,
            previous_month,
        )[1]
    )


    cells = []


    for offset in range(
        first_weekday
    ):

        day_number = (
            previous_days
            - first_weekday
            + offset
            + 1
        )

        cells.append(
            {
                "day":
                    day_number,

                "current_month":
                    False,

                "date":
                    None,
            }
        )


    for day_number in range(
        1,
        days_in_month + 1,
    ):

        current_date = date(
            year,
            month,
            day_number,
        )

        cells.append(
            {
                "day":
                    day_number,

                "current_month":
                    True,

                "date":
                    current_date,

                "date_text":
                    current_date.strftime(
                        "%Y-%m-%d"
                    ),
            }
        )


    next_day = 1

    while len(
        cells
    ) < 42:

        cells.append(
            {
                "day":
                    next_day,

                "current_month":
                    False,

                "date":
                    None,
            }
        )

        next_day += 1


    return cells


# ==========================================================
# Main Generator
# ==========================================================

def generate_calendar_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CALENDAR_STATES
        )


    if state not in CALENDAR_STATES:

        raise ValueError(
            f"Unknown calendar state: "
            f"{state}"
        )


    today = date.today()


    year = today.year

    month = today.month


    events = generate_events(
        base_date=today,
        count=random.randint(
            14,
            24,
        ),
    )


    # ======================================================
    # Overlap State
    # ======================================================

    if state == "overlapping_events":

        overlap_date = today

        for index in range(
            min(
                4,
                len(
                    events
                ),
            )
        ):

            start_dt = datetime.combine(
                overlap_date,
                datetime.min.time(),
            ).replace(
                hour=10,
                minute=index * 15,
            )

            events[
                index
            ][
                "date"
            ] = overlap_date

            events[
                index
            ][
                "date_text"
            ] = overlap_date.strftime(
                "%Y-%m-%d"
            )

            events[
                index
            ][
                "start"
            ] = start_dt

            events[
                index
            ][
                "start_text"
            ] = start_dt.strftime(
                "%H:%M"
            )


    # ======================================================
    # All Day State
    # ======================================================

    if state == "all_day_events":

        for index in range(
            min(
                5,
                len(
                    events
                ),
            )
        ):

            events[
                index
            ][
                "date"
            ] = today

            events[
                index
            ][
                "date_text"
            ] = today.strftime(
                "%Y-%m-%d"
            )

            events[
                index
            ][
                "all_day"
            ] = True

            events[
                index
            ][
                "start_text"
            ] = "All day"

            events[
                index
            ][
                "end_text"
            ] = ""


    # ======================================================
    # Selected Event
    # ======================================================

    selected_event = None


    if state in {
        "event_selected",
        "edit_event",
        "reminder_menu",
        "delete_event_dialog",
    }:

        selected_event = random.choice(
            events
        )

        selected_event[
            "selected"
        ] = True


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    search_results = []


    if state in {
        "search_open",
        "search_results",
    }:

        search_query = random.choice(
            [
                "meeting",
                "project",
                "review",
                "study",
                "call",
            ]
        )


    if state == "search_results":

        search_results = random.sample(

            events,

            k=min(
                random.randint(
                    4,
                    8,
                ),
                len(
                    events
                ),
            ),
        )


    # ======================================================
    # Create/Edit Form
    # ======================================================

    form_event = {

        "title":
            random.choice(
                EVENT_TITLES
            ),

        "date_text":
            today.strftime(
                "%Y-%m-%d"
            ),

        "start_text":
            "10:00",

        "end_text":
            "11:00",

        "location":
            "Meeting Room",

        "calendar":
            random.choice(
                CALENDARS
            )[
                "name"
            ],

        "description":
            fake.sentence(
                nb_words=10
            ),
    }


    if state == "edit_event" and selected_event:

        form_event = {

            "title":
                selected_event[
                    "title"
                ],

            "date_text":
                selected_event[
                    "date_text"
                ],

            "start_text":
                selected_event[
                    "start_text"
                ],

            "end_text":
                selected_event[
                    "end_text"
                ],

            "location":
                selected_event[
                    "location"
                ],

            "calendar":
                selected_event[
                    "calendar"
                ],

            "description":
                selected_event[
                    "description"
                ],
        }


    # ======================================================
    # View Mode
    # ======================================================

    if state in {
        "week_view",
        "overlapping_events",
        "all_day_events",
    }:

        view_mode = "week"

    elif state == "day_view":

        view_mode = "day"

    else:

        view_mode = "month"


    # ======================================================
    # Week Dates
    # ======================================================

    week_start = (
        today
        - timedelta(
            days=today.weekday()
        )
    )


    week_days = [

        {
            "date":
                week_start
                + timedelta(
                    days=index
                ),

            "label":
                (
                    week_start
                    + timedelta(
                        days=index
                    )
                ).strftime(
                    "%a"
                ),

            "day":
                (
                    week_start
                    + timedelta(
                        days=index
                    )
                ).day,

            "date_text":
                (
                    week_start
                    + timedelta(
                        days=index
                    )
                ).strftime(
                    "%Y-%m-%d"
                ),
        }

        for index
        in range(
            7
        )
    ]


    return {

        "state":
            state,

        "view_mode":
            view_mode,

        "today":
            today,

        "today_text":
            today.strftime(
                "%Y-%m-%d"
            ),

        "month_title":
            today.strftime(
                "%B %Y"
            ),

        "month_days":
            generate_month_days(
                year,
                month,
            ),

        "week_days":
            week_days,

        "events":
            events,

        "selected_event":
            selected_event,

        "search_query":
            search_query,

        "search_results":
            search_results,

        "form_event":
            form_event,

        "calendars":
            [
                dict(
                    entry
                )
                for entry
                in CALENDARS
            ],

        "reminder_options":
            REMINDER_OPTIONS.copy(),

        "selected_reminder":
            random.choice(
                REMINDER_OPTIONS
            ),
    }