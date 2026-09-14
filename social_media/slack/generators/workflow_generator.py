# social_media/slack/generators/workflow_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_avatar,
    get_random_emoji,
    get_random_workspace_image,
)


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
]


WORKFLOW_NAMES = [
    "New request workflow",
    "Bug triage automation",
    "Weekly research update",
    "Release approval",
    "Dataset review workflow",
    "New member onboarding",
    "Design feedback flow",
]


TRIGGERS = [
    {
        "type": "message",
        "title": "When a message is posted",
        "description": "Start when a new message appears in a channel.",
        "icon": "chat",
    },
    {
        "type": "reaction",
        "title": "When a reaction is added",
        "description": "Start when someone reacts to a message.",
        "icon": "add_reaction",
    },
    {
        "type": "schedule",
        "title": "On a schedule",
        "description": "Run automatically at a scheduled time.",
        "icon": "schedule",
    },
    {
        "type": "form",
        "title": "When a form is submitted",
        "description": "Start when someone submits a workflow form.",
        "icon": "description",
    },
]


ACTION_LIBRARY = [
    {
        "type": "send_message",
        "title": "Send a message",
        "description": "Post a message to a channel.",
        "icon": "send",
    },
    {
        "type": "form",
        "title": "Collect information",
        "description": "Ask someone to complete a form.",
        "icon": "list_alt",
    },
    {
        "type": "assign",
        "title": "Assign a person",
        "description": "Assign the workflow to a teammate.",
        "icon": "person_add",
    },
    {
        "type": "delay",
        "title": "Wait",
        "description": "Pause before continuing.",
        "icon": "timer",
    },
    {
        "type": "condition",
        "title": "Add a condition",
        "description": "Continue only when a condition matches.",
        "icon": "fork_right",
    },
    {
        "type": "notify",
        "title": "Send notification",
        "description": "Notify selected people.",
        "icon": "notifications",
    },
]


CHANNELS = [
    "general",
    "engineering",
    "design",
    "research",
    "product",
    "release",
    "accessibility",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_person(index: int) -> dict:

    return {
        "id": index,
        "name": fake.name(),
        "avatar": get_random_avatar(),
    }


def generate_step(
    index: int,
    action: dict,
) -> dict:

    reaction = None

    if random.random() < 0.18:
        reaction = get_random_emoji()

    return {
        "id": index,

        "type":
            action["type"],

        "title":
            action["title"],

        "description":
            action["description"],

        "icon":
            action["icon"],

        "enabled":
            random.random() < 0.88,

        "has_error":
            random.random() < 0.12,

        "reaction":
            reaction,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_workflow_data() -> dict:

    people = [
        generate_person(index)
        for index in range(
            random.randint(8, 14)
        )
    ]

    trigger = random.choice(
        TRIGGERS
    )

    action_count = random.randint(
        3,
        6,
    )

    selected_actions = random.sample(
        ACTION_LIBRARY,
        k=action_count,
    )

    steps = [
        generate_step(
            index=index + 1,
            action=action,
        )
        for index, action
        in enumerate(selected_actions)
    ]

    selected_step = random.choice(
        steps
    )

    collaborators = random.sample(
        people,
        k=random.randint(
            2,
            4,
        ),
    )

    return {

        "workspace": {
            "name":
                random.choice(
                    WORKSPACE_NAMES
                ),

            "image":
                get_random_workspace_image(),
        },

        "workflow_name":
            random.choice(
                WORKFLOW_NAMES
            ),

        "trigger":
            trigger,

        "steps":
            steps,

        "selected_step":
            selected_step,

        "collaborators":
            collaborators,

        "channel":
            random.choice(
                CHANNELS
            ),

        "status":
            random.choice(
                [
                    "Draft",
                    "Active",
                    "Needs attention",
                ]
            ),

        "run_count":
            random.randint(
                0,
                284,
            ),

        "last_run":
            random.choice(
                [
                    "Never",
                    "5 minutes ago",
                    "1 hour ago",
                    "Yesterday",
                ]
            ),

        "side_panel":
            random.choice(
                [
                    "configure",
                    "steps",
                ]
            ),

        "is_enabled":
            random.random() < 0.72,

        "search_placeholder":
            "Search workflow steps",
    }


if __name__ == "__main__":

    data = generate_workflow_data()

    print(
        "Workflow:",
        data["workflow_name"]
    )

    print(
        "Steps:",
        len(
            data["steps"]
        )
    )