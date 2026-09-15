from __future__ import annotations

import random

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_attachment_image,
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Compose States
# ==========================================================

COMPOSE_STATES = [
    "blank",
    "filled",
    "recipient_suggestions",
    "cc_bcc_expanded",
    "attachments",
    "schedule_menu",
    "discard_confirm",
    "draft_saved",
]


# ==========================================================
# Content Pools
# ==========================================================

SUBJECTS = [
    "Project follow-up",
    "Research update",
    "Meeting request",
    "Files for review",
    "Travel details",
    "Quick question",
    "Design feedback",
    "Weekly summary",
]

BODY_TEXTS = [
    "Hi,\n\nI wanted to follow up with a quick update. Please review the details below and let me know if anything should be changed.\n\nBest regards,",
    "Hello,\n\nI have attached the latest files for your review. Please let me know if you have any questions.\n\nThanks,",
    "Hi everyone,\n\nHere is a short summary of the items we discussed. I will share the remaining details once they are finalized.\n\nRegards,",
    "Hello,\n\nWould you be available for a short meeting this week? Please let me know which time works best.\n\nThank you,",
]

ATTACHMENT_NAMES = [
    "report.pdf",
    "notes.docx",
    "presentation.pptx",
    "invoice.pdf",
    "photo.jpg",
]


# ==========================================================
# Helpers
# ==========================================================

def _person() -> dict:

    name = fake.name()

    return {
        "name": name,
        "email": fake.email(),
        "avatar": get_random_avatar(),
    }


def _recipient_chip(
    index: int,
) -> dict:

    person = _person()

    return {
        "id": f"recipient_{index}",
        "name": person["name"],
        "email": person["email"],
        "avatar": person["avatar"],
    }


def _suggestion(
    index: int,
) -> dict:

    person = _person()

    return {
        "id": f"suggestion_{index}",
        "name": person["name"],
        "email": person["email"],
        "avatar": person["avatar"],
    }


def _attachment(
    index: int,
) -> dict:

    filename = random.choice(
        ATTACHMENT_NAMES
    )

    return {
        "id": f"compose_attachment_{index}",
        "name": filename,
        "size": f"{random.randint(90, 980)} KB",
        "preview": (
            get_random_attachment_image()
            if filename.endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                )
            )
            else None
        ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_compose_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            COMPOSE_STATES
        )
    )

    if selected_state not in COMPOSE_STATES:

        raise ValueError(
            f"Unknown compose state: {selected_state}. "
            f"Expected one of: {COMPOSE_STATES}"
        )

    filled = (
        selected_state
        != "blank"
    )

    recipient_count = (
        0
        if selected_state == "blank"
        else random.randint(
            1,
            3,
        )
    )

    recipients = [
        _recipient_chip(
            index
        )
        for index in range(
            recipient_count
        )
    ]

    attachment_count = (
        random.randint(
            1,
            3,
        )
        if selected_state
        == "attachments"
        else 0
    )

    return {

        "state":
            selected_state,

        "title":
            "New message",

        "from_account":
            _person(),

        "recipients":
            recipients,

        "cc":
            [
                _recipient_chip(100)
            ]
            if selected_state
            == "cc_bcc_expanded"
            else [],

        "bcc":
            [
                _recipient_chip(101)
            ]
            if selected_state
            == "cc_bcc_expanded"
            else [],

        "subject":
            random.choice(
                SUBJECTS
            )
            if filled
            else "",

        "body":
            random.choice(
                BODY_TEXTS
            )
            if filled
            else "",

        "suggestions":
            [
                _suggestion(index)
                for index in range(
                    random.randint(
                        4,
                        7,
                    )
                )
            ]
            if selected_state
            == "recipient_suggestions"
            else [],

        "attachments":
            [
                _attachment(index)
                for index in range(
                    attachment_count
                )
            ],

        "show_cc_bcc": (
            selected_state
            == "cc_bcc_expanded"
        ),

        "schedule_menu_open": (
            selected_state
            == "schedule_menu"
        ),

        "discard_confirm_open": (
            selected_state
            == "discard_confirm"
        ),

        "draft_saved": (
            selected_state
            == "draft_saved"
        ),

        "draft_time":
            random.choice([
                "Saved just now",
                "Saved 1 min ago",
                "Saved 3 min ago",
            ]),

        "schedule_options": [
            "Tomorrow morning",
            "Tomorrow afternoon",
            "Monday morning",
            "Pick date & time",
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_compose_data()

    print("\n==============================")
    print("EMAIL COMPOSE GENERATOR")
    print("==============================")

    print(
        "State:",
        data["state"],
    )

    print(
        "Recipients:",
        len(
            data["recipients"]
        ),
    )

    print(
        "Attachments:",
        len(
            data["attachments"]
        ),
    )
