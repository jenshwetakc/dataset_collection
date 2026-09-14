from __future__ import annotations

import random

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_driver_image,
    get_random_vehicle_image,
)


fake = Faker()


DRIVER_STATUSES = [
    "Driver is on the way",
    "Driver is arriving",
    "Your ride is nearby",
    "Driver is heading to pickup",
]


CAR_MODELS = [
    "Toyota Camry",
    "Hyundai Sonata",
    "Honda Accord",
    "Kia K5",
    "Tesla Model 3",
    "Toyota Prius",
    "Hyundai Ioniq",
]


CAR_COLORS = [
    "Black",
    "White",
    "Silver",
    "Gray",
    "Blue",
]


SAFETY_ACTIONS = [
    {
        "label": "Safety",
        "icon": "shield",
    },
    {
        "label": "Share trip",
        "icon": "ios_share",
    },
    {
        "label": "Help",
        "icon": "help",
    },
]


def generate_address() -> str:

    return (
        f"{fake.street_address()}, "
        f"{fake.city()}"
    )


def generate_driver() -> dict:

    rating = round(
        random.uniform(
            4.75,
            5.0,
        ),
        2,
    )

    return {
        "name":
            fake.first_name(),

        "rating":
            rating,

        "trips":
            random.randint(
                350,
                5800,
            ),

        "image":
            get_random_driver_image(),
    }


def generate_vehicle() -> dict:

    return {
        "model":
            random.choice(
                CAR_MODELS
            ),

        "color":
            random.choice(
                CAR_COLORS
            ),

        "plate":
            (
                f"{random.randint(10, 99)}"
                f"{random.choice(['A', 'B', 'C', 'D'])}"
                f"{random.randint(1000, 9999)}"
            ),

        "image":
            get_random_vehicle_image(),
    }


def generate_route_points() -> list[dict]:

    pickup = {
        "x":
            random.randint(
                58,
                76,
            ),

        "y":
            random.randint(
                54,
                74,
            ),
    }

    driver = {
        "x":
            random.randint(
                24,
                42,
            ),

        "y":
            random.randint(
                22,
                40,
            ),
    }

    midpoint_1 = {
        "x":
            random.randint(
                36,
                48,
            ),

        "y":
            random.randint(
                34,
                46,
            ),
    }

    midpoint_2 = {
        "x":
            random.randint(
                48,
                60,
            ),

        "y":
            random.randint(
                42,
                58,
            ),
    }

    return [
        driver,
        midpoint_1,
        midpoint_2,
        pickup,
    ]


def create_points_string(
    points: list[dict],
) -> str:

    return " ".join(
        f"{point['x']},{point['y']}"
        for point in points
    )


def generate_trip_tracking_data() -> dict:

    eta_minutes = random.randint(
        2,
        8,
    )

    driver = generate_driver()
    vehicle = generate_vehicle()

    route_points = generate_route_points()

    driver_point = route_points[0]
    pickup_point = route_points[-1]

    return {

        "status":
            random.choice(
                DRIVER_STATUSES
            ),

        "eta_minutes":
            eta_minutes,

        "eta_text":
            f"{eta_minutes} min",

        "arrival_text":
            f"Arriving in {eta_minutes} min",

        "pickup": {
            "label":
                "Pickup",
            "name":
                random.choice(
                    [
                        "Main entrance",
                        "Front gate",
                        "Pickup zone",
                        "Current location",
                    ]
                ),
            "address":
                generate_address(),
        },

        "destination": {
            "label":
                "Destination",
            "name":
                fake.company(),
            "address":
                generate_address(),
        },

        "driver":
            driver,

        "vehicle":
            vehicle,

        "contact_actions": [
            {
                "label":
                    "Message",
                "icon":
                    "chat",
            },
            {
                "label":
                    "Call",
                "icon":
                    "call",
            },
        ],

        "safety_actions":
            SAFETY_ACTIONS,

        "trip_progress": {
            "value":
                random.randint(
                    25,
                    65,
                ),
        },

        "map": {
            "driver":
                driver_point,

            "pickup":
                pickup_point,

            "route_points":
                route_points,

            "route_points_string":
                create_points_string(
                    route_points
                ),

            "nearby_cars": [
                {
                    "x":
                        random.randint(
                            12,
                            88,
                        ),
                    "y":
                        random.randint(
                            12,
                            82,
                        ),
                }
                for _ in range(
                    random.randint(
                        2,
                        5,
                    )
                )
            ],
        },
    }


if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_trip_tracking_data()
    )