from __future__ import annotations

import random

from faker import Faker

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_markers,
    generate_parks,
    generate_roads,
    generate_water,
)

from social_media.google_maps.generators.media_generator import (
    get_random_avatar,
    get_random_cafe_image,
    get_random_hotel_image,
    get_random_place_image,
    get_random_restaurant_image,
)


fake = Faker()


# ==========================================================
# Tabs
# ==========================================================

SAVED_TABS = [
    {
        "key": "lists",
        "label": "Lists",
    },
    {
        "key": "labeled",
        "label": "Labeled",
    },
    {
        "key": "visited",
        "label": "Visited",
    },
]


# ==========================================================
# Collection Types
# ==========================================================

COLLECTION_OPTIONS = [
    {
        "name": "Favorites",
        "icon": "favorite",
    },
    {
        "name": "Want to go",
        "icon": "bookmark",
    },
    {
        "name": "Travel plans",
        "icon": "flight",
    },
    {
        "name": "Restaurants",
        "icon": "restaurant",
    },
    {
        "name": "Coffee spots",
        "icon": "local_cafe",
    },
    {
        "name": "Weekend places",
        "icon": "weekend",
    },
    {
        "name": "Shopping",
        "icon": "shopping_bag",
    },
]


PLACE_TYPES = [
    "Cafe",
    "Coffee shop",
    "Restaurant",
    "Hotel",
    "Bakery",
    "Museum",
    "Park",
    "Shopping center",
]


# ==========================================================
# Image Resolver
# ==========================================================

def get_saved_place_image(
    place_type: str,
) -> str | None:

    value = place_type.lower()

    if (
        "cafe" in value
        or "coffee" in value
        or "bakery" in value
    ):

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
# Collection
# ==========================================================

def generate_collection(
    index: int,
) -> dict:

    base = random.choice(
        COLLECTION_OPTIONS
    )

    collaborative = (
        random.random()
        < 0.35
    )

    collaborators = []

    if collaborative:

        for _ in range(
            random.randint(
                1,
                3,
            )
        ):

            collaborators.append(
                {
                    "avatar":
                        get_random_avatar(),

                    "name":
                        fake.first_name(),
                }
            )

    return {
        "id":
            index,

        "name":
            base["name"],

        "icon":
            base["icon"],

        "count":
            random.randint(
                3,
                48,
            ),

        "private":
            random.random()
            < 0.50,

        "collaborative":
            collaborative,

        "collaborators":
            collaborators,

        "color_role":
            random.choice(
                [
                    "primary",
                    "info",
                    "success",
                    "warning",
                ]
            ),
    }


# ==========================================================
# Saved Place
# ==========================================================

def generate_saved_place(
    index: int,
) -> dict:

    place_type = random.choice(
        PLACE_TYPES
    )

    rating = round(
        random.uniform(
            3.7,
            5.0,
        ),
        1,
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
            random.randint(
                20,
                9000,
            ),

        "distance":
            random.choice(
                [
                    "0.2 mi",
                    "0.4 mi",
                    "0.7 mi",
                    "1.1 mi",
                    "2.4 mi",
                ]
            ),

        "address":
            fake.street_address(),

        "image":
            get_saved_place_image(
                place_type
            ),

        "note":
            random.choice(
                [
                    "",
                    "Try this weekend",
                    "Recommended by a friend",
                    "Good for brunch",
                    "Visit next month",
                    "Great view",
                ]
            ),

        "collection":
            random.choice(
                [
                    "Favorites",
                    "Want to go",
                    "Travel plans",
                    "Restaurants",
                ]
            ),

        "visited":
            random.random()
            < 0.30,
    }


# ==========================================================
# Saved Data
# ==========================================================

def generate_saved_data() -> dict:

    selected_tab = random.choice(
        SAVED_TABS
    )

    tabs = [
        {
            **tab,
            "selected":
                tab["key"]
                == selected_tab["key"],
        }
        for tab
        in SAVED_TABS
    ]

    collection_count = random.randint(
        4,
        7,
    )

    collections = [
        generate_collection(
            index
        )
        for index
        in range(
            collection_count
        )
    ]

    saved_place_count = random.randint(
        8,
        15,
    )

    saved_places = [
        generate_saved_place(
            index
        )
        for index
        in range(
            saved_place_count
        )
    ]

    return {

        "tabs":
            tabs,

        "selected_tab":
            selected_tab["key"],

        "collections":
            collections,

        "saved_places":
            saved_places,

        "profile_avatar":
            get_random_avatar(),

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

                "markers":
                    generate_markers(
                        count=random.randint(
                            6,
                            10,
                        )
                    ),
            },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_saved_data()
    )

    print(
        "\n=============================="
    )

    print(
        "SAVED / LISTS"
    )

    print(
        "=============================="
    )

    print(
        "Collections:",
        len(
            data["collections"]
        ),
    )

    print(
        "Saved places:",
        len(
            data["saved_places"]
        ),
    )

    print(
        "Selected tab:",
        data["selected_tab"],
    )