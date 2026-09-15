from __future__ import annotations

import random

from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
    get_random_thumbnail,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Utility
# ==========================================================

def format_count(
    value: int,
) -> str:

    if value >= 1_000_000_000:

        value = value / 1_000_000_000

        return (
            f"{value:.1f}B"
            .replace(".0B", "B")
        )

    if value >= 1_000_000:

        value = value / 1_000_000

        return (
            f"{value:.1f}M"
            .replace(".0M", "M")
        )

    if value >= 1_000:

        value = value / 1_000

        return (
            f"{value:.1f}K"
            .replace(".0K", "K")
        )

    return str(value)


# ==========================================================
# Channel
# ==========================================================

def generate_channel_name() -> str:

    return random.choice(
        [
            fake.name(),
            f"{fake.first_name()} Tech",
            f"{fake.word().title()} Studio",
            f"{fake.word().title()} Official",
            f"The {fake.last_name()} Show",
            f"{fake.word().title()} Academy",
        ]
    )


def generate_channel() -> dict[str, Any]:

    subscribers = random.randint(
        500,
        30_000_000,
    )

    return {
        "name":
            generate_channel_name(),

        "avatar":
            get_random_avatar(),

        "verified":
            random.random() < 0.35,

        "subscribers":
            subscribers,

        "subscribers_text":
            f"{format_count(subscribers)} subscribers",
    }


# ==========================================================
# Notification Time
# ==========================================================

def generate_notification_time() -> str:

    return random.choice(
        [
            "2 minutes ago",
            "8 minutes ago",
            "20 minutes ago",
            "45 minutes ago",
            "1 hour ago",
            "2 hours ago",
            "4 hours ago",
            "8 hours ago",
            "12 hours ago",
            "1 day ago",
            "2 days ago",
            "3 days ago",
            "1 week ago",
        ]
    )


# ==========================================================
# Notification Text
# ==========================================================

def generate_video_title() -> str:

    return (
        fake.sentence(
            nb_words=random.randint(
                5,
                11,
            )
        )
        .rstrip(".")
    )


def generate_notification_message(
    notification_type: str,
    channel: dict[str, Any],
) -> str:

    channel_name = channel["name"]

    if notification_type == "upload":

        return (
            f"{channel_name} uploaded: "
            f"{generate_video_title()}"
        )

    if notification_type == "live":

        return (
            f"{channel_name} is live now: "
            f"{generate_video_title()}"
        )

    if notification_type == "premiere":

        return (
            f"{channel_name} scheduled a premiere: "
            f"{generate_video_title()}"
        )

    if notification_type == "recommendation":

        return (
            "Recommended: "
            f"{generate_video_title()}"
        )

    if notification_type == "reply":

        return (
            f"{channel_name} replied to your comment: "
            f"“{fake.sentence(nb_words=random.randint(4, 9)).rstrip('.')}”"
        )

    if notification_type == "mention":

        return (
            f"{channel_name} mentioned you in a comment."
        )

    if notification_type == "community":

        return (
            f"{channel_name} posted: "
            f"{fake.sentence(nb_words=random.randint(5, 12)).rstrip('.')}"
        )

    return (
        f"New activity from {channel_name}"
    )


# ==========================================================
# Notification
# ==========================================================

def generate_notification(
    index: int,
) -> dict[str, Any]:

    notification_type = random.choices(
        population=[
            "upload",
            "live",
            "premiere",
            "recommendation",
            "reply",
            "mention",
            "community",
        ],
        weights=[
            30,
            8,
            8,
            18,
            12,
            8,
            16,
        ],
        k=1,
    )[0]

    channel = generate_channel()

    has_thumbnail = (
        notification_type
        in {
            "upload",
            "live",
            "premiere",
            "recommendation",
        }
    )

    unread = random.random() < 0.40

    return {
        "id":
            f"notification_{index}",

        "type":
            notification_type,

        "channel":
            channel,

        "message":
            generate_notification_message(
                notification_type,
                channel,
            ),

        "timestamp":
            generate_notification_time(),

        "thumbnail":
            (
                get_random_thumbnail()
                if has_thumbnail
                else None
            ),

        "has_thumbnail":
            has_thumbnail,

        "unread":
            unread,

        "show_more":
            True,

        "show_action":
            notification_type
            in {
                "live",
                "premiere",
            },

        "action_label":
            (
                "Watch"
                if notification_type == "live"
                else "Notify me"
                if notification_type == "premiere"
                else None
            ),
    }


# ==========================================================
# Notification Sections
# ==========================================================

def generate_notification_sections() -> list[dict[str, Any]]:

    total_count = random.randint(
        14,
        28,
    )

    notifications = [
        generate_notification(index)
        for index in range(total_count)
    ]

    split_today = random.randint(
        6,
        min(
            12,
            len(notifications),
        ),
    )

    today_items = (
        notifications[
            :split_today
        ]
    )

    earlier_items = (
        notifications[
            split_today:
        ]
    )

    sections = [
        {
            "id":
                "today",

            "title":
                "Today",

            "items":
                today_items,
        },
    ]

    if earlier_items:

        sections.append(
            {
                "id":
                    "earlier",

                "title":
                    "Earlier",

                "items":
                    earlier_items,
            }
        )

    return sections


# ==========================================================
# Header
# ==========================================================

def generate_header() -> dict[str, Any]:

    return {
        "logo_text":
            "YouTube",

        "search_placeholder":
            "Search",

        "show_voice_search":
            random.random() < 0.90,

        "show_create":
            True,

        "show_notifications":
            True,

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> list[dict[str, Any]]:

    return [
        {
            "label": "Home",
            "icon": "home",
            "semantic": "home",
            "selected": False,
        },
        {
            "label": "Shorts",
            "icon": "smart_display",
            "semantic": "shorts",
            "selected": False,
        },
        {
            "label": "Subscriptions",
            "icon": "subscriptions",
            "semantic": "subscriptions",
            "selected": False,
        },
        {
            "label": "You",
            "icon": "account_circle",
            "semantic": "you",
            "selected": False,
        },
        {
            "label": "History",
            "icon": "history",
            "semantic": "history",
            "selected": False,
        },
    ]


# ==========================================================
# Bottom Navigation
# ==========================================================

def generate_bottom_navigation() -> list[dict[str, Any]]:

    return [
        {
            "label": "Home",
            "icon": "home",
            "semantic": "home",
            "selected": False,
            "create": False,
        },
        {
            "label": "Shorts",
            "icon": "smart_display",
            "semantic": "shorts",
            "selected": False,
            "create": False,
        },
        {
            "label": "",
            "icon": "add_circle",
            "semantic": "create",
            "selected": False,
            "create": True,
        },
        {
            "label": "Subscriptions",
            "icon": "subscriptions",
            "semantic": "subscriptions",
            "selected": False,
            "create": False,
        },
        {
            "label": "You",
            "icon": "account_circle",
            "semantic": "you",
            "selected": False,
            "create": False,
        },
    ]


# ==========================================================
# Page Controls
# ==========================================================

def generate_controls() -> dict[str, Any]:

    return {
        "title":
            "Notifications",

        "settings_label":
            "Notification settings",

        "filter_label":
            "All",

        "filters":
            [
                {
                    "label": "All",
                    "value": "all",
                    "selected": True,
                },
                {
                    "label": "Mentions",
                    "value": "mentions",
                    "selected": False,
                },
            ],
    }


# ==========================================================
# Notifications Page
# ==========================================================

def generate_notifications_page() -> dict[str, Any]:

    sections = (
        generate_notification_sections()
    )

    unread_count = sum(
        1

        for section in sections

        for notification
        in section["items"]

        if notification["unread"]
    )

    return {
        "page_type":
            "notifications",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "controls":
            generate_controls(),

        "sections":
            sections,

        "unread_count":
            unread_count,

        "layout": {
            "show_sidebar":
                True,

            "show_bottom_navigation":
                True,

            "show_filters":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_notifications_page()
    )

    print(
        "\n"
        "=================================="
    )

    print(
        "YOUTUBE NOTIFICATIONS PAGE"
    )

    print(
        "=================================="
    )

    print(
        "Sections:",
        len(page["sections"])
    )

    total_notifications = sum(
        len(
            section["items"]
        )

        for section
        in page["sections"]
    )

    print(
        "Notifications:",
        total_notifications
    )

    print(
        "Unread:",
        page["unread_count"]
    )

    for section in page["sections"]:

        print(
            section["title"],
            ":",
            len(section["items"]),
        )

    print(
        "\nFirst few notifications:"
    )

    for section in page["sections"]:

        for notification in section["items"][:3]:

            print(
                notification["type"],
                "|",
                notification["message"],
            )

        break