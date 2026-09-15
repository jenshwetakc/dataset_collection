from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_parks,
    generate_roads,
    generate_water,
)

from social_media.google_maps.generators.media_generator import (
    get_random_cafe_image,
    get_random_hotel_image,
    get_random_place_image,
    get_random_restaurant_image,
)


fake = Faker()


# ==========================================================
# Travel Modes
# ==========================================================

TRAVEL_MODES = [
    {
        "key": "walk",
        "label": "Walk",
        "icon": "directions_walk",
    },
    {
        "key": "drive",
        "label": "Drive",
        "icon": "directions_car",
    },
    {
        "key": "transit",
        "label": "Subway",
        "icon": "subway",
    },
    {
        "key": "bike",
        "label": "Bike",
        "icon": "directions_bike",
    },
    {
        "key": "bus",
        "label": "Bus",
        "icon": "directions_bus",
    },
]


# ==========================================================
# Place Types
# ==========================================================

PLACE_TYPES = [
    "Home",
    "Cafe",
    "Restaurant",
    "University",
    "Office",
    "Hotel",
    "Shopping center",
    "Park",
    "Museum",
    "Station",
]


# ==========================================================
# Image Resolver
# ==========================================================

def get_timeline_place_image(
    place_type: str,
) -> str | None:

    value = place_type.lower()

    if "cafe" in value:

        return (
            get_random_cafe_image()
            or get_random_place_image()
        )

    if "restaurant" in value:

        return (
            get_random_restaurant_image()
            or get_random_place_image()
        )

    if "hotel" in value:

        return (
            get_random_hotel_image()
            or get_random_place_image()
        )

    return get_random_place_image()


# ==========================================================
# Date Tabs
# ==========================================================

def generate_date_tabs() -> list[dict]:

    today = datetime.now()

    tabs = []

    for index in range(5):

        date = (
            today
            - timedelta(
                days=index
            )
        )

        if index == 0:

            label = "Today"

        elif index == 1:

            label = "Yesterday"

        else:

            label = date.strftime(
                "%b %d"
            )

        tabs.append(
            {
                "id":
                    index,

                "label":
                    label,

                "date":
                    date.strftime(
                        "%Y-%m-%d"
                    ),

                "selected":
                    index == 0,
            }
        )

    return tabs


# ==========================================================
# Place Visit
# ==========================================================

def generate_visit(
    index: int,
    current_minutes: int,
) -> tuple[dict, int]:

    place_type = random.choice(
        PLACE_TYPES
    )

    duration = random.randint(
        20,
        150,
    )

    start_minutes = current_minutes

    end_minutes = (
        start_minutes
        + duration
    )

    def minutes_to_time(
        minutes: int,
    ) -> str:

        hours = (
            minutes // 60
        )

        mins = (
            minutes % 60
        )

        suffix = (
            "AM"
            if hours < 12
            else "PM"
        )

        display_hour = (
            hours % 12
        )

        if display_hour == 0:
            display_hour = 12

        return (
            f"{display_hour}:"
            f"{mins:02d} "
            f"{suffix}"
        )

    if place_type == "Home":

        name = random.choice(
            [
                "Home",
                "Apartment",
            ]
        )

    elif place_type == "University":

        name = random.choice(
            [
                "Central University",
                "Engineering Building",
                "Research Center",
            ]
        )

    elif place_type == "Station":

        name = (
            fake.last_name()
            + " Station"
        )

    else:

        name = (
            fake.company()
            .replace(
                ", Inc.",
                "",
            )
            .replace(
                " LLC",
                "",
            )
        )

    visit = {
        "id":
            index,

        "type":
            place_type,

        "name":
            name,

        "address":
            fake.street_address(),

        "start_time":
            minutes_to_time(
                start_minutes
            ),

        "end_time":
            minutes_to_time(
                end_minutes
            ),

        "duration":
            duration,

        "duration_label":
            (
                f"{duration // 60} hr "
                f"{duration % 60} min"
                if duration >= 60
                else f"{duration} min"
            ),

        "image":
            get_timeline_place_image(
                place_type
            ),

        "rating":
            (
                round(
                    random.uniform(
                        3.8,
                        5.0,
                    ),
                    1,
                )
                if place_type not in {
                    "Home",
                    "University",
                    "Office",
                    "Station",
                }
                else None
            ),

        "saved":
            random.random()
            < 0.30,

        "x":
            random.randint(
                14,
                86,
            ),

        "y":
            random.randint(
                15,
                85,
            ),
    }

    return (
        visit,
        end_minutes,
    )


# ==========================================================
# Travel Segment
# ==========================================================

def generate_segment(
    index: int,
) -> dict:

    mode = random.choice(
        TRAVEL_MODES
    )

    distance = round(
        random.uniform(
            0.3,
            8.5,
        ),
        1,
    )

    speed_map = {
        "walk": 4.5,
        "bike": 13.0,
        "drive": 28.0,
        "transit": 24.0,
        "bus": 20.0,
    }

    duration = max(
        4,
        int(
            (
                distance
                / speed_map[
                    mode["key"]
                ]
            )
            * 60
        ),
    )

    return {
        "id":
            index,

        "mode":
            mode["key"],

        "label":
            mode["label"],

        "icon":
            mode["icon"],

        "distance":
            distance,

        "distance_label":
            f"{distance} km",

        "duration":
            duration,

        "duration_label":
            f"{duration} min",

        "traffic":
            (
                random.choice(
                    [
                        "",
                        "Light traffic",
                        "Moderate traffic",
                    ]
                )
                if mode["key"]
                == "drive"
                else ""
            ),
    }


# ==========================================================
# Timeline
# ==========================================================

def generate_timeline_items() -> tuple[
    list[dict],
    list[dict],
]:

    visit_count = random.randint(
        4,
        7,
    )

    current_minutes = random.randint(
        7 * 60,
        9 * 60,
    )

    visits = []
    segments = []

    for index in range(
        visit_count
    ):

        visit, current_minutes = (
            generate_visit(
                index,
                current_minutes,
            )
        )

        visits.append(
            visit
        )

        if index < visit_count - 1:

            segment = (
                generate_segment(
                    index
                )
            )

            segments.append(
                segment
            )

            current_minutes += (
                segment[
                    "duration"
                ]
            )

    return (
        visits,
        segments,
    )


# ==========================================================
# Map Route
# ==========================================================

def build_route_segments(
    visits: list[dict],
) -> list[dict]:

    import math

    segments = []

    for index in range(
        len(visits) - 1
    ):

        start = visits[index]
        end = visits[index + 1]

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
# Main Data
# ==========================================================

def generate_timeline_data() -> dict:

    visits, segments = (
        generate_timeline_items()
    )

    total_distance = round(
        sum(
            segment["distance"]
            for segment
            in segments
        ),
        1,
    )

    travel_minutes = sum(
        segment["duration"]
        for segment
        in segments
    )

    today = datetime.now()

    return {

        "date_tabs":
            generate_date_tabs(),

        "date_title":
            today.strftime(
                "%A, %B %d"
            ),

        "visits":
            visits,

        "segments":
            segments,

        "route_segments":
            build_route_segments(
                visits
            ),

        "stats": {
            "places":
                len(
                    visits
                ),

            "distance":
                f"{total_distance} km",

            "travel_time":
                (
                    f"{travel_minutes // 60} hr "
                    f"{travel_minutes % 60} min"
                    if travel_minutes >= 60
                    else f"{travel_minutes} min"
                ),

            "trips":
                len(
                    segments
                ),
        },

        "map": {
            "roads":
                generate_roads(
                    count=random.randint(
                        18,
                        30,
                    )
                ),

            "buildings":
                generate_buildings(
                    count=random.randint(
                        28,
                        48,
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
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_timeline_data()
    )

    print(
        data["date_title"]
    )

    print(
        "Visits:",
        len(
            data["visits"]
        ),
    )

    print(
        "Segments:",
        len(
            data["segments"]
        ),
    )

    print(
        "Stats:",
        data["stats"],
    )