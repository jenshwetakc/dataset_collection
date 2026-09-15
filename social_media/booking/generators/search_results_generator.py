from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_hotel_image,
)


# ==========================================================
# States
# ==========================================================

RESULT_STATES = [
    "standard",
    "map_split",
    "filters_open",
    "sort_open",
    "compact_cards",
    "deal_heavy",
    "no_results",
]


SORT_OPTIONS = [
    "Our top picks",
    "Price: low to high",
    "Price: high to low",
    "Best reviewed",
    "Distance from center",
]


FILTERS = [
    "Free cancellation",
    "Breakfast included",
    "Hotels",
    "Apartments",
    "Resorts",
    "Swimming pool",
    "Parking",
    "Free WiFi",
]


HOTEL_NAMES = [
    "Central Park Hotel",
    "Skyline Residence",
    "Urban Nest Seoul",
    "Grand Riverside Hotel",
    "City View Suites",
    "The Modern Stay",
    "Metro Boutique Hotel",
    "Harbor Residence",
    "Royal Garden Hotel",
    "Blue River Suites",
]


AREAS = [
    "City Center",
    "Downtown",
    "Riverside",
    "Old Town",
    "Central District",
    "Business District",
]


# ==========================================================
# Property
# ==========================================================

def generate_property(
    force_deal: bool = False,
) -> dict:

    rating = round(
        random.uniform(
            7.4,
            9.8,
        ),
        1,
    )

    old_price = random.randint(
        120,
        460,
    )

    discount = random.randint(
        10,
        35,
    )

    deal = (
        True
        if force_deal
        else random.random() < 0.55
    )

    price = (
        round(
            old_price
            * (
                1 - discount / 100
            )
        )
        if deal
        else old_price
    )

    return {
        "name":
            random.choice(
                HOTEL_NAMES
            ),

        "area":
            random.choice(
                AREAS
            ),

        "distance":
            round(
                random.uniform(
                    0.2,
                    6.5,
                ),
                1,
            ),

        "image":
            get_random_hotel_image(),

        "rating":
            rating,

        "reviews":
            random.randint(
                80,
                7000,
            ),

        "price":
            price,

        "old_price":
            old_price,

        "discount":
            discount,

        "deal":
            deal,

        "favorite":
            random.random() < 0.30,

        "breakfast":
            random.random() < 0.50,

        "free_cancel":
            random.random() < 0.65,

        "limited":
            random.random() < 0.22,

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
# Generator
# ==========================================================

def generate_search_results_data() -> dict:

    state = random.choice(
        RESULT_STATES
    )

    deal_heavy = (
        state == "deal_heavy"
    )

    no_results = (
        state == "no_results"
    )

    result_count = (
        0
        if no_results
        else random.randint(
            7,
            14,
        )
    )

    properties = [
        generate_property(
            force_deal=deal_heavy
        )
        for _ in range(
            result_count
        )
    ]

    selected_filters = random.sample(
        FILTERS,
        k=random.randint(
            1,
            3,
        ),
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "show_map":
            state == "map_split",

        "filters_open":
            state == "filters_open",

        "sort_open":
            state == "sort_open",

        "compact_cards":
            state == "compact_cards",

        "no_results":
            no_results,

        # ------------------------------------------
        # Search
        # ------------------------------------------

        "destination":
            random.choice(
                [
                    "Seoul",
                    "Tokyo",
                    "Paris",
                    "London",
                    "Bangkok",
                ]
            ),

        "date_text":
            random.choice(
                [
                    "Sep 12 – Sep 15",
                    "Sep 18 – Sep 22",
                    "Oct 02 – Oct 05",
                    "Oct 10 – Oct 14",
                ]
            ),

        "guest_text":
            random.choice(
                [
                    "2 adults · 1 room",
                    "1 adult · 1 room",
                    "3 adults · 2 rooms",
                    "2 adults · 1 child",
                ]
            ),

        # ------------------------------------------
        # Filters
        # ------------------------------------------

        "filters":
            FILTERS.copy(),

        "selected_filters":
            selected_filters,

        # ------------------------------------------
        # Sort
        # ------------------------------------------

        "sort_options":
            SORT_OPTIONS.copy(),

        "selected_sort":
            random.choice(
                SORT_OPTIONS
            ),

        # ------------------------------------------
        # Results
        # ------------------------------------------

        "result_count":
            result_count,

        "properties":
            properties,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_search_results_data()
    )

    print(
        "State:",
        data[
            "state"
        ],
    )

    print(
        "Results:",
        data[
            "result_count"
        ],
    )