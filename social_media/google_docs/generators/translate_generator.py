from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


TRANSLATE_STATES = [
    "empty",
    "translated",
    "language_menu",
    "history",
    "saved",
    "camera_sheet",
    "voice_sheet",
]

LANGUAGES = [
    "English",
    "Korean",
    "Japanese",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Chinese",
    "Hindi",
]


def generate_translation(
    fake: Faker,
    source_language: str,
    target_language: str,
) -> dict:
    source_text = fake.sentence(
        nb_words=random.randint(5, 15),
    )

    target_words = [
        fake.word().capitalize()
        for _ in range(
            random.randint(5, 13)
        )
    ]

    return {
        "id": fake.uuid4(),
        "source_language": source_language,
        "target_language": target_language,
        "source_text": source_text,
        "translated_text": " ".join(target_words) + ".",
        "source_pronunciation": fake.sentence(
            nb_words=random.randint(3, 7),
        ),
        "target_pronunciation": fake.sentence(
            nb_words=random.randint(3, 7),
        ),
        "saved": random.random() < 0.42,
    }


def generate_history_items(
    fake: Faker,
    count: int,
) -> list[dict]:
    items = []

    for index in range(count):
        source_language, target_language = random.sample(
            LANGUAGES,
            k=2,
        )

        translation = generate_translation(
            fake=fake,
            source_language=source_language,
            target_language=target_language,
        )

        created_at = datetime.now() - timedelta(
            hours=random.randint(1, 120),
        )

        translation["date_label"] = created_at.strftime(
            "%b %d",
        )

        items.append(translation)

    return items


def generate_translate_data(
    state: str | None = None,
    seed: int | None = None,
) -> dict:
    if state is not None and state not in TRANSLATE_STATES:
        raise ValueError(
            f"Unknown translate state: {state}. "
            f"Expected one of: {TRANSLATE_STATES}"
        )

    fake = Faker()

    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    state = state or random.choice(
        TRANSLATE_STATES,
    )

    source_language, target_language = random.sample(
        LANGUAGES,
        k=2,
    )

    current_translation = generate_translation(
        fake=fake,
        source_language=source_language,
        target_language=target_language,
    )

    if state == "empty":
        current_translation["source_text"] = ""
        current_translation["translated_text"] = ""
        current_translation["source_pronunciation"] = ""
        current_translation["target_pronunciation"] = ""

    history_items = generate_history_items(
        fake=fake,
        count=random.randint(6, 10),
    )

    saved_items = [
        item
        for item in history_items
        if item["saved"]
    ]

    if not saved_items:
        saved_items = history_items[:3]

    return {
        "state": state,
        "source_language": source_language,
        "target_language": target_language,
        "languages": LANGUAGES,
        "translation": current_translation,
        "history_items": history_items,
        "saved_items": saved_items,
        "detected_language": random.choice(LANGUAGES),
        "voice_text": fake.sentence(
            nb_words=random.randint(4, 10),
        ),
    }