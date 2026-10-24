from __future__ import annotations

import random

from copy import deepcopy

from faker import Faker


fake = Faker("en_US")


STORES_STATES = [
    "results",
    "filtered",
    "filter_open",
    "store_selected",
    "store_details",
    "hours_expanded",
    "location_denied",
    "empty_results",
]


def generate_stores_data(
    sample_index: int = 0,
) -> dict:
    """Generate synthetic store-locator content."""

    city = fake.city()

    names = [
        "City Center",
        "Westfield Shopping Center",
        "Market Street",
        "Riverside Plaza",
    ]

    # Positions are illustrative percentages within the map.
    positions = [
        (28, 32),
        (65, 25),
        (46, 63),
        (77, 73),
    ]

    stores = []

    for index, (name, position) in enumerate(
        zip(names, positions),
        start=1,
    ):
        is_open = index != 3
        has_services = index != 4

        stores.append({
            "id": f"store-{sample_index}-{index}",
            "number": index,
            "name": f"SEPHORA {name}",
            "address": fake.street_address(),
            "city": city,
            "region": fake.state_abbr(),
            "postal_code": fake.postcode(),
            "phone": "(555) 010-0123",
            "distance": round(
                random.uniform(0.4, 2.0) + index,
                1,
            ),
            "is_open": is_open,
            "status": (
                "Open until 8:00 PM"
                if is_open
                else "Closed · Opens tomorrow at 10:00 AM"
            ),
            "has_services": has_services,
            "pickup": index != 2,
            "map_x": position[0],
            "map_y": position[1],
            "services": (
                [
                    "Makeup services",
                    "Skincare consultations",
                    "Beauty events",
                ]
                if has_services
                else ["Beauty events"]
            ),
            "hours": [
                {
                    "day": day,
                    "hours": (
                        "11:00 AM – 6:00 PM"
                        if day == "Sunday"
                        else "10:00 AM – 8:00 PM"
                    ),
                }
                for day in [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
            ],
        })

    return {
        "sample_index": sample_index,
        "state": "results",
        "popup_visible": False,
        "query": city,
        "stores": stores,
        "selected_store": deepcopy(stores[0]),
        "open_only": False,
        "services_only": False,
        "radius": "25 miles",
        "hours_open": False,
    }


def apply_stores_state(
    base_data: dict,
    state: str,
) -> dict:
    """Create one independent screenshot state."""

    if state not in STORES_STATES:
        raise ValueError(
            f"Unknown stores state: {state}"
        )

    data = deepcopy(base_data)

    data["state"] = state

    data["popup_visible"] = state in {
        "filter_open",
        "store_details",
    }

    data["hours_open"] = state == "hours_expanded"

    if state == "filtered":
        data["open_only"] = True
        data["services_only"] = True

        data["stores"] = [
            store
            for store in data["stores"]
            if store["is_open"]
            and store["has_services"]
        ]

    elif state == "empty_results":
        data["query"] = "Remote location"
        data["stores"] = []

    return data