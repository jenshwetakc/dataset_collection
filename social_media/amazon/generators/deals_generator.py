from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

DEAL_STATES = [
    "default",
    "lightning_deals",
    "category_filtered",
    "watched_deals",
    "deal_detail_open",
    "expired_deal",
    "deal_claimed",
    "low_stock_deals",
    "coupon_deals",
    "empty_filtered",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [
    "All",
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Grocery",
    "Beauty",
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

    "Beauty": [
        "Daily Hydrating Skin Care Set",
        "Lightweight Facial Moisturizer",
        "Hair Care Essentials Bundle",
        "Travel Beauty Organizer",
    ],
}


# ==========================================================
# Deal
# ==========================================================

def generate_deal(
    force_lightning: bool = False,
    force_expired: bool = False,
    force_low_stock: bool = False,
    force_coupon: bool = False,
) -> dict:

    category = random.choice(
        [
            "Electronics",
            "Fashion",
            "Home",
            "Books",
            "Grocery",
            "Beauty",
        ]
    )

    current_price = round(
        random.uniform(
            8.99,
            399.99,
        ),
        2,
    )

    discount = random.choice(
        [
            10,
            15,
            20,
            25,
            30,
            40,
            50,
        ]
    )

    original_price = round(
        current_price
        / (
            1
            - discount / 100
        ),
        2,
    )

    lightning = (
        force_lightning
        or random.random() < 0.35
    )

    expired = (
        force_expired
        or random.random() < 0.06
    )

    percent_claimed = (
        100
        if expired
        else random.randint(
            8,
            95,
        )
    )

    low_stock = (
        force_low_stock
        or percent_claimed >= 85
    )

    coupon = (
        force_coupon
        or random.random() < 0.25
    )

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

        "current_price":
            current_price,

        "original_price":
            original_price,

        "discount":
            discount,

        "rating":
            round(
                random.uniform(
                    3.8,
                    5.0,
                ),
                1,
            ),

        "review_count":
            random.randint(
                15,
                22000,
            ),

        "lightning":
            lightning,

        "expired":
            expired,

        "claimed":
            percent_claimed,

        "low_stock":
            low_stock,

        "coupon":
            coupon,

        "coupon_percent":
            (
                random.choice(
                    [
                        5,
                        10,
                        15,
                    ]
                )
                if coupon
                else None
            ),

        "watched":
            random.random() < 0.25,

        "prime":
            random.random() < 0.7,

        "time_left":
            random.choice(
                [
                    "12 min left",
                    "34 min left",
                    "1 hr left",
                    "2 hrs left",
                    "Ends soon",
                ]
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_deals_data() -> dict:

    state = random.choice(
        DEAL_STATES
    )

    selected_category = "All"

    if state == "category_filtered":

        selected_category = random.choice(
            CATEGORIES[1:]
        )


    # ======================================================
    # Generate Deals
    # ======================================================

    if state == "empty_filtered":

        deals = []

        selected_category = random.choice(
            CATEGORIES[1:]
        )

    else:

        deal_count = random.randint(
            8,
            16,
        )

        deals = []

        for _ in range(
            deal_count
        ):

            deal = generate_deal(

                force_lightning=(
                    state
                    == "lightning_deals"
                ),

                force_expired=(
                    state
                    == "expired_deal"
                    and len(deals) == 0
                ),

                force_low_stock=(
                    state
                    == "low_stock_deals"
                ),

                force_coupon=(
                    state
                    == "coupon_deals"
                ),
            )

            if (
                selected_category
                != "All"
            ):

                deal["category"] = (
                    selected_category
                )

                deal["title"] = random.choice(
                    PRODUCT_TITLES[
                        selected_category
                    ]
                )

                deal["image"] = (
                    get_category_image(
                        selected_category
                    )
                )

            deals.append(
                deal
            )


    # ======================================================
    # Watched
    # ======================================================

    if state == "watched_deals":

        for deal in deals:

            deal["watched"] = (
                random.random()
                < 0.8
            )


    # ======================================================
    # Claimed
    # ======================================================

    claimed_deal = None

    if (
        state == "deal_claimed"
        and deals
    ):

        claimed_deal = random.choice(
            deals
        )


    # ======================================================
    # Selected Deal
    # ======================================================

    selected_deal = (
        random.choice(
            deals
        )
        if deals
        else None
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "categories":
            CATEGORIES,

        "selected_category":
            selected_category,

        "deals":
            deals,

        "deal_count":
            len(deals),

        "selected_deal":
            selected_deal,

        "claimed_deal":
            claimed_deal,

        "show_deal_dialog":
            (
                state
                == "deal_detail_open"
                and selected_deal
                is not None
            ),

        "show_claim_message":
            (
                state
                == "deal_claimed"
                and claimed_deal
                is not None
            ),

        "show_lightning_only":
            state == "lightning_deals",

        "show_watch_only":
            state == "watched_deals",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_deals_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON DEALS GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Deals:",
        len(
            data["deals"]
        ),
    )

    print(
        "Category:",
        data["selected_category"],
    )

    print(
        "Dialog:",
        data["show_deal_dialog"],
    )