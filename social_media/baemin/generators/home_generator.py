from __future__ import annotations

import random

from faker import Faker

from social_media.baemin.generators.media_generator import (
    get_random_banner,
    get_random_category_image,
    get_random_food_image,
    get_random_restaurant_image,
)


fake = Faker()


# ==========================================================
# Static Content Pools
# ==========================================================

CATEGORY_POOL = [

    (
        "Chicken",
        "lunch_dining",
    ),

    (
        "Korean",
        "rice_bowl",
    ),

    (
        "Chinese",
        "ramen_dining",
    ),

    (
        "Japanese",
        "set_meal",
    ),

    (
        "Pizza",
        "local_pizza",
    ),

    (
        "Burger",
        "lunch_dining",
    ),

    (
        "Cafe",
        "local_cafe",
    ),

    (
        "Dessert",
        "cake",
    ),

    (
        "Fast food",
        "fastfood",
    ),

    (
        "Healthy",
        "nutrition",
    ),

    (
        "Asian",
        "ramen_dining",
    ),

    (
        "Late night",
        "nightlife",
    ),
]


RESTAURANT_NAMES = [

    "Seoul Kitchen",
    "Han River Chicken",
    "Daily Bowl",
    "Myeongdong Table",
    "Golden Chicken",
    "Kitchen 88",
    "Fresh Seoul",
    "Happy Burger",
    "Busan Noodles",
    "Midnight Kitchen",
    "Tokyo Table",
    "Good Meal",
    "Mama's Kitchen",
    "Gangnam Pizza",
    "Rice & Grill",
    "Corner Cafe",
]


FOOD_NAMES = [

    "Crispy Fried Chicken",
    "Spicy Chicken Set",
    "Beef Rice Bowl",
    "Kimchi Stew",
    "Pork Cutlet",
    "Cheese Pizza",
    "Double Burger",
    "Tteokbokki",
    "Bibimbap",
    "Cream Pasta",
    "Grilled Pork",
    "Chicken Rice",
    "Udon Set",
    "Seafood Noodles",
    "Salmon Bowl",
]


PROMOTION_TITLES = [

    "Free delivery today",
    "Save on your next meal",
    "Dinner deals are here",
    "Popular restaurants near you",
    "Weekend delivery special",
]


PROMOTION_SUBTITLES = [

    "Selected restaurants only",
    "Order now and enjoy the discount",
    "Limited-time benefits",
    "Discover today's most popular menus",
    "More food, fewer delivery fees",
]


# ==========================================================
# Helpers
# ==========================================================

def random_delivery_time() -> str:

    start = random.choice(
        [
            15,
            20,
            25,
            30,
            35,
        ]
    )

    end = (
        start
        + random.choice(
            [
                10,
                15,
                20,
            ]
        )
    )

    return (
        f"{start}-{end} min"
    )


def random_delivery_fee() -> str:

    value = random.choice(
        [
            0,
            0,
            0,
            1000,
            1500,
            2000,
            2500,
            3000,
        ]
    )

    if value == 0:

        return "Free delivery"

    return (
        f"₩{value:,} delivery"
    )


def random_distance() -> str:

    return (
        f"{random.uniform(0.3, 4.8):.1f} km"
    )


# ==========================================================
# Category
# ==========================================================

def generate_category(
    index: int,
) -> dict:

    name, icon = (
        CATEGORY_POOL[
            index
            % len(
                CATEGORY_POOL
            )
        ]
    )

    return {

        "name":
            name,

        "icon":
            icon,

        "image":
            get_random_category_image(),
    }


# ==========================================================
# Restaurant
# ==========================================================

def generate_restaurant(
    index: int,
) -> dict:

    rating = round(
        random.uniform(
            4.1,
            5.0,
        ),
        1,
    )

    review_count = random.randint(
        80,
        9500,
    )

    tags = random.sample(

        [
            "Popular",
            "Fast delivery",
            "New",
            "Free delivery",
            "Coupon",
            "Best seller",
            "Great value",
        ],

        k=random.randint(
            1,
            3,
        ),
    )

    return {

        "id":
            index,

        "name":
            random.choice(
                RESTAURANT_NAMES
            ),

        "image":
            (
                get_random_restaurant_image()
                or get_random_food_image()
            ),

        "rating":
            rating,

        "review_count":
            review_count,

        "delivery_time":
            random_delivery_time(),

        "delivery_fee":
            random_delivery_fee(),

        "distance":
            random_distance(),

        "minimum_order":
            random.choice(
                [
                    "₩8,000 minimum",
                    "₩10,000 minimum",
                    "₩12,000 minimum",
                    "₩15,000 minimum",
                ]
            ),

        "tags":
            tags,

        "favorite":
            random.random() < 0.2,

        "sponsored":
            random.random() < 0.14,
    }


# ==========================================================
# Recommended Menu
# ==========================================================

def generate_food_card(
    index: int,
) -> dict:

    price = random.randrange(
        6500,
        26000,
        500,
    )

    return {

        "id":
            index,

        "name":
            random.choice(
                FOOD_NAMES
            ),

        "restaurant":
            random.choice(
                RESTAURANT_NAMES
            ),

        "image":
            get_random_food_image(),

        "price":
            f"₩{price:,}",

        "rating":
            round(
                random.uniform(
                    4.2,
                    5.0,
                ),
                1,
            ),
    }


# ==========================================================
# Promotion
# ==========================================================

def generate_promotion(
    index: int,
) -> dict:

    return {

        "id":
            index,

        "title":
            random.choice(
                PROMOTION_TITLES
            ),

        "subtitle":
            random.choice(
                PROMOTION_SUBTITLES
            ),

        "image":
            (
                get_random_banner()
                or get_random_food_image()
            ),

        "button_text":
            random.choice(
                [
                    "Order now",
                    "Explore",
                    "View deals",
                ]
            ),
    }


# ==========================================================
# Home Generator
# ==========================================================

def generate_home_data() -> dict:

    categories = [

        generate_category(
            index
        )

        for index
        in range(
            random.randint(
                8,
                12,
            )
        )
    ]

    restaurants = [

        generate_restaurant(
            index
        )

        for index
        in range(
            random.randint(
                12,
                22,
            )
        )
    ]

    recommended_food = [

        generate_food_card(
            index
        )

        for index
        in range(
            random.randint(
                6,
                10,
            )
        )
    ]

    promotions = [

        generate_promotion(
            index
        )

        for index
        in range(
            random.randint(
                2,
                4,
            )
        )
    ]

    selected_category = random.choice(
        [
            "All",
            "Popular",
            "Free delivery",
            "Fast delivery",
        ]
    )

    return {

        "location": {

            "label":
                "Deliver to",

            "address":
                random.choice(
                    [
                        "Gangnam-gu, Seoul",
                        "Mapo-gu, Seoul",
                        "Seongbuk-gu, Seoul",
                        "Songpa-gu, Seoul",
                        "Jongno-gu, Seoul",
                    ]
                ),
        },

        "greeting":
            random.choice(
                [
                    "What would you like to eat?",
                    "What's for today?",
                    "Find something delicious",
                ]
            ),

        "search_placeholder":
            random.choice(
                [
                    "Search restaurants or food",
                    "What would you like to eat?",
                    "Search for a menu",
                ]
            ),

        "categories":
            categories,

        "promotions":
            promotions,

        "recommended_food":
            recommended_food,

        "restaurants":
            restaurants,

        "filters": [
            "All",
            "Popular",
            "Free delivery",
            "Fast delivery",
            "Coupons",
        ],

        "selected_filter":
            selected_category,

        "cart_count":
            random.choice(
                [
                    0,
                    0,
                    1,
                    2,
                    3,
                ]
            ),

        "notification_count":
            random.choice(
                [
                    0,
                    0,
                    1,
                    2,
                    4,
                ]
            ),

        "profile_name":
            fake.first_name(),
    }