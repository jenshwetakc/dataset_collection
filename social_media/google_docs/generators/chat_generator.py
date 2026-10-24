from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


CHAT_STATES = [
    "inbox",
    "direct_message",
    "space",
    "thread_open",
    "search_results",
    "new_message_dialog",
    "new_space_dialog",
]

SPACE_TOPICS = [
    "Product launch",
    "Design reviews",
    "Customer research",
    "Engineering updates",
    "Marketing planning",
    "Team operations",
]


def make_initials(name: str) -> str:
    return "".join(
        part[0].upper()
        for part in name.split()
        if part
    )[:2]


def generate_person(
    fake: Faker,
) -> dict:
    name = fake.name()

    return {
        "name": name,
        "email": fake.email(),
        "initials": make_initials(name),
        "color": fake.hex_color(),
        "online": random.random() < 0.62,
    }


def generate_message(
    fake: Faker,
    person: dict,
    minutes_ago: int,
    own_message: bool = False,
) -> dict:
    sent_at = datetime.now() - timedelta(
        minutes=minutes_ago,
    )

    return {
        "id": fake.uuid4(),
        "author": person,
        "text": fake.sentence(
            nb_words=random.randint(5, 17),
        ),
        "time": sent_at.strftime("%H:%M"),
        "own_message": own_message,
        "reaction_count": random.choice([0, 0, 0, 1, 2]),
        "has_attachment": random.random() < 0.16,
    }


def generate_chat_data(
    state: str | None = None,
    seed: int | None = None,
) -> dict:
    if state is not None and state not in CHAT_STATES:
        raise ValueError(
            f"Unknown chat state: {state}. "
            f"Expected one of: {CHAT_STATES}"
        )

    fake = Faker()

    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    state = state or random.choice(CHAT_STATES)

    current_user = generate_person(fake)
    people = [
        generate_person(fake)
        for _ in range(12)
    ]

    spaces = []

    for index in range(6):
        spaces.append(
            {
                "id": fake.uuid4(),
                "name": f"{random.choice(SPACE_TOPICS)} "
                f"{random.choice(['Hub', 'Space', 'Group'])}",
                "member_count": random.randint(4, 38),
                "unread_count": random.choice([0, 0, 1, 2, 4]),
                "color": fake.hex_color(),
            }
        )

    conversations = []

    for index, person in enumerate(people[:8]):
        conversations.append(
            {
                "id": fake.uuid4(),
                "person": person,
                "preview": fake.sentence(
                    nb_words=random.randint(4, 9),
                ),
                "time": (
                    f"{random.randint(8, 11)}:"
                    f"{random.randint(0, 59):02d}"
                ),
                "unread_count": random.choice([0, 0, 0, 1, 2]),
            }
        )

    active_person = random.choice(people)
    active_space = random.choice(spaces)

    messages = []

    for index in range(random.randint(8, 13)):
        author = (
            current_user
            if index % 4 == 3
            else random.choice(people[:5])
        )

        messages.append(
            generate_message(
                fake=fake,
                person=author,
                minutes_ago=(len(messages) + 1) * 12,
                own_message=(
                    author["email"]
                    == current_user["email"]
                ),
            )
        )

    search_results = [
        {
            "id": fake.uuid4(),
            "person": random.choice(people),
            "text": fake.sentence(
                nb_words=random.randint(8, 18),
            ),
            "space_name": random.choice(spaces)["name"],
            "date": fake.date_this_year().strftime(
                "%b %d",
            ),
        }
        for _ in range(6)
    ]

    thread_root = random.choice(messages)

    thread_replies = [
        generate_message(
            fake=fake,
            person=random.choice(people[:5]),
            minutes_ago=random.randint(5, 120),
        )
        for _ in range(random.randint(3, 6))
    ]

    return {
        "state": state,
        "current_user": current_user,
        "conversations": conversations,
        "spaces": spaces,
        "active_person": active_person,
        "active_space": active_space,
        "messages": messages,
        "thread_root": thread_root,
        "thread_replies": thread_replies,
        "search_query": fake.word(),
        "search_results": search_results,
        "compose_text": (
            fake.sentence(nb_words=7)
            if state == "new_message_dialog"
            else ""
        ),
    }