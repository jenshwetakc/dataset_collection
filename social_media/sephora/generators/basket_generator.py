from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

BASKET_STATES = [
    "filled",
    "mixed_fulfillment",
    "quantity_open",
    "promo_applied",
    "promo_error",
    "samples_dialog",
    "remove_dialog",
    "empty",
]

POPUP_STATES = {
    "samples_dialog",
    "remove_dialog",
}


def money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def calculate_totals(data: dict) -> None:
    subtotal = sum(
        item["price_cents"] * item["quantity"]
        for item in data["products"]
    )

    # Synthetic dataset offer, not a live Sephora promotion.
    discount = (
        subtotal // 10
        if data["state"] == "promo_applied"
        else 0
    )

    data["item_count"] = sum(
        item["quantity"]
        for item in data["products"]
    )

    data["subtotal_text"] = money(subtotal)
    data["discount_text"] = money(discount)
    data["total_text"] = money(subtotal - discount)


def generate_basket_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:

    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    products = []

    names = [
        "Daily Hydrating Face Cream",
        "Soft Finish Lip Color",
        "Refreshing Gel Cleanser",
        "Everyday Eau de Parfum",
    ]

    for index in range(random.randint(2, 4)):
        price_cents = random.randint(18, 85) * 100

        products.append({
            "id": f"basket-{sample_index}-{index}",
            "brand": fake.company(),
            "name": names[index],
            "image": get_random_image(directory),
            "size": random.choice([
                "Standard Size",
                "Mini Size",
                "Value Size",
            ]),
            "variant": random.choice([
                "Original",
                "Rose",
                "Neutral",
            ]),
            "quantity": random.randint(1, 2),
            "price_cents": price_cents,
            "price_text": money(price_cents),
            "fulfillment": "shipping",
        })

    samples = [
        {
            "id": f"sample-{index}",
            "brand": fake.company(),
            "name": name,
            "image": get_random_image(directory),
        }
        for index, name in enumerate([
            "Hydrating Serum Sample",
            "Floral Fragrance Sample",
            "Gentle Cleanser Sample",
            "Nourishing Hair Mask Sample",
        ])
    ]

    data = {
        "sample_index": sample_index,
        "state": "filled",
        "popup_visible": False,
        "products": products,
        "samples": samples,
        "selected_sample_ids": [
            samples[0]["id"],
            samples[1]["id"],
        ],
        "selected_product": deepcopy(products[0]),
        "quantity_product_id": products[0]["id"],
        "store_name": f"{fake.city()} Beauty Center",
        "promo_code": "",
        "promo_message": "",
    }

    calculate_totals(data)
    return data


def apply_basket_state(
    base_data: dict,
    state: str,
) -> dict:

    if state not in BASKET_STATES:
        raise ValueError(f"Unknown basket state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES

    if state == "mixed_fulfillment":
        data["products"][-1]["fulfillment"] = "pickup"

    elif state == "promo_applied":
        data["promo_code"] = "DEMO10"
        data["promo_message"] = (
            "Demo offer applied: 10% merchandise discount."
        )

    elif state == "promo_error":
        data["promo_code"] = "EXPIRED"
        data["promo_message"] = (
            "This offer could not be applied. Check the code."
        )

    elif state == "empty":
        data["products"] = []

    calculate_totals(data)
    return data