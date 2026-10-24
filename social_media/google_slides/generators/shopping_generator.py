from __future__ import annotations

import random

from faker import Faker

from system.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


fake = Faker()

CATEGORIES = [
    "Electronics",
    "Home & kitchen",
    "Fashion",
    "Beauty",
    "Sports",
    "Office supplies",
]

COLORS = [
    "#1A73E8",
    "#7B1FA2",
    "#00897B",
    "#E37400",
    "#C5221F",
]


def get_asset_image() -> str | None:
    return get_random_image(
        ASSETS_ROOT
    )


def generate_product(
    index: int,
) -> dict:
    price = random.randint(12, 850)
    discount = random.choice(
        [0, 0, 0, 10, 15, 20, 30]
    )

    return {
        "id": f"product-{index}",
        "name": fake.sentence(
            nb_words=random.randint(3, 7)
        ).rstrip("."),
        "brand": fake.company(),
        "category": random.choice(CATEGORIES),
        "price": price,
        "old_price": (
            round(
                price / (1 - discount / 100),
                2,
            )
            if discount
            else None
        ),
        "discount": discount,
        "rating": round(
            random.uniform(3.8, 5.0),
            1,
        ),
        "review_count": random.randint(
            15,
            8_500,
        ),
        "shipping": random.choice(
            [
                "Free delivery",
                "Delivery in 2–4 days",
                "Pickup available",
            ]
        ),
        "store": fake.company(),
        "image": get_asset_image(),
        "color": random.choice(COLORS),
        "image_label": fake.word().upper(),
    }


def generate_shopping_data() -> dict:
    products = [
        generate_product(index)
        for index in range(
            random.randint(18, 28)
        )
    ]

    cart_items = random.sample(
        products,
        k=random.randint(1, 3),
    )

    for product in cart_items:
        product["quantity"] = random.randint(1, 3)

    subtotal = sum(
        product["price"] * product["quantity"]
        for product in cart_items
    )

    state = random.choices(
        [
            "search_results",
            "product_detail",
            "cart",
            "filter_sheet",
            "checkout_dialog",
        ],
        weights=[
            35,
            26,
            16,
            13,
            10,
        ],
        k=1,
    )[0]

    return {
        "app_name": "Google Shopping",
        "state": state,
        "search_query": fake.word(),
        "products": products,
        "search_results": random.sample(
            products,
            k=min(12, len(products)),
        ),
        "featured_products": random.sample(
            products,
            k=min(5, len(products)),
        ),
        "selected_product": random.choice(
            products
        ),
        "cart_items": cart_items,
        "cart_subtotal": subtotal,
        "cart_shipping": random.choice(
            [0, 0, 8, 12]
        ),
        "filters": {
            "category": random.choice(
                CATEGORIES
            ),
            "min_price": random.choice(
                [0, 25, 50, 100]
            ),
            "max_price": random.choice(
                [250, 500, 1000]
            ),
        },
    }