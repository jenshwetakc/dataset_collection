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

NOTIFICATION_STATES = [
    "all_notifications",
    "unread",
    "event_reminders",
    "schedule_changes",
    "responses",
    "snoozed",
    "search_results",
    "empty_notifications",
    "loading",
    "error",
    "notification_details_dialog",
    "snooze_dialog",
    "clear_all_dialog",
    "notification_settings_dialog",
    "mobile_filter_sheet",
]


# ==========================================================
# Constants
# ==========================================================

EVENT_TITLES = [
    "Product roadmap review",
    "Design system workshop",
    "Research planning",
    "Sprint retrospective",
    "Release readiness",
    "Customer interview",
    "Accessibility review",
    "Quarterly planning",
    "Project kickoff",
    "Team synchronization",
]

LOCATIONS = [
    "Meeting Room A",
    "Conference Room B",
    "Design Studio",
    "Google Meet",
    "Zoom",
    "Main Office",
    "Online meeting",
]

NOTIFICATION_CONFIG = {
    "reminder": {
        "icon": "notifications",
        "label": "Reminder",
    },
    "schedule_change": {
        "icon": "update",
        "label": "Schedule change",
    },
    "response": {
        "icon": "how_to_reg",
        "label": "Response",
    },
    "invitation": {
        "icon": "mail",
        "label": "Invitation",
    },
    "cancelled": {
        "icon": "event_busy",
        "label": "Cancelled",
    },
}

SNOOZE_OPTIONS = [
    {
        "id": "ten_minutes",
        "label": "10 minutes",
        "description": "Remind me again shortly",
        "icon": "timer",
    },
    {
        "id": "one_hour",
        "label": "1 hour",
        "description": "Remind me in one hour",
        "icon": "schedule",
    },
    {
        "id": "tomorrow",
        "label": "Tomorrow",
        "description": "Tomorrow at 9:00 AM",
        "icon": "today",
    },
    {
        "id": "custom",
        "label": "Custom",
        "description": "Choose a date and time",
        "icon": "edit_calendar",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_initials(name: str) -> str:
    parts = [
        part
        for part in name.split()
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


def generate_notification(
    index: int,
) -> dict:
    notification_type = random.choice(
        list(NOTIFICATION_CONFIG)
    )

    config = NOTIFICATION_CONFIG[
        notification_type
    ]

    organizer_name = fake.name()
    event_title = random.choice(EVENT_TITLES)

    event_datetime = (
        datetime.now()
        + timedelta(
            days=random.randint(0, 10),
            hours=random.randint(1, 9),
        )
    )

    if notification_type == "reminder":
        message = (
            f"{event_title} starts in "
            f"{random.choice([10, 15, 30, 60])} minutes."
        )

    elif notification_type == "schedule_change":
        message = (
            f"{organizer_name} changed the time "
            f"of {event_title}."
        )

    elif notification_type == "response":
        response = random.choice([
            "accepted",
            "declined",
            "tentatively accepted",
        ])

        message = (
            f"{organizer_name} {response} "
            f"the invitation to {event_title}."
        )

    elif notification_type == "invitation":
        message = (
            f"{organizer_name} invited you "
            f"to {event_title}."
        )

    else:
        message = (
            f"{event_title} was cancelled "
            f"by {organizer_name}."
        )

    return {
        "id": f"notification-{index}",
        "type": notification_type,
        "type_label": config["label"],
        "icon": config["icon"],
        "title": event_title,
        "message": message,
        "organizer": organizer_name,
        "organizer_initials":
            generate_initials(
                organizer_name
            ),
        "organizer_email": fake.email(),
        "event_date":
            event_datetime.strftime(
                "%A, %B %d"
            ),
        "event_time":
            event_datetime.strftime(
                "%I:%M %p"
            ),
        "location":
            random.choice(LOCATIONS),
        "received_time":
            random.choice([
                "Just now",
                "5 min ago",
                "20 min ago",
                "1 hour ago",
                "Yesterday",
            ]),
        "unread":
            random.random() < 0.55,
        "snoozed":
            random.random() < 0.18,
        "important":
            random.random() < 0.25,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_notifications_data(
    state: str | None = None,
) -> dict:
    state = (
        state
        or random.choice(
            NOTIFICATION_STATES
        )
    )

    if state not in NOTIFICATION_STATES:
        raise ValueError(
            f"Unknown notification state: {state}. "
            f"Available states: {NOTIFICATION_STATES}"
        )

    notifications = [
        generate_notification(index)
        for index in range(
            1,
            random.randint(9, 15),
        )
    ]

    selected_notification = notifications[0]

    popup_states = {
        "notification_details_dialog",
        "snooze_dialog",
        "clear_all_dialog",
        "notification_settings_dialog",
        "mobile_filter_sheet",
    }

    if state == "unread":
        for notification in notifications:
            notification["unread"] = True

    elif state == "event_reminders":
        notifications = [
            notification
            for notification in notifications
            if notification["type"] == "reminder"
        ]

    elif state == "schedule_changes":
        notifications = [
            notification
            for notification in notifications
            if notification["type"]
            in {
                "schedule_change",
                "cancelled",
            }
        ]

    elif state == "responses":
        notifications = [
            notification
            for notification in notifications
            if notification["type"] == "response"
        ]

    elif state == "snoozed":
        for notification in notifications:
            notification["snoozed"] = True

    elif state == "search_results":
        notifications = notifications[:3]

    elif state == "empty_notifications":
        notifications = []

    profile_name = fake.name()

    return {
        "state": state,

        "popup_open":
            state in popup_states,

        "profile": {
            "name": profile_name,
            "initials":
                generate_initials(
                    profile_name
                ),
        },

        "page_title":
            "Notifications",

        "search_query": (
            random.choice([
                "meeting",
                "planning",
                "review",
            ])
            if state == "search_results"
            else ""
        ),

        "notifications":
            notifications,

        "selected_notification":
            selected_notification,

        "notification_count":
            len(notifications),

        "unread_count":
            sum(
                notification["unread"]
                for notification in notifications
            ),

        "reminder_count":
            sum(
                notification["type"]
                == "reminder"
                for notification in notifications
            ),

        "schedule_change_count":
            sum(
                notification["type"]
                in {
                    "schedule_change",
                    "cancelled",
                }
                for notification in notifications
            ),

        "response_count":
            sum(
                notification["type"]
                == "response"
                for notification in notifications
            ),

        "snoozed_count":
            sum(
                notification["snoozed"]
                for notification in notifications
            ),

        "snooze_options":
            SNOOZE_OPTIONS,

        "settings": {
            "event_reminders": True,
            "schedule_changes": True,
            "guest_responses": True,
            "new_invitations": True,
            "email_notifications":
                random.choice([
                    True,
                    False,
                ]),
            "desktop_notifications":
                random.choice([
                    True,
                    False,
                ]),
        },

        "error_message": (
            "Notifications could not be loaded. "
            "Check your connection and try again."
        ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":
    for page_state in NOTIFICATION_STATES:
        data = generate_notifications_data(
            state=page_state
        )

        print(
            page_state,
            len(data["notifications"]),
            data["popup_open"],
        )