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

COLLECTION_STATES = [
    "collections_grid",
    "collection_open",
    "empty_collection",
    "multi_select",
    "create_collection",
    "rename_collection",
    "sort_menu",
    "delete_confirmation",
]


# ==========================================================
# Collection Names
# ==========================================================

COLLECTION_NAMES = [
    "Favorites",
    "To Read",
    "Research",
    "Weekend Reads",
    "Technology",
    "Fiction",
    "History",
    "Reference",
    "Summer Reading",
    "Work",
    "Study",
    "Classics",
]


# ==========================================================
# Book Generator
# ==========================================================

def generate_book(
    index: int,
) -> dict:

    return {

        "id":
            f"book_{index:03d}",

        "title":
            random.choice(
                [
                    "The Silent Horizon",
                    "Understanding Tomorrow",
                    "Beyond the Last City",
                    "Fragments of Memory",
                    "The Hidden Machine",
                    "A Study of Change",
                    "The Future Within",
                    "Echoes of History",
                    "Notes from the River",
                    "The Art of Thinking",
                ]
            ),

        "author":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "progress":
            random.choice(
                [
                    0,
                    random.randint(
                        10,
                        80,
                    ),
                    100,
                ]
            ),

        "downloaded":
            random.random()
            < 0.65,

        "selected":
            False,
    }


# ==========================================================
# Collection Generator
# ==========================================================

def generate_collection(
    index: int,
) -> dict:

    count = random.randint(
        0,
        16,
    )

    books = [
        generate_book(
            book_index
        )
        for book_index
        in range(
            count
        )
    ]

    preview_covers = [
        book["cover"]
        for book in books
        if book["cover"]
    ][:4]

    return {

        "id":
            f"collection_{index:03d}",

        "name":
            random.choice(
                COLLECTION_NAMES
            ),

        "book_count":
            count,

        "books":
            books,

        "preview_covers":
            preview_covers,

        "updated":
            random.choice(
                [
                    "Today",
                    "Yesterday",
                    "3 days ago",
                    "Last week",
                ]
            ),
    }


# ==========================================================
# Collections Page
# ==========================================================

def generate_collections_page() -> dict:

    state = random.choice(
        COLLECTION_STATES
    )

    collection_count = random.randint(
        5,
        10,
    )

    collections = [
        generate_collection(
            index
        )
        for index
        in range(
            collection_count
        )
    ]


    # ======================================================
    # Selected Collection
    # ======================================================

    active_collection = random.choice(
        collections
    )

    if state == "empty_collection":

        active_collection = {
            **active_collection,
            "book_count": 0,
            "books": [],
            "preview_covers": [],
        }


    # ======================================================
    # Multi Select
    # ======================================================

    if state == "multi_select":

        books = active_collection[
            "books"
        ]

        if not books:

            books = [
                generate_book(
                    index
                )
                for index
                in range(
                    6
                )
            ]

            active_collection[
                "books"
            ] = books

            active_collection[
                "book_count"
            ] = len(
                books
            )

        selected_count = random.randint(
            1,
            min(
                4,
                len(
                    books
                ),
            ),
        )

        selected_indices = random.sample(
            range(
                len(
                    books
                )
            ),
            k=selected_count,
        )

        for index in selected_indices:

            books[
                index
            ][
                "selected"
            ] = True


    # ======================================================
    # Popup States
    # ======================================================

    show_create_dialog = (
        state
        == "create_collection"
    )

    show_rename_dialog = (
        state
        == "rename_collection"
    )

    show_sort_menu = (
        state
        == "sort_menu"
    )

    show_delete_confirmation = (
        state
        == "delete_confirmation"
    )

    popup_open = any(
        [
            show_create_dialog,
            show_rename_dialog,
            show_sort_menu,
            show_delete_confirmation,
        ]
    )


    # ======================================================
    # Open State
    # ======================================================

    show_collection_contents = (
        state
        in {
            "collection_open",
            "empty_collection",
            "multi_select",
            "rename_collection",
            "sort_menu",
            "delete_confirmation",
        }
    )


    return {

        "state":
            state,

        "collections":
            collections,

        "active_collection":
            active_collection,

        "show_collection_contents":
            show_collection_contents,

        "multi_select":
            state
            == "multi_select",

        "show_create_dialog":
            show_create_dialog,

        "show_rename_dialog":
            show_rename_dialog,

        "show_sort_menu":
            show_sort_menu,

        "show_delete_confirmation":
            show_delete_confirmation,

        "popup_open":
            popup_open,

        "sort":
            random.choice(
                [
                    "Recent",
                    "Title",
                    "Author",
                    "Progress",
                ]
            ),

        "new_collection_name":
            random.choice(
                [
                    "Reading List",
                    "New Collection",
                    "Research Notes",
                    "Books for Later",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_collections_page()
    )

    print(
        "\n=============================="
    )

    print(
        "KINDLE COLLECTIONS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page[
            "state"
        ]
    )

    print(
        "Popup:",
        page[
            "popup_open"
        ]
    )

    print(
        "Active collection:",
        page[
            "active_collection"
        ][
            "name"
        ]
    )