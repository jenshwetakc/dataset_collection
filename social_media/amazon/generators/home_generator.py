from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
    get_random_banner_image,
    get_random_product_image,
)


# ==========================================================
# Constants
# ==========================================================

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Grocery",
    "Beauty",
    "Sports",
    "Toys",
]

SEARCH_PLACEHOLDERS = [
    "Search products",
    "Search Amazon",
    "What are you looking for?",
    "Search deals and products",
]

LOCATIONS = [
    "Seoul 02841",
    "Busan 48058",
    "Incheon 21554",
    "Daejeon 34134",
    "Daegu 41911",
]

SECTION_TITLES = [
    "Deals for you",
    "Recommended for you",
    "Popular products",
    "Today's offers",
    "Keep shopping",
    "Trending now",
    "Customers also viewed",
]

PRODUCT_NAMES = {
    "Electronics": [
        "Wireless Noise Cancelling Headphones",
        "Portable Bluetooth Speaker",
        "Smart Watch with Fitness Tracking",
        "Compact Mechanical Keyboard",
        "USB-C Fast Charging Hub",
    ],

    "Fashion": [
        "Classic Cotton Everyday Shirt",
        "Lightweight Running Sneakers",
        "Casual Crossbody Shoulder Bag",
        "Relaxed Fit Everyday Jacket",
        "Minimal Leather Style Wallet",
    ],

    "Home": [
        "Modern Table Lamp",
        "Soft Cotton Bedding Set",
        "Compact Storage Organizer",
        "Non-Stick Kitchen Cookware Set",
        "Decorative Indoor Plant Pot",
    ],

    "Books": [
        "The Modern Guide to Better Thinking",
        "Practical Machine Learning Handbook",
        "Creative Design Principles",
        "Stories for Quiet Evenings",
        "Introduction to Software Systems",
    ],

    "Grocery": [
        "Premium Roasted Coffee Beans",
        "Organic Mixed Snack Box",
        "Breakfast Cereal Variety Pack",
        "Assorted Tea Collection",
        "Healthy Daily Nut Mix",
    ],
}


# ==========================================================
# Price
# ==========================================================

def generate_price() -> dict:

    current = round(
        random.uniform(
            8.99,
            499.99,
        ),
        2,
    )

    discounted = (
        random.random()
        < 0.45
    )

    if discounted:

        discount_percent = (
            random.choice(
                [
                    5,
                    10,
                    15,
                    20,
                    25,
                    30,
                    40,
                ]
            )
        )

        original = round(
            current
            / (
                1
                - discount_percent
                / 100
            ),
            2,
        )

    else:

        discount_percent = None
        original = None

    return {
        "current":
            current,

        "original":
            original,

        "discount_percent":
            discount_percent,
    }


# ==========================================================
# Product
# ==========================================================

def generate_product(
    category: str | None = None,
) -> dict:

    if category is None:

        category = random.choice(
            [
                "Electronics",
                "Fashion",
                "Home",
                "Books",
                "Grocery",
            ]
        )

    titles = (
        PRODUCT_NAMES.get(
            category,
            PRODUCT_NAMES[
                "Electronics"
            ],
        )
    )

    rating = round(
        random.uniform(
            3.6,
            5.0,
        ),
        1,
    )

    review_count = random.randint(
        15,
        18000,
    )

    price = generate_price()

    badge = random.choice(
        [
            None,
            None,
            None,
            "Best Seller",
            "Limited Deal",
            "Top Choice",
        ]
    )

    prime = (
        random.random()
        < 0.6
    )

    return {

        "title":
            random.choice(
                titles
            ),

        "category":
            category,

        "image":
            get_category_image(
                category
            ),

        "rating":
            rating,

        "review_count":
            review_count,

        "price":
            price,

        "badge":
            badge,

        "prime":
            prime,

        "free_delivery":
            random.random()
            < 0.65,

        "sponsored":
            random.random()
            < 0.15,
    }


# ==========================================================
# Category Card
# ==========================================================

def generate_category_card(
    title: str,
) -> dict:

    return {
        "title":
            title,

        "image":
            get_category_image(
                title
            ),
    }


# ==========================================================
# Product Section
# ==========================================================

def generate_product_section() -> dict:

    title = random.choice(
        SECTION_TITLES
    )

    product_count = random.randint(
        4,
        8,
    )

    return {
        "title":
            title,

        "products": [
            generate_product()
            for _ in range(
                product_count
            )
        ],
    }


# ==========================================================
# Home State
# ==========================================================

def generate_home_state() -> str:

    return random.choice(
        [
            "default",
            "deal_heavy",
            "personalized",
            "compact",
        ]
    )


# ==========================================================
# Main Generator
# ==========================================================

def generate_home_data() -> dict:

    selected_categories = random.sample(
        CATEGORIES,
        k=random.randint(
            4,
            min(
                8,
                len(CATEGORIES),
            ),
        ),
    )

    state = generate_home_state()

    if state == "deal_heavy":
        section_count = 4

    elif state == "compact":
        section_count = 2

    else:
        section_count = 3

    sections = [
        generate_product_section()
        for _ in range(
            section_count
        )
    ]

    return {

        "state":
            state,

        "search_placeholder":
            random.choice(
                SEARCH_PLACEHOLDERS
            ),

        "location":
            random.choice(
                LOCATIONS
            ),

        "cart_count":
            random.randint(
                0,
                7,
            ),

        "hero": {
            "image":
                get_random_banner_image(),

            "title":
                random.choice(
                    [
                        "Discover something new",
                        "Great prices on everyday favorites",
                        "Deals selected for you",
                        "Upgrade your everyday",
                        "Shop this week's highlights",
                    ]
                ),

            "subtitle":
                random.choice(
                    [
                        "Explore popular picks across categories",
                        "New products and limited-time offers",
                        "Find useful products for home and work",
                        "Shop trending products today",
                    ]
                ),
        },

        "categories": [
            generate_category_card(
                category
            )
            for category
            in selected_categories
        ],

        "featured_products": [
            generate_product()
            for _ in range(
                random.randint(
                    4,
                    7,
                )
            )
        ],

        "sections":
            sections,

        "recommended_image":
            get_random_product_image(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_home_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON HOME GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Categories:",
        len(
            data["categories"]
        ),
    )

    print(
        "Sections:",
        len(
            data["sections"]
        ),
    )