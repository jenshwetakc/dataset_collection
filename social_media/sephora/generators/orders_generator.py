from __future__ import annotations

import random
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

ORDER_STATES = [
    "placed",
    "in_progress",
    "shipped",
    "delivered",
    "delivery_exception",
    "pickup_ready",
    "cancel_dialog",
    "canceled",
]


def money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def generate_order_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:
    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    products = []

    for index, name in enumerate(random.sample([
        "Hydrating Face Cream",
        "Soft Finish Lipstick",
        "Gentle Gel Cleanser",
        "Everyday Fragrance",
    ], random.randint(2, 4))):
        cents = random.randint(20, 80) * 100

        products.append({
            "id": f"order-product-{sample_index}-{index}",
            "brand": fake.company(),
            "name": name,
            "image": get_random_image(directory),
            "size": random.choice(["Standard Size", "Mini Size"]),
            "quantity": 1,
            "price_cents": cents,
            "price_text": money(cents),
        })

    subtotal = sum(
        product["price_cents"] * product["quantity"]
        for product in products
    )

    # Synthetic tax for dataset screenshots.
    tax = round(subtotal * 0.08)
    today = date.today()

    return {
        "state": "placed",
        "popup_visible": False,
        "order_number": fake.numerify("DEMO-########"),
        "order_date": (today - timedelta(days=3)).strftime("%B %d, %Y"),
        "arrival_date": (today + timedelta(days=2)).strftime("%B %d, %Y"),
        "delivery_date": today.strftime("%B %d, %Y"),
        "customer_name": fake.name(),
        "address": fake.street_address(),
        "city_line": f"{fake.city()}, {fake.state_abbr()} {fake.postcode()}",
        "store_name": f"{fake.city()} Beauty Center",
        "tracking_number": fake.numerify("DEMO###########"),
        "payment_last4": fake.numerify("####"),
        "products": products,
        "subtotal_text": money(subtotal),
        "tax_text": money(tax),
        "total_text": money(subtotal + tax),
        "status_label": "Placed",
        "status_icon": "receipt_long",
        "status_message": "We have received your order.",
        "progress_index": 0,
        "events": [
            {
                "title": "Shipment moving through the network",
                "location": fake.city(),
                "time": "Today · 8:30 AM",
            },
            {
                "title": "Package accepted by carrier",
                "location": fake.city(),
                "time": "Yesterday · 4:15 PM",
            },
            {
                "title": "Shipping label created",
                "location": "Fulfillment center",
                "time": "Yesterday · 10:00 AM",
            },
        ],
    }


def apply_order_state(base_data: dict, state: str) -> dict:
    if state not in ORDER_STATES:
        raise ValueError(f"Unknown order state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state == "cancel_dialog"

    configurations = {
        "placed": (
            "Placed", "receipt_long",
            "We have received your order.", 0,
        ),
        "in_progress": (
            "In Progress", "inventory_2",
            "Your order is being prepared.", 1,
        ),
        "shipped": (
            "Shipped", "local_shipping",
            "Your package is on its way.", 2,
        ),
        "delivered": (
            "Delivered", "check_circle",
            "Your package has been delivered.", 3,
        ),
        "delivery_exception": (
            "Delivery Update", "error_outline",
            "Delivery is delayed. Check the tracking updates.", 2,
        ),
        "pickup_ready": (
            "Ready for Pickup", "storefront",
            "Your order is ready at your selected store.", 2,
        ),
        "cancel_dialog": (
            "Placed", "receipt_long",
            "We have received your order.", 0,
        ),
        "canceled": (
            "Canceled", "cancel",
            "This order has been canceled.", -1,
        ),
    }

    label, symbol, message, progress = configurations[state]

    data.update({
        "status_label": label,
        "status_icon": symbol,
        "status_message": message,
        "progress_index": progress,
    })

    return data