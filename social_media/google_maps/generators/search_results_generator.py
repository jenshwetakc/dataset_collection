from __future__ import annotations

import random

from faker import Faker

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_markers,
    generate_parks,
    generate_roads,
    generate_water,
)

from social_media.google_maps.generators.media_generator import (
    get_random_cafe_image,
    get_random_hotel_image,
    get_random_place_image,
    get_random_restaurant_image,
)


fake = Faker()


# ==========================================================
# Search Queries
# ==========================================================

SEARCH_QUERIES = [
    "coffee near me",
    "restaurants nearby",
    "hotels near me",
    "best brunch",
    "Korean restaurants",
    "pizza",
    "parks nearby",
    "shopping malls",
    "bakery",
    "museums",
    "pharmacy",
    "gas stations",
]


# ==========================================================
# Filter Chips
# ==========================================================

FILTER_OPTIONS = [
    {
        "label": "Open now",
        "icon": "schedule",
        "type": "toggle",
    },
    {
        "label": "Top rated",
        "icon": "star",
        "type": "toggle",
    },
    {
        "label": "Price",
        "icon": "payments",
        "type": "menu",
    },
    {
        "label": "Distance",
        "icon": "near_me",
        "type": "menu",
    },
    {
        "label": "Rating",
        "icon": "star_rate",
        "type": "menu",
    },
    {
        "label": "More filters",
        "icon": "tune",
        "type": "menu",
    },
]


# ==========================================================
# Search Categories
# ==========================================================

RESULT_TYPES = [
    "Coffee shop",
    "Cafe",
    "Restaurant",
    "Bakery",
    "Hotel",
    "Korean restaurant",
    "Italian restaurant",
    "Shopping center",
    "Museum",
    "Park",
]


# ==========================================================
# Image Resolver
# ==========================================================

def get_result_image(
    result_type: str,
) -> str | None:

    value = result_type.lower()

    if (
        "coffee" in value
        or "cafe" in value
        or "bakery" in value
    ):
        return (
            get_random_cafe_image()
            or get_random_place_image()
        )

    if "restaurant" in value:

        return (
            get_random_restaurant_image()
            or get_random_place_image()
        )

    if "hotel" in value:

        return (
            get_random_hotel_image()
            or get_random_place_image()
        )

    return get_random_place_image()


# ==========================================================
# Generate Result
# ==========================================================

def generate_search_result(
    index: int,
) -> dict:

    result_type = random.choice(
        RESULT_TYPES
    )

    rating = round(
        random.uniform(
            3.5,
            5.0,
        ),
        1,
    )

    review_count = random.randint(
        15,
        12000,
    )

    open_now = (
        random.random()
        < 0.82
    )

    sponsored = (
        index < 3
        and random.random()
        < 0.22
    )

    popular = (
        rating >= 4.5
        and review_count >= 500
        and random.random() < 0.45
    )

    return {

        "id":
            index,

        "name":
            (
                fake.company()
                .replace(
                    ", Inc.",
                    "",
                )
                .replace(
                    " LLC",
                    "",
                )
            ),

        "type":
            result_type,

        "rating":
            rating,

        "reviews":
            review_count,

        "price":
            random.choice(
                [
                    "",
                    "$",
                    "$$",
                    "$$$",
                ]
            ),

        "open_now":
            open_now,

        "open_text":
            (
                random.choice(
                    [
                        "Open",
                        "Open · Closes 9 PM",
                        "Open · Closes 10 PM",
                        "Open · Closes 11 PM",
                    ]
                )
                if open_now
                else "Closed"
            ),

        "distance":
            random.choice(
                [
                    "0.2 mi",
                    "0.3 mi",
                    "0.4 mi",
                    "0.6 mi",
                    "0.8 mi",
                    "1.1 mi",
                    "1.4 mi",
                    "2.2 mi",
                ]
            ),

        "address":
            fake.street_address(),

        "neighborhood":
            fake.city(),

        "image":
            get_result_image(
                result_type
            ),

        "sponsored":
            sponsored,

        "popular":
            popular,

        "saved":
            random.random()
            < 0.18,

        "delivery":
            (
                random.random()
                < 0.40
            ),

        "takeout":
            (
                random.random()
                < 0.55
            ),

        "selected":
            False,
    }


# ==========================================================
# Search Results Data
# ==========================================================

def generate_search_results_data() -> dict:

    query = random.choice(
        SEARCH_QUERIES
    )

    result_count = random.randint(
        8,
        15,
    )

    results = [
        generate_search_result(
            index
        )
        for index
        in range(
            result_count
        )
    ]

    selected_index = random.randrange(
        len(
            results
        )
    )

    results[
        selected_index
    ][
        "selected"
    ] = True

    selected_result = (
        results[
            selected_index
        ]
    )

    filters = random.sample(
        FILTER_OPTIONS,
        k=random.randint(
            4,
            len(
                FILTER_OPTIONS
            ),
        ),
    )

    for index, item in enumerate(
        filters
    ):

        item = dict(
            item
        )

        item[
            "selected"
        ] = (
            index == 0
            and random.random()
            < 0.6
        )

        filters[
            index
        ] = item

    return {

        "query":
            query,

        "result_summary":
            random.choice(
                [
                    f"{result_count} places",
                    f"About {result_count * random.randint(3, 9)} results",
                    "Results near this area",
                ]
            ),

        "filters":
            filters,

        "results":
            results,

        "selected_result":
            selected_result,

        "map":
            {
                "roads":
                    generate_roads(
                        count=random.randint(
                            18,
                            28,
                        )
                    ),

                "buildings":
                    generate_buildings(
                        count=random.randint(
                            30,
                            55,
                        )
                    ),

                "parks":
                    generate_parks(),

                "water":
                    generate_water(),

                "labels":
                    generate_map_labels(
                        count=random.randint(
                            8,
                            15,
                        )
                    ),

                "markers":
                    generate_markers(
                        count=min(
                            result_count,
                            12,
                        )
                    ),
            },

        "sort_label":
            random.choice(
                [
                    "Relevance",
                    "Distance",
                    "Rating",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_search_results_data()
    )

    print(
        "\n=============================="
    )

    print(
        "GOOGLE MAPS SEARCH RESULTS"
    )

    print(
        "=============================="
    )

    print(
        "Query:",
        data[
            "query"
        ],
    )

    print(
        "Results:",
        len(
            data[
                "results"
            ]
        ),
    )

    print(
        "Selected:",
        data[
            "selected_result"
        ][
            "name"
        ],
    )