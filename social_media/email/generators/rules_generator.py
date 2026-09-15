from __future__ import annotations

import random

from faker import Faker


fake = Faker()


RULE_STATES = [
    "rules_list",
    "rule_selected",
    "create_rule",
    "edit_rule",
    "condition_builder",
    "action_builder",
    "rule_test_results",
    "delete_rule_confirm",
    "mobile_rule_sheet",
]


CONDITION_FIELDS = [
    "From",
    "To",
    "Subject",
    "Has words",
    "Doesn't have",
    "Has attachment",
]


ACTION_TYPES = [
    "Apply label",
    "Mark as read",
    "Star message",
    "Forward to",
    "Archive",
    "Delete",
]


def _rule(
    index: int,
) -> dict:

    enabled = (
        random.random()
        < 0.75
    )

    condition_count = random.randint(
        1,
        3,
    )

    action_count = random.randint(
        1,
        3,
    )

    conditions = [
        {
            "field":
                random.choice(
                    CONDITION_FIELDS
                ),

            "value":
                random.choice([
                    fake.email(),
                    "invoice",
                    "project",
                    "newsletter",
                    "meeting",
                    "attachment",
                ]),
        }
        for _ in range(
            condition_count
        )
    ]

    actions = [
        {
            "type":
                random.choice(
                    ACTION_TYPES
                ),

            "value":
                random.choice([
                    "Work",
                    "Important",
                    "Archive",
                    fake.email(),
                    "",
                ]),
        }
        for _ in range(
            action_count
        )
    ]

    return {
        "id":
            f"rule_{index}",

        "name":
            random.choice([
                "Work emails",
                "Invoices",
                "Newsletters",
                "Project updates",
                "Meeting invites",
                "Receipts",
            ]),

        "enabled":
            enabled,

        "conditions":
            conditions,

        "actions":
            actions,

        "match_count":
            random.randint(
                3,
                320,
            ),
    }


def generate_rules_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            RULE_STATES
        )
    )

    if selected_state not in RULE_STATES:

        raise ValueError(
            f"Unknown rule state: "
            f"{selected_state}"
        )

    rules = [
        _rule(index)
        for index in range(
            random.randint(
                6,
                12,
            )
        )
    ]

    selected_rule = random.choice(
        rules
    )

    return {
        "state":
            selected_state,

        "title":
            "Mail rules",

        "rules":
            rules,

        "selected_rule":
            selected_rule,

        "show_selected":
            selected_state
            == "rule_selected",

        "show_create":
            selected_state
            == "create_rule",

        "show_edit":
            selected_state
            == "edit_rule",

        "condition_builder_open":
            selected_state
            == "condition_builder",

        "action_builder_open":
            selected_state
            == "action_builder",

        "test_results_open":
            selected_state
            == "rule_test_results",

        "delete_confirm_open":
            selected_state
            == "delete_rule_confirm",

        "mobile_rule_sheet_open":
            selected_state
            == "mobile_rule_sheet",

        "condition_fields":
            CONDITION_FIELDS,

        "action_types":
            ACTION_TYPES,

        "test_matches": [
            {
                "sender":
                    fake.name(),

                "subject":
                    fake.sentence(
                        nb_words=5
                    ),

                "time":
                    random.choice([
                        "09:42",
                        "Yesterday",
                        "Sep 2",
                    ]),
            }
            for _ in range(
                random.randint(
                    3,
                    6,
                )
            )
        ],
    }