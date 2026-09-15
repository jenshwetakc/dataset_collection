from __future__ import annotations

import random

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_attachment_image,
)


fake = Faker()


# ==========================================================
# Viewer States
# ==========================================================

ATTACHMENT_STATES = [
    "image_preview",
    "document_preview",
    "gallery",
    "details_open",
    "download_progress",
    "share_menu",
    "delete_confirm",
    "mobile_actions_sheet",
]


# ==========================================================
# Pools
# ==========================================================

FILE_NAMES = [
    "research-summary.pdf",
    "meeting-notes.docx",
    "design-review.pptx",
    "invoice-september.pdf",
    "project-photo.jpg",
    "diagram.png",
]

FILE_TYPES = [
    "PDF document",
    "Word document",
    "Presentation",
    "Image",
]


# ==========================================================
# Helpers
# ==========================================================

def _file(
    index: int,
) -> dict:

    name = random.choice(
        FILE_NAMES
    )

    is_image = name.endswith(
        (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        )
    )

    return {
        "id": f"attachment_{index}",
        "name": name,
        "type": (
            "Image"
            if is_image
            else random.choice(
                FILE_TYPES[:-1]
            )
        ),
        "size": f"{random.randint(120, 4200)} KB",
        "preview": (
            get_random_attachment_image()
            if is_image
            else None
        ),
        "uploaded_by": fake.name(),
        "modified": random.choice([
            "Today",
            "Yesterday",
            "Sep 3",
            "Aug 29",
        ]),
    }


def _document_lines() -> list[str]:

    return [
        fake.sentence(
            nb_words=random.randint(
                8,
                14,
            )
        )
        for _ in range(
            random.randint(
                10,
                18,
            )
        )
    ]


# ==========================================================
# Public Generator
# ==========================================================

def generate_attachment_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            ATTACHMENT_STATES
        )
    )

    if selected_state not in ATTACHMENT_STATES:

        raise ValueError(
            f"Unknown attachment state: {selected_state}. "
            f"Expected one of: {ATTACHMENT_STATES}"
        )

    files = [
        _file(index)
        for index in range(
            random.randint(
                5,
                9,
            )
        )
    ]

    if selected_state == "image_preview":

        image_files = [
            file
            for file in files
            if file["preview"]
        ]

        if image_files:
            selected_file = random.choice(
                image_files
            )
        else:
            selected_file = {
                "id": "attachment_image_fallback",
                "name": "project-photo.jpg",
                "type": "Image",
                "size": "860 KB",
                "preview": get_random_attachment_image(),
                "uploaded_by": fake.name(),
                "modified": "Today",
            }

    else:

        selected_file = random.choice(
            files
        )

    return {
        "state":
            selected_state,

        "title":
            "Attachment preview",

        "files":
            files,

        "selected_file":
            selected_file,

        "document_lines":
            _document_lines(),

        "show_gallery":
            selected_state
            == "gallery",

        "show_details":
            selected_state
            == "details_open",

        "download_progress":
            (
                random.randint(
                    18,
                    86,
                )
                if selected_state
                == "download_progress"
                else None
            ),

        "share_menu_open":
            selected_state
            == "share_menu",

        "delete_confirm_open":
            selected_state
            == "delete_confirm",

        "mobile_actions_sheet_open":
            selected_state
            == "mobile_actions_sheet",

        "sender":
            fake.name(),

        "message_subject":
            random.choice([
                "Files for review",
                "Project update",
                "Meeting attachments",
                "Invoice documents",
            ]),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_attachment_data()

    print(
        "State:",
        data["state"],
    )

    print(
        "Files:",
        len(
            data["files"]
        ),
    )
