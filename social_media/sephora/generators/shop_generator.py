from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

SHOP_STATES = [
    "home",
    "search_results",
    "filter_open",
    "quick_view",
    "basket_added",
]

POPUP_STATES = {
    "filter_open",
    "quick_view",
    "basket_added",
}

CATEGORIES = [
    "Makeup",
    "Skincare",
    "Fragrance",
    "Hair",
    "Tools & Brushes",
    "Bath & Body",
]

PRODUCT_TYPES = {
    "Makeup": [
        "Soft Matte Lipstick",
        "Luminous Foundation",
        "Cream Blush",
        "Volume Mascara",
        "Eyeshadow Palette",
    ],
    "Skincare": [
        "Hydrating Serum",
        "Barrier Moisturizer",
        "Gentle Cleanser",
        "Brightening Eye Cream",
        "Daily Sunscreen",
    ],
    "Fragrance": [
        "Floral Eau de Parfum",
        "Amber Eau de Toilette",
        "Discovery Fragrance Set",
    ],
    "Hair": [
        "Repair Hair Mask",
        "Scalp Serum",
        "Hydrating Shampoo",
    ],
    "Tools & Brushes": [
        "Complexion Brush",
        "Blending Sponge Set",
        "Travel Brush Collection",
    ],
    "Bath & Body": [
        "Nourishing Body Cream",
        "Body Wash",
        "Hand Cream Set",
    ],
}

SHADE_COLORS = [
    "#9B4855",
    "#BA7263",
    "#D49880",
    "#7B3945",
    "#C58E73",
    "#916349",
]

SORT_OPTIONS = [
    "Recommended",
    "Best Selling",
    "Newest",
    "Price: Low to High",
    "Price: High to Low",
]


def money(value: int) -> str:
    return f"${value}.00"


def generate_shop_page(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:
    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    # Synthetic brands and user names.
    brands = [
        fake.company()
        for _ in range(6)
    ]

    products = []

    for index in range(random.randint(18, 26)):
        category = random.choice(CATEGORIES)
        price = random.randint(12, 120)

        products.append({
            "id": f"product_{sample_index}_{index}",
            "brand": random.choice(brands),
            "name": random.choice(PRODUCT_TYPES[category]),
            "category": category,
            "image": get_random_image(directory),
            "price": price,
            "price_text": money(price),
            "rating": round(random.uniform(3.8, 5.0), 1),
            "review_count": random.randint(20, 4500),
            "badge": random.choice([
                "New",
                "Bestseller",
                "Limited Edition",
                "",
                "",
            ]),
            "saved": random.random() < 0.25,
            "shades": random.sample(
                SHADE_COLORS,
                k=random.randint(3, 6),
            ),
            "size": random.choice([
                "Standard size",
                "Mini size",
                "Value size",
            ]),
            "description": (
                "Discover a new addition to your beauty routine. "
                "Explore the available shades and sizes."
            ),
        })

    # Pick a category that actually exists in this sample.
    query = random.choice(products)["category"]

    search_products = [
        product
        for product in products
        if product["category"] == query
    ]

    selected_product = random.choice(products)

    basket_count = random.randint(0, 4)

    return {
        "sample_index": sample_index,
        "state": "home",
        "popup_visible": False,
        "customer_name": fake.first_name(),
        "categories": list(CATEGORIES),
        "brands": brands,
        "products": products,
        "search_products": search_products,
        "search_query": query,
        "selected_product": selected_product,
        "basket_count": basket_count,
        "basket_count_after": basket_count + 1,
        "sort_options": list(SORT_OPTIONS),
        "sort_selected": "Recommended",
        "hero_title": random.choice([
            "Find your next beauty favorite",
            "A fresh start for your beauty routine",
            "Discover something beautiful",
        ]),
        "hero_subtitle": (
            "Explore new arrivals, everyday essentials, "
            "and products selected for you."
        ),
        "hero_image": get_random_image(directory),
        "promotion": random.choice([
            "Discover new beauty arrivals",
            "Explore this season’s beauty essentials",
            "Find your next skincare favorite",
        ]),
        "filter_categories": [
            {
                "name": category,
                "selected": category == query,
            }
            for category in CATEGORIES
        ],
        "filter_brands": [
            {
                "name": brand,
                "selected": index == 0,
            }
            for index, brand in enumerate(brands)
        ],
        "price_min": 0,
        "price_max": 150,
        "price_selected": 100,
        "in_stock_only": True,
    }


def apply_shop_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in SHOP_STATES:
        raise ValueError(
            f"Unknown Sephora shop state: {state!r}. "
            f"Available states: {SHOP_STATES}"
        )

    return {
        **page_data,
        "state": state,
        "popup_visible": state in POPUP_STATES,
    }