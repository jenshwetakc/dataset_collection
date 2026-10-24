from __future__ import annotations

import random

from faker import Faker


CONTACT_STATES = [
    "contacts_list",
    "contact_detail",
    "search_results",
    "label_contacts",
    "edit_contact_dialog",
    "create_contact_dialog",
    "merge_suggestions",
]

LABEL_NAMES = [
    "Friends",
    "Work",
    "Family",
    "Project team",
]


def get_initials(name: str) -> str:
    return "".join(
        word[0].upper()
        for word in name.split()
        if word
    )[:2]


def generate_contact(fake: Faker) -> dict:
    name = fake.name()

    return {
        "id": fake.uuid4(),
        "name": name,
        "initials": get_initials(name),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "company": fake.company(),
        "job_title": fake.job(),
        "address": fake.address().replace("\n", ", "),
        "note": fake.sentence(
            nb_words=random.randint(7, 16),
        ),
        "color": fake.hex_color(),
        "label": random.choice(LABEL_NAMES),
        "starred": random.random() < 0.28,
    }


def generate_contacts_data(
    state: str | None = None,
    seed: int | None = None,
) -> dict:
    if state is not None and state not in CONTACT_STATES:
        raise ValueError(
            f"Unknown contacts state: {state}. "
            f"Expected one of: {CONTACT_STATES}"
        )

    fake = Faker()

    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    state = state or random.choice(
        CONTACT_STATES,
    )

    contacts = sorted(
        [
            generate_contact(fake)
            for _ in range(
                random.randint(13, 20)
            )
        ],
        key=lambda contact: contact["name"],
    )

    selected_contact = random.choice(
        contacts,
    )

    query = fake.first_name()

    search_contacts = [
        contact
        for contact in contacts
        if query[0].lower()
        in contact["name"].lower()
    ]

    if len(search_contacts) < 3:
        search_contacts = contacts[:5]

    selected_label = random.choice(
        LABEL_NAMES,
    )

    label_contacts = [
        contact
        for contact in contacts
        if contact["label"] == selected_label
    ]

    if not label_contacts:
        label_contacts = contacts[:4]

    merge_pair = random.sample(
        contacts,
        k=2,
    )

    return {
        "state": state,
        "contacts": contacts,
        "selected_contact": selected_contact,
        "search_query": query,
        "search_contacts": search_contacts,
        "labels": LABEL_NAMES,
        "selected_label": selected_label,
        "label_contacts": label_contacts,
        "merge_pair": merge_pair,
        "new_contact": generate_contact(fake),
    }