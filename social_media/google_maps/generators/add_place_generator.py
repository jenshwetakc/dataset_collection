from __future__ import annotations

import random

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
# Categories
# ==========================================================

PLACE_CATEGORIES = [
    {
        "key": "restaurant",
        "label": "Restaurant",
        "icon": "restaurant",
    },
    {
        "key": "cafe",
        "label": "Cafe",
        "icon": "local_cafe",
    },
    {
        "key": "hotel",
        "label": "Hotel",
        "icon": "hotel",
    },
    {
        "key": "shopping",
        "label": "Shopping",
        "icon": "shopping_bag",
    },
    {
        "key": "park",
        "label": "Park",
        "icon": "park",
    },
    {
        "key": "museum",
        "label": "Museum",
        "icon": "museum",
    },
    {
        "key": "pharmacy",
        "label": "Pharmacy",
        "icon": "local_pharmacy",
    },
]


# ==========================================================
# Days
# ==========================================================

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


# ==========================================================
# Image Helper
# ==========================================================

def get_category_image(
    category: str,
) -> str | None:

    if category == "restaurant":

        return (
            get_random_restaurant_image()
            or get_random_place_image()
        )

    if category == "cafe":

        return (
            get_random_cafe_image()
            or get_random_place_image()
        )

    if category == "hotel":

        return (
            get_random_hotel_image()
            or get_random_place_image()
        )

    return get_random_place_image()


# ==========================================================
# Opening Hours
# ==========================================================

def generate_hours() -> list[dict]:

    rows = []

    for day in DAYS:

        closed = (
            random.random()
            < 0.12
        )

        rows.append(
            {
                "day":
                    day,

                "closed":
                    closed,

                "open":
                    (
                        ""
                        if closed
                        else random.choice(
                            [
                                "7:00 AM",
                                "8:00 AM",
                                "9:00 AM",
                                "10:00 AM",
                            ]
                        )
                    ),

                "close":
                    (
                        ""
                        if closed
                        else random.choice(
                            [
                                "6:00 PM",
                                "8:00 PM",
                                "9:00 PM",
                                "10:00 PM",
                                "11:00 PM",
                            ]
                        )
                    ),
            }
        )

    return rows


# ==========================================================
# Photos
# ==========================================================

def generate_photos(
    category: str,
) -> list[str]:

    photos = []

    for _ in range(
        random.randint(
            1,
            4,
        )
    ):

        image = (
            get_category_image(
                category
            )
        )

        if (
            image
            and image
            not in photos
        ):
            photos.append(
                image
            )

    return photos


# ==========================================================
# Main Data
# ==========================================================

def generate_add_place_data() -> dict:

    selected_category = (
        random.choice(
            PLACE_CATEGORIES
        )
    )

    city = fake.city()

    address = fake.street_address()

    return {

        "place_name":
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

        "category":
            selected_category,

        "categories":
            [
                {
                    **category,
                    "selected":
                        category["key"]
                        == selected_category["key"],
                }
                for category
                in PLACE_CATEGORIES
            ],

        "address":
            address,

        "city":
            city,

        "phone":
            fake.phone_number(),

        "website":
            random.choice(
                [
                    "",
                    "www.example.com",
                    "example-place.com",
                ]
            ),

        "description":
            random.choice(
                [
                    "",
                    "Popular neighborhood location.",
                    "Newly opened local business.",
                    "Family-owned place with convenient access.",
                ]
            ),

        "photos":
            generate_photos(
                selected_category["key"]
            ),

        "hours":
            generate_hours(),

        "wheelchair_accessible":
            random.random()
            < 0.55,

        "has_parking":
            random.random()
            < 0.48,

        "outdoor_seating":
            random.random()
            < 0.35,

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

            "selected_location":
                {
                    "x":
                        random.randint(
                            38,
                            62,
                        ),

                    "y":
                        random.randint(
                            34,
                            64,
                        ),
                },
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_add_place_data()

    print(
        "Place:",
        data["place_name"],
    )

    print(
        "Category:",
        data["category"]["label"],
    )

    print(
        "Photos:",
        len(
            data["photos"]
        ),
    )