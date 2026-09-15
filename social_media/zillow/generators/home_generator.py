from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_hero_image,
    get_random_property_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

PROPERTY_TYPES = [
    "House for sale",
    "Condo for sale",
    "Townhouse for sale",
    "Single family home",
    "New construction",
    "Coming soon",
]


HOME_STYLES = [
    "Modern",
    "Contemporary",
    "Traditional",
    "Craftsman",
    "Ranch",
    "Colonial",
    "Mediterranean",
]


LISTING_BADGES = [
    "New",
    "Open house",
    "Price cut",
    "3D Home",
    "New construction",
    "Featured",
    None,
    None,
    None,
]


CITY_STATE_PAIRS = [
    ("Seattle", "WA"),
    ("Bellevue", "WA"),
    ("Austin", "TX"),
    ("Denver", "CO"),
    ("Portland", "OR"),
    ("San Diego", "CA"),
    ("Los Angeles", "CA"),
    ("Phoenix", "AZ"),
    ("Charlotte", "NC"),
    ("Atlanta", "GA"),
    ("Chicago", "IL"),
    ("Boston", "MA"),
    ("Miami", "FL"),
    ("Nashville", "TN"),
    ("Dallas", "TX"),
]


HERO_HEADLINES = [
    "Find your way home",
    "A home is waiting for you",
    "Discover a place you'll love",
    "Start your next move",
]


HERO_SUBTITLES = [
    "Search homes, rentals, neighborhoods and more.",
    "Explore homes that match your life and your budget.",
    "Discover places to buy, rent and call home.",
    "Your next home search starts here.",
]


SEARCH_PLACEHOLDERS = [
    "Enter an address, neighborhood, city, or ZIP code",
    "Search by city, neighborhood, or address",
    "Where do you want to live?",
    "Search homes and neighborhoods",
]


# ==========================================================
# Formatting Helpers
# ==========================================================

def format_price(
    value: int,
) -> str:

    return (
        "$"
        f"{value:,}"
    )


def format_compact_price(
    value: int,
) -> str:

    if value >= 1_000_000:

        return (
            "$"
            f"{value / 1_000_000:.1f}M"
        )

    if value >= 1_000:

        return (
            "$"
            f"{round(value / 1000)}K"
        )

    return format_price(
        value
    )


# ==========================================================
# Location
# ==========================================================

def generate_location() -> dict:

    city, state = random.choice(
        CITY_STATE_PAIRS
    )

    zipcode = fake.postcode()

    return {
        "city": city,
        "state": state,
        "zipcode": zipcode,
    }


# ==========================================================
# Property
# ==========================================================

def generate_property(
    index: int,
) -> dict:

    location = (
        generate_location()
    )

    price = random.randrange(
        180_000,
        2_600_000,
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
            5,
        ]
    )

    square_feet = random.randint(
        650,
        4_800,
    )

    lot_size = round(
        random.uniform(
            0.08,
            2.5,
        ),
        2,
    )

    days_on_market = random.randint(
        0,
        85,
    )

    monthly_estimate = round(
        price
        * random.uniform(
            0.004,
            0.007,
        )
    )

    badge = random.choice(
        LISTING_BADGES
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
            format_compact_price(
                price
            ),

        "beds":
            beds,

        "baths":
            baths,

        "sqft":
            square_feet,

        "lot_size":
            lot_size,

        "property_type":
            random.choice(
                PROPERTY_TYPES
            ),

        "style":
            random.choice(
                HOME_STYLES
            ),

        "address":
            fake.street_address(),

        "city":
            location[
                "city"
            ],

        "state":
            location[
                "state"
            ],

        "zipcode":
            location[
                "zipcode"
            ],

        "image":
            get_random_property_image(),

        "badge":
            badge,

        "days_on_market":
            days_on_market,

        "monthly_estimate":
            f"${monthly_estimate:,}/mo",

        "favorite":
            random.random()
            < 0.25,

        "featured":
            random.random()
            < 0.20,

        "open_house":
            random.random()
            < 0.20,
    }


# ==========================================================
# Action Card
# ==========================================================

def generate_action_cards() -> list[dict]:

    return [

        {
            "title":
                "Buy a home",

            "description":
                (
                    "Find your place with immersive photos, "
                    "local information and powerful search."
                ),

            "button_text":
                "Search homes",

            "icon":
                "home",

            "semantic":
                "buy_home",
        },

        {
            "title":
                "Sell a home",

            "description":
                (
                    "Explore your home's value and learn "
                    "about different ways to sell."
                ),

            "button_text":
                "See your options",

            "icon":
                "sell",

            "semantic":
                "sell_home",
        },

        {
            "title":
                "Rent a home",

            "description":
                (
                    "Discover apartments, houses and "
                    "townhomes available for rent."
                ),

            "button_text":
                "Find rentals",

            "icon":
                "apartment",

            "semantic":
                "rent_home",
        },
    ]


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> dict:

    return {

        "left": [
            "Buy",
            "Rent",
            "Sell",
        ],

        "right": [
            "Home Loans",
            "Agent finder",
            "Manage Rentals",
        ],

        "mobile": [

            {
                "label": "Home",
                "icon": "home",
                "active": True,
            },

            {
                "label": "Search",
                "icon": "search",
                "active": False,
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
# Main Generator
# ==========================================================

def generate_home_data() -> dict:

    featured_properties = [

        generate_property(
            index
        )

        for index in range(
            random.randint(
                5,
                8,
            )
        )
    ]


    recommended_properties = [

        generate_property(
            index + 100
        )

        for index in range(
            random.randint(
                4,
                7,
            )
        )
    ]


    recently_viewed = [

        generate_property(
            index + 200
        )

        for index in range(
            random.randint(
                3,
                5,
            )
        )
    ]


    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "navigation":
            generate_navigation(),


        "hero": {

            "title":
                random.choice(
                    HERO_HEADLINES
                ),

            "subtitle":
                random.choice(
                    HERO_SUBTITLES
                ),

            "search_placeholder":
                random.choice(
                    SEARCH_PLACEHOLDERS
                ),

            "image":
                get_random_hero_image(),

            "search_mode":
                random.choice(
                    [
                        "Buy",
                        "Rent",
                        "Buy",
                        "Buy",
                    ]
                ),
        },


        "featured": {

            "title":
                random.choice(
                    [
                        "Homes for you",
                        "Recommended homes",
                        "Explore homes you may like",
                    ]
                ),

            "subtitle":
                random.choice(
                    [
                        "Based on homes you viewed",
                        "Fresh listings selected for you",
                        "New possibilities for your search",
                    ]
                ),

            "properties":
                featured_properties,
        },


        "actions":
            generate_action_cards(),


        "recommended": {

            "title":
                random.choice(
                    [
                        "Explore more homes",
                        "More homes to discover",
                        "Homes worth a look",
                    ]
                ),

            "properties":
                recommended_properties,
        },


        "recent": {

            "title":
                "Recently viewed",

            "properties":
                recently_viewed,
        },


        "footer": {

            "links": [
                "About",
                "Zestimates",
                "Research",
                "Careers",
                "Help",
                "Privacy",
                "Terms",
            ],

            "copyright":
                "Synthetic real estate interface",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_home_data()
    )

    print(
        "Hero:",
        data[
            "hero"
        ][
            "title"
        ],
    )

    print(
        "Featured properties:",
        len(
            data[
                "featured"
            ][
                "properties"
            ]
        ),
    )

    for property_data in (
        data[
            "featured"
        ][
            "properties"
        ][:3]
    ):

        print(
            property_data[
                "price_text"
            ],
            property_data[
                "address"
            ],
        )