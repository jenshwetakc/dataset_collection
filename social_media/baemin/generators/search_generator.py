from __future__ import annotations

import random

from faker import Faker

from social_media.baemin.generators.media_generator import (
    get_random_food_image,
    get_random_restaurant_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Pools
# ==========================================================

CUISINES = [
    "Korean",
    "Chicken",
    "Japanese",
    "Chinese",
    "Pizza",
    "Burger",
    "Cafe",
    "Dessert",
    "Asian",
    "Healthy",
    "Fast food",
]


FOOD_KEYWORDS = [
    "fried chicken",
    "pizza",
    "burger",
    "tteokbokki",
    "bibimbap",
    "ramen",
    "pasta",
    "sushi",
    "coffee",
    "cake",
    "rice bowl",
    "noodles",
]


RESTAURANT_SUFFIXES = [
    "Kitchen",
    "Table",
    "House",
    "Bistro",
    "Chicken",
    "Cafe",
    "Grill",
    "Diner",
    "Express",
    "Lab",
]


FILTERS = [
    "All",
    "Free delivery",
    "Fast delivery",
    "Top rated",
    "Coupons",
    "Under 30 min",
]


SORT_OPTIONS = [
    "Recommended",
    "Rating",
    "Delivery time",
    "Distance",
]


# ==========================================================
# Helpers
# ==========================================================

def random_price_text(
    minimum: int = 8000,
    maximum: int = 30000,
) -> str:

    value = random.randrange(
        minimum,
        maximum + 500,
        500,
    )

    return f"₩{value:,}"


def random_restaurant_name() -> str:

    first = random.choice(
        [
            fake.first_name(),
            fake.last_name(),
            fake.city().split()[0],
            fake.color_name(),
            random.choice(
                [
                    "Seoul",
                    "Han",
                    "Daily",
                    "Golden",
                    "Happy",
                    "Urban",
                    "Fresh",
                    "Good",
                ]
            ),
        ]
    )

    suffix = random.choice(
        RESTAURANT_SUFFIXES
    )

    return f"{first} {suffix}"


def random_search_query() -> str:

    return random.choice(
        FOOD_KEYWORDS
    )


# ==========================================================
# Search Result
# ==========================================================

def generate_search_result(
    index: int,
) -> dict:

    rating = round(
        random.uniform(
            3.9,
            5.0,
        ),
        1,
    )

    delivery_minutes = random.choice(
        [
            (15, 25),
            (20, 30),
            (25, 35),
            (30, 40),
            (35, 50),
        ]
    )

    tags = random.sample(
        [
            "Popular",
            "Coupon",
            "Free delivery",
            "New",
            "Fast",
            "Best seller",
            "Great value",
        ],
        k=random.randint(
            1,
            3,
        ),
    )

    description = fake.sentence(
        nb_words=random.randint(
            6,
            12,
        )
    )

    return {

        "id":
            index,

        "name":
            random_restaurant_name(),

        "image":
            (
                get_random_restaurant_image()
                or get_random_food_image()
            ),

        "cuisine":
            random.choice(
                CUISINES
            ),

        "description":
            description,

        "rating":
            rating,

        "review_count":
            random.randint(
                15,
                15000,
            ),

        "delivery_time":
            (
                f"{delivery_minutes[0]}-"
                f"{delivery_minutes[1]} min"
            ),

        "distance":
            f"{random.uniform(0.2, 6.5):.1f} km",

        "delivery_fee":
            random.choice(
                [
                    "Free delivery",
                    "₩1,000 delivery",
                    "₩1,500 delivery",
                    "₩2,000 delivery",
                    "₩3,000 delivery",
                ]
            ),

        "minimum_order":
            (
                f"{random_price_text()} minimum"
            ),

        "tags":
            tags,

        "favorite":
            random.random()
            < 0.2,

        "sponsored":
            random.random()
            < 0.12,
    }


# ==========================================================
# Recent Search
# ==========================================================

def generate_recent_searches() -> list[dict]:

    count = random.randint(
        3,
        7,
    )

    result = []

    used = set()

    while len(result) < count:

        query = random.choice(
            FOOD_KEYWORDS
        )

        if query in used:

            continue

        used.add(
            query
        )

        result.append(
            {
                "query":
                    query,

                "time":
                    fake.date_time_between(
                        start_date="-7d",
                        end_date="now",
                    ).strftime(
                        "%b %d"
                    ),
            }
        )

    return result


# ==========================================================
# Suggestions
# ==========================================================

def generate_suggestions() -> list[str]:

    return random.sample(
        FOOD_KEYWORDS,
        k=random.randint(
            5,
            9,
        ),
    )


# ==========================================================
# Search Generator
# ==========================================================

def generate_search_data() -> dict:

    query = random_search_query()

    result_count = random.randint(
        8,
        22,
    )

    results = [

        generate_search_result(
            index
        )

        for index
        in range(
            result_count
        )
    ]

    selected_filter = random.choice(
        FILTERS
    )

    selected_sort = random.choice(
        SORT_OPTIONS
    )

    return {

        "query":
            query,

        "search_placeholder":
            random.choice(
                [
                    "Search restaurants or food",
                    "What would you like to eat?",
                    "Find restaurants near you",
                    "Search for your favorite menu",
                ]
            ),

        "recent_searches":
            generate_recent_searches(),

        "suggestions":
            generate_suggestions(),

        "filters":
            FILTERS,

        "selected_filter":
            selected_filter,

        "sort_options":
            SORT_OPTIONS,

        "selected_sort":
            selected_sort,

        "results":
            results,

        "result_count":
            len(
                results
            ),

        "location":
            fake.city(),

        "header_text":
            random.choice(
                [
                    "Search",
                    "Find your next meal",
                    "What are you craving?",
                ]
            ),
    }