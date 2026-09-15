from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
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


MARKET_LABELS = [
    "Strong seller demand",
    "Balanced market",
    "Competitive market",
    "High buyer activity",
    "Moderate demand",
]


TASK_OPTIONS = [
    {
        "title": "Review your home facts",
        "description": (
            "Keep bedrooms, bathrooms and other "
            "property details up to date."
        ),
        "icon": "fact_check",
        "semantic": "review_home_facts",
    },
    {
        "title": "Add home improvements",
        "description": (
            "Record renovations or upgrades that "
            "may help improve your home profile."
        ),
        "icon": "construction",
        "semantic": "add_home_improvements",
    },
    {
        "title": "Explore selling options",
        "description": (
            "See possible ways to prepare and "
            "market your home."
        ),
        "icon": "sell",
        "semantic": "explore_selling_options",
    },
    {
        "title": "Check nearby sales",
        "description": (
            "Review recently sold homes around "
            "your neighborhood."
        ),
        "icon": "location_city",
        "semantic": "check_nearby_sales",
    },
]


# ==========================================================
# Formatting
# ==========================================================

def format_price(
    value: int | float,
) -> str:

    return (
        "$"
        f"{round(value):,}"
    )


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
# Value History
# ==========================================================

def generate_value_history(
    current_value: int,
) -> list[dict]:

    labels = [
        "Sep",
        "Oct",
        "Nov",
        "Dec",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
    ]

    starting_value = int(
        current_value
        * random.uniform(
            0.88,
            0.97,
        )
    )

    values = []

    value = (
        starting_value
    )

    for index, label in enumerate(
        labels
    ):

        if index == (
            len(
                labels
            )
            - 1
        ):

            value = (
                current_value
            )

        else:

            value += random.randint(
                -12_000,
                25_000,
            )

        values.append(
            {
                "label":
                    label,

                "value":
                    value,

                "value_text":
                    format_price(
                        value
                    ),
            }
        )

    minimum = min(
        item[
            "value"
        ]
        for item in values
    )

    maximum = max(
        item[
            "value"
        ]
        for item in values
    )

    difference = max(
        1,
        maximum
        - minimum
    )

    for item in values:

        item[
            "height_percent"
        ] = (
            22
            +
            round(
                (
                    item[
                        "value"
                    ]
                    - minimum
                )
                /
                difference
                *
                70
            )
        )

    return values


# ==========================================================
# Comparable Home
# ==========================================================

def generate_comparable(
    index: int,
    city: str,
    state: str,
    current_value: int,
) -> dict:

    price = round(
        current_value
        * random.uniform(
            0.75,
            1.25,
        )
        / 5000
    ) * 5000

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
                5,
            ),

        "baths":
            random.choice(
                [
                    1.5,
                    2,
                    2.5,
                    3,
                    3.5,
                ]
            ),

        "sqft":
            random.randint(
                1000,
                3400,
            ),

        "address":
            fake.street_address(),

        "city":
            city,

        "state":
            state,

        "distance":
            round(
                random.uniform(
                    0.1,
                    2.8,
                ),
                1,
            ),

        "sold_days":
            random.randint(
                4,
                90,
            ),

        "image":
            get_random_property_image(),
    }


# ==========================================================
# Facts
# ==========================================================

def generate_home_facts() -> list[dict]:

    bedrooms = random.randint(
        2,
        6,
    )

    bathrooms = random.choice(
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
        1100,
        4200,
    )

    return [

        {
            "label":
                "Bedrooms",

            "value":
                str(
                    bedrooms
                ),

            "icon":
                "bed",

            "editable":
                True,
        },

        {
            "label":
                "Bathrooms",

            "value":
                str(
                    bathrooms
                ),

            "icon":
                "bathtub",

            "editable":
                True,
        },

        {
            "label":
                "Living area",

            "value":
                f"{sqft:,} sqft",

            "icon":
                "square_foot",

            "editable":
                True,
        },

        {
            "label":
                "Year built",

            "value":
                str(
                    random.randint(
                        1950,
                        2020,
                    )
                ),

            "icon":
                "calendar_month",

            "editable":
                False,
        },

        {
            "label":
                "Lot size",

            "value":
                (
                    f"{round(
                        random.uniform(
                            0.08,
                            1.4,
                        ),
                        2,
                    )} acres"
                ),

            "icon":
                "landscape",

            "editable":
                True,
        },

        {
            "label":
                "Home type",

            "value":
                random.choice(
                    [
                        "Single family",
                        "Townhouse",
                        "Condo",
                    ]
                ),

            "icon":
                "home",

            "editable":
                False,
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_homeowner_dashboard_data() -> dict:

    city, state = random.choice(
        CITIES
    )

    current_value = random.randrange(
        320_000,
        2_200_000,
        5_000,
    )

    monthly_change = random.randint(
        -30_000,
        45_000,
    )

    yearly_change = random.randint(
        -60_000,
        140_000,
    )

    yearly_percent = (
        yearly_change
        /
        max(
            1,
            current_value
            - yearly_change
        )
        *
        100
    )


    comparables = [

        generate_comparable(
            index=index,
            city=city,
            state=state,
            current_value=current_value,
        )

        for index in range(
            random.randint(
                4,
                7,
            )
        )
    ]


    tasks = []

    for index, task in enumerate(
        TASK_OPTIONS
    ):

        value = dict(
            task
        )

        value[
            "completed"
        ] = (
            random.random()
            < 0.35
        )

        value[
            "id"
        ] = (
            index
        )

        tasks.append(
            value
        )


    completed_count = sum(
        task[
            "completed"
        ]
        for task in tasks
    )


    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "home": {

            "address":
                fake.street_address(),

            "city":
                city,

            "state":
                state,

            "zipcode":
                fake.postcode(),

            "image":
                get_random_property_image(),

            "ownership_status":
                random.choice(
                    [
                        "Your home",
                        "Owner dashboard",
                    ]
                ),
        },


        "value": {

            "current":
                current_value,

            "current_text":
                format_price(
                    current_value
                ),

            "monthly_change":
                monthly_change,

            "monthly_change_text":
                (
                    f"+{format_price(monthly_change)}"
                    if monthly_change > 0

                    else format_price(
                        monthly_change
                    )
                ),

            "monthly_positive":
                monthly_change >= 0,

            "yearly_change":
                yearly_change,

            "yearly_change_text":
                (
                    f"+{format_price(yearly_change)}"
                    if yearly_change > 0

                    else format_price(
                        yearly_change
                    )
                ),

            "yearly_positive":
                yearly_change >= 0,

            "yearly_percent":
                round(
                    yearly_percent,
                    1,
                ),

            "confidence":
                random.randint(
                    70,
                    95,
                ),
        },


        "history":
            generate_value_history(
                current_value
            ),


        "market": {

            "status":
                random.choice(
                    MARKET_LABELS
                ),

            "median_price":
                format_price(
                    round(
                        current_value
                        * random.uniform(
                            0.75,
                            1.05,
                        )
                    )
                ),

            "days_on_market":
                random.randint(
                    8,
                    48,
                ),

            "sale_to_list":
                round(
                    random.uniform(
                        96,
                        104,
                    ),
                    1,
                ),

            "homes_for_sale":
                random.randint(
                    80,
                    920,
                ),
        },


        "comparables":
            comparables,


        "facts":
            generate_home_facts(),


        "tasks":
            tasks,


        "task_progress": {

            "completed":
                completed_count,

            "total":
                len(
                    tasks
                ),

            "percent":
                round(
                    completed_count
                    /
                    len(
                        tasks
                    )
                    *
                    100
                ),
        },


        "mobile_navigation": [

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
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_homeowner_dashboard_data()
    )

    print(
        "Address:",
        data[
            "home"
        ][
            "address"
        ],
    )

    print(
        "Value:",
        data[
            "value"
        ][
            "current_text"
        ],
    )

    print(
        "Comparables:",
        len(
            data[
                "comparables"
            ]
        ),
    )