# social_media/facebook/generators/events_generator.py

from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_cover_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

EVENT_STATES = [
    "default",
    "default",
    "upcoming",
    "invites",
    "past_events",
    "event_preview",
    "create_event",
    "invite_people",
    "event_menu_open",
    "search_active",
]


EVENT_CATEGORIES = [
    {
        "name": "Music",
        "icon": "music_note",
    },
    {
        "name": "Food",
        "icon": "restaurant",
    },
    {
        "name": "Sports",
        "icon": "sports_soccer",
    },
    {
        "name": "Art",
        "icon": "palette",
    },
    {
        "name": "Technology",
        "icon": "devices",
    },
    {
        "name": "Travel",
        "icon": "flight",
    },
]


EVENT_NAMES = [
    "Weekend Music Festival",
    "Photography Walk",
    "Community Meetup",
    "Food & Coffee Festival",
    "Tech Networking Night",
    "Morning Run Club",
    "Creative Design Workshop",
    "Book Club Gathering",
    "Outdoor Movie Night",
    "Local Art Exhibition",
]


LOCATIONS = [
    "Seoul",
    "Gangnam",
    "Hongdae",
    "Itaewon",
    "Mapo",
    "Jamsil",
    "Yongsan",
]


# ==========================================================
# Date
# ==========================================================

def generate_event_date(
    future: bool = True,
) -> dict:

    now = datetime.now()

    if future:

        event_date = (
            now
            + timedelta(
                days=random.randint(
                    1,
                    60,
                )
            )
        )

    else:

        event_date = (
            now
            - timedelta(
                days=random.randint(
                    1,
                    90,
                )
            )
        )

    return {
        "month":
            event_date.strftime(
                "%b"
            ).upper(),

        "day":
            event_date.strftime(
                "%d"
            ),

        "date_text":
            event_date.strftime(
                "%a, %b %d"
            ),

        "time":
            random.choice(
                [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "7:30 PM",
                ]
            ),
    }


# ==========================================================
# Event
# ==========================================================

def generate_event(
    index: int,
    future: bool = True,
) -> dict:

    event_date = generate_event_date(
        future=future
    )

    return {
        "id":
            index,

        "name":
            random.choice(
                EVENT_NAMES
            ),

        "cover":
            get_random_cover_image(),

        "month":
            event_date["month"],

        "day":
            event_date["day"],

        "date_text":
            event_date["date_text"],

        "time":
            event_date["time"],

        "location":
            random.choice(
                LOCATIONS
            ),

        "interested":
            random.randint(
                10,
                2500,
            ),

        "going":
            random.randint(
                4,
                900,
            ),

        "category":
            random.choice(
                EVENT_CATEGORIES
            )["name"],

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "invited":
            random.random() < 0.28,
    }


# ==========================================================
# Collections
# ==========================================================

def generate_upcoming_events(
    count: int = 10,
) -> list[dict]:

    return [
        generate_event(
            index=index,
            future=True,
        )
        for index in range(count)
    ]


def generate_past_events(
    count: int = 6,
) -> list[dict]:

    return [
        generate_event(
            index=index,
            future=False,
        )
        for index in range(count)
    ]


# ==========================================================
# Invite People
# ==========================================================

def generate_invite_person(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "selected":
            random.random() < 0.3,
    }


def generate_invite_people(
    count: int = 8,
) -> list[dict]:

    return [
        generate_invite_person(index)
        for index in range(count)
    ]


# ==========================================================
# Navigation
# ==========================================================

def generate_event_navigation() -> list[dict]:

    return [
        {
            "name": "Home",
            "icon": "event",
        },
        {
            "name": "Your events",
            "icon": "calendar_month",
        },
        {
            "name": "Birthdays",
            "icon": "cake",
        },
        {
            "name": "Notifications",
            "icon": "notifications",
        },
        {
            "name": "Create event",
            "icon": "add_circle",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_event_state(
    event_count: int,
) -> dict:

    name = random.choice(
        EVENT_STATES
    )

    selected_event = None

    if name in {
        "event_preview",
        "event_menu_open",
        "invite_people",
    }:

        selected_event = random.randint(
            0,
            max(
                0,
                min(
                    event_count - 1,
                    6,
                )
            ),
        )

    query = ""

    if name == "search_active":

        query = random.choice(
            [
                "music",
                "food",
                "tech",
                "art",
                "sports",
            ]
        )

    return {
        "name":
            name,

        "selected_event":
            selected_event,

        "query":
            query,
    }


# ==========================================================
# Complete Data
# ==========================================================

def generate_events_data() -> dict:

    upcoming = generate_upcoming_events(
        count=random.randint(
            8,
            14,
        )
    )

    past = generate_past_events(
        count=random.randint(
            4,
            8,
        )
    )

    invited = [
        event
        for event in upcoming
        if event["invited"]
    ]

    if not invited:

        upcoming[0]["invited"] = True
        invited = [
            upcoming[0]
        ]

    return {
        "navigation":
            generate_event_navigation(),

        "categories":
            EVENT_CATEGORIES,

        "upcoming":
            upcoming,

        "past":
            past,

        "invited":
            invited,

        "invite_people":
            generate_invite_people(
                count=random.randint(
                    6,
                    10,
                )
            ),

        "state":
            generate_event_state(
                event_count=len(
                    upcoming
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_events_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK EVENTS GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Upcoming:",
        len(
            data["upcoming"]
        ),
    )

    print(
        "Past:",
        len(
            data["past"]
        ),
    )

    print(
        "Invited:",
        len(
            data["invited"]
        ),
    )

    print(
        "State:",
        data["state"],
    )