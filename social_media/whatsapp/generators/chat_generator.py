import random
from pathlib import Path

from faker import Faker


fake = Faker()



# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)


# ==========================================================
# Asset Paths
# ==========================================================

AVATAR_DIR = (
    PROJECT_ROOT
    / "assets"
    / "avatars"
)





# ==========================================================
# Avatar Generator
# ==========================================================

def get_avatar_files():

    if not AVATAR_DIR.exists():
        return []

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    return [
        path
        for path in AVATAR_DIR.iterdir()
        if path.suffix.lower() in extensions
    ]


def get_random_avatar() -> str | None:

    avatars = get_avatar_files()

    if not avatars:
        return None

    avatar = random.choice(
        avatars
    )

    return avatar.resolve().as_uri()


# ==========================================================
# Message Generator
# ==========================================================

def generate_message() -> str:
    """
    Generate a short fake chat message.
    """

    message_type = random.choices(
        [
            "short",
            "medium",
        ],
        weights=[
            0.75,
            0.25,
        ],
        k=1,
    )[0]

    if message_type == "short":

        return fake.sentence(
            nb_words=random.randint(
                2,
                7,
            )
        )

    return fake.text(
        max_nb_chars=random.randint(
            25,
            60,
        )
    ).replace(
        "\n",
        " "
    )


# ==========================================================
# Time Generator
# ==========================================================

def generate_time() -> str:

    possibilities = [
        fake.time(
            pattern="%H:%M"
        ),
        "Yesterday",
        fake.day_of_week(),
    ]

    return random.choice(
        possibilities
    )


# ==========================================================
# Single Chat
# ==========================================================

def generate_chat():

    unread = random.choices(
        population=[
            0,
            random.randint(1, 9),
        ],
        weights=[
            0.70,
            0.30,
        ],
        k=1,
    )[0]

    return {

        "name":
            fake.name(),

        "message":
            generate_message(),

        "time":
            generate_time(),

        "avatar":
            get_random_avatar(),

        "unread":
            unread,

        "muted":
            random.random() < 0.15,

        "pinned":
            random.random() < 0.12,

        "read":
            random.random() < 0.65,
    }


# ==========================================================
# Chat Page Generator
# ==========================================================

def generate_chat_page(
    min_chats: int = 8,
    max_chats: int = 16,
):

    count = random.randint(
        min_chats,
        max_chats,
    )

    chats = [
        generate_chat()
        for _ in range(count)
    ]

    return {
        "chats": chats,

        "selected_filter":
            random.choice(
                [
                    "all",
                    "unread",
                    "favorites",
                    "groups",
                ]
            ),
    }

def generate_system_status():
    return {
        "time": fake.time(
            pattern="%H:%M"
        ),
        "wifi": random.choice([
            True,
            True,
            True,
            False,
        ]),
        "signal_level": random.randint(1, 4),
        "battery": random.randint(10, 100),
        "charging": random.random() < 0.15,
    }

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = generate_chat_page()

    for chat in page["chats"]:
        print(chat)