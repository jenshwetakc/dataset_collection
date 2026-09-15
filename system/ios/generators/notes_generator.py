from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

NOTES_STATES = [

    "notes_list",

    "note_editor",

    "checklist",

    "folder_view",

    "search_active",

    "drawing",

    "share_sheet",

    "delete_confirmation",
]


NOTES_STATE_WEIGHTS = [

    22,

    22,

    12,

    10,

    10,

    10,

    8,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Note
# ==========================================================

def generate_note(
    index: int,
) -> dict:

    titles = [

        "Research Notes",

        "Meeting Summary",

        "Ideas",

        "Weekly Tasks",

        "Experiment Results",

        "Presentation Outline",

        "Reading List",

        "Travel Plans",

        "Shopping List",

        "Project Notes",
    ]


    snippets = [

        "Review the latest results and compare with the previous run.",

        "Discuss the next milestones and prepare updated slides.",

        "Check the dataset generation pipeline and annotation output.",

        "Read the paper and summarize the main findings.",

        "Prepare examples for tomorrow's meeting.",

        "Update the implementation notes before the next experiment.",

        "Remember to verify the viewport rendering behavior.",

        "Finalize the list of tasks for this week.",
    ]


    return {

        "id":
            f"note_{index}",

        "title":
            random.choice(
                titles
            ),

        "snippet":
            random.choice(
                snippets
            ),

        "time":
            random.choice([
                "9:41 AM",
                "10:12 AM",
                "11:27 AM",
                "1:05 PM",
                "Yesterday",
                "Friday",
                "Thursday",
            ]),

        "pinned":
            random.random() < 0.20,

        "locked":
            random.random() < 0.08,

        "has_attachment":
            random.random() < 0.25,

        "word_count":
            random.randint(
                18,
                180,
            ),
    }


# ==========================================================
# Notes
# ==========================================================

def generate_notes(
    count: int = 12,
) -> list[dict]:

    return [

        generate_note(
            index
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Folder
# ==========================================================

def generate_folders() -> list[dict]:

    definitions = [

        "Notes",

        "Work",

        "Research",

        "Personal",

        "Shared",

        "Recently Deleted",
    ]


    result = []


    for index, title in enumerate(
        definitions
    ):

        result.append({

            "id":
                title
                .lower()
                .replace(
                    " ",
                    "_"
                ),

            "title":
                title,

            "count":
                random.randint(
                    2,
                    48,
                ),

            "shared":
                title == "Shared",

            "deleted":
                title == "Recently Deleted",

            "icon":
                get_lucide_icon(
                    "folder"
                ),
        })


    return result


# ==========================================================
# Checklist
# ==========================================================

def generate_checklist() -> list[dict]:

    items = [

        "Review experiment logs",

        "Generate new screenshots",

        "Check annotations",

        "Update presentation",

        "Read related paper",

        "Prepare meeting notes",

        "Run validation",

        "Upload latest results",
    ]


    random.shuffle(
        items
    )


    return [

        {
            "id":
                f"check_{index}",

            "text":
                item,

            "checked":
                random.random() < 0.40,
        }

        for index, item
        in enumerate(
            items[:6]
        )
    ]


# ==========================================================
# Search
# ==========================================================

def generate_search_data(
    notes: list[dict],
) -> dict:

    query = random.choice([

        "research",

        "meeting",

        "project",

        "notes",

        "experiment",
    ])


    results = [

        note

        for note
        in notes

        if (
            query.lower()
            in note["title"].lower()
            or query.lower()
            in note["snippet"].lower()
        )
    ]


    if not results:

        results = random.sample(

            notes,

            k=min(
                len(
                    notes
                ),
                5,
            ),
        )


    return {

        "query":
            query,

        "results":
            results,
    }


# ==========================================================
# Drawing
# ==========================================================

def generate_drawing_data() -> dict:

    strokes = []


    for index in range(
        random.randint(
            5,
            9,
        )
    ):

        strokes.append({

            "id":
                f"stroke_{index}",

            "x":
                random.randint(
                    8,
                    78,
                ),

            "y":
                random.randint(
                    10,
                    76,
                ),

            "width":
                random.randint(
                    50,
                    160,
                ),

            "rotation":
                random.randint(
                    -35,
                    35,
                ),

            "thickness":
                random.choice([
                    2,
                    3,
                    4,
                    5,
                ]),
        })


    return {

        "strokes":
            strokes,

        "selected_tool":
            random.choice([
                "pen",
                "marker",
                "pencil",
            ]),

        "tools": [

            {
                "id":
                    "pen",

                "icon":
                    get_lucide_icon(
                        "pen-tool"
                    ),
            },

            {
                "id":
                    "marker",

                "icon":
                    get_lucide_icon(
                        "highlighter"
                    ),
            },

            {
                "id":
                    "pencil",

                "icon":
                    get_lucide_icon(
                        "pencil"
                    ),
            },

            {
                "id":
                    "eraser",

                "icon":
                    get_lucide_icon(
                        "eraser"
                    ),
            },

            {
                "id":
                    "lasso",

                "icon":
                    get_lucide_icon(
                        "scan"
                    ),
            },
        ],
    }


# ==========================================================
# Share Sheet
# ==========================================================

def generate_share_sheet() -> dict:

    return {

        "title":
            "Share Note",

        "apps": [

            {
                "id":
                    "messages",

                "title":
                    "Messages",

                "icon":
                    resolve_icon(
                        "message",
                        "message-circle",
                    ),

                "style":
                    "green",
            },

            {
                "id":
                    "mail",

                "title":
                    "Mail",

                "icon":
                    resolve_icon(
                        "mail",
                        "mail",
                    ),

                "style":
                    "blue",
            },

            {
                "id":
                    "files",

                "title":
                    "Files",

                "icon":
                    resolve_icon(
                        "folder",
                        "folder",
                    ),

                "style":
                    "blue",
            },

            {
                "id":
                    "copy",

                "title":
                    "Copy",

                "icon":
                    get_lucide_icon(
                        "copy"
                    ),

                "style":
                    "gray",
            },
        ],

        "actions": [

            {
                "id":
                    "collaborate",

                "title":
                    "Collaborate",

                "icon":
                    get_lucide_icon(
                        "users"
                    ),
            },

            {
                "id":
                    "send_copy",

                "title":
                    "Send Copy",

                "icon":
                    get_lucide_icon(
                        "send"
                    ),
            },

            {
                "id":
                    "print",

                "title":
                    "Print",

                "icon":
                    get_lucide_icon(
                        "printer"
                    ),
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_notes_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            NOTES_STATES,

            weights=
                NOTES_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in NOTES_STATES:

        raise ValueError(
            f"Unknown Notes state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Data
    # ======================================================

    notes = generate_notes()


    active_note = random.choice(
        notes
    )


    folders = (
        generate_folders()
    )


    active_folder = random.choice(
        folders
    )


    # ======================================================
    # Overlay
    # ======================================================

    is_overlay_state = (
        state
        in {
            "share_sheet",
            "delete_confirmation",
        }
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "title":
            "Notes",


        # --------------------------------------------------
        # Notes
        # --------------------------------------------------

        "notes":
            notes,

        "active_note":
            active_note,


        # --------------------------------------------------
        # Folders
        # --------------------------------------------------

        "folders":
            folders,

        "active_folder":
            active_folder,


        # --------------------------------------------------
        # Checklist
        # --------------------------------------------------

        "checklist":
            generate_checklist(),


        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "search":
            generate_search_data(
                notes
            ),


        # --------------------------------------------------
        # Drawing
        # --------------------------------------------------

        "drawing":
            generate_drawing_data(),


        # --------------------------------------------------
        # Share
        # --------------------------------------------------

        "share_sheet":
            generate_share_sheet(),


        # --------------------------------------------------
        # Delete
        # --------------------------------------------------

        "delete_confirmation": {

            "title":
                "Delete Note?",

            "message":
                (
                    "This note will be moved "
                    "to Recently Deleted."
                ),

            "cancel":
                "Cancel",

            "confirm":
                "Delete Note",
        },


        # --------------------------------------------------
        # Icons
        # --------------------------------------------------

        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "compose":
                get_lucide_icon(
                    "square-pen"
                ),

            "back":
                resolve_icon(
                    "back"
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis"
                ),

            "folder":
                get_lucide_icon(
                    "folder"
                ),

            "folder_plus":
                get_lucide_icon(
                    "folder-plus"
                ),

            "pin":
                get_lucide_icon(
                    "pin"
                ),

            "lock":
                resolve_icon(
                    "lock"
                ),

            "attachment":
                get_lucide_icon(
                    "paperclip"
                ),

            "share":
                resolve_icon(
                    "share",
                    "share"
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "checklist":
                get_lucide_icon(
                    "list-checks"
                ),

            "draw":
                get_lucide_icon(
                    "pen-tool"
                ),

            "camera":
                resolve_icon(
                    "camera"
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in NOTES_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_notes_data(
                state=
                    state
            ),

            sort_dicts=False,
        )