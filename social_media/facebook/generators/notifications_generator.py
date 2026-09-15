# social_media/facebook/generators/notifications_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_post_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

NOTIFICATION_STATES = [
    "default",
    "default",
    "unread_only",
    "earlier_notifications",
    "notification_menu_open",
    "mark_all_read",
    "settings_open",
    "filter_active",
]


NOTIFICATION_TYPES = [
    {
        "icon": "thumb_up",
        "action": "liked your post.",
    },
    {
        "icon": "chat_bubble",
        "action": "commented on your photo.",
    },
    {
        "icon": "person_add",
        "action": "sent you a friend request.",
    },
    {
        "icon": "groups",
        "action": "invited you to join a group.",
    },
    {
        "icon": "celebration",
        "action": "has a birthday today.",
    },
    {
        "icon": "share",
        "action": "shared your post.",
    },
    {
        "icon": "event",
        "action": "invited you to an event.",
    },
]


TIMESTAMPS = [
    "Just now",
    "2 min",
    "8 min",
    "20 min",
    "1 h",
    "3 h",
    "Yesterday",
    "2 days ago",
]


FILTER_OPTIONS = [
    "All",
    "Unread",
    "Comments",
    "Tags",
    "Friend requests",
]


# ==========================================================
# Notification
# ==========================================================

def generate_notification(
    index: int,
) -> dict:

    selected = random.choice(
        NOTIFICATION_TYPES
    )

    has_preview = (
        random.random() < 0.25
    )

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "icon":
            selected["icon"],

        "action":
            selected["action"],

        "timestamp":
            random.choice(
                TIMESTAMPS
            ),

        "unread":
            random.random() < 0.45,

        "preview":
            (
                get_random_post_image()
                if has_preview
                else None
            ),

        "today":
            random.random() < 0.65,
    }


def generate_notifications(
    count: int = 18,
) -> list[dict]:

    return [
        generate_notification(index)
        for index in range(count)
    ]


# ==========================================================
# State
# ==========================================================

def generate_notifications_state(
    notification_count: int,
) -> dict:

    name = random.choice(
        NOTIFICATION_STATES
    )

    selected_notification = None

    if name == "notification_menu_open":

        selected_notification = random.randint(
            0,
            max(
                0,
                min(
                    notification_count - 1,
                    8,
                )
            ),
        )

    selected_filter = None

    if name == "filter_active":

        selected_filter = random.choice(
            FILTER_OPTIONS[1:]
        )

    return {
        "name":
            name,

        "selected_notification":
            selected_notification,

        "selected_filter":
            selected_filter,
    }


# ==========================================================
# Settings
# ==========================================================

def generate_notification_settings() -> list[dict]:

    return [
        {
            "name": "Push notifications",
            "icon": "notifications_active",
            "enabled": random.random() < 0.8,
        },
        {
            "name": "Email notifications",
            "icon": "mail",
            "enabled": random.random() < 0.5,
        },
        {
            "name": "SMS notifications",
            "icon": "sms",
            "enabled": random.random() < 0.3,
        },
        {
            "name": "Friend requests",
            "icon": "person_add",
            "enabled": True,
        },
        {
            "name": "Tags",
            "icon": "sell",
            "enabled": random.random() < 0.8,
        },
    ]


# ==========================================================
# Complete Data
# ==========================================================

def generate_notifications_data() -> dict:

    notifications = generate_notifications(
        count=random.randint(
            14,
            22,
        )
    )

    return {
        "notifications":
            notifications,

        "filters":
            FILTER_OPTIONS,

        "settings":
            generate_notification_settings(),

        "state":
            generate_notifications_state(
                notification_count=len(
                    notifications
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_notifications_data()

    unread_count = len(
        [
            item
            for item in data["notifications"]
            if item["unread"]
        ]
    )

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK NOTIFICATIONS GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Notifications:",
        len(
            data["notifications"]
        ),
    )

    print(
        "Unread:",
        unread_count,
    )

    print(
        "State:",
        data["state"],
    )