from __future__ import annotations

import random

from datetime import (
    date,
    timedelta,
)

from social_media.booking.generators.media_generator import (
    get_random_destination_image,
    get_random_hotel_image,
)


# ==========================================================
# Data Pools
# ==========================================================

DESTINATIONS = [
    {
        "city": "Seoul",
        "country": "South Korea",
    },
    {
        "city": "Tokyo",
        "country": "Japan",
    },
    {
        "city": "Paris",
        "country": "France",
    },
    {
        "city": "London",
        "country": "United Kingdom",
    },
    {
        "city": "Bangkok",
        "country": "Thailand",
    },
    {
        "city": "Singapore",
        "country": "Singapore",
    },
    {
        "city": "Rome",
        "country": "Italy",
    },
    {
        "city": "Barcelona",
        "country": "Spain",
    },
    {
        "city": "New York",
        "country": "United States",
    },
    {
        "city": "Sydney",
        "country": "Australia",
    },
]


PROPERTY_TYPES = [
    {
        "name": "Hotels",
        "icon": "hotel",
    },
    {
        "name": "Apartments",
        "icon": "apartment",
    },
    {
        "name": "Resorts",
        "icon": "pool",
    },
    {
        "name": "Villas",
        "icon": "villa",
    },
    {
        "name": "Cabins",
        "icon": "cabin",
    },
    {
        "name": "Guest houses",
        "icon": "house",
    },
]


HOTEL_NAMES = [
    "Grand Central Hotel",
    "Ocean View Resort",
    "Urban Stay Suites",
    "Riverside Boutique Hotel",
    "The Metropolitan",
    "City Garden Residence",
    "Harbor View Hotel",
    "Royal Park Suites",
    "Skyline Residence",
    "The Heritage Hotel",
    "Golden Bay Resort",
    "Central Plaza Hotel",
    "Moonlight Residence",
    "Park Avenue Suites",
    "Blue Horizon Hotel",
]


NEIGHBORHOODS = [
    "City Center",
    "Downtown",
    "Old Town",
    "Central District",
    "Riverside",
    "Business District",
    "Historic Quarter",
    "Waterfront",
]


AMENITIES = [
    "Free breakfast",
    "Free cancellation",
    "Swimming pool",
    "Airport shuttle",
    "Fitness center",
    "Free WiFi",
    "Parking included",
    "Excellent location",
]


DEAL_MESSAGES = [
    "Save 15% on selected stays",
    "Getaway deals for your next trip",
    "Limited-time prices on great stays",
    "Member prices available",
]


# ==========================================================
# Date Helpers
# ==========================================================

def generate_dates() -> dict:

    today = date.today()

    check_in = (
        today
        + timedelta(
            days=random.randint(
                3,
                30,
            )
        )
    )

    nights = random.randint(
        1,
        7,
    )

    check_out = (
        check_in
        + timedelta(
            days=nights
        )
    )

    return {
        "check_in":
            check_in.strftime(
                "%a, %b %d"
            ),

        "check_out":
            check_out.strftime(
                "%a, %b %d"
            ),

        "nights":
            nights,
    }


# ==========================================================
# Destination
# ==========================================================

def generate_destination() -> dict:

    destination = dict(
        random.choice(
            DESTINATIONS
        )
    )

    destination[
        "image"
    ] = (
        get_random_destination_image()
    )

    return destination


# ==========================================================
# Search
# ==========================================================

def generate_search_data() -> dict:

    destination = (
        generate_destination()
    )

    dates = (
        generate_dates()
    )

    adults = random.randint(
        1,
        4,
    )

    children = random.randint(
        0,
        2,
    )

    rooms = random.randint(
        1,
        2,
    )

    guest_parts = [
        f"{adults} adult"
        + (
            "s"
            if adults != 1
            else ""
        ),
    ]

    if children > 0:

        guest_parts.append(
            f"{children} child"
            + (
                "ren"
                if children != 1
                else ""
            )
        )

    guest_parts.append(
        f"{rooms} room"
        + (
            "s"
            if rooms != 1
            else ""
        )
    )

    return {
        "destination":
            destination,

        "dates":
            dates,

        "adults":
            adults,

        "children":
            children,

        "rooms":
            rooms,

        "guest_text":
            " · ".join(
                guest_parts
            ),
    }


# ==========================================================
# Recent Search
# ==========================================================

def generate_recent_search() -> dict:

    destination = (
        generate_destination()
    )

    dates = (
        generate_dates()
    )

    return {
        "city":
            destination[
                "city"
            ],

        "country":
            destination[
                "country"
            ],

        "image":
            destination[
                "image"
            ],

        "date_text":
            (
                f"{dates['check_in']} – "
                f"{dates['check_out']}"
            ),

        "guest_text":
            random.choice(
                [
                    "1 room · 2 adults",
                    "1 room · 1 adult",
                    "2 rooms · 3 adults",
                    "1 room · 2 adults · 1 child",
                ]
            ),
    }


# ==========================================================
# Trending Destination
# ==========================================================

def generate_trending_destination() -> dict:

    destination = (
        generate_destination()
    )

    return {
        **destination,

        "properties":
            random.randint(
                120,
                4800,
            ),
    }


# ==========================================================
# Property Type
# ==========================================================

def generate_property_type(
    source: dict,
) -> dict:

    return {
        "name":
            source[
                "name"
            ],

        "icon":
            source[
                "icon"
            ],

        "image":
            get_random_hotel_image(),

        "count":
            random.randint(
                80,
                3500,
            ),
    }


# ==========================================================
# Hotel Card
# ==========================================================

def generate_hotel_card() -> dict:

    destination = (
        random.choice(
            DESTINATIONS
        )
    )

    rating = round(
        random.uniform(
            7.2,
            9.8,
        ),
        1,
    )

    review_count = random.randint(
        80,
        8400,
    )

    old_price = random.randint(
        130,
        520,
    )

    discount = random.randint(
        10,
        28,
    )

    current_price = round(
        old_price
        * (
            1
            - discount / 100
        )
    )

    selected_amenities = random.sample(
        AMENITIES,
        k=random.randint(
            2,
            4,
        ),
    )

    if rating >= 9.2:

        rating_label = "Wonderful"

    elif rating >= 8.7:

        rating_label = "Excellent"

    elif rating >= 8.0:

        rating_label = "Very good"

    else:

        rating_label = "Good"

    return {
        "name":
            random.choice(
                HOTEL_NAMES
            ),

        "city":
            destination[
                "city"
            ],

        "country":
            destination[
                "country"
            ],

        "neighborhood":
            random.choice(
                NEIGHBORHOODS
            ),

        "image":
            get_random_hotel_image(),

        "rating":
            rating,

        "rating_label":
            rating_label,

        "review_count":
            review_count,

        "old_price":
            old_price,

        "price":
            current_price,

        "discount":
            discount,

        "currency":
            random.choice(
                [
                    "US$",
                    "₩",
                    "€",
                ]
            ),

        "nights":
            random.randint(
                1,
                4,
            ),

        "amenities":
            selected_amenities,

        "favorite":
            random.random()
            < 0.35,

        "deal":
            random.random()
            < 0.60,

        "limited":
            random.random()
            < 0.20,
    }


# ==========================================================
# Promotion
# ==========================================================

def generate_promotion() -> dict:

    return {
        "title":
            random.choice(
                DEAL_MESSAGES
            ),

        "description":
            random.choice(
                [
                    (
                        "Book your next stay and "
                        "save on selected properties."
                    ),
                    (
                        "Discover special prices "
                        "available for a limited time."
                    ),
                    (
                        "Find member-only discounts "
                        "on popular destinations."
                    ),
                ]
            ),

        "button_text":
            random.choice(
                [
                    "Find deals",
                    "Explore stays",
                    "See offers",
                ]
            ),

        "icon":
            random.choice(
                [
                    "travel",
                    "luggage",
                    "hotel",
                    "flight_takeoff",
                ]
            ),
    }


# ==========================================================
# Home Generator
# ==========================================================

def generate_home_data() -> dict:

    search = (
        generate_search_data()
    )

    recent_searches = [
        generate_recent_search()
        for _ in range(
            random.randint(
                2,
                4,
            )
        )
    ]

    destination_count = (
        random.randint(
            5,
            8,
        )
    )

    destinations = [
        generate_trending_destination()
        for _ in range(
            destination_count
        )
    ]


    # ======================================================
    # Copy before shuffling
    # ======================================================

    property_type_pool = (
        PROPERTY_TYPES.copy()
    )

    random.shuffle(
        property_type_pool
    )

    property_types = [
        generate_property_type(
            source
        )
        for source in (
            property_type_pool[:6]
        )
    ]


    recommended = [
        generate_hotel_card()
        for _ in range(
            random.randint(
                6,
                10,
            )
        )
    ]


    return {

        # ------------------------------------------
        # Header
        # ------------------------------------------

        "brand_name":
            "Booking",

        "currency":
            random.choice(
                [
                    "USD",
                    "KRW",
                    "EUR",
                ]
            ),

        "navigation": [
            {
                "label":
                    "Stays",

                "icon":
                    "bed",

                "active":
                    True,
            },
            {
                "label":
                    "Flights",

                "icon":
                    "flight",

                "active":
                    False,
            },
            {
                "label":
                    "Car rentals",

                "icon":
                    "directions_car",

                "active":
                    False,
            },
            {
                "label":
                    "Attractions",

                "icon":
                    "attractions",

                "active":
                    False,
            },
            {
                "label":
                    "Airport taxis",

                "icon":
                    "local_taxi",

                "active":
                    False,
            },
        ],


        # ------------------------------------------
        # Hero
        # ------------------------------------------

        "headline":
            random.choice(
                [
                    "Find your next stay",
                    "Where do you want to go?",
                    "Discover somewhere new",
                    "Your next trip starts here",
                ]
            ),

        "subheadline":
            random.choice(
                [
                    (
                        "Search deals on hotels, "
                        "homes, and much more."
                    ),
                    (
                        "Find stays for every "
                        "kind of trip."
                    ),
                    (
                        "Book unique places in "
                        "destinations around the world."
                    ),
                ]
            ),


        # ------------------------------------------
        # Search
        # ------------------------------------------

        "search":
            search,


        # ------------------------------------------
        # Sections
        # ------------------------------------------

        "promotion":
            generate_promotion(),

        "recent_searches":
            recent_searches,

        "destinations":
            destinations,

        "property_types":
            property_types,

        "recommended":
            recommended,


        # ------------------------------------------
        # Bottom Navigation
        # ------------------------------------------

        "mobile_navigation": [
            {
                "label":
                    "Search",

                "icon":
                    "search",

                "active":
                    True,
            },
            {
                "label":
                    "Saved",

                "icon":
                    "favorite",

                "active":
                    False,
            },
            {
                "label":
                    "Trips",

                "icon":
                    "luggage",

                "active":
                    False,
            },
            {
                "label":
                    "Profile",

                "icon":
                    "person",

                "active":
                    False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_home_data()
    )

    print(
        "\n=============================="
    )

    print(
        "BOOKING HOME GENERATOR"
    )

    print(
        "=============================="
    )

    print(
        "Destination:",
        data[
            "search"
        ][
            "destination"
        ][
            "city"
        ],
    )

    print(
        "Recent searches:",
        len(
            data[
                "recent_searches"
            ]
        ),
    )

    print(
        "Destinations:",
        len(
            data[
                "destinations"
            ]
        ),
    )

    print(
        "Property types:",
        len(
            data[
                "property_types"
            ]
        ),
    )

    print(
        "Recommended:",
        len(
            data[
                "recommended"
            ]
        ),
    )

    print(
        "Destination image:",
        data[
            "search"
        ][
            "destination"
        ][
            "image"
        ]
        is not None,
    )