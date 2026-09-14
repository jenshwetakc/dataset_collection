# social_media/slack/generators/huddle_generator.py

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
]


CHANNEL_NAMES = [
    "engineering",
    "design",
    "research",
    "product",
    "team-updates",
    "machine-learning",
    "general",
]


REACTIONS = [
    "👍",
    "❤️",
    "🎉",
    "👏",
    "😂",
    "🔥",
]


CHAT_MESSAGES = [
    "I can see your screen now.",
    "The latest version looks good.",
    "Could you zoom in a little?",
    "I think this is the correct layout.",
    "Let's compare it with the previous build.",
    "The mobile version still needs one adjustment.",
    "This works much better now.",
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

        "muted":
            random.random() < 0.38,

        "camera_on":
            random.random() < 0.52,

        "speaking":
            False,

        "hand_raised":
            random.random() < 0.12,

        "reaction":
            (
                random.choice(
                    REACTIONS
                )
                if random.random() < 0.16
                else None
            ),

        "connection":
            random.choice(
                [
                    "excellent",
                    "good",
                    "good",
                    "fair",
                ]
            ),
    }


# ==========================================================
# Chat
# ==========================================================

def generate_chat_messages(
    people: list[dict],
) -> list[dict]:

    return [

        {
            "author":
                random.choice(
                    people
                ),

            "text":
                random.choice(
                    CHAT_MESSAGES
                ),

            "time":
                random.choice(
                    [
                        "10:14",
                        "10:18",
                        "10:21",
                        "10:24",
                        "10:28",
                        "10:31",
                    ]
                ),
        }

        for _ in range(
            random.randint(
                5,
                9,
            )
        )
    ]


# ==========================================================
# Huddle Generator
# ==========================================================

def generate_huddle_data() -> dict:

    participant_count = random.randint(
        5,
        10,
    )

    participants = [

        generate_person(
            index=index
        )

        for index in range(
            participant_count
        )
    ]

    active_speaker = random.choice(
        participants
    )

    active_speaker[
        "speaking"
    ] = True

    workspace_name = random.choice(
        WORKSPACE_NAMES
    )

    channel_name = random.choice(
        CHANNEL_NAMES
    )

    current_user = participants[0]

    controls = {

        "microphone_on":
            not current_user["muted"],

        "camera_on":
            current_user[
                "camera_on"
            ],

        "screen_sharing":
            random.random() < 0.18,

        "captions_on":
            random.random() < 0.22,

        "side_panel":
            random.choice(
                [
                    "participants",
                    "chat",
                ]
            ),
    }

    return {

        "workspace": {
            "name":
                workspace_name,

            "image":
                get_random_workspace_image(),
        },

        "channel": {
            "name":
                channel_name,
        },

        "participants":
            participants,

        "active_speaker":
            active_speaker,

        "current_user":
            current_user,

        "controls":
            controls,

        "chat_messages":
            generate_chat_messages(
                participants
            ),

        "duration":
            random.choice(
                [
                    "12:34",
                    "18:09",
                    "24:45",
                    "37:11",
                    "46:20",
                ]
            ),

        "topic":
            random.choice(
                [
                    "Weekly project sync",
                    "Design review",
                    "Implementation discussion",
                    "Research meeting",
                    "Release planning",
                    "Dataset review",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_huddle_data()

    print(
        "\n=============================="
    )

    print(
        "SLACK HUDDLE DATA"
    )

    print(
        "=============================="
    )

    print(
        "Workspace:",
        data["workspace"]["name"]
    )

    print(
        "Channel:",
        data["channel"]["name"]
    )

    print(
        "Participants:",
        len(
            data["participants"]
        )
    )

    print(
        "Active speaker:",
        data["active_speaker"]["name"]
    )