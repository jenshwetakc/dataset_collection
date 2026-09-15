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
    get_random_street_view_image,
)


fake = Faker()


# ==========================================================
# Categories
# ==========================================================

PLACE_TYPES = [
    "Cafe",
    "Restaurant",
    "Hotel",
    "Museum",
    "Shopping center",
    "Park",
    "Landmark",
]


# ==========================================================
# Hotspot Directions
# ==========================================================

HOTSPOT_ICONS = [
    "arrow_upward",
    "north_east",
    "north_west",
    "arrow_forward",
]


# ==========================================================
# Place Image
# ==========================================================

def get_place_image(
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
# Hotspots
# ==========================================================

def generate_hotspots() -> list[dict]:

    hotspots = []

    for index in range(
        random.randint(
            3,
            6,
        )
    ):

        hotspots.append(
            {
                "id":
                    index,

                "x":
                    random.randint(
                        15,
                        85,
                    ),

                "y":
                    random.randint(
                        35,
                        76,
                    ),

                "icon":
                    random.choice(
                        HOTSPOT_ICONS
                    ),

                "distance":
                    random.choice(
                        [
                            "10 m",
                            "20 m",
                            "35 m",
                            "50 m",
                        ]
                    ),
            }
        )

    return hotspots


# ==========================================================
# Photo Strip
# ==========================================================

def generate_photos(
    place_type: str,
) -> list[str]:

    photos = []

    for _ in range(
        random.randint(
            4,
            7,
        )
    ):

        image = get_place_image(
            place_type
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
# Street View Data
# ==========================================================

def generate_street_view_data() -> dict:

    place_type = random.choice(
        PLACE_TYPES
    )

    rating = round(
        random.uniform(
            3.8,
            5.0,
        ),
        1,
    )

    street_view_image = (
        get_random_street_view_image()
        or get_place_image(
            place_type
        )
    )

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

        "place_type":
            place_type,

        "rating":
            rating,

        "reviews":
            random.randint(
                40,
                12000,
            ),

        "address":
            fake.street_address(),

        "city":
            fake.city(),

        "open_text":
            random.choice(
                [
                    "Open · Closes 9 PM",
                    "Open · Closes 10 PM",
                    "Open · Closes 11 PM",
                    "Open 24 hours",
                ]
            ),

        "saved":
            random.random()
            < 0.30,

        "street_view_image":
            street_view_image,

        "photos":
            generate_photos(
                place_type
            ),

        "hotspots":
            generate_hotspots(),

        "orientation":
            random.randint(
                0,
                359,
            ),

        "zoom":
            random.choice(
                [
                    1.0,
                    1.2,
                    1.4,
                    1.6,
                ]
            ),

        "map": {
            "roads":
                generate_roads(
                    count=random.randint(
                        14,
                        22,
                    )
                ),

            "buildings":
                generate_buildings(
                    count=random.randint(
                        20,
                        35,
                    )
                ),

            "parks":
                generate_parks(),

            "water":
                generate_water(),

            "labels":
                generate_map_labels(
                    count=random.randint(
                        6,
                        10,
                    )
                ),

            "marker":
                {
                    "x":
                        random.randint(
                            42,
                            58,
                        ),

                    "y":
                        random.randint(
                            40,
                            62,
                        ),
                },
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_street_view_data()
    )

    print(
        "Street View:",
        data["place_name"],
    )

    print(
        "Hotspots:",
        len(
            data["hotspots"]
        ),
    )

    print(
        "Photos:",
        len(
            data["photos"]
        ),
    )