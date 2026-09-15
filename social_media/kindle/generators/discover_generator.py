from __future__ import annotations

import random

from faker import Faker

from social_media.kindle.generators.media_generator import (
    get_random_book_cover,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

DISCOVER_STATES = [
    "discover_home",
    "genre_browse",
    "deals",
    "bestsellers",
    "personalized",
    "genre_filter",
    "purchase_options",
    "preview_open",
]


# ==========================================================
# Genres
# ==========================================================

GENRES = [
    {
        "name": "Fiction",
        "icon": "auto_stories",
    },
    {
        "name": "Mystery",
        "icon": "mystery",
    },
    {
        "name": "Science Fiction",
        "icon": "rocket_launch",
    },
    {
        "name": "Fantasy",
        "icon": "castle",
    },
    {
        "name": "Biography",
        "icon": "person_book",
    },
    {
        "name": "History",
        "icon": "history_edu",
    },
    {
        "name": "Business",
        "icon": "business_center",
    },
    {
        "name": "Technology",
        "icon": "computer",
    },
]


# ==========================================================
# Titles
# ==========================================================

TITLE_STARTS = [
    "The Hidden",
    "Beyond the",
    "The Last",
    "Fragments of",
    "A Guide to",
    "Understanding",
    "The Art of",
    "Inside the",
    "Notes from",
    "Echoes of",
]


TITLE_ENDS = [
    "Future",
    "Machine",
    "World",
    "Memory",
    "City",
    "Unknown",
    "Journey",
    "Mind",
    "River",
    "Stars",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_title() -> str:

    return (
        f"{random.choice(TITLE_STARTS)} "
        f"{random.choice(TITLE_ENDS)}"
    )


def generate_book(
    index: int,
) -> dict:

    original_price = round(
        random.uniform(
            7.99,
            24.99,
        ),
        2,
    )

    discount = random.choice(
        [
            0,
            0,
            10,
            20,
            30,
            50,
        ]
    )

    current_price = (
        original_price
        * (
            1
            - discount / 100
        )
    )

    return {

        "id":
            f"discover_book_{index:03d}",

        "title":
            generate_title(),

        "author":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "genre":
            random.choice(
                GENRES
            )[
                "name"
            ],

        "rating":
            round(
                random.uniform(
                    3.7,
                    5.0,
                ),
                1,
            ),

        "rating_count":
            random.randint(
                80,
                30000,
            ),

        "price":
            f"${current_price:.2f}",

        "original_price":
            f"${original_price:.2f}",

        "discount":
            discount,

        "kindle_unlimited":
            random.random()
            < 0.35,

        "bestseller":
            random.random()
            < 0.22,

        "editors_pick":
            random.random()
            < 0.16,

        "sample_available":
            random.random()
            < 0.80,
    }


# ==========================================================
# Shelves
# ==========================================================

def generate_shelf(
    title: str,
    count: int,
) -> dict:

    return {

        "title":
            title,

        "books": [
            generate_book(
                index
            )
            for index in range(
                count
            )
        ],
    }


# ==========================================================
# Generator
# ==========================================================

def generate_discover_page() -> dict:

    state = random.choice(
        DISCOVER_STATES
    )

    featured = [
        generate_book(
            index
        )
        for index in range(
            6
        )
    ]

    recommended = generate_shelf(
        "Recommended for you",
        random.randint(
            6,
            10,
        ),
    )

    trending = generate_shelf(
        "Trending now",
        random.randint(
            6,
            10,
        ),
    )

    deals = generate_shelf(
        "Limited-time deals",
        random.randint(
            6,
            10,
        ),
    )

    bestsellers = generate_shelf(
        "Best sellers",
        random.randint(
            6,
            10,
        ),
    )


    # ======================================================
    # Force deal books
    # ======================================================

    for book in deals[
        "books"
    ]:

        if book[
            "discount"
        ] == 0:

            book[
                "discount"
            ] = random.choice(
                [
                    20,
                    30,
                    50,
                ]
            )


    # ======================================================
    # Force bestseller
    # ======================================================

    for book in bestsellers[
        "books"
    ]:

        book[
            "bestseller"
        ] = True


    # ======================================================
    # Popup States
    # ======================================================

    show_genre_filter = (
        state
        == "genre_filter"
    )

    show_purchase_options = (
        state
        == "purchase_options"
    )

    show_preview = (
        state
        == "preview_open"
    )

    popup_open = any(
        [
            show_genre_filter,
            show_purchase_options,
            show_preview,
        ]
    )


    # ======================================================
    # Selected Book
    # ======================================================

    all_books = (
        featured
        + recommended["books"]
        + trending["books"]
    )

    selected_book = (
        random.choice(
            all_books
        )
        if all_books
        else None
    )


    # ======================================================
    # Primary Content State
    # ======================================================

    selected_genre = random.choice(
        GENRES
    )[
        "name"
    ]


    return {

        "state":
            state,

        "popup_open":
            popup_open,

        "show_genre_filter":
            show_genre_filter,

        "show_purchase_options":
            show_purchase_options,

        "show_preview":
            show_preview,

        "selected_book":
            selected_book,

        "selected_genre":
            selected_genre,

        "genres":
            GENRES,

        "featured":
            featured,

        "recommended":
            recommended,

        "trending":
            trending,

        "deals":
            deals,

        "bestsellers":
            bestsellers,

        "show_deals_focus":
            state == "deals",

        "show_bestsellers_focus":
            state == "bestsellers",

        "show_genre_focus":
            state == "genre_browse",

        "show_personalized_focus":
            state == "personalized",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_discover_page()
    )

    print(
        "\n=============================="
    )

    print(
        "KINDLE DISCOVER"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page["state"],
    )

    print(
        "Popup:",
        page["popup_open"],
    )

    print(
        "Genre:",
        page["selected_genre"],
    )