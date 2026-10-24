from __future__ import annotations

import random

from faker import Faker


fake = Faker()


MEET_STATES = [
    "prejoin",
    "call_grid",
    "presentation",
    "chat_open",
    "people_open",
    "settings_dialog",
    "leave_dialog",
]


AVATAR_COLORS = [
    "#1a73e8",
    "#ea4335",
    "#34a853",
    "#9334e6",
    "#fbbc04",
    "#00897b",
]


def get_initials(
    name: str,
) -> str:

    return "".join(
        word[0].upper()
        for word in name.split()[:2]
    )


def generate_person(
    index: int,
) -> dict:

    name = fake.name()

    return {
        "id":
            f"person_{index:03d}",

        "name":
            name,

        "email":
            fake.email(),

        "initials":
            get_initials(name),

        "color":
            random.choice(
                AVATAR_COLORS
            ),

        "muted":
            random.random() < 0.45,

        "presenting":
            False,
    }


def generate_chat_message(
    index: int,
    people: list[dict],
) -> dict:

    person = random.choice(people)

    return {
        "id":
            f"message_{index:03d}",

        "author":
            person["name"],

        "initials":
            person["initials"],

        "color":
            person["color"],

        "text":
            fake.sentence(
                nb_words=random.randint(5, 13),
            ),

        "time":
            random.choice(
                [
                    "10:02 AM",
                    "10:05 AM",
                    "10:11 AM",
                    "10:15 AM",
                ]
            ),
    }


def generate_meet_page(
    state: str | None = None,
) -> dict:

    state = (
        state
        or random.choice(
            MEET_STATES
        )
    )

    participants = [
        generate_person(index)
        for index in range(
            random.randint(4, 9)
        )
    ]

    participants[0]["name"] = "You"
    participants[0]["initials"] = "SK"
    participants[0]["muted"] = False

    presenter = random.choice(
        participants[1:]
    )

    presenter["presenting"] = True

    chat_messages = [
        generate_chat_message(
            index=index,
            people=participants[1:],
        )
        for index in range(
            random.randint(4, 8)
        )
    ]

    return {
        "app_name":
            "Google Meet",

        "state":
            state,

        "meeting_title":
            fake.sentence(
                nb_words=random.randint(3, 6),
            ).rstrip("."),

        "meeting_code":
            fake.bothify(
                text="???-????-???",
            ).lower(),

        "participants":
            participants,

        "presenter":
            presenter,

        "chat_messages":
            chat_messages,

        "participant_count":
            len(participants),

        "captions_enabled":
            random.random() < 0.35,

        "camera_enabled":
            state != "prejoin"
            or random.random() < 0.65,

        "microphone_enabled":
            random.random() < 0.70,
    }