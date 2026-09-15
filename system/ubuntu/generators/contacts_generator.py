from __future__ import annotations

import random

from faker import Faker

from system.ubuntu.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

CONTACTS_STATES = [

    "contact_list",

    "contact_selected",

    "favorites",

    "groups",

    "search_open",

    "search_results",

    "create_contact",

    "edit_contact",

    "contact_actions_menu",

    "import_contacts",

    "duplicate_warning",

    "delete_contact_dialog",
]


# ==========================================================
# Groups
# ==========================================================

GROUPS = [

    "All Contacts",

    "Favorites",

    "Family",

    "Friends",

    "Work",

    "University",
]


# ==========================================================
# Action Menu
# ==========================================================

CONTACT_ACTIONS = [

    {
        "label":
            "Edit Contact",

        "icon":
            "edit",
    },

    {
        "label":
            "Add to Favorites",

        "icon":
            "star",
    },

    {
        "label":
            "Share Contact",

        "icon":
            "share",
    },

    {
        "label":
            "Export",

        "icon":
            "download",
    },

    {
        "label":
            "Delete Contact",

        "icon":
            "delete",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_phone() -> str:

    return fake.phone_number()


def generate_contact(
    index: int,
) -> dict:

    name = fake.name()

    email = (
        name
        .lower()
        .replace(
            " ",
            ".",
        )
        + "@example.com"
    )


    return {

        "id":
            index,

        "name":
            name,

        "initial":
            name[
                0
            ].upper(),

        "avatar":
            get_random_avatar(),

        "phone":
            generate_phone(),

        "email":
            email,

        "company":
            random.choice(
                [
                    "",
                    "Open Source Lab",
                    "Design Studio",
                    "Research Group",
                    "University",
                    "Software Team",
                    "Creative Works",
                ]
            ),

        "job":
            random.choice(
                [
                    "",
                    "Software Engineer",
                    "Researcher",
                    "Designer",
                    "Professor",
                    "Student",
                    "Project Manager",
                ]
            ),

        "address":
            fake.address()
            .replace(
                "\n",
                ", ",
            ),

        "birthday":
            fake.date_of_birth(
                minimum_age=20,
                maximum_age=65,
            ).strftime(
                "%b %d, %Y"
            ),

        "favorite":
            random.random()
            < 0.25,

        "group":
            random.choice(
                GROUPS[
                    2:
                ]
            ),

        "selected":
            False,

        "notes":
            fake.sentence(
                nb_words=random.randint(
                    5,
                    12,
                )
            ),
    }


def generate_contacts(
    minimum: int = 12,
    maximum: int = 24,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    contacts = [

        generate_contact(
            index
        )

        for index in range(
            count
        )
    ]


    contacts.sort(
        key=lambda contact:
            contact[
                "name"
            ]
    )


    return contacts


# ==========================================================
# Import Entries
# ==========================================================

def generate_import_sources() -> list[dict]:

    return [

        {
            "label":
                "vCard File",

            "description":
                "Import contacts from a .vcf file",

            "icon":
                "contact_page",
        },

        {
            "label":
                "CSV File",

            "description":
                "Import names, email addresses, and phone numbers",

            "icon":
                "table_view",
        },

        {
            "label":
                "Online Account",

            "description":
                "Import from a connected online account",

            "icon":
                "cloud",
        },
    ]


# ==========================================================
# Main
# ==========================================================

def generate_contacts_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CONTACTS_STATES
        )


    if state not in CONTACTS_STATES:

        raise ValueError(
            f"Unknown Contacts state: "
            f"{state}"
        )


    contacts = generate_contacts()


    selected_contact = None


    if state in {
        "contact_selected",
        "edit_contact",
        "contact_actions_menu",
        "duplicate_warning",
        "delete_contact_dialog",
    }:

        selected_contact = random.choice(
            contacts
        )

        selected_contact[
            "selected"
        ] = True


    # ======================================================
    # Favorites
    # ======================================================

    favorite_contacts = [

        contact

        for contact
        in contacts

        if contact[
            "favorite"
        ]
    ]


    if len(
        favorite_contacts
    ) < 3:

        favorite_contacts = random.sample(
            contacts,
            k=min(
                4,
                len(
                    contacts
                ),
            ),
        )

        for contact in favorite_contacts:

            contact[
                "favorite"
            ] = True


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    search_results = []


    if state in {
        "search_open",
        "search_results",
    }:

        target = random.choice(
            contacts
        )

        search_query = (
            target[
                "name"
            ]
            .split()[0]
        )


    if state == "search_results":

        search_results = [

            contact

            for contact
            in contacts

            if search_query.lower()
            in contact[
                "name"
            ].lower()
        ]


        if not search_results:

            search_results = random.sample(
                contacts,
                k=min(
                    5,
                    len(
                        contacts
                    ),
                ),
            )


    # ======================================================
    # Group Counts
    # ======================================================

    group_entries = []

    for group_name in GROUPS:

        if group_name == "All Contacts":

            count = len(
                contacts
            )

        elif group_name == "Favorites":

            count = len(
                favorite_contacts
            )

        else:

            count = len(
                [
                    contact
                    for contact
                    in contacts
                    if contact[
                        "group"
                    ]
                    == group_name
                ]
            )


        group_entries.append(
            {
                "name":
                    group_name,

                "count":
                    count,

                "selected":
                    group_name
                    == (
                        "Favorites"
                        if state
                        == "favorites"
                        else "All Contacts"
                    ),
            }
        )


    # ======================================================
    # Form
    # ======================================================

    if state == "edit_contact" and selected_contact:

        form_contact = dict(
            selected_contact
        )

    else:

        name = fake.name()

        form_contact = {

            "name":
                name,

            "phone":
                generate_phone(),

            "email":
                (
                    name
                    .lower()
                    .replace(
                        " ",
                        ".",
                    )
                    + "@example.com"
                ),

            "company":
                fake.company(),

            "job":
                random.choice(
                    [
                        "Engineer",
                        "Researcher",
                        "Designer",
                    ]
                ),

            "address":
                fake.address()
                .replace(
                    "\n",
                    ", ",
                ),

            "notes":
                fake.sentence(
                    nb_words=9
                ),

            "avatar":
                get_random_avatar(),
        }


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "contacts":
            contacts,

        "favorite_contacts":
            favorite_contacts,

        "selected_contact":
            selected_contact,

        "group_entries":
            group_entries,

        "search_query":
            search_query,

        "search_results":
            search_results,

        "form_contact":
            form_contact,

        "action_entries":
            [
                dict(
                    entry
                )
                for entry
                in CONTACT_ACTIONS
            ],

        "import_entries":
            generate_import_sources(),
    }