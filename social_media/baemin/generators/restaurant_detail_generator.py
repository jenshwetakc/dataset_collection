from __future__ import annotations

import random

from social_media.baemin.generators.media_generator import (
    get_random_food_image,
    get_random_restaurant_image,
)


# ==========================================================
# Restaurant Names
# ==========================================================

RESTAURANT_NAMES = [

    "Seoul Chicken Lab",
    "Gangnam Kitchen",
    "Han River Table",
    "Golden Chicken",
    "Daily Seoul",
    "Kitchen 88",
    "Myeongdong House",
    "Busan Bowl",
]


# ==========================================================
# Menu Section Pool
# ==========================================================

MENU_SECTIONS = [

    "Popular",
    "Signature",
    "Chicken",
    "Rice",
    "Noodles",
    "Side dishes",
    "Drinks",
    "Desserts",
]


# ==========================================================
# Menu Names
# ==========================================================

MENU_NAMES = [

    "Original Fried Chicken",
    "Spicy Garlic Chicken",
    "Soy Garlic Chicken",
    "Cheese Chicken",
    "Boneless Chicken Set",
    "Chicken Rice Bowl",
    "Spicy Rice Bowl",
    "Kimchi Fried Rice",
    "Beef Bibimbap",
    "Cream Pasta",
    "Seafood Noodles",
    "Tteokbokki",
    "Cheese Fries",
    "Sweet Potato Fries",
    "Chicken Dumplings",
    "Coleslaw",
    "Corn Cheese",
    "Coke",
    "Lemon Soda",
    "Iced Tea",
]


MENU_DESCRIPTIONS = [

    "Freshly prepared with our signature seasoning.",
    "Crispy outside and juicy inside.",
    "A customer favorite with rich savory flavor.",
    "Served fresh with our house-made sauce.",
    "Perfect for sharing with friends and family.",
    "Prepared with premium ingredients.",
    "One of our most popular menu items.",
]


# ==========================================================
# Helper
# ==========================================================

def make_price(
    minimum: int = 6000,
    maximum: int = 30000,
) -> str:

    value = random.randrange(
        minimum,
        maximum + 500,
        500,
    )

    return f"₩{value:,}"


# ==========================================================
# Menu Item
# ==========================================================

def generate_menu_item(
    index: int,
) -> dict:

    has_image = (
        random.random()
        < 0.82
    )

    return {

        "id":
            index,

        "name":
            random.choice(
                MENU_NAMES
            ),

        "description":
            random.choice(
                MENU_DESCRIPTIONS
            ),

        "price":
            make_price(),

        "image":
            (
                get_random_food_image()
                if has_image
                else None
            ),

        "popular":
            random.random()
            < 0.22,

        "discount":
            (
                random.choice(
                    [
                        "10% off",
                        "15% off",
                        "20% off",
                    ]
                )
                if random.random() < 0.16
                else None
            ),

        "sold_out":
            random.random()
            < 0.06,

        "review_count":
            random.randint(
                15,
                2500,
            ),
    }


# ==========================================================
# Menu Section
# ==========================================================

def generate_menu_section(
    name: str,
    section_index: int,
) -> dict:

    count = random.randint(
        4,
        8,
    )

    return {

        "id":
            section_index,

        "name":
            name,

        "description":
            (
                "Most loved items"
                if name == "Popular"
                else None
            ),

        "items": [

            generate_menu_item(
                section_index * 100
                + item_index
            )

            for item_index
            in range(
                count
            )
        ],
    }


# ==========================================================
# Restaurant Detail
# ==========================================================

def generate_restaurant_detail_data() -> dict:

    section_count = random.randint(
        5,
        8,
    )

    section_names = (
        MENU_SECTIONS[
            :section_count
        ]
    )

    rating = round(
        random.uniform(
            4.2,
            5.0,
        ),
        1,
    )

    return {

        "restaurant": {

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
                random.randint(
                    500,
                    18000,
                ),

            "category":
                random.choice(
                    [
                        "Chicken",
                        "Korean",
                        "Fast food",
                        "Asian",
                    ]
                ),

            "distance":
                f"{random.uniform(0.4, 4.5):.1f} km",

            "delivery_time":
                random.choice(
                    [
                        "20-30 min",
                        "25-35 min",
                        "30-40 min",
                        "35-45 min",
                    ]
                ),

            "delivery_fee":
                random.choice(
                    [
                        "Free delivery",
                        "₩1,000 delivery",
                        "₩1,500 delivery",
                        "₩2,000 delivery",
                    ]
                ),

            "minimum_order":
                random.choice(
                    [
                        "₩8,000",
                        "₩10,000",
                        "₩12,000",
                        "₩15,000",
                    ]
                ),

            "favorite":
                random.random()
                < 0.35,

            "notice":
                random.choice(
                    [
                        "Freshly prepared after your order.",
                        "Orders may take longer during peak hours.",
                        "Packaging fee may apply to some menu items.",
                        "Free delivery available on selected orders.",
                    ]
                ),
        },


        # ==================================================
        # Tabs
        # ==================================================

        "tabs": [
            "Menu",
            "Reviews",
            "Info",
        ],

        "selected_tab":
            "Menu",


        # ==================================================
        # Menu
        # ==================================================

        "menu_sections": [

            generate_menu_section(
                name,
                index,
            )

            for index, name
            in enumerate(
                section_names
            )
        ],


        # ==================================================
        # Cart
        # ==================================================

        "cart": {

            "count":
                random.choice(
                    [
                        0,
                        0,
                        1,
                        2,
                        3,
                    ]
                ),

            "total":
                make_price(
                    12000,
                    60000,
                ),
        },
    }