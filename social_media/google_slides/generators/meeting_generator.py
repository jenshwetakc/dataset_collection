from __future__ import annotations

import random

from faker import Faker


fake = Faker()

MEETING_STATES = [
    "pre_join",
    "in_meeting",
    "screen_sharing",
    "chat_open",
    "people_open",
    "settings_open",
    "leave_dialog",
    "presentation_fullscreen",
]

ACCENT_COLORS = [
    "#1A73E8",
    "#9334E6",
    "#E8710A",
    "#188038",
    "#C5221F",
]

TOPICS = [
    "Weekly product review",
    "Design sync",
    "Research planning",
    "Mobile release review",
    "Project kickoff",
]

CHAT_MESSAGES = [
    "Thanks everyone. I have added the notes to the document.",
    "The prototype is ready for review.",
    "Could we revisit the timeline on the next call?",
    "I will share the updated design after the meeting.",
    "That approach sounds good to me.",
]


def make_person(
    index: int,
    host: bool = False,
) -> dict:
    name = fake.name()

    return {
        "id": f"person_{index}",
        "name": name,
        "initials": "".join(
            part[0].upper()
            for part in name.split()[:2]
        ),
        "color": random.choice(ACCENT_COLORS),
        "host": host,
        "muted": random.random() < 0.58,
        "camera_off": random.random() < 0.28,
        "raised_hand": random.random() < 0.15,
        "speaking": random.random() < 0.18,
    }


def make_chat_message(
    people: list[dict],
) -> dict:
    sender = random.choice(people)

    return {
        "sender": sender["name"],
        "initials": sender["initials"],
        "color": sender["color"],
        "time": (
            f"{random.randint(9, 11)}:"
            f"{random.randint(0, 59):02d}"
        ),
        "text": random.choice(CHAT_MESSAGES),
    }


def generate_meeting_data() -> dict:
    state = random.choice(MEETING_STATES)

    people = [
        make_person(
            index=0,
            host=True,
        ),
    ]

    for index in range(
        random.randint(3, 8),
    ):
        people.append(
            make_person(index + 1),
        )

    current_user = {
        "name": "Shweta KC",
        "initials": "SK",
        "color": "#9334E6",
        "muted": random.random() < 0.35,
        "camera_off": random.random() < 0.25,
    }

    presentation_title = random.choice(
        [
            "Q4 product strategy",
            "Interface research findings",
            "Mobile app design proposal",
            "Launch planning overview",
        ]
    )

    return {
        "app_name": "Google Meet",
        "state": state,
        "meeting": {
            "title": random.choice(TOPICS),
            "code": (
                f"{fake.lexify('???')}-"
                f"{fake.lexify('????')}-"
                f"{fake.lexify('???')}"
            ),
            "duration": (
                f"{random.randint(5, 58)}:"
                f"{random.randint(0, 59):02d}"
            ),
        },
        "current_user": current_user,
        "people": people,
        "chat_messages": [
            make_chat_message(people)
            for _ in range(
                random.randint(3, 6),
            )
        ],
        "chat_draft": fake.sentence(
            nb_words=7,
        ),
        "presentation": {
            "title": presentation_title,
            "subtitle": fake.catch_phrase(),
            "accent": random.choice(ACCENT_COLORS),
            "image_src": None,
            "slide_number": random.randint(2, 8),
            "total_slides": random.randint(10, 18),
        },
        "pre_join": {
            "camera_enabled": random.random() < 0.7,
            "microphone_enabled": random.random() < 0.75,
            "background_effect": random.choice(
                [
                    "None",
                    "Blur",
                    "Office",
                    "Abstract",
                ]
            ),
        },
        "captions_enabled": random.random() < 0.4,
        "recording": random.random() < 0.12,
        "settings": {
            "camera": "FaceTime HD Camera",
            "microphone": "MacBook Pro Microphone",
            "speaker": "MacBook Pro Speakers",
            "noise_cancellation": random.random() < 0.6,
        },
    }