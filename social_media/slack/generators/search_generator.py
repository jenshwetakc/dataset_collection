# social_media/slack/generators/search_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_avatar,
    get_random_attachment,
    get_random_workspace_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Constants
# ==========================================================

WORKSPACE_NAMES = [
    "Acme Studio",
    "Northstar",
    "Orbit Labs",
    "Pixel Works",
    "Nova Research",
    "Mosaic",
    "Vertex",
    "Nimbus",
    "Launchpad",
]


CHANNEL_NAMES = [
    "general",
    "engineering",
    "design",
    "product",
    "research",
    "frontend",
    "backend",
    "accessibility",
    "machine-learning",
    "team-updates",
    "release",
    "random",
]


SEARCH_TERMS = [
    "design",
    "release",
    "mobile",
    "dataset",
    "annotation",
    "accessibility",
    "renderer",
    "testing",
    "project",
    "prototype",
]


MESSAGE_TEMPLATES = [
    "The {term} update is ready for another review.",
    "I uploaded the latest {term} screenshots for comparison.",
    "We should validate the {term} behavior on tablet as well.",
    "The current {term} implementation works correctly on desktop.",
    "I found another issue related to the {term} layout.",
    "Can someone review the new {term} version?",
    "The {term} changes were included in today's build.",
    "This document summarizes our current {term} approach.",
]


FILE_TYPES = [
    "pdf",
    "pptx",
    "docx",
    "zip",
    "png",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_time_text() -> str:

    hour = random.randint(
        8,
        20,
    )

    minute = random.choice(
        [
            0,
            5,
            10,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
        ]
    )

    suffix = (
        "AM"
        if hour < 12
        else "PM"
    )

    display_hour = hour

    if display_hour > 12:
        display_hour -= 12

    return (
        f"{display_hour}:"
        f"{minute:02d} "
        f"{suffix}"
    )


def generate_person() -> dict:

    return {
        "name":
            fake.name(),

        "title":
            random.choice(
                [
                    "Software Engineer",
                    "Product Designer",
                    "Researcher",
                    "Product Manager",
                    "Frontend Engineer",
                    "Backend Engineer",
                    "UX Designer",
                    "Data Scientist",
                ]
            ),

        "avatar":
            get_random_avatar(),

        "online":
            random.random() < 0.7,
    }


# ==========================================================
# People Results
# ==========================================================

def generate_people_results() -> list[dict]:

    return [

        generate_person()

        for _ in range(
            random.randint(
                3,
                6,
            )
        )
    ]


# ==========================================================
# Channel Results
# ==========================================================

def generate_channel_results() -> list[dict]:

    selected = random.sample(
        CHANNEL_NAMES,
        k=random.randint(
            3,
            6,
        ),
    )

    return [

        {
            "name":
                name,

            "description":
                fake.sentence(
                    nb_words=random.randint(
                        5,
                        10,
                    )
                ),

            "member_count":
                random.randint(
                    8,
                    240,
                ),

            "private":
                random.random() < 0.18,

            "joined":
                random.random() < 0.68,
        }

        for name
        in selected
    ]


# ==========================================================
# File Results
# ==========================================================

def generate_file_results(
    people: list[dict],
    search_term: str,
) -> list[dict]:

    results = []

    for index in range(
        random.randint(
            3,
            5,
        )
    ):

        extension = random.choice(
            FILE_TYPES
        )

        preview = (
            get_random_attachment()
            if extension == "png"
            else None
        )

        results.append(
            {
                "id":
                    index,

                "name":
                    (
                        search_term
                        + "_"
                        + fake.word()
                        + "."
                        + extension
                    ),

                "extension":
                    extension,

                "author":
                    random.choice(
                        people
                    ),

                "channel":
                    random.choice(
                        CHANNEL_NAMES
                    ),

                "size":
                    (
                        f"{random.randint(120, 980)} KB"
                    ),

                "time":
                    generate_time_text(),

                "preview":
                    preview,
            }
        )

    return results


# ==========================================================
# Message Results
# ==========================================================

def generate_message_results(
    people: list[dict],
    search_term: str,
) -> list[dict]:

    results = []

    for index in range(
        random.randint(
            10,
            18,
        )
    ):

        message_template = random.choice(
            MESSAGE_TEMPLATES
        )

        results.append(
            {
                "id":
                    index,

                "author":
                    random.choice(
                        people
                    ),

                "channel":
                    random.choice(
                        CHANNEL_NAMES
                    ),

                "time":
                    generate_time_text(),

                "before_text":
                    random.choice(
                        [
                            "The ",
                            "Our ",
                            "This ",
                            "Latest ",
                            "",
                        ]
                    ),

                "highlight":
                    search_term,

                "after_text":
                    (
                        " "
                        + message_template.format(
                            term=""
                        ).strip()
                    ),

                "reply_count":
                    (
                        random.randint(
                            2,
                            12,
                        )
                        if random.random() < 0.24
                        else 0
                    ),

                "reaction_count":
                    (
                        random.randint(
                            1,
                            18,
                        )
                        if random.random() < 0.28
                        else 0
                    ),
            }
        )

    return results


# ==========================================================
# Search Page
# ==========================================================

def generate_search_data() -> dict:

    search_term = random.choice(
        SEARCH_TERMS
    )

    people = generate_people_results()

    channels = generate_channel_results()

    files = generate_file_results(
        people=people,
        search_term=search_term,
    )

    messages = generate_message_results(
        people=people,
        search_term=search_term,
    )

    workspace_name = random.choice(
        WORKSPACE_NAMES
    )

    total_results = (
        len(people)
        + len(channels)
        + len(files)
        + len(messages)
    )

    return {

        # ------------------------------------------------------
        # Workspace
        # ------------------------------------------------------

        "workspace": {
            "name":
                workspace_name,

            "image":
                get_random_workspace_image(),
        },


        # ------------------------------------------------------
        # Query
        # ------------------------------------------------------

        "query":
            search_term,

        "total_results":
            total_results,


        # ------------------------------------------------------
        # Tabs
        # ------------------------------------------------------

        "tabs": [
            {
                "label":
                    "Messages",

                "count":
                    len(messages),

                "selected":
                    True,
            },
            {
                "label":
                    "Files",

                "count":
                    len(files),

                "selected":
                    False,
            },
            {
                "label":
                    "People",

                "count":
                    len(people),

                "selected":
                    False,
            },
            {
                "label":
                    "Channels",

                "count":
                    len(channels),

                "selected":
                    False,
            },
        ],


        # ------------------------------------------------------
        # Filters
        # ------------------------------------------------------

        "filters": [
            "From",
            "In",
            "After",
            "Before",
            "Has",
        ],


        # ------------------------------------------------------
        # Results
        # ------------------------------------------------------

        "people":
            people,

        "channels":
            channels,

        "files":
            files,

        "messages":
            messages,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_search_data()

    print(
        "\n=============================="
    )

    print(
        "SLACK SEARCH DATA"
    )

    print(
        "=============================="
    )

    print(
        "Query:",
        data["query"]
    )

    print(
        "Total results:",
        data["total_results"]
    )

    print(
        "Messages:",
        len(
            data["messages"]
        )
    )

    print(
        "Files:",
        len(
            data["files"]
        )
    )