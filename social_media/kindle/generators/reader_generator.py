from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Reader States
# ==========================================================

READER_STATES = [
    "clean",
    "controls",
    "font_settings",
    "table_of_contents",
    "text_selection",
    "bookmarked",
]


# ==========================================================
# Reader Themes
# ==========================================================

READING_THEMES = [
    "system",
    "light",
    "sepia",
    "dark",
]


# ==========================================================
# Font Families
# ==========================================================

FONT_FAMILIES = [
    "Bookerly",
    "Georgia",
    "Arial",
    "Serif",
]


# ==========================================================
# Chapter Titles
# ==========================================================

CHAPTER_TITLES = [
    "A Quiet Beginning",
    "Across the River",
    "The Hidden Path",
    "A Different Morning",
    "Between Two Worlds",
    "The Long Journey",
    "What Remains",
    "Into the Unknown",
    "A New Direction",
    "The Final Letter",
]


# ==========================================================
# Paragraph Generator
# ==========================================================

def generate_paragraphs(
    count: int,
) -> list[str]:

    return [
        fake.paragraph(
            nb_sentences=random.randint(
                4,
                8,
            )
        )
        for _ in range(
            count
        )
    ]


# ==========================================================
# Contents
# ==========================================================

def generate_contents() -> list[dict]:

    chapter_count = random.randint(
        8,
        14,
    )

    current = random.randint(
        2,
        chapter_count - 1,
    )

    chapters = []

    for index in range(
        1,
        chapter_count + 1,
    ):

        chapters.append(
            {
                "number":
                    index,

                "title":
                    random.choice(
                        CHAPTER_TITLES
                    ),

                "active":
                    index == current,

                "progress":
                    random.randint(
                        0,
                        100,
                    ),
            }
        )

    return chapters


# ==========================================================
# Selected Text
# ==========================================================

def generate_selected_text() -> str:

    options = [
        "The smallest choices often shape the direction of an entire life.",
        "Memory has a strange way of preserving what the mind tries to forget.",
        "He understood then that distance was not measured only in miles.",
        "Every answer seemed to reveal another question waiting beneath it.",
    ]

    return random.choice(
        options
    )


# ==========================================================
# Reader Generator
# ==========================================================

def generate_reader_page() -> dict:

    state = random.choice(
        READER_STATES
    )

    progress = random.randint(
        4,
        96,
    )

    current_page = random.randint(
        10,
        380,
    )

    total_pages = random.randint(
        max(
            400,
            current_page + 20,
        ),
        760,
    )

    chapter_number = random.randint(
        1,
        12,
    )

    font_size = random.choice(
        [
            16,
            17,
            18,
            19,
            20,
            21,
            22,
        ]
    )

    line_height = random.choice(
        [
            1.45,
            1.55,
            1.65,
            1.75,
            1.85,
        ]
    )

    paragraphs = generate_paragraphs(
        random.randint(
            7,
            12,
        )
    )

    return {

        # ==================================================
        # State
        # ==================================================

        "state":
            state,

        "show_controls":
            state
            in {
                "controls",
                "font_settings",
                "table_of_contents",
                "text_selection",
                "bookmarked",
            },

        "show_font_settings":
            state
            == "font_settings",

        "show_contents":
            state
            == "table_of_contents",

        "show_selection":
            state
            == "text_selection",

        "bookmarked":
            state
            == "bookmarked",


        # ==================================================
        # Book
        # ==================================================

        "book_title":
            random.choice(
                [
                    "The Silent Horizon",
                    "Fragments of Memory",
                    "Beyond the Last City",
                    "A Study of Tomorrow",
                    "The Hidden River",
                ]
            ),

        "author":
            fake.name(),

        "chapter_number":
            chapter_number,

        "chapter_title":
            random.choice(
                CHAPTER_TITLES
            ),

        "paragraphs":
            paragraphs,


        # ==================================================
        # Reading Progress
        # ==================================================

        "progress":
            progress,

        "current_page":
            current_page,

        "total_pages":
            total_pages,

        "time_left":
            random.choice(
                [
                    "4 min left in chapter",
                    "7 min left in chapter",
                    "12 min left in chapter",
                    "18 min left in chapter",
                ]
            ),


        # ==================================================
        # Typography
        # ==================================================

        "font_family":
            random.choice(
                FONT_FAMILIES
            ),

        "font_size":
            font_size,

        "line_height":
            line_height,

        "margin_width":
            random.choice(
                [
                    "narrow",
                    "medium",
                    "wide",
                ]
            ),

        "reading_theme":
            random.choice(
                READING_THEMES
            ),


        # ==================================================
        # Contents
        # ==================================================

        "contents":
            generate_contents(),


        # ==================================================
        # Selection
        # ==================================================

        "selected_text":
            generate_selected_text(),

        "selection_action":
            random.choice(
                [
                    "highlight",
                    "note",
                    "lookup",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    reader = generate_reader_page()

    print(
        "\n=============================="
    )

    print(
        "KINDLE READER"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        reader[
            "state"
        ]
    )

    print(
        "Book:",
        reader[
            "book_title"
        ]
    )

    print(
        "Progress:",
        reader[
            "progress"
        ],
    )

    print(
        "Font:",
        reader[
            "font_family"
        ],
        reader[
            "font_size"
        ],
    )