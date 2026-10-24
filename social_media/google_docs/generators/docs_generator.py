from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


DOCS_STATES = [
    "editing",
    "text_selected",
    "comments_open",
    "outline_open",
    "share_dialog",
    "find_replace",
    "version_history",
]

DOCUMENT_TYPES = [
    "Project proposal",
    "Weekly meeting notes",
    "Research outline",
    "Product requirements",
    "Course assignment",
    "Team retrospective",
]


def generate_paragraph(
    fake: Faker,
) -> str:

    sentences = [
        fake.sentence(
            nb_words=random.randint(8, 16)
        )
        for _ in range(
            random.randint(2, 4)
        )
    ]

    return " ".join(sentences)


def generate_collaborators(
    fake: Faker,
) -> list[dict]:

    colors = [
        "#1a73e8",
        "#188038",
        "#9334e6",
        "#c5221f",
        "#e37400",
    ]

    collaborators = []

    for index in range(
        random.randint(2, 5)
    ):

        name = fake.name()

        collaborators.append(
            {
                "name": name,
                "initials": "".join(
                    part[0]
                    for part in name.split()[:2]
                ).upper(),
                "color": colors[
                    index % len(colors)
                ],
            }
        )

    return collaborators


def generate_sections(
    fake: Faker,
) -> list[dict]:

    heading_pool = [
        "Overview",
        "Goals and scope",
        "Key findings",
        "Implementation plan",
        "Open questions",
        "Next steps",
    ]

    random.shuffle(heading_pool)

    sections = []

    for index, heading in enumerate(
        heading_pool[
            :random.randint(3, 5)
        ]
    ):

        sections.append(
            {
                "id": f"section_{index}",
                "heading": heading,
                "level": (
                    1
                    if index == 0
                    else random.choice([1, 2])
                ),
                "paragraphs": [
                    generate_paragraph(fake)
                    for _ in range(
                        random.randint(1, 3)
                    )
                ],
            }
        )

    return sections


def generate_comments(
    fake: Faker,
    collaborators: list[dict],
) -> list[dict]:

    comments = []

    for index in range(
        random.randint(2, 4)
    ):

        collaborator = random.choice(
            collaborators
        )

        comments.append(
            {
                "id": f"comment_{index}",
                "author": collaborator["name"],
                "initials": collaborator["initials"],
                "color": collaborator["color"],
                "message": fake.sentence(
                    nb_words=random.randint(8, 15)
                ),
                "time": random.choice(
                    [
                        "Just now",
                        "8 min ago",
                        "Yesterday",
                    ]
                ),
                "resolved": random.random() < 0.2,
            }
        )

    return comments


def generate_docs_page(
    state: str | None = None,
    seed: int | None = None,
) -> dict:
    """
    Generate one Google Docs-style page.

    Available states:
    - editing
    - text_selected
    - comments_open
    - outline_open
    - share_dialog
    - find_replace
    - version_history
    """

    if state is None:
        state = random.choice(
            DOCS_STATES
        )

    if state not in DOCS_STATES:
        raise ValueError(
            f"Unknown Docs state: {state}. "
            f"Available states: {DOCS_STATES}"
        )

    page_seed = (
        seed
        if seed is not None
        else random.randint(0, 2**31 - 1)
    )

    random.seed(page_seed)

    fake = Faker()
    fake.seed_instance(page_seed)

    collaborators = generate_collaborators(
        fake
    )

    sections = generate_sections(
        fake
    )

    first_paragraph = (
        sections[0]["paragraphs"][0]
    )

    selected_words = first_paragraph.split()

    selected_text = " ".join(
        selected_words[3:12]
    )

    edited_at = (
        datetime.now()
        - timedelta(
            minutes=random.randint(1, 180)
        )
    )

    return {
        "state": state,
        "seed": page_seed,
        "document": {
            "title": (
                f"{random.choice(DOCUMENT_TYPES)} "
                f"— {fake.company()}"
            ),
            "folder_name": random.choice(
                [
                    "My Drive",
                    "Work",
                    "Shared with me",
                ]
            ),
            "last_edited": edited_at.strftime(
                "%I:%M %p"
            ).lstrip("0"),
            "page_count": random.randint(2, 8),
            "word_count": random.randint(
                540,
                2400,
            ),
            "sections": sections,
            "selected_text": selected_text,
        },
        "toolbar": {
            "font": random.choice(
                [
                    "Arial",
                    "Roboto",
                    "Times New Roman",
                    "Georgia",
                ]
            ),
            "font_size": random.choice(
                [10, 11, 12, 14]
            ),
            "zoom": random.choice(
                ["90%", "100%", "110%"]
            ),
        },
        "collaborators": collaborators,
        "comments": generate_comments(
            fake,
            collaborators,
        ),
        "outline": [
            {
                "title": section["heading"],
                "level": section["level"],
            }
            for section in sections
        ],
        "find_replace": {
            "find_text": random.choice(
                [
                    "project",
                    "research",
                    "plan",
                    "team",
                ]
            ),
            "replace_text": random.choice(
                [
                    "proposal",
                    "study",
                    "roadmap",
                    "group",
                ]
            ),
            "matches": random.randint(1, 6),
        },
        "share": {
            "general_access": random.choice(
                [
                    "Restricted",
                    "Anyone with the link",
                ]
            ),
            "role": random.choice(
                [
                    "Viewer",
                    "Commenter",
                    "Editor",
                ]
            ),
        },
        "version_history": [
            {
                "label": "Current version",
                "time": "Just now",
            },
            {
                "label": (
                    f"Edited by "
                    f"{collaborators[0]['name']}"
                ),
                "time": "Today",
            },
            {
                "label": (
                    "Version from yesterday"
                ),
                "time": "Yesterday",
            },
        ],
    }