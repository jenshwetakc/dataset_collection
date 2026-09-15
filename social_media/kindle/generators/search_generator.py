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

SEARCH_STATES = [
    "search_idle",
    "recent_searches",
    "suggestions",
    "results",
    "no_results",
    "filters_open",
    "category_browse",
    "preview_open",
]


# ==========================================================
# Search Queries
# ==========================================================

SEARCH_QUERIES = [
    "science fiction",
    "artificial intelligence",
    "history of technology",
    "modern psychology",
    "mystery novels",
    "machine learning",
    "personal finance",
    "space exploration",
    "Japanese literature",
    "productivity",
    "philosophy",
    "fantasy novels",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [
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
        "name": "Technology",
        "icon": "computer",
    },
    {
        "name": "Business",
        "icon": "business_center",
    },
]


# ==========================================================
# Titles
# ==========================================================

TITLE_STARTS = [
    "The Hidden",
    "Beyond the",
    "A Guide to",
    "Understanding",
    "The Future of",
    "Inside the",
    "The Last",
    "Lessons from",
    "Fragments of",
    "The Art of",
]


TITLE_ENDS = [
    "Machine",
    "Mind",
    "Future",
    "World",
    "City",
    "Unknown",
    "Memory",
    "Journey",
    "Ocean",
    "Universe",
]


# ==========================================================
# Title Generator
# ==========================================================

def generate_title() -> str:

    return (
        f"{random.choice(TITLE_STARTS)} "
        f"{random.choice(TITLE_ENDS)}"
    )


# ==========================================================
# Book Result
# ==========================================================

def generate_search_book(
    index: int,
) -> dict:

    return {

        "id":
            f"search_book_{index:03d}",

        "title":
            generate_title(),

        "author":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "rating":
            round(
                random.uniform(
                    3.6,
                    5.0,
                ),
                1,
            ),

        "rating_count":
            random.randint(
                50,
                15000,
            ),

        "price":
            f"${random.uniform(1.99, 19.99):.2f}",

        "genre":
            random.choice(
                [
                    "Fiction",
                    "Technology",
                    "History",
                    "Psychology",
                    "Biography",
                    "Fantasy",
                    "Science Fiction",
                ]
            ),

        "kindle_unlimited":
            random.random()
            < 0.35,

        "bestseller":
            random.random()
            < 0.15,

        "sample_available":
            random.random()
            < 0.70,
    }


# ==========================================================
# Recent Search
# ==========================================================

def generate_recent_searches() -> list[str]:

    return random.sample(
        SEARCH_QUERIES,
        k=random.randint(
            3,
            6,
        ),
    )


# ==========================================================
# Suggestions
# ==========================================================

def generate_suggestions(
    query: str,
) -> list[dict]:

    return [
        {
            "text":
                suggestion,

            "type":
                random.choice(
                    [
                        "query",
                        "author",
                        "book",
                    ]
                ),
        }
        for suggestion in random.sample(
            SEARCH_QUERIES,
            k=random.randint(
                4,
                7,
            ),
        )
    ]


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> dict:

    return {

        "format": random.choice(
            [
                "All formats",
                "Kindle",
                "Books",
            ]
        ),

        "rating": random.choice(
            [
                "Any rating",
                "4 stars & up",
                "4.5 stars & up",
            ]
        ),

        "price": random.choice(
            [
                "Any price",
                "Under $5",
                "$5–$10",
                "$10–$20",
            ]
        ),

        "sort": random.choice(
            [
                "Relevance",
                "Top rated",
                "Newest",
                "Price: Low to high",
            ]
        ),

        "unlimited_only":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Search Page Generator
# ==========================================================

def generate_search_page() -> dict:

    state = random.choice(
        SEARCH_STATES
    )

    query = random.choice(
        SEARCH_QUERIES
    )

    has_query = state in {
        "suggestions",
        "results",
        "no_results",
        "filters_open",
        "preview_open",
    }


    # ======================================================
    # Results
    # ======================================================

    result_count = 0

    results = []

    if state in {
        "results",
        "filters_open",
        "preview_open",
    }:

        result_count = random.randint(
            8,
            24,
        )

        results = [
            generate_search_book(
                index
            )
            for index in range(
                result_count
            )
        ]


    # ======================================================
    # Preview
    # ======================================================

    preview_book = None

    if state == "preview_open":

        if not results:

            results = [
                generate_search_book(
                    index
                )
                for index in range(
                    8
                )
            ]

        preview_book = random.choice(
            results
        )


    # ======================================================
    # Page
    # ======================================================

    return {

        "state":
            state,


        # ==================================================
        # State Flags
        # ==================================================

        "show_recent":
            state
            in {
                "search_idle",
                "recent_searches",
            },

        "show_suggestions":
            state
            == "suggestions",

        "show_results":
            state
            in {
                "results",
                "filters_open",
                "preview_open",
            },

        "show_no_results":
            state
            == "no_results",

        "show_filters":
            state
            == "filters_open",

        "show_categories":
            state
            in {
                "search_idle",
                "category_browse",
            },

        "show_preview":
            state
            == "preview_open",


        # ==================================================
        # Search
        # ==================================================

        "query":
            query
            if has_query
            else "",

        "placeholder":
            random.choice(
                [
                    "Search Kindle",
                    "Search books, authors and genres",
                    "Find your next book",
                ]
            ),


        # ==================================================
        # Recent
        # ==================================================

        "recent_searches":
            generate_recent_searches(),


        # ==================================================
        # Suggestions
        # ==================================================

        "suggestions":
            generate_suggestions(
                query
            ),


        # ==================================================
        # Results
        # ==================================================

        "result_count":
            result_count,

        "results":
            results,


        # ==================================================
        # Categories
        # ==================================================

        "categories":
            CATEGORIES,


        # ==================================================
        # Filters
        # ==================================================

        "filters":
            generate_filters(),


        # ==================================================
        # Preview
        # ==================================================

        "preview_book":
            preview_book,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = generate_search_page()

    print(
        "\n=============================="
    )

    print(
        "KINDLE SEARCH"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page["state"],
    )

    print(
        "Query:",
        page["query"],
    )

    print(
        "Results:",
        len(
            page["results"]
        ),
    )