# social_media/youtube/generators/watch_generator.py

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
# Content Pools
# ==========================================================

VIDEO_TOPICS = [
    "Python Tutorial for Beginners",
    "Machine Learning Explained",
    "Artificial Intelligence Explained",
    "Building a Modern Web Application",
    "Travel Vlog Around the World",
    "Street Food Tour",
    "Relaxing Music for Studying",
    "Beginner Workout Routine",
    "Technology News",
    "Computer Science Explained",
    "Photography Tips",
    "The Future of Robotics",
    "JavaScript Full Course",
    "Cybersecurity Explained",
    "Data Science Tutorial",
]


COMMENT_TEXTS = [
    "This was really helpful, thanks for explaining it so clearly.",
    "I learned a lot from this video.",
    "Great video! Looking forward to the next one.",
    "This explanation finally made sense to me.",
    "Thanks for sharing this.",
    "Really useful information.",
    "I have been looking for a video like this.",
    "The examples were very helpful.",
    "Amazing content as always.",
    "This deserves more views.",
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


def generate_duration() -> str:

    if random.random() < 0.10:

        hours = random.randint(
            1,
            4,
        )

        minutes = random.randint(
            0,
            59,
        )

        seconds = random.randint(
            0,
            59,
        )

        return (
            f"{hours}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )


    minutes = random.randint(
        1,
        59,
    )

    seconds = random.randint(
        0,
        59,
    )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


def generate_upload_time() -> str:

    return random.choice(
        [
            "10 minutes ago",
            "1 hour ago",
            "3 hours ago",
            "1 day ago",
            "2 days ago",
            "1 week ago",
            "2 weeks ago",
            "1 month ago",
            "3 months ago",
            "6 months ago",
            "1 year ago",
        ]
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel_name() -> str:

    variants = [
        fake.name(),

        (
            f"{fake.first_name()} "
            f"Tech"
        ),

        (
            f"{fake.word().title()} "
            f"Studio"
        ),

        (
            f"{fake.word().title()} "
            f"Academy"
        ),

        (
            f"The "
            f"{fake.last_name()} "
            f"Show"
        ),
    ]

    return random.choice(
        variants
    )


def generate_channel() -> dict[str, Any]:

    subscribers = random.randint(
        500,
        20_000_000,
    )

    return {

        "name":
            generate_channel_name(),

        "avatar":
            get_random_avatar(),

        "verified":
            random.random()
            < 0.30,

        "subscribers":
            subscribers,

        "subscribers_text":
            (
                f"{format_count(subscribers)} "
                f"subscribers"
            ),

        "subscribed":
            random.random()
            < 0.25,
    }


# ==========================================================
# Main Video
# ==========================================================

def generate_video_title() -> str:

    if random.random() < 0.55:

        return random.choice(
            VIDEO_TOPICS
        )

    return (
        fake.sentence(
            nb_words=random.randint(
                6,
                12,
            )
        )
        .rstrip(".")
    )


def generate_main_video() -> dict[str, Any]:

    views = random.randint(
        1_000,
        500_000_000,
    )

    likes = random.randint(
        100,
        max(
            100,
            int(
                views * 0.10
            ),
        ),
    )

    return {

        "title":
            generate_video_title(),

        # We use an offline image as the synthetic
        # player frame / video preview.
        "thumbnail":
            get_random_thumbnail(),

        "duration":
            generate_duration(),

        "views":
            views,

        "views_text":
            f"{format_count(views)} views",

        "likes":
            likes,

        "likes_text":
            format_count(
                likes
            ),

        "uploaded":
            generate_upload_time(),

        "channel":
            generate_channel(),

        "description":
            (
                fake.paragraph(
                    nb_sentences=random.randint(
                        2,
                        5,
                    )
                )
            ),
    }


# ==========================================================
# Action Buttons
# ==========================================================

def generate_actions(
    video: dict[str, Any],
) -> list[dict[str, Any]]:

    return [

        {
            "label":
                video[
                    "likes_text"
                ],

            "icon":
                "thumb_up",

            "semantic":
                "like",

            "selected":
                random.random()
                < 0.10,
        },

        {
            "label":
                "Share",

            "icon":
                "share",

            "semantic":
                "share",

            "selected":
                False,
        },

        {
            "label":
                "Download",

            "icon":
                "download",

            "semantic":
                "download",

            "selected":
                False,
        },

        {
            "label":
                "Save",

            "icon":
                "playlist_add",

            "semantic":
                "save",

            "selected":
                False,
        },
    ]


# ==========================================================
# Comments
# ==========================================================

def generate_comment(
    index: int,
) -> dict[str, Any]:

    likes = random.randint(
        0,
        20_000,
    )

    replies = random.randint(
        0,
        120,
    )

    return {

        "id":
            f"comment_{index}",

        "author":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "timestamp":
            generate_upload_time(),

        "text":
            (
                random.choice(
                    COMMENT_TEXTS
                )
                if random.random() < 0.65
                else fake.sentence(
                    nb_words=random.randint(
                        6,
                        18,
                    )
                )
            ),

        "likes":
            likes,

        "likes_text":
            (
                format_count(likes)
                if likes > 0
                else ""
            ),

        "reply_count":
            replies,

        "reply_text":
            (
                f"{replies} replies"
                if replies > 1
                else (
                    "1 reply"
                    if replies == 1
                    else ""
                )
            ),

        "creator_hearted":
            random.random()
            < 0.05,
    }


def generate_comments(
    min_comments: int = 8,
    max_comments: int = 20,
) -> dict[str, Any]:

    count = random.randint(
        min_comments,
        max_comments,
    )

    total_comments = random.randint(
        count,
        500_000,
    )

    return {

        "total":
            total_comments,

        "total_text":
            (
                f"{format_count(total_comments)} "
                f"Comments"
            ),

        "items":
            [
                generate_comment(
                    index
                )
                for index in range(
                    count
                )
            ],
    }


# ==========================================================
# Recommended Video
# ==========================================================

def generate_recommended_video(
    index: int,
) -> dict[str, Any]:

    views = random.randint(
        100,
        300_000_000,
    )

    return {

        "id":
            f"recommended_{index}",

        "title":
            generate_video_title(),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            generate_duration(),

        "channel":
            generate_channel_name(),

        "verified":
            random.random()
            < 0.20,

        "views_text":
            f"{format_count(views)} views",

        "uploaded":
            generate_upload_time(),
    }


def generate_recommendations(
    min_items: int = 12,
    max_items: int = 30,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_items,
        max_items,
    )

    return [
        generate_recommended_video(
            index
        )
        for index in range(
            count
        )
    ]


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
            random.random()
            < 0.90,

        "show_create":
            True,

        "show_notifications":
            True,

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> list[dict[str, Any]]:

    return [

        {
            "label": "Home",
            "icon": "home",
            "semantic": "home",
            "selected": False,
        },

        {
            "label": "Shorts",
            "icon": "smart_display",
            "semantic": "shorts",
            "selected": False,
        },

        {
            "label": "Subscriptions",
            "icon": "subscriptions",
            "semantic": "subscriptions",
            "selected": False,
        },

        {
            "label": "You",
            "icon": "account_circle",
            "semantic": "you",
            "selected": False,
        },

        {
            "label": "History",
            "icon": "history",
            "semantic": "history",
            "selected": False,
        },
    ]


# ==========================================================
# Bottom Navigation
# ==========================================================

def generate_bottom_navigation() -> list[dict[str, Any]]:

    return [

        {
            "label": "Home",
            "icon": "home",
            "semantic": "home",
            "selected": False,
            "create": False,
        },

        {
            "label": "Shorts",
            "icon": "smart_display",
            "semantic": "shorts",
            "selected": False,
            "create": False,
        },

        {
            "label": "",
            "icon": "add_circle",
            "semantic": "create",
            "selected": False,
            "create": True,
        },

        {
            "label": "Subscriptions",
            "icon": "subscriptions",
            "semantic": "subscriptions",
            "selected": False,
            "create": False,
        },

        {
            "label": "You",
            "icon": "account_circle",
            "semantic": "you",
            "selected": False,
            "create": False,
        },
    ]


# ==========================================================
# Watch Page
# ==========================================================

def generate_watch_page() -> dict[str, Any]:

    video = (
        generate_main_video()
    )

    return {

        "page_type":
            "watch",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "video":
            video,

        "actions":
            generate_actions(
                video
            ),

        "comments":
            generate_comments(),

        "recommendations":
            generate_recommendations(),

        "layout": {

            "show_sidebar":
                False,

            "show_comments":
                True,

            "show_recommendations":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_watch_page()
    )

    print(
        "\n=============================="
    )

    print(
        "YOUTUBE WATCH PAGE"
    )

    print(
        "=============================="
    )


    print(
        "\nTitle:",
        page["video"]["title"]
    )


    print(
        "Channel:",
        page["video"][
            "channel"
        ][
            "name"
        ]
    )


    print(
        "Views:",
        page["video"][
            "views_text"
        ]
    )


    print(
        "Comments:",
        page["comments"][
            "total_text"
        ]
    )


    print(
        "Recommendations:",
        len(
            page[
                "recommendations"
            ]
        )
    )