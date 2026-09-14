# social_media/slack/generators/profile_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_avatar,
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


JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Product Designer",
    "UX Researcher",
    "Product Manager",
    "Frontend Engineer",
    "Backend Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "QA Engineer",
]


DEPARTMENTS = [
    "Engineering",
    "Design",
    "Research",
    "Product",
    "Data",
    "Quality",
    "Platform",
]


LOCATIONS = [
    "Seoul",
    "Busan",
    "Tokyo",
    "Singapore",
    "London",
    "New York",
    "San Francisco",
    "Remote",
]


STATUS_TEXTS = [
    "In a meeting",
    "Working remotely",
    "Focusing",
    "Reviewing",
    "Lunch",
    "Available",
    "Heads down",
]


CHANNEL_NAMES = [
    "general",
    "engineering",
    "design",
    "research",
    "product",
    "machine-learning",
    "frontend",
    "backend",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_person(
    index: int,
) -> dict:

    name = fake.name()

    return {

        "id":
            index,

        "name":
            name,

        "avatar":
            get_random_avatar(),

        "title":
            random.choice(
                JOB_TITLES
            ),

        "department":
            random.choice(
                DEPARTMENTS
            ),

        "location":
            random.choice(
                LOCATIONS
            ),

        "email":
            fake.email(),

        "phone":
            fake.phone_number(),

        "timezone":
            random.choice(
                [
                    "GMT+9",
                    "GMT+8",
                    "GMT",
                    "GMT-5",
                    "GMT-8",
                ]
            ),

        "local_time":
            random.choice(
                [
                    "9:14 AM",
                    "10:32 AM",
                    "1:25 PM",
                    "3:48 PM",
                    "6:05 PM",
                ]
            ),

        "online":
            random.random() < 0.7,

        "status":
            random.choice(
                STATUS_TEXTS
            ),

        "status_emoji":
            random.choice(
                [
                    "💻",
                    "🎧",
                    "☕",
                    "📚",
                    "🧪",
                    "🚀",
                ]
            ),

        "pronouns":
            random.choice(
                [
                    "she/her",
                    "he/him",
                    "they/them",
                    "",
                ]
            ),

        "manager":
            fake.name(),

        "start_date":
            random.choice(
                [
                    "Jan 2023",
                    "Mar 2024",
                    "Jun 2022",
                    "Sep 2025",
                    "Feb 2021",
                ]
            ),

        "bio":
            fake.sentence(
                nb_words=random.randint(
                    8,
                    15,
                )
            ),
    }


# ==========================================================
# Profile Data
# ==========================================================

def generate_profile_data() -> dict:

    people = [

        generate_person(
            index=index
        )

        for index in range(
            random.randint(
                12,
                20,
            )
        )
    ]

    selected_index = random.randint(
        0,
        len(people) - 1,
    )

    selected_person = people[
        selected_index
    ]

    channels = random.sample(
        CHANNEL_NAMES,
        k=random.randint(
            4,
            7,
        ),
    )

    workspace_name = random.choice(
        WORKSPACE_NAMES
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
        # People
        # ------------------------------------------------------

        "people":
            people,

        "selected_person":
            selected_person,


        # ------------------------------------------------------
        # Shared Channels
        # ------------------------------------------------------

        "shared_channels":
            channels,


        # ------------------------------------------------------
        # Profile Settings / Controls
        # ------------------------------------------------------

        "controls": [

            {
                "label":
                    "Notifications",

                "description":
                    "Notify me when this person messages.",

                "enabled":
                    random.random() < 0.7,
            },

            {
                "label":
                    "Mute conversation",

                "description":
                    "Hide notifications from direct messages.",

                "enabled":
                    random.random() < 0.25,
            },

            {
                "label":
                    "Show activity",

                "description":
                    "Show this member in your activity feed.",

                "enabled":
                    random.random() < 0.8,
            },
        ],


        # ------------------------------------------------------
        # Search
        # ------------------------------------------------------

        "search_placeholder":
            f"Search {workspace_name}",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_profile_data()

    print(
        "\n=============================="
    )

    print(
        "SLACK PROFILE DATA"
    )

    print(
        "=============================="
    )

    print(
        "Workspace:",
        data["workspace"]["name"]
    )

    print(
        "People:",
        len(
            data["people"]
        )
    )

    print(
        "Selected:",
        data["selected_person"]["name"]
    )