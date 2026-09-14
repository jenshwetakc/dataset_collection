# social_media/slack/generators/thread_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_attachment,
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


MESSAGE_TEXTS = [
    "I pushed the latest implementation. Could someone review it?",
    "The mobile layout looks better after the spacing update.",
    "There is still one issue with the tablet breakpoint.",
    "I uploaded a new example so we can compare the behavior.",
    "The annotation result now matches what we expected.",
    "Can we keep this pattern consistent across the other screens?",
    "I tested the latest version on desktop and mobile.",
    "The renderer is now producing the correct bounding boxes.",
    "We should verify the behavior on the smallest viewport.",
    "This version fixes the overlapping navigation issue.",
]


THREAD_REPLY_TEXTS = [
    "I tested it and it works correctly on my side.",
    "I can reproduce the issue on the tablet layout.",
    "The desktop version looks good now.",
    "I think the problem comes from the sticky header.",
    "That makes sense. I will update the CSS.",
    "I uploaded another screenshot for comparison.",
    "The annotation box is correct after the latest change.",
    "We should also check this in dark mode.",
    "I agree. Let's keep the same behavior everywhere.",
    "This is much closer to the expected Slack layout.",
]


REACTIONS = [
    "👍",
    "❤️",
    "🎉",
    "👀",
    "✅",
    "🔥",
    "👏",
    "🚀",
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

        "avatar":
            get_random_avatar(),

        "title":
            random.choice(
                [
                    "Software Engineer",
                    "Product Designer",
                    "Researcher",
                    "Product Manager",
                    "Frontend Engineer",
                    "Backend Engineer",
                    "Data Scientist",
                ]
            ),

        "online":
            random.random() < 0.72,
    }


# ==========================================================
# Reactions
# ==========================================================

def generate_reactions() -> list[dict]:

    if random.random() < 0.4:

        return []

    selected = random.sample(
        REACTIONS,
        k=random.randint(
            1,
            3,
        ),
    )

    return [
        {
            "emoji":
                emoji,

            "count":
                random.randint(
                    1,
                    14,
                ),
        }

        for emoji
        in selected
    ]


# ==========================================================
# Main Message
# ==========================================================

def generate_message(
    people: list[dict],
    index: int,
) -> dict:

    return {
        "id":
            index,

        "author":
            random.choice(
                people
            ),

        "time":
            generate_time_text(),

        "text":
            random.choice(
                MESSAGE_TEXTS
            ),

        "reactions":
            generate_reactions(),

        "reply_count":
            (
                random.randint(
                    2,
                    12,
                )
                if random.random() < 0.4
                else 0
            ),

        "attachment":
            (
                get_random_attachment()
                if random.random() < 0.18
                else None
            ),
    }


# ==========================================================
# Thread Reply
# ==========================================================

def generate_thread_reply(
    people: list[dict],
    index: int,
) -> dict:

    return {
        "id":
            index,

        "author":
            random.choice(
                people
            ),

        "time":
            generate_time_text(),

        "text":
            random.choice(
                THREAD_REPLY_TEXTS
            ),

        "reactions":
            generate_reactions(),

        "edited":
            random.random() < 0.1,
    }


# ==========================================================
# Channels
# ==========================================================

def generate_channels() -> list[dict]:

    names = random.sample(
        CHANNEL_NAMES,
        k=random.randint(
            8,
            11,
        ),
    )

    return [
        {
            "name":
                name,

            "selected":
                index == 0,

            "unread":
                (
                    random.randint(
                        1,
                        8,
                    )
                    if (
                        index != 0
                        and random.random() < 0.25
                    )
                    else 0
                ),

            "private":
                random.random() < 0.15,
        }

        for index, name
        in enumerate(names)
    ]


# ==========================================================
# Thread Page
# ==========================================================

def generate_thread_data() -> dict:

    people = [
        generate_person()

        for _ in range(
            random.randint(
                10,
                16,
            )
        )
    ]

    channels = generate_channels()

    channel = channels[0]

    messages = [
        generate_message(
            people=people,
            index=index,
        )

        for index in range(
            random.randint(
                10,
                16,
            )
        )
    ]

    # Ensure selected message has a thread.
    selected_index = random.randint(
        2,
        len(messages) - 3,
    )

    selected_message = messages[
        selected_index
    ]

    selected_message[
        "reply_count"
    ] = random.randint(
        5,
        12,
    )

    thread_replies = [
        generate_thread_reply(
            people=people,
            index=index,
        )

        for index in range(
            selected_message[
                "reply_count"
            ]
        )
    ]

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
        # Channel
        # ------------------------------------------------------

        "channel": {
            "name":
                channel["name"],

            "description":
                fake.sentence(
                    nb_words=random.randint(
                        6,
                        10,
                    )
                ),

            "member_count":
                random.randint(
                    18,
                    96,
                ),
        },


        # ------------------------------------------------------
        # Navigation
        # ------------------------------------------------------

        "channels":
            channels,


        # ------------------------------------------------------
        # Main Conversation
        # ------------------------------------------------------

        "messages":
            messages,

        "selected_message_id":
            selected_message["id"],


        # ------------------------------------------------------
        # Thread
        # ------------------------------------------------------

        "thread": {
            "parent":
                selected_message,

            "replies":
                thread_replies,

            "reply_count":
                len(
                    thread_replies
                ),
        },


        # ------------------------------------------------------
        # Members
        # ------------------------------------------------------

        "members":
            people[:6],


        # ------------------------------------------------------
        # Search
        # ------------------------------------------------------

        "search_placeholder":
            f"Search {workspace_name}",

        "thread_placeholder":
            "Reply to thread",
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_thread_data()

    print(
        "\n=============================="
    )

    print(
        "SLACK THREAD DATA"
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
        "Messages:",
        len(
            data["messages"]
        )
    )

    print(
        "Thread replies:",
        data["thread"]["reply_count"]
    )