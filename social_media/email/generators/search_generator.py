from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Search States
# ==========================================================

SEARCH_STATES = [
    "results",
    "no_results",
    "suggestions",
    "advanced_filters",
    "attachment_only",
    "date_filtered",
    "mobile_filter_sheet",
]


# ==========================================================
# Pools
# ==========================================================

SEARCH_QUERIES = [
    "project update",
    "meeting",
    "invoice",
    "travel",
    "research",
    "attachment",
    "design review",
    "reservation",
]

SUBJECTS = [
    "Project update and next steps",
    "Meeting notes and action items",
    "Your invoice is ready",
    "Travel reservation details",
    "Research progress summary",
    "Design review feedback",
    "Attached files for review",
    "Weekly status update",
]

SNIPPETS = [
    "Here is the latest information and the files we discussed.",
    "Please review the attached document before our next meeting.",
    "Everything has been confirmed and no additional action is required.",
    "I have summarized the key points below for your reference.",
    "The requested update is complete. Let me know if anything should change.",
]

FILTER_LABELS = [
    "From",
    "To",
    "Has attachment",
    "Date",
    "Unread",
]


# ==========================================================
# Helpers
# ==========================================================

def _time_text() -> str:

    now = datetime.now()

    value = (
        now
        - timedelta(
            hours=random.randint(
                1,
                120,
            )
        )
    )

    if value.date() == now.date():
        return value.strftime(
            "%H:%M"
        )

    return value.strftime(
        "%b %d"
    )


def _result(
    index: int,
    force_attachment: bool = False,
) -> dict:

    sender = fake.name()

    has_attachment = (
        True
        if force_attachment
        else random.random() < 0.35
    )

    return {
        "id": f"search_result_{index}",
        "sender": sender,
        "email": fake.email(),
        "avatar": get_random_avatar(),
        "subject": random.choice(
            SUBJECTS
        ),
        "snippet": random.choice(
            SNIPPETS
        ),
        "time": _time_text(),
        "unread": (
            random.random()
            < 0.35
        ),
        "starred": (
            random.random()
            < 0.2
        ),
        "has_attachment": has_attachment,
        "label": random.choice([
            "Inbox",
            "Work",
            "Updates",
            "Travel",
        ]),
    }


def _suggestion(
    index: int,
) -> dict:

    return {
        "id": f"search_suggestion_{index}",
        "icon": random.choice([
            "history",
            "search",
            "person",
            "label",
        ]),
        "text": random.choice([
            "project update",
            "from:alex",
            "has:attachment",
            "label:work",
            "invoice",
            "meeting notes",
        ]),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_search_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            SEARCH_STATES
        )
    )

    if selected_state not in SEARCH_STATES:

        raise ValueError(
            f"Unknown search state: {selected_state}. "
            f"Expected one of: {SEARCH_STATES}"
        )

    query = random.choice(
        SEARCH_QUERIES
    )

    if selected_state == "no_results":

        results = []

    else:

        result_count = random.randint(
            8,
            18,
        )

        force_attachment = (
            selected_state
            == "attachment_only"
        )

        results = [
            _result(
                index=index,
                force_attachment=force_attachment,
            )
            for index in range(
                result_count
            )
        ]

    return {

        "state":
            selected_state,

        "query":
            query,

        "results":
            results,

        "result_count":
            len(
                results
            ),

        "suggestions":
            [
                _suggestion(
                    index
                )
                for index in range(
                    random.randint(
                        4,
                        7,
                    )
                )
            ]
            if selected_state
            == "suggestions"
            else [],

        "advanced_filters_open": (
            selected_state
            == "advanced_filters"
        ),

        "mobile_filter_sheet_open": (
            selected_state
            == "mobile_filter_sheet"
        ),

        "active_chips": (
            [
                "Has attachment"
            ]
            if selected_state
            == "attachment_only"
            else (
                [
                    "Last 7 days",
                    "Inbox",
                ]
                if selected_state
                == "date_filtered"
                else []
            )
        ),

        "filter_labels":
            FILTER_LABELS,

        "date_filter":
            random.choice([
                "Last 7 days",
                "Last 30 days",
                "This year",
            ]),

        "from_value":
            fake.email(),

        "to_value":
            fake.email(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_search_data()

    print("\n==============================")
    print("EMAIL SEARCH GENERATOR")
    print("==============================")

    print(
        "State:",
        data["state"],
    )

    print(
        "Query:",
        data["query"],
    )

    print(
        "Results:",
        data["result_count"],
    )
