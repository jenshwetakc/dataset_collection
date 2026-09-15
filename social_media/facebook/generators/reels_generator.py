# social_media/facebook/generators/reels_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_post_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

REELS_STATES = [
    "default",
    "default",
    "comments_open",
    "share_sheet",
    "reaction_picker",
    "more_menu",
    "creator_preview",
    "paused",
]


CAPTIONS = [
    "A little moment from today.",
    "Weekend vibes.",
    "This made my day.",
    "Exploring something new.",
    "One of my favorite places.",
    "Good memories.",
    "A perfect afternoon.",
    "Just sharing this moment.",
]


MUSIC_NAMES = [
    "Original audio",
    "Morning Light",
    "Weekend Mood",
    "City Nights",
    "Summer Memories",
    "Soft Horizon",
]


# ==========================================================
# Reel
# ==========================================================

def generate_reel(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "creator":
            fake.name(),

        "username":
            fake.user_name(),

        "avatar":
            get_random_avatar(),

        "thumbnail":
            get_random_post_image(),

        # For synthetic HTML we can visually use an image
        # inside a video-like region if no local video assets
        # are currently available.
        "video_poster":
            get_random_post_image(),

        "caption":
            random.choice(
                CAPTIONS
            ),

        "music":
            random.choice(
                MUSIC_NAMES
            ),

        "likes":
            random.randint(
                10,
                95000,
            ),

        "comments":
            random.randint(
                0,
                8500,
            ),

        "shares":
            random.randint(
                0,
                3200,
            ),

        "following":
            random.random() < 0.45,
    }


def generate_reels(
    count: int = 6,
) -> list[dict]:

    return [
        generate_reel(index)
        for index in range(count)
    ]


# ==========================================================
# Comment
# ==========================================================

def generate_comment(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "text":
            random.choice(
                [
                    "Love this!",
                    "Amazing!",
                    "This looks great.",
                    "So good!",
                    "Beautiful moment.",
                    "Where is this?",
                    "This made me smile.",
                ]
            ),

        "timestamp":
            random.choice(
                [
                    "1m",
                    "4m",
                    "8m",
                    "20m",
                    "1h",
                ]
            ),

        "likes":
            random.randint(
                0,
                320,
            ),
    }


def generate_comments(
    count: int = 6,
) -> list[dict]:

    return [
        generate_comment(index)
        for index in range(count)
    ]


# ==========================================================
# Share Targets
# ==========================================================

def generate_share_targets(
    count: int = 8,
) -> list[dict]:

    return [
        {
            "id":
                index,

            "name":
                fake.first_name(),

            "avatar":
                get_random_avatar(),
        }
        for index in range(count)
    ]


# ==========================================================
# State
# ==========================================================

def generate_reels_state(
    reel_count: int,
) -> dict:

    name = random.choice(
        REELS_STATES
    )

    selected_reel = random.randint(
        0,
        max(
            0,
            reel_count - 1,
        ),
    )

    return {
        "name":
            name,

        "selected_reel":
            selected_reel,
    }


# ==========================================================
# Complete Data
# ==========================================================

def generate_reels_data() -> dict:

    reels = generate_reels(
        count=random.randint(
            5,
            8,
        )
    )

    return {
        "reels":
            reels,

        "comments":
            generate_comments(
                count=random.randint(
                    5,
                    8,
                )
            ),

        "share_targets":
            generate_share_targets(
                count=random.randint(
                    6,
                    10,
                )
            ),

        "state":
            generate_reels_state(
                reel_count=len(
                    reels
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_reels_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK REELS GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Reels:",
        len(
            data["reels"]
        ),
    )

    print(
        "Comments:",
        len(
            data["comments"]
        ),
    )

    print(
        "Share targets:",
        len(
            data["share_targets"]
        ),
    )

    print(
        "State:",
        data["state"],
    )