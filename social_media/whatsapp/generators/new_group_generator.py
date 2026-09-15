import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Contact Generation
# ==========================================================

def generate_contact():

    name = fake.name()

    return {
        "name":
            name,

        "avatar":
            get_random_avatar(),

        "status":
            random.choice(
                [
                    "Available",
                    "Busy",
                    "At work",
                    "At school",
                    "In a meeting",
                    "Hey there! I am using WhatsApp.",
                    "",
                ]
            ),

        "phone":
            fake.phone_number(),

        "selected":
            False,

        "is_business":
            random.random() < 0.07,

        "is_verified":
            random.random() < 0.05,
    }


# ==========================================================
# Selected Members
# ==========================================================

def select_members(
    contacts,
):

    if not contacts:

        return []


    max_selected = min(
        len(contacts),
        random.randint(
            0,
            6,
        ),
    )


    if max_selected == 0:

        return []


    selected = random.sample(
        contacts,
        max_selected,
    )


    for contact in selected:

        contact["selected"] = True


    return selected


# ==========================================================
# Search State
# ==========================================================

def generate_search_state():

    active = (
        random.random()
        < 0.25
    )


    if not active:

        return {
            "active": False,
            "query": "",
        }


    return {
        "active":
            True,

        "query":
            random.choice(
                [
                    fake.first_name(),
                    fake.last_name(),
                    fake.word(),
                ]
            ),
    }


# ==========================================================
# Group Contact Alphabetically
# ==========================================================

def group_contacts(
    contacts,
):

    grouped = {}


    for contact in contacts:

        name = (
            contact["name"]
            or ""
        )


        letter = (
            name[0].upper()
            if name
            else "#"
        )


        grouped.setdefault(
            letter,
            [],
        ).append(
            contact
        )


    output = []


    for letter in sorted(
        grouped.keys()
    ):

        output.append(
            {
                "letter":
                    letter,

                "contacts":
                    sorted(
                        grouped[letter],
                        key=lambda item:
                            item["name"],
                    ),
            }
        )


    return output


# ==========================================================
# New Group Page
# ==========================================================

def generate_new_group_page(
    min_contacts=16,
    max_contacts=34,
):

    contact_count = random.randint(
        min_contacts,
        max_contacts,
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


    selected_members = (
        select_members(
            contacts
        )
    )


    search = (
        generate_search_state()
    )


    # ------------------------------------------------------
    # Search filtering
    # ------------------------------------------------------

    visible_contacts = contacts


    if (
        search["active"]
        and search["query"]
    ):

        query = (
            search["query"]
            .lower()
        )


        matches = [

            contact

            for contact in contacts

            if query
            in contact[
                "name"
            ].lower()

        ]


        if matches:

            visible_contacts = matches


    groups = (
        group_contacts(
            visible_contacts
        )
    )


    selected_count = (
        len(
            selected_members
        )
    )


    # ------------------------------------------------------
    # UI State
    # ------------------------------------------------------

    max_members = random.choice(
        [
            256,
            512,
            1024,
        ]
    )


    return {

        # --------------------------------------------------
        # Page
        # --------------------------------------------------

        "title":
            "New group",

        "subtitle":
            "Add participants",

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "search":
            search,

        "search_placeholder":
            "Search name or number",

        # --------------------------------------------------
        # Contacts
        # --------------------------------------------------

        "contacts":
            visible_contacts,

        "groups":
            groups,

        "contact_count":
            len(
                visible_contacts
            ),

        "all_contact_count":
            len(
                contacts
            ),

        # --------------------------------------------------
        # Selection
        # --------------------------------------------------

        "selected_members":
            selected_members,

        "selected_count":
            selected_count,

        "max_members":
            max_members,

        "can_continue":
            selected_count > 0,

        # --------------------------------------------------
        # UI variations
        # --------------------------------------------------

        "show_selected_strip":
            selected_count > 0,

        "show_member_limit":
            random.random()
            < 0.80,

        "show_alphabet_headers":
            True,

        "show_overflow":
            random.random()
            < 0.25,
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_new_group_page()
    )


    print(
        "\nNEW GROUP PAGE"
    )


    print(
        "Title:",
        page["title"]
    )


    print(
        "Contacts:",
        page["contact_count"]
    )


    print(
        "Selected:",
        page["selected_count"]
    )


    print(
        "Maximum:",
        page["max_members"]
    )


    print(
        "Can continue:",
        page["can_continue"]
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
        "\nSELECTED MEMBERS"
    )


    for member in page[
        "selected_members"
    ]:

        print(
            "-",
            member["name"]
        )


    print(
        "\nGROUPS"
    )


    for group in page[
        "groups"
    ]:

        print(
            group["letter"],
            ":",
            len(
                group["contacts"]
            ),
        )