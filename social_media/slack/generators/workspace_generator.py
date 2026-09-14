# social_media/slack/generators/workspace_generator.py

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
# Slack Vocabulary
# ==========================================================

CHANNEL_NAMES = [
    "general",
    "announcements",
    "engineering",
    "design",
    "product",
    "research",
    "marketing",
    "random",
    "frontend",
    "backend",
    "mobile",
    "machine-learning",
    "accessibility",
    "release",
    "support",
    "project-alpha",
    "project-orbit",
    "team-updates",
]


WORKSPACE_NAMES = [
    "Acme Studio",
    "Northstar",
    "Orbit Labs",
    "Pixel Works",
    "Nova Research",
    "Mosaic",
    "Vertex",
    "Bluebird",
    "Nimbus",
    "Launchpad",
]


MESSAGE_TEMPLATES = [
    "Good morning everyone! Here is a quick update from my side.",
    "I pushed the latest changes. Could someone review them when you have time?",
    "This looks much better after the latest iteration.",
    "I found one edge case that we should probably handle before release.",
    "The new layout works well on mobile and desktop.",
    "I'll update the document with the results from today's test.",
    "Has anyone tested this on the smaller viewport yet?",
    "I think we should keep this behavior consistent across the other screens.",
    "Nice work on this. The interaction feels much clearer now.",
    "The implementation is ready for another round of testing.",
    "I added a few comments to the design.",
    "Can we discuss this during the afternoon sync?",
    "The latest build fixed the issue we saw yesterday.",
    "There are still a couple of spacing issues on the tablet layout.",
    "I'll prepare a separate example for this case.",
]


STATUS_MESSAGES = [
    "",
    "",
    "",
    "In a meeting",
    "Working remotely",
    "Heads down",
    "Reviewing PRs",
    "Designing",
]


REACTION_EMOJIS = [
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

def _generate_time() -> str:

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


def _generate_person() -> dict:

    name = fake.name()

    return {

        "name":
            name,

        "avatar":
            get_random_avatar(),

        "status":
            random.choice(
                STATUS_MESSAGES
            ),

        "online":
            random.random() < 0.75,
    }


# ==========================================================
# Reaction Generator
# ==========================================================

def generate_reactions() -> list[dict]:

    if random.random() < 0.45:

        return []

    reaction_count = random.randint(
        1,
        3,
    )

    emojis = random.sample(
        REACTION_EMOJIS,
        k=reaction_count,
    )

    return [

        {
            "emoji":
                emoji,

            "count":
                random.randint(
                    1,
                    18,
                ),
        }

        for emoji
        in emojis
    ]


# ==========================================================
# Attachment Generator
# ==========================================================

def generate_attachment() -> dict | None:

    if random.random() > 0.22:

        return None

    attachment_type = random.choice(
        [
            "image",
            "image",
            "file",
        ]
    )

    if attachment_type == "image":

        return {

            "type":
                "image",

            "image":
                get_random_attachment(),

            "filename":
                fake.file_name(
                    extension="png"
                ),

        }

    return {

        "type":
            "file",

        "filename":
            fake.file_name(
                extension=random.choice(
                    [
                        "pdf",
                        "docx",
                        "pptx",
                        "zip",
                    ]
                )
            ),

        "size":
            f"{random.randint(120, 950)} KB",
    }


# ==========================================================
# Message Generator
# ==========================================================

def generate_message(
    author: dict,
    message_index: int,
) -> dict:

    text = random.choice(
        MESSAGE_TEMPLATES
    )

    if random.random() < 0.32:

        text = (
            text
            + " "
            + fake.sentence(
                nb_words=random.randint(
                    5,
                    12,
                )
            )
        )

    has_thread = (
        random.random()
        < 0.25
    )

    reply_count = (
        random.randint(
            2,
            14,
        )
        if has_thread
        else 0
    )

    return {

        "id":
            message_index,

        "author":
            author,

        "time":
            _generate_time(),

        "text":
            text,

        "edited":
            random.random() < 0.08,

        "reactions":
            generate_reactions(),

        "attachment":
            generate_attachment(),

        "reply_count":
            reply_count,

        "thread_label":
            (
                f"{reply_count} replies"
                if reply_count
                else None
            ),
    }


# ==========================================================
# Channel Generator
# ==========================================================

def generate_channels() -> list[dict]:

    count = random.randint(
        9,
        15,
    )

    selected_names = random.sample(
        CHANNEL_NAMES,
        k=count,
    )

    channels = []

    for index, name in enumerate(
        selected_names
    ):

        channels.append(

            {
                "name":
                    name,

                "selected":
                    index == 0,

                "private":
                    (
                        random.random()
                        < 0.16
                    ),

                "unread":
                    (
                        random.randint(
                            1,
                            14,
                        )
                        if (
                            index != 0
                            and random.random()
                            < 0.25
                        )
                        else 0
                    ),

                "muted":
                    (
                        random.random()
                        < 0.08
                    ),
            }
        )

    return channels


# ==========================================================
# Direct Messages
# ==========================================================

def generate_direct_messages(
    people: list[dict],
) -> list[dict]:

    selected_people = random.sample(
        people,
        k=min(
            random.randint(
                4,
                7,
            ),
            len(people),
        ),
    )

    return [

        {
            **person,

            "unread":
                (
                    random.randint(
                        1,
                        5,
                    )
                    if random.random() < 0.2
                    else 0
                ),
        }

        for person
        in selected_people
    ]


# ==========================================================
# Workspace Generator
# ==========================================================

def generate_workspace_data() -> dict:

    people = [

        _generate_person()

        for _ in range(
            random.randint(
                12,
                20,
            )
        )
    ]

    channels = generate_channels()

    current_channel = (
        channels[0]
    )

    message_count = random.randint(
        18,
        32,
    )

    messages = []

    for message_index in range(
        message_count
    ):

        author = random.choice(
            people
        )

        messages.append(

            generate_message(
                author=author,
                message_index=message_index,
            )
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

            "member_count":
                random.randint(
                    24,
                    240,
                ),
        },


        # ------------------------------------------------------
        # Current User
        # ------------------------------------------------------

        "current_user":
            people[0],


        # ------------------------------------------------------
        # Navigation
        # ------------------------------------------------------

        "channels":
            channels,

        "direct_messages":
            generate_direct_messages(
                people
            ),


        # ------------------------------------------------------
        # Current Channel
        # ------------------------------------------------------

        "channel": {

            "name":
                current_channel[
                    "name"
                ],

            "description":
                fake.sentence(
                    nb_words=random.randint(
                        6,
                        11,
                    )
                ),

            "member_count":
                random.randint(
                    8,
                    85,
                ),

            "bookmarked":
                random.random() < 0.5,
        },


        # ------------------------------------------------------
        # Messages
        # ------------------------------------------------------

        "messages":
            messages,


        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        "search_placeholder":
            f"Search {workspace_name}",


        # ------------------------------------------------------
        # Composer
        # ------------------------------------------------------

        "composer_placeholder":
            (
                "Message #"
                + current_channel[
                    "name"
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_workspace_data()
    )

    print(
        "\n=============================="
    )

    print(
        "SLACK WORKSPACE DATA"
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
        "Channels:",
        len(
            data["channels"]
        )
    )