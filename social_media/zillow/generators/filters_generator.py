from __future__ import annotations

import random


# ==========================================================
# Constants
# ==========================================================

HOME_TYPES = [
    {
        "label": "Houses",
        "icon": "home",
        "semantic": "houses",
    },
    {
        "label": "Townhomes",
        "icon": "holiday_village",
        "semantic": "townhomes",
    },
    {
        "label": "Condos",
        "icon": "apartment",
        "semantic": "condos",
    },
    {
        "label": "Multi-family",
        "icon": "domain",
        "semantic": "multi_family",
    },
    {
        "label": "Lots / land",
        "icon": "landscape",
        "semantic": "lots_land",
    },
    {
        "label": "Manufactured",
        "icon": "house",
        "semantic": "manufactured",
    },
]


AMENITIES = [
    {
        "label": "Air conditioning",
        "icon": "ac_unit",
        "semantic": "air_conditioning",
    },
    {
        "label": "Garage",
        "icon": "garage",
        "semantic": "garage",
    },
    {
        "label": "Pool",
        "icon": "pool",
        "semantic": "pool",
    },
    {
        "label": "Waterfront",
        "icon": "water",
        "semantic": "waterfront",
    },
    {
        "label": "Fireplace",
        "icon": "fireplace",
        "semantic": "fireplace",
    },
    {
        "label": "View",
        "icon": "landscape",
        "semantic": "view",
    },
    {
        "label": "Basement",
        "icon": "foundation",
        "semantic": "basement",
    },
    {
        "label": "Single story",
        "icon": "home_work",
        "semantic": "single_story",
    },
]


LISTING_TYPES = [
    {
        "label": "For sale",
        "semantic": "for_sale",
    },
    {
        "label": "New construction",
        "semantic": "new_construction",
    },
    {
        "label": "Coming soon",
        "semantic": "coming_soon",
    },
    {
        "label": "Foreclosures",
        "semantic": "foreclosures",
    },
    {
        "label": "By owner",
        "semantic": "by_owner",
    },
]


BED_BATH_OPTIONS = [
    "Any",
    "1+",
    "2+",
    "3+",
    "4+",
    "5+",
]


SQUARE_FEET_OPTIONS = [
    "Any",
    "750",
    "1,000",
    "1,500",
    "2,000",
    "3,000",
]


LOT_SIZE_OPTIONS = [
    "Any",
    "2,000 sqft",
    "5,000 sqft",
    "0.25 acres",
    "0.5 acres",
    "1 acre",
]


KEYWORD_OPTIONS = [
    "Updated kitchen",
    "Large backyard",
    "Ocean view",
    "Home office",
    "Open floor plan",
    "Walk-in closet",
    "Newly renovated",
]


# ==========================================================
# Helper
# ==========================================================

def create_selected_items(
    items: list[dict],
    minimum: int = 1,
    maximum: int = 3,
) -> list[dict]:

    maximum = min(
        maximum,
        len(items),
    )

    selected_count = random.randint(
        minimum,
        maximum,
    )

    selected_indexes = set(
        random.sample(
            range(
                len(items)
            ),
            k=selected_count,
        )
    )

    result = []

    for index, item in enumerate(
        items
    ):

        value = dict(
            item
        )

        value[
            "selected"
        ] = (
            index
            in selected_indexes
        )

        result.append(
            value
        )

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_filters_data() -> dict:

    minimum_price = random.choice(
        [
            200_000,
            250_000,
            300_000,
            400_000,
            500_000,
        ]
    )

    maximum_price = random.choice(
        [
            700_000,
            850_000,
            1_000_000,
            1_250_000,
            1_500_000,
            2_000_000,
        ]
    )

    if maximum_price <= minimum_price:

        maximum_price = (
            minimum_price
            + 500_000
        )


    selected_beds = random.choice(
        BED_BATH_OPTIONS
    )

    selected_baths = random.choice(
        BED_BATH_OPTIONS
    )


    home_types = (
        create_selected_items(
            HOME_TYPES,
            minimum=1,
            maximum=3,
        )
    )


    amenities = (
        create_selected_items(
            AMENITIES,
            minimum=0,
            maximum=4,
        )
    )


    listing_types = (
        create_selected_items(
            LISTING_TYPES,
            minimum=1,
            maximum=3,
        )
    )


    selected_keywords = random.sample(
        KEYWORD_OPTIONS,
        k=random.randint(
            1,
            3,
        ),
    )


    active_count = (

        sum(
            item[
                "selected"
            ]
            for item
            in home_types
        )

        + sum(
            item[
                "selected"
            ]
            for item
            in amenities
        )

        + sum(
            item[
                "selected"
            ]
            for item
            in listing_types
        )

        + (
            0
            if selected_beds == "Any"
            else 1
        )

        + (
            0
            if selected_baths == "Any"
            else 1
        )

        + random.randint(
            1,
            4,
        )
    )


    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "location":
            random.choice(
                [
                    "Seattle, WA",
                    "Austin, TX",
                    "Denver, CO",
                    "San Diego, CA",
                    "Boston, MA",
                    "Portland, OR",
                ]
            ),


        "result_count":
            random.randint(
                80,
                3800,
            ),


        "active_filter_count":
            active_count,


        "listing_types":
            listing_types,


        "price": {

            "minimum":
                minimum_price,

            "maximum":
                maximum_price,

            "minimum_text":
                f"${minimum_price:,}",

            "maximum_text":
                f"${maximum_price:,}",

            "minimum_percent":
                round(
                    minimum_price
                    / 2_000_000
                    * 100
                ),

            "maximum_percent":
                min(
                    100,
                    round(
                        maximum_price
                        / 2_000_000
                        * 100
                    ),
                ),
        },


        "beds": {

            "options":
                BED_BATH_OPTIONS,

            "selected":
                selected_beds,
        },


        "baths": {

            "options":
                BED_BATH_OPTIONS,

            "selected":
                selected_baths,
        },


        "home_types":
            home_types,


        "square_feet": {

            "minimum":
                random.choice(
                    SQUARE_FEET_OPTIONS
                ),

            "maximum":
                random.choice(
                    SQUARE_FEET_OPTIONS[
                        2:
                    ]
                ),
        },


        "lot_size": {

            "minimum":
                random.choice(
                    LOT_SIZE_OPTIONS
                ),
        },


        "year_built": {

            "minimum":
                random.choice(
                    [
                        "",
                        "1950",
                        "1970",
                        "1990",
                        "2000",
                        "2010",
                    ]
                ),

            "maximum":
                random.choice(
                    [
                        "",
                        "2000",
                        "2010",
                        "2020",
                        "2026",
                    ]
                ),
        },


        "amenities":
            amenities,


        "toggles": [

            {
                "label":
                    "Open houses only",

                "description":
                    "Show homes with an upcoming open house.",

                "semantic":
                    "open_house_only",

                "enabled":
                    random.random()
                    < 0.35,
            },

            {
                "label":
                    "3D tours",

                "description":
                    "Only show listings with a virtual 3D tour.",

                "semantic":
                    "three_d_tour",

                "enabled":
                    random.random()
                    < 0.40,
            },

            {
                "label":
                    "Hide 55+ communities",

                "description":
                    "Exclude age-restricted communities.",

                "semantic":
                    "hide_senior_communities",

                "enabled":
                    random.random()
                    < 0.50,
            },

            {
                "label":
                    "Parking available",

                "description":
                    "Require at least one parking space.",

                "semantic":
                    "parking_available",

                "enabled":
                    random.random()
                    < 0.45,
            },
        ],


        "keywords":
            selected_keywords,


        "days_on_market":
            random.choice(
                [
                    "Any",
                    "1 day",
                    "7 days",
                    "14 days",
                    "30 days",
                    "90 days",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_filters_data()
    )

    print(
        "Location:",
        data[
            "location"
        ],
    )

    print(
        "Filters:",
        data[
            "active_filter_count"
        ],
    )

    print(
        "Results:",
        data[
            "result_count"
        ],
    )