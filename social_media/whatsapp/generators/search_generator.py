import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_search_time():

    return random.choice(
        [
            fake.time(
                pattern="%H:%M"
            ),
            "Yesterday",
            "Monday",
            "Tuesday",
            "Friday",
        ]
    )


def generate_short_message():

    return fake.sentence(
        nb_words=random.randint(
            4,
            10,
        )
    )


def generate_query():

    query_type = random.choice(
        [
            "name",
            "word",
            "topic",
        ]
    )


    if query_type == "name":

        return fake.first_name()


    if query_type == "topic":

        return random.choice(
            [
                "project",
                "meeting",
                "research",
                "conference",
                "report",
                "photos",
                "travel",
                "study",
                "assignment",
                "presentation",
            ]
        )


    return fake.word()


# ==========================================================
# Recent Search
# ==========================================================

def generate_recent_search():

    return {

        "query":
            random.choice(
                [
                    fake.first_name(),
                    fake.word(),
                    "project",
                    "meeting",
                    "research",
                    "photos",
                    "report",
                ]
            ),
    }


# ==========================================================
# Person Result
# ==========================================================

def generate_person_result():

    subtitle_type = random.choice(
        [
            "status",
            "phone",
            "none",
        ]
    )


    if subtitle_type == "status":

        subtitle = random.choice(
            [
                "Available",
                "Busy",
                "At work",
                "Hey there! I am using WhatsApp.",
            ]
        )

    elif subtitle_type == "phone":

        subtitle = fake.phone_number()

    else:

        subtitle = None


    return {

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "subtitle":
            subtitle,

        "verified":
            random.random() < 0.08,
    }


# ==========================================================
# Chat Result
# ==========================================================

def generate_chat_result():

    unread = random.choices(
        [
            0,
            random.randint(1, 9),
            random.randint(10, 40),
        ],
        weights=[
            0.65,
            0.28,
            0.07,
        ],
        k=1,
    )[0]


    return {

        "name":
            random.choice(
                [
                    fake.name(),
                    fake.company(),
                    fake.catch_phrase(),
                ]
            ),

        "avatar":
            get_random_avatar(),

        "message":
            generate_short_message(),

        "time":
            generate_search_time(),

        "unread":
            unread,

        "muted":
            random.random() < 0.20,

        "pinned":
            random.random() < 0.12,
    }


# ==========================================================
# Message Result
# ==========================================================

def generate_message_result():

    has_image = (
        random.random() < 0.18
    )


    return {

        "sender":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "message":
            fake.sentence(
                nb_words=random.randint(
                    6,
                    16,
                )
            ),

        "time":
            generate_search_time(),

        "chat_name":
            random.choice(
                [
                    fake.name(),
                    fake.company(),
                    fake.catch_phrase(),
                ]
            ),

        "image":
            (
                get_random_chat_image()
                if has_image
                else None
            ),
    }


# ==========================================================
# Search Result State
# ==========================================================

def generate_populated_search():

    query = (
        generate_query()
    )


    people_count = random.randint(
        1,
        4,
    )

    chat_count = random.randint(
        2,
        6,
    )

    message_count = random.randint(
        2,
        8,
    )


    return {

        "state":
            "results",

        "query":
            query,

        "show_clear_button":
            True,

        "recent_searches":
            [],

        "people":
            [
                generate_person_result()
                for _ in range(
                    people_count
                )
            ],

        "chats":
            [
                generate_chat_result()
                for _ in range(
                    chat_count
                )
            ],

        "messages":
            [
                generate_message_result()
                for _ in range(
                    message_count
                )
            ],
    }


# ==========================================================
# Empty Search State
# ==========================================================

def generate_empty_search():

    return {

        "state":
            "empty",

        "query":
            generate_query(),

        "show_clear_button":
            True,

        "recent_searches":
            [],

        "people":
            [],

        "chats":
            [],

        "messages":
            [],

        "empty_title":
            "No results found",

        "empty_subtitle":
            "Try searching for something else.",
    }


# ==========================================================
# Initial Search State
# ==========================================================

def generate_initial_search():

    recent_count = random.randint(
        3,
        7,
    )


    return {

        "state":
            "initial",

        "query":
            "",

        "show_clear_button":
            False,

        "recent_searches":
            [
                generate_recent_search()
                for _ in range(
                    recent_count
                )
            ],

        "people":
            [],

        "chats":
            [],

        "messages":
            [],
    }


# ==========================================================
# Search Page
# ==========================================================

def generate_search_page():

    state = random.choices(
        [
            "results",
            "initial",
            "empty",
        ],
        weights=[
            0.65,
            0.25,
            0.10,
        ],
        k=1,
    )[0]


    if state == "results":

        search_data = (
            generate_populated_search()
        )

    elif state == "empty":

        search_data = (
            generate_empty_search()
        )

    else:

        search_data = (
            generate_initial_search()
        )


    search_data.update(
        {

            "title":
                "Search",

            "placeholder":
                "Search...",

            "selected_navigation":
                None,

            "filters":
                [
                    {
                        "label":
                            "Unread",

                        "semantic":
                            "unread_filter",
                    },
                    {
                        "label":
                            "Photos",

                        "semantic":
                            "photos_filter",
                    },
                    {
                        "label":
                            "Videos",

                        "semantic":
                            "videos_filter",
                    },
                    {
                        "label":
                            "Links",

                        "semantic":
                            "links_filter",
                    },
                ],
        }
    )


    return search_data


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_search_page()
    )


    print(
        "\nSEARCH PAGE"
    )

    print(
        "State:",
        page["state"]
    )

    print(
        "Query:",
        page["query"]
    )

    print(
        "Recent searches:",
        len(
            page["recent_searches"]
        )
    )

    print(
        "People:",
        len(
            page["people"]
        )
    )

    print(
        "Chats:",
        len(
            page["chats"]
        )
    )

    print(
        "Messages:",
        len(
            page["messages"]
        )
    )