from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

NOTEPAD_STATES = [
    "blank",
    "document",
    "multiple_tabs",
    "unsaved",
    "find",
    "replace",
    "word_wrap",
    "zoomed",
    "settings",
    "save_as",
    "encoding_menu",
    "close_unsaved_dialog",
]


# ==========================================================
# Sample Documents
# ==========================================================

DOCUMENT_POOL = [
    {
        "name": "notes.txt",
        "content": [
            "Research notes",
            "",
            "1. Review the latest experiment results.",
            "2. Check the annotation distribution.",
            "3. Prepare figures for the presentation.",
            "4. Compare light and dark mode performance.",
            "",
            "Next meeting: Friday at 2:30 PM.",
        ],
    },
    {
        "name": "todo.txt",
        "content": [
            "TODO",
            "",
            "- Run dataset generation",
            "- Verify YOLO labels",
            "- Check screenshot quality",
            "- Review model training logs",
            "- Update documentation",
        ],
    },
    {
        "name": "experiment.txt",
        "content": [
            "Experiment Summary",
            "",
            "Dataset: synthetic GUI screenshots",
            "Model: object detection baseline",
            "Status: training",
            "",
            "Notes:",
            "The current layout diversity looks improved.",
            "Need to inspect small-element annotations.",
        ],
    },
    {
        "name": "meeting_notes.txt",
        "content": [
            "Meeting Notes",
            "",
            "Topic: GUI dataset generation",
            "Participants: Research team",
            "",
            "Discussion:",
            "- Increase page diversity",
            "- Add more popup states",
            "- Continue testing viewport variations",
        ],
    },
]


# ==========================================================
# Encoding
# ==========================================================

ENCODINGS = [
    "UTF-8",
    "UTF-8 with BOM",
    "UTF-16 LE",
    "UTF-16 BE",
    "ANSI",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_tabs(
    state: str,
) -> list[dict]:

    if state == "multiple_tabs":

        count = random.randint(
            2,
            4,
        )

    else:

        count = 1


    selected_documents = random.sample(
        DOCUMENT_POOL,
        k=min(
            count,
            len(
                DOCUMENT_POOL
            ),
        ),
    )


    tabs = []

    for index, doc in enumerate(
        selected_documents
    ):

        tabs.append(
            {
                "name":
                    doc["name"],

                "active":
                    index == 0,

                "unsaved":
                    (
                        state
                        in {
                            "unsaved",
                            "close_unsaved_dialog",
                        }
                        and
                        index == 0
                    ),
            }
        )

    return tabs


def generate_document(
    state: str,
) -> dict:

    if state == "blank":

        return {
            "name":
                "Untitled",

            "content":
                [],

            "unsaved":
                False,
        }


    document = random.choice(
        DOCUMENT_POOL
    )


    return {
        "name":
            document["name"],

        "content":
            document["content"],

        "unsaved":
            state
            in {
                "unsaved",
                "close_unsaved_dialog",
            },
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_notepad_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            NOTEPAD_STATES
        )


    if state not in NOTEPAD_STATES:

        raise ValueError(
            f"Unknown Notepad state: "
            f"{state}"
        )


    document = generate_document(
        state
    )


    tabs = generate_tabs(
        state
    )


    search_query = (
        random.choice(
            [
                "dataset",
                "experiment",
                "notes",
                "review",
                "training",
            ]
        )
        if state
        in {
            "find",
            "replace",
        }
        else ""
    )


    replace_text = (
        random.choice(
            [
                "results",
                "analysis",
                "dataset",
                "model",
            ]
        )
        if state
        == "replace"
        else ""
    )


    zoom = (
        random.choice(
            [
                125,
                150,
                175,
                200,
            ]
        )
        if state
        == "zoomed"
        else 100
    )


    return {
        "state":
            state,

        "document":
            document,

        "tabs":
            tabs,

        "search_query":
            search_query,

        "replace_text":
            replace_text,

        "word_wrap":
            state
            == "word_wrap"
            or random.random()
            < 0.55,

        "zoom":
            zoom,

        "line":
            random.randint(
                1,
                max(
                    1,
                    len(
                        document[
                            "content"
                        ]
                    ),
                ),
            ),

        "column":
            random.randint(
                1,
                30,
            ),

        "encoding":
            random.choice(
                ENCODINGS
            ),

        "available_encodings":
            ENCODINGS,

        "settings": {
            "theme":
                random.choice(
                    [
                        "System",
                        "Light",
                        "Dark",
                    ]
                ),

            "font":
                random.choice(
                    [
                        "Consolas",
                        "Cascadia Mono",
                        "Segoe UI",
                        "Courier New",
                    ]
                ),

            "font_size":
                random.choice(
                    [
                        11,
                        12,
                        14,
                        16,
                    ]
                ),

            "word_wrap":
                random.random()
                < 0.65,
        },

        "save_as": {
            "filename":
                random.choice(
                    [
                        "notes.txt",
                        "research_notes.txt",
                        "document.txt",
                    ]
                ),

            "folder":
                random.choice(
                    [
                        "Documents",
                        "Desktop",
                        "Downloads",
                    ]
                ),
        },
    }