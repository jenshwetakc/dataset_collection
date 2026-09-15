from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_property_image,
    get_random_agent_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

CITIES = [
    ("Seattle", "WA"),
    ("Bellevue", "WA"),
    ("Austin", "TX"),
    ("Denver", "CO"),
    ("Portland", "OR"),
    ("San Diego", "CA"),
    ("Boston", "MA"),
    ("Miami", "FL"),
]


PROPERTY_TYPES = [
    "House",
    "Condo",
    "Townhome",
    "New construction",
    "Single family",
]


PRICE_CHANGE_OPTIONS = [
    -50000,
    -30000,
    -25000,
    -15000,
    -10000,
    0,
    0,
    0,
    10000,
]


# ==========================================================
# Formatting
# ==========================================================

def format_price(
    value: int,
) -> str:

    return (
        "$"
        f"{value:,}"
    )


# ==========================================================
# Saved Property
# ==========================================================

def generate_saved_property(
    index: int,
) -> dict:

    city, state = random.choice(
        CITIES
    )

    price = random.randrange(
        250_000,
        2_300_000,
        5_000,
    )

    price_change = random.choice(
        PRICE_CHANGE_OPTIONS
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
        650,
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

        "price_change":
            price_change,

        "price_change_text":
            (
                (
                    f"-${abs(price_change):,}"
                )
                if price_change < 0

                else (
                    f"+${price_change:,}"
                    if price_change > 0
                    else None
                )
            ),

        "price_decreased":
            price_change < 0,

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

        "saved_days":
            random.randint(
                1,
                140,
            ),

        "note":
            (
                random.choice(
                    [
                        "Great neighborhood",
                        "Love the kitchen",
                        "Close to work",
                        "Good backyard",
                        "Potential favorite",
                        "",
                        "",
                    ]
                )
            ),

        "has_open_house":
            random.random()
            < 0.20,

        "pending":
            random.random()
            < 0.08,
    }


# ==========================================================
# Folder
# ==========================================================

def generate_folders() -> list[dict]:

    names = [
        "All saved",
        "Favorites",
        "Weekend tours",
        "Family picks",
        "Maybe",
    ]

    result = []

    for index, name in enumerate(
        names
    ):

        result.append(
            {
                "name":
                    name,

                "count":
                    random.randint(
                        2,
                        24,
                    ),

                "icon":
                    (
                        "favorite"
                        if name == "Favorites"
                        else (
                            "calendar_month"
                            if name == "Weekend tours"
                            else (
                                "group"
                                if name == "Family picks"
                                else "folder"
                            )
                        )
                    ),

                "active":
                    index == 0,
            }
        )

    return result


# ==========================================================
# Collaborators
# ==========================================================

def generate_collaborators() -> list[dict]:

    collaborators = []

    for index in range(
        random.randint(
            2,
            5,
        )
    ):

        collaborators.append(
            {
                "name":
                    fake.first_name(),

                "image":
                    get_random_agent_image(),

                "initials":
                    fake.first_name()[
                        :1
                    ].upper(),

                "owner":
                    index == 0,
            }
        )

    return collaborators


# ==========================================================
# Saved Searches
# ==========================================================

def generate_saved_searches() -> list[dict]:

    result = []

    for index in range(
        random.randint(
            3,
            5,
        )
    ):

        city, state = random.choice(
            CITIES
        )

        minimum = random.choice(
            [
                250_000,
                350_000,
                450_000,
                600_000,
            ]
        )

        maximum = minimum + random.choice(
            [
                300_000,
                500_000,
                750_000,
                1_000_000,
            ]
        )

        result.append(
            {
                "name":
                    random.choice(
                        [
                            f"{city} homes",
                            f"{city} family homes",
                            f"{city} under budget",
                            f"{city} favorites",
                        ]
                    ),

                "location":
                    f"{city}, {state}",

                "criteria":
                    (
                        f"${minimum // 1000}K–"
                        f"${maximum // 1000}K · "
                        f"{random.randint(2, 4)}+ beds"
                    ),

                "new_count":
                    random.randint(
                        0,
                        14,
                    ),

                "alerts_enabled":
                    random.random()
                    < 0.75,

                "frequency":
                    random.choice(
                        [
                            "Instant",
                            "Daily",
                            "Weekly",
                        ]
                    ),
            }
        )

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_saved_homes_data() -> dict:

    properties = [

        generate_saved_property(
            index
        )

        for index in range(
            random.randint(
                10,
                18,
            )
        )
    ]

    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "user": {

            "name":
                fake.first_name(),

            "avatar":
                get_random_agent_image(),
        },


        "folders":
            generate_folders(),


        "properties":
            properties,


        "summary": {

            "title":
                random.choice(
                    [
                        "Saved homes",
                        "Your saved homes",
                        "Homes you're watching",
                    ]
                ),

            "count":
                len(
                    properties
                ),

            "sort":
                random.choice(
                    [
                        "Recently saved",
                        "Price: low to high",
                        "Price: high to low",
                        "Newest listing",
                    ]
                ),

            "view_mode":
                random.choice(
                    [
                        "grid",
                        "grid",
                        "list",
                    ]
                ),
        },


        "collaboration": {

            "title":
                random.choice(
                    [
                        "Family home search",
                        "Our favorites",
                        "Home shortlist",
                    ]
                ),

            "collaborators":
                generate_collaborators(),

            "shared":
                True,
        },


        "saved_searches":
            generate_saved_searches(),


        "mobile_navigation": [

            {
                "label":
                    "Home",

                "icon":
                    "home",

                "active":
                    False,
            },

            {
                "label":
                    "Search",

                "icon":
                    "search",

                "active":
                    False,
            },

            {
                "label":
                    "Saved",

                "icon":
                    "favorite",

                "active":
                    True,
            },

            {
                "label":
                    "Updates",

                "icon":
                    "notifications",

                "active":
                    False,
            },

            {
                "label":
                    "Profile",

                "icon":
                    "person",

                "active":
                    False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_saved_homes_data()
    )

    print(
        "Saved homes:",
        len(
            data[
                "properties"
            ]
        )
    )

    print(
        "Saved searches:",
        len(
            data[
                "saved_searches"
            ]
        )
    )