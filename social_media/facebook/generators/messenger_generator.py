from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_post_image,
    get_random_emoji_with_source,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

MESSENGER_STATES = [
    "default",
    "default",
    "chat_open",
    "search_active",
    "message_menu_open",
    "emoji_picker",
    "attachment_sheet",
    "conversation_info",
    "call_overlay",
]


MESSAGE_TEXTS = [
    "Hey! How are you?",
    "Are you free later today?",
    "That sounds great.",
    "I'll send you the details.",
    "Thanks for letting me know!",
    "See you soon.",
    "Haha, that's amazing.",
    "Can you check this?",
    "I really like this idea.",
    "Let's do it.",
    "I'll message you when I arrive.",
    "That photo looks great.",
]


RECENT_PREVIEWS = [
    "Sounds good!",
    "See you tomorrow.",
    "Sent a photo",
    "Thank you!",
    "Let's talk later.",
    "Okay",
    "Can you send it again?",
    "See you soon!",
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

        "online":
            random.random()
            < 0.55,

        "last_active":
            random.choice(
                [
                    "Active now",
                    "Active 5m ago",
                    "Active 20m ago",
                    "Active 1h ago",
                    "Active yesterday",
                ]
            ),
    }


# ==========================================================
# Conversation
# ==========================================================

def generate_conversation(
    index: int,
) -> dict:

    person = generate_person(
        index
    )

    return {
        "id":
            index,

        "person":
            person,

        "preview":
            random.choice(
                RECENT_PREVIEWS
            ),

        "timestamp":
            random.choice(
                [
                    "Now",
                    "5m",
                    "20m",
                    "1h",
                    "3h",
                    "1d",
                ]
            ),

        "unread":
            random.random()
            < 0.35,

        "muted":
            random.random()
            < 0.15,
    }


def generate_conversations(
    count: int = 10,
) -> list[dict]:

    return [
        generate_conversation(
            index
        )
        for index in range(
            count
        )
    ]


# ==========================================================
# Message
# ==========================================================

def generate_message(
    index: int,
    person: dict,
) -> dict:

    if random.random() < 0.7:

        mine = (
            index % 3 != 0
        )

    else:

        mine = (
            random.random()
            < 0.5
        )


    message_type = random.choices(
        population=[
            "text",
            "image",
            "emoji",
        ],
        weights=[
            0.70,
            0.18,
            0.12,
        ],
        k=1,
    )[0]


    text = None

    image = None

    emoji = None


    if message_type == "text":

        text = random.choice(
            MESSAGE_TEXTS
        )


    elif message_type == "image":

        image = get_random_post_image()

        # Fallback
        if image is None:

            message_type = "text"

            text = random.choice(
                MESSAGE_TEXTS
            )


    elif message_type == "emoji":

        emoji = (
            get_random_emoji_with_source()
        )

        # Fallback
        if emoji is None:

            message_type = "text"

            text = random.choice(
                MESSAGE_TEXTS
            )


    return {
        "id":
            index,

        "mine":
            mine,

        "avatar":
            (
                None
                if mine
                else person["avatar"]
            ),

        "type":
            message_type,

        "text":
            text,

        "image":
            image,

        "emoji":
            emoji,

        "timestamp":
            random.choice(
                [
                    "10:12 AM",
                    "10:15 AM",
                    "10:22 AM",
                    "10:30 AM",
                    "11:02 AM",
                    "11:24 AM",
                ]
            ),

        "seen":
            (
                mine
                and
                random.random()
                < 0.7
            ),
    }


def generate_messages(
    person: dict,
    count: int = 14,
) -> list[dict]:

    return [
        generate_message(
            index=index,
            person=person,
        )
        for index in range(
            count
        )
    ]


# ==========================================================
# Emoji Picker
# ==========================================================

def generate_emojis(
    count: int = 24,
) -> list[dict]:

    emojis = []

    attempts = 0

    max_attempts = max(
        count * 5,
        40,
    )

    while (
        len(emojis) < count
        and
        attempts < max_attempts
    ):

        attempts += 1

        emoji = (
            get_random_emoji_with_source()
        )

        if emoji is None:
            continue

        emojis.append(
            {
                "id":
                    len(
                        emojis
                    ),

                "image":
                    emoji[
                        "image"
                    ],

                "source":
                    emoji[
                        "source"
                    ],
            }
        )

    return emojis


# ==========================================================
# Shared Media
# ==========================================================

def generate_shared_media(
    count: int = 6,
) -> list[dict]:

    media = []

    for index in range(
        count
    ):

        image = (
            get_random_post_image()
        )

        if image is None:
            continue

        media.append(
            {
                "id":
                    index,

                "image":
                    image,
            }
        )

    return media


# ==========================================================
# Attachment Options
# ==========================================================

def generate_attachment_options() -> list[dict]:

    return [
        {
            "name":
                "Photos",

            "icon":
                "photo_library",
        },
        {
            "name":
                "Camera",

            "icon":
                "photo_camera",
        },
        {
            "name":
                "Document",

            "icon":
                "description",
        },
        {
            "name":
                "Location",

            "icon":
                "location_on",
        },
        {
            "name":
                "Contact",

            "icon":
                "person",
        },
        {
            "name":
                "Poll",

            "icon":
                "poll",
        },
    ]


# ==========================================================
# Conversation Detail Actions
# ==========================================================

def generate_detail_actions() -> list[dict]:

    return [
        {
            "name":
                "Profile",

            "icon":
                "person",
        },
        {
            "name":
                "Mute",

            "icon":
                "notifications",
        },
        {
            "name":
                "Search",

            "icon":
                "search",
        },
    ]


# ==========================================================
# Conversation Detail Options
# ==========================================================

def generate_detail_options() -> list[dict]:

    return [
        {
            "name":
                "Theme",

            "icon":
                "palette",
        },
        {
            "name":
                "Privacy & support",

            "icon":
                "lock",
        },
        {
            "name":
                "Block",

            "icon":
                "block",
        },
        {
            "name":
                "Delete chat",

            "icon":
                "delete",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_messenger_state(
    conversation_count: int,
) -> dict:

    name = random.choice(
        MESSENGER_STATES
    )

    selected_conversation = (
        random.randint(
            0,
            max(
                0,
                min(
                    conversation_count - 1,
                    5,
                )
            ),
        )
    )


    search_text = ""

    if name == "search_active":

        search_text = random.choice(
            [
                "Anna",
                "John",
                "project",
                "photo",
                "meeting",
            ]
        )


    return {
        "name":
            name,

        "selected_conversation":
            selected_conversation,

        "selected_message":
            None,

        "search_text":
            search_text,
    }


# ==========================================================
# Complete Messenger Data
# ==========================================================

def generate_messenger_data() -> dict:

    conversations = (
        generate_conversations(
            count=random.randint(
                8,
                13,
            )
        )
    )


    state = (
        generate_messenger_state(
            conversation_count=len(
                conversations
            )
        )
    )


    selected_index = (
        state[
            "selected_conversation"
        ]
    )


    selected_person = (
        conversations[
            selected_index
        ]["person"]
    )


    messages = (
        generate_messages(
            person=selected_person,

            count=random.randint(
                12,
                18,
            ),
        )
    )


    if (
        state["name"]
        == "message_menu_open"
    ):

        state[
            "selected_message"
        ] = random.randint(
            0,
            max(
                0,
                min(
                    len(messages) - 1,
                    8,
                )
            ),
        )


    return {
        "conversations":
            conversations,

        "selected_person":
            selected_person,

        "messages":
            messages,

        "shared_media":
            generate_shared_media(
                count=6
            ),

        "emojis":
            generate_emojis(
                count=random.randint(
                    20,
                    32,
                )
            ),

        "attachments":
            generate_attachment_options(),

        "detail_actions":
            generate_detail_actions(),

        "detail_options":
            generate_detail_options(),

        "state":
            state,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_messenger_data()
    )

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK MESSENGER GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Conversations:",
        len(
            data[
                "conversations"
            ]
        ),
    )

    print(
        "Messages:",
        len(
            data[
                "messages"
            ]
        ),
    )

    print(
        "Emoji picker count:",
        len(
            data[
                "emojis"
            ]
        ),
    )

    print(
        "Shared media:",
        len(
            data[
                "shared_media"
            ]
        ),
    )

    print(
        "Selected person:",
        data[
            "selected_person"
        ]["name"],
    )

    print(
        "State:",
        data[
            "state"
        ],
    )


    emoji_sources = {}

    for emoji in data[
        "emojis"
    ]:

        source = (
            emoji[
                "source"
            ]
        )

        emoji_sources[
            source
        ] = (
            emoji_sources.get(
                source,
                0,
            )
            + 1
        )


    print(
        "Emoji sources:",
        emoji_sources,
    )