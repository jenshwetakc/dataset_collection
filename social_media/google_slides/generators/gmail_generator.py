from __future__ import annotations

import random

from faker import Faker

fake = Faker()

GMAIL_STATES = [
    "inbox",
    "starred",
    "search_results",
    "email_open",
    "thread_open",
    "compose",
    "reply_composer",
    "label_menu_open",
    "attachment_preview",
    "delete_confirmation_dialog",
]

LABELS = [
    ("Work", "#4285F4"),
    ("Important", "#EA4335"),
    ("Travel", "#34A853"),
    ("Personal", "#A142F4"),
]

COLORS = [
    "#1A73E8",
    "#0F9D58",
    "#9334E6",
    "#E37400",
    "#D93025",
]


def initials(name: str) -> str:
    return "".join(
        word[0].upper()
        for word in name.split()[:2]
    ) or "U"


def generate_messages() -> list[dict]:
    messages = []

    for index in range(random.randint(12, 18)):
        sender = fake.name()
        subject = fake.sentence(
            nb_words=random.randint(3, 7),
        ).rstrip(".")
        unread = random.random() < 0.42

        messages.append(
            {
                "id": f"message_{index}",
                "sender": sender,
                "sender_initials": initials(sender),
                "sender_color": random.choice(COLORS),
                "email": fake.email(),
                "subject": subject,
                "preview": fake.sentence(
                    nb_words=random.randint(10, 18),
                ),
                "body": [
                    fake.paragraph(nb_sentences=3),
                    fake.paragraph(nb_sentences=2),
                ],
                "date": fake.date_between(
                    start_date="-50d",
                    end_date="today",
                ).strftime("%b %d"),
                "unread": unread,
                "starred": random.random() < 0.25,
                "important": random.random() < 0.27,
                "labels": random.sample(
                    LABELS,
                    k=random.randint(0, 2),
                ),
                "has_attachment": random.random() < 0.28,
                "attachment_name": fake.file_name(
                    extension=random.choice(
                        ["pdf", "png", "docx"]
                    )
                ),
                "thread_count": random.randint(1, 4),
            }
        )

    return messages


def generate_gmail_data(
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:
    del viewport

    state = state or random.choice(GMAIL_STATES)

    if state not in GMAIL_STATES:
        raise ValueError(
            f"Unsupported Gmail state: {state}"
        )

    messages = generate_messages()
    selected_message = random.choice(messages)

    return {
        "app_name": "Gmail",
        "state": state,
        "messages": messages,
        "selected_message": selected_message,
        "active_folder": (
            "Starred"
            if state == "starred"
            else "Inbox"
        ),
        "search": {
            "visible": state == "search_results",
            "query": random.choice(
                ["project update", "meeting", "report"]
            ),
        },
        "compose": {
            "visible": state == "compose",
            "recipient": fake.email(),
            "subject": fake.sentence(
                nb_words=5,
            ).rstrip("."),
            "body": fake.paragraph(
                nb_sentences=3,
            ),
        },
        "reply": {
            "visible": state == "reply_composer",
            "body": fake.paragraph(
                nb_sentences=2,
            ),
        },
        "label_menu": {
            "visible": state == "label_menu_open",
            "label_entries": LABELS,
        },
        "attachment_preview": {
            "visible": state == "attachment_preview",
        },
        "delete_dialog": {
            "visible": state == "delete_confirmation_dialog",
        },
    }