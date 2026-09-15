from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_property_image,
)


fake = Faker()


# ==========================================================
# Search Locations
# ==========================================================

LOCATIONS = [
    ("Seattle", "WA"),
    ("Bellevue", "WA"),
    ("Austin", "TX"),
    ("Denver", "CO"),
    ("Portland", "OR"),
    ("San Diego", "CA"),
    ("Phoenix", "AZ"),
    ("Charlotte", "NC"),
    ("Atlanta", "GA"),
    ("Boston", "MA"),
    ("Miami", "FL"),
    ("Nashville", "TN"),
]


PROPERTY_TYPES = [
    "House for sale",
    "Condo for sale",
    "Townhouse for sale",
    "New construction",
    "Single family home",
]


BADGES = [
    "New",
    "Open house",
    "Price cut",
    "3D Home",
    "New construction",
    None,
    None,
    None,
]


MAP_ROAD_NAMES = [
    "Pine St",
    "Lake Ave",
    "Madison St",
    "Broadway",
    "Oak Rd",
    "Main St",
    "Cedar Ave",
    "Market St",
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    value: int,
) -> str:

    return f"${value:,}"


def compact_price(
    value: int,
) -> str:

    if value >= 1_000_000:

        return (
            f"${value / 1_000_000:.1f}M"
        )

    return (
        f"${round(value / 1000)}K"
    )


# ==========================================================
# Property
# ==========================================================

def generate_property(
    index: int,
    city: str,
    state: str,
) -> dict:

    price = random.randrange(
        220_000,
        2_800_000,
        5_000,
    )

    beds = random.randint(
        1,
        6,
    )

    baths = random.choice(
        [
            1,
            1.5,
            2,
            2.5,
            3,
            3.5,
            4,
        ]
    )

    sqft = random.randint(
        600,
        4200,
    )

    return {

        "id":
            index,

        "price":
            price,

        "price_text":
            format_price(
                price
            ),

        "compact_price":
            compact_price(
                price
            ),

        "beds":
            beds,

        "baths":
            baths,

        "sqft":
            sqft,

        "address":
            fake.street_address(),

        "city":
            city,

        "state":
            state,

        "zipcode":
            fake.postcode(),

        "property_type":
            random.choice(
                PROPERTY_TYPES
            ),

        "image":
            get_random_property_image(),

        "badge":
            random.choice(
                BADGES
            ),

        "favorite":
            random.random()
            < 0.22,

        "days_on_market":
            random.randint(
                0,
                70,
            ),

        "broker":
            fake.company(),

        "latitude_offset":
            random.uniform(
                8,
                92,
            ),

        "longitude_offset":
            random.uniform(
                8,
                92,
            ),
    }


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> list[dict]:

    return [

        {
            "label":
                "For sale",

            "icon":
                "keyboard_arrow_down",

            "active":
                True,

            "semantic":
                "listing_type_filter",
        },

        {
            "label":
                "Price",

            "icon":
                "keyboard_arrow_down",

            "active":
                False,

            "semantic":
                "price_filter",
        },

        {
            "label":
                "Beds & baths",

            "icon":
                "keyboard_arrow_down",

            "active":
                False,

            "semantic":
                "beds_baths_filter",
        },

        {
            "label":
                "Home type",

            "icon":
                "keyboard_arrow_down",

            "active":
                False,

            "semantic":
                "home_type_filter",
        },

        {
            "label":
                "More",

            "icon":
                "tune",

            "active":
                False,

            "semantic":
                "more_filters",
        },
    ]


# ==========================================================
# Map Roads
# ==========================================================

def generate_map_roads() -> list[dict]:

    roads = []

    for index in range(
        7
    ):

        roads.append(
            {
                "name":
                    random.choice(
                        MAP_ROAD_NAMES
                    ),

                "top":
                    random.randint(
                        5,
                        90,
                    ),

                "rotation":
                    random.randint(
                        -30,
                        30,
                    ),

                "width":
                    random.randint(
                        45,
                        110,
                    ),
            }
        )

    return roads


# ==========================================================
# Main Generator
# ==========================================================

def generate_search_results_data() -> dict:

    city, state = random.choice(
        LOCATIONS
    )

    count = random.randint(
        14,
        24,
    )

    properties = [

        generate_property(
            index=index,
            city=city,
            state=state,
        )

        for index in range(
            count
        )
    ]

    result_count = random.randint(
        220,
        3800,
    )

    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "location": {
            "city": city,
            "state": state,
            "query":
                f"{city}, {state}",
        },


        "filters":
            generate_filters(),


        "summary": {

            "title":
                f"{city} {state} Real Estate & Homes For Sale",

            "result_count":
                result_count,

            "result_count_text":
                f"{result_count:,} results",

            "sort":
                random.choice(
                    [
                        "Homes for You",
                        "Newest",
                        "Price: Low to High",
                        "Price: High to Low",
                    ]
                ),
        },


        "properties":
            properties,


        "map": {

            "roads":
                generate_map_roads(),

            "show_transit":
                random.random()
                < 0.5,

            "show_parks":
                random.random()
                < 0.7,
        },


        "mobile_navigation": [

            {
                "label": "Home",
                "icon": "home",
                "active": False,
            },

            {
                "label": "Search",
                "icon": "search",
                "active": True,
            },

            {
                "label": "Saved",
                "icon": "favorite",
                "active": False,
            },

            {
                "label": "Updates",
                "icon": "notifications",
                "active": False,
            },

            {
                "label": "Profile",
                "icon": "person",
                "active": False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_search_results_data()
    )

    print(
        data[
            "summary"
        ][
            "title"
        ]
    )

    print(
        "Properties:",
        len(
            data[
                "properties"
            ]
        )
    )