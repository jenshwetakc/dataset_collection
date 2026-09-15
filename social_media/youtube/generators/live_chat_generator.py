from __future__ import annotations

import random
from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
    get_random_thumbnail,
)


fake = Faker()


# ==========================================================
# Live Chat States
# ==========================================================

LIVE_CHAT_STATES = [
    "normal",
    "pinned_message",
    "super_chat",
    "members_only",
    "chat_paused",
]


# ==========================================================
# Utility
# ==========================================================

def format_count(
    value: int,
) -> str:

    if value >= 1_000_000:

        return (
            f"{value / 1_000_000:.1f}M"
            .replace(".0M", "M")
        )

    if value >= 1_000:

        return (
            f"{value / 1_000:.1f}K"
            .replace(".0K", "K")
        )

    return str(value)


def format_duration(
    seconds: int,
) -> str:

    hours = seconds // 3600

    minutes = (
        seconds % 3600
    ) // 60

    seconds = seconds % 60

    if hours:

        return (
            f"{hours}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel() -> dict[str, Any]:

    subscribers = random.randint(
        1_000,
        20_000_000,
    )

    return {
        "name": random.choice(
            [
                fake.name(),
                f"{fake.first_name()} Live",
                f"{fake.word().title()} Gaming",
                f"{fake.word().title()} Studio",
                f"{fake.word().title()} TV",
            ]
        ),

        "avatar": get_random_avatar(),

        "verified":
            random.random() < 0.40,

        "subscribers":
            subscribers,

        "subscribers_text":
            (
                f"{format_count(subscribers)} "
                f"subscribers"
            ),
    }


# ==========================================================
# Livestream
# ==========================================================

def generate_livestream() -> dict[str, Any]:

    viewers = random.randint(
        100,
        500_000,
    )

    elapsed_seconds = random.randint(
        60,
        4 * 3600,
    )

    return {
        "title":
            random.choice(
                [
                    "LIVE: Let's Build Something Together",
                    "Breaking News Live Coverage",
                    "Live Gaming Session",
                    "Late Night Live Stream",
                    "Live Q&A With Viewers",
                    "Exploring the City Live",
                    "Live Coding and Discussion",
                    "Community Livestream",
                ]
            ),

        "frame":
            get_random_thumbnail(),

        "channel":
            generate_channel(),

        "viewer_count":
            viewers,

        "viewer_count_text":
            (
                f"{format_count(viewers)} watching"
            ),

        "elapsed_seconds":
            elapsed_seconds,

        "elapsed_text":
            format_duration(
                elapsed_seconds
            ),

        "likes":
            random.randint(
                100,
                200_000,
            ),

        "likes_text":
            format_count(
                random.randint(
                    100,
                    200_000,
                )
            ),
    }


# ==========================================================
# Chat User
# ==========================================================

def generate_chat_user() -> dict[str, Any]:

    role = random.choices(
        [
            "viewer",
            "member",
            "moderator",
            "owner",
        ],
        weights=[
            78,
            12,
            7,
            3,
        ],
        k=1,
    )[0]

    return {
        "name":
            random.choice(
                [
                    fake.user_name(),
                    fake.first_name(),
                    fake.name(),
                ]
            ),

        "avatar":
            get_random_avatar(),

        "role":
            role,

        "verified":
            random.random() < 0.05,
    }


# ==========================================================
# Chat Message
# ==========================================================

def generate_chat_text() -> str:

    return random.choice(
        [
            "This is amazing!",
            "Hello everyone 👋",
            "Watching from home!",
            "That was incredible",
            "Can you explain that again?",
            "Great stream!",
            "Let's go 🔥",
            "I have been waiting for this!",
            "Thanks for the livestream",
            "This part is really interesting.",
            "What happens next?",
            "Love the content!",
            fake.sentence(
                nb_words=random.randint(
                    3,
                    12,
                )
            ),
        ]
    )


def generate_chat_message(
    index: int,
) -> dict[str, Any]:

    user = generate_chat_user()

    return {
        "id":
            f"chat_message_{index}",

        "type":
            "message",

        "user":
            user,

        "text":
            generate_chat_text(),

        "timestamp":
            random.choice(
                [
                    "Now",
                    "1 sec ago",
                    "5 sec ago",
                    "12 sec ago",
                    "30 sec ago",
                    "1 min ago",
                ]
            ),

        "liked":
            random.random() < 0.05,

        "show_more":
            random.random() < 0.30,
    }


# ==========================================================
# Super Chat
# ==========================================================

def generate_super_chat(
    index: int,
) -> dict[str, Any]:

    amount = random.choice(
        [
            "$2.00",
            "$5.00",
            "$10.00",
            "$20.00",
            "$50.00",
        ]
    )

    return {
        "id":
            f"super_chat_{index}",

        "type":
            "super_chat",

        "user":
            generate_chat_user(),

        "amount":
            amount,

        "text":
            random.choice(
                [
                    "Thanks for the stream!",
                    "Keep up the great work!",
                    "Really enjoying this!",
                    "Greetings from another country!",
                    "Amazing content!",
                ]
            ),

        "timestamp":
            "Now",
    }


# ==========================================================
# Pinned Message
# ==========================================================

def generate_pinned_message() -> dict[str, Any]:

    return {
        "enabled":
            True,

        "user":
            generate_chat_user(),

        "text":
            random.choice(
                [
                    "Welcome! Please keep the chat respectful.",
                    "Don't forget to like the livestream!",
                    "Q&A starts soon — send your questions!",
                    "Links mentioned in the stream are in the description.",
                ]
            ),

        "label":
            "Pinned by moderator",
    }


# ==========================================================
# Chat Messages
# ==========================================================

def generate_chat_messages(
    state: str,
) -> list[dict[str, Any]]:

    count = random.randint(
        16,
        28,
    )

    messages = []

    for index in range(count):

        if (
            state == "super_chat"
            and
            index == random.randint(
                3,
                min(
                    count - 1,
                    8,
                ),
            )
        ):

            messages.append(
                generate_super_chat(
                    index
                )
            )

        else:

            messages.append(
                generate_chat_message(
                    index
                )
            )

    return messages


# ==========================================================
# Chat Header
# ==========================================================

def generate_chat_header(
    state: str,
) -> dict[str, Any]:

    return {
        "title":
            "Top chat",

        "show_filter":
            True,

        "show_close":
            True,

        "show_more":
            True,

        "paused":
            state == "chat_paused",

        "pause_label":
            (
                "Chat paused"
                if state == "chat_paused"
                else None
            ),
    }


# ==========================================================
# Chat Input
# ==========================================================

def generate_chat_input(
    state: str,
) -> dict[str, Any]:

    members_only = (
        state == "members_only"
    )

    return {
        "placeholder":
            (
                "Members-only chat"
                if members_only
                else "Chat..."
            ),

        "members_only":
            members_only,

        "enabled":
            not members_only,

        "show_emoji":
            True,

        "show_send":
            True,

        "show_account":
            True,

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Video Controls
# ==========================================================

def generate_player() -> dict[str, Any]:

    return {
        "playing":
            True,

        "muted":
            random.random() < 0.15,

        "show_controls":
            True,

        "show_settings":
            True,

        "show_captions":
            True,

        "show_fullscreen":
            True,
    }


# ==========================================================
# Header
# ==========================================================

def generate_header() -> dict[str, Any]:

    return {
        "logo_text":
            "YouTube",

        "search_placeholder":
            "Search",

        "show_voice_search":
            True,

        "show_create":
            True,

        "show_notifications":
            True,

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Main Page
# ==========================================================

def generate_live_chat_page(
    state: str | None = None,
) -> dict[str, Any]:

    if state is None:

        state = random.choice(
            LIVE_CHAT_STATES
        )

    if state not in LIVE_CHAT_STATES:

        raise ValueError(
            f"Unknown live chat state: {state}. "
            f"Expected one of: {LIVE_CHAT_STATES}"
        )

    livestream = (
        generate_livestream()
    )

    return {
        "page_type":
            "live_chat",

        "state":
            state,

        "header":
            generate_header(),

        "livestream":
            livestream,

        "player":
            generate_player(),

        "chat_header":
            generate_chat_header(
                state
            ),

        "chat_messages":
            generate_chat_messages(
                state
            ),

        "pinned_message":
            (
                generate_pinned_message()
                if state == "pinned_message"
                else {
                    "enabled": False,
                }
            ),

        "chat_input":
            generate_chat_input(
                state
            ),

        "actions": {
            "like_label":
                livestream[
                    "likes_text"
                ],

            "share_label":
                "Share",

            "subscribe_label":
                random.choice(
                    [
                        "Subscribe",
                        "Subscribed",
                    ]
                ),
        },

        "layout": {
            "show_video":
                True,

            "show_chat":
                True,

            "show_video_info":
                True,

            "show_chat_input":
                True,

            "show_pinned_message":
                state
                == "pinned_message",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE LIVE CHAT"
    )

    print(
        "=========================================="
    )

    for state in LIVE_CHAT_STATES:

        page = (
            generate_live_chat_page(
                state=state
            )
        )

        print(
            "\n"
            "------------------------------------------"
        )

        print(
            "State:",
            page["state"]
        )

        print(
            "Title:",
            page["livestream"]["title"]
        )

        print(
            "Viewers:",
            page["livestream"][
                "viewer_count_text"
            ]
        )

        print(
            "Messages:",
            len(
                page["chat_messages"]
            )
        )

        print(
            "Pinned:",
            page[
                "pinned_message"
            ].get(
                "enabled",
                False,
            )
        )

        print(
            "Input enabled:",
            page[
                "chat_input"
            ]["enabled"]
        )