from __future__ import annotations

import random

from faker import Faker

from social_media.google_maps.generators.media_generator import (
    get_random_avatar,
    get_random_cafe_image,
    get_random_hotel_image,
    get_random_place_image,
    get_random_restaurant_image,
)


fake = Faker()


# ==========================================================
# Category Configuration
# ==========================================================

CATEGORY_OPTIONS = [
    {
        "label": "Restaurants",
        "icon": "restaurant",
    },
    {
        "label": "Hotels",
        "icon": "hotel",
    },
    {
        "label": "Gas",
        "icon": "local_gas_station",
    },
    {
        "label": "Coffee",
        "icon": "local_cafe",
    },
    {
        "label": "Groceries",
        "icon": "local_grocery_store",
    },
    {
        "label": "Shopping",
        "icon": "shopping_bag",
    },
    {
        "label": "Parks",
        "icon": "park",
    },
    {
        "label": "Parking",
        "icon": "local_parking",
    },
    {
        "label": "Pharmacies",
        "icon": "local_pharmacy",
    },
    {
        "label": "ATMs",
        "icon": "local_atm",
    },
]


# ==========================================================
# Place Types
# ==========================================================

PLACE_TYPES = [
    "Restaurant",
    "Cafe",
    "Hotel",
    "Bakery",
    "Park",
    "Museum",
    "Shopping center",
    "Bookstore",
    "Korean restaurant",
    "Italian restaurant",
]


PLACE_ICONS = [
    "restaurant",
    "local_cafe",
    "hotel",
    "park",
    "museum",
    "shopping_bag",
    "local_florist",
    "bakery_dining",
]


# ==========================================================
# Opening States
# ==========================================================

OPEN_STATES = [
    {
        "label": "Open",
        "status": "open",
    },
    {
        "label": "Open 24 hours",
        "status": "open",
    },
    {
        "label": "Closes 10 PM",
        "status": "open",
    },
    {
        "label": "Closes 11 PM",
        "status": "open",
    },
    {
        "label": "Closed",
        "status": "closed",
    },
]


# ==========================================================
# Map Road Generation
# ==========================================================

def generate_roads(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            15,
            25,
        )

    roads = []

    for index in range(
        count
    ):

        major = (
            random.random()
            < 0.22
        )

        roads.append(
            {
                "id":
                    index,

                "x":
                    random.randint(
                        -10,
                        95,
                    ),

                "y":
                    random.randint(
                        -5,
                        100,
                    ),

                "length":
                    random.randint(
                        25,
                        75,
                    ),

                "angle":
                    random.randint(
                        -70,
                        70,
                    ),

                "width":
                    (
                        random.randint(
                            9,
                            14,
                        )
                        if major
                        else random.randint(
                            4,
                            8,
                        )
                    ),

                "major":
                    major,
            }
        )

    return roads


# ==========================================================
# Building Generation
# ==========================================================

def generate_buildings(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            24,
            45,
        )

    buildings = []

    for index in range(
        count
    ):

        buildings.append(
            {
                "id":
                    index,

                "x":
                    random.randint(
                        2,
                        94,
                    ),

                "y":
                    random.randint(
                        3,
                        94,
                    ),

                "width":
                    random.randint(
                        2,
                        7,
                    ),

                "height":
                    random.randint(
                        2,
                        7,
                    ),

                "rotation":
                    random.randint(
                        -20,
                        20,
                    ),
            }
        )

    return buildings


# ==========================================================
# Park Generation
# ==========================================================

def generate_parks() -> list[dict]:

    parks = []

    for index in range(
        random.randint(
            1,
            4,
        )
    ):

        parks.append(
            {
                "id":
                    index,

                "x":
                    random.randint(
                        5,
                        80,
                    ),

                "y":
                    random.randint(
                        5,
                        80,
                    ),

                "width":
                    random.randint(
                        8,
                        22,
                    ),

                "height":
                    random.randint(
                        7,
                        20,
                    ),

                "radius":
                    random.randint(
                        25,
                        48,
                    ),
            }
        )

    return parks


# ==========================================================
# Water Generation
# ==========================================================

def generate_water() -> dict | None:

    if random.random() > 0.45:

        return None

    return {
        "x":
            random.choice(
                [
                    -12,
                    65,
                    75,
                ]
            ),

        "y":
            random.randint(
                5,
                55,
            ),

        "width":
            random.randint(
                25,
                48,
            ),

        "height":
            random.randint(
                18,
                45,
            ),

        "rotation":
            random.randint(
                -25,
                25,
            ),
    }


# ==========================================================
# Map Labels
# ==========================================================

def generate_map_labels(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            8,
            15,
        )

    labels = []

    for index in range(
        count
    ):

        labels.append(
            {
                "id":
                    index,

                "text":
                    fake.street_name(),

                "x":
                    random.randint(
                        8,
                        88,
                    ),

                "y":
                    random.randint(
                        8,
                        90,
                    ),

                "rotation":
                    random.randint(
                        -35,
                        35,
                    ),
            }
        )

    return labels


# ==========================================================
# Marker Generation
# ==========================================================

def generate_markers(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            7,
            14,
        )

    markers = []

    for index in range(
        count
    ):

        markers.append(
            {
                "id":
                    index,

                "icon":
                    random.choice(
                        PLACE_ICONS
                    ),

                "x":
                    random.randint(
                        8,
                        92,
                    ),

                "y":
                    random.randint(
                        14,
                        88,
                    ),

                "selected":
                    False,
            }
        )

    if markers:

        random.choice(
            markers
        )[
            "selected"
        ] = True

    return markers


# ==========================================================
# Place Image
# ==========================================================

def get_place_image_by_type(
    place_type: str,
) -> str | None:

    place_type_lower = (
        place_type.lower()
    )

    if (
        "restaurant"
        in place_type_lower
    ):

        return (
            get_random_restaurant_image()
            or get_random_place_image()
        )

    if (
        "cafe"
        in place_type_lower
        or "bakery"
        in place_type_lower
    ):

        return (
            get_random_cafe_image()
            or get_random_place_image()
        )

    if (
        "hotel"
        in place_type_lower
    ):

        return (
            get_random_hotel_image()
            or get_random_place_image()
        )

    return get_random_place_image()


# ==========================================================
# Generate One Place
# ==========================================================

def generate_place(
    index: int,
) -> dict:

    place_type = random.choice(
        PLACE_TYPES
    )

    rating = round(
        random.uniform(
            3.6,
            5.0,
        ),
        1,
    )

    review_count = random.randint(
        12,
        8500,
    )

    opening_state = random.choice(
        OPEN_STATES
    )

    return {
        "id":
            index,

        "name":
            (
                fake.company()
                .replace(
                    ", Inc.",
                    "",
                )
                .replace(
                    " LLC",
                    "",
                )
            ),

        "type":
            place_type,

        "rating":
            rating,

        "reviews":
            review_count,

        "price_level":
            random.choice(
                [
                    "$",
                    "$$",
                    "$$$",
                    "",
                ]
            ),

        "distance":
            random.choice(
                [
                    "0.2 mi",
                    "0.3 mi",
                    "0.5 mi",
                    "0.7 mi",
                    "1.1 mi",
                    "1.4 mi",
                    "2.0 mi",
                ]
            ),

        "open_label":
            opening_state[
                "label"
            ],

        "open_status":
            opening_state[
                "status"
            ],

        "address":
            fake.street_address(),

        "image":
            get_place_image_by_type(
                place_type
            ),

        "saved":
            random.random()
            < 0.16,
    }


# ==========================================================
# Home Data
# ==========================================================

def generate_home_data() -> dict:

    categories = random.sample(
        CATEGORY_OPTIONS,
        k=random.randint(
            5,
            min(
                8,
                len(
                    CATEGORY_OPTIONS
                ),
            ),
        ),
    )

    places = [
        generate_place(
            index
        )
        for index
        in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    search_suggestions = [
        random.choice(
            [
                "Restaurants near me",
                "Coffee",
                "Hotels",
                "Gas stations",
                "Things to do",
                "Shopping",
            ]
        ),
        fake.city(),
        fake.street_name(),
    ]

    return {
        # --------------------------------------------------
        # Header / Search
        # --------------------------------------------------

        "search_placeholder":
            random.choice(
                [
                    "Search here",
                    "Search Google Maps",
                    "Search nearby places",
                ]
            ),

        "search_suggestions":
            search_suggestions,

        "avatar":
            get_random_avatar(),

        # --------------------------------------------------
        # Category chips
        # --------------------------------------------------

        "categories":
            categories,

        # --------------------------------------------------
        # Map
        # --------------------------------------------------

        "map":
            {
                "roads":
                    generate_roads(),

                "buildings":
                    generate_buildings(),

                "parks":
                    generate_parks(),

                "water":
                    generate_water(),

                "labels":
                    generate_map_labels(),

                "markers":
                    generate_markers(),
            },

        # --------------------------------------------------
        # Current location
        # --------------------------------------------------

        "current_location":
            {
                "x":
                    random.randint(
                        35,
                        65,
                    ),

                "y":
                    random.randint(
                        35,
                        65,
                    ),
            },

        # --------------------------------------------------
        # Places
        # --------------------------------------------------

        "places":
            places,

        "sheet_title":
            random.choice(
                [
                    "Explore nearby",
                    "Places nearby",
                    "Discover around you",
                    "Nearby recommendations",
                ]
            ),

        # --------------------------------------------------
        # Navigation
        # --------------------------------------------------

        "navigation_items":
            [
                {
                    "label":
                        "Explore",

                    "icon":
                        "explore",

                    "selected":
                        True,
                },
                {
                    "label":
                        "You",

                    "icon":
                        "bookmark",

                    "selected":
                        False,
                },
                {
                    "label":
                        "Contribute",

                    "icon":
                        "add_circle",

                    "selected":
                        False,
                },
            ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_home_data()

    print(
        "\n=============================="
    )

    print(
        "GOOGLE MAPS HOME DATA"
    )

    print(
        "=============================="
    )

    print(
        "Categories:",
        len(
            data[
                "categories"
            ]
        ),
    )

    print(
        "Places:",
        len(
            data[
                "places"
            ]
        ),
    )

    print(
        "Roads:",
        len(
            data[
                "map"
            ][
                "roads"
            ]
        ),
    )

    print(
        "Markers:",
        len(
            data[
                "map"
            ][
                "markers"
            ]
        ),
    )