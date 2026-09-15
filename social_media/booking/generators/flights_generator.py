from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

FLIGHT_STATES = [
    "standard",
    "cheapest",
    "fastest",
    "filters_open",
    "fare_details",
    "no_flights",
]


AIRLINES = [
    "Korean Air",
    "Asiana Airlines",
    "Japan Airlines",
    "ANA",
    "Singapore Airlines",
    "Air France",
    "Lufthansa",
    "Emirates",
]


AIRLINE_CODES = [
    "KE",
    "OZ",
    "JL",
    "NH",
    "SQ",
    "AF",
    "LH",
    "EK",
]


AIRPORTS = [
    {
        "city": "Seoul",
        "code": "ICN",
    },
    {
        "city": "Tokyo",
        "code": "NRT",
    },
    {
        "city": "Paris",
        "code": "CDG",
    },
    {
        "city": "London",
        "code": "LHR",
    },
    {
        "city": "Singapore",
        "code": "SIN",
    },
]


# ==========================================================
# Flight
# ==========================================================

def generate_flight(
    *,
    force_cheapest: bool = False,
    force_fastest: bool = False,
) -> dict:

    origin = random.choice(
        AIRPORTS
    )

    destination_pool = [
        item
        for item in AIRPORTS
        if item["code"] != origin["code"]
    ]

    destination = random.choice(
        destination_pool
    )

    airline_index = random.randrange(
        len(
            AIRLINES
        )
    )

    stops = random.choice(
        [
            0,
            0,
            0,
            1,
            1,
            2,
        ]
    )

    duration_hours = random.randint(
        2,
        15,
    )

    duration_minutes = random.choice(
        [
            0,
            15,
            30,
            45,
        ]
    )

    base_price = random.randint(
        140,
        950,
    )

    if force_cheapest:
        base_price = random.randint(
            110,
            280,
        )

    if force_fastest:
        duration_hours = random.randint(
            2,
            6,
        )

        stops = random.choice(
            [
                0,
                0,
                1,
            ]
        )

    depart_hour = random.randint(
        5,
        21,
    )

    depart_minute = random.choice(
        [
            "00",
            "15",
            "30",
            "45",
        ]
    )

    arrive_hour = (
        depart_hour
        + duration_hours
    ) % 24

    arrive_minute = depart_minute

    return {
        "airline":
            AIRLINES[
                airline_index
            ],

        "airline_code":
            AIRLINE_CODES[
                airline_index
            ],

        "origin_city":
            origin[
                "city"
            ],

        "origin_code":
            origin[
                "code"
            ],

        "destination_city":
            destination[
                "city"
            ],

        "destination_code":
            destination[
                "code"
            ],

        "departure_time":
            f"{depart_hour:02d}:{depart_minute}",

        "arrival_time":
            f"{arrive_hour:02d}:{arrive_minute}",

        "duration":
            (
                f"{duration_hours}h "
                f"{duration_minutes}m"
            ),

        "stops":
            stops,

        "stop_text":
            (
                "Direct"
                if stops == 0
                else (
                    f"{stops} stop"
                    if stops == 1
                    else f"{stops} stops"
                )
            ),

        "price":
            base_price,

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),

        "baggage":
            random.choice(
                [
                    "Carry-on included",
                    "1 checked bag included",
                    "No checked baggage",
                ]
            ),

        "refundable":
            random.random() < 0.35,

        "limited":
            random.random() < 0.20,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_flights_data() -> dict:

    state = random.choice(
        FLIGHT_STATES
    )

    no_flights = (
        state == "no_flights"
    )

    cheapest = (
        state == "cheapest"
    )

    fastest = (
        state == "fastest"
    )

    filters_open = (
        state == "filters_open"
    )

    fare_details = (
        state == "fare_details"
    )

    flights = (
        []
        if no_flights
        else [
            generate_flight(
                force_cheapest=
                    cheapest,

                force_fastest=
                    fastest,
            )
            for _ in range(
                random.randint(
                    6,
                    12,
                )
            )
        ]
    )

    selected_flight = (
        random.choice(
            flights
        )
        if flights
        else None
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "no_flights":
            no_flights,

        "filters_open":
            filters_open,

        "fare_details":
            fare_details,

        # ------------------------------------------
        # Search
        # ------------------------------------------

        "trip_type":
            "Round trip",

        "origin":
            "Seoul (ICN)",

        "destination":
            "Tokyo (NRT)",

        "dates":
            "Sep 18 – Sep 23",

        "travelers":
            "1 adult · Economy",

        # ------------------------------------------
        # Results
        # ------------------------------------------

        "flights":
            flights,

        "selected_flight":
            selected_flight,

        # ------------------------------------------
        # Sort
        # ------------------------------------------

        "sort_tabs": [
            {
                "label":
                    "Best",

                "active":
                    state == "standard",
            },
            {
                "label":
                    "Cheapest",

                "active":
                    cheapest,
            },
            {
                "label":
                    "Fastest",

                "active":
                    fastest,
            },
        ],

        # ------------------------------------------
        # Filters
        # ------------------------------------------

        "filters": [
            "Direct flights",
            "1 stop or fewer",
            "Checked baggage",
            "Refundable",
            "Morning departure",
            "Evening departure",
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_flights_data()
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Flights:",
        len(
            data["flights"]
        ),
    )