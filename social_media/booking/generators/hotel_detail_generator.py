from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_hotel_image,
    get_random_room_image,
)


# ==========================================================
# States
# ==========================================================

DETAIL_STATES = [
    "standard",
    "gallery_focus",
    "room_selection",
    "deal_heavy",
    "reviews_focus",
    "sold_out",
]


HOTEL_NAMES = [
    "Grand Central Hotel",
    "Riverside Boutique Hotel",
    "The Metropolitan",
    "Skyline Residence",
    "Ocean View Resort",
    "Royal Park Suites",
    "Urban Stay Hotel",
    "Harbor View Residence",
]


CITIES = [
    "Seoul",
    "Tokyo",
    "Paris",
    "London",
    "Bangkok",
    "Singapore",
]


AREAS = [
    "City Center",
    "Downtown",
    "Riverside",
    "Old Town",
    "Business District",
    "Central District",
]


FACILITIES = [
    {
        "label": "Free WiFi",
        "icon": "wifi",
    },
    {
        "label": "Swimming pool",
        "icon": "pool",
    },
    {
        "label": "Fitness center",
        "icon": "fitness_center",
    },
    {
        "label": "Restaurant",
        "icon": "restaurant",
    },
    {
        "label": "Parking",
        "icon": "local_parking",
    },
    {
        "label": "Airport shuttle",
        "icon": "airport_shuttle",
    },
    {
        "label": "Room service",
        "icon": "room_service",
    },
    {
        "label": "Breakfast",
        "icon": "bakery_dining",
    },
]


ROOM_NAMES = [
    "Standard Double Room",
    "Deluxe King Room",
    "Superior Twin Room",
    "Family Suite",
    "Executive Room",
    "City View Suite",
]


BED_TYPES = [
    "1 queen bed",
    "1 king bed",
    "2 single beds",
    "1 king bed + sofa bed",
]


REVIEW_TEXTS = [
    (
        "Excellent location and very comfortable rooms. "
        "The staff were friendly and helpful."
    ),
    (
        "Great stay with clean rooms and convenient access "
        "to restaurants and public transport."
    ),
    (
        "The room was spacious and quiet. Breakfast had "
        "a good selection."
    ),
    (
        "Very comfortable property with an excellent "
        "location near the city center."
    ),
]


# ==========================================================
# Gallery
# ==========================================================

def generate_gallery() -> list[dict]:

    return [
        {
            "image":
                get_random_hotel_image(),

            "semantic":
                f"hotel_gallery_image_{index + 1}",
        }
        for index in range(
            random.randint(
                5,
                8,
            )
        )
    ]


# ==========================================================
# Room
# ==========================================================

def generate_room(
    *,
    sold_out: bool = False,
    force_deal: bool = False,
) -> dict:

    old_price = random.randint(
        140,
        480,
    )

    discount = random.randint(
        10,
        30,
    )

    deal = (
        force_deal
        or random.random() < 0.45
    )

    price = (
        round(
            old_price
            * (
                1
                - discount / 100
            )
        )
        if deal
        else old_price
    )

    return {
        "name":
            random.choice(
                ROOM_NAMES
            ),

        "image":
            get_random_room_image(),

        "bed":
            random.choice(
                BED_TYPES
            ),

        "guests":
            random.randint(
                1,
                4,
            ),

        "size":
            random.randint(
                20,
                58,
            ),

        "price":
            price,

        "old_price":
            old_price,

        "discount":
            discount,

        "deal":
            deal,

        "breakfast":
            random.random() < 0.55,

        "free_cancel":
            random.random() < 0.65,

        "pay_later":
            random.random() < 0.45,

        "limited":
            (
                not sold_out
                and random.random() < 0.25
            ),

        "sold_out":
            sold_out,

        "currency":
            random.choice(
                [
                    "US$",
                    "₩",
                    "€",
                ]
            ),
    }


# ==========================================================
# Review
# ==========================================================

def generate_review() -> dict:

    score = round(
        random.uniform(
            7.8,
            10.0,
        ),
        1,
    )

    return {
        "name":
            random.choice(
                [
                    "Emma",
                    "Daniel",
                    "Mina",
                    "Lucas",
                    "Sophie",
                    "Alex",
                    "Jin",
                    "Maria",
                ]
            ),

        "country":
            random.choice(
                [
                    "South Korea",
                    "Japan",
                    "United Kingdom",
                    "Germany",
                    "France",
                    "United States",
                ]
            ),

        "score":
            score,

        "text":
            random.choice(
                REVIEW_TEXTS
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_hotel_detail_data() -> dict:

    state = random.choice(
        DETAIL_STATES
    )

    sold_out = (
        state == "sold_out"
    )

    deal_heavy = (
        state == "deal_heavy"
    )

    gallery_focus = (
        state == "gallery_focus"
    )

    room_selection = (
        state == "room_selection"
    )

    reviews_focus = (
        state == "reviews_focus"
    )

    rating = round(
        random.uniform(
            8.0,
            9.7,
        ),
        1,
    )

    city = random.choice(
        CITIES
    )

    rooms = [
        generate_room(
            sold_out=sold_out,
            force_deal=deal_heavy,
        )
        for _ in range(
            random.randint(
                3,
                6,
            )
        )
    ]

    reviews = [
        generate_review()
        for _ in range(
            random.randint(
                3,
                6,
            )
        )
    ]

    facility_pool = (
        FACILITIES.copy()
    )

    random.shuffle(
        facility_pool
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "gallery_focus":
            gallery_focus,

        "room_selection":
            room_selection,

        "deal_heavy":
            deal_heavy,

        "reviews_focus":
            reviews_focus,

        "sold_out":
            sold_out,

        # ------------------------------------------
        # Property
        # ------------------------------------------

        "name":
            random.choice(
                HOTEL_NAMES
            ),

        "city":
            city,

        "area":
            random.choice(
                AREAS
            ),

        "address":
            (
                f"{random.randint(10, 240)} "
                f"{random.choice(['Central', 'River', 'Park', 'City'])} "
                f"Street, {city}"
            ),

        "rating":
            rating,

        "review_count":
            random.randint(
                320,
                8200,
            ),

        "stars":
            random.randint(
                3,
                5,
            ),

        "description":
            random.choice(
                [
                    (
                        "Stay in the heart of the city with easy "
                        "access to shopping, restaurants and public transport."
                    ),
                    (
                        "A modern property offering spacious rooms, "
                        "comfortable facilities and an excellent location."
                    ),
                    (
                        "Enjoy stylish accommodation close to popular "
                        "attractions and major transport connections."
                    ),
                ]
            ),

        # ------------------------------------------
        # Gallery
        # ------------------------------------------

        "gallery":
            generate_gallery(),

        # ------------------------------------------
        # Facilities
        # ------------------------------------------

        "facilities":
            facility_pool[:6],

        # ------------------------------------------
        # Rooms
        # ------------------------------------------

        "rooms":
            rooms,

        # ------------------------------------------
        # Reviews
        # ------------------------------------------

        "reviews":
            reviews,

        # ------------------------------------------
        # Booking
        # ------------------------------------------

        "check_in":
            "Sep 18",

        "check_out":
            "Sep 21",

        "guests":
            random.choice(
                [
                    "2 adults · 1 room",
                    "1 adult · 1 room",
                    "2 adults · 1 child",
                    "3 adults · 2 rooms",
                ]
            ),

        "nights":
            3,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_hotel_detail_data()
    )

    print(
        "\n=============================="
    )

    print(
        "BOOKING HOTEL DETAIL"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Hotel:",
        data["name"],
    )

    print(
        "Gallery:",
        len(
            data["gallery"]
        ),
    )

    print(
        "Rooms:",
        len(
            data["rooms"]
        ),
    )

    print(
        "Reviews:",
        len(
            data["reviews"]
        ),
    )