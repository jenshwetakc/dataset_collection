from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_avatar,
    get_random_game_cover,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

FRIEND_STATES = [
    "Online",
    "Away",
    "Busy",
    "Offline",
]


GAME_ACTIVITY = [
    "In Game",
    "Playing",
    "Online",
    "In Menu",
]


MESSAGE_SNIPPETS = [
    "Are you joining tonight?",
    "That match was wild.",
    "Send me the lobby invite.",
    "I finally finished the campaign.",
    "Want to play co-op later?",
    "Check out this new update.",
    "GG!",
    "I'll be online in a few minutes.",
]


# ==========================================================
# Friend
# ==========================================================

def generate_friend() -> dict:

    state = random.choice(
        FRIEND_STATES
    )

    in_game = (
        state != "Offline"
        and random.random() < 0.55
    )

    return {

        "name":
            fake.user_name(),

        "avatar":
            get_random_avatar(),

        "state":
            state,

        "in_game":
            in_game,

        "game":
            (
                fake.catch_phrase()
                if in_game
                else None
            ),

        "activity":
            (
                random.choice(
                    GAME_ACTIVITY
                )
                if state != "Offline"
                else "Offline"
            ),

        "unread":
            (
                random.randint(
                    1,
                    8,
                )
                if random.random() < 0.28
                else 0
            ),

        "favorite":
            random.random() < 0.22,
    }


# ==========================================================
# Message
# ==========================================================

def generate_message(
    incoming: bool,
) -> dict:

    return {

        "incoming":
            incoming,

        "text":
            random.choice(
                MESSAGE_SNIPPETS
            )
            if random.random() < 0.6
            else fake.sentence(
                nb_words=random.randint(
                    4,
                    12,
                )
            ),

        "timestamp":
            random.choice([
                "10:23",
                "10:28",
                "11:02",
                "11:16",
                "12:41",
                "14:08",
                "15:17",
            ]),
    }


# ==========================================================
# Recent Chat
# ==========================================================

def generate_recent_chat(
    friend: dict,
) -> dict:

    return {

        "friend":
            friend,

        "last_message":
            random.choice(
                MESSAGE_SNIPPETS
            ),

        "timestamp":
            random.choice([
                "Now",
                "4m",
                "18m",
                "1h",
                "3h",
                "Yesterday",
            ]),

        "unread":
            friend["unread"],
    }


# ==========================================================
# Shared Game
# ==========================================================

def generate_shared_game() -> dict:

    return {

        "title":
            fake.catch_phrase(),

        "cover":
            get_random_game_cover(),

        "playtime":
            f"{random.uniform(2, 500):.1f} hrs",
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_friends_chat_data() -> dict:

    friends = [
        generate_friend()
        for _ in range(
            random.randint(
                14,
                24,
            )
        )
    ]

    online_friends = [
        friend
        for friend
        in friends
        if friend["state"] != "Offline"
    ]

    if not online_friends:

        friends[0]["state"] = "Online"
        online_friends = [
            friends[0]
        ]

    selected_friend = (
        random.choice(
            online_friends
        )
    )

    recent_friends = random.sample(
        friends,
        k=min(
            7,
            len(friends),
        ),
    )

    messages = []

    incoming = random.choice([
        True,
        False,
    ])

    for _ in range(
        random.randint(
            8,
            14,
        )
    ):

        messages.append(
            generate_message(
                incoming=incoming
            )
        )

        if random.random() < 0.68:
            incoming = not incoming

    return {

        "title":
            "Friends & Chat",

        "search_placeholder":
            "Search friends",

        "friends":
            friends,

        "selected_friend":
            selected_friend,

        "recent_chats": [
            generate_recent_chat(
                friend
            )
            for friend
            in recent_friends
        ],

        "messages":
            messages,

        "shared_games": [
            generate_shared_game()
            for _ in range(
                random.randint(
                    2,
                    4,
                )
            )
        ],

        "online_count":
            len(
                online_friends
            ),

        "total_count":
            len(
                friends
            ),
    }