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

HIGHLIGHT_STATES = [
    "highlights_list",
    "notes_list",
    "searching",
    "multi_select",
    "edit_note",
    "filter_menu",
    "delete_confirmation",
    "empty_state",
]


# ==========================================================
# Highlight Colors
# ==========================================================

HIGHLIGHT_COLORS = [
    "yellow",
    "blue",
    "pink",
    "orange",
]


# ==========================================================
# Books
# ==========================================================

BOOK_TITLES = [
    "The Silent Horizon",
    "Fragments of Memory",
    "The Hidden Machine",
    "A Study of Tomorrow",
    "Beyond the Last City",
    "The Art of Thinking",
    "Notes from the River",
]


# ==========================================================
# Entry
# ==========================================================

def generate_entry(
    index: int,
) -> dict:

    has_note = (
        random.random()
        < 0.55
    )

    return {

        "id":
            f"entry_{index:03d}",

        "book_title":
            random.choice(
                BOOK_TITLES
            ),

        "author":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "chapter":
            random.choice(
                [
                    "Chapter 2",
                    "Chapter 4",
                    "Chapter 7",
                    "Chapter 9",
                    "Introduction",
                    "Epilogue",
                ]
            ),

        "location":
            random.randint(
                120,
                5100,
            ),

        "highlight":
            fake.paragraph(
                nb_sentences=random.randint(
                    1,
                    3,
                )
            ),

        "note":
            (
                fake.sentence(
                    nb_words=random.randint(
                        6,
                        16,
                    )
                )
                if has_note
                else ""
            ),

        "has_note":
            has_note,

        "highlight_color":
            random.choice(
                HIGHLIGHT_COLORS
            ),

        "created":
            random.choice(
                [
                    "Today",
                    "Yesterday",
                    "3 days ago",
                    "Last week",
                    "2 weeks ago",
                ]
            ),

        "selected":
            False,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_highlights_page() -> dict:

    state = random.choice(
        HIGHLIGHT_STATES
    )

    entry_count = random.randint(
        8,
        18,
    )

    entries = [
        generate_entry(
            index
        )
        for index in range(
            entry_count
        )
    ]


    # ======================================================
    # Multi Select
    # ======================================================

    if state == "multi_select":

        selected_count = random.randint(
            1,
            min(
                4,
                len(
                    entries
                ),
            ),
        )

        indices = random.sample(
            range(
                len(
                    entries
                )
            ),
            k=selected_count,
        )

        for index in indices:

            entries[
                index
            ][
                "selected"
            ] = True


    # ======================================================
    # Empty State
    # ======================================================

    if state == "empty_state":

        entries = []


    # ======================================================
    # Search State
    # ======================================================

    search_query = ""

    if state == "searching":

        search_query = random.choice(
            [
                "memory",
                "future",
                "machine",
                "journey",
            ]
        )


    # ======================================================
    # Popup
    # ======================================================

    show_edit_note = (
        state
        == "edit_note"
    )

    show_filter_menu = (
        state
        == "filter_menu"
    )

    show_delete_confirmation = (
        state
        == "delete_confirmation"
    )

    popup_open = any(
        [
            show_edit_note,
            show_filter_menu,
            show_delete_confirmation,
        ]
    )


    # ======================================================
    # Active Entry
    # ======================================================

    active_entry = (
        random.choice(
            entries
        )
        if entries
        else None
    )


    return {

        "state":
            state,

        "entries":
            entries,

        "active_entry":
            active_entry,

        "active_tab":
            (
                "Notes"
                if state == "notes_list"
                else "Highlights"
            ),

        "search_query":
            search_query,

        "multi_select":
            state == "multi_select",

        "show_edit_note":
            show_edit_note,

        "show_filter_menu":
            show_filter_menu,

        "show_delete_confirmation":
            show_delete_confirmation,

        "popup_open":
            popup_open,

        "filter_book":
            random.choice(
                [
                    "All books",
                    random.choice(
                        BOOK_TITLES
                    ),
                ]
            ),

        "sort":
            random.choice(
                [
                    "Newest",
                    "Oldest",
                    "Book",
                    "Location",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_highlights_page()
    )

    print(
        "\n=============================="
    )

    print(
        "KINDLE HIGHLIGHTS & NOTES"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page["state"],
    )

    print(
        "Entries:",
        len(
            page["entries"]
        ),
    )

    print(
        "Popup:",
        page["popup_open"],
    )