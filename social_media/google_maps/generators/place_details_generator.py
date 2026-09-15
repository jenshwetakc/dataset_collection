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
    get_random_street_view_image,
)


fake = Faker()


# ==========================================================
# Place Types
# ==========================================================

PLACE_TYPES = [
    "Cafe",
    "Coffee shop",
    "Restaurant",
    "Korean restaurant",
    "Italian restaurant",
    "Hotel",
    "Bakery",
    "Museum",
    "Shopping center",
    "Park",
]


# ==========================================================
# Amenities
# ==========================================================

AMENITIES = [
    {
        "label": "Wi-Fi",
        "icon": "wifi",
    },
    {
        "label": "Parking",
        "icon": "local_parking",
    },
    {
        "label": "Wheelchair accessible",
        "icon": "accessible",
    },
    {
        "label": "Takeout",
        "icon": "takeout_dining",
    },
    {
        "label": "Delivery",
        "icon": "delivery_dining",
    },
    {
        "label": "Outdoor seating",
        "icon": "deck",
    },
    {
        "label": "Reservations",
        "icon": "event_available",
    },
    {
        "label": "Restroom",
        "icon": "wc",
    },
]


# ==========================================================
# Review Phrases
# ==========================================================

REVIEW_TEXTS = [
    "Great atmosphere and friendly service. I would definitely come back.",
    "The location is convenient and the staff were very helpful.",
    "Really enjoyed the food and the overall atmosphere.",
    "Clean, comfortable, and easy to find. Service was quick.",
    "One of my favorite places in the area. Highly recommended.",
    "Good experience overall. It can get busy during peak hours.",
    "Excellent service and a nice selection. Everything felt well organized.",
    "Nice place to stop by with friends. The staff were welcoming.",
]


# ==========================================================
# Image Resolver
# ==========================================================

def get_place_image(
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
# Place Name
# ==========================================================

def generate_place_name(
    place_type: str,
) -> str:

    prefix = random.choice(
        [
            fake.first_name(),
            fake.last_name(),
            fake.city(),
            random.choice(
                [
                    "Central",
                    "Garden",
                    "Riverside",
                    "Urban",
                    "Golden",
                    "Blue",
                    "Green",
                ]
            ),
        ]
    )

    suffix_map = {

        "Cafe":
            [
                "Cafe",
                "Coffee",
                "Roasters",
            ],

        "Coffee shop":
            [
                "Coffee",
                "Cafe",
                "Roastery",
            ],

        "Restaurant":
            [
                "Kitchen",
                "Restaurant",
                "Bistro",
            ],

        "Korean restaurant":
            [
                "Korean Kitchen",
                "BBQ",
                "House",
            ],

        "Italian restaurant":
            [
                "Trattoria",
                "Italian Kitchen",
                "Pizzeria",
            ],

        "Hotel":
            [
                "Hotel",
                "Residence",
                "Suites",
            ],

        "Bakery":
            [
                "Bakery",
                "Bakehouse",
                "Bread",
            ],

        "Museum":
            [
                "Museum",
                "Gallery",
                "Center",
            ],

        "Shopping center":
            [
                "Mall",
                "Shopping Center",
                "Plaza",
            ],

        "Park":
            [
                "Park",
                "Garden",
                "Square",
            ],
    }

    suffix = random.choice(
        suffix_map[
            place_type
        ]
    )

    return (
        f"{prefix} {suffix}"
    )


# ==========================================================
# Business Hours
# ==========================================================

def generate_hours() -> list[dict]:

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    closed_day = (
        random.choice(
            days
        )
        if random.random() < 0.20
        else None
    )

    hours = []

    for day in days:

        if day == closed_day:

            value = "Closed"

        else:

            opening = random.choice(
                [
                    "7:00 AM",
                    "8:00 AM",
                    "9:00 AM",
                    "10:00 AM",
                ]
            )

            closing = random.choice(
                [
                    "8:00 PM",
                    "9:00 PM",
                    "10:00 PM",
                    "11:00 PM",
                ]
            )

            value = (
                f"{opening} – {closing}"
            )

        hours.append(
            {
                "day":
                    day,

                "hours":
                    value,

                "today":
                    False,
            }
        )

    hours[
        random.randrange(
            len(hours)
        )
    ][
        "today"
    ] = True

    return hours


# ==========================================================
# Popular Times
# ==========================================================

def generate_popular_times() -> list[dict]:

    labels = [
        "6a",
        "8a",
        "10a",
        "12p",
        "2p",
        "4p",
        "6p",
        "8p",
        "10p",
    ]

    peak_index = random.randint(
        3,
        6,
    )

    result = []

    for index, label in enumerate(
        labels
    ):

        distance = abs(
            index
            - peak_index
        )

        base = max(
            15,
            90
            - distance * random.randint(
                12,
                20,
            )
        )

        value = min(
            100,
            max(
                10,
                base
                + random.randint(
                    -12,
                    12,
                ),
            ),
        )

        result.append(
            {
                "label":
                    label,

                "value":
                    value,
            }
        )

    return result


# ==========================================================
# Review
# ==========================================================

def generate_review(
    index: int,
) -> dict:

    rating = random.choices(
        [
            5,
            4,
            3,
            2,
        ],
        weights=[
            58,
            30,
            9,
            3,
        ],
        k=1,
    )[0]

    return {

        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "rating":
            rating,

        "time":
            random.choice(
                [
                    "2 days ago",
                    "1 week ago",
                    "2 weeks ago",
                    "1 month ago",
                    "3 months ago",
                    "6 months ago",
                ]
            ),

        "text":
            random.choice(
                REVIEW_TEXTS
            ),

        "likes":
            random.randint(
                0,
                180,
            ),

        "local_guide":
            random.random()
            < 0.28,
    }


# ==========================================================
# Photo Gallery
# ==========================================================

def generate_gallery(
    place_type: str,
) -> list[str]:

    images = []

    for _ in range(
        random.randint(
            4,
            8,
        )
    ):

        image = get_place_image(
            place_type
        )

        if (
            image
            and image
            not in images
        ):
            images.append(
                image
            )

    street_view = (
        get_random_street_view_image()
    )

    if (
        street_view
        and street_view
        not in images
    ):
        images.append(
            street_view
        )

    return images


# ==========================================================
# Place Details Data
# ==========================================================

def generate_place_details_data() -> dict:

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

    review_count = random.randint(
        80,
        18000,
    )

    open_now = (
        random.random()
        < 0.82
    )

    gallery = (
        generate_gallery(
            place_type
        )
    )

    amenities = random.sample(
        AMENITIES,
        k=random.randint(
            3,
            min(
                7,
                len(
                    AMENITIES
                ),
            ),
        ),
    )

    reviews = [
        generate_review(
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

    markers = (
        generate_markers(
            count=random.randint(
                4,
                8,
            )
        )
    )

    return {

        "name":
            generate_place_name(
                place_type
            ),

        "type":
            place_type,

        "rating":
            rating,

        "reviews":
            review_count,

        "price":
            random.choice(
                [
                    "",
                    "$",
                    "$$",
                    "$$$",
                ]
            ),

        "address":
            fake.street_address(),

        "city":
            fake.city(),

        "phone":
            fake.phone_number(),

        "website":
            random.choice(
                [
                    "www.example.com",
                    "example-place.com",
                    "visit-example.com",
                ]
            ),

        "open_now":
            open_now,

        "open_text":
            (
                random.choice(
                    [
                        "Open · Closes 9 PM",
                        "Open · Closes 10 PM",
                        "Open · Closes 11 PM",
                        "Open 24 hours",
                    ]
                )
                if open_now
                else "Closed"
            ),

        "description":
            random.choice(
                [
                    "Popular local destination with a relaxed atmosphere and convenient access.",
                    "Well-known neighborhood spot offering a comfortable setting and friendly service.",
                    "A popular place in the area with strong reviews from visitors and local residents.",
                    "Conveniently located destination known for its welcoming atmosphere and quality service.",
                ]
            ),

        "saved":
            random.random()
            < 0.25,

        "gallery":
            gallery,

        "hero_image":
            (
                gallery[0]
                if gallery
                else None
            ),

        "hours":
            generate_hours(),

        "popular_times":
            generate_popular_times(),

        "amenities":
            amenities,

        "reviews_list":
            reviews,

        "map":
            {
                "roads":
                    generate_roads(
                        count=random.randint(
                            20,
                            30,
                        )
                    ),

                "buildings":
                    generate_buildings(
                        count=random.randint(
                            30,
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
                            9,
                            15,
                        )
                    ),

                "markers":
                    markers,

                "place_marker":
                    {
                        "x":
                            random.randint(
                                40,
                                65,
                            ),

                        "y":
                            random.randint(
                                35,
                                60,
                            ),
                    },
            },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_place_details_data()
    )

    print(
        "\n=============================="
    )

    print(
        "PLACE DETAILS"
    )

    print(
        "=============================="
    )

    print(
        data["name"]
    )

    print(
        data["type"]
    )

    print(
        data["rating"]
    )

    print(
        "Gallery:",
        len(
            data["gallery"]
        ),
    )

    print(
        "Reviews:",
        len(
            data["reviews_list"]
        ),
    )