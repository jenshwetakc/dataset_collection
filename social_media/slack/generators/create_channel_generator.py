# social_media/slack/generators/create_channel_generator.py

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


CHANNEL_NAMES = [
    "project-nova",
    "release-planning",
    "design-review",
    "research-sync",
    "mobile-team",
    "dataset-review",
    "accessibility",
    "frontend",
    "experiment-lab",
]


CHANNEL_PURPOSES = [
    "Discuss planning, implementation, and weekly progress.",
    "Coordinate upcoming releases and resolve blockers.",
    "Share design updates and collect feedback from the team.",
    "Discuss research findings, experiments, and next steps.",
    "Keep project files, decisions, and updates in one place.",
    "Review generated datasets and annotation quality.",
]


ROLE_LABELS = [
    "Software Engineer",
    "Product Designer",
    "Researcher",
    "Product Manager",
    "Data Scientist",
    "QA Engineer",
    "Frontend Engineer",
    "Backend Engineer",
]


# ==========================================================
# Person
# ==========================================================

def generate_person(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "role":
            random.choice(
                ROLE_LABELS
            ),

        "selected":
            False,
    }


# ==========================================================
# Data
# ==========================================================

def generate_create_channel_data() -> dict:

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

    selected_people = random.sample(
        people,
        k=random.randint(
            2,
            5,
        ),
    )

    for person in selected_people:

        person["selected"] = True

    workspace_name = random.choice(
        WORKSPACE_NAMES
    )

    private_channel = (
        random.random()
        < 0.28
    )

    allow_external = (
        random.random()
        < 0.18
    )

    channel_name = random.choice(
        CHANNEL_NAMES
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
        # Channel Form
        # ------------------------------------------------------

        "channel_name":
            channel_name,

        "channel_purpose":
            random.choice(
                CHANNEL_PURPOSES
            ),

        "private_channel":
            private_channel,

        "allow_external":
            allow_external,

        "posting_permission":
            random.choice(
                [
                    "Everyone",
                    "Admins only",
                    "Selected people",
                ]
            ),


        # ------------------------------------------------------
        # Members
        # ------------------------------------------------------

        "people":
            people,

        "selected_people":
            selected_people,

        "remaining_count":
            max(
                0,
                len(people)
                - len(selected_people),
            ),


        # ------------------------------------------------------
        # Existing Channels
        # ------------------------------------------------------

        "background_channels":
            random.sample(
                [
                    "general",
                    "engineering",
                    "design",
                    "research",
                    "product",
                    "team-updates",
                    "random",
                    "release",
                    "accessibility",
                ],
                k=7,
            ),


        # ------------------------------------------------------
        # Modal
        # ------------------------------------------------------

        "modal_step":
            random.choice(
                [
                    "details",
                    "members",
                ]
            ),

        "search_placeholder":
            "Search people",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_create_channel_data()

    print(
        "Workspace:",
        data["workspace"]["name"]
    )

    print(
        "Channel:",
        data["channel_name"]
    )

    print(
        "Selected:",
        len(
            data["selected_people"]
        )
    )