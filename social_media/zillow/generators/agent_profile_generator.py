from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_agent_image,
    get_random_property_image,
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


SPECIALTIES = [
    "Buyer's agent",
    "Listing agent",
    "Relocation",
    "Luxury homes",
    "First-time buyers",
    "Investment properties",
    "New construction",
    "Condos",
]


LANGUAGES = [
    "English",
    "Spanish",
    "Korean",
    "French",
    "Chinese",
]


REVIEW_TEXTS = [
    (
        "Very responsive throughout the entire process and "
        "helped us understand each step clearly."
    ),
    (
        "Excellent local knowledge and strong communication. "
        "We always knew what was happening next."
    ),
    (
        "Made our home search much easier and helped us compare "
        "properties objectively."
    ),
    (
        "Professional, patient, and very knowledgeable about "
        "the neighborhoods we were considering."
    ),
    (
        "Helped us prepare a competitive offer and guided us "
        "through negotiations."
    ),
]


PROPERTY_TYPES = [
    "Single family home",
    "Condo",
    "Townhome",
    "New construction",
]


# ==========================================================
# Formatting
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
# Listing
# ==========================================================

def generate_listing(
    index: int,
    city: str,
    state: str,
) -> dict:

    price = random.randrange(
        280_000,
        2_200_000,
        5_000,
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
            random.randint(
                2,
                6,
            ),

        "baths":
            random.choice(
                [
                    1.5,
                    2,
                    2.5,
                    3,
                    3.5,
                    4,
                ]
            ),

        "sqft":
            random.randint(
                850,
                4200,
            ),

        "address":
            fake.street_address(),

        "city":
            city,

        "state":
            state,

        "image":
            get_random_property_image(),

        "property_type":
            random.choice(
                PROPERTY_TYPES
            ),

        "status":
            random.choice(
                [
                    "For sale",
                    "Pending",
                    "Open house",
                ]
            ),
    }


# ==========================================================
# Review
# ==========================================================

def generate_review(
    index: int,
) -> dict:

    reviewer_name = fake.first_name()

    rating = random.choice(
        [
            4,
            4.5,
            5,
            5,
            5,
        ]
    )

    return {

        "id":
            index,

        "reviewer":
            reviewer_name,

        "initial":
            reviewer_name[
                :1
            ].upper(),

        "rating":
            rating,

        "date":
            random.choice(
                [
                    "2 weeks ago",
                    "1 month ago",
                    "3 months ago",
                    "6 months ago",
                    "Last year",
                ]
            ),

        "service":
            random.choice(
                [
                    "Bought a home",
                    "Sold a home",
                    "Bought and sold",
                    "Local consultation",
                ]
            ),

        "text":
            random.choice(
                REVIEW_TEXTS
            ),
    }


# ==========================================================
# Sales History
# ==========================================================

def generate_sale(
    index: int,
) -> dict:

    city, state = random.choice(
        CITIES
    )

    price = random.randrange(
        300_000,
        2_000_000,
        5_000,
    )

    return {

        "id":
            index,

        "address":
            fake.street_address(),

        "city":
            city,

        "state":
            state,

        "price":
            price,

        "price_text":
            format_price(
                price
            ),

        "date":
            random.choice(
                [
                    "Aug 2026",
                    "Jul 2026",
                    "Jun 2026",
                    "May 2026",
                    "Apr 2026",
                ]
            ),

        "side":
            random.choice(
                [
                    "Buyer",
                    "Seller",
                    "Buyer & seller",
                ]
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_agent_profile_data() -> dict:

    city, state = random.choice(
        CITIES
    )

    agent_name = fake.name()

    total_sales = random.randint(
        70,
        940,
    )

    sales_last_year = random.randint(
        8,
        72,
    )

    minimum_price = random.randrange(
        250_000,
        500_000,
        25_000,
    )

    maximum_price = random.randrange(
        1_200_000,
        4_000_000,
        50_000,
    )

    average_price = random.randrange(
        450_000,
        1_500_000,
        10_000,
    )

    rating = round(
        random.uniform(
            4.6,
            5.0,
        ),
        1,
    )

    review_count = random.randint(
        24,
        480,
    )

    specialties = random.sample(
        SPECIALTIES,
        k=random.randint(
            3,
            6,
        ),
    )

    languages = random.sample(
        LANGUAGES,
        k=random.randint(
            1,
            3,
        ),
    )

    active_listings = [

        generate_listing(
            index,
            city,
            state,
        )

        for index in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    reviews = [

        generate_review(
            index
        )

        for index in range(
            random.randint(
                5,
                8,
            )
        )
    ]

    sales = [

        generate_sale(
            index
        )

        for index in range(
            random.randint(
                5,
                8,
            )
        )
    ]

    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "agent": {

            "name":
                agent_name,

            "first_name":
                agent_name.split()[0],

            "image":
                get_random_agent_image(),

            "initial":
                agent_name[
                    :1
                ].upper(),

            "company":
                fake.company(),

            "location":
                f"{city}, {state}",

            "team":
                random.choice(
                    [
                        None,
                        f"{fake.last_name()} Real Estate Team",
                        f"The {fake.last_name()} Group",
                    ]
                ),

            "verified":
                random.random()
                < 0.75,

            "rating":
                rating,

            "review_count":
                review_count,

            "total_sales":
                total_sales,

            "sales_last_year":
                sales_last_year,

            "minimum_price":
                minimum_price,

            "maximum_price":
                maximum_price,

            "price_range":
                (
                    f"{compact_price(minimum_price)}"
                    f" – "
                    f"{compact_price(maximum_price)}"
                ),

            "average_price":
                average_price,

            "average_price_text":
                format_price(
                    average_price
                ),

            "years_experience":
                random.randint(
                    4,
                    28,
                ),

            "phone":
                fake.phone_number(),

            "specialties":
                specialties,

            "languages":
                languages,

            "bio":
                (
                    fake.paragraph(
                        nb_sentences=5
                    )
                    + " "
                    + fake.paragraph(
                        nb_sentences=4
                    )
                ),
        },


        "active_listings":
            active_listings,


        "reviews":
            reviews,


        "sales":
            sales,


        "rating_breakdown": [

            {
                "label": "Local knowledge",
                "value": round(
                    random.uniform(
                        4.5,
                        5.0,
                    ),
                    1,
                ),
            },

            {
                "label": "Process expertise",
                "value": round(
                    random.uniform(
                        4.4,
                        5.0,
                    ),
                    1,
                ),
            },

            {
                "label": "Responsiveness",
                "value": round(
                    random.uniform(
                        4.5,
                        5.0,
                    ),
                    1,
                ),
            },

            {
                "label": "Negotiation skills",
                "value": round(
                    random.uniform(
                        4.3,
                        5.0,
                    ),
                    1,
                ),
            },
        ],


        "mobile_navigation": [

            {
                "label": "Home",
                "icon": "home",
                "active": False,
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
                "label": "Agents",
                "icon": "support_agent",
                "active": True,
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
        generate_agent_profile_data()
    )

    print(
        "Agent:",
        data[
            "agent"
        ][
            "name"
        ],
    )

    print(
        "Rating:",
        data[
            "agent"
        ][
            "rating"
        ],
    )

    print(
        "Listings:",
        len(
            data[
                "active_listings"
            ]
        ),
    )