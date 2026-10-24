from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Appointment States
# ==========================================================

APPOINTMENT_STATES = [
    "service_selection",
    "staff_selection",
    "date_selection",
    "time_selection",
    "booking_form",
    "booking_confirmation",
    "no_availability",
    "appointment_details_dialog",
    "reschedule_dialog",
    "cancel_appointment_dialog",
    "mobile_date_sheet",
]


# ==========================================================
# Static Synthetic Options
# ==========================================================

SERVICE_DEFINITIONS = [
    {
        "name": "Initial consultation",
        "icon": "forum",
        "duration": 30,
        "price": 0,
        "description": (
            "A short introductory meeting to discuss "
            "requirements, questions, and goals."
        ),
    },
    {
        "name": "Project review",
        "icon": "fact_check",
        "duration": 60,
        "price": 50,
        "description": (
            "Review current project progress, open issues, "
            "and recommended next steps."
        ),
    },
    {
        "name": "Research mentoring",
        "icon": "school",
        "duration": 45,
        "price": 35,
        "description": (
            "One-to-one mentoring for research planning, "
            "methods, writing, and publication strategy."
        ),
    },
    {
        "name": "Design feedback",
        "icon": "palette",
        "duration": 45,
        "price": 40,
        "description": (
            "Detailed feedback about interface design, "
            "accessibility, and usability."
        ),
    },
    {
        "name": "Technical support",
        "icon": "support_agent",
        "duration": 30,
        "price": 25,
        "description": (
            "Troubleshooting session for technical "
            "problems and implementation questions."
        ),
    },
    {
        "name": "Career consultation",
        "icon": "work",
        "duration": 45,
        "price": 30,
        "description": (
            "Discuss professional goals, career planning, "
            "and future opportunities."
        ),
    },
]


STAFF_ROLES = [
    "Senior consultant",
    "Research advisor",
    "Design specialist",
    "Technical consultant",
    "Project advisor",
    "Career specialist",
]


NEXT_AVAILABLE_OPTIONS = [
    "Today",
    "Tomorrow",
    "Wednesday",
    "Thursday",
    "Friday",
    "Next Monday",
]


MEETING_METHODS = [
    {
        "id": "google_meet",
        "name": "Google Meet",
        "icon": "videocam",
    },
    {
        "id": "zoom",
        "name": "Zoom",
        "icon": "video_camera_front",
    },
    {
        "id": "phone",
        "name": "Phone call",
        "icon": "call",
    },
    {
        "id": "in_person",
        "name": "In person",
        "icon": "meeting_room",
    },
]


TIME_ZONES = [
    "Asia/Seoul",
    "UTC",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Berlin",
    "Asia/Tokyo",
    "Asia/Singapore",
]


CANCELLATION_REASONS = [
    "Schedule conflict",
    "No longer needed",
    "Booked by mistake",
    "Need a different specialist",
    "Need a different appointment type",
    "Other",
]


# ==========================================================
# Initials
# ==========================================================

def generate_initials(
    name: str,
) -> str:
    """
    Generate initials from a synthetic Faker name.

    Faker's standard Generator does not provide an
    `initials()` method, so initials are derived safely
    from the generated name.
    """

    name_parts = [
        part
        for part in name.strip().split()
        if part
    ]

    if not name_parts:
        return "U"

    if len(name_parts) == 1:
        return (
            name_parts[0][0]
            .upper()
        )

    return (
        name_parts[0][0]
        + name_parts[-1][0]
    ).upper()


# ==========================================================
# Customer Generator
# ==========================================================

def generate_customer() -> dict:
    """
    Generate a completely synthetic customer.
    """

    name = fake.name()

    return {
        "name":
            name,

        "initials":
            generate_initials(
                name
            ),

        "email":
            fake.email(),

        "phone":
            fake.phone_number(),

        "company":
            fake.company(),

        "job_title":
            fake.job(),

        "address":
            fake.address()
            .replace(
                "\n",
                ", ",
            ),

        "notes":
            fake.sentence(
                nb_words=random.randint(
                    8,
                    16,
                )
            ),
    }


# ==========================================================
# Profile Generator
# ==========================================================

def generate_profile() -> dict:
    """
    Generate a synthetic signed-in profile.
    """

    name = fake.name()

    return {
        "name":
            name,

        "initials":
            generate_initials(
                name
            ),

        "email":
            fake.email(),

        "avatar_url":
            None,
    }


# ==========================================================
# Staff Generator
# ==========================================================

def generate_staff_member(
    index: int,
) -> dict:
    """
    Generate one synthetic appointment specialist.
    """

    name = fake.name()

    available = (
        random.random() < 0.85
    )

    return {
        "id":
            f"staff-{index}",

        "name":
            name,

        "initials":
            generate_initials(
                name
            ),

        "email":
            fake.email(),

        "role":
            random.choice(
                STAFF_ROLES
            ),

        "company":
            fake.company(),

        "rating":
            round(
                random.uniform(
                    4.5,
                    5.0,
                ),
                1,
            ),

        "review_count":
            random.randint(
                18,
                320,
            ),

        "next_available":
            random.choice(
                NEXT_AVAILABLE_OPTIONS
            ),

        "available":
            available,

        "bio":
            fake.paragraph(
                nb_sentences=2
            ),

        "specialties":
            random.sample(
                [
                    "Planning",
                    "Research",
                    "Accessibility",
                    "Interface design",
                    "Technical review",
                    "Project management",
                    "Career development",
                ],
                k=random.randint(
                    2,
                    4,
                ),
            ),
    }


def generate_staff_members(
    count: int = 5,
) -> list[dict]:
    """
    Generate multiple synthetic staff members.
    """

    staff_members = [
        generate_staff_member(
            index=index,
        )
        for index in range(
            1,
            count + 1,
        )
    ]

    if staff_members:
        staff_members[0]["available"] = True
        staff_members[0]["selected"] = True

    for staff_member in staff_members[1:]:
        staff_member["selected"] = False

    return staff_members


# ==========================================================
# Service Generator
# ==========================================================

def generate_services() -> list[dict]:
    """
    Generate appointment services.
    """

    services = []

    for index, definition in enumerate(
        SERVICE_DEFINITIONS,
        start=1,
    ):
        services.append({
            "id":
                f"service-{index}",

            "name":
                definition["name"],

            "icon":
                definition["icon"],

            "duration":
                definition["duration"],

            "price":
                definition["price"],

            "description":
                definition["description"],

            "selected":
                index == 1,

            "available":
                random.random() < 0.95,
        })

    return services


# ==========================================================
# Calendar Day Generator
# ==========================================================

def generate_calendar_days(
    number_of_days: int = 14,
) -> list[dict]:
    """
    Generate synthetic appointment dates.
    """

    today = datetime.now()

    days = []

    selected_assigned = False

    for offset in range(
        number_of_days
    ):
        value = (
            today
            + timedelta(
                days=offset,
            )
        )

        is_weekend = (
            value.weekday() >= 5
        )

        available = (
            not is_weekend
            and random.random() < 0.85
        )

        selected = False

        if (
            available
            and not selected_assigned
            and offset > 0
        ):
            selected = True
            selected_assigned = True

        days.append({
            "id":
                f"day-{offset}",

            "weekday":
                value.strftime("%a"),

            "day":
                value.day,

            "month":
                value.strftime("%b"),

            "year":
                value.year,

            "iso_date":
                value.strftime(
                    "%Y-%m-%d"
                ),

            "full_date":
                value.strftime(
                    "%A, %B %d, %Y"
                ),

            "available":
                available,

            "selected":
                selected,

            "is_today":
                offset == 0,

            "is_weekend":
                is_weekend,
        })

    if (
        days
        and not selected_assigned
    ):
        days[0]["available"] = True
        days[0]["selected"] = True

    return days


# ==========================================================
# Time Slot Generator
# ==========================================================

def generate_time_slots(
    *,
    start_hour: int = 9,
    end_hour: int = 18,
    interval_minutes: int = 30,
) -> list[dict]:
    """
    Generate appointment time slots.
    """

    slots = []

    slot_index = 0

    current = (
        datetime.now()
        .replace(
            hour=start_hour,
            minute=0,
            second=0,
            microsecond=0,
        )
    )

    ending = (
        datetime.now()
        .replace(
            hour=end_hour,
            minute=0,
            second=0,
            microsecond=0,
        )
    )

    while current < ending:
        available = (
            random.random() < 0.68
        )

        slots.append({
            "id":
                f"time-{slot_index}",

            "time":
                current.strftime(
                    "%I:%M %p"
                ),

            "time_24":
                current.strftime(
                    "%H:%M"
                ),

            "available":
                available,

            "selected":
                False,

            "period": (
                "Morning"
                if current.hour < 12
                else (
                    "Afternoon"
                    if current.hour < 17
                    else "Evening"
                )
            ),
        })

        current += timedelta(
            minutes=interval_minutes,
        )

        slot_index += 1

    available_slots = [
        slot
        for slot in slots
        if slot["available"]
    ]

    if available_slots:
        random.choice(
            available_slots
        )["selected"] = True

    elif slots:
        slots[0]["available"] = True
        slots[0]["selected"] = True

    return slots


# ==========================================================
# Meeting Method Generator
# ==========================================================

def generate_meeting_methods() -> list[dict]:
    """
    Return meeting methods with one selected method.
    """

    selected_index = random.randrange(
        len(MEETING_METHODS)
    )

    return [
        {
            **method,
            "selected":
                index == selected_index,
        }
        for index, method in enumerate(
            MEETING_METHODS
        )
    ]


# ==========================================================
# Appointment History Generator
# ==========================================================

def generate_appointment_history(
    count: int = 3,
) -> list[dict]:
    """
    Generate fictional previous appointment records.
    """

    history = []

    for index in range(
        1,
        count + 1,
    ):
        specialist_name = fake.name()

        date_value = (
            datetime.now()
            - timedelta(
                days=random.randint(
                    5,
                    120,
                ),
            )
        )

        history.append({
            "id":
                f"history-{index}",

            "service":
                random.choice(
                    SERVICE_DEFINITIONS
                )["name"],

            "specialist":
                specialist_name,

            "specialist_initials":
                generate_initials(
                    specialist_name
                ),

            "date":
                date_value.strftime(
                    "%B %d, %Y"
                ),

            "status":
                random.choice([
                    "Completed",
                    "Completed",
                    "Cancelled",
                ]),
        })

    return history


# ==========================================================
# Selected Record Helpers
# ==========================================================

def get_selected_record(
    records: list[dict],
) -> dict:
    """
    Return the selected record or the first record.
    """

    selected = next(
        (
            record
            for record in records
            if record.get(
                "selected",
                False,
            )
        ),
        None,
    )

    if selected is not None:
        return selected

    if not records:
        raise ValueError(
            "Cannot select a record "
            "from an empty list."
        )

    return records[0]


# ==========================================================
# Main Appointment Generator
# ==========================================================

def generate_appointment_data(
    state: str | None = None,
) -> dict:
    """
    Generate complete synthetic data for all appointment
    scheduling states.
    """

    if state is None:
        state = random.choice(
            APPOINTMENT_STATES
        )

    if state not in APPOINTMENT_STATES:
        raise ValueError(
            f"Unknown appointment state: "
            f"{state}. "
            f"Available states: "
            f"{APPOINTMENT_STATES}"
        )

    profile = generate_profile()
    customer = generate_customer()

    services = generate_services()

    staff_members = (
        generate_staff_members(
            count=random.randint(
                4,
                6,
            )
        )
    )

    calendar_days = (
        generate_calendar_days(
            number_of_days=14,
        )
    )

    time_slots = (
        generate_time_slots(
            start_hour=9,
            end_hour=18,
            interval_minutes=30,
        )
    )

    meeting_methods = (
        generate_meeting_methods()
    )

    selected_service = (
        get_selected_record(
            services
        )
    )

    selected_staff = (
        get_selected_record(
            staff_members
        )
    )

    selected_day = (
        get_selected_record(
            calendar_days
        )
    )

    selected_time = (
        get_selected_record(
            time_slots
        )
    )

    selected_meeting_method = (
        get_selected_record(
            meeting_methods
        )
    )

    if state == "no_availability":
        for day in calendar_days:
            day["available"] = False
            day["selected"] = False

        for slot in time_slots:
            slot["available"] = False
            slot["selected"] = False

    popup_states = {
        "appointment_details_dialog",
        "reschedule_dialog",
        "cancel_appointment_dialog",
        "mobile_date_sheet",
    }

    booking_reference = (
        f"APT-"
        f"{random.randint(100000, 999999)}"
    )

    created_at = datetime.now()

    cancellation_deadline = (
        created_at
        + timedelta(
            hours=random.choice([
                12,
                24,
                48,
            ]),
        )
    )

    return {
        "app_name":
            "Calendar Appointments",

        "state":
            state,

        "popup_open":
            state in popup_states,

        "page_title":
            "Schedule an appointment",

        "profile":
            profile,

        "customer":
            customer,

        "steps": [
            {
                "id":
                    "service_selection",

                "label":
                    "Service",

                "number":
                    1,
            },
            {
                "id":
                    "staff_selection",

                "label":
                    "Specialist",

                "number":
                    2,
            },
            {
                "id":
                    "date_selection",

                "label":
                    "Date",

                "number":
                    3,
            },
            {
                "id":
                    "time_selection",

                "label":
                    "Time",

                "number":
                    4,
            },
            {
                "id":
                    "booking_form",

                "label":
                    "Details",

                "number":
                    5,
            },
        ],

        "services":
            services,

        "staff_members":
            staff_members,

        "calendar_days":
            calendar_days,

        "time_slots":
            time_slots,

        "meeting_methods":
            meeting_methods,

        "selected_service":
            selected_service,

        "selected_staff":
            selected_staff,

        "selected_day":
            selected_day,

        "selected_time":
            selected_time,

        "selected_meeting_method":
            selected_meeting_method,

        "booking_reference":
            booking_reference,

        "appointment_status":
            random.choice([
                "Confirmed",
                "Pending confirmation",
            ]),

        "timezone":
            random.choice(
                TIME_ZONES
            ),

        "cancellation_reasons":
            CANCELLATION_REASONS.copy(),

        "appointment_history":
            generate_appointment_history(
                count=random.randint(
                    2,
                    5,
                )
            ),

        "created_at":
            created_at.strftime(
                "%B %d, %Y at %I:%M %p"
            ),

        "cancellation_deadline":
            cancellation_deadline.strftime(
                "%B %d at %I:%M %p"
            ),

        "confirmation_message":
            fake.sentence(
                nb_words=random.randint(
                    8,
                    14,
                )
            ),
    }


# ==========================================================
# Generate Specific State
# ==========================================================

def generate_appointment_state(
    state: str,
) -> dict:
    """
    Convenience function for generating a specific state.
    """

    return generate_appointment_data(
        state=state,
    )


# ==========================================================
# Generate All States
# ==========================================================

def generate_all_appointment_states() -> list[dict]:
    """
    Generate one sample for every appointment state.
    """

    return [
        generate_appointment_data(
            state=state,
        )
        for state in APPOINTMENT_STATES
    ]


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":
    import pprint

    print(
        "\n=========================================="
    )
    print(
        "CALENDAR APPOINTMENT GENERATOR"
    )
    print(
        "=========================================="
    )

    sample = generate_appointment_data()

    print(
        "State:",
        sample["state"],
    )

    print(
        "Profile:",
        sample["profile"]["name"],
    )

    print(
        "Customer:",
        sample["customer"]["name"],
    )

    print(
        "Customer email:",
        sample["customer"]["email"],
    )

    print(
        "Selected service:",
        sample["selected_service"]["name"],
    )

    print(
        "Selected staff:",
        sample["selected_staff"]["name"],
    )

    print(
        "Selected date:",
        sample["selected_day"]["full_date"],
    )

    print(
        "Selected time:",
        sample["selected_time"]["time"],
    )

    print(
        "Popup open:",
        sample["popup_open"],
    )

    print(
        "\nGenerated data:"
    )

    pprint.pp(
        sample
    )