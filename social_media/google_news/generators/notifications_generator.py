from __future__ import annotations

import random

from faker import Faker

from social_media.google_news.generators.media_generator import (
    get_random_article_image,
    get_random_avatar,
    get_random_publisher_logo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

NOTIFICATION_STATES = [
    "normal",
    "unread",
    "grouped",
    "empty",
    "settings",
    "permission_dialog",
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "For you",
        "icon": "home",
        "selected": False,
    },
    {
        "label": "Headlines",
        "icon": "article",
        "selected": False,
    },
    {
        "label": "Following",
        "icon": "star",
        "selected": False,
    },
    {
        "label": "Notifications",
        "icon": "notifications",
        "selected": True,
    },
]


# ==========================================================
# Pools
# ==========================================================

PUBLISHERS = [
    "Global News",
    "Daily Chronicle",
    "The Observer",
    "World Report",
    "Morning Journal",
    "Tech Daily",
    "Science Today",
    "Business Review",
    "City News",
    "National Desk",
]


TOPICS = [
    "Technology",
    "World",
    "Business",
    "Science",
    "Climate",
    "Health",
    "Sports",
    "Entertainment",
]


NOTIFICATION_TYPES = [
    "breaking",
    "topic",
    "source",
    "recommendation",
    "local",
    "live",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "Just now",
            "4 min ago",
            "12 min ago",
            "28 min ago",
            "1 hour ago",
            "2 hours ago",
            "Yesterday",
        ]
    )


def generate_publisher() -> dict:

    return {
        "name":
            random.choice(
                PUBLISHERS
            ),

        "logo":
            get_random_publisher_logo(),
    }


# ==========================================================
# Notification
# ==========================================================

def generate_notification(
    *,
    force_unread: bool | None = None,
) -> dict:

    notification_type = (
        random.choice(
            NOTIFICATION_TYPES
        )
    )


    if force_unread is None:

        unread = (
            random.random()
            < 0.40
        )

    else:

        unread = (
            force_unread
        )


    topic = (
        random.choice(
            TOPICS
        )
    )


    publisher = (
        generate_publisher()
    )


    if notification_type == "breaking":

        title = (
            "Breaking: "
            +
            fake.sentence(
                nb_words=random.randint(
                    6,
                    11,
                )
            )
        )

        icon = "breaking_news"

    elif notification_type == "topic":

        title = (
            f"New stories about {topic}"
        )

        icon = "interests"

    elif notification_type == "source":

        title = (
            f"{publisher['name']} published a new story"
        )

        icon = "newspaper"

    elif notification_type == "recommendation":

        title = (
            "Recommended for you: "
            +
            fake.sentence(
                nb_words=random.randint(
                    5,
                    10,
                )
            )
        )

        icon = "auto_awesome"

    elif notification_type == "local":

        title = (
            "Local update: "
            +
            fake.sentence(
                nb_words=random.randint(
                    5,
                    10,
                )
            )
        )

        icon = "location_on"

    else:

        title = (
            "Live coverage: "
            +
            fake.sentence(
                nb_words=random.randint(
                    5,
                    10,
                )
            )
        )

        icon = "live_tv"


    return {

        "type":
            notification_type,

        "title":
            title,

        "body":
            fake.text(
                max_nb_chars=random.randint(
                    80,
                    150,
                )
            ),

        "timestamp":
            generate_timestamp(),

        "publisher":
            publisher,

        "topic":
            topic,

        "icon":
            icon,

        "image":
            (
                get_random_article_image()
                if random.random()
                < 0.65
                else None
            ),

        "unread":
            unread,

        "important":
            (
                notification_type
                in {
                    "breaking",
                    "live",
                }
            ),

        "saved":
            random.random()
            < 0.15,
    }


# ==========================================================
# Grouped Notifications
# ==========================================================

def generate_groups() -> list[dict]:

    return [
        {
            "label":
                "Today",

            "notifications": [
                generate_notification()
                for _ in range(
                    random.randint(
                        3,
                        5,
                    )
                )
            ],
        },
        {
            "label":
                "Yesterday",

            "notifications": [
                generate_notification()
                for _ in range(
                    random.randint(
                        2,
                        4,
                    )
                )
            ],
        },
        {
            "label":
                "Earlier",

            "notifications": [
                generate_notification()
                for _ in range(
                    random.randint(
                        2,
                        4,
                    )
                )
            ],
        },
    ]


# ==========================================================
# Settings
# ==========================================================

def generate_settings() -> list[dict]:

    return [
        {
            "label": "Breaking news",
            "description":
                "Major developing stories and urgent alerts",
            "icon": "breaking_news",
            "enabled": True,
        },
        {
            "label": "Topics you follow",
            "description":
                "Updates from topics in your Following feed",
            "icon": "interests",
            "enabled":
                random.random()
                < 0.80,
        },
        {
            "label": "Sources you follow",
            "description":
                "New stories from followed publishers",
            "icon": "newspaper",
            "enabled":
                random.random()
                < 0.75,
        },
        {
            "label": "Local news",
            "description":
                "Important stories from your area",
            "icon": "location_on",
            "enabled":
                random.random()
                < 0.70,
        },
        {
            "label": "Recommended stories",
            "description":
                "Personalized news suggestions",
            "icon": "auto_awesome",
            "enabled":
                random.random()
                < 0.65,
        },
        {
            "label": "Live coverage",
            "description":
                "Updates from ongoing events",
            "icon": "live_tv",
            "enabled":
                random.random()
                < 0.80,
        },
    ]


# ==========================================================
# Main
# ==========================================================

def generate_notifications_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            NOTIFICATION_STATES
        )
    )


    if selected_state not in NOTIFICATION_STATES:

        raise ValueError(
            f"Unknown notification state: "
            f"{selected_state}"
        )


    notifications = []

    groups = []


    if selected_state not in {
        "empty",
        "settings",
    }:

        if selected_state == "unread":

            notifications = [
                generate_notification(
                    force_unread=(
                        index
                        < 5
                    )
                )
                for index in range(
                    random.randint(
                        7,
                        11,
                    )
                )
            ]

        else:

            notifications = [
                generate_notification()
                for _ in range(
                    random.randint(
                        7,
                        11,
                    )
                )
            ]


    if selected_state == "grouped":

        groups = (
            generate_groups()
        )

        notifications = []


    unread_count = sum(
        1
        for item in notifications
        if item["unread"]
    )


    if groups:

        unread_count = sum(
            1
            for group in groups
            for item in group["notifications"]
            if item["unread"]
        )


    return {

        "state":
            selected_state,

        "brand": {
            "name":
                "Google News",
        },

        "user": {
            "name":
                fake.name(),

            "avatar":
                get_random_avatar(),
        },

        "navigation":
            NAVIGATION_ITEMS,

        "page_title":
            "Notifications",

        "page_subtitle":
            "News alerts and updates for you",

        "notifications":
            notifications,

        "groups":
            groups,

        "unread_count":
            unread_count,

        "settings":
            generate_settings(),

        "permission": {
            "title":
                "Turn on notifications?",

            "message":
                (
                    "Get breaking news, local alerts "
                    "and updates from topics you follow."
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in NOTIFICATION_STATES:

        print(
            "\n=============================="
        )

        print(
            state.upper()
        )

        print(
            "=============================="
        )

        pprint(
            generate_notifications_data(
                state=state
            )
        )