from __future__ import annotations

import calendar
import random

from datetime import (
    date,
    datetime,
    timedelta,
)

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Calendar States
# ==========================================================

CALENDAR_STATES = [
    "calendar_month",
    "calendar_week",
    "event_selected",
    "meeting_invite",
    "create_event",
    "edit_event",
    "attendee_suggestions",
    "date_picker_popup",
    "event_more_menu",
    "delete_event_confirm",
    "mobile_event_sheet",
]


# ==========================================================
# Pools
# ==========================================================

EVENT_TITLES = [
    "Project sync",
    "Research meeting",
    "Design review",
    "Weekly planning",
    "Team stand-up",
    "Client discussion",
    "Paper review",
    "Sprint retrospective",
    "Lunch meeting",
    "Workshop",
]

LOCATIONS = [
    "Meeting Room A",
    "Conference Room 3",
    "Online meeting",
    "Research Lab",
    "Main Office",
    "Room 402",
]

EVENT_TYPES = [
    "meeting",
    "focus",
    "personal",
    "reminder",
]


# ==========================================================
# Helpers
# ==========================================================

def _person() -> dict:

    name = fake.name()

    return {
        "name": name,
        "email": fake.email(),
        "avatar": get_random_avatar(),
    }


def _event(
    index: int,
    base_date: date,
) -> dict:

    event_date = (
        base_date
        + timedelta(
            days=random.randint(
                -6,
                20,
            )
        )
    )

    start_hour = random.randint(
        8,
        18,
    )

    duration = random.choice([
        30,
        45,
        60,
        90,
    ])

    start_time = datetime.combine(
        event_date,
        datetime.min.time(),
    ).replace(
        hour=start_hour,
        minute=random.choice([
            0,
            30,
        ]),
    )

    end_time = (
        start_time
        + timedelta(
            minutes=duration,
        )
    )

    attendees = [
        _person()
        for _ in range(
            random.randint(
                1,
                5,
            )
        )
    ]

    return {
        "id":
            f"event_{index}",

        "title":
            random.choice(
                EVENT_TITLES
            ),

        "date":
            event_date.isoformat(),

        "day":
            event_date.day,

        "weekday":
            event_date.strftime(
                "%A"
            ),

        "start":
            start_time.strftime(
                "%H:%M"
            ),

        "end":
            end_time.strftime(
                "%H:%M"
            ),

        "time_range":
            (
                f"{start_time.strftime('%H:%M')}"
                f" – "
                f"{end_time.strftime('%H:%M')}"
            ),

        "location":
            random.choice(
                LOCATIONS
            ),

        "type":
            random.choice(
                EVENT_TYPES
            ),

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "organizer":
            _person(),

        "attendees":
            attendees,

        "response":
            random.choice([
                "accepted",
                "tentative",
                "pending",
            ]),

        "online":
            random.random()
            < 0.55,

        "reminder":
            random.choice([
                "10 minutes before",
                "30 minutes before",
                "1 hour before",
            ]),
    }


def _build_month_days(
    year: int,
    month: int,
    events: list[dict],
) -> list[dict]:

    _, days_in_month = calendar.monthrange(
        year,
        month,
    )

    result = []

    for day_number in range(
        1,
        days_in_month + 1,
    ):

        day_events = [
            event
            for event in events
            if (
                datetime.fromisoformat(
                    event["date"]
                ).year == year
                and
                datetime.fromisoformat(
                    event["date"]
                ).month == month
                and
                datetime.fromisoformat(
                    event["date"]
                ).day == day_number
            )
        ]

        result.append({
            "day":
                day_number,

            "events":
                day_events[:3],

            "event_count":
                len(
                    day_events
                ),
        })

    return result


def _week_days(
    base_date: date,
) -> list[dict]:

    monday = (
        base_date
        - timedelta(
            days=base_date.weekday()
        )
    )

    return [
        {
            "date":
                (
                    monday
                    + timedelta(
                        days=index
                    )
                ).isoformat(),

            "weekday":
                (
                    monday
                    + timedelta(
                        days=index
                    )
                ).strftime(
                    "%a"
                ),

            "day":
                (
                    monday
                    + timedelta(
                        days=index
                    )
                ).day,
        }
        for index in range(
            7
        )
    ]


# ==========================================================
# Public Generator
# ==========================================================

def generate_calendar_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            CALENDAR_STATES
        )
    )

    if selected_state not in CALENDAR_STATES:

        raise ValueError(
            f"Unknown calendar state: "
            f"{selected_state}"
        )

    today = date.today()

    event_count = random.randint(
        16,
        28,
    )

    events = [
        _event(
            index=index,
            base_date=today,
        )
        for index in range(
            event_count
        )
    ]

    selected_event = random.choice(
        events
    )

    edit_event = dict(
        selected_event
    )

    attendee_suggestions = [
        _person()
        for _ in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    return {
        "state":
            selected_state,

        "title":
            "Calendar",

        "today":
            today.isoformat(),

        "current_month":
            today.strftime(
                "%B %Y"
            ),

        "current_year":
            today.year,

        "current_month_number":
            today.month,

        "month_days":
            _build_month_days(
                year=today.year,
                month=today.month,
                events=events,
            ),

        "week_days":
            _week_days(
                today
            ),

        "events":
            events,

        "selected_event":
            selected_event,

        "show_week":
            selected_state
            == "calendar_week",

        "show_selected_event":
            selected_state
            in {
                "event_selected",
                "meeting_invite",
            },

        "show_create_event":
            selected_state
            == "create_event",

        "show_edit_event":
            selected_state
            == "edit_event",

        "attendee_suggestions":
            (
                attendee_suggestions
                if selected_state
                == "attendee_suggestions"
                else []
            ),

        "date_picker_open":
            selected_state
            == "date_picker_popup",

        "event_more_menu_open":
            selected_state
            == "event_more_menu",

        "delete_confirm_open":
            selected_state
            == "delete_event_confirm",

        "mobile_event_sheet_open":
            selected_state
            == "mobile_event_sheet",

        "form":
            (
                edit_event
                if selected_state
                == "edit_event"
                else {
                    "title":
                        random.choice(
                            EVENT_TITLES
                        ),

                    "date":
                        today.isoformat(),

                    "start":
                        "10:00",

                    "end":
                        "11:00",

                    "location":
                        random.choice(
                            LOCATIONS
                        ),

                    "description":
                        "",

                    "attendees":
                        [],
                }
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_calendar_data()

    print(
        "state=",
        data["state"],
    )

    print(
        "events=",
        len(
            data["events"]
        ),
    )