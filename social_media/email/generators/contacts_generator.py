from __future__ import annotations

import random

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Contacts States
# ==========================================================

CONTACT_STATES = [
    "list",
    "selected",
    "favorites",
    "grouped",
    "search_results",
    "add_contact",
    "edit_contact",
    "delete_confirm",
    "mobile_details_sheet",
]


# ==========================================================
# Helpers
# ==========================================================

def _contact(
    index: int,
) -> dict:

    name = fake.name()

    return {
        "id": f"contact_{index}",
        "name": name,
        "email": fake.email(),
        "phone": fake.phone_number(),
        "company": fake.company(),
        "role": fake.job(),
        "avatar": get_random_avatar(),
        "favorite": random.random() < 0.25,
        "group": random.choice([
            "Work",
            "Family",
            "Friends",
            "Other",
        ]),
        "notes": fake.sentence(
            nb_words=random.randint(
                6,
                12,
            )
        ),
    }


def _form_contact() -> dict:

    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "company": fake.company(),
        "role": fake.job(),
        "notes": fake.sentence(
            nb_words=10
        ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_contacts_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            CONTACT_STATES
        )
    )

    if selected_state not in CONTACT_STATES:

        raise ValueError(
            f"Unknown contacts state: {selected_state}. "
            f"Expected one of: {CONTACT_STATES}"
        )

    contacts = [
        _contact(index)
        for index in range(
            random.randint(
                12,
                22,
            )
        )
    ]

    if selected_state == "favorites":

        filtered_contacts = [
            contact
            for contact in contacts
            if contact["favorite"]
        ]

        if not filtered_contacts:
            contacts[0]["favorite"] = True
            filtered_contacts = [
                contacts[0]
            ]

    elif selected_state == "search_results":

        filtered_contacts = contacts[
            :random.randint(
                3,
                7,
            )
        ]

    else:

        filtered_contacts = contacts

    selected_contact = (
        random.choice(
            filtered_contacts
        )
        if filtered_contacts
        else None
    )

    grouped_contacts = {}

    for contact in filtered_contacts:

        grouped_contacts.setdefault(
            contact["group"],
            [],
        ).append(
            contact
        )

    return {
        "state":
            selected_state,

        "title":
            "Contacts",

        "contacts":
            filtered_contacts,

        "all_contacts":
            contacts,

        "selected_contact":
            selected_contact,

        "groups":
            grouped_contacts,

        "search_query":
            (
                random.choice([
                    "alex",
                    "kim",
                    "design",
                    "research",
                    "company",
                ])
                if selected_state
                == "search_results"
                else ""
            ),

        "show_selected":
            selected_state
            in {
                "selected",
                "edit_contact",
                "delete_confirm",
                "mobile_details_sheet",
            },

        "show_add_contact":
            selected_state
            == "add_contact",

        "show_edit_contact":
            selected_state
            == "edit_contact",

        "show_delete_confirm":
            selected_state
            == "delete_confirm",

        "show_mobile_details_sheet":
            selected_state
            == "mobile_details_sheet",

        "form":
            (
                dict(
                    selected_contact
                )
                if (
                    selected_state
                    == "edit_contact"
                    and selected_contact
                    is not None
                )
                else _form_contact()
            ),

        "tabs": [
            "All",
            "Favorites",
            "Groups",
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_contacts_data()

    print("\n==============================")
    print("EMAIL CONTACTS GENERATOR")
    print("==============================")

    print(
        "State:",
        data["state"],
    )

    print(
        "Contacts:",
        len(
            data["contacts"]
        ),
    )
