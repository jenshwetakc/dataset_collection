from __future__ import annotations

import random
from datetime import datetime


SETTINGS_STATES = [
    "overview",
    "general",
    "notifications",
    "working_hours",
    "time_zone",
    "event_defaults",
    "connected_apps",
    "add_calendar_dialog",
    "import_export_dialog",
    "delete_calendar_dialog",
    "mobile_settings_sheet",
]

COLORS = [
    "#4285F4",
    "#34A853",
    "#FBBC04",
    "#EA4335",
    "#A142F4",
    "#00ACC1",
]

TIME_ZONES = [
    "UTC",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Berlin",
    "Asia/Kolkata",
    "Asia/Tokyo",
    "Australia/Sydney",
]

WEEK_DAYS = [
    {"key": "mon", "short": "M", "label": "Monday"},
    {"key": "tue", "short": "T", "label": "Tuesday"},
    {"key": "wed", "short": "W", "label": "Wednesday"},
    {"key": "thu", "short": "T", "label": "Thursday"},
    {"key": "fri", "short": "F", "label": "Friday"},
    {"key": "sat", "short": "S", "label": "Saturday"},
    {"key": "sun", "short": "S", "label": "Sunday"},
]


def generate_calendars() -> list[dict]:
    names = [
        ("Personal", "person"),
        ("Work", "work"),
        ("Birthdays", "cake"),
        ("Project Atlas", "rocket_launch"),
    ]

    calendars = []

    for index, (name, icon) in enumerate(names):
        calendars.append({
            "id": f"calendar-{index + 1}",
            "name": name,
            "icon": icon,
            "color": random.choice(COLORS),
            "visible": random.random() < 0.85,
            "primary": index == 0,
            "event_count": random.randint(8, 64),
        })

    return calendars


def generate_notification_rules() -> list[dict]:
    return [
        {
            "id": "rule-events",
            "title": "Event notifications",
            "description": "Get notified before scheduled events.",
            "enabled": True,
            "method": "Notification",
            "amount": random.choice([5, 10, 15, 30]),
            "unit": "minutes",
            "icon": "notifications",
        },
        {
            "id": "rule-email",
            "title": "Email reminders",
            "description": "Receive a daily overview by email.",
            "enabled": random.choice([True, False]),
            "method": "Email",
            "amount": 1,
            "unit": "day",
            "icon": "mail",
        },
        {
            "id": "rule-changes",
            "title": "Changed events",
            "description": "Notify me when an invitation changes.",
            "enabled": True,
            "method": "Notification",
            "amount": 0,
            "unit": "immediately",
            "icon": "update",
        },
        {
            "id": "rule-cancellations",
            "title": "Cancelled events",
            "description": "Alert me when an event is cancelled.",
            "enabled": random.choice([True, False]),
            "method": "Email",
            "amount": 0,
            "unit": "immediately",
            "icon": "event_busy",
        },
    ]


def generate_connected_apps() -> list[dict]:
    return [
        {
            "name": "Zoom",
            "icon": "videocam",
            "description": "Add Zoom meetings to calendar events.",
            "connected": True,
            "status": "Connected",
        },
        {
            "name": "Microsoft Teams",
            "icon": "groups",
            "description": "Create Teams meetings from events.",
            "connected": random.choice([True, False]),
            "status": "Connected",
        },
        {
            "name": "Slack",
            "icon": "tag",
            "description": "Receive calendar reminders in Slack.",
            "connected": random.choice([True, False]),
            "status": "Connected",
        },
        {
            "name": "Notion",
            "icon": "description",
            "description": "Attach Notion pages to events.",
            "connected": False,
            "status": "Available",
        },
    ]


def generate_working_days() -> list[dict]:
    selected = {"mon", "tue", "wed", "thu", "fri"}

    if random.random() < 0.25:
        selected.add("sat")

    return [
        {
            **day,
            "enabled": day["key"] in selected,
        }
        for day in WEEK_DAYS
    ]


def get_state_title(state: str) -> str:
    titles = {
        "overview": "Settings",
        "general": "General",
        "notifications": "Notifications",
        "working_hours": "Working hours",
        "time_zone": "Time zone",
        "event_defaults": "Event defaults",
        "connected_apps": "Connected apps",
        "add_calendar_dialog": "Settings",
        "import_export_dialog": "Settings",
        "delete_calendar_dialog": "Settings",
        "mobile_settings_sheet": "Settings",
    }

    return titles[state]


def generate_settings_data(
    state: str | None = None,
) -> dict:
    if state is None:
        state = random.choice(SETTINGS_STATES)

    if state not in SETTINGS_STATES:
        raise ValueError(
            f"Unknown settings state: {state}. "
            f"Available states: {SETTINGS_STATES}"
        )

    popup_states = {
        "add_calendar_dialog",
        "import_export_dialog",
        "delete_calendar_dialog",
        "mobile_settings_sheet",
    }

    current_year = datetime.now().year

    return {
        "state": state,
        "page_title": get_state_title(state),
        "popup_open": state in popup_states,
        "is_mobile_sheet": state == "mobile_settings_sheet",

        "profile": {
            "name": random.choice([
                "Alex Morgan",
                "Jordan Lee",
                "Taylor Smith",
                "Morgan Chen",
            ]),
            "email": random.choice([
                "alex@example.com",
                "jordan@example.com",
                "taylor@example.com",
            ]),
            "initials": random.choice(["AM", "JL", "TS", "MC"]),
        },

        "navigation": [
            {
                "id": "overview",
                "label": "Settings overview",
                "icon": "settings",
            },
            {
                "id": "general",
                "label": "General",
                "icon": "tune",
            },
            {
                "id": "notifications",
                "label": "Notifications",
                "icon": "notifications",
            },
            {
                "id": "working_hours",
                "label": "Working hours",
                "icon": "schedule",
            },
            {
                "id": "time_zone",
                "label": "Time zone",
                "icon": "public",
            },
            {
                "id": "event_defaults",
                "label": "Event defaults",
                "icon": "event",
            },
            {
                "id": "connected_apps",
                "label": "Connected apps",
                "icon": "extension",
            },
        ],

        "calendars": generate_calendars(),
        "notification_rules": generate_notification_rules(),
        "connected_apps": generate_connected_apps(),
        "working_days": generate_working_days(),

        "general": {
            "language": "English (United States)",
            "country": "United States",
            "date_format": "MM/DD/YYYY",
            "time_format": random.choice(["12-hour", "24-hour"]),
            "week_start": random.choice(["Sunday", "Monday"]),
            "show_weekends": random.choice([True, True, False]),
            "show_declined": random.choice([True, False]),
            "compact_events": random.choice([True, False]),
        },

        "working_hours": {
            "enabled": True,
            "start": random.choice(["08:00", "08:30", "09:00"]),
            "end": random.choice(["17:00", "17:30", "18:00"]),
            "location": random.choice([
                "Office",
                "Remote",
                "Hybrid",
            ]),
        },

        "time_zone": {
            "primary": random.choice(TIME_ZONES),
            "secondary": random.choice(TIME_ZONES),
            "show_secondary": random.choice([True, False]),
            "auto_detect": random.choice([True, True, False]),
        },

        "event_defaults": {
            "duration": random.choice([30, 45, 60]),
            "visibility": random.choice([
                "Default visibility",
                "Private",
                "Public",
            ]),
            "guest_permission": "Modify event",
            "video_meeting": random.choice([
                "None",
                "Google Meet",
                "Zoom",
            ]),
            "color": random.choice(COLORS),
            "add_notifications": True,
        },

        "storage": {
            "used": random.randint(18, 76),
            "events": random.randint(320, 2840),
            "attachments": random.randint(20, 340),
        },

        "import_history": [
            {
                "filename": f"events-{current_year}.ics",
                "result": "128 events imported",
                "status": "Complete",
            },
            {
                "filename": "team-calendar.ics",
                "result": "42 events imported",
                "status": "Complete",
            },
        ],
    }


if __name__ == "__main__":
    import pprint

    pprint.pp(generate_settings_data())