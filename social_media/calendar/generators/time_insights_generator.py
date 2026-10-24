from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

TIME_INSIGHT_STATES = [
    "overview",
    "focus_time",
    "meeting_insights",
    "work_life_balance",
    "goals",
    "no_data",
    "metric_details_dialog",
    "create_goal_dialog",
    "export_report_dialog",
    "mobile_filter_sheet",
]


# ==========================================================
# Constants
# ==========================================================

INSIGHT_NAVIGATION = [
    {
        "id": "overview",
        "label": "Overview",
        "icon": "dashboard",
    },
    {
        "id": "focus_time",
        "label": "Focus time",
        "icon": "psychology",
    },
    {
        "id": "meeting_insights",
        "label": "Meetings",
        "icon": "groups",
    },
    {
        "id": "work_life_balance",
        "label": "Work-life balance",
        "icon": "balance",
    },
    {
        "id": "goals",
        "label": "Goals",
        "icon": "flag",
    },
]


MEETING_CATEGORIES = [
    {
        "name": "Team meetings",
        "icon": "groups",
        "color": "#4285F4",
    },
    {
        "name": "One-to-one",
        "icon": "person",
        "color": "#34A853",
    },
    {
        "name": "Project reviews",
        "icon": "fact_check",
        "color": "#A142F4",
    },
    {
        "name": "External meetings",
        "icon": "public",
        "color": "#FBBC04",
    },
]


FOCUS_LABELS = [
    "Deep work",
    "Research",
    "Writing",
    "Planning",
    "Development",
]


GOAL_DEFINITIONS = [
    {
        "title": "Increase focus time",
        "icon": "psychology",
        "unit": "hours",
    },
    {
        "title": "Reduce meeting time",
        "icon": "groups",
        "unit": "hours",
    },
    {
        "title": "Finish work on time",
        "icon": "schedule",
        "unit": "days",
    },
    {
        "title": "Keep lunch time free",
        "icon": "lunch_dining",
        "unit": "days",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_initials(
    name: str,
) -> str:
    parts = [
        part
        for part in name.strip().split()
        if part
    ]

    if not parts:
        return "U"

    if len(parts) == 1:
        return parts[0][0].upper()

    return (
        parts[0][0]
        + parts[-1][0]
    ).upper()


def minutes_to_text(
    minutes: int,
) -> str:
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours and remaining_minutes:
        return (
            f"{hours}h "
            f"{remaining_minutes}m"
        )

    if hours:
        return f"{hours}h"

    return f"{remaining_minutes}m"


# ==========================================================
# Profile
# ==========================================================

def generate_profile() -> dict:
    name = fake.name()

    return {
        "name":
            name,

        "email":
            fake.email(),

        "initials":
            generate_initials(
                name
            ),
    }


# ==========================================================
# Week Data
# ==========================================================

def generate_week_data() -> list[dict]:
    start_date = (
        datetime.now()
        - timedelta(
            days=datetime.now().weekday()
        )
    )

    week = []

    for index in range(7):
        value = (
            start_date
            + timedelta(days=index)
        )

        meeting_minutes = random.randint(
            30,
            300,
        )

        focus_minutes = random.randint(
            30,
            360,
        )

        collaboration_minutes = random.randint(
            15,
            180,
        )

        total_minutes = (
            meeting_minutes
            + focus_minutes
            + collaboration_minutes
        )

        week.append({
            "id":
                f"day-{index}",

            "weekday":
                value.strftime("%a"),

            "date":
                value.strftime("%b %d"),

            "meeting_minutes":
                meeting_minutes,

            "focus_minutes":
                focus_minutes,

            "collaboration_minutes":
                collaboration_minutes,

            "total_minutes":
                total_minutes,

            "meeting_height":
                min(
                    100,
                    max(
                        12,
                        round(
                            meeting_minutes
                            / 300
                            * 100
                        ),
                    ),
                ),

            "focus_height":
                min(
                    100,
                    max(
                        12,
                        round(
                            focus_minutes
                            / 360
                            * 100
                        ),
                    ),
                ),

            "is_today":
                value.date()
                == datetime.now().date(),
        })

    return week


# ==========================================================
# Metrics
# ==========================================================

def generate_metrics(
    week_data: list[dict],
) -> list[dict]:
    meeting_minutes = sum(
        day["meeting_minutes"]
        for day in week_data
    )

    focus_minutes = sum(
        day["focus_minutes"]
        for day in week_data
    )

    collaboration_minutes = sum(
        day["collaboration_minutes"]
        for day in week_data
    )

    total_minutes = sum(
        day["total_minutes"]
        for day in week_data
    )

    return [
        {
            "id": "focus",
            "title": "Focus time",
            "icon": "psychology",
            "value": minutes_to_text(
                focus_minutes
            ),
            "change": random.randint(-12, 28),
            "positive": True,
            "description": (
                "Time protected for uninterrupted work"
            ),
        },
        {
            "id": "meetings",
            "title": "Meeting time",
            "icon": "groups",
            "value": minutes_to_text(
                meeting_minutes
            ),
            "change": random.randint(-25, 18),
            "positive": False,
            "description": (
                "Time spent in scheduled meetings"
            ),
        },
        {
            "id": "collaboration",
            "title": "Collaboration",
            "icon": "forum",
            "value": minutes_to_text(
                collaboration_minutes
            ),
            "change": random.randint(-10, 25),
            "positive": True,
            "description": (
                "Shared work and communication time"
            ),
        },
        {
            "id": "scheduled",
            "title": "Scheduled time",
            "icon": "calendar_today",
            "value": minutes_to_text(
                total_minutes
            ),
            "change": random.randint(-8, 16),
            "positive": True,
            "description": (
                "Total time scheduled this week"
            ),
        },
    ]


# ==========================================================
# Focus Sessions
# ==========================================================

def generate_focus_sessions() -> list[dict]:
    sessions = []

    for index in range(
        random.randint(5, 9)
    ):
        date_value = (
            datetime.now()
            - timedelta(
                days=random.randint(0, 12)
            )
        )

        duration = random.choice([
            30,
            45,
            60,
            90,
            120,
        ])

        sessions.append({
            "id":
                f"focus-{index}",

            "title":
                random.choice(
                    FOCUS_LABELS
                ),

            "date":
                date_value.strftime(
                    "%a, %b %d"
                ),

            "duration":
                duration,

            "duration_text":
                minutes_to_text(
                    duration
                ),

            "completed":
                random.random() < 0.82,

            "interruption_count":
                random.randint(0, 5),
        })

    return sessions


# ==========================================================
# Meeting Categories
# ==========================================================

def generate_meeting_categories() -> list[dict]:
    categories = []

    for index, category in enumerate(
        MEETING_CATEGORIES,
        start=1,
    ):
        minutes = random.randint(
            60,
            420,
        )

        categories.append({
            "id":
                f"meeting-category-{index}",

            "name":
                category["name"],

            "icon":
                category["icon"],

            "color":
                category["color"],

            "minutes":
                minutes,

            "time_text":
                minutes_to_text(
                    minutes
                ),

            "meeting_count":
                random.randint(2, 14),

            "percentage":
                random.randint(15, 85),
        })

    return categories


# ==========================================================
# Meeting Records
# ==========================================================

def generate_meetings() -> list[dict]:
    meetings = []

    for index in range(
        random.randint(5, 10)
    ):
        organizer_name = fake.name()

        date_value = (
            datetime.now()
            - timedelta(
                days=random.randint(0, 14)
            )
        )

        duration = random.choice([
            30,
            45,
            60,
            90,
        ])

        meetings.append({
            "id":
                f"meeting-{index}",

            "title":
                random.choice([
                    "Weekly team sync",
                    "Project planning",
                    "Research review",
                    "Design feedback",
                    "Release readiness",
                    "One-to-one meeting",
                ]),

            "organizer":
                organizer_name,

            "organizer_initials":
                generate_initials(
                    organizer_name
                ),

            "date":
                date_value.strftime(
                    "%a, %b %d"
                ),

            "duration":
                duration,

            "duration_text":
                minutes_to_text(
                    duration
                ),

            "attendee_count":
                random.randint(2, 18),
        })

    return meetings


# ==========================================================
# Work-Life Metrics
# ==========================================================

def generate_balance_metrics() -> list[dict]:
    return [
        {
            "id": "after_hours",
            "title": "After-hours work",
            "icon": "nights_stay",
            "value": random.randint(1, 7),
            "unit": "hours",
            "progress": random.randint(15, 65),
            "description": (
                "Scheduled work outside regular hours"
            ),
        },
        {
            "id": "meeting_free",
            "title": "Meeting-free days",
            "icon": "event_available",
            "value": random.randint(1, 4),
            "unit": "days",
            "progress": random.randint(20, 80),
            "description": (
                "Days without scheduled meetings"
            ),
        },
        {
            "id": "lunch_protected",
            "title": "Protected lunch",
            "icon": "lunch_dining",
            "value": random.randint(2, 5),
            "unit": "days",
            "progress": random.randint(40, 100),
            "description": (
                "Lunch periods without meetings"
            ),
        },
        {
            "id": "end_on_time",
            "title": "Finished on time",
            "icon": "schedule",
            "value": random.randint(2, 5),
            "unit": "days",
            "progress": random.randint(35, 100),
            "description": (
                "Workdays ending at the planned time"
            ),
        },
    ]


# ==========================================================
# Goals
# ==========================================================

def generate_goals() -> list[dict]:
    goals = []

    for index, definition in enumerate(
        GOAL_DEFINITIONS,
        start=1,
    ):
        target = random.randint(
            4,
            12,
        )

        current = random.randint(
            1,
            target,
        )

        progress = round(
            current
            / target
            * 100
        )

        goals.append({
            "id":
                f"goal-{index}",

            "title":
                definition["title"],

            "icon":
                definition["icon"],

            "unit":
                definition["unit"],

            "target":
                target,

            "current":
                current,

            "progress":
                progress,

            "completed":
                progress >= 100,

            "enabled":
                random.random() < 0.9,
        })

    return goals


# ==========================================================
# Main Generator
# ==========================================================

def generate_time_insights_data(
    state: str | None = None,
) -> dict:
    if state is None:
        state = random.choice(
            TIME_INSIGHT_STATES
        )

    if state not in TIME_INSIGHT_STATES:
        raise ValueError(
            f"Unknown time insight state: "
            f"{state}. "
            f"Available states: "
            f"{TIME_INSIGHT_STATES}"
        )

    profile = generate_profile()

    week_data = generate_week_data()

    metrics = generate_metrics(
        week_data
    )

    focus_sessions = (
        generate_focus_sessions()
    )

    meeting_categories = (
        generate_meeting_categories()
    )

    meetings = generate_meetings()

    balance_metrics = (
        generate_balance_metrics()
    )

    goals = generate_goals()

    popup_states = {
        "metric_details_dialog",
        "create_goal_dialog",
        "export_report_dialog",
        "mobile_filter_sheet",
    }

    selected_metric = random.choice(
        metrics
    )

    selected_meeting = random.choice(
        meetings
    )

    return {
        "app_name":
            "Calendar Time Insights",

        "state":
            state,

        "popup_open":
            state in popup_states,

        "page_title":
            "Time insights",

        "profile":
            profile,

        "navigation":
            INSIGHT_NAVIGATION.copy(),

        "period": {
            "id": "this_week",
            "label": "This week",
            "start": (
                datetime.now()
                - timedelta(
                    days=datetime.now()
                    .weekday()
                )
            ).strftime("%b %d"),

            "end": (
                datetime.now()
                + timedelta(
                    days=6
                    - datetime.now()
                    .weekday()
                )
            ).strftime("%b %d"),
        },

        "period_options": [
            {
                "id": "this_week",
                "label": "This week",
            },
            {
                "id": "last_week",
                "label": "Last week",
            },
            {
                "id": "last_30_days",
                "label": "Last 30 days",
            },
            {
                "id": "custom",
                "label": "Custom range",
            },
        ],

        "week_data":
            (
                []
                if state == "no_data"
                else week_data
            ),

        "metrics":
            (
                []
                if state == "no_data"
                else metrics
            ),

        "focus_sessions":
            focus_sessions,

        "meeting_categories":
            meeting_categories,

        "meetings":
            meetings,

        "balance_metrics":
            balance_metrics,

        "goals":
            goals,

        "selected_metric":
            selected_metric,

        "selected_meeting":
            selected_meeting,

        "focus_goal": {
            "target_minutes":
                random.choice([
                    600,
                    720,
                    900,
                    1200,
                ]),

            "current_minutes":
                random.randint(
                    300,
                    900,
                ),
        },

        "work_hours": {
            "start":
                random.choice([
                    "08:00 AM",
                    "08:30 AM",
                    "09:00 AM",
                ]),

            "end":
                random.choice([
                    "05:00 PM",
                    "05:30 PM",
                    "06:00 PM",
                ]),
        },

        "export_formats": [
            {
                "id": "pdf",
                "label": "PDF report",
                "icon": "picture_as_pdf",
            },
            {
                "id": "csv",
                "label": "CSV data",
                "icon": "table_view",
            },
            {
                "id": "image",
                "label": "Dashboard image",
                "icon": "image",
            },
        ],
    }


# ==========================================================
# State Helpers
# ==========================================================

def generate_time_insights_state(
    state: str,
) -> dict:
    return generate_time_insights_data(
        state=state,
    )


def generate_all_time_insight_states() -> list[dict]:
    return [
        generate_time_insights_data(
            state=state
        )
        for state in TIME_INSIGHT_STATES
    ]


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":
    import pprint

    sample = (
        generate_time_insights_data()
    )

    print(
        "\n=========================================="
    )
    print(
        "CALENDAR TIME INSIGHTS"
    )
    print(
        "=========================================="
    )

    print(
        "State:",
        sample["state"],
    )

    print(
        "Synthetic profile:",
        sample["profile"]["name"],
    )

    print(
        "Metrics:",
        len(sample["metrics"]),
    )

    print(
        "Focus sessions:",
        len(sample["focus_sessions"]),
    )

    print(
        "Meetings:",
        len(sample["meetings"]),
    )

    print(
        "Goals:",
        len(sample["goals"]),
    )

    print(
        "Popup:",
        sample["popup_open"],
    )

    pprint.pp(
        sample
    )