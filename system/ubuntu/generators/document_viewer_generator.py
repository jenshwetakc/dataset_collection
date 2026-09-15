from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

DOCUMENT_VIEWER_STATES = [

    "document_open",

    "thumbnail_sidebar",

    "two_page_view",

    "zoomed_in",

    "zoomed_out",

    "search_open",

    "search_results",

    "bookmarks_open",

    "annotations_open",

    "presentation_mode",

    "properties_open",

    "password_prompt",

    "print_dialog",

    "close_unsaved_dialog",
]


# ==========================================================
# Document Names
# ==========================================================

DOCUMENT_NAMES = [

    "research-paper.pdf",

    "project-report.pdf",

    "meeting-notes.pdf",

    "user-study.pdf",

    "design-specification.pdf",

    "lecture-slides.pdf",

    "technical-report.pdf",

    "thesis-draft.pdf",

    "requirements.pdf",

    "experiment-results.pdf",
]


# ==========================================================
# Bookmark Titles
# ==========================================================

BOOKMARK_TITLES = [

    "Introduction",

    "Background",

    "Methodology",

    "Implementation",

    "Evaluation",

    "Results",

    "Discussion",

    "Limitations",

    "Conclusion",

    "References",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_page(
    index: int,
) -> dict:

    paragraph_count = random.randint(
        3,
        6,
    )

    paragraphs = [

        fake.paragraph(
            nb_sentences=random.randint(
                2,
                4,
            )
        )

        for _ in range(
            paragraph_count
        )
    ]


    return {

        "number":
            index + 1,

        "title":
            random.choice(
                [
                    "",
                    fake.sentence(
                        nb_words=random.randint(
                            3,
                            7,
                        )
                    ).rstrip(
                        "."
                    ),
                ]
            ),

        "paragraphs":
            paragraphs,

        "has_figure":
            random.random()
            < 0.34,

        "has_table":
            random.random()
            < 0.22,

        "selected":
            False,
    }


def generate_pages() -> list[dict]:

    count = random.randint(
        8,
        18,
    )


    pages = [

        generate_page(
            index
        )

        for index in range(
            count
        )
    ]


    current_index = random.randrange(
        len(
            pages
        )
    )

    pages[
        current_index
    ][
        "selected"
    ] = True


    return pages


# ==========================================================
# Bookmarks
# ==========================================================

def generate_bookmarks(
    total_pages: int,
) -> list[dict]:

    count = random.randint(
        4,
        min(
            8,
            total_pages,
        ),
    )


    titles = random.sample(
        BOOKMARK_TITLES,
        k=count,
    )


    bookmarks = []


    for index, title in enumerate(
        titles
    ):

        bookmarks.append(
            {
                "title":
                    title,

                "page":
                    min(
                        total_pages,
                        1
                        + index
                        * random.randint(
                            1,
                            3,
                        ),
                    ),
            }
        )


    return bookmarks


# ==========================================================
# Search Results
# ==========================================================

def generate_search_results(
    total_pages: int,
) -> list[dict]:

    query = random.choice(
        [
            "method",
            "result",
            "system",
            "evaluation",
            "design",
            "dataset",
        ]
    )


    count = random.randint(
        3,
        7,
    )


    results = []


    for index in range(
        count
    ):

        results.append(
            {
                "page":
                    random.randint(
                        1,
                        total_pages,
                    ),

                "snippet":
                    fake.sentence(
                        nb_words=random.randint(
                            8,
                            14,
                        )
                    ),

                "match_index":
                    index + 1,
            }
        )


    return query, results


# ==========================================================
# Annotations
# ==========================================================

def generate_annotations(
    total_pages: int,
) -> list[dict]:

    types = [
        "Highlight",
        "Note",
        "Underline",
    ]


    entries = []


    for index in range(
        random.randint(
            3,
            6,
        )
    ):

        annotation_type = random.choice(
            types
        )


        entries.append(
            {
                "type":
                    annotation_type,

                "page":
                    random.randint(
                        1,
                        total_pages,
                    ),

                "text":
                    fake.sentence(
                        nb_words=random.randint(
                            5,
                            11,
                        )
                    ),

                "icon":
                    (
                        "highlight"
                        if annotation_type
                        == "Highlight"
                        else
                        "comment"
                        if annotation_type
                        == "Note"
                        else
                        "format_underlined"
                    ),
            }
        )


    return entries


# ==========================================================
# Metadata
# ==========================================================

def generate_properties(
    name: str,
    total_pages: int,
) -> list[dict]:

    return [

        {
            "label":
                "File",

            "value":
                name,

            "icon":
                "description",
        },

        {
            "label":
                "Pages",

            "value":
                str(
                    total_pages
                ),

            "icon":
                "article",
        },

        {
            "label":
                "File Size",

            "value":
                f"{random.uniform(0.8, 18.0):.1f} MB",

            "icon":
                "hard_drive",
        },

        {
            "label":
                "Format",

            "value":
                "PDF",

            "icon":
                "picture_as_pdf",
        },

        {
            "label":
                "Author",

            "value":
                fake.name(),

            "icon":
                "person",
        },

        {
            "label":
                "Created",

            "value":
                random.choice(
                    [
                        "Sep 5, 2026",
                        "Sep 3, 2026",
                        "Aug 28, 2026",
                        "Aug 15, 2026",
                    ]
                ),

            "icon":
                "calendar_today",
        },
    ]


# ==========================================================
# Main
# ==========================================================

def generate_document_viewer_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            DOCUMENT_VIEWER_STATES
        )


    if state not in DOCUMENT_VIEWER_STATES:

        raise ValueError(
            f"Unknown Document Viewer state: "
            f"{state}"
        )


    pages = generate_pages()


    current_page = next(
        page
        for page in pages
        if page[
            "selected"
        ]
    )


    total_pages = len(
        pages
    )


    # ======================================================
    # Zoom
    # ======================================================

    if state == "zoomed_in":

        zoom = random.choice(
            [
                150,
                175,
                200,
            ]
        )

    elif state == "zoomed_out":

        zoom = random.choice(
            [
                50,
                67,
                75,
            ]
        )

    else:

        zoom = random.choice(
            [
                90,
                100,
                110,
            ]
        )


    # ======================================================
    # Search
    # ======================================================

    search_query, search_results = (
        generate_search_results(
            total_pages
        )
    )


    # ======================================================
    # Print
    # ======================================================

    copies = random.randint(
        1,
        3,
    )


    # ======================================================
    # Result
    # ======================================================

    document_name = random.choice(
        DOCUMENT_NAMES
    )


    return {

        "state":
            state,

        "document_name":
            document_name,

        "pages":
            pages,

        "current_page":
            current_page,

        "total_pages":
            total_pages,

        "zoom":
            zoom,

        "search_query":
            (
                search_query
                if state in {
                    "search_open",
                    "search_results",
                }
                else ""
            ),

        "search_results":
            search_results,

        "bookmarks":
            generate_bookmarks(
                total_pages
            ),

        "annotations":
            generate_annotations(
                total_pages
            ),

        "properties":
            generate_properties(
                document_name,
                total_pages,
            ),

        "copies":
            copies,

        "print_all_pages":
            random.random()
            < 0.7,

        "duplex":
            random.random()
            < 0.5,

        "password_hint":
            random.choice(
                [
                    "",
                    "Password required",
                    "Enter document password",
                ]
            ),
    }