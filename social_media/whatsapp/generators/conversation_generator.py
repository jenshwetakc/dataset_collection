import random

from pathlib import Path

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_emoji,
    get_random_chat_image,
     get_random_avatar,
)


fake = Faker()


# ==========================================================
# Paths
# ==========================================================

# PROJECT_ROOT = (
#     Path(__file__)
#     .resolve()
#     .parents[1]
# )
#
# AVATAR_DIR = (
#     PROJECT_ROOT
#     / "assets"
#     / "avatars"
# )

# print(AVATAR_DIR)

# ==========================================================
# Utilities
# ==========================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

#
# def get_files(
#     directory: Path,
# ):
#     """
#     Return supported image files from a directory.
#     """
#
#     if not directory.exists():
#         return []
#
#     return [
#         file
#         for file in directory.iterdir()
#         if (
#             file.is_file()
#             and file.suffix.lower()
#             in IMAGE_EXTENSIONS
#         )
#     ]
#
#
# def get_random_local_image(
#     directory: Path,
# ):
#
#     files = get_files(
#         directory
#     )
#
#     if not files:
#         return None
#
#     return (
#         random.choice(files)
#         .resolve()
#         .as_uri()
#     )
#
#
# def get_random_avatar():
#
#     return get_random_local_image(
#         AVATAR_DIR
#     )


# ==========================================================
# Time
# ==========================================================

def generate_message_time():
    """
    Generate chat-style time.
    """

    return fake.time(
        pattern="%H:%M"
    )


# ==========================================================
# Text
# ==========================================================

def generate_text_message():
    """
    Generate short, medium or long chat text.
    """

    message_length = random.choices(
        [
            "short",
            "medium",
            "long",
        ],
        weights=[
            0.55,
            0.35,
            0.10,
        ],
        k=1,
    )[0]


    if message_length == "short":

        return fake.sentence(
            nb_words=random.randint(
                2,
                7,
            )
        )


    if message_length == "medium":

        return fake.sentence(
            nb_words=random.randint(
                8,
                16,
            )
        )


    return fake.text(
        max_nb_chars=random.randint(
            100,
            220,
        )
    ).replace(
        "\n",
        " "
    )


# ==========================================================
# Emoji
# ==========================================================

def generate_emoji_asset():
    """
    Return one random emoji asset from
    Noto Emoji or Twemoji.
    """

    emoji = get_random_emoji()

    if not emoji:
        return None

    if not emoji.get("uri"):
        return None

    return {
        "uri": emoji["uri"],
        "source": emoji["source"],
    }


def generate_emoji_list():
    """
    Generate 1-5 emoji assets for one emoji message.
    """

    count = random.choices(
        [
            1,
            2,
            3,
            4,
            5,
        ],
        weights=[
            0.45,
            0.25,
            0.15,
            0.10,
            0.05,
        ],
        k=1,
    )[0]

    emojis = []

    for _ in range(count):

        emoji = generate_emoji_asset()

        if emoji:
            emojis.append(
                emoji
            )

    return emojis


# ==========================================================
# Reactions
# ==========================================================

def generate_reaction():
    """
    Occasionally add an emoji reaction.

    Returns:
        None

    or:

        {
            "uri": "...",
            "source": "noto"
        }
    """

    if random.random() >= 0.12:
        return None

    return generate_emoji_asset()


# ==========================================================
# Message State
# ==========================================================

def generate_direction():

    return random.choice(
        [
            "incoming",
            "outgoing",
        ]
    )


def generate_message_status(
    direction: str,
):

    if direction == "incoming":
        return None

    return random.choices(
        [
            "sent",
            "delivered",
            "read",
        ],
        weights=[
            0.10,
            0.25,
            0.65,
        ],
        k=1,
    )[0]


# ==========================================================
# Base Message
# ==========================================================

def base_message(
    message_type: str,
):

    direction = (
        generate_direction()
    )

    return {

        "type":
            message_type,

        "direction":
            direction,

        "time":
            generate_message_time(),

        "status":
            generate_message_status(
                direction
            ),

        "forwarded":
            random.random() < 0.08,

        "reaction":
            generate_reaction(),

        "reply":
            None,
    }


# ==========================================================
# Text Message
# ==========================================================

def generate_text():

    message = base_message(
        "text"
    )

    message["text"] = (
        generate_text_message()
    )

    return message


# ==========================================================
# Emoji Message
# ==========================================================

def generate_emoji():

    message = base_message(
        "emoji"
    )

    message["emojis"] = (
        generate_emoji_list()
    )

    return message


# ==========================================================
# Image Message
# ==========================================================

def generate_image_message():

    message = base_message(
        "image"
    )

    message.update({

        "image":
            get_random_chat_image(),

        "caption":
            (
                fake.sentence(
                    nb_words=random.randint(
                        2,
                        8,
                    )
                )
                if random.random() < 0.55
                else None
            ),

    })

    return message


# ==========================================================
# URL Preview
# ==========================================================

def generate_url_message():

    message = base_message(
        "url_link"
    )

    message.update({

        "url":
            fake.url(),

        "title":
            fake.sentence(
                nb_words=random.randint(
                    3,
                    7,
                )
            ),

        "description":
            fake.sentence(
                nb_words=random.randint(
                    6,
                    14,
                )
            ),

        "preview_image":
            (
                get_random_chat_image()
                if random.random() < 0.75
                else None
            ),

    })

    return message


# ==========================================================
# Call Event
# ==========================================================

def generate_call_event():

    direction = random.choice(
        [
            "incoming",
            "outgoing",
        ]
    )

    call_type = random.choice(
        [
            "voice",
            "video",
        ]
    )

    if (
        direction == "incoming"
        and random.random() < 0.25
    ):

        call_status = "missed"

    else:

        call_status = "completed"


    duration = None

    if call_status == "completed":

        minutes = random.randint(
            0,
            59,
        )

        seconds = random.randint(
            0,
            59,
        )

        duration = (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )


    return {

        "type":
            "call",

        "direction":
            direction,

        "call_type":
            call_type,

        "call_status":
            call_status,

        "duration":
            duration,

        "time":
            generate_message_time(),

        "status":
            None,

        "forwarded":
            False,

        "reaction":
            None,

        "reply":
            None,
    }


# ==========================================================
# Voice Message
# ==========================================================

def generate_voice_message():

    message = base_message(
        "voice"
    )

    seconds = random.randint(
        2,
        180,
    )

    minutes = (
        seconds // 60
    )

    remaining_seconds = (
        seconds % 60
    )

    message.update({

        "duration":
            f"{minutes}:"
            f"{remaining_seconds:02d}",

        "played":
            random.random() < 0.6,

        "progress":
            random.uniform(
                0.1,
                0.95,
            ),

    })

    return message


# ==========================================================
# Deleted Message
# ==========================================================

def generate_deleted_message():

    message = base_message(
        "deleted"
    )

    # Deleted messages should not normally
    # receive reactions.
    message["reaction"] = None

    message["text"] = (
        "This message was deleted"
    )

    return message


# ==========================================================
# Date Separator
# ==========================================================

def generate_date_separator():

    return {

        "type":
            "date_separator",

        "text":
            random.choice(
                [
                    "Today",
                    "Yesterday",
                    fake.date(
                        pattern="%d %B %Y"
                    ),
                ]
            ),
    }


# ==========================================================
# Message Generator
# ==========================================================

MESSAGE_GENERATORS = {

    "text":
        generate_text,

    "emoji":
        generate_emoji,

    "image":
        generate_image_message,

    "url_link":
        generate_url_message,

    "call":
        generate_call_event,

    "voice":
        generate_voice_message,

    "deleted":
        generate_deleted_message,
}


MESSAGE_TYPES = [
    "text",
    "emoji",
    "image",
    "url_link",
    "call",
    "voice",
    "deleted",
]


MESSAGE_WEIGHTS = [
    0.45,   # text
    0.08,   # emoji
    0.14,   # image
    0.09,   # URL
    0.08,   # call
    0.12,   # voice
    0.04,   # deleted
]


def generate_message():

    message_type = random.choices(
        MESSAGE_TYPES,
        weights=MESSAGE_WEIGHTS,
        k=1,
    )[0]

    return MESSAGE_GENERATORS[
        message_type
    ]()


# ==========================================================
# Reply Helpers
# ==========================================================

def build_reply_preview(
    target,
):
    """
    Create simple reply text based on the
    original message type.
    """

    target_type = target.get(
        "type"
    )


    if target_type == "text":

        return {
            "type": "text",
            "text": target.get(
                "text",
                ""
            ),
            "direction": target.get(
                "direction"
            ),
        }


    if target_type == "emoji":

        return {
            "type": "emoji",
            "text": "Emoji",
            "direction": target.get(
                "direction"
            ),
        }


    if target_type == "image":

        return {
            "type": "image",
            "text": (
                target.get("caption")
                or "Photo"
            ),
            "direction": target.get(
                "direction"
            ),
        }


    if target_type == "voice":

        return {
            "type": "voice",
            "text": "Voice message",
            "direction": target.get(
                "direction"
            ),
        }


    if target_type == "url_link":

        return {
            "type": "url_link",
            "text": (
                target.get("title")
                or target.get("url")
                or "Link"
            ),
            "direction": target.get(
                "direction"
            ),
        }


    return None


# ==========================================================
# Reply Injection
# ==========================================================

def add_random_replies(
    messages,
):

    previous_messages = []

    for message in messages:

        if message.get("type") in {
            "date_separator",
            "call",
            "deleted",
        }:
            continue


        if (
            previous_messages
            and random.random() < 0.12
        ):

            valid_targets = [

                target

                for target
                in previous_messages[-5:]

                if target.get("type")
                in {
                    "text",
                    "emoji",
                    "image",
                    "voice",
                    "url_link",
                }
            ]


            if valid_targets:

                target = random.choice(
                    valid_targets
                )

                reply = (
                    build_reply_preview(
                        target
                    )
                )

                if reply:

                    message["reply"] = (
                        reply
                    )


        previous_messages.append(
            message
        )


    return messages


# ==========================================================
# Conversation Page
# ==========================================================

def generate_conversation_page(
    min_messages: int = 12,
    max_messages: int = 28,
):

    message_count = random.randint(
        min_messages,
        max_messages,
    )

    messages = []


    # Start with a date separator sometimes
    if random.random() < 0.75:

        messages.append(
            generate_date_separator()
        )


    for _ in range(
        message_count
    ):

        messages.append(
            generate_message()
        )


    messages = add_random_replies(
        messages
    )


    # Composer state
    composer_has_text = (
        random.random() < 0.25
    )


    return {

        "contact": {

            "name":
                fake.name(),

            "avatar":
                get_random_avatar(),

            "status":
                random.choice(
                    [
                        "online",
                        "last seen recently",
                        "typing…",
                    ]
                ),
        },


        "messages":
            messages,


        "composer": {

            "has_text":
                composer_has_text,

            "text":
                (
                    fake.sentence(
                        nb_words=random.randint(
                            2,
                            7,
                        )
                    )
                    if composer_has_text
                    else ""
                ),
        },
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_conversation_page()
    )

    print(
        page["contact"]
    )

    for message in page["messages"]:
        print(message)