from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

PRODUCT_STATES = [
    "overview",
    "size_selected",
    "pickup_selected",
    "reviews",
    "gallery_dialog",
    "store_dialog",
    "basket_added",
]

POPUP_STATES = {
    "gallery_dialog",
    "store_dialog",
    "basket_added",
}


def generate_product_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:
    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    price = random.randint(25, 80)

    gallery = [
        get_random_image(directory)
        for _ in range(4)
    ]

    sizes = [
        {
            "label": "Mini size",
            "volume": "15 mL",
            "price": round(price * 0.55),
        },
        {
            "label": "Standard size",
            "volume": "50 mL",
            "price": price,
        },
        {
            "label": "Value size",
            "volume": "100 mL",
            "price": round(price * 1.65),
        },
    ]

    reviews = [
        {
            "author": fake.user_name(),
            "rating": random.randint(3, 5),
            "title": random.choice([
                "A lovely addition to my routine",
                "Comfortable and lightweight",
                "Works well for my skin",
            ]),
            "body": (
                "I enjoyed the texture and found it easy "
                "to include in my daily routine."
            ),
            "skin_type": random.choice([
                "Dry",
                "Combination",
                "Normal",
            ]),
            "helpful": random.randint(0, 45),
        }
        for _ in range(8)
    ]

    stores = [
        {
            "name": f"{fake.city()} Beauty Center",
            "address": fake.street_address(),
            "distance": round(random.uniform(0.5, 12), 1),
            "available": index != 2,
        }
        for index in range(4)
    ]

    return {
        "state": "overview",
        "popup_visible": False,
        "brand": fake.company(),
        "name": random.choice([
            "Barrier Comfort Hydrating Cream",
            "Daily Glow Moisturizer",
            "Ceramide Recovery Face Cream",
        ]),
        "gallery": gallery,
        "gallery_index": 0,
        "sizes": sizes,
        "selected_size": 1,
        "price_text": f"${price:.2f}",
        "rating": round(random.uniform(4.1, 4.9), 1),
        "review_count": random.randint(100, 3200),
        "reviews": reviews,
        "stores": stores,
        "selected_store": stores[0],
        "fulfillment": "shipping",
        "quantity": 1,
        "highlights": [
            {"name": "Hydrating", "icon": "water_drop"},
            {"name": "Cream Formula", "icon": "spa"},
            {"name": "For Dry Skin", "icon": "face"},
            {"name": "Fragrance-Free", "icon": "eco"},
        ],
        "description": (
            "A lightweight daily moisturizer designed "
            "for a comfortable, hydrated-looking complexion."
        ),
        "directions": (
            "Apply a small amount to clean skin "
            "as part of your morning or evening routine."
        ),
        "ingredients": (
            "Synthetic product information for UI simulation. "
            "Ingredient details vary by generated sample."
        ),
    }


def apply_product_state(data: dict, state: str) -> dict:
    if state not in PRODUCT_STATES:
        raise ValueError(f"Unknown product state: {state}")

    result = {
        **data,
        "state": state,
        "popup_visible": state in POPUP_STATES,
    }

    if state == "size_selected":
        result["selected_size"] = 2
        price = data["sizes"][2]["price"]
        result["price_text"] = f"${price:.2f}"

    elif state == "pickup_selected":
        result["fulfillment"] = "pickup"

    elif state == "gallery_dialog":
        result["gallery_index"] = 1

    return result