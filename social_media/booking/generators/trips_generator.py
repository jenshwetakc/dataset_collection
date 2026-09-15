from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_hotel_image,
)


# ==========================================================
# States
# ==========================================================

TRIP_STATES = [
    "upcoming",
    "past",
    "cancelled",
    "empty",
    "trip_detail",
    "support_open",
]


HOTEL_NAMES = [
    "Grand Central Hotel",
    "Skyline Residence",
    "Riverside Boutique Hotel",
    "Royal Park Suites",
    "Urban Stay Seoul",
    "Harbor View Hotel",
    "The Metropolitan",
    "Ocean View Resort",
]


CITIES = [
    "Seoul",
    "Tokyo",
    "Paris",
    "London",
    "Bangkok",
    "Singapore",
    "Rome",
]


ROOM_TYPES = [
    "Standard Double Room",
    "Deluxe King Room",
    "Superior Twin Room",
    "Family Suite",
    "City View Room",
]


# ==========================================================
# Trip
# ==========================================================

def generate_trip(
    *,
    status: str,
) -> dict:

    city = random.choice(
        CITIES
    )

    nights = random.randint(
        2,
        5,
    )

    return {
        "hotel_name":
            random.choice(
                HOTEL_NAMES
            ),

        "city":
            city,

        "image":
            get_random_hotel_image(),

        "room":
            random.choice(
                ROOM_TYPES
            ),

        "status":
            status,

        "check_in":
            random.choice(
                [
                    "Sep 18",
                    "Oct 03",
                    "Oct 14",
                    "Nov 02",
                ]
            ),

        "check_out":
            random.choice(
                [
                    "Sep 21",
                    "Oct 06",
                    "Oct 18",
                    "Nov 06",
                ]
            ),

        "nights":
            nights,

        "guests":
            random.choice(
                [
                    "1 adult",
                    "2 adults",
                    "2 adults · 1 child",
                    "3 adults",
                ]
            ),

        "confirmation":
            f"BK{random.randint(100000, 999999)}",

        "price":
            random.randint(
                180,
                920,
            ),

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),

        "free_cancel":
            (
                status == "upcoming"
                and random.random() < 0.60
            ),

        "reviewed":
            (
                status == "past"
                and random.random() < 0.35
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_trips_data() -> dict:

    state = random.choice(
        TRIP_STATES
    )

    empty = (
        state == "empty"
    )

    detail_open = (
        state == "trip_detail"
    )

    support_open = (
        state == "support_open"
    )

    if state in {
        "upcoming",
        "trip_detail",
        "support_open",
    }:

        trip_status = "upcoming"

    elif state == "past":

        trip_status = "past"

    elif state == "cancelled":

        trip_status = "cancelled"

    else:

        trip_status = "upcoming"


    trip_count = (
        0
        if empty
        else random.randint(
            2,
            5,
        )
    )


    trips = [
        generate_trip(
            status=trip_status
        )
        for _ in range(
            trip_count
        )
    ]


    selected_trip = (
        random.choice(
            trips
        )
        if trips
        else None
    )


    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "empty":
            empty,

        "detail_open":
            detail_open,

        "support_open":
            support_open,

        # ------------------------------------------
        # Header
        # ------------------------------------------

        "title":
            "Trips",

        "subtitle":
            random.choice(
                [
                    "Manage your bookings and travel plans.",
                    "Everything you need for your upcoming stays.",
                    "Your reservations in one place.",
                ]
            ),

        # ------------------------------------------
        # Filters
        # ------------------------------------------

        "tabs": [
            {
                "label":
                    "Upcoming",

                "active":
                    trip_status == "upcoming",
            },
            {
                "label":
                    "Past",

                "active":
                    trip_status == "past",
            },
            {
                "label":
                    "Cancelled",

                "active":
                    trip_status == "cancelled",
            },
        ],

        # ------------------------------------------
        # Trips
        # ------------------------------------------

        "trips":
            trips,

        "selected_trip":
            selected_trip,

        # ------------------------------------------
        # Empty
        # ------------------------------------------

        "empty_title":
            "No trips here yet",

        "empty_text":
            (
                "When you book a stay, your reservation "
                "will appear here."
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_trips_data()
    )

    print(
        "\n=============================="
    )

    print(
        "BOOKING TRIPS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Trips:",
        len(
            data["trips"]
        ),
    )