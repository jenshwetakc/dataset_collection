from __future__ import annotations

import random
import math
from faker import Faker

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_parks,
    generate_roads,
    generate_water,
)


fake = Faker()


# ==========================================================
# Travel Modes
# ==========================================================

TRAVEL_MODES = [
    {
        "key": "driving",
        "label": "Drive",
        "icon": "directions_car",
    },
    {
        "key": "transit",
        "label": "Transit",
        "icon": "directions_transit",
    },
    {
        "key": "walking",
        "label": "Walk",
        "icon": "directions_walk",
    },
    {
        "key": "cycling",
        "label": "Bike",
        "icon": "directions_bike",
    },
]


# ==========================================================
# Address Generator
# ==========================================================

def generate_location_name() -> str:

    options = [
        fake.street_address(),
        fake.company(),
        fake.city(),
        fake.street_name(),
    ]

    return random.choice(
        options
    )


# ==========================================================
# Route Point Generator
# ==========================================================

def generate_route_points(
    count: int | None = None,
) -> list[dict]:

    if count is None:
        count = random.randint(
            5,
            9,
        )

    start_x = random.randint(
        15,
        30,
    )

    start_y = random.randint(
        65,
        82,
    )

    end_x = random.randint(
        68,
        88,
    )

    end_y = random.randint(
        18,
        38,
    )

    points = []

    for index in range(
        count
    ):

        ratio = (
            index
            / max(
                count - 1,
                1,
            )
        )

        x = (
            start_x
            + (
                end_x
                - start_x
            )
            * ratio
            + random.uniform(
                -5,
                5,
            )
        )

        y = (
            start_y
            + (
                end_y
                - start_y
            )
            * ratio
            + random.uniform(
                -5,
                5,
            )
        )

        points.append(
            {
                "x": round(
                    max(
                        5,
                        min(
                            95,
                            x,
                        ),
                    ),
                    2,
                ),
                "y": round(
                    max(
                        5,
                        min(
                            95,
                            y,
                        ),
                    ),
                    2,
                ),
            }
        )

    points[0] = {
        "x": start_x,
        "y": start_y,
    }

    points[-1] = {
        "x": end_x,
        "y": end_y,
    }

    return points


# ==========================================================
# Route Alternatives
# ==========================================================

def generate_route_option(
    index: int,
    selected: bool = False,
) -> dict:

    duration_minutes = random.randint(
        8,
        55,
    )

    distance = round(
        random.uniform(
            1.2,
            22.0,
        ),
        1,
    )

    points = (
        generate_route_points()
    )

    return {

        "id":
            index,

        "selected":
            selected,

        "duration":
            f"{duration_minutes} min",

        "distance":
            f"{distance} mi",

        "arrival":
            (
                f"{random.randint(1, 11)}:"
                f"{random.choice(['00', '10', '20', '30', '40', '50'])} "
                f"{random.choice(['AM', 'PM'])}"
            ),

        "via":
            random.choice(
                [
                    "via Main St",
                    "via Highway 1",
                    "via Central Ave",
                    "via Riverside Rd",
                    "via City Center",
                    "via Expressway",
                ]
            ),

        "traffic":
            random.choice(
                [
                    "Typical traffic",
                    "Light traffic",
                    "Moderate traffic",
                    "Heavy traffic",
                ]
            ),

        "toll":
            random.random()
            < 0.20,

        "fastest":
            selected
            and random.random()
            < 0.75,

        "points":
            points,

        "segments":
            build_route_segments(
                points
            ),
    }

# ==========================================================
# Directions Data
# ==========================================================

def generate_directions_data() -> dict:

    origin = random.choice(
        [
            "Your location",
            generate_location_name(),
        ]
    )

    destination = generate_location_name()

    selected_mode = random.choice(
        TRAVEL_MODES
    )

    route_count = random.randint(
        2,
        3,
    )

    routes = [
        generate_route_option(
            index=index,
            selected=(
                index == 0
            ),
        )
        for index
        in range(
            route_count
        )
    ]

    return {
        "origin":
            origin,

        "destination":
            destination,

        "travel_modes":
            [
                {
                    **mode,
                    "selected":
                        mode["key"]
                        == selected_mode["key"],
                }
                for mode
                in TRAVEL_MODES
            ],

        "selected_mode":
            selected_mode["key"],

        "routes":
            routes,

        "selected_route":
            routes[0],

        "map":
            {
                "roads":
                    generate_roads(
                        count=random.randint(
                            18,
                            28,
                        )
                    ),

                "buildings":
                    generate_buildings(
                        count=random.randint(
                            28,
                            50,
                        )
                    ),

                "parks":
                    generate_parks(),

                "water":
                    generate_water(),

                "labels":
                    generate_map_labels(
                        count=random.randint(
                            8,
                            14,
                        )
                    ),
            },

        "avoid_options":
            random.sample(
                [
                    "Tolls",
                    "Highways",
                    "Ferries",
                ],
                k=random.randint(
                    0,
                    2,
                ),
            ),

        "navigation_message":
            random.choice(
                [
                    "Fastest route now",
                    "Best route based on current traffic",
                    "Similar ETA on alternate routes",
                ]
            ),
    }



def build_route_segments(
    points: list[dict],
) -> list[dict]:

    segments = []

    for index in range(
        len(points) - 1
    ):

        start = points[index]
        end = points[index + 1]

        dx = (
            end["x"]
            - start["x"]
        )

        dy = (
            end["y"]
            - start["y"]
        )

        length = math.sqrt(
            dx * dx
            + dy * dy
        )

        angle = math.degrees(
            math.atan2(
                dy,
                dx,
            )
        )

        segments.append(
            {
                "x":
                    start["x"],

                "y":
                    start["y"],

                "length":
                    round(
                        length,
                        2,
                    ),

                "angle":
                    round(
                        angle,
                        2,
                    ),
            }
        )

    return segments

# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_directions_data()

    print(
        "Origin:",
        data["origin"],
    )

    print(
        "Destination:",
        data["destination"],
    )

    print(
        "Routes:",
        len(
            data["routes"]
        ),
    )

    print(
        "Mode:",
        data["selected_mode"],
    )