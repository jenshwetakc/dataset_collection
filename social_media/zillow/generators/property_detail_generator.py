from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_property_image,
    get_random_interior_image,
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
    ("San Diego", "CA"),
    ("Portland", "OR"),
    ("Boston", "MA"),
    ("Miami", "FL"),
]


PROPERTY_TYPES = [
    "Single family residence",
    "Townhouse",
    "Condominium",
    "Detached home",
    "Contemporary home",
]


FEATURES = [
    "Hardwood flooring",
    "Central air",
    "Updated kitchen",
    "Walk-in closet",
    "Attached garage",
    "Fireplace",
    "Private patio",
    "Laundry room",
    "Stainless steel appliances",
    "Large backyard",
    "High ceilings",
    "Smart thermostat",
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    price: int,
) -> str:

    return f"${price:,}"


# ==========================================================
# Gallery
# ==========================================================

def generate_gallery() -> list[str]:

    images = []

    for index in range(
        5
    ):

        if index == 0:

            image = (
                get_random_property_image()
            )

        else:

            image = (
                get_random_interior_image()
                or get_random_property_image()
            )

        if image:

            images.append(
                image
            )

    return images


# ==========================================================
# Main Generator
# ==========================================================

def generate_property_detail_data() -> dict:

    city, state = random.choice(
        CITIES
    )

    price = random.randrange(
        280_000,
        2_800_000,
        5_000,
    )

    beds = random.randint(
        2,
        6,
    )

    baths = random.choice(
        [
            1.5,
            2,
            2.5,
            3,
            3.5,
            4,
        ]
    )

    sqft = random.randint(
        900,
        4500,
    )

    year_built = random.randint(
        1950,
        2025,
    )

    lot_size = round(
        random.uniform(
            0.08,
            1.8,
        ),
        2,
    )

    monthly_payment = round(
        price
        * random.uniform(
            0.0045,
            0.007,
        )
    )

    zestimate = round(
        price
        * random.uniform(
            0.94,
            1.06,
        )
    )

    property_tax = round(
        price
        * random.uniform(
            0.008,
            0.018,
        )
    )

    agent_name = fake.name()

    selected_features = random.sample(
        FEATURES,
        k=random.randint(
            6,
            10,
        ),
    )

    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "gallery":
            generate_gallery(),


        "listing": {

            "price":
                price,

            "price_text":
                format_price(
                    price
                ),

            "beds":
                beds,

            "baths":
                baths,

            "sqft":
                sqft,

            "property_type":
                random.choice(
                    PROPERTY_TYPES
                ),

            "address":
                fake.street_address(),

            "city":
                city,

            "state":
                state,

            "zipcode":
                fake.postcode(),

            "days_on_market":
                random.randint(
                    1,
                    72,
                ),

            "views":
                random.randint(
                    180,
                    14000,
                ),

            "saves":
                random.randint(
                    12,
                    1800,
                ),

            "status":
                random.choice(
                    [
                        "For sale",
                        "Active",
                        "New listing",
                    ]
                ),
        },


        "financial": {

            "monthly_payment":
                f"${monthly_payment:,}/mo",

            "zestimate":
                format_price(
                    zestimate
                ),

            "property_tax":
                f"${property_tax:,}/yr",

            "hoa":
                (
                    f"${random.randint(0, 850)}/mo"
                    if random.random() < 0.45
                    else "None"
                ),
        },


        "facts": [

            {
                "icon": "bed",
                "label": "Bedrooms",
                "value": str(beds),
            },

            {
                "icon": "bathtub",
                "label": "Bathrooms",
                "value": str(baths),
            },

            {
                "icon": "square_foot",
                "label": "Living area",
                "value": f"{sqft:,} sqft",
            },

            {
                "icon": "calendar_month",
                "label": "Year built",
                "value": str(year_built),
            },

            {
                "icon": "landscape",
                "label": "Lot",
                "value": f"{lot_size} acres",
            },

            {
                "icon": "home",
                "label": "Property type",
                "value": random.choice(
                    PROPERTY_TYPES
                ),
            },
        ],


        "description": (
            fake.paragraph(
                nb_sentences=random.randint(
                    5,
                    8,
                )
            )
            + " "
            + fake.paragraph(
                nb_sentences=random.randint(
                    3,
                    5,
                )
            )
        ),


        "features":
            selected_features,


        "agent": {

            "name":
                agent_name,

            "company":
                fake.company(),

            "phone":
                fake.phone_number(),

            "image":
                get_random_agent_image(),

            "rating":
                round(
                    random.uniform(
                        4.3,
                        5.0,
                    ),
                    1,
                ),

            "reviews":
                random.randint(
                    15,
                    640,
                ),
        },


        "contact": {

            "name":
                fake.name(),

            "email":
                fake.email(),

            "phone":
                fake.phone_number(),

            "message":
                (
                    "I am interested in this property "
                    "and would like more information."
                ),
        },


        "price_history": [

            {
                "date": "Today",
                "event": "Listed for sale",
                "price": format_price(
                    price
                ),
            },

            {
                "date": "2 years ago",
                "event": "Sold",
                "price": format_price(
                    round(
                        price
                        * random.uniform(
                            0.72,
                            0.88,
                        )
                    )
                ),
            },

            {
                "date": "5 years ago",
                "event": "Listed",
                "price": format_price(
                    round(
                        price
                        * random.uniform(
                            0.58,
                            0.75,
                        )
                    )
                ),
            },
        ],
    }