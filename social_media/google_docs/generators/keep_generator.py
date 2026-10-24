from __future__ import annotations

import random

from faker import Faker


fake = Faker()


KEEP_STATES = [
    "notes_grid",
    "notes_list",
    "label_view",
    "search_results",
    "checklist_note",
    "note_editor",
    "color_picker",
    "archive",
    "trash",
]


NOTE_COLORS = [
    "#fff8b8",
    "#f4d7f3",
    "#d9f2e6",
    "#dbe9ff",
    "#fde0c5",
    "#e9e9e9",
]


LABELS = [
    "Work",
    "Personal",
    "Ideas",
    "Travel",
    "Recipes",
    "Important",
]


def generate_checklist() -> list[dict]:

    return [
        {
            "text":
                fake.sentence(
                    nb_words=random.randint(2, 5),
                ).rstrip("."),

            "checked":
                random.random() < 0.35,
        }
        for _ in range(
            random.randint(3, 7)
        )
    ]


def generate_note(
    index: int,
) -> dict:

    has_checklist = (
        random.random() < 0.35
    )

    return {
        "id":
            f"note_{index:03d}",

        "title":
            fake.sentence(
                nb_words=random.randint(2, 5),
            ).rstrip("."),

        "body":
            fake.paragraph(
                nb_sentences=random.randint(1, 3),
            ),

        "color":
            random.choice(
                NOTE_COLORS
            ),

        "label":
            random.choice(
                LABELS
            ),

        "pinned":
            random.random() < 0.25,

        "archived":
            random.random() < 0.18,

        "trashed":
            random.random() < 0.12,

        "checklist":
            (
                generate_checklist()
                if has_checklist
                else []
            ),
    }


def generate_keep_page(
    state: str | None = None,
) -> dict:

    state = (
        state
        or random.choice(
            KEEP_STATES
        )
    )

    notes = [
        generate_note(index)
        for index in range(
            random.randint(16, 26)
        )
    ]

    selected_note = random.choice(
        notes
    )

    checklist_note = next(
        (
            note
            for note in notes
            if note["checklist"]
        ),
        None,
    )

    if checklist_note is None:

        checklist_note = notes[0]

        checklist_note["checklist"] = (
            generate_checklist()
        )

    if state == "archive":

        visible_notes = [
            note
            for note in notes
            if note["archived"]
        ]

        if not visible_notes:

            notes[0]["archived"] = True
            visible_notes = [notes[0]]

    elif state == "trash":

        visible_notes = [
            note
            for note in notes
            if note["trashed"]
        ]

        if not visible_notes:

            notes[0]["trashed"] = True
            visible_notes = [notes[0]]

    elif state == "checklist_note":

        visible_notes = [
            checklist_note
        ]

        selected_note = checklist_note

    else:

        visible_notes = [
            note
            for note in notes
            if (
                not note["archived"]
                and not note["trashed"]
            )
        ]

    search_query = random.choice(
        [
            fake.word(),
            "project",
            "ideas",
            "travel",
            "recipe",
        ]
    )

    selected_label = random.choice(
        LABELS
    )

    return {
        "app_name":
            "Google Keep",

        "state":
            state,

        "notes":
            visible_notes,

        "selected_note":
            selected_note,

        "labels":
            LABELS,

        "selected_label":
            selected_label,

        "search_query":
            search_query,

        "view_mode":
            (
                "list"
                if state == "notes_list"
                else "grid"
            ),

        "title":
            {
                "notes_grid": "Notes",
                "notes_list": "Notes",
                "label_view": selected_label,
                "search_results": (
                    f"Search results for "
                    f"“{search_query}”"
                ),
                "checklist_note": "Notes",
                "note_editor": "Notes",
                "color_picker": "Notes",
                "archive": "Archive",
                "trash": "Trash",
            }[state],
    }