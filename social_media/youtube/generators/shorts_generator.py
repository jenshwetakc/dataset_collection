from __future__ import annotations

import random

from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
    get_random_short_image,
)


fake = Faker()


# ==========================================================
# Content Pools
# ==========================================================

SHORT_TOPICS = [
    "You need to try this!",
    "This changed everything",
    "Wait for the ending",
    "Quick tutorial",
    "Did you know this?",
    "Amazing trick",
    "One minute challenge",
    "Best moment today",
    "You won't believe this",
    "Easy tip for beginners",
    "Watch this before you start",
    "This is actually useful",
    "A simple way to do it",
    "The result is incredible",
    "POV: you finally figured it out",
]


HASHTAGS = [
    "#shorts",
    "#viral",
    "#trending",
    "#tutorial",
    "#funny",
    "#tech",
    "#travel",
    "#food",
    "#music",
    "#gaming",
    "#learn",
    "#tips",
    "#lifehack",
]


AUDIO_TITLES = [
    "Original sound",
    "Trending audio",
    "Summer vibes",
    "Late night mix",
    "Original audio",
    "Daily moments",
    "Good vibes",
    "Popular sound",
]


# ==========================================================
# Utility
# ==========================================================

def format_count(
    value: int,
) -> str:

    if value >= 1_000_000_000:

        result = (
            value / 1_000_000_000
        )

        return (
            f"{result:.1f}B"
            .replace(
                ".0B",
                "B",
            )
        )


    if value >= 1_000_000:

        result = (
            value / 1_000_000
        )

        return (
            f"{result:.1f}M"
            .replace(
                ".0M",
                "M",
            )
        )


    if value >= 1_000:

        result = (
            value / 1_000
        )

        return (
            f"{result:.1f}K"
            .replace(
                ".0K",
                "K",
            )
        )


    return str(
        value
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel_name() -> str:

    variants = [

        fake.user_name(),

        fake.first_name(),

        (
            f"{fake.first_name()} "
            f"Official"
        ),

        (
            f"{fake.word().title()} "
            f"Studio"
        ),

        (
            f"{fake.word().title()} "
            f"Daily"
        ),
    ]


    return random.choice(
        variants
    )


def generate_channel() -> dict[str, Any]:

    return {

        "name":
            generate_channel_name(),

        "avatar":
            get_random_avatar(),

        "verified":
            random.random()
            < 0.20,

        "subscribed":
            random.random()
            < 0.18,
    }


# ==========================================================
# Caption
# ==========================================================

def generate_caption() -> str:

    topic = random.choice(
        SHORT_TOPICS
    )


    hashtag_count = random.randint(
        1,
        4,
    )


    hashtags = random.sample(
        HASHTAGS,
        hashtag_count,
    )


    if random.random() < 0.35:

        extra = (
            fake.sentence(
                nb_words=random.randint(
                    4,
                    9,
                )
            )
            .rstrip(".")
        )

        return (
            f"{topic} {extra} "
            f"{' '.join(hashtags)}"
        )


    return (
        f"{topic} "
        f"{' '.join(hashtags)}"
    )


# ==========================================================
# Audio
# ==========================================================

def generate_audio(
    channel_name: str,
) -> dict[str, Any]:

    if random.random() < 0.55:

        title = (
            f"Original sound - "
            f"{channel_name}"
        )

    else:

        title = random.choice(
            AUDIO_TITLES
        )


    return {

        "title":
            title,

        "icon":
            "music_note",
    }


# ==========================================================
# Short
# ==========================================================

def generate_short(
    index: int,
) -> dict[str, Any]:

    channel = (
        generate_channel()
    )


    likes = random.randint(
        0,
        10_000_000,
    )


    comments = random.randint(
        0,
        500_000,
    )


    shares = random.randint(
        0,
        200_000,
    )


    return {

        "id":
            f"short_{index}",

        "image":
            get_random_short_image(),

        "channel":
            channel,

        "caption":
            generate_caption(),

        "audio":
            generate_audio(
                channel["name"]
            ),

        "likes":
            likes,

        "likes_text":
            format_count(
                likes
            ),

        "comments":
            comments,

        "comments_text":
            format_count(
                comments
            ),

        "shares":
            shares,

        "shares_text":
            format_count(
                shares
            ),

        "liked":
            random.random()
            < 0.10,

        "disliked":
            False,

        "show_remix":
            random.random()
            < 0.65,
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

        "show_create":
            True,

        "show_notifications":
            True,

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Sidebar Navigation
# ==========================================================

def generate_navigation() -> list[dict[str, Any]]:

    return [

        {
            "label":
                "Home",

            "icon":
                "home",

            "semantic":
                "home",

            "selected":
                False,
        },

        {
            "label":
                "Shorts",

            "icon":
                "smart_display",

            "semantic":
                "shorts",

            "selected":
                True,
        },

        {
            "label":
                "Subscriptions",

            "icon":
                "subscriptions",

            "semantic":
                "subscriptions",

            "selected":
                False,
        },

        {
            "label":
                "You",

            "icon":
                "account_circle",

            "semantic":
                "you",

            "selected":
                False,
        },

        {
            "label":
                "History",

            "icon":
                "history",

            "semantic":
                "history",

            "selected":
                False,
        },
    ]


# ==========================================================
# Bottom Navigation
# ==========================================================

def generate_bottom_navigation() -> list[dict[str, Any]]:

    return [

        {
            "label":
                "Home",

            "icon":
                "home",

            "semantic":
                "home",

            "selected":
                False,

            "create":
                False,
        },

        {
            "label":
                "Shorts",

            "icon":
                "smart_display",

            "semantic":
                "shorts",

            "selected":
                True,

            "create":
                False,
        },

        {
            "label":
                "",

            "icon":
                "add_circle",

            "semantic":
                "create",

            "selected":
                False,

            "create":
                True,
        },

        {
            "label":
                "Subscriptions",

            "icon":
                "subscriptions",

            "semantic":
                "subscriptions",

            "selected":
                False,

            "create":
                False,
        },

        {
            "label":
                "You",

            "icon":
                "account_circle",

            "semantic":
                "you",

            "selected":
                False,

            "create":
                False,
        },
    ]


# ==========================================================
# Shorts Page
# ==========================================================

def generate_shorts_page(
    min_shorts: int = 8,
    max_shorts: int = 16,
) -> dict[str, Any]:

    count = random.randint(
        min_shorts,
        max_shorts,
    )


    shorts = [

        generate_short(
            index
        )

        for index in range(
            count
        )
    ]


    return {

        "page_type":
            "shorts",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "shorts":
            shorts,

        "layout": {

            "show_sidebar":
                True,

            "show_bottom_navigation":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_shorts_page(
            min_shorts=4,
            max_shorts=4,
        )
    )


    print(
        "\n"
        "=============================="
    )

    print(
        "YOUTUBE SHORTS"
    )

    print(
        "=============================="
    )


    print(
        "Shorts:",
        len(
            page["shorts"]
        )
    )


    for short in page["shorts"]:

        print(
            "\n------------------------------"
        )

        print(
            "Channel:",
            short["channel"]["name"]
        )

        print(
            "Caption:",
            short["caption"]
        )

        print(
            "Likes:",
            short["likes_text"]
        )

        print(
            "Comments:",
            short["comments_text"]
        )

        print(
            "Image:",
            bool(
                short["image"]
            )
        )