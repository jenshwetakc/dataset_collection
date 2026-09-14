# social_media/slack/generators/activity_generator.py

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
    "general",
    "engineering",
    "design",
    "product",
    "research",
    "frontend",
    "backend",
    "accessibility",
    "random",
    "team-updates",
    "release",
    "machine-learning",
]


ACTIVITY_TYPES = [
    "mention",
    "reaction",
    "thread_reply",
    "channel_invite",
    "direct_message",
]


REACTIONS = [
    "👍",
    "❤️",
    "🎉",
    "🔥",
    "👀",
    "✅",
    "👏",
    "🚀",
]


MENTION_MESSAGES = [
    "Could you take a look at this when you have a chance?",
    "I think @you worked on something similar last week.",
    "@you can probably help us verify this behavior.",
    "This should match the implementation @you added earlier.",
    "@you do you think we should keep this layout?",
    "I tagged @you because this affects the mobile version too.",
    "@you could you review the updated screenshots?",
]


THREAD_MESSAGES = [
    "I agree with the approach you suggested.",
    "That fixed the issue on my side.",
    "I added another example to the thread.",
    "We should probably test this on tablet as well.",
    "I uploaded the latest version for comparison.",
    "The spacing looks better after the update.",
]


DIRECT_MESSAGES = [
    "Do you have a minute to check something?",
    "I sent you the latest build.",
    "Thanks for the review!",
    "Can we sync later today?",
    "I think I found the issue.",
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

        "online":
            random.random() < 0.72,
    }


# ==========================================================
# Individual Activity Items
# ==========================================================

def generate_mention(
    person: dict,
    index: int,
) -> dict:

    return {

        "id":
            index,

        "type":
            "mention",

        "person":
            person,

        "channel":
            random.choice(
                CHANNEL_NAMES
            ),

        "time":
            generate_time_text(),

        "message":
            random.choice(
                MENTION_MESSAGES
            ),

        "unread":
            random.random() < 0.62,

        "reaction":
            None,

        "reply_count":
            random.randint(
                0,
                8,
            ),
    }


def generate_reaction(
    person: dict,
    index: int,
) -> dict:

    return {

        "id":
            index,

        "type":
            "reaction",

        "person":
            person,

        "channel":
            random.choice(
                CHANNEL_NAMES
            ),

        "time":
            generate_time_text(),

        "message":
            random.choice(
                [
                    "The latest implementation is ready for review.",
                    "I updated the screenshots and annotations.",
                    "This is the version we discussed yesterday.",
                    "The mobile layout is working correctly now.",
                    "The generated sample looks much more realistic.",
                ]
            ),

        "unread":
            random.random() < 0.45,

        "reaction":
            random.choice(
                REACTIONS
            ),

        "reply_count":
            0,
    }


def generate_thread_reply(
    person: dict,
    index: int,
) -> dict:

    return {

        "id":
            index,

        "type":
            "thread_reply",

        "person":
            person,

        "channel":
            random.choice(
                CHANNEL_NAMES
            ),

        "time":
            generate_time_text(),

        "message":
            random.choice(
                THREAD_MESSAGES
            ),

        "unread":
            random.random() < 0.55,

        "reaction":
            None,

        "reply_count":
            random.randint(
                2,
                12,
            ),
    }


def generate_channel_invite(
    person: dict,
    index: int,
) -> dict:

    return {

        "id":
            index,

        "type":
            "channel_invite",

        "person":
            person,

        "channel":
            random.choice(
                CHANNEL_NAMES
            ),

        "time":
            generate_time_text(),

        "message":
            (
                f"{person['name']} "
                f"invited you to join "
                f"#{random.choice(CHANNEL_NAMES)}."
            ),

        "unread":
            random.random() < 0.7,

        "reaction":
            None,

        "reply_count":
            0,
    }


def generate_direct_message(
    person: dict,
    index: int,
) -> dict:

    return {

        "id":
            index,

        "type":
            "direct_message",

        "person":
            person,

        "channel":
            None,

        "time":
            generate_time_text(),

        "message":
            random.choice(
                DIRECT_MESSAGES
            ),

        "unread":
            random.random() < 0.65,

        "reaction":
            None,

        "reply_count":
            0,
    }


# ==========================================================
# Generic Activity
# ==========================================================

def generate_activity_item(
    people: list[dict],
    index: int,
) -> dict:

    person = random.choice(
        people
    )

    activity_type = random.choices(
        ACTIVITY_TYPES,
        weights=[
            34,
            24,
            20,
            8,
            14,
        ],
        k=1,
    )[0]

    if activity_type == "mention":

        return generate_mention(
            person,
            index,
        )

    if activity_type == "reaction":

        return generate_reaction(
            person,
            index,
        )

    if activity_type == "thread_reply":

        return generate_thread_reply(
            person,
            index,
        )

    if activity_type == "channel_invite":

        return generate_channel_invite(
            person,
            index,
        )

    return generate_direct_message(
        person,
        index,
    )


# ==========================================================
# Sidebar Data
# ==========================================================

def generate_sidebar_channels() -> list[dict]:

    channels = random.sample(
        CHANNEL_NAMES,
        k=random.randint(
            7,
            10,
        ),
    )

    return [

        {
            "name":
                channel,

            "unread":
                (
                    random.randint(
                        1,
                        12,
                    )
                    if random.random() < 0.28
                    else 0
                ),
        }

        for channel
        in channels
    ]


# ==========================================================
# Activity Page
# ==========================================================

def generate_activity_data() -> dict:

    people = [

        generate_person()

        for _ in range(
            random.randint(
                12,
                18,
            )
        )
    ]

    today_count = random.randint(
        7,
        12,
    )

    yesterday_count = random.randint(
        5,
        9,
    )

    earlier_count = random.randint(
        3,
        7,
    )

    current_index = 0

    groups = []

    for title, count in [
        (
            "Today",
            today_count,
        ),
        (
            "Yesterday",
            yesterday_count,
        ),
        (
            "Earlier",
            earlier_count,
        ),
    ]:

        items = []

        for _ in range(
            count
        ):

            items.append(
                generate_activity_item(
                    people=people,
                    index=current_index,
                )
            )

            current_index += 1

        groups.append(
            {
                "title":
                    title,

                "items":
                    items,
            }
        )

    unread_count = sum(

        1

        for group in groups

        for item in group["items"]

        if item["unread"]
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
        # Sidebar
        # ------------------------------------------------------

        "channels":
            generate_sidebar_channels(),

        "direct_messages":
            random.sample(
                people,
                k=min(
                    5,
                    len(people),
                ),
            ),


        # ------------------------------------------------------
        # Activity
        # ------------------------------------------------------

        "activity_groups":
            groups,

        "unread_count":
            unread_count,


        # ------------------------------------------------------
        # Filter Tabs
        # ------------------------------------------------------

        "filters": [
            {
                "label":
                    "All",

                "selected":
                    True,
            },
            {
                "label":
                    "Mentions",

                "selected":
                    False,
            },
            {
                "label":
                    "Threads",

                "selected":
                    False,
            },
            {
                "label":
                    "Reactions",

                "selected":
                    False,
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

    data = generate_activity_data()

    print(
        "\n=============================="
    )

    print(
        "SLACK ACTIVITY DATA"
    )

    print(
        "=============================="
    )

    print(
        "Workspace:",
        data["workspace"]["name"]
    )

    print(
        "Unread:",
        data["unread_count"]
    )

    print(
        "Groups:",
        len(
            data["activity_groups"]
        )
    )