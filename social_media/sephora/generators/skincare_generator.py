from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from social_media.sephora.generators.shop_generator import (
    generate_shop_page,
)

SKINCARE_STATES = [
    "browse",
    "filtered",
    "sort_open",
    "filter_open",
    "quicklook",
    "empty_results",
]

POPUP_STATES = {
    "sort_open",
    "filter_open",
    "quicklook",
}

CONCERNS = [
    "Dryness",
    "Dullness",
    "Acne & Blemishes",
    "Fine Lines & Wrinkles",
    "Uneven Texture",
]

PRODUCT_NAMES = [
    "Hydrating Ceramide Essence",
    "Barrier Repair Moisturizer",
    "Gentle Daily Cleanser",
    "Brightening Vitamin C Serum",
    "Overnight Recovery Mask",
    "Daily Mineral Sunscreen",
    "Hydrating Lip Treatment",
]

CATEGORIES = [
    "Moisturizers",
    "Shop by Concern",
    "Masks",
    "Vegan",
    "Lip Balms & Treatments",
    "Cleansers",
    "Mini Size",
    "Eye Care",
    "Treatments",
    "Sunscreen",
    "Value & Gift Sets",
]

FILTER_GROUPS = [
    "Price Range",
    "Brand",
    "Rating",
    "Skin Concerns",
    "Shopping Preferences",
    "Ingredient Preferences",
    "Skin Type",
    "Age Range",
    "Formulation",
    "Size",
    "Sun Protection",
]


def generate_skincare_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:
    shared = generate_shop_page(
        sample_index=sample_index,
        media_dir=media_dir,
    )

    products = deepcopy(shared["products"])

    for index, product in enumerate(products):
        product["name"] = random.choice(PRODUCT_NAMES)
        product["category"] = "Skincare"

        # Ensure every concern is represented.
        product["concern"] = CONCERNS[index % len(CONCERNS)]
        product["size_count"] = random.randint(1, 3)

    return {
        "state": "browse",
        "popup_visible": False,
        "products": products,
        "visible_products": products,
        "selected_product": products[0],
        "categories": list(CATEGORIES),
        "departments": [
            "New",
            "Makeup",
            "Skincare",
            "Fragrance",
            "Hair",
            "Bath & Body",
            "Mini Size",
            "Brands",
            "Gifts & Value Sets",
            "Sale & Offers",
        ],
        "shortcuts": [
            "New",
            "Bestsellers",
            "Value Sets",
            "Mini Size",
            "Jumbo Size",
            "Clean",
            "Vegan",
            "Cruelty-Free",
            "Korean Skincare",
        ],
        "filter_groups": list(FILTER_GROUPS),
        "concerns": list(CONCERNS),
        "selected_concern": "Dryness",
        "sort_options": [
            "Relevance",
            "Bestselling",
            "Top Rated",
            "New",
            "Price: Low to High",
            "Price: High to Low",
        ],
        "sort_selected": "Relevance",
        "brands": shared["brands"],
        "active_filters": [],
        "result_count": len(products),
    }


def apply_skincare_state(
    data: dict,
    state: str,
) -> dict:
    if state not in SKINCARE_STATES:
        raise ValueError(f"Unknown skincare state: {state}")

    result = {
        **data,
        "state": state,
        "popup_visible": state in POPUP_STATES,
        "active_filters": [],
        "visible_products": data["products"],
    }

    if state == "filtered":
        result["active_filters"] = [data["selected_concern"]]
        result["visible_products"] = [
            product
            for product in data["products"]
            if product["concern"] == data["selected_concern"]
        ]

    elif state == "empty_results":
        result["active_filters"] = [
            data["selected_concern"],
            "Under $5",
        ]
        result["visible_products"] = []

    result["result_count"] = len(result["visible_products"])

    return result