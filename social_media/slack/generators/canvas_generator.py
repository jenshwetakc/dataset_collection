# social_media/slack/generators/canvas_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_attachment,
    get_random_avatar,
    get_random_emoji,
    get_random_workspace_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

WORKSPACE_NAMES = [
    "Acme Studio",
    "Northstar",
    "Orbit Labs",
    "Pixel Works",
    "Nova Research",
    "Mosaic",
    "Vertex",
    "Nimbus",
]


CANVAS_TITLES = [
    "Project launch plan",
    "Dataset annotation guide",
    "Research notes",
    "Design review",
    "Release checklist",
    "Team planning",
    "Experiment overview",
]


SECTION_TITLES = [
    "Overview",
    "Goals",
    "Implementation",
    "Milestones",
    "Open questions",
    "Next steps",
]


TASK_TEXTS = [
    "Review the latest implementation",
    "Validate mobile layouts",
    "Check annotation quality",
    "Update documentation",
    "Run accessibility checks",
    "Prepare release notes",
    "Compare light and dark themes",
]


COMMENT_TEXTS = [
    "Could we clarify this section?",
    "This looks good to me.",
    "I added another example here.",
    "Can we verify this on mobile too?",
    "I think this should be moved earlier.",
    "Let's keep this consistent with the other screens.",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_person(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "online":
            random.random() < 0.75,
    }


def generate_task(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "text":
            random.choice(
                TASK_TEXTS
            ),

        "completed":
            random.random() < 0.45,
    }


def generate_comment(
    people: list[dict],
    index: int,
) -> dict:

    reaction = None

    if random.random() < 0.35:

        reaction = (
            get_random_emoji()
        )

    return {
        "id":
            index,

        "author":
            random.choice(
                people
            ),

        "text":
            random.choice(
                COMMENT_TEXTS
            ),

        "time":
            random.choice(
                [
                    "9:14 AM",
                    "10:32 AM",
                    "11:08 AM",
                    "1:46 PM",
                    "3:21 PM",
                ]
            ),

        "reaction":
            reaction,
    }


# ==========================================================
# Main
# ==========================================================

def generate_canvas_data() -> dict:

    people = [
        generate_person(
            index=index
        )
        for index in range(
            random.randint(
                8,
                14,
            )
        )
    ]

    collaborators = random.sample(
        people,
        k=random.randint(
            3,
            6,
        ),
    )

    comments = [
        generate_comment(
            people=people,
            index=index,
        )
        for index in range(
            random.randint(
                5,
                9,
            )
        )
    ]

    tasks = [
        generate_task(
            index=index
        )
        for index in range(
            random.randint(
                5,
                8,
            )
        )
    ]

    workspace_name = random.choice(
        WORKSPACE_NAMES
    )

    return {

        "workspace": {
            "name":
                workspace_name,

            "image":
                get_random_workspace_image(),
        },

        "title":
            random.choice(
                CANVAS_TITLES
            ),

        "subtitle":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    12,
                )
            ),

        "section_title":
            random.choice(
                SECTION_TITLES
            ),

        "paragraphs": [
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            )
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],

        "tasks":
            tasks,

        "collaborators":
            collaborators,

        "comments":
            comments,

        "attachment":
            (
                get_random_attachment()
                if random.random() < 0.7
                else None
            ),

        "updated_text":
            random.choice(
                [
                    "Updated 3 minutes ago",
                    "Updated 12 minutes ago",
                    "Updated today",
                    "Updated yesterday",
                ]
            ),

        "comment_count":
            len(
                comments
            ),

        "panel_mode":
            random.choice(
                [
                    "comments",
                    "details",
                ]
            ),

        "toolbar_items": [
            "format_bold",
            "format_italic",
            "link",
            "format_list_bulleted",
            "checklist",
            "code",
            "image",
        ],
    }


if __name__ == "__main__":

    data = generate_canvas_data()

    print(
        "Canvas:",
        data["title"]
    )

    print(
        "Tasks:",
        len(
            data["tasks"]
        )
    )

    print(
        "Comments:",
        data["comment_count"]
    )