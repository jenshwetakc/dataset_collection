from __future__ import annotations

import random

from faker import Faker

fake = Faker()

FORM_STATES = [
    "form_editor",
    "question_selected",
    "question_type_menu",
    "theme_customizer",
    "preview_mode",
    "responses_summary",
    "responses_individual",
    "share_dialog",
    "delete_question_dialog",
]

QUESTION_TYPES = [
    "Multiple choice",
    "Checkboxes",
    "Short answer",
    "Paragraph",
    "Linear scale",
]

ACCENTS = [
    "#673AB7",
    "#1A73E8",
    "#188038",
    "#E8710A",
    "#C5221F",
]


def make_question(index: int) -> dict:
    question_type = random.choice(QUESTION_TYPES)

    return {
        "id": f"question_{index}",
        "title": fake.sentence(
            nb_words=random.randint(4, 9),
        ).rstrip("."),
        "type": question_type,
        "required": random.random() < 0.45,
        "options": [
            fake.sentence(
                nb_words=random.randint(2, 5),
            ).rstrip(".")
            for _ in range(
                random.randint(3, 5),
            )
        ],
        "responses": [
            {
                "label": fake.word().title(),
                "value": random.randint(8, 72),
            }
            for _ in range(4)
        ],
    }


def generate_forms_data() -> dict:
    questions = [
        make_question(index)
        for index in range(
            random.randint(3, 6),
        )
    ]

    selected = random.choice(questions)
    state = random.choice(FORM_STATES)
    respondent_name = fake.name()

    return {
        "app_name": "Google Forms",
        "state": state,
        "form": {
            "title": fake.catch_phrase(),
            "description": fake.paragraph(
                nb_sentences=2,
            ),
            "accent": random.choice(ACCENTS),
            "responses_count": random.randint(12, 240),
        },
        "questions": questions,
        "selected_question": selected,
        "respondent": {
            "name": respondent_name,
            "email": fake.email(),
        },
        "share": {
            "email": fake.email(),
            "collect_emails": random.random() < 0.5,
        },
    }