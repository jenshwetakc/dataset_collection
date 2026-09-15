import random
import string

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_status():

    return random.choice(
        [
            "Available",
            "Busy",
            "At work",
            "At school",
            "Sleeping",
            "In a meeting",
            "Battery about to die",
            "Hey there! I am using WhatsApp.",
            "",
        ]
    )


def generate_contact():

    name = fake.name()

    return {
        "name":
            name,

        "avatar":
            get_random_avatar(),

        "status":
            generate_status(),

        "phone":
            fake.phone_number(),

        "is_business":
            random.random() < 0.08,

        "is_verified":
            random.random() < 0.05,

        "is_favorite":
            random.random() < 0.12,

        "first_letter":
            name[0].upper()
            if name
            else "#",
    }


# ==========================================================
# Action Rows
# ==========================================================

def generate_action_rows():

    actions = [
        {
            "id": "new_group",
            "title": "New group",
            "subtitle": None,
            "icon": "group_add",
        },
        {
            "id": "new_contact",
            "title": "New contact",
            "subtitle": None,
            "icon": "person_add",
        },
        {
            "id": "new_community",
            "title": "New community",
            "subtitle": None,
            "icon": "groups",
        },
    ]


    # Randomly keep 2–3 actions for more diversity.
    action_count = random.randint(
        2,
        len(actions),
    )

    return actions[:action_count]


# ==========================================================
# Contact Groups
# ==========================================================

def group_contacts(
    contacts,
):

    groups = {}

    for contact in contacts:

        letter = contact[
            "first_letter"
        ]

        groups.setdefault(
            letter,
            [],
        ).append(
            contact
        )


    grouped = []

    for letter in sorted(
        groups.keys()
    ):

        grouped.append(
            {
                "letter":
                    letter,

                "contacts":
                    sorted(
                        groups[letter],
                        key=lambda item:
                            item["name"],
                    ),
            }
        )

    return grouped


# ==========================================================
# Search State
# ==========================================================

def generate_search_state():

    active = (
        random.random()
        < 0.30
    )


    if not active:

        return {
            "active": False,
            "query": "",
        }


    query = random.choice(
        [
            fake.first_name(),
            fake.last_name(),
            random.choice(
                string.ascii_letters
            ),
        ]
    )


    return {
        "active":
            True,

        "query":
            query,
    }


# ==========================================================
# New Chat Page
# ==========================================================

def generate_new_chat_page(
    min_contacts=12,
    max_contacts=30,
):

    contact_count = (
        random.randint(
            min_contacts,
            max_contacts,
        )
    )


    contacts = [
        generate_contact()

        for _ in range(
            contact_count
        )
    ]


    contacts = sorted(
        contacts,
        key=lambda item:
            item["name"],
    )


    grouped_contacts = (
        group_contacts(
            contacts
        )
    )


    search = (
        generate_search_state()
    )


    # ------------------------------------------------------
    # Optional filtering when search is active
    # ------------------------------------------------------

    if (
        search["active"]
        and search["query"]
    ):

        query = (
            search["query"]
            .lower()
        )


        filtered_contacts = [

            contact

            for contact in contacts

            if query
            in contact[
                "name"
            ].lower()

        ]


        # If Faker happened to produce no match,
        # keep the full list so the page still has content.
        if filtered_contacts:

            visible_contacts = (
                filtered_contacts
            )

        else:

            visible_contacts = (
                contacts
            )

    else:

        visible_contacts = (
            contacts
        )


    visible_groups = (
        group_contacts(
            visible_contacts
        )
    )


    return {

        # --------------------------------------------------
        # Page
        # --------------------------------------------------

        "title":
            "New chat",

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "search":
            search,

        "search_placeholder":
            "Search name or number",

        # --------------------------------------------------
        # Actions
        # --------------------------------------------------

        "actions":
            generate_action_rows(),

        # --------------------------------------------------
        # Contacts
        # --------------------------------------------------

        "contacts":
            visible_contacts,

        "groups":
            visible_groups,

        "contact_count":
            len(
                visible_contacts
            ),

        "all_contact_count":
            len(
                contacts
            ),

        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        "show_refresh":
            random.random()
            < 0.30,

        "show_overflow":
            random.random()
            < 0.45,

        "show_alphabet_headers":
            True,

        "show_contact_count":
            random.random()
            < 0.75,
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_new_chat_page()
    )


    print(
        "\nNEW CHAT PAGE"
    )


    print(
        "Title:",
        page["title"]
    )


    print(
        "Search active:",
        page["search"]["active"]
    )


    print(
        "Search query:",
        page["search"]["query"]
    )


    print(
        "Actions:",
        len(
            page["actions"]
        )
    )


    print(
        "Contacts:",
        page["contact_count"]
    )


    print(
        "Groups:",
        len(
            page["groups"]
        )
    )


    print(
        "\nACTION ROWS"
    )


    for action in page[
        "actions"
    ]:

        print(
            "-",
            action["title"],
            "|",
            action["icon"],
        )


    print(
        "\nCONTACT GROUPS"
    )


    for group in page[
        "groups"
    ]:

        print(
            "\n",
            group["letter"],
        )


        for contact in group[
            "contacts"
        ][:3]:

            print(
                "  -",
                contact["name"],
                "|",
                contact["status"],
            )