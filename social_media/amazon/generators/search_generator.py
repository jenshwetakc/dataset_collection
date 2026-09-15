from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# Search Queries
# ==========================================================

SEARCH_QUERIES = [
    "wireless headphones",
    "coffee maker",
    "running shoes",
    "mechanical keyboard",
    "smart watch",
    "desk lamp",
    "travel backpack",
    "bluetooth speaker",
    "office chair",
    "water bottle",
    "tablet stand",
    "phone charger",
]


# ==========================================================
# Categories
# ==========================================================

SEARCH_CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Grocery",
]


# ==========================================================
# Sort Options
# ==========================================================

SORT_OPTIONS = [
    {
        "label": "Featured",
        "value": "featured",
    },
    {
        "label": "Price: Low to High",
        "value": "price_low",
    },
    {
        "label": "Price: High to Low",
        "value": "price_high",
    },
    {
        "label": "Average Customer Review",
        "value": "rating",
    },
    {
        "label": "Newest Arrivals",
        "value": "newest",
    },
]


# ==========================================================
# States
# ==========================================================

SEARCH_STATES = [
    "default",
    "filters_applied",
    "sort_open",
    "low_results",
    "deal_heavy",
    "sponsored_heavy",
    "no_results",
    "mobile_filter_sheet",
    "mobile_sort_sheet",
]


# ==========================================================
# Product Titles
# ==========================================================

PRODUCT_TITLES = {

    "Electronics": [
        "Wireless Bluetooth Headphones with Deep Bass",
        "Portable Bluetooth Speaker with Long Battery Life",
        "Mechanical Keyboard with Compact Layout",
        "Smart Watch with Activity Tracking",
        "USB-C Fast Charger and Cable Set",
        "Noise Cancelling Over-Ear Headphones",
        "Compact Wireless Mouse",
        "Portable Power Bank",
    ],

    "Fashion": [
        "Lightweight Everyday Running Shoes",
        "Classic Cotton Casual Shirt",
        "Minimal Crossbody Shoulder Bag",
        "Everyday Lightweight Jacket",
        "Comfort Walking Sneakers",
        "Casual Travel Backpack",
    ],

    "Home": [
        "Modern LED Desk Lamp",
        "Compact Coffee Maker",
        "Storage Organizer Set",
        "Nonstick Cookware Set",
        "Soft Cotton Bedding Set",
        "Ergonomic Office Chair",
    ],

    "Books": [
        "Practical Machine Learning Handbook",
        "Modern Software Engineering",
        "Introduction to User Interface Design",
        "Creative Thinking for Everyday Problems",
    ],

    "Grocery": [
        "Premium Roasted Coffee Beans",
        "Healthy Mixed Nut Snack Pack",
        "Assorted Tea Collection",
        "Breakfast Cereal Variety Pack",
    ],
}


# ==========================================================
# Price
# ==========================================================

def generate_price(
    deal_probability: float = 0.35,
) -> dict:

    price = round(
        random.uniform(
            9.99,
            699.99,
        ),
        2,
    )

    has_deal = (
        random.random()
        < deal_probability
    )

    if not has_deal:

        return {
            "current":
                price,

            "original":
                None,

            "discount":
                None,
        }

    discount = random.choice(
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

    original = round(
        price
        / (
            1
            - discount / 100
        ),
        2,
    )

    return {
        "current":
            price,

        "original":
            original,

        "discount":
            discount,
    }


# ==========================================================
# Product
# ==========================================================

def generate_search_product(
    category: str,
    deal_probability: float = 0.35,
    sponsored_probability: float = 0.15,
) -> dict:

    titles = PRODUCT_TITLES.get(
        category,
        PRODUCT_TITLES[
            "Electronics"
        ],
    )

    badge = random.choice(
        [
            None,
            None,
            None,
            "Best Seller",
            "Amazon's Choice",
            "Limited Deal",
        ]
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

        "price":
            generate_price(
                deal_probability=
                    deal_probability
            ),

        "rating":
            round(
                random.uniform(
                    3.5,
                    5.0,
                ),
                1,
            ),

        "review_count":
            random.randint(
                12,
                25000,
            ),

        "badge":
            badge,

        "prime":
            random.random()
            < 0.65,

        "sponsored":
            random.random()
            < sponsored_probability,

        "free_delivery":
            random.random()
            < 0.7,

        "stock":
            random.choice(
                [
                    "In Stock",
                    "In Stock",
                    "In Stock",
                    "Only a few left",
                ]
            ),
    }


# ==========================================================
# Filter Group
# ==========================================================

def generate_filter_group(
    name: str,
    values: list[str],
    allow_selection: bool,
) -> dict:

    items = []

    for value in values:

        selected = (
            allow_selection
            and random.random()
            < 0.25
        )

        items.append(
            {
                "label":
                    value,

                "selected":
                    selected,
            }
        )

    return {
        "name":
            name,

        "items":
            items,
    }


# ==========================================================
# Filters
# ==========================================================

def generate_filters(
    filters_applied: bool,
) -> list[dict]:

    return [

        generate_filter_group(
            "Delivery",
            [
                "Get It Today",
                "Get It Tomorrow",
                "Prime Delivery",
            ],
            filters_applied,
        ),

        generate_filter_group(
            "Customer Review",
            [
                "4 Stars & Up",
                "3 Stars & Up",
            ],
            filters_applied,
        ),

        generate_filter_group(
            "Price",
            [
                "Under $25",
                "$25 to $50",
                "$50 to $100",
                "$100 to $200",
                "$200 & Above",
            ],
            filters_applied,
        ),

        generate_filter_group(
            "Availability",
            [
                "Include Out of Stock",
            ],
            filters_applied,
        ),
    ]


# ==========================================================
# Active Filter Chips
# ==========================================================

def collect_active_filters(
    filters: list[dict],
) -> list[str]:

    active = []

    for group in filters:

        for item in group["items"]:

            if item["selected"]:

                active.append(
                    item["label"]
                )

    return active


# ==========================================================
# Main Generator
# ==========================================================

def generate_search_data() -> dict:

    state = random.choice(
        SEARCH_STATES
    )

    category = random.choice(
        SEARCH_CATEGORIES
    )

    query = random.choice(
        SEARCH_QUERIES
    )


    # ======================================================
    # State Configuration
    # ======================================================

    filters_applied = (
        state
        == "filters_applied"
    )

    if state == "deal_heavy":

        deal_probability = 0.85

    else:

        deal_probability = 0.35


    if state == "sponsored_heavy":

        sponsored_probability = 0.65

    else:

        sponsored_probability = 0.15


    if state == "no_results":

        product_count = 0

    elif state == "low_results":

        product_count = random.randint(
            2,
            5,
        )

    else:

        product_count = random.randint(
            10,
            18,
        )


    # ======================================================
    # Filters
    # ======================================================

    filters = generate_filters(
        filters_applied=
            filters_applied
    )

    active_filters = (
        collect_active_filters(
            filters
        )
    )


    # ======================================================
    # Products
    # ======================================================

    products = [

        generate_search_product(
            category=
                category,

            deal_probability=
                deal_probability,

            sponsored_probability=
                sponsored_probability,
        )

        for _ in range(
            product_count
        )
    ]


    # ======================================================
    # Sort
    # ======================================================

    selected_sort = random.choice(
        SORT_OPTIONS
    )


    # ======================================================
    # Result Count
    # ======================================================

    if state == "no_results":

        result_count = 0

    elif state == "low_results":

        result_count = product_count

    else:

        result_count = random.randint(
            100,
            50000,
        )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "query":
            query,

        "category":
            category,

        "result_count":
            result_count,

        "products":
            products,

        "filters":
            filters,

        "active_filters":
            active_filters,

        "sort_options":
            SORT_OPTIONS,

        "selected_sort":
            selected_sort,

        "show_sort_menu":
            (
                state
                == "sort_open"
            ),

        "show_filter_sheet":
            (
                state
                == "mobile_filter_sheet"
            ),

        "show_sort_sheet":
            (
                state
                == "mobile_sort_sheet"
            ),

        "cart_count":
            random.randint(
                0,
                8,
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_search_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON SEARCH GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Query:",
        data["query"],
    )

    print(
        "Products:",
        len(
            data["products"]
        ),
    )

    print(
        "Active filters:",
        data["active_filters"],
    )