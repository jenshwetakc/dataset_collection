from __future__ import annotations

import random

from faker import Faker


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Pools
# ==========================================================

ADDRESS_LABELS = [
    "Home",
    "Work",
    "School",
    "Apartment",
    "Office",
    "Gym",
]


SEARCH_PLACEHOLDERS = [
    "Search for an address",
    "Where should we deliver?",
    "Search street, building or area",
    "Enter your delivery address",
]


LOCATION_HINTS = [
    "Move the map to adjust your delivery location.",
    "Choose the exact place where you'd like your order delivered.",
    "Confirm the pin location for accurate delivery.",
]


SEOUL_DISTRICTS = [
    "Gangnam-gu",
    "Mapo-gu",
    "Songpa-gu",
    "Jongno-gu",
    "Seocho-gu",
    "Yongsan-gu",
    "Seodaemun-gu",
    "Yeongdeungpo-gu",
]


PLACE_TYPES = [
    "Apartment",
    "Office Building",
    "Residence",
    "Shopping Center",
    "University",
    "Station",
    "Cafe",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_korean_style_address() -> str:

    district = random.choice(
        SEOUL_DISTRICTS
    )

    road_number = random.randint(
        1,
        250,
    )

    building_number = random.randint(
        1,
        80,
    )

    return (
        f"{road_number} "
        f"{fake.street_name()}, "
        f"{district}, Seoul "
        f"{building_number}"
    )


def generate_address_detail() -> str:

    return random.choice(
        [
            f"Building {random.choice(['A', 'B', 'C', 'D'])}, "
            f"Room {random.randint(101, 2508)}",

            f"Apartment {random.randint(101, 3505)}",

            f"Floor {random.randint(2, 25)}",

            "Main entrance",

            "Leave at the front door",

            f"Unit {random.randint(1, 90)}",
        ]
    )


# ==========================================================
# Saved Address
# ==========================================================

def generate_saved_address(
    index: int,
) -> dict:

    label = random.choice(
        ADDRESS_LABELS
    )

    return {

        "id":
            index,

        "label":
            label,

        "address":
            generate_korean_style_address(),

        "detail":
            generate_address_detail(),

        "icon":
            {
                "Home":
                    "home",

                "Work":
                    "work",

                "School":
                    "school",

                "Apartment":
                    "apartment",

                "Office":
                    "business",

                "Gym":
                    "fitness_center",
            }.get(
                label,
                "location_on",
            ),

        "selected":
            False,
    }


# ==========================================================
# Recent Address
# ==========================================================

def generate_recent_address(
    index: int,
) -> dict:

    return {

        "id":
            index,

        "name":
            random.choice(
                [
                    fake.company(),
                    fake.city(),
                    fake.street_name(),
                    random.choice(
                        SEOUL_DISTRICTS
                    ),
                    f"{fake.first_name()} Building",
                ]
            ),

        "address":
            generate_korean_style_address(),

        "place_type":
            random.choice(
                PLACE_TYPES
            ),
    }


# ==========================================================
# Map Markers
# ==========================================================

def generate_map_markers() -> list[dict]:

    markers = []

    count = random.randint(
        5,
        9,
    )

    for index in range(
        count
    ):

        markers.append(
            {
                "id":
                    index,

                "left":
                    random.randint(
                        10,
                        88,
                    ),

                "top":
                    random.randint(
                        12,
                        76,
                    ),

                "icon":
                    random.choice(
                        [
                            "restaurant",
                            "storefront",
                            "local_cafe",
                            "apartment",
                            "location_on",
                        ]
                    ),

                "selected":
                    index == 0,
            }
        )

    return markers


# ==========================================================
# Main Generator
# ==========================================================

def generate_location_picker_data() -> dict:

    saved_addresses = [

        generate_saved_address(
            index
        )

        for index in range(
            random.randint(
                2,
                4,
            )
        )
    ]

    selected_index = random.randrange(
        len(
            saved_addresses
        )
    )

    saved_addresses[
        selected_index
    ][
        "selected"
    ] = True

    selected_address = (
        saved_addresses[
            selected_index
        ]
    )

    return {

        "page_title":
            random.choice(
                [
                    "Delivery location",
                    "Choose location",
                    "Set delivery address",
                ]
            ),

        "search_placeholder":
            random.choice(
                SEARCH_PLACEHOLDERS
            ),

        "location_hint":
            random.choice(
                LOCATION_HINTS
            ),

        "selected_address":
            selected_address,

        "saved_addresses":
            saved_addresses,

        "recent_addresses": [

            generate_recent_address(
                index
            )

            for index in range(
                random.randint(
                    4,
                    8,
                )
            )
        ],

        "map_markers":
            generate_map_markers(),

        "map_area":
            random.choice(
                SEOUL_DISTRICTS
            ),

        "location_accuracy":
            random.choice(
                [
                    "High accuracy",
                    "Within 20 m",
                    "Within 35 m",
                    "GPS location",
                ]
            ),
    }