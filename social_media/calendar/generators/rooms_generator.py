from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


ROOM_BOOKING_STATES = [
    "available_rooms",
    "room_schedule",
    "favorites",
    "search_results",
    "map_view",
    "no_results",
    "booking_details_dialog",
    "create_booking_dialog",
    "booking_conflict_dialog",
    "room_details_dialog",
    "mobile_filter_sheet",
]


BUILDINGS = [
    "Innovation Center",
    "Research Hall",
    "Main Office",
    "Library Annex",
]


ROOM_NAMES = [
    "Orion",
    "Atlas",
    "Aurora",
    "Nova",
    "Willow",
    "Maple",
    "Summit",
    "Horizon",
]


ROOM_FEATURES = [
    {
        "icon": "videocam",
        "label": "Video conferencing",
    },
    {
        "icon": "tv",
        "label": "Display",
    },
    {
        "icon": "draw",
        "label": "Whiteboard",
    },
    {
        "icon": "volume_up",
        "label": "Speakers",
    },
    {
        "icon": "accessible",
        "label": "Accessible",
    },
]


def generate_time_slots() -> list[dict]:
    slots = []

    start_hour = 8

    for index in range(10):
        hour = start_hour + index

        available = random.random() < 0.65

        slots.append({
            "id": f"slot-{index}",
            "time": (
                datetime.now()
                .replace(
                    hour=hour,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                .strftime("%I:%M %p")
            ),
            "available": available,
            "label": (
                "Available"
                if available
                else "Booked"
            ),
        })

    return slots


def generate_room(
    index: int,
) -> dict:
    feature_count = random.randint(
        2,
        len(ROOM_FEATURES),
    )

    building = random.choice(
        BUILDINGS
    )

    floor = random.randint(
        1,
        8,
    )

    capacity = random.choice([
        4,
        6,
        8,
        10,
        12,
        16,
        20,
        30,
    ])

    return {
        "id": f"room-{index}",

        "name":
            random.choice(
                ROOM_NAMES
            ),

        "building":
            building,

        "floor":
            floor,

        "location": (
            f"{building}, Floor {floor}"
        ),

        "capacity":
            capacity,

        "available":
            random.random() < 0.72,

        "available_until":
            random.choice([
                "11:00 AM",
                "12:30 PM",
                "2:00 PM",
                "4:30 PM",
                "All day",
            ]),

        "favorite":
            random.random() < 0.35,

        "features":
            random.sample(
                ROOM_FEATURES,
                k=feature_count,
            ),

        "time_slots":
            generate_time_slots(),

        "description": (
            "A comfortable meeting room with modern "
            "presentation and collaboration equipment."
        ),
    }


def generate_bookings(
    room: dict,
) -> list[dict]:
    titles = [
        "Weekly team sync",
        "Research meeting",
        "Design review",
        "Client presentation",
        "Planning session",
    ]

    organizers = [
        "Mina Park",
        "Alex Morgan",
        "Jordan Lee",
        "Taylor Kim",
    ]

    bookings = []

    for index in range(
        random.randint(3, 6)
    ):
        start_hour = random.randint(
            8,
            16,
        )

        bookings.append({
            "id": f"booking-{index}",

            "title":
                random.choice(
                    titles
                ),

            "organizer":
                random.choice(
                    organizers
                ),

            "start":
                f"{start_hour:02d}:00",

            "end":
                f"{start_hour + 1:02d}:00",

            "room_name":
                room["name"],
        })

    return sorted(
        bookings,
        key=lambda booking: booking["start"],
    )


def generate_rooms_data(
    state: str | None = None,
) -> dict:
    if state is None:
        state = random.choice(
            ROOM_BOOKING_STATES
        )

    if state not in ROOM_BOOKING_STATES:
        raise ValueError(
            f"Unknown room booking state: {state}. "
            f"Available states: {ROOM_BOOKING_STATES}"
        )

    rooms = [
        generate_room(index)
        for index in range(
            1,
            random.randint(7, 11),
        )
    ]

    if state == "favorites":
        for index, room in enumerate(
            rooms
        ):
            room["favorite"] = (
                index < 4
            )

        rooms = [
            room
            for room in rooms
            if room["favorite"]
        ]

    if state == "search_results":
        for room in rooms:
            room["building"] = (
                "Research Hall"
            )
            room["location"] = (
                f"Research Hall, "
                f"Floor {room['floor']}"
            )

    if state == "no_results":
        rooms = []

    selected_room = (
        rooms[0]
        if rooms
        else generate_room(999)
    )

    selected_room["available"] = True

    popup_states = {
        "booking_details_dialog",
        "create_booking_dialog",
        "booking_conflict_dialog",
        "room_details_dialog",
        "mobile_filter_sheet",
    }

    selected_date = (
        datetime.now()
        + timedelta(
            days=random.randint(0, 7)
        )
    )

    return {
        "app_name":
            "Calendar Rooms",

        "state":
            state,

        "popup_open":
            state in popup_states,

        "page_title":
            "Rooms & resources",

        "search_query": (
            "Research Hall"
            if state == "search_results"
            else ""
        ),

        "profile": {
            "initials":
                random.choice([
                    "SK",
                    "AM",
                    "JL",
                ]),
        },

        "selected_date":
            selected_date.strftime(
                "%A, %B %d"
            ),

        "selected_room":
            selected_room,

        "rooms":
            rooms,

        "bookings":
            generate_bookings(
                selected_room
            ),

        "filters": [
            {
                "id": "available_now",
                "label": "Available now",
                "icon": "schedule",
                "selected": True,
            },
            {
                "id": "capacity",
                "label": "8+ people",
                "icon": "group",
                "selected": False,
            },
            {
                "id": "video",
                "label": "Video conferencing",
                "icon": "videocam",
                "selected": False,
            },
            {
                "id": "accessible",
                "label": "Accessible",
                "icon": "accessible",
                "selected": False,
            },
        ],

        "navigation": [
            {
                "id": "available_rooms",
                "label": "Find a room",
                "icon": "meeting_room",
            },
            {
                "id": "room_schedule",
                "label": "Room schedules",
                "icon": "calendar_view_day",
            },
            {
                "id": "favorites",
                "label": "Favorites",
                "icon": "star",
            },
            {
                "id": "map_view",
                "label": "Map",
                "icon": "map",
            },
        ],
    }


if __name__ == "__main__":
    import pprint

    pprint.pp(
        generate_rooms_data()
    )