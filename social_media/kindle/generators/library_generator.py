from __future__ import annotations

import random

from faker import Faker

from social_media.kindle.generators.media_generator import (
    get_random_author_image,
    get_random_book_cover,
)


fake = Faker()


# ==========================================================
# Configuration
# ==========================================================

BOOK_COUNTS = [
    8,
    10,
    12,
    14,
    16,
]


LIBRARY_TABS = [
    "All",
    "Books",
    "Samples",
    "Documents",
]


SORT_OPTIONS = [
    "Recent",
    "Title",
    "Author",
]


VIEW_MODES = [
    "grid",
    "list",
]


BOOK_STATES = [
    "downloaded",
    "cloud",
    "reading",
    "finished",
]


BOOK_GENRES = [
    "Fiction",
    "Mystery",
    "Science",
    "History",
    "Biography",
    "Technology",
    "Fantasy",
    "Romance",
    "Business",
    "Philosophy",
]


# ==========================================================
# Book Titles
# ==========================================================

TITLE_STARTS = [
    "The Silent",
    "Beyond the",
    "Echoes of",
    "A Study of",
    "The Last",
    "Hidden",
    "Fragments of",
    "The Art of",
    "Letters from",
    "Notes on",
    "Understanding",
    "The Future of",
    "Journey Through",
    "Inside the",
    "Stories from",
]


TITLE_ENDS = [
    "Forest",
    "Sky",
    "Mind",
    "Ocean",
    "Machine",
    "World",
    "Night",
    "City",
    "Unknown",
    "Stars",
    "Memory",
    "River",
    "Empire",
    "Dream",
    "Future",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_book_title() -> str:

    return (
        f"{random.choice(TITLE_STARTS)} "
        f"{random.choice(TITLE_ENDS)}"
    )


def generate_author_name() -> str:

    return fake.name()


def generate_progress() -> int:

    values = [
        0,
        0,
        0,
        random.randint(
            3,
            25,
        ),
        random.randint(
            25,
            65,
        ),
        random.randint(
            65,
            95,
        ),
        100,
    ]

    return random.choice(
        values
    )


# ==========================================================
# Book
# ==========================================================

def generate_book(
    index: int,
) -> dict:

    progress = generate_progress()

    if progress == 100:

        state = "finished"

    elif progress > 0:

        state = "reading"

    else:

        state = random.choice(
            [
                "downloaded",
                "cloud",
            ]
        )

    return {

        "id":
            f"book_{index:03d}",

        "title":
            generate_book_title(),

        "author":
            generate_author_name(),

        "cover":
            get_random_book_cover(),

        "author_image":
            get_random_author_image(),

        "genre":
            random.choice(
                BOOK_GENRES
            ),

        "progress":
            progress,

        "state":
            state,

        "downloaded":
            state
            in {
                "downloaded",
                "reading",
                "finished",
            },

        "is_new":
            random.random()
            < 0.14,

        "is_sample":
            random.random()
            < 0.10,

        "rating":
            round(
                random.uniform(
                    3.6,
                    5.0,
                ),
                1,
            ),

        "pages":
            random.randint(
                160,
                740,
            ),

        "last_opened":
            random.choice(
                [
                    "Today",
                    "Yesterday",
                    "2 days ago",
                    "Last week",
                    "2 weeks ago",
                ]
            ),

        "description":
            fake.paragraph(
                nb_sentences=3
            ),
    }


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> list[dict]:

    return [

        {
            "label": "Home",
            "icon": "home",
            "active": False,
        },

        {
            "label": "Library",
            "icon": "library_books",
            "active": True,
        },

        {
            "label": "Discover",
            "icon": "explore",
            "active": False,
        },

        {
            "label": "More",
            "icon": "menu",
            "active": False,
        },
    ]


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> list[dict]:

    filters = [

        {
            "label": "Downloaded",
            "icon": "download_done",
        },

        {
            "label": "Unread",
            "icon": "bookmark_border",
        },

        {
            "label": "Books",
            "icon": "menu_book",
        },
    ]

    selected_index = random.randrange(
        len(filters)
    )

    for index, item in enumerate(
        filters
    ):

        item[
            "selected"
        ] = (
            index
            == selected_index
        )

    return filters


# ==========================================================
# Library Generator
# ==========================================================

def generate_library_data() -> dict:

    book_count = random.choice(
        BOOK_COUNTS
    )

    books = [

        generate_book(
            index
        )

        for index
        in range(
            book_count
        )
    ]

    continue_reading = [

        book

        for book
        in books

        if (
            book[
                "progress"
            ]
            > 0
            and book[
                "progress"
            ]
            < 100
        )
    ]

    if not continue_reading:

        selected = random.choice(
            books
        )

        selected[
            "progress"
        ] = random.randint(
            15,
            75,
        )

        selected[
            "state"
        ] = "reading"

        continue_reading = [
            selected
        ]

    return {

        # ==================================================
        # Identity
        # ==================================================

        "page_title":
            "Library",

        "greeting":
            random.choice(
                [
                    "Your Library",
                    "My Kindle Library",
                    "Books & Documents",
                ]
            ),


        # ==================================================
        # Search
        # ==================================================

        "search_placeholder":
            random.choice(
                [
                    "Search your library",
                    "Search books and authors",
                    "Find a title",
                ]
            ),


        # ==================================================
        # View State
        # ==================================================

        "view_mode":
            random.choice(
                VIEW_MODES
            ),

        "sort":
            random.choice(
                SORT_OPTIONS
            ),

        "active_tab":
            random.choice(
                LIBRARY_TABS[:2]
            ),


        # ==================================================
        # Controls
        # ==================================================

        "tabs": [

            {
                "label":
                    tab,

                "active":
                    False,
            }

            for tab
            in LIBRARY_TABS
        ],

        "filters":
            generate_filters(),

        "navigation":
            generate_navigation(),


        # ==================================================
        # Books
        # ==================================================

        "books":
            books,

        "continue_reading":
            continue_reading[:4],


        # ==================================================
        # Counts
        # ==================================================

        "book_count":
            book_count,

        "downloaded_count":
            sum(
                1
                for book
                in books
                if book[
                    "downloaded"
                ]
            ),
    }


# ==========================================================
# Finalize Tab State
# ==========================================================

def generate_library_page() -> dict:

    data = generate_library_data()

    active_tab = data[
        "active_tab"
    ]

    for tab in data[
        "tabs"
    ]:

        tab[
            "active"
        ] = (
            tab[
                "label"
            ]
            == active_tab
        )

    return data


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_library_page()

    print(
        "\n=============================="
    )

    print(
        "KINDLE LIBRARY DATA"
    )

    print(
        "=============================="
    )

    print(
        "View mode:",
        data[
            "view_mode"
        ]
    )

    print(
        "Books:",
        len(
            data[
                "books"
            ]
        )
    )

    print(
        "Continue reading:",
        len(
            data[
                "continue_reading"
            ]
        )
    )

    print(
        "Active tab:",
        data[
            "active_tab"
        ]
    )