from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_destination_image,
    get_random_landmark_image,
)


# ==========================================================
# States
# ==========================================================

ATTRACTION_STATES = [
    "standard",
    "category_focus",
    "time_slots",
    "map_split",
    "ticket_drawer",
    "sold_out",
]


CATEGORIES = [
    {
        "label": "Museums",
        "icon": "museum",
    },
    {
        "label": "Tours",
        "icon": "tour",
    },
    {
        "label": "Landmarks",
        "icon": "location_city",
    },
    {
        "label": "Food",
        "icon": "restaurant",
    },
    {
        "label": "Shows",
        "icon": "theater_comedy",
    },
    {
        "label": "Outdoors",
        "icon": "nature",
    },
]


ATTRACTION_NAMES = [
    "City Highlights Walking Tour",
    "National Museum Admission",
    "River Night Cruise",
    "Historic Palace Experience",
    "Observation Deck Ticket",
    "Street Food Discovery Tour",
    "Traditional Culture Experience",
    "City Bike Tour",
    "Modern Art Museum",
    "Evening City Lights Tour",
]


LOCATIONS = [
    "Seoul",
    "Tokyo",
    "Paris",
    "London",
    "Singapore",
    "Bangkok",
]


DURATIONS = [
    "1 hour",
    "1.5 hours",
    "2 hours",
    "3 hours",
    "Half day",
]


TIME_SLOTS = [
    "09:00",
    "10:30",
    "12:00",
    "14:00",
    "15:30",
    "17:00",
    "19:00",
]


# ==========================================================
# Attraction
# ==========================================================

def generate_attraction(
    *,
    force_sold_out: bool = False,
) -> dict:

    category = random.choice(
        CATEGORIES
    )

    rating = round(
        random.uniform(
            7.6,
            9.8,
        ),
        1,
    )

    old_price = random.randint(
        25,
        160,
    )

    deal = random.random() < 0.35

    discount = random.randint(
        10,
        25,
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

    sold_out = (
        force_sold_out
        or random.random() < 0.10
    )

    slots = random.sample(
        TIME_SLOTS,
        k=random.randint(
            3,
            6,
        ),
    )

    return {
        "name":
            random.choice(
                ATTRACTION_NAMES
            ),

        "category":
            category["label"],

        "category_icon":
            category["icon"],

        "location":
            random.choice(
                LOCATIONS
            ),

        "image":
            get_random_landmark_image()
            or get_random_destination_image(),

        "rating":
            rating,

        "reviews":
            random.randint(
                80,
                5200,
            ),

        "duration":
            random.choice(
                DURATIONS
            ),

        "price":
            price,

        "old_price":
            old_price,

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),

        "deal":
            deal,

        "discount":
            discount,

        "instant_confirmation":
            random.random() < 0.65,

        "free_cancel":
            random.random() < 0.60,

        "skip_line":
            random.random() < 0.35,

        "sold_out":
            sold_out,

        "limited":
            (
                not sold_out
                and random.random() < 0.20
            ),

        "time_slots":
            slots,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_attractions_data() -> dict:

    state = random.choice(
        ATTRACTION_STATES
    )

    sold_out_state = (
        state == "sold_out"
    )

    attractions = [
        generate_attraction(
            force_sold_out=
                sold_out_state
        )
        for _ in range(
            random.randint(
                6,
                10,
            )
        )
    ]

    selected_attraction = (
        random.choice(
            attractions
        )
    )

    category_pool = (
        CATEGORIES.copy()
    )

    random.shuffle(
        category_pool
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "category_focus":
            state == "category_focus",

        "time_slots_open":
            state == "time_slots",

        "map_split":
            state == "map_split",

        "ticket_drawer":
            state == "ticket_drawer",

        "sold_out_state":
            sold_out_state,

        # ------------------------------------------
        # Search
        # ------------------------------------------

        "destination":
            random.choice(
                LOCATIONS
            ),

        "date":
            random.choice(
                [
                    "Sep 18",
                    "Sep 19",
                    "Sep 20",
                    "Sep 21",
                ]
            ),

        # ------------------------------------------
        # Categories
        # ------------------------------------------

        "categories":
            category_pool,

        "selected_category":
            category_pool[0]["label"],

        # ------------------------------------------
        # Results
        # ------------------------------------------

        "attractions":
            attractions,

        "selected_attraction":
            selected_attraction,

        # ------------------------------------------
        # Sort
        # ------------------------------------------

        "sort":
            random.choice(
                [
                    "Recommended",
                    "Top rated",
                    "Lowest price",
                    "Most popular",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_attractions_data()
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Attractions:",
        len(
            data["attractions"]
        ),
    )