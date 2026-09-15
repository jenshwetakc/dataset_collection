from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

TAXI_STATES = [
    "standard",
    "vehicle_select",
    "passenger_details",
    "driver_tracking",
    "confirmation",
    "no_availability",
]


AIRPORTS = [
    "Incheon International Airport",
    "Gimpo International Airport",
    "Narita International Airport",
    "Haneda Airport",
    "Heathrow Airport",
    "Charles de Gaulle Airport",
]


DESTINATIONS = [
    "Grand Central Hotel",
    "City Center",
    "Seoul Station",
    "Gangnam District",
    "Downtown Hotel",
    "Riverside Residence",
]


VEHICLES = [
    {
        "name": "Standard",
        "icon": "directions_car",
        "passengers": 3,
        "bags": 2,
    },
    {
        "name": "Executive",
        "icon": "local_taxi",
        "passengers": 3,
        "bags": 2,
    },
    {
        "name": "People carrier",
        "icon": "airport_shuttle",
        "passengers": 6,
        "bags": 5,
    },
    {
        "name": "Large van",
        "icon": "airport_shuttle",
        "passengers": 8,
        "bags": 7,
    },
]


DRIVER_NAMES = [
    "Jin Park",
    "Daniel Kim",
    "Min Lee",
    "Alex Choi",
    "Sung Han",
]


# ==========================================================
# Vehicle
# ==========================================================

def generate_vehicle() -> dict:

    source = dict(
        random.choice(
            VEHICLES
        )
    )

    price = random.randint(
        35,
        140,
    )

    return {
        **source,

        "price":
            price,

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),

        "free_cancel":
            random.random() < 0.65,

        "meet_greet":
            random.random() < 0.55,

        "flight_tracking":
            random.random() < 0.45,

        "rating":
            round(
                random.uniform(
                    8.0,
                    9.8,
                ),
                1,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_airport_taxi_data() -> dict:

    state = random.choice(
        TAXI_STATES
    )

    no_availability = (
        state == "no_availability"
    )

    vehicles = (
        []
        if no_availability
        else [
            generate_vehicle()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ]
    )

    selected_vehicle = (
        random.choice(
            vehicles
        )
        if vehicles
        else None
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "vehicle_select":
            state == "vehicle_select",

        "passenger_details":
            state == "passenger_details",

        "driver_tracking":
            state == "driver_tracking",

        "confirmation":
            state == "confirmation",

        "no_availability":
            no_availability,

        # ------------------------------------------
        # Route
        # ------------------------------------------

        "pickup":
            random.choice(
                AIRPORTS
            ),

        "destination":
            random.choice(
                DESTINATIONS
            ),

        "date":
            random.choice(
                [
                    "Sep 18",
                    "Sep 20",
                    "Oct 02",
                    "Oct 11",
                ]
            ),

        "time":
            random.choice(
                [
                    "08:30",
                    "10:00",
                    "13:45",
                    "18:30",
                    "22:00",
                ]
            ),

        "flight_number":
            random.choice(
                [
                    "KE901",
                    "OZ102",
                    "JL512",
                    "AF264",
                    "LH712",
                ]
            ),

        "passengers":
            random.randint(
                1,
                4,
            ),

        "bags":
            random.randint(
                1,
                4,
            ),

        # ------------------------------------------
        # Journey
        # ------------------------------------------

        "distance":
            random.randint(
                24,
                68,
            ),

        "duration":
            random.choice(
                [
                    "45 min",
                    "55 min",
                    "1 hr 10 min",
                    "1 hr 25 min",
                ]
            ),

        # ------------------------------------------
        # Vehicles
        # ------------------------------------------

        "vehicles":
            vehicles,

        "selected_vehicle":
            selected_vehicle,

        # ------------------------------------------
        # Passenger
        # ------------------------------------------

        "passenger": {
            "name":
                random.choice(
                    [
                        "Alex Kim",
                        "Emma Park",
                        "Daniel Lee",
                        "Mina Choi",
                    ]
                ),

            "email":
                "traveler@example.com",

            "phone":
                "+82 10 1234 5678",
        },

        # ------------------------------------------
        # Driver
        # ------------------------------------------

        "driver": {
            "name":
                random.choice(
                    DRIVER_NAMES
                ),

            "rating":
                round(
                    random.uniform(
                        4.7,
                        5.0,
                    ),
                    1,
                ),

            "vehicle":
                random.choice(
                    [
                        "Hyundai Sonata",
                        "Kia K5",
                        "Hyundai Staria",
                        "Genesis G80",
                    ]
                ),

            "plate":
                f"{random.randint(10,99)}"
                f"{random.choice(['A','B','C'])}"
                f"{random.randint(1000,9999)}",
        },

        # ------------------------------------------
        # Confirmation
        # ------------------------------------------

        "booking_reference":
            f"TX{random.randint(100000, 999999)}",
    }


if __name__ == "__main__":

    data = generate_airport_taxi_data()

    print(
        "State:",
        data["state"],
    )

    print(
        "Vehicles:",
        len(
            data["vehicles"]
        ),
    )