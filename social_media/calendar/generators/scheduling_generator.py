from __future__ import annotations

import random

from datetime import (
    date,
    datetime,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# Scheduling States
# ==========================================================

SCHEDULING_STATES = [
    "availability_grid",
    "team_schedule",
    "meeting_poll",
    "booking_form",
    "conflict_warning",
    "timezone_menu",
    "invitee_panel",
    "recurring_dialog",
    "booking_confirmation",
    "empty_availability",
]


TIMEZONES = [
    "Asia/Seoul",
    "America/Los_Angeles",
    "America/New_York",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Australia/Sydney",
]


MEETING_TITLES = [
    "Project planning",
    "Research discussion",
    "Weekly team sync",
    "Design review",
    "Progress meeting",
    "Client consultation",
    "Thesis discussion",
    "Sprint retrospective",
]


# ==========================================================
# Participant Generator
# ==========================================================

def generate_participant(
    index: int,
) -> dict:

    name = fake.name()

    initials = "".join(
        name_part[0].upper()
        for name_part in name.split()[:2]
    )

    return {
        "id":
            f"participant_{index}",

        "name":
            name,

        "email":
            fake.email(),

        "initials":
            initials,

        "role":
            random.choice(
                [
                    "Organizer",
                    "Required",
                    "Optional",
                ]
            ),

        "status":
            random.choice(
                [
                    "accepted",
                    "accepted",
                    "pending",
                    "declined",
                ]
            ),

        "color":
            random.choice(
                [
                    "blue",
                    "green",
                    "purple",
                    "orange",
                    "teal",
                ]
            ),
    }


# ==========================================================
# Time Slot Generator
# ==========================================================

def generate_time_slots(
    participant_count: int,
    empty: bool = False,
) -> list[dict]:

    slots = []

    start_hour = 8

    for slot_index in range(
        20
    ):

        hour = (
            start_hour
            + slot_index // 2
        )

        minute = (
            30
            if slot_index % 2
            else 0
        )

        start_datetime = (
            datetime.combine(
                date.today(),
                datetime.min.time(),
            )
            .replace(
                hour=hour,
                minute=minute,
            )
        )

        end_datetime = (
            start_datetime
            + timedelta(
                minutes=30,
            )
        )

        if empty:

            availability = [
                False
                for _ in range(
                    participant_count
                )
            ]

        else:

            availability = [
                random.random() < 0.68
                for _ in range(
                    participant_count
                )
            ]

        available_count = sum(
            availability
        )

        slots.append(
            {
                "id":
                    f"slot_{slot_index}",

                "start":
                    start_datetime.strftime(
                        "%H:%M"
                    ),

                "end":
                    end_datetime.strftime(
                        "%H:%M"
                    ),

                "label":
                    start_datetime.strftime(
                        "%I:%M %p"
                    ).lstrip(
                        "0"
                    ),

                "availability":
                    availability,

                "available_count":
                    available_count,

                "fully_available":
                    (
                        available_count
                        == participant_count
                    ),

                "mostly_available":
                    (
                        available_count
                        >= max(
                            1,
                            participant_count - 1,
                        )
                    ),

                "selected":
                    False,
            }
        )

    return slots


# ==========================================================
# Meeting Poll
# ==========================================================

def generate_poll_options(
    start_date: date,
) -> list[dict]:

    poll_options = []

    for index in range(
        random.randint(
            3,
            6,
        )
    ):

        option_date = (
            start_date
            + timedelta(
                days=index
            )
        )

        start_hour = random.choice(
            [
                9,
                10,
                11,
                14,
                15,
                16,
            ]
        )

        votes = random.randint(
            1,
            8,
        )

        poll_options.append(
            {
                "id":
                    f"poll_option_{index}",

                "day_name":
                    option_date.strftime(
                        "%A"
                    ),

                "date_text":
                    option_date.strftime(
                        "%B %d"
                    ),

                "time_text":
                    (
                        f"{start_hour}:00 – "
                        f"{start_hour + 1}:00"
                    ),

                "votes":
                    votes,

                "selected":
                    index == 1,

                "best":
                    False,
            }
        )

    if poll_options:

        best_option = max(
            poll_options,
            key=lambda option:
                option["votes"],
        )

        best_option["best"] = True

    return poll_options


# ==========================================================
# Main Generator
# ==========================================================

def generate_scheduling_data(
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
            SCHEDULING_STATES
        )

    if state not in SCHEDULING_STATES:

        raise ValueError(
            f"Unknown scheduling state: {state}. "
            f"Available states: {SCHEDULING_STATES}"
        )

    participant_count = random.randint(
        4,
        7,
    )

    participants = [
        generate_participant(
            index
        )
        for index in range(
            participant_count
        )
    ]

    empty_availability = (
        state
        == "empty_availability"
    )

    time_slots = generate_time_slots(
        participant_count=participant_count,
        empty=empty_availability,
    )

    selectable_slots = [
        slot
        for slot in time_slots
        if slot["mostly_available"]
    ]

    if selectable_slots:

        selected_slot = random.choice(
            selectable_slots
        )

    elif time_slots:

        selected_slot = time_slots[0]

    else:

        selected_slot = None

    if selected_slot is not None:

        selected_slot["selected"] = True

    popup_states = {
        "conflict_warning",
        "timezone_menu",
        "invitee_panel",
        "recurring_dialog",
        "booking_confirmation",
    }

    meeting_date = (
        date.today()
        + timedelta(
            days=random.randint(
                1,
                14,
            )
        )
    )

    return {
        "state":
            state,

        "popup_open":
            state in popup_states,

        "is_mobile_sheet":
            state == "invitee_panel",

        "meeting_title":
            random.choice(
                MEETING_TITLES
            ),

        "meeting_date":
            meeting_date.isoformat(),

        "meeting_date_text":
            meeting_date.strftime(
                "%A, %B %d"
            ),

        "duration":
            random.choice(
                [
                    30,
                    45,
                    60,
                    90,
                ]
            ),

        "location":
            random.choice(
                [
                    "Google Meet",
                    "Conference Room A",
                    "Research Lab",
                    "Zoom",
                    "Microsoft Teams",
                ]
            ),

        "timezone":
            "Asia/Seoul",

        "timezones":
            TIMEZONES,

        "participants":
            participants,

        "participant_count":
            len(participants),

        "time_slots":
            time_slots,

        "selected_slot":
            selected_slot,

        "poll_options":
            generate_poll_options(
                meeting_date
            ),

        "recurrence_options": [
            "Does not repeat",
            "Daily",
            "Every weekday",
            "Weekly",
            "Monthly",
            "Custom",
        ],

        "selected_recurrence":
            "Weekly",

        "notify_attendees":
            True,

        "allow_guests":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "working_hours": {
            "start": "08:00",
            "end": "18:00",
        },

        "viewport":
            viewport or {},
    }