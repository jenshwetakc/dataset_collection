from __future__ import annotations

import math
import random

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
# Maneuvers
# ==========================================================

MANEUVERS = [
    {
        "icon": "turn_right",
        "instruction": "Turn right",
    },
    {
        "icon": "turn_left",
        "instruction": "Turn left",
    },
    {
        "icon": "straight",
        "instruction": "Continue straight",
    },
    {
        "icon": "fork_right",
        "instruction": "Keep right",
    },
    {
        "icon": "fork_left",
        "instruction": "Keep left",
    },
    {
        "icon": "roundabout_right",
        "instruction": "At the roundabout, take the exit",
    },
    {
        "icon": "ramp_right",
        "instruction": "Take the ramp",
    },
    {
        "icon": "merge",
        "instruction": "Merge onto the highway",
    },
]


# ==========================================================
# Distance Labels
# ==========================================================

DISTANCE_LABELS = [
    "100 m",
    "200 m",
    "300 m",
    "500 m",
    "0.4 mi",
    "0.6 mi",
    "0.8 mi",
    "1.2 mi",
]


# ==========================================================
# Road Names
# ==========================================================

def generate_road_name() -> str:

    return random.choice(
        [
            fake.street_name(),
            "Main Street",
            "Central Avenue",
            "Riverside Drive",
            "Park Road",
            "Broadway",
            "Highway 1",
            "City Expressway",
        ]
    )


# ==========================================================
# Route Points
# ==========================================================

def generate_navigation_route_points(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            7,
            11,
        )

    start_x = random.randint(
        42,
        58,
    )

    start_y = random.randint(
        72,
        88,
    )

    end_x = random.randint(
        45,
        75,
    )

    end_y = random.randint(
        8,
        25,
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
                -8,
                8,
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
                "x":
                    round(
                        max(
                            5,
                            min(
                                95,
                                x,
                            ),
                        ),
                        2,
                    ),

                "y":
                    round(
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
# Route Segment Geometry
# ==========================================================

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
# Secondary Route
# ==========================================================

def generate_secondary_route() -> dict | None:

    if random.random() > 0.45:

        return None

    points = (
        generate_navigation_route_points(
            count=random.randint(
                6,
                9,
            )
        )
    )

    return {
        "points":
            points,

        "segments":
            build_route_segments(
                points
            ),

        "extra_minutes":
            random.randint(
                2,
                9,
            ),
    }


# ==========================================================
# Navigation Data
# ==========================================================

def generate_navigation_data() -> dict:

    maneuver = random.choice(
        MANEUVERS
    )

    route_points = (
        generate_navigation_route_points()
    )

    remaining_minutes = random.randint(
        6,
        65,
    )

    remaining_distance = round(
        random.uniform(
            1.1,
            28.0,
        ),
        1,
    )

    current_speed = random.randint(
        18,
        75,
    )

    speed_limit = random.choice(
        [
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            65,
        ]
    )

    next_road = (
        generate_road_name()
    )

    return {

        # --------------------------------------------------
        # Maneuver
        # --------------------------------------------------

        "maneuver": {
            "icon":
                maneuver["icon"],

            "instruction":
                maneuver["instruction"],

            "road":
                next_road,

            "distance":
                random.choice(
                    DISTANCE_LABELS
                ),
        },

        # --------------------------------------------------
        # Following Maneuver
        # --------------------------------------------------

        "next_maneuver": {
            "icon":
                random.choice(
                    MANEUVERS
                )["icon"],

            "distance":
                random.choice(
                    [
                        "then 0.2 mi",
                        "then 400 m",
                        "then 0.5 mi",
                        "then 700 m",
                    ]
                ),
        },

        # --------------------------------------------------
        # Map
        # --------------------------------------------------

        "map": {
            "roads":
                generate_roads(
                    count=random.randint(
                        22,
                        34,
                    )
                ),

            "buildings":
                generate_buildings(
                    count=random.randint(
                        35,
                        62,
                    )
                ),

            "parks":
                generate_parks(),

            "water":
                generate_water(),

            "labels":
                generate_map_labels(
                    count=random.randint(
                        10,
                        17,
                    )
                ),

            "route_points":
                route_points,

            "route_segments":
                build_route_segments(
                    route_points
                ),

            "secondary_route":
                generate_secondary_route(),
        },

        # --------------------------------------------------
        # Navigation Position
        # --------------------------------------------------

        "vehicle_position": {
            "x":
                route_points[0]["x"],

            "y":
                route_points[0]["y"],
        },

        # --------------------------------------------------
        # ETA
        # --------------------------------------------------

        "eta": {
            "minutes":
                remaining_minutes,

            "duration_text":
                f"{remaining_minutes} min",

            "distance_text":
                f"{remaining_distance} mi",

            "arrival_time":
                (
                    f"{random.randint(1, 11)}:"
                    f"{random.choice(['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'])} "
                    f"{random.choice(['AM', 'PM'])}"
                ),
        },

        # --------------------------------------------------
        # Speed
        # --------------------------------------------------

        "speed": {
            "current":
                current_speed,

            "limit":
                speed_limit,

            "unit":
                "mph",
        },

        # --------------------------------------------------
        # Traffic
        # --------------------------------------------------

        "traffic": random.choice(
            [
                "Light traffic",
                "Moderate traffic",
                "Usual traffic",
                "Heavy traffic ahead",
            ]
        ),

        # --------------------------------------------------
        # Voice
        # --------------------------------------------------

        "voice_muted":
            random.random()
            < 0.22,

        # --------------------------------------------------
        # Lane Guidance
        # --------------------------------------------------

        "lane_guidance":
            (
                random.random()
                < 0.45
            ),

        "lane_count":
            random.randint(
                2,
                5,
            ),

        "active_lane":
            random.randint(
                1,
                3,
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_navigation_data()
    )

    print(
        "\n=============================="
    )

    print(
        "NAVIGATION"
    )

    print(
        "=============================="
    )

    print(
        data["maneuver"]
    )

    print(
        data["eta"]
    )

    print(
        data["speed"]
    )