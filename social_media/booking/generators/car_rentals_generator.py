from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

CAR_STATES = [
    "standard",
    "map_split",
    "filters_open",
    "vehicle_detail",
    "deal_heavy",
    "no_cars",
]


CAR_MODELS = [
    {
        "name": "Toyota Corolla",
        "category": "Compact",
        "icon": "directions_car",
    },
    {
        "name": "Hyundai Avante",
        "category": "Economy",
        "icon": "directions_car",
    },
    {
        "name": "Kia K5",
        "category": "Standard",
        "icon": "directions_car",
    },
    {
        "name": "BMW 3 Series",
        "category": "Premium",
        "icon": "directions_car",
    },
    {
        "name": "Hyundai Tucson",
        "category": "SUV",
        "icon": "airport_shuttle",
    },
    {
        "name": "Kia Carnival",
        "category": "Minivan",
        "icon": "airport_shuttle",
    },
]


SUPPLIERS = [
    "Hertz",
    "Avis",
    "Sixt",
    "Europcar",
    "Budget",
    "Local Rent",
]


LOCATIONS = [
    "Incheon International Airport",
    "Seoul Station",
    "Gangnam",
    "Gimpo Airport",
    "City Center",
]


FILTERS = [
    "Automatic",
    "Manual",
    "Free cancellation",
    "Unlimited mileage",
    "SUV",
    "Compact",
    "Premium",
    "Airport pickup",
]


# ==========================================================
# Car
# ==========================================================

def generate_car(
    *,
    force_deal: bool = False,
) -> dict:

    source = dict(
        random.choice(
            CAR_MODELS
        )
    )

    old_price = random.randint(
        45,
        180,
    )

    discount = random.randint(
        10,
        30,
    )

    deal = (
        force_deal
        or random.random() < 0.45
    )

    price = (
        round(
            old_price
            * (
                1
                - discount / 100
            )
        )
        if deal
        else old_price
    )

    seats = random.choice(
        [
            4,
            5,
            7,
        ]
    )

    bags = random.choice(
        [
            1,
            2,
            3,
            4,
        ]
    )

    return {
        **source,

        "supplier":
            random.choice(
                SUPPLIERS
            ),

        "transmission":
            random.choice(
                [
                    "Automatic",
                    "Manual",
                ]
            ),

        "fuel":
            random.choice(
                [
                    "Petrol",
                    "Hybrid",
                    "Electric",
                    "Diesel",
                ]
            ),

        "seats":
            seats,

        "bags":
            bags,

        "doors":
            random.choice(
                [
                    4,
                    5,
                ]
            ),

        "price":
            price,

        "old_price":
            old_price,

        "discount":
            discount,

        "deal":
            deal,

        "free_cancel":
            random.random() < 0.60,

        "unlimited":
            random.random() < 0.50,

        "airport_pickup":
            random.random() < 0.55,

        "limited":
            random.random() < 0.20,

        "rating":
            round(
                random.uniform(
                    7.5,
                    9.6,
                ),
                1,
            ),

        "reviews":
            random.randint(
                90,
                3200,
            ),

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),
    }


# ==========================================================
# Main
# ==========================================================

def generate_car_rentals_data() -> dict:

    state = random.choice(
        CAR_STATES
    )

    no_cars = (
        state == "no_cars"
    )

    map_split = (
        state == "map_split"
    )

    filters_open = (
        state == "filters_open"
    )

    vehicle_detail = (
        state == "vehicle_detail"
    )

    deal_heavy = (
        state == "deal_heavy"
    )

    cars = (
        []
        if no_cars
        else [
            generate_car(
                force_deal=
                    deal_heavy
            )
            for _ in range(
                random.randint(
                    6,
                    11,
                )
            )
        ]
    )

    selected_car = (
        random.choice(
            cars
        )
        if cars
        else None
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "no_cars":
            no_cars,

        "map_split":
            map_split,

        "filters_open":
            filters_open,

        "vehicle_detail":
            vehicle_detail,

        # ------------------------------------------
        # Search
        # ------------------------------------------

        "pickup_location":
            random.choice(
                LOCATIONS
            ),

        "dropoff_location":
            random.choice(
                LOCATIONS
            ),

        "pickup_date":
            "Sep 18",

        "dropoff_date":
            "Sep 23",

        "pickup_time":
            random.choice(
                [
                    "09:00",
                    "10:30",
                    "12:00",
                    "14:00",
                ]
            ),

        # ------------------------------------------
        # Cars
        # ------------------------------------------

        "cars":
            cars,

        "selected_car":
            selected_car,

        # ------------------------------------------
        # Filters
        # ------------------------------------------

        "filters":
            FILTERS.copy(),

        "selected_filters":
            random.sample(
                FILTERS,
                k=random.randint(
                    1,
                    3,
                ),
            ),

        # ------------------------------------------
        # Sort
        # ------------------------------------------

        "sort_options": [
            "Recommended",
            "Price: low to high",
            "Supplier rating",
            "Car size",
        ],

        "selected_sort":
            random.choice(
                [
                    "Recommended",
                    "Price: low to high",
                    "Supplier rating",
                    "Car size",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_car_rentals_data()
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Cars:",
        len(
            data["cars"]
        ),
    )