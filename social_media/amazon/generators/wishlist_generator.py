from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

WISHLIST_STATES = [
    "empty",
    "grid_view",
    "list_view",
    "sort_open",
    "filtered",
    "private_list",
    "public_list",
    "share_dialog",
    "collaborator_dialog",
    "moved_to_cart",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Grocery",
]


# ==========================================================
# Product Titles
# ==========================================================

PRODUCT_TITLES = {

    "Electronics": [
        "Wireless Noise Cancelling Headphones",
        "Portable Bluetooth Speaker",
        "Smart Watch with Fitness Tracking",
        "Mechanical Keyboard",
        "USB-C Fast Charging Hub",
        "Compact Wireless Mouse",
    ],

    "Fashion": [
        "Lightweight Running Shoes",
        "Classic Cotton Casual Shirt",
        "Minimal Crossbody Bag",
        "Relaxed Fit Jacket",
        "Comfort Walking Sneakers",
    ],

    "Home": [
        "Modern LED Desk Lamp",
        "Compact Coffee Maker",
        "Storage Organizer Set",
        "Nonstick Cookware Set",
        "Soft Cotton Bedding Set",
    ],

    "Books": [
        "Practical Machine Learning Handbook",
        "Modern Software Engineering",
        "Introduction to UI Design",
        "Creative Thinking for Everyday Problems",
    ],

    "Grocery": [
        "Premium Roasted Coffee Beans",
        "Healthy Mixed Nut Pack",
        "Assorted Tea Collection",
        "Breakfast Cereal Variety Pack",
    ],
}


# ==========================================================
# Sort Options
# ==========================================================

SORT_OPTIONS = [
    "Default",
    "Price: Low to High",
    "Price: High to Low",
    "Recently Added",
    "Rating",
]


# ==========================================================
# Wishlist Product
# ==========================================================

def generate_wishlist_item() -> dict:

    category = random.choice(
        CATEGORIES
    )

    price = round(
        random.uniform(
            9.99,
            499.99,
        ),
        2,
    )

    has_old_price = (
        random.random()
        < 0.35
    )

    if has_old_price:

        old_price = round(
            price
            * random.uniform(
                1.08,
                1.45,
            ),
            2,
        )

    else:

        old_price = None

    return {

        "title":
            random.choice(
                PRODUCT_TITLES[
                    category
                ]
            ),

        "category":
            category,

        "image":
            get_category_image(
                category
            ),

        "price":
            price,

        "old_price":
            old_price,

        "rating":
            round(
                random.uniform(
                    3.7,
                    5.0,
                ),
                1,
            ),

        "review_count":
            random.randint(
                15,
                18000,
            ),

        "prime":
            random.random()
            < 0.65,

        "stock":
            random.choice(
                [
                    "In Stock",
                    "In Stock",
                    "Only a few left",
                    "Temporarily unavailable",
                ]
            ),

        "badge":
            random.choice(
                [
                    None,
                    None,
                    "Best Seller",
                    "Limited Deal",
                    "Top Pick",
                ]
            ),

        "added_days_ago":
            random.randint(
                1,
                180,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_wishlist_data() -> dict:

    state = random.choice(
        WISHLIST_STATES
    )

    if state == "empty":

        items = []

    else:

        items = [
            generate_wishlist_item()
            for _ in range(
                random.randint(
                    5,
                    12,
                )
            )
        ]


    # ======================================================
    # View Mode
    # ======================================================

    if state == "list_view":

        view_mode = "list"

    else:

        view_mode = random.choice(
            [
                "grid",
                "grid",
                "list",
            ]
        )


    # ======================================================
    # Privacy
    # ======================================================

    if state == "public_list":

        privacy = "Public"

    else:

        privacy = "Private"


    # ======================================================
    # Filtering
    # ======================================================

    active_filter = None

    if state == "filtered":

        active_filter = random.choice(
            [
                "In Stock",
                "Prime",
                "Under $50",
                "Deals",
            ]
        )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "list_name":
            random.choice(
                [
                    "My Wishlist",
                    "Things I Like",
                    "Saved Products",
                    "Future Purchases",
                    "Shopping Ideas",
                ]
            ),

        "description":
            random.choice(
                [
                    "Products saved for later.",
                    "Ideas and items I may purchase.",
                    "A collection of products I like.",
                    "",
                ]
            ),

        "privacy":
            privacy,

        "view_mode":
            view_mode,

        "items":
            items,

        "item_count":
            len(items),

        "sort_options":
            SORT_OPTIONS,

        "selected_sort":
            random.choice(
                SORT_OPTIONS
            ),

        "show_sort_menu":
            state == "sort_open",

        "active_filter":
            active_filter,

        "show_share_dialog":
            state == "share_dialog",

        "show_collaborator_dialog":
            state == "collaborator_dialog",

        "show_moved_message":
            state == "moved_to_cart",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_wishlist_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON WISHLIST GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Items:",
        len(
            data["items"]
        ),
    )

    print(
        "View:",
        data["view_mode"],
    )

    print(
        "Privacy:",
        data["privacy"],
    )