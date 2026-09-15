import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Time
# ==========================================================

def generate_item_time():

    return random.choice(
        [
            fake.time(
                pattern="%H:%M"
            ),
            "Yesterday",
            "Monday",
            "Tuesday",
        ]
    )


# ==========================================================
# Message Text
# ==========================================================

def generate_message_text():

    message_type = random.choices(
        [
            "short",
            "medium",
        ],
        weights=[
            0.65,
            0.35,
        ],
        k=1,
    )[0]


    if message_type == "short":

        return fake.sentence(
            nb_words=random.randint(
                3,
                8,
            )
        )


    return fake.sentence(
        nb_words=random.randint(
            8,
            16,
        )
    )


# ==========================================================
# Announcement
# ==========================================================

def generate_announcement():

    unread = random.choices(
        [
            0,
            random.randint(1, 9),
            random.randint(10, 50),
        ],
        weights=[
            0.55,
            0.35,
            0.10,
        ],
        k=1,
    )[0]


    return {

        "name":
            "Announcements",

        "message":
            generate_message_text(),

        "time":
            generate_item_time(),

        "unread":
            unread,

        "muted":
            random.random() < 0.15,

        "thumbnail":
            (
                get_random_chat_image()
                if random.random() < 0.20
                else None
            ),
    }


# ==========================================================
# Community Group
# ==========================================================

def generate_group():

    unread = random.choices(
        [
            0,
            random.randint(1, 9),
            random.randint(10, 99),
        ],
        weights=[
            0.60,
            0.30,
            0.10,
        ],
        k=1,
    )[0]


    return {

        "name":
            fake.catch_phrase(),

        "avatar":
            get_random_avatar(),

        "message":
            generate_message_text(),

        "time":
            generate_item_time(),

        "unread":
            unread,

        "muted":
            random.random() < 0.25,

        "pinned":
            random.random() < 0.15,

        "thumbnail":
            (
                get_random_chat_image()
                if random.random() < 0.15
                else None
            ),
    }


# ==========================================================
# Community
# ==========================================================

def generate_community(
    min_groups: int = 2,
    max_groups: int = 5,
):

    group_count = random.randint(
        min_groups,
        max_groups,
    )


    groups = [

        generate_group()

        for _ in range(
            group_count
        )
    ]


    return {

        "name":
            fake.company(),

        "avatar":
            get_random_avatar(),

        "announcement":
            generate_announcement(),

        "groups":
            groups,

        "group_count":
            group_count,

        "show_view_all":
            group_count > 3,

        "description":
            (
                fake.sentence(
                    nb_words=random.randint(
                        5,
                        10,
                    )
                )
                if random.random() < 0.35
                else None
            ),
    }


# ==========================================================
# New Community Entry
# ==========================================================

def generate_new_community_entry():

    return {

        "title":
            "New community",

        "subtitle":
            "Create a community",

        "show":
            True,
    }


# ==========================================================
# Communities Page
# ==========================================================

def generate_communities_page(
    min_communities: int = 1,
    max_communities: int = 4,
):

    community_count = random.randint(
        min_communities,
        max_communities,
    )


    communities = [

        generate_community()

        for _ in range(
            community_count
        )
    ]


    return {

        "title":
            "Communities",

        "new_community":
            generate_new_community_entry(),

        "communities":
            communities,

        "community_count":
            community_count,

        "selected_navigation":
            "communities",

        "fab": {

            "show":
                True,

            "semantic":
                "new_community_button",
        },
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_communities_page()
    )


    print(
        "\nPAGE"
    )

    print(
        "Title:",
        page["title"]
    )

    print(
        "Community count:",
        page["community_count"]
    )


    for index, community in enumerate(
        page["communities"],
        start=1,
    ):

        print(
            f"\nCOMMUNITY {index}"
        )

        print(
            "Name:",
            community["name"]
        )

        print(
            "Avatar:",
            community["avatar"] is not None
        )

        print(
            "Description:",
            community["description"]
        )

        print(
            "Announcement:",
            community["announcement"]
        )

        print(
            "Groups:"
        )

        for group in community[
            "groups"
        ]:

            print(
                "   ",
                group
            )