import random
from pathlib import Path

from faker import Faker
from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
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


# ==========================================================
# Local Avatar Utilities
# ==========================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# def get_files(
#     directory: Path,
# ):
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
# def get_random_avatar():
#
#     files = get_files(
#         AVATAR_DIR
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


# ==========================================================
# Relative Times
# ==========================================================

def generate_relative_time():

    choice = random.choices(
        [
            "minutes",
            "hours",
            "yesterday",
        ],
        weights=[
            0.45,
            0.40,
            0.15,
        ],
        k=1,
    )[0]

    if choice == "minutes":

        return (
            f"{random.randint(1, 59)} "
            f"minutes ago"
        )

    if choice == "hours":

        value = random.randint(
            1,
            12,
        )

        return (
            f"{value} "
            f"{'hour' if value == 1 else 'hours'} ago"
        )

    return "Yesterday"


# ==========================================================
# Status Item
# ==========================================================

def generate_status_item(
    viewed=None,
):

    if viewed is None:

        viewed = random.random() < 0.35

    return {

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "time":
            generate_relative_time(),

        "viewed":
            viewed,

        # Number of pieces in the story/status ring.
        "segments":
            random.randint(
                1,
                6,
            ),
    }


# ==========================================================
# My Status
# ==========================================================

def generate_my_status():

    has_status = (
        random.random() < 0.55
    )

    return {

        "avatar":
            get_random_avatar(),

        "has_status":
            has_status,

        "time":
            (
                generate_relative_time()
                if has_status
                else None
            ),

        "segments":
            (
                random.randint(
                    1,
                    5,
                )
                if has_status
                else 0
            ),

        "label":
            (
                "Tap to add status update"
                if not has_status
                else generate_relative_time()
            ),
    }


# ==========================================================
# Channel Message Text
# ==========================================================

def generate_channel_message():

    message_type = random.choices(
        [
            "short",
            "medium",
        ],
        weights=[
            0.65,
            0.35,
        ],
        k=1,
    )[0]

    if message_type == "short":

        return fake.sentence(
            nb_words=random.randint(
                3,
                8,
            )
        )

    return fake.sentence(
        nb_words=random.randint(
            8,
            16,
        )
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel():

    unread = random.choices(
        [
            0,
            random.randint(1, 9),
            random.randint(10, 99),
        ],
        weights=[
            0.55,
            0.35,
            0.10,
        ],
        k=1,
    )[0]

    has_thumbnail = (
        random.random() < 0.35
    )

    return {

        "name":
            fake.company(),

        "avatar":
            get_random_avatar(),

        "message":
            generate_channel_message(),

        "time":
            fake.time(
                pattern="%H:%M"
            ),

        "verified":
            random.random() < 0.35,

        "unread":
            unread,

        "following":
            True,

        "thumbnail":
            (
                get_random_chat_image()
                if has_thumbnail
                else None
            ),
    }


# ==========================================================
# Suggested Channel
# ==========================================================

def generate_suggested_channel():

    follower_count = random.choice(
        [
            f"{random.randint(1, 999)}K followers",
            f"{random.uniform(1.0, 9.9):.1f}M followers",
            f"{random.randint(10, 999)} followers",
        ]
    )

    return {

        "name":
            fake.company(),

        "avatar":
            get_random_avatar(),

        "followers":
            follower_count,

        "verified":
            random.random() < 0.30,

        "following":
            random.random() < 0.15,
    }


# ==========================================================
# Updates Page
# ==========================================================

def generate_updates_page(
    min_recent: int = 3,
    max_recent: int = 8,
    min_viewed: int = 1,
    max_viewed: int = 5,
    min_channels: int = 2,
    max_channels: int = 6,
    min_suggested: int = 3,
    max_suggested: int = 6,
):

    recent_count = random.randint(
        min_recent,
        max_recent,
    )

    viewed_count = random.randint(
        min_viewed,
        max_viewed,
    )

    channel_count = random.randint(
        min_channels,
        max_channels,
    )

    suggested_count = random.randint(
        min_suggested,
        max_suggested,
    )


    recent_updates = [
        generate_status_item(
            viewed=False
        )
        for _ in range(
            recent_count
        )
    ]


    viewed_updates = [
        generate_status_item(
            viewed=True
        )
        for _ in range(
            viewed_count
        )
    ]


    channels = [
        generate_channel()
        for _ in range(
            channel_count
        )
    ]


    suggested_channels = [
        generate_suggested_channel()
        for _ in range(
            suggested_count
        )
    ]


    return {

        "title":
            "Updates",

        "my_status":
            generate_my_status(),

        "recent_updates":
            recent_updates,

        "viewed_updates":
            viewed_updates,

        "channels":
            channels,

        "suggested_channels":
            suggested_channels,

        "show_viewed":
            bool(
                viewed_updates
            ),

        "show_channels":
            bool(
                channels
            ),

        "show_suggested_channels":
            bool(
                suggested_channels
            ),

        # Selected bottom navigation item.
        "selected_navigation":
            "updates",

        # Can later control FAB states.
        "fab": {

            "show_text_status":
                True,

            "show_camera_status":
                True,
        },
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = generate_updates_page()

    print(
        "\nMY STATUS"
    )

    print(
        page["my_status"]
    )


    print(
        "\nRECENT"
    )

    for item in page[
        "recent_updates"
    ]:

        print(item)


    print(
        "\nVIEWED"
    )

    for item in page[
        "viewed_updates"
    ]:

        print(item)


    print(
        "\nCHANNELS"
    )

    for channel in page[
        "channels"
    ]:

        print(channel)


    print(
        "\nSUGGESTED"
    )

    for channel in page[
        "suggested_channels"
    ]:

        print(channel)