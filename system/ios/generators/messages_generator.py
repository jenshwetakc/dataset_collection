from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

MESSAGES_STATES = [

    "conversation_list",

    "chat_thread",

    "typing",

    "message_reactions",

    "message_info",

    "attachment_sheet",

    "new_message",

    "delete_confirmation",
]


MESSAGES_STATE_WEIGHTS = [

    22,

    24,

    12,

    10,

    8,

    10,

    8,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Person
# ==========================================================

def generate_person(
    index: int,
) -> dict:

    name = fake.name()

    initials = "".join(
        part[0]
        for part in name.split()[:2]
    ).upper()


    return {

        "id":
            f"person_{index}",

        "name":
            name,

        "initials":
            initials,

        "phone":
            fake.numerify(
                "010-####-####"
            ),

        "online":
            random.random() < 0.35,
    }


# ==========================================================
# Conversations
# ==========================================================

def generate_conversations(
    count: int = 10,
) -> list[dict]:

    people = [

        generate_person(
            index
        )

        for index
        in range(
            count
        )
    ]


    previews = [

        "Sounds good!",

        "Are you free later?",

        "I sent the updated file.",

        "See you tomorrow.",

        "Thank you!",

        "Can you check this?",

        "Let's meet at 4.",

        "That works for me.",

        "I'll call you later.",

        "Got it 👍",
    ]


    conversations = []


    for index, person in enumerate(
        people
    ):

        conversations.append({

            "id":
                f"conversation_{index}",

            "person":
                person,

            "preview":
                random.choice(
                    previews
                ),

            "time":
                random.choice([
                    "9:41 AM",
                    "10:18 AM",
                    "11:03 AM",
                    "1:42 PM",
                    "Yesterday",
                    "Friday",
                    "Thursday",
                ]),

            "unread":
                random.random() < 0.32,

            "muted":
                random.random() < 0.12,
        })


    return conversations


# ==========================================================
# Messages
# ==========================================================

def generate_messages(
    count: int = 14,
) -> list[dict]:

    texts = [

        "Hey!",

        "How are you?",

        "I'm doing well.",

        "Did you see the latest update?",

        "Yes, I checked it.",

        "Looks good to me.",

        "Can you send me the screenshot?",

        "Sure, sending it now.",

        "Thanks!",

        "No problem.",

        "Let's discuss this tomorrow.",

        "Sounds good.",

        "See you then.",

        "Okay 👍",
    ]


    messages = []


    for index in range(
        count
    ):

        outgoing = (
            random.random()
            < 0.52
        )


        messages.append({

            "id":
                f"message_{index}",

            "text":
                random.choice(
                    texts
                ),

            "outgoing":
                outgoing,

            "time":
                random.choice([
                    "9:41 AM",
                    "9:43 AM",
                    "9:45 AM",
                    "10:01 AM",
                    "10:12 AM",
                ]),

            "delivered":
                outgoing
                and random.random() < 0.85,

            "read":
                outgoing
                and random.random() < 0.45,

            "reaction":
                (
                    random.choice([
                        "heart",
                        "thumbs_up",
                        "laugh",
                    ])
                    if random.random() < 0.18
                    else None
                ),
        })


    return messages


# ==========================================================
# Reactions
# ==========================================================

def generate_reactions() -> list[dict]:

    return [

        {
            "id":
                "heart",

            "label":
                "Love",

            "symbol":
                "♥",
        },

        {
            "id":
                "thumbs_up",

            "label":
                "Like",

            "symbol":
                "👍",
        },

        {
            "id":
                "thumbs_down",

            "label":
                "Dislike",

            "symbol":
                "👎",
        },

        {
            "id":
                "laugh",

            "label":
                "Laugh",

            "symbol":
                "😂",
        },

        {
            "id":
                "emphasis",

            "label":
                "Emphasize",

            "symbol":
                "‼",
        },

        {
            "id":
                "question",

            "label":
                "Question",

            "symbol":
                "?",
        },
    ]


# ==========================================================
# Attachment Sheet
# ==========================================================

def generate_attachment_sheet() -> dict:

    return {

        "items": [

            {
                "id":
                    "camera",

                "title":
                    "Camera",

                "icon":
                    resolve_icon(
                        "camera"
                    ),
            },

            {
                "id":
                    "photos",

                "title":
                    "Photos",

                "icon":
                    resolve_icon(
                        "image",
                        "image"
                    ),
            },

            {
                "id":
                    "location",

                "title":
                    "Location",

                "icon":
                    resolve_icon(
                        "location",
                        "map-pin"
                    ),
            },

            {
                "id":
                    "contact",

                "title":
                    "Contact",

                "icon":
                    get_lucide_icon(
                        "contact"
                    ),
            },

            {
                "id":
                    "document",

                "title":
                    "Document",

                "icon":
                    get_lucide_icon(
                        "file-text"
                    ),
            },
        ],
    }


# ==========================================================
# Message Info
# ==========================================================

def generate_message_info(
    message: dict,
) -> dict:

    return {

        "message":
            message,

        "sent":
            "Today, 9:41 AM",

        "delivered":
            "Today, 9:41 AM",

        "read":
            (
                "Today, 9:43 AM"
                if message["read"]
                else "Not Read"
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_messages_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            MESSAGES_STATES,

            weights=
                MESSAGES_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in MESSAGES_STATES:

        raise ValueError(
            f"Unknown Messages state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Data
    # ======================================================

    conversations = (
        generate_conversations()
    )


    active_conversation = (
        random.choice(
            conversations
        )
    )


    messages = (
        generate_messages()
    )


    active_message = (
        random.choice(
            messages
        )
    )


    # ======================================================
    # Overlay
    # ======================================================

    is_overlay_state = (
        state
        in {
            "message_reactions",
            "message_info",
            "attachment_sheet",
            "delete_confirmation",
        }
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,

        "title":
            "Messages",


        # --------------------------------------------------
        # Conversations
        # --------------------------------------------------

        "conversations":
            conversations,

        "active_conversation":
            active_conversation,


        # --------------------------------------------------
        # Messages
        # --------------------------------------------------

        "messages":
            messages,

        "active_message":
            active_message,


        # --------------------------------------------------
        # Reactions
        # --------------------------------------------------

        "reactions":
            generate_reactions(),


        # --------------------------------------------------
        # Info
        # --------------------------------------------------

        "message_info":
            generate_message_info(
                active_message
            ),


        # --------------------------------------------------
        # Attachment
        # --------------------------------------------------

        "attachment_sheet":
            generate_attachment_sheet(),


        # --------------------------------------------------
        # Delete
        # --------------------------------------------------

        "delete_confirmation": {

            "title":
                "Delete Message?",

            "message":
                (
                    "This message will be deleted "
                    "from this conversation."
                ),

            "cancel":
                "Cancel",

            "confirm":
                "Delete",
        },


        # --------------------------------------------------
        # New Message
        # --------------------------------------------------

        "new_message": {

            "recipient":
                random.choice([
                    "",
                    fake.name(),
                    fake.numerify(
                        "010-####-####"
                    ),
                ]),

            "draft":
                random.choice([
                    "",
                    "Hi!",
                    "Are you available?",
                    "Can we talk later?",
                ]),
        },


        # --------------------------------------------------
        # Icons
        # --------------------------------------------------

        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "compose":
                get_lucide_icon(
                    "square-pen"
                ),

            "back":
                resolve_icon(
                    "back"
                ),

            "info":
                resolve_icon(
                    "info"
                ),

            "phone":
                resolve_icon(
                    "phone"
                ),

            "video":
                get_lucide_icon(
                    "video"
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "send":
                get_lucide_icon(
                    "arrow-up"
                ),

            "camera":
                resolve_icon(
                    "camera"
                ),

            "mic":
                get_lucide_icon(
                    "mic"
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right"
                ),

            "message":
                resolve_icon(
                    "message",
                    "message-circle"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in MESSAGES_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_messages_data(
                state=
                    state
            ),

            sort_dicts=False,
        )