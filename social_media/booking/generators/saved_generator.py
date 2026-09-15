from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_hotel_image,
)


# ==========================================================
# States
# ==========================================================

SAVED_STATES = [
    "grid",
    "list",
    "collection",
    "empty",
    "share_dialog",
    "remove_confirmation",
]


HOTEL_NAMES = [
    "Grand Central Hotel",
    "The Metropolitan",
    "Royal Garden Hotel",
    "Skyline Residence",
    "Ocean View Resort",
    "Riverside Boutique Hotel",
    "Urban Stay Suites",
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


COLLECTION_NAMES = [
    "Summer trip",
    "Weekend ideas",
    "Seoul favorites",
    "Dream stays",
    "City breaks",
]


# ==========================================================
# Saved Property
# ==========================================================

def generate_saved_property() -> dict:

    price = random.randint(
        90,
        420,
    )

    rating = round(
        random.uniform(
            7.5,
            9.8,
        ),
        1,
    )

    return {
        "name":
            random.choice(
                HOTEL_NAMES
            ),

        "city":
            random.choice(
                CITIES
            ),

        "image":
            get_random_hotel_image(),

        "rating":
            rating,

        "reviews":
            random.randint(
                120,
                6500,
            ),

        "price":
            price,

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),

        "deal":
            random.random() < 0.45,

        "breakfast":
            random.random() < 0.50,

        "free_cancel":
            random.random() < 0.65,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_saved_data() -> dict:

    state = random.choice(
        SAVED_STATES
    )

    empty = (
        state == "empty"
    )

    properties = (
        []
        if empty
        else [
            generate_saved_property()
            for _ in range(
                random.randint(
                    5,
                    10,
                )
            )
        ]
    )

    selected_property = (
        random.choice(
            properties
        )
        if properties
        else None
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "grid_view":
            state == "grid",

        "list_view":
            state == "list",

        "collection_view":
            state == "collection",

        "empty":
            empty,

        "share_dialog":
            state == "share_dialog",

        "remove_confirmation":
            state == "remove_confirmation",

        # ------------------------------------------
        # Page
        # ------------------------------------------

        "title":
            "Saved",

        "subtitle":
            "Places you saved for later.",

        # ------------------------------------------
        # Collection
        # ------------------------------------------

        "collection_name":
            random.choice(
                COLLECTION_NAMES
            ),

        "collection_description":
            random.choice(
                [
                    "Properties for your next getaway.",
                    "Favorite stays for an upcoming trip.",
                    "Places worth visiting later.",
                ]
            ),

        # ------------------------------------------
        # Properties
        # ------------------------------------------

        "properties":
            properties,

        "selected_property":
            selected_property,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_saved_data()

    print(
        "State:",
        data["state"],
    )

    print(
        "Properties:",
        len(
            data["properties"]
        ),
    )