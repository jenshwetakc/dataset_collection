from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_vehicle_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_address() -> str:

    return (
        f"{fake.street_address()}, "
        f"{fake.city()}"
    )


def generate_dates() -> list[dict]:

    today = datetime.now()

    dates = []

    selected_index = random.randint(
        0,
        3,
    )


    for index in range(7):

        date = (
            today
            + timedelta(
                days=index
            )
        )

        dates.append(
            {
                "day":
                    date.strftime("%a"),

                "date":
                    date.strftime("%d"),

                "month":
                    date.strftime("%b"),

                "selected":
                    index == selected_index,
            }
        )


    return dates


def generate_times() -> list[dict]:

    start_hour = random.randint(
        7,
        15,
    )

    selected_index = random.randint(
        0,
        4,
    )

    times = []


    for index in range(8):

        total_minutes = (
            start_hour * 60
            + index * 30
        )

        hour = (
            total_minutes // 60
        )

        minute = (
            total_minutes % 60
        )


        times.append(
            {
                "label":
                    f"{hour:02d}:{minute:02d}",

                "selected":
                    index == selected_index,
            }
        )


    return times


def generate_benefits() -> list[dict]:

    return [
        {
            "icon":
                "schedule",

            "title":
                "Pickup protection",

            "subtitle":
                "Extra wait time included",
        },
        {
            "icon":
                "event_available",

            "title":
                "Reserve in advance",

            "subtitle":
                "Plan your ride ahead of time",
        },
        {
            "icon":
                "cancel",

            "title":
                "Flexible cancellation",

            "subtitle":
                "Cancel before your pickup window",
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_reserve_ride_data() -> dict:

    base_fare = random.uniform(
        18,
        42,
    )

    high_fare = (
        base_fare
        + random.uniform(
            5,
            16,
        )
    )


    return {

        "title":
            "Reserve a ride",

        "subtitle":
            "Schedule your trip in advance",

        "pickup": {

            "label":
                "Pickup",

            "value":
                random.choice(
                    [
                        "Current location",
                        "Home",
                        "Work",
                    ]
                ),

            "address":
                generate_address(),

            "icon":
                "radio_button_checked",
        },

        "destination": {

            "label":
                "Destination",

            "value":
                random.choice(
                    [
                        fake.company(),
                        f"{fake.city()} Station",
                        f"{fake.city()} Airport",
                        f"{fake.city()} Hotel",
                    ]
                ),

            "address":
                generate_address(),

            "icon":
                "location_on",
        },

        "dates":
            generate_dates(),

        "times":
            generate_times(),

        "reserve_option": {

            "name":
                random.choice(
                    [
                        "UberX Reserve",
                        "Comfort Reserve",
                        "Uber Green Reserve",
                    ]
                ),

            "vehicle_image":
                get_random_vehicle_image(),

            "capacity":
                random.choice(
                    [
                        "4 seats",
                        "4 passengers",
                        "Up to 4 riders",
                    ]
                ),

            "fare":
                (
                    f"${base_fare:.0f}"
                    f"–"
                    f"${high_fare:.0f}"
                ),

            "badge":
                random.choice(
                    [
                        "Recommended",
                        "Reserve",
                        None,
                    ]
                ),
        },

        "benefits":
            generate_benefits(),

        "payment": {

            "label":
                "Payment method",

            "method":
                random.choice(
                    [
                        "Visa •••• 4281",
                        "Mastercard •••• 8024",
                        "Uber Cash",
                        "Personal",
                    ]
                ),

            "icon":
                "credit_card",
        },

        "note":
            random.choice(
                [
                    "Your driver may arrive up to 15 minutes before pickup.",
                    "You'll receive trip reminders before your scheduled ride.",
                    "Reserve availability may vary by pickup location.",
                ]
            ),

        "primary_action":
            random.choice(
                [
                    "Schedule UberX",
                    "Reserve ride",
                    "Confirm reservation",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_reserve_ride_data()
    )