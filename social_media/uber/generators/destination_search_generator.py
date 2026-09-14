from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

PLACE_TYPES = [
    "Cafe",
    "Restaurant",
    "Hotel",
    "Shopping center",
    "Airport",
    "Station",
    "Office",
    "University",
    "Hospital",
    "Park",
]


PLACE_ICONS = [
    "location_on",
    "restaurant",
    "local_cafe",
    "hotel",
    "shopping_bag",
    "flight",
    "train",
    "business",
]


SAVED_PLACES = [
    {
        "label": "Home",
        "icon": "home",
    },
    {
        "label": "Work",
        "icon": "work",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_address() -> str:

    return (
        f"{fake.street_address()}, "
        f"{fake.city()}"
    )


def generate_place_name() -> str:

    if random.random() < 0.45:

        return fake.company()

    place_type = random.choice(
        PLACE_TYPES
    )

    return (
        f"{fake.city()} "
        f"{place_type}"
    )


def generate_recent_place() -> dict:

    return {
        "name":
            generate_place_name(),

        "address":
            generate_address(),

        "icon":
            "history",
    }


def generate_suggested_place() -> dict:

    return {
        "name":
            generate_place_name(),

        "address":
            generate_address(),

        "distance":
            f"{random.uniform(0.3, 9.5):.1f} km",

        "icon":
            random.choice(
                PLACE_ICONS
            ),

        "badge":
            random.choice(
                [
                    None,
                    None,
                    "Popular",
                    "Nearby",
                ]
            ),
    }


def generate_map_marker(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "x":
            random.randint(
                12,
                88,
            ),

        "y":
            random.randint(
                12,
                84,
            ),

        "icon":
            random.choice(
                [
                    "restaurant",
                    "local_cafe",
                    "shopping_bag",
                    "hotel",
                    "location_on",
                ]
            ),
    }


# ==========================================================
# Generator
# ==========================================================

def generate_destination_search_data() -> dict:

    recent_count = random.randint(
        4,
        7,
    )

    suggestion_count = random.randint(
        5,
        8,
    )

    marker_count = random.randint(
        4,
        7,
    )

    saved_places = []

    for item in SAVED_PLACES:

        saved_places.append(
            {
                **item,

                "address":
                    generate_address(),
            }
        )


    return {

        "title":
            "Search destination",

        "pickup": {

            "label":
                "Pickup",

            "value":
                random.choice(
                    [
                        "Current location",
                        "My location",
                        "Pickup location",
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

            "placeholder":
                random.choice(
                    [
                        "Where to?",
                        "Search destination",
                        "Enter destination",
                    ]
                ),

            "icon":
                "location_on",
        },

        "saved_places":
            saved_places,

        "recent_places": [

            generate_recent_place()

            for _ in range(
                recent_count
            )
        ],

        "suggested_places": [

            generate_suggested_place()

            for _ in range(
                suggestion_count
            )
        ],

        "map": {

            "user_location": {

                "x":
                    random.randint(
                        35,
                        65,
                    ),

                "y":
                    random.randint(
                        30,
                        65,
                    ),
            },

            "markers": [

                generate_map_marker(
                    index
                )

                for index
                in range(
                    marker_count
                )
            ],
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_destination_search_data()
    )