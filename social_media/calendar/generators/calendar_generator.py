from __future__ import annotations

import calendar as calendar_module
import random

from datetime import (
    date,
    datetime,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# Calendar States
# ==========================================================

CALENDAR_STATES = [
    "month_view",
    "week_view",
    "day_view",
    "agenda_view",
    "search_results",
    "overlapping_events",
    "empty_schedule",
    "event_details_dialog",
    "create_event_dialog",
    "edit_event_dialog",
    "mobile_event_sheet",
]


# ==========================================================
# Static Data
# ==========================================================

EVENT_TITLES = [
    "Team stand-up",
    "Project review",
    "Design critique",
    "Research meeting",
    "Lunch with Alex",
    "Focus time",
    "Client call",
    "Release planning",
    "Weekly sync",
    "Doctor appointment",
    "Conference session",
    "Interview",
    "Gym session",
    "Study group",
]

EVENT_LOCATIONS = [
    "Conference Room A",
    "Research Lab",
    "Main Office",
    "Video call",
    "Campus Library",
    "Design Studio",
    "",
]

EVENT_COLORS = [
    "blue",
    "green",
    "purple",
    "orange",
    "red",
    "teal",
]


# ==========================================================
# Event Generator
# ==========================================================

def generate_event(
    event_date: date,
    index: int,
    overlapping: bool = False,
) -> dict:

    if overlapping:
        start_hour = random.choice(
            [
                9,
                10,
                10,
                11,
            ]
        )
    else:
        start_hour = random.randint(
            8,
            18,
        )

    start_minute = random.choice(
        [
            0,
            0,
            15,
            30,
            45,
        ]
    )

    duration = random.choice(
        [
            30,
            45,
            60,
            90,
            120,
        ]
    )

    start_datetime = (
        datetime.combine(
            event_date,
            datetime.min.time(),
        )
        .replace(
            hour=start_hour,
            minute=start_minute,
        )
    )

    end_datetime = (
        start_datetime
        + timedelta(
            minutes=duration,
        )
    )

    attendees = []

    for attendee_index in range(
        random.randint(
            1,
            5,
        )
    ):

        attendee_name = fake.name()

        initials = "".join(
            name_part[0].upper()
            for name_part in attendee_name.split()[:2]
        )

        attendees.append(
            {
                "id":
                    attendee_index,

                "name":
                    attendee_name,

                "initials":
                    initials,
            }
        )

    return {
        "id":
            (
                f"event_"
                f"{event_date:%Y%m%d}_"
                f"{index}"
            ),

        "title":
            random.choice(
                EVENT_TITLES
            ),

        "date":
            event_date.isoformat(),

        "day_number":
            event_date.day,

        "start_hour":
            start_datetime.hour,

        "start":
            start_datetime.strftime(
                "%H:%M"
            ),

        "end":
            end_datetime.strftime(
                "%H:%M"
            ),

        "time_text":
            (
                f"{start_datetime.strftime('%I:%M %p').lstrip('0')}"
                f" – "
                f"{end_datetime.strftime('%I:%M %p').lstrip('0')}"
            ),

        "color":
            random.choice(
                EVENT_COLORS
            ),

        "location":
            random.choice(
                EVENT_LOCATIONS
            ),

        "description":
            fake.sentence(
                nb_words=random.randint(
                    8,
                    18,
                )
            ),

        "attendees":
            attendees,

        "attendee_count":
            len(attendees),

        "all_day":
            False,

        "has_video_call":
            random.random() < 0.45,

        "reminder":
            random.choice(
                [
                    "10 minutes before",
                    "30 minutes before",
                    "1 hour before",
                    "None",
                ]
            ),
    }


# ==========================================================
# Events
# ==========================================================

def generate_events(
    anchor_date: date,
    count: int,
    overlapping: bool = False,
) -> list[dict]:

    events = []

    for index in range(
        count
    ):

        if overlapping:

            event_date = anchor_date

        else:

            event_date = (
                anchor_date
                + timedelta(
                    days=random.randint(
                        0,
                        40,
                    )
                )
            )

        events.append(
            generate_event(
                event_date=event_date,
                index=index,
                overlapping=overlapping,
            )
        )

    return events


# ==========================================================
# Month Grid
# ==========================================================

def generate_month_days(
    anchor_date: date,
    events: list[dict],
) -> list[dict]:

    calendar = calendar_module.Calendar(
        firstweekday=0
    )

    event_lookup = {}

    for event in events:

        event_lookup.setdefault(
            event["date"],
            [],
        ).append(
            event
        )

    month_days = []

    for current_date in calendar.itermonthdates(
        anchor_date.year,
        anchor_date.month,
    ):

        date_key = (
            current_date.isoformat()
        )

        date_events = event_lookup.get(
            date_key,
            [],
        )

        month_days.append(
            {
                "date":
                    date_key,

                "number":
                    current_date.day,

                "in_current_month":
                    (
                        current_date.month
                        == anchor_date.month
                    ),

                "is_today":
                    (
                        current_date
                        == date.today()
                    ),

                "is_weekend":
                    (
                        current_date.weekday()
                        >= 5
                    ),

                "events":
                    date_events[:4],

                "hidden_event_count":
                    max(
                        0,
                        len(date_events) - 4,
                    ),
            }
        )

    return month_days


# ==========================================================
# Week Grid
# ==========================================================

def generate_week_days(
    selected_date: date,
    events: list[dict],
) -> list[dict]:

    week_start = (
        selected_date
        - timedelta(
            days=selected_date.weekday()
        )
    )

    week_days = []

    for offset in range(
        7
    ):

        current_date = (
            week_start
            + timedelta(
                days=offset
            )
        )

        date_key = (
            current_date.isoformat()
        )

        week_days.append(
            {
                "date":
                    date_key,

                "name":
                    current_date.strftime(
                        "%a"
                    ),

                "number":
                    current_date.day,

                "is_today":
                    (
                        current_date
                        == date.today()
                    ),

                "events": [
                    event
                    for event in events
                    if event["date"] == date_key
                ],
            }
        )

    return week_days


# ==========================================================
# Agenda
# ==========================================================

def generate_agenda_days(
    selected_date: date,
    events: list[dict],
) -> list[dict]:

    agenda_days = []

    for offset in range(
        21
    ):

        current_date = (
            selected_date
            + timedelta(
                days=offset
            )
        )

        date_key = (
            current_date.isoformat()
        )

        day_events = [
            event
            for event in events
            if event["date"] == date_key
        ]

        if not day_events:
            continue

        agenda_days.append(
            {
                "date":
                    date_key,

                "day_name":
                    current_date.strftime(
                        "%A"
                    ),

                "date_text":
                    current_date.strftime(
                        "%B %d"
                    ),

                "is_today":
                    (
                        current_date
                        == date.today()
                    ),

                "events":
                    sorted(
                        day_events,
                        key=lambda value:
                            value["start"],
                    ),
            }
        )

    return agenda_days


# ==========================================================
# Mini Calendar
# ==========================================================

def generate_mini_calendar(
    anchor_date: date,
) -> list[dict]:

    calendar = calendar_module.Calendar(
        firstweekday=0
    )

    return [
        {
            "number":
                current_date.day,

            "date":
                current_date.isoformat(),

            "in_current_month":
                (
                    current_date.month
                    == anchor_date.month
                ),

            "is_today":
                (
                    current_date
                    == date.today()
                ),
        }
        for current_date
        in calendar.itermonthdates(
            anchor_date.year,
            anchor_date.month,
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_calendar_data(
    state: str | None = None,
    seed: int | None = None,
    viewport: dict | None = None,
) -> dict:

    if seed is not None:

        random.seed(
            seed
        )

        Faker.seed(
            seed
        )

    if state is None:

        state = random.choice(
            CALENDAR_STATES
        )

    if state not in CALENDAR_STATES:

        raise ValueError(
            f"Unknown Calendar state: {state}. "
            f"Available states: {CALENDAR_STATES}"
        )

    today = date.today()

    selected_date = (
        today
        + timedelta(
            days=random.randint(
                -7,
                7,
            )
        )
    )

    month_anchor = (
        selected_date.replace(
            day=1
        )
    )

    if state == "empty_schedule":

        events = []

    elif state == "overlapping_events":

        events = generate_events(
            anchor_date=selected_date,
            count=random.randint(
                7,
                11,
            ),
            overlapping=True,
        )

    else:

        events = generate_events(
            anchor_date=month_anchor,
            count=random.randint(
                22,
                38,
            ),
        )

    selected_event = (
        random.choice(events)
        if events
        else None
    )

    popup_states = {
        "event_details_dialog",
        "create_event_dialog",
        "edit_event_dialog",
        "mobile_event_sheet",
    }

    if state in {
        "week_view",
        "overlapping_events",
    }:

        current_view = "week"

    elif state == "day_view":

        current_view = "day"

    elif state in {
        "agenda_view",
        "search_results",
        "empty_schedule",
    }:

        current_view = "agenda"

    else:

        current_view = "month"

    search_query = (
        "meeting"
        if state == "search_results"
        else ""
    )

    search_results = [
        event
        for event in events
        if any(
            keyword in event["title"].lower()
            for keyword in [
                "meeting",
                "review",
                "sync",
            ]
        )
    ]

    hours = [
        {
            "value":
                hour,

            "label":
                datetime.strptime(
                    str(hour),
                    "%H",
                ).strftime(
                    "%I %p"
                ).lstrip(
                    "0"
                ),
        }
        for hour in range(
            7,
            22,
        )
    ]

    return {
        "state":
            state,

        "current_view":
            current_view,

        "popup_open":
            state in popup_states,

        "is_mobile_sheet":
            state == "mobile_event_sheet",

        "selected_date":
            selected_date.isoformat(),

        "today":
            today.isoformat(),

        "month_title":
            month_anchor.strftime(
                "%B %Y"
            ),

        "events":
            events,

        "selected_event":
            selected_event,

        "month_days":
            generate_month_days(
                anchor_date=month_anchor,
                events=events,
            ),

        "week_days":
            generate_week_days(
                selected_date=selected_date,
                events=events,
            ),

        "agenda_days":
            generate_agenda_days(
                selected_date=selected_date,
                events=events,
            ),

        "mini_calendar_days":
            generate_mini_calendar(
                anchor_date=month_anchor,
            ),

        "hours":
            hours,

        "search_query":
            search_query,

        "search_results":
            search_results,

        "weekday_names": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ],

        "calendars": [
            {
                "id": "personal",
                "name": "Personal",
                "color": "blue",
                "checked": True,
            },
            {
                "id": "work",
                "name": "Work",
                "color": "purple",
                "checked": True,
            },
            {
                "id": "research",
                "name": "Research",
                "color": "green",
                "checked": True,
            },
            {
                "id": "birthdays",
                "name": "Birthdays",
                "color": "orange",
                "checked": False,
            },
        ],

        "viewport":
            viewport or {},
    }