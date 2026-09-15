from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
    get_random_product_image,
)


# ==========================================================
# States
# ==========================================================

PRODUCT_STATES = [
    "default",
    "variant_selected",
    "coupon_available",
    "low_stock",
    "out_of_stock",
    "gallery_open",
    "added_to_cart",
    "deal",
    "prime_delivery",
    "buy_box_alt",
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
# Titles
# ==========================================================

PRODUCT_TITLES = {

    "Electronics": [
        "Wireless Noise Cancelling Headphones",
        "Portable Bluetooth Speaker with Deep Bass",
        "Smart Watch with Fitness and Sleep Tracking",
        "Compact Mechanical Keyboard",
        "USB-C Fast Charging Hub",
    ],

    "Fashion": [
        "Lightweight Everyday Running Shoes",
        "Classic Cotton Casual Shirt",
        "Minimal Crossbody Shoulder Bag",
        "Relaxed Fit Lightweight Jacket",
        "Comfort Walking Sneakers",
    ],

    "Home": [
        "Modern LED Desk Lamp",
        "Compact Coffee Maker",
        "Nonstick Cookware Set",
        "Soft Cotton Bedding Set",
        "Storage Organizer System",
    ],

    "Books": [
        "Practical Machine Learning Handbook",
        "Modern Software Engineering",
        "Introduction to User Interface Design",
        "Creative Thinking for Everyday Problems",
        "Stories for Quiet Evenings",
    ],

    "Grocery": [
        "Premium Roasted Coffee Beans",
        "Healthy Mixed Nut Snack Pack",
        "Assorted Tea Collection",
        "Breakfast Cereal Variety Pack",
        "Organic Snack Box",
    ],
}


# ==========================================================
# Variant Values
# ==========================================================

COLORS = [
    "Black",
    "White",
    "Blue",
    "Silver",
    "Green",
]

SIZES = [
    "Small",
    "Medium",
    "Large",
    "X-Large",
]

STYLES = [
    "Standard",
    "Premium",
    "Compact",
    "Pro",
]


# ==========================================================
# Price
# ==========================================================

def generate_price(
    force_deal: bool = False,
) -> dict:

    current = round(
        random.uniform(
            19.99,
            799.99,
        ),
        2,
    )

    has_deal = (
        force_deal
        or random.random() < 0.35
    )

    if not has_deal:

        return {
            "current": current,
            "original": None,
            "discount": None,
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
        current
        / (
            1
            - discount / 100
        ),
        2,
    )

    return {
        "current": current,
        "original": original,
        "discount": discount,
    }


# ==========================================================
# Gallery
# ==========================================================

def generate_gallery(
    category: str,
) -> list[str]:

    images = []

    count = random.randint(
        4,
        7,
    )

    for _ in range(count):

        image = get_category_image(
            category
        )

        if image is None:

            image = get_random_product_image()

        if image is not None:
            images.append(image)

    return images


# ==========================================================
# Variants
# ==========================================================

def generate_variant_group(
    name: str,
    values: list[str],
    selected: str | None = None,
) -> dict:

    if selected is None:

        selected = random.choice(
            values
        )

    return {
        "name": name,

        "selected": selected,

        "values": [
            {
                "label": value,
                "selected": value == selected,
            }
            for value in values
        ],
    }


def generate_variants(
    force_variant_state: bool,
) -> list[dict]:

    groups = []

    if random.random() < 0.85:

        groups.append(
            generate_variant_group(
                "Color",
                random.sample(
                    COLORS,
                    k=random.randint(
                        3,
                        len(COLORS),
                    ),
                ),
            )
        )

    if random.random() < 0.5:

        groups.append(
            generate_variant_group(
                "Size",
                random.sample(
                    SIZES,
                    k=random.randint(
                        3,
                        len(SIZES),
                    ),
                ),
            )
        )

    if random.random() < 0.35:

        groups.append(
            generate_variant_group(
                "Style",
                random.sample(
                    STYLES,
                    k=random.randint(
                        2,
                        len(STYLES),
                    ),
                ),
            )
        )

    if (
        force_variant_state
        and not groups
    ):

        groups.append(
            generate_variant_group(
                "Color",
                COLORS[:4],
                selected="Blue",
            )
        )

    return groups


# ==========================================================
# Feature List
# ==========================================================

def generate_features() -> list[str]:

    features = [
        "Designed for everyday use",
        "Durable construction and lightweight design",
        "Easy setup with intuitive controls",
        "Suitable for home, work, or travel",
        "Backed by a limited manufacturer warranty",
        "Compact design for convenient storage",
        "Improved comfort for extended use",
    ]

    return random.sample(
        features,
        k=random.randint(
            4,
            6,
        ),
    )


# ==========================================================
# Review Distribution
# ==========================================================

def generate_review_distribution() -> list[dict]:

    five = random.randint(
        50,
        80,
    )

    four = random.randint(
        8,
        20,
    )

    three = random.randint(
        4,
        12,
    )

    two = random.randint(
        1,
        7,
    )

    one = max(
        1,
        100
        - five
        - four
        - three
        - two,
    )

    values = [
        five,
        four,
        three,
        two,
        one,
    ]

    return [
        {
            "stars":
                5 - index,

            "percent":
                value,
        }
        for index, value
        in enumerate(values)
    ]


# ==========================================================
# Related Products
# ==========================================================

def generate_related_products(
    category: str,
) -> list[dict]:

    products = []

    for _ in range(
        random.randint(
            4,
            7,
        )
    ):

        products.append(
            {
                "title":
                    random.choice(
                        PRODUCT_TITLES[
                            category
                        ]
                    ),

                "image":
                    get_category_image(
                        category
                    ),

                "price":
                    round(
                        random.uniform(
                            12.99,
                            399.99,
                        ),
                        2,
                    ),

                "rating":
                    round(
                        random.uniform(
                            3.7,
                            5.0,
                        ),
                        1,
                    ),
            }
        )

    return products


# ==========================================================
# Main Generator
# ==========================================================

def generate_product_data() -> dict:

    state = random.choice(
        PRODUCT_STATES
    )

    category = random.choice(
        CATEGORIES
    )

    title = random.choice(
        PRODUCT_TITLES[
            category
        ]
    )


    # ======================================================
    # Stock
    # ======================================================

    if state == "out_of_stock":

        stock_status = "Out of Stock"
        in_stock = False
        stock_count = 0

    elif state == "low_stock":

        stock_count = random.randint(
            1,
            5,
        )

        stock_status = (
            f"Only {stock_count} left in stock"
        )

        in_stock = True

    else:

        stock_status = "In Stock"
        stock_count = random.randint(
            10,
            100,
        )

        in_stock = True


    # ======================================================
    # Price
    # ======================================================

    price = generate_price(
        force_deal=(
            state == "deal"
        )
    )


    # ======================================================
    # Coupon
    # ======================================================

    coupon_available = (
        state == "coupon_available"
        or random.random() < 0.2
    )

    coupon_percent = (
        random.choice(
            [
                5,
                10,
                15,
                20,
            ]
        )
        if coupon_available
        else None
    )


    # ======================================================
    # Delivery
    # ======================================================

    if state == "prime_delivery":

        delivery_text = (
            "FREE Prime delivery tomorrow"
        )

        prime = True

    else:

        prime = (
            random.random()
            < 0.7
        )

        delivery_text = random.choice(
            [
                "FREE delivery tomorrow",
                "FREE delivery Friday",
                "Delivery available this week",
                "Fast delivery available",
            ]
        )


    # ======================================================
    # Variants
    # ======================================================

    variants = generate_variants(
        force_variant_state=(
            state == "variant_selected"
        )
    )


    # ======================================================
    # Gallery
    # ======================================================

    gallery = generate_gallery(
        category
    )

    main_image = (
        gallery[0]
        if gallery
        else get_random_product_image()
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "category":
            category,

        "title":
            title,

        "brand":
            random.choice(
                [
                    "Auralux",
                    "Nexora",
                    "Velora",
                    "Omnitek",
                    "Brightline",
                    "Everpeak",
                ]
            ),

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
                50,
                24000,
            ),

        "answered_questions":
            random.randint(
                10,
                800,
            ),

        "price":
            price,

        "badge":
            random.choice(
                [
                    None,
                    None,
                    "Best Seller",
                    "Amazon's Choice",
                    "Limited Deal",
                ]
            ),

        "coupon_available":
            coupon_available,

        "coupon_percent":
            coupon_percent,

        "prime":
            prime,

        "delivery_text":
            delivery_text,

        "in_stock":
            in_stock,

        "stock_status":
            stock_status,

        "stock_count":
            stock_count,

        "quantity":
            random.randint(
                1,
                3,
            ),

        "gallery":
            gallery,

        "main_image":
            main_image,

        "variants":
            variants,

        "features":
            generate_features(),

        "seller":
            random.choice(
                [
                    "Amazon",
                    "TechDirect",
                    "Prime Retail",
                    "HomeMarket",
                    "Official Store",
                ]
            ),

        "ships_from":
            random.choice(
                [
                    "Amazon",
                    "Local Fulfillment Center",
                    "Official Store",
                ]
            ),

        "show_gallery_modal":
            (
                state == "gallery_open"
            ),

        "show_added_dialog":
            (
                state == "added_to_cart"
            ),

        "alternate_buy_box":
            (
                state == "buy_box_alt"
            ),

        "review_distribution":
            generate_review_distribution(),

        "related_products":
            generate_related_products(
                category
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_product_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON PRODUCT GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Category:",
        data["category"],
    )

    print(
        "Stock:",
        data["stock_status"],
    )

    print(
        "Variants:",
        len(
            data["variants"]
        ),
    )

    print(
        "Images:",
        len(
            data["gallery"]
        ),
    )