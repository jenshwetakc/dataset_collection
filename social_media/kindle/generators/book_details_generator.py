from __future__ import annotations

import random

from faker import Faker

from social_media.kindle.generators.media_generator import (
    get_random_author_image,
    get_random_book_cover,
)


fake = Faker()


# ==========================================================
# Page States
# ==========================================================

BOOK_DETAIL_STATES = [
    "owned",
    "not_owned",
    "sample_available",
    "downloading",
    "downloaded",
    "reading",
    "finished",
    "wishlist",
    "more_options",
]


GENRES = [
    "Literary Fiction",
    "Mystery",
    "Thriller",
    "Science Fiction",
    "Fantasy",
    "Biography",
    "History",
    "Technology",
    "Business",
    "Psychology",
]


TITLE_STARTS = [
    "The Silent",
    "Beyond the",
    "Hidden",
    "Fragments of",
    "The Last",
    "Notes from",
    "A Study of",
    "Echoes of",
    "Inside the",
    "Journey Through",
]


TITLE_ENDS = [
    "Forest",
    "City",
    "Mind",
    "Future",
    "River",
    "Machine",
    "World",
    "Night",
    "Unknown",
    "Memory",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_title() -> str:

    return (
        f"{random.choice(TITLE_STARTS)} "
        f"{random.choice(TITLE_ENDS)}"
    )


def generate_review_breakdown() -> list[dict]:

    values = {
        5: random.randint(55, 80),
        4: random.randint(10, 25),
        3: random.randint(4, 12),
        2: random.randint(1, 6),
        1: random.randint(1, 5),
    }

    return [
        {
            "stars": stars,
            "percentage": percentage,
        }
        for stars, percentage
        in values.items()
    ]


def generate_related_books(
    count: int = 6,
) -> list[dict]:

    return [
        {
            "id": f"related_{index}",
            "title": generate_title(),
            "author": fake.name(),
            "cover": get_random_book_cover(),
            "rating": round(
                random.uniform(
                    3.8,
                    5.0,
                ),
                1,
            ),
        }
        for index in range(
            count
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_book_details_page() -> dict:

    state = random.choice(
        BOOK_DETAIL_STATES
    )

    owned = state in {
        "owned",
        "downloading",
        "downloaded",
        "reading",
        "finished",
        "more_options",
    }

    downloading = (
        state == "downloading"
    )

    downloaded = state in {
        "downloaded",
        "reading",
        "finished",
    }

    reading = (
        state == "reading"
    )

    finished = (
        state == "finished"
    )

    wishlist = (
        state == "wishlist"
    )

    sample_available = state in {
        "sample_available",
        "not_owned",
        "wishlist",
    }

    progress = 0

    if reading:

        progress = random.randint(
            10,
            89,
        )

    elif finished:

        progress = 100

    return {

        # ==================================================
        # State
        # ==================================================

        "state":
            state,

        "owned":
            owned,

        "downloading":
            downloading,

        "downloaded":
            downloaded,

        "reading":
            reading,

        "finished":
            finished,

        "wishlist":
            wishlist,

        "sample_available":
            sample_available,

        "show_more_menu":
            state == "more_options",


        # ==================================================
        # Book
        # ==================================================

        "title":
            generate_title(),

        "subtitle":
            random.choice(
                [
                    "",
                    "A Novel",
                    "Stories of Change",
                    "A Journey Into Tomorrow",
                    "Lessons from an Unexpected Life",
                ]
            ),

        "author":
            fake.name(),

        "author_image":
            get_random_author_image(),

        "cover":
            get_random_book_cover(),

        "genre":
            random.choice(
                GENRES
            ),

        "rating":
            round(
                random.uniform(
                    3.8,
                    5.0,
                ),
                1,
            ),

        "rating_count":
            random.randint(
                320,
                18500,
            ),

        "pages":
            random.randint(
                180,
                720,
            ),

        "language":
            "English",

        "publication_year":
            random.randint(
                2005,
                2026,
            ),

        "publisher":
            random.choice(
                [
                    "Northlight Press",
                    "Riverside Books",
                    "Oak House Publishing",
                    "Blue Lantern",
                    "Westbridge Press",
                ]
            ),

        "description":
            fake.paragraph(
                nb_sentences=6
            ),

        "price":
            f"${random.uniform(2.99, 19.99):.2f}",


        # ==================================================
        # Progress
        # ==================================================

        "progress":
            progress,

        "download_progress":
            random.randint(
                8,
                88,
            )
            if downloading
            else 0,


        # ==================================================
        # Reviews
        # ==================================================

        "review_breakdown":
            generate_review_breakdown(),

        "review_quotes": [
            {
                "name": fake.name(),
                "rating": random.randint(
                    4,
                    5,
                ),
                "text": fake.paragraph(
                    nb_sentences=2
                ),
            }
            for _ in range(
                random.randint(
                    2,
                    4,
                )
            )
        ],


        # ==================================================
        # Related
        # ==================================================

        "related_books":
            generate_related_books(
                random.randint(
                    4,
                    8,
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    book = generate_book_details_page()

    print(
        "\n=============================="
    )

    print(
        "KINDLE BOOK DETAILS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        book["state"],
    )

    print(
        "Title:",
        book["title"],
    )

    print(
        "Owned:",
        book["owned"],
    )

    print(
        "Downloaded:",
        book["downloaded"],
    )