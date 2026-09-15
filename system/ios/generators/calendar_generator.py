from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

CALENDAR_STATES = [

    "month_view",

    "day_view",

    "event_detail",

    "create_event",

    "search_active",

    "invitation",

    "delete_confirmation",

    "empty_day",
]


CALENDAR_STATE_WEIGHTS = [

    24,

    20,

    12,

    12,

    10,

    8,

    6,

    8,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Calendar Definitions
# ==========================================================

CALENDARS = [

    {
        "id": "work",
        "title": "Work",
        "color": "#0A84FF",
    },

    {
        "id": "personal",
        "title": "Personal",
        "color": "#BF5AF2",
    },

    {
        "id": "study",
        "title": "Study",
        "color": "#30D158",
    },

    {
        "id": "important",
        "title": "Important",
        "color": "#FF453A",
    },

    {
        "id": "other",
        "title": "Other",
        "color": "#FF9F0A",
    },
]


# ==========================================================
# Event
# ==========================================================

def generate_event(
    index: int,
) -> dict:

    calendar = random.choice(
        CALENDARS
    )

    start_hour = random.randint(
        8,
        19,
    )

    duration = random.choice([
        30,
        45,
        60,
        90,
        120,
    ])

    end_minutes = (
        start_hour * 60
        + duration
    )

    end_hour = (
        end_minutes // 60
    )

    end_minute = (
        end_minutes % 60
    )


    titles = [

        "Research Meeting",

        "Project Review",

        "Lunch",

        "Presentation Practice",

        "Study Session",

        "Team Sync",

        "Doctor Appointment",

        "Coffee with Alex",

        "Weekly Planning",

        "Design Review",

        "Experiment Check",

        "Call with Team",
    ]


    locations = [

        "Meeting Room",

        "Office",

        "Campus",

        "Online",

        "Library",

        "Cafe",

        "",
    ]


    return {

        "id":
            f"event_{index}",

        "title":
            random.choice(
                titles
            ),

        "calendar":
            calendar,

        "start_hour":
            start_hour,

        "start_time":
            f"{start_hour:02d}:00",

        "end_time":
            f"{end_hour:02d}:{end_minute:02d}",

        "duration":
            duration,

        "location":
            random.choice(
                locations
            ),

        "notes":
            random.choice([
                "",
                "Bring the latest draft.",
                "Review results before meeting.",
                "Prepare slides.",
                "Discuss next steps.",
            ]),

        "all_day":
            random.random() < 0.10,

        "video_call":
            random.random() < 0.30,

        "has_alert":
            random.random() < 0.80,
    }


# ==========================================================
# Events
# ==========================================================

def generate_events(
    count: int = 8,
) -> list[dict]:

    return [

        generate_event(
            index
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Month Grid
# ==========================================================

def generate_month_days() -> list[dict]:

    now = datetime.now()

    first = now.replace(
        day=1
    )

    first_weekday = (
        first.weekday()
        + 1
    ) % 7

    days_in_month = 30

    if now.month in {
        1,
        3,
        5,
        7,
        8,
        10,
        12,
    }:

        days_in_month = 31

    elif now.month == 2:

        days_in_month = 28


    cells = []


    # Previous month filler

    for index in range(
        first_weekday
    ):

        cells.append({

            "day":
                30 - first_weekday + index + 1,

            "current_month":
                False,

            "today":
                False,

            "event_count":
                0,
        })


    # Current month

    for day in range(
        1,
        days_in_month + 1,
    ):

        cells.append({

            "day":
                day,

            "current_month":
                True,

            "today":
                day == now.day,

            "event_count":
                random.choice([
                    0,
                    0,
                    1,
                    1,
                    2,
                    3,
                ]),
        })


    # Fill six weeks

    next_day = 1

    while len(
        cells
    ) < 42:

        cells.append({

            "day":
                next_day,

            "current_month":
                False,

            "today":
                False,

            "event_count":
                0,
        })

        next_day += 1


    return cells


# ==========================================================
# Search
# ==========================================================

def generate_search(
    events: list[dict],
) -> dict:

    query = random.choice([

        "meeting",

        "project",

        "study",

        "review",

        "call",
    ])


    results = [

        event
        for event
        in events
        if query.lower()
        in event["title"].lower()
    ]


    if not results:

        results = random.sample(

            events,

            k=min(
                len(events),
                4,
            ),
        )


    return {

        "query":
            query,

        "results":
            results,
    }


# ==========================================================
# Invitation
# ==========================================================

def generate_invitation() -> dict:

    return {

        "title":
            random.choice([
                "Team Dinner",
                "Research Discussion",
                "Project Review",
                "Weekly Sync",
            ]),

        "organizer":
            fake.name(),

        "time":
            random.choice([
                "Today, 4:00 PM",
                "Tomorrow, 10:30 AM",
                "Friday, 2:00 PM",
            ]),

        "location":
            random.choice([
                "Meeting Room",
                "Campus Cafe",
                "Online",
            ]),

        "actions": [

            {
                "id":
                    "decline",

                "title":
                    "Decline",
            },

            {
                "id":
                    "maybe",

                "title":
                    "Maybe",
            },

            {
                "id":
                    "accept",

                "title":
                    "Accept",
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_calendar_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            CALENDAR_STATES,

            weights=
                CALENDAR_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in CALENDAR_STATES:

        raise ValueError(
            f"Unknown Calendar state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Events
    # ======================================================

    events = (

        []

        if state == "empty_day"

        else generate_events(
            count=
                random.randint(
                    6,
                    11,
                )
        )
    )


    active_event = (

        random.choice(
            events
        )

        if events
        else None
    )


    # ======================================================
    # Overlay States
    # ======================================================

    is_overlay_state = (
        state
        in {
            "event_detail",
            "create_event",
            "invitation",
            "delete_confirmation",
        }
    )


    now = datetime.now()


    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "title":
            "Calendar",


        "month": {

            "title":
                now.strftime(
                    "%B %Y"
                ),

            "days":
                generate_month_days(),

            "weekdays": [
                "Sun",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
            ],
        },


        "day": {

            "weekday":
                now.strftime(
                    "%A"
                ),

            "date":
                now.strftime(
                    "%B %d"
                ).replace(
                    " 0",
                    " "
                ),
        },


        "events":
            events,

        "active_event":
            active_event,


        "search":
            generate_search(
                events
            )
            if events
            else {
                "query": "",
                "results": [],
            },


        "invitation":
            generate_invitation(),


        "delete_confirmation": {

            "title":
                "Delete Event?",

            "message":
                (
                    "This event will be removed "
                    "from your calendar."
                ),

            "cancel":
                "Cancel",

            "confirm":
                "Delete Event",
        },


        "create_event": {

            "title":
                random.choice([
                    "",
                    "New Event",
                    "Meeting",
                    "Study Session",
                ]),

            "location":
                random.choice([
                    "",
                    "Meeting Room",
                    "Campus",
                    "Online",
                ]),

            "all_day":
                random.random() < 0.18,

            "alert":
                random.choice([
                    "None",
                    "At time of event",
                    "10 minutes before",
                    "30 minutes before",
                ]),
        },


        "icons": {

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "search":
                resolve_icon(
                    "search"
                ),

            "back":
                resolve_icon(
                    "back"
                ),

            "calendar":
                resolve_icon(
                    "calendar"
                ),

            "location":
                resolve_icon(
                    "location",
                    "map-pin",
                ),

            "video":
                get_lucide_icon(
                    "video"
                ),

            "bell":
                resolve_icon(
                    "notifications",
                    "bell",
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "chevron":
                resolve_icon(
                    "forward"
                ),

            "clock":
                get_lucide_icon(
                    "clock-3"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in CALENDAR_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_calendar_data(
                state=
                    state
            ),

            sort_dicts=False,
        )