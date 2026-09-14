from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_vehicle_image,
)


fake = Faker()


# ==========================================================
# Ride Statuses
# ==========================================================

RIDE_STATUSES = [
    "Completed",
    "Completed",
    "Completed",
    "Canceled",
]


RIDE_TYPES = [
    "UberX",
    "Comfort",
    "UberXL",
    "Green",
    "Premier",
    "Taxi",
    "Black",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_address() -> str:

    return (
        f"{fake.street_address()}, "
        f"{fake.city()}"
    )


def generate_trip_datetime() -> datetime:

    days_ago = random.randint(
        1,
        120,
    )

    hour = random.randint(
        6,
        23,
    )

    minute = random.randint(
        0,
        59,
    )

    return (
        datetime.now()
        - timedelta(
            days=days_ago,
        )
    ).replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )


def format_trip_date(
    value: datetime,
) -> str:

    return value.strftime(
        "%b %d"
    )


def format_trip_time(
    value: datetime,
) -> str:

    return value.strftime(
        "%I:%M %p"
    ).lstrip(
        "0"
    )


# ==========================================================
# Trip Generator
# ==========================================================

def generate_trip(
    index: int,
) -> dict:

    trip_datetime = (
        generate_trip_datetime()
    )

    status = random.choice(
        RIDE_STATUSES
    )

    ride_type = random.choice(
        RIDE_TYPES
    )

    duration_minutes = random.randint(
        8,
        52,
    )

    distance_km = round(
        random.uniform(
            2.1,
            28.0,
        ),
        1,
    )

    price = round(
        random.uniform(
            8.0,
            72.0,
        ),
        2,
    )

    if status == "Canceled":

        price = random.choice(
            [
                0.0,
                round(
                    random.uniform(
                        3.0,
                        8.0,
                    ),
                    2,
                ),
            ]
        )

    return {

        "id":
            index,

        "ride_type":
            ride_type,

        "status":
            status,

        "date":
            format_trip_date(
                trip_datetime
            ),

        "time":
            format_trip_time(
                trip_datetime
            ),

        "timestamp":
            f"{format_trip_date(trip_datetime)}, "
            f"{format_trip_time(trip_datetime)}",

        "pickup": {
            "name":
                random.choice(
                    [
                        "Pickup location",
                        "Main entrance",
                        "Current location",
                        fake.company(),
                    ]
                ),

            "address":
                generate_address(),
        },

        "destination": {
            "name":
                fake.company(),

            "address":
                generate_address(),
        },

        "duration":
            f"{duration_minutes} min",

        "distance":
            f"{distance_km:.1f} km",

        "price":
            f"${price:.2f}",

        "vehicle_image":
            get_random_vehicle_image(),

        "rating":
            (
                random.randint(
                    3,
                    5,
                )
                if (
                    status
                    == "Completed"
                    and random.random()
                    < 0.65
                )
                else None
            ),

        "has_receipt":
            status
            == "Completed",

        "has_issue":
            random.random()
            < 0.18,
    }


# ==========================================================
# Upcoming Trip
# ==========================================================

def generate_upcoming_trip() -> dict:

    future = (
        datetime.now()
        + timedelta(
            days=random.randint(
                1,
                10,
            ),
            hours=random.randint(
                1,
                12,
            ),
        )
    )

    return {

        "ride_type":
            random.choice(
                [
                    "UberX",
                    "Comfort",
                    "UberXL",
                ]
            ),

        "date":
            future.strftime(
                "%b %d"
            ),

        "time":
            future.strftime(
                "%I:%M %p"
            ).lstrip(
                "0"
            ),

        "pickup": {
            "name":
                "Scheduled pickup",

            "address":
                generate_address(),
        },

        "destination": {
            "name":
                fake.company(),

            "address":
                generate_address(),
        },

        "vehicle_image":
            get_random_vehicle_image(),
    }


# ==========================================================
# Activity Generator
# ==========================================================

def generate_activity_data() -> dict:

    trip_count = random.randint(
        8,
        14,
    )

    upcoming_count = random.choice(
        [
            0,
            0,
            1,
            2,
        ]
    )

    trips = [

        generate_trip(
            index
        )

        for index
        in range(
            trip_count
        )
    ]

    upcoming = [

        generate_upcoming_trip()

        for _ in range(
            upcoming_count
        )
    ]

    return {

        "title":
            "Activity",

        "tabs": [
            {
                "label":
                    "Past",
                "selected":
                    True,
            },
            {
                "label":
                    "Upcoming",
                "selected":
                    False,
            },
        ],

        "trip_count":
            trip_count,

        "trips":
            trips,

        "upcoming":
            upcoming,

        "navigation": [
            {
                "label":
                    "Home",
                "icon":
                    "home",
                "selected":
                    False,
            },
            {
                "label":
                    "Activity",
                "icon":
                    "receipt_long",
                "selected":
                    True,
            },
            {
                "label":
                    "Account",
                "icon":
                    "person",
                "selected":
                    False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_activity_data()
    )