from __future__ import annotations

import random

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_vehicle_image,
)


fake = Faker()


# ==========================================================
# Ride Catalog
# ==========================================================

RIDE_TYPES = [
    {
        "name": "UberX",
        "description": "Affordable everyday rides",
        "seats": 4,
        "base_price": 14.0,
    },
    {
        "name": "Comfort",
        "description": "Newer cars with extra legroom",
        "seats": 4,
        "base_price": 18.0,
    },
    {
        "name": "UberXL",
        "description": "Affordable rides for groups",
        "seats": 6,
        "base_price": 24.0,
    },
    {
        "name": "Green",
        "description": "Low-emission rides",
        "seats": 4,
        "base_price": 16.0,
    },
    {
        "name": "Premier",
        "description": "Premium rides in luxury cars",
        "seats": 4,
        "base_price": 29.0,
    },
    {
        "name": "Taxi",
        "description": "Metered city taxi ride",
        "seats": 4,
        "base_price": 17.0,
    },
    {
        "name": "Black",
        "description": "High-end professional service",
        "seats": 4,
        "base_price": 36.0,
    },
]


BADGES = [
    "Recommended",
    "Fastest",
    "Low price",
    "Eco",
    "Popular",
    None,
    None,
]


CARD_TYPES = [
    "Visa",
    "Mastercard",
    "Debit card",
    "Business card",
]

PLACE_TYPES = [
    "Airport",
    "Station",
    "Mall",
    "Office",
    "Restaurant",
    "Hotel",
    "University",
    "Hospital",
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    value: float,
) -> str:

    return f"${value:.2f}"


def generate_address() -> str:

    return (
        f"{fake.street_address()}, "
        f"{fake.city()}"
    )


def generate_place_name() -> str:

    place_type = random.choice(
        PLACE_TYPES
    )

    if random.random() < 0.5:
        return fake.company()

    return f"{fake.city()} {place_type}"


def generate_map_marker(
    kind: str,
    x: int,
    y: int,
) -> dict:

    icon_lookup = {
        "pickup": "radio_button_checked",
        "destination": "location_on",
        "vehicle": "directions_car",
    }

    return {
        "kind": kind,
        "x": x,
        "y": y,
        "icon": icon_lookup.get(
            kind,
            "location_on",
        ),
    }


def build_route_points(
    pickup_x: int,
    pickup_y: int,
    destination_x: int,
    destination_y: int,
) -> list[dict]:

    midpoint_x = (
        pickup_x + destination_x
    ) / 2

    midpoint_y = (
        pickup_y + destination_y
    ) / 2

    control_1_x = int(
        midpoint_x + random.randint(-10, 10)
    )
    control_1_y = int(
        pickup_y + random.randint(5, 18)
    )

    control_2_x = int(
        midpoint_x + random.randint(-8, 12)
    )
    control_2_y = int(
        destination_y - random.randint(6, 18)
    )

    return [
        {
            "x": pickup_x,
            "y": pickup_y,
        },
        {
            "x": control_1_x,
            "y": control_1_y,
        },
        {
            "x": control_2_x,
            "y": control_2_y,
        },
        {
            "x": destination_x,
            "y": destination_y,
        },
    ]


def create_points_string(
    points: list[dict],
) -> str:

    return " ".join(
        f"{point['x']},{point['y']}"
        for point in points
    )


# ==========================================================
# Ride Option
# ==========================================================

def generate_ride_option(
    ride_spec: dict,
    selected: bool,
) -> dict:

    eta_minutes = random.randint(
        2,
        12,
    )

    price_multiplier = random.uniform(
        0.95,
        1.35,
    )

    raw_price = (
        ride_spec["base_price"]
        * price_multiplier
    )

    has_old_price = random.random() < 0.25
    old_price = None

    if has_old_price:
        old_price = raw_price + random.uniform(
            1.5,
            5.5,
        )

    badge = random.choice(
        BADGES
    )

    if ride_spec["name"] == "Green" and badge is None:
        badge = "Eco"

    if selected and badge is None:
        badge = random.choice(
            [
                "Recommended",
                "Fastest",
                "Popular",
            ]
        )

    return {
        "name":
            ride_spec["name"],

        "description":
            ride_spec["description"],

        "seats":
            ride_spec["seats"],

        "eta_minutes":
            eta_minutes,

        "eta_text":
            f"{eta_minutes} min away",

        "arrival_text":
            f"Pickup in {eta_minutes} min",

        "price_value":
            round(
                raw_price,
                2,
            ),

        "price_text":
            format_price(
                raw_price
            ),

        "old_price_text":
            (
                format_price(old_price)
                if old_price is not None
                else None
            ),

        "badge":
            badge,

        "selected":
            selected,

        "image":
            get_random_vehicle_image(),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_ride_options_data() -> dict:

    ride_count = random.randint(
        4,
        6,
    )

    selected_catalog = random.sample(
        RIDE_TYPES,
        k=ride_count,
    )

    selected_index = random.randint(
        0,
        ride_count - 1,
    )

    rides = []

    for index, ride_spec in enumerate(
        selected_catalog
    ):
        rides.append(
            generate_ride_option(
                ride_spec=ride_spec,
                selected=(
                    index
                    == selected_index
                ),
            )
        )

    selected_ride = rides[
        selected_index
    ]

    pickup_name = random.choice(
        [
            "Current location",
            "Pickup spot",
            "Nearby pickup point",
        ]
    )

    destination_name = generate_place_name()

    pickup_x = random.randint(
        28,
        42,
    )
    pickup_y = random.randint(
        24,
        36,
    )

    destination_x = random.randint(
        58,
        76,
    )
    destination_y = random.randint(
        54,
        74,
    )

    route_points = build_route_points(
        pickup_x=pickup_x,
        pickup_y=pickup_y,
        destination_x=destination_x,
        destination_y=destination_y,
    )

    vehicle_markers = []

    for _ in range(
        random.randint(2, 4)
    ):
        vehicle_markers.append(
            generate_map_marker(
                kind="vehicle",
                x=random.randint(15, 88),
                y=random.randint(16, 82),
            )
        )

    return {

        # --------------------------------------------------
        # App Bar
        # --------------------------------------------------

        "title":
            "Choose a ride",


        # --------------------------------------------------
        # Route
        # --------------------------------------------------

        "pickup": {
            "name":
                pickup_name,
            "address":
                generate_address(),
            "icon":
                "radio_button_checked",
        },

        "destination": {
            "name":
                destination_name,
            "address":
                generate_address(),
            "icon":
                "location_on",
        },

        "trip_meta": {
            "distance":
                f"{random.uniform(3.2, 18.7):.1f} km",
            "duration":
                f"{random.randint(12, 38)} min",
        },


        # --------------------------------------------------
        # Map
        # --------------------------------------------------

        "map": {
            "pickup_marker":
                generate_map_marker(
                    kind="pickup",
                    x=pickup_x,
                    y=pickup_y,
                ),

            "destination_marker":
                generate_map_marker(
                    kind="destination",
                    x=destination_x,
                    y=destination_y,
                ),

            "vehicle_markers":
                vehicle_markers,

            "route_points":
                route_points,

            "route_points_string":
                create_points_string(
                    route_points
                ),
        },


        # --------------------------------------------------
        # Rides
        # --------------------------------------------------

        "rides":
            rides,

        "selected_ride_name":
            selected_ride["name"],


        # --------------------------------------------------
        # Payment
        # --------------------------------------------------

        "payment": {
            "method":
                random.choice(
                    CARD_TYPES
                ),
            "last_four":
                f"{random.randint(1000, 9999)}",
        },


        # --------------------------------------------------
        # CTA
        # --------------------------------------------------

        "confirm_text":
            f"Choose {selected_ride['name']}",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_ride_options_data()
    )