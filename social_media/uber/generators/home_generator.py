from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

SEARCH_PROMPTS = [
    "Where to?",
    "Enter destination",
    "Where are you going?",
    "Search destination",
]


QUICK_PLACES = [
    {
        "label": "Home",
        "icon": "home",
    },
    {
        "label": "Work",
        "icon": "work",
    },
    {
        "label": "Airport",
        "icon": "flight",
    },
]


PLACE_TYPES = [
    "Restaurant",
    "Cafe",
    "Shopping center",
    "Hotel",
    "Office",
    "University",
    "Station",
    "Park",
    "Hospital",
    "Airport",
]


NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "selected": True,
    },
    {
        "label": "Activity",
        "icon": "receipt_long",
        "selected": False,
    },
    {
        "label": "Account",
        "icon": "person",
        "selected": False,
    },
]


# ==========================================================
# Address Generation
# ==========================================================

def generate_address() -> str:

    return (
        f"{fake.street_address()}, "
        f"{fake.city()}"
    )


# ==========================================================
# Recent Destination
# ==========================================================

def generate_recent_destination() -> dict:

    return {
        "name":
            fake.company(),

        "address":
            generate_address(),

        "type":
            random.choice(
                PLACE_TYPES
            ),

        "icon":
            random.choice(
                [
                    "location_on",
                    "history",
                    "business",
                    "restaurant",
                    "local_cafe",
                    "shopping_bag",
                ]
            ),
    }


# ==========================================================
# Suggestion
# ==========================================================

def generate_suggestion() -> dict:

    place_type = random.choice(
        PLACE_TYPES
    )

    return {
        "name":
            fake.company(),

        "address":
            generate_address(),

        "type":
            place_type,

        "distance":
            f"{random.uniform(0.4, 8.5):.1f} km",

        "icon":
            random.choice(
                [
                    "location_on",
                    "storefront",
                    "business",
                    "restaurant",
                    "local_cafe",
                    "hotel",
                ]
            ),
    }


# ==========================================================
# Map Marker
# ==========================================================

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
                82,
            ),

        "icon":
            random.choice(
                [
                    "location_on",
                    "restaurant",
                    "local_cafe",
                    "shopping_bag",
                    "hotel",
                    "local_parking",
                ]
            ),
    }


# ==========================================================
# Road
# ==========================================================

def generate_road(
    index: int,
) -> dict:

    orientation = random.choice(
        [
            "horizontal",
            "vertical",
            "diagonal",
        ]
    )

    if orientation == "horizontal":

        return {
            "id": index,
            "orientation": orientation,
            "top": random.randint(8, 88),
            "left": -5,
            "width": 110,
            "rotation": random.randint(-8, 8),
        }

    if orientation == "vertical":

        return {
            "id": index,
            "orientation": orientation,
            "top": -5,
            "left": random.randint(8, 88),
            "width": 110,
            "rotation": random.randint(82, 98),
        }

    return {
        "id": index,
        "orientation": orientation,
        "top": random.randint(5, 80),
        "left": random.randint(-15, 35),
        "width": random.randint(80, 140),
        "rotation": random.choice(
            [
                -35,
                -25,
                20,
                30,
                40,
            ]
        ),
    }


# ==========================================================
# Home Generator
# ==========================================================

def generate_home_data() -> dict:

    recent_count = random.randint(
        3,
        6,
    )

    suggestion_count = random.randint(
        3,
        6,
    )

    marker_count = random.randint(
        4,
        8,
    )

    road_count = random.randint(
        7,
        12,
    )


    quick_places = []

    for item in QUICK_PLACES:

        quick_places.append(
            {
                **item,
                "address":
                    generate_address(),
            }
        )


    return {

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        "brand":
            "Uber",

        "greeting":
            random.choice(
                [
                    "Good morning",
                    "Good afternoon",
                    "Good evening",
                    "Ready to go?",
                ]
            ),

        "search_prompt":
            random.choice(
                SEARCH_PROMPTS
            ),


        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "pickup_label":
            "Current location",

        "pickup_address":
            generate_address(),


        # --------------------------------------------------
        # Quick Places
        # --------------------------------------------------

        "quick_places":
            quick_places,


        # --------------------------------------------------
        # Recent Destinations
        # --------------------------------------------------

        "recent_destinations": [

            generate_recent_destination()

            for _ in range(
                recent_count
            )
        ],


        # --------------------------------------------------
        # Suggestions
        # --------------------------------------------------

        "suggestions": [

            generate_suggestion()

            for _ in range(
                suggestion_count
            )
        ],


        # --------------------------------------------------
        # Map
        # --------------------------------------------------

        "map": {

            "roads": [

                generate_road(
                    index
                )

                for index
                in range(
                    road_count
                )
            ],

            "markers": [

                generate_map_marker(
                    index
                )

                for index
                in range(
                    marker_count
                )
            ],

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
        },


        # --------------------------------------------------
        # Navigation
        # --------------------------------------------------

        "navigation":
            NAVIGATION_ITEMS,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_home_data()
    )