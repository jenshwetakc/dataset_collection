from __future__ import annotations

import random

from faker import Faker


fake = Faker()


LABEL_STATES = [
    "labels_list",
    "label_selected",
    "create_label",
    "edit_label",
    "nested_labels",
    "color_picker_popup",
    "move_messages_dialog",
    "delete_label_confirm",
    "mobile_label_sheet",
]


LABEL_COLORS = [
    "red",
    "orange",
    "yellow",
    "green",
    "teal",
    "blue",
    "purple",
    "pink",
]


def _label(
    index: int,
) -> dict:

    nested = (
        random.random()
        < 0.35
    )

    return {
        "id":
            f"label_{index}",

        "name":
            random.choice([
                "Work",
                "Research",
                "Personal",
                "Travel",
                "Receipts",
                "Important",
                "Projects",
                "Newsletters",
            ]),

        "color":
            random.choice(
                LABEL_COLORS
            ),

        "message_count":
            random.randint(
                3,
                420,
            ),

        "unread_count":
            random.randint(
                0,
                30,
            ),

        "nested":
            nested,

        "parent":
            (
                random.choice([
                    "Work",
                    "Projects",
                    "Personal",
                ])
                if nested
                else None
            ),
    }


def generate_labels_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            LABEL_STATES
        )
    )

    if selected_state not in LABEL_STATES:

        raise ValueError(
            f"Unknown labels state: "
            f"{selected_state}"
        )

    labels = [
        _label(
            index
        )
        for index in range(
            random.randint(
                8,
                14,
            )
        )
    ]

    selected_label = random.choice(
        labels
    )

    nested_labels = [
        label
        for label in labels
        if label["nested"]
    ]

    if (
        selected_state
        == "nested_labels"
        and
        not nested_labels
    ):

        labels[0]["nested"] = True
        labels[0]["parent"] = "Work"

    return {
        "state":
            selected_state,

        "title":
            "Labels",

        "labels":
            labels,

        "selected_label":
            selected_label,

        "show_selected":
            selected_state
            == "label_selected",

        "show_create":
            selected_state
            == "create_label",

        "show_edit":
            selected_state
            == "edit_label",

        "show_nested":
            selected_state
            == "nested_labels",

        "color_picker_open":
            selected_state
            == "color_picker_popup",

        "move_messages_open":
            selected_state
            == "move_messages_dialog",

        "delete_confirm_open":
            selected_state
            == "delete_label_confirm",

        "mobile_label_sheet_open":
            selected_state
            == "mobile_label_sheet",

        "colors":
            LABEL_COLORS,

        "form": {
            "name":
                (
                    selected_label["name"]
                    if selected_state
                    == "edit_label"
                    else fake.word().title()
                ),

            "parent":
                random.choice([
                    "",
                    "Work",
                    "Projects",
                    "Personal",
                ]),
        },

        "move_targets": [
            label["name"]
            for label in labels[:6]
        ],
    }