# social_media/facebook/generators/marketplace_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_product_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

MARKETPLACE_STATES = [
    "default",
    "default",
    "category_selected",
    "filters_open",
    "product_preview",
    "saved_items",
    "seller_menu_open",
    "search_active",
]


CATEGORIES = [
    {
        "name": "Vehicles",
        "icon": "directions_car",
    },
    {
        "name": "Property rentals",
        "icon": "apartment",
    },
    {
        "name": "Apparel",
        "icon": "checkroom",
    },
    {
        "name": "Classifieds",
        "icon": "inventory_2",
    },
    {
        "name": "Electronics",
        "icon": "devices",
    },
    {
        "name": "Entertainment",
        "icon": "sports_esports",
    },
    {
        "name": "Family",
        "icon": "family_restroom",
    },
    {
        "name": "Garden",
        "icon": "yard",
    },
    {
        "name": "Home goods",
        "icon": "chair",
    },
    {
        "name": "Sporting goods",
        "icon": "fitness_center",
    },
]


PRODUCT_NAMES = [
    "Wireless Headphones",
    "Modern Desk Lamp",
    "Compact Coffee Machine",
    "Mechanical Keyboard",
    "Office Chair",
    "Smart Watch",
    "Camera Lens",
    "Gaming Monitor",
    "Wooden Dining Table",
    "Mountain Bicycle",
    "Portable Speaker",
    "Vintage Jacket",
    "Bookshelf",
    "Tablet Computer",
    "Electric Scooter",
]


CONDITIONS = [
    "New",
    "Like new",
    "Good",
    "Fair",
]


LOCATIONS = [
    "Seoul",
    "Gangnam-gu",
    "Mapo-gu",
    "Songpa-gu",
    "Jongno-gu",
    "Yongsan-gu",
    "Seongdong-gu",
]


# ==========================================================
# Seller
# ==========================================================

def generate_seller() -> dict:

    return {
        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "rating":
            round(
                random.uniform(
                    3.8,
                    5.0,
                ),
                1,
            ),
    }


# ==========================================================
# Product
# ==========================================================

def generate_product(
    index: int,
) -> dict:

    price = random.randint(
        10,
        1500,
    )

    original_price = None

    if random.random() < 0.22:

        original_price = (
            price
            + random.randint(
                10,
                200,
            )
        )

    return {
        "id":
            index,

        "title":
            random.choice(
                PRODUCT_NAMES
            ),

        "image":
            get_random_product_image(),

        "price":
            price,

        "original_price":
            original_price,

        "location":
            random.choice(
                LOCATIONS
            ),

        "condition":
            random.choice(
                CONDITIONS
            ),

        "listed_time":
            random.choice(
                [
                    "Just now",
                    "20 min ago",
                    "1 hour ago",
                    "3 hours ago",
                    "Yesterday",
                    "2 days ago",
                ]
            ),

        "saved":
            random.random() < 0.22,

        "seller":
            generate_seller(),

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),
    }


# ==========================================================
# Product Collection
# ==========================================================

def generate_products(
    count: int = 18,
) -> list[dict]:

    return [
        generate_product(index)
        for index in range(count)
    ]


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> dict:

    return {
        "radius":
            random.choice(
                [
                    5,
                    10,
                    20,
                    40,
                    80,
                ]
            ),

        "min_price":
            random.choice(
                [
                    0,
                    10,
                    50,
                    100,
                ]
            ),

        "max_price":
            random.choice(
                [
                    200,
                    500,
                    1000,
                    2000,
                ]
            ),

        "condition":
            random.choice(
                [
                    "Any",
                    "New",
                    "Like new",
                    "Good",
                ]
            ),
    }


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> list[dict]:

    return [
        {
            "name": "Browse all",
            "icon": "storefront",
        },
        {
            "name": "Notifications",
            "icon": "notifications",
        },
        {
            "name": "Inbox",
            "icon": "chat",
        },
        {
            "name": "Buying",
            "icon": "shopping_bag",
        },
        {
            "name": "Selling",
            "icon": "sell",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_marketplace_state(
    product_count: int,
) -> dict:

    name = random.choice(
        MARKETPLACE_STATES
    )

    selected_product = None

    if name in {
        "product_preview",
        "seller_menu_open",
    }:

        selected_product = random.randint(
            0,
            max(
                0,
                min(
                    product_count - 1,
                    8,
                )
            ),
        )

    selected_category = None

    if name == "category_selected":

        selected_category = random.choice(
            CATEGORIES
        )["name"]

    search_text = ""

    if name == "search_active":

        search_text = random.choice(
            [
                "bike",
                "desk",
                "camera",
                "chair",
                "monitor",
                "phone",
            ]
        )

    return {
        "name":
            name,

        "selected_product":
            selected_product,

        "selected_category":
            selected_category,

        "search_text":
            search_text,
    }


# ==========================================================
# Complete Marketplace Data
# ==========================================================

def generate_marketplace_data() -> dict:

    products = generate_products(
        count=random.randint(
            14,
            22,
        )
    )

    saved_products = [
        product
        for product in products
        if product["saved"]
    ]

    if not saved_products:

        products[0]["saved"] = True

        saved_products = [
            products[0]
        ]

    return {
        "navigation":
            generate_navigation(),

        "categories":
            CATEGORIES,

        "products":
            products,

        "saved_products":
            saved_products,

        "filters":
            generate_filters(),

        "state":
            generate_marketplace_state(
                product_count=len(
                    products
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_marketplace_data()
    )

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK MARKETPLACE GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Products:",
        len(
            data["products"]
        ),
    )

    print(
        "Saved products:",
        len(
            data["saved_products"]
        ),
    )

    print(
        "Categories:",
        len(
            data["categories"]
        ),
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Filters:",
        data["filters"],
    )