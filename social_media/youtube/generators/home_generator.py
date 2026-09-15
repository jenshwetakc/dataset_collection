# social_media/youtube/generators/home_generator.py

from __future__ import annotations

import random

from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
    get_random_thumbnail,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Content Pools
# ==========================================================

VIDEO_TOPICS = [
    "Python Tutorial for Beginners",
    "Machine Learning Explained",
    "Building a Modern Web Application",
    "Artificial Intelligence Explained",
    "Top Programming Tips",
    "A Day in My Life",
    "Street Food Around the World",
    "Easy Dinner Recipes",
    "Morning Workout Routine",
    "Relaxing Music for Studying",
    "Latest Technology News",
    "Amazing Places You Need to Visit",
    "Photography Tips for Beginners",
    "Understanding Computer Science",
    "Learn JavaScript in One Hour",
    "The Future of Robotics",
    "Beginner Guitar Lesson",
    "Productivity Tips That Actually Work",
    "Top Games You Should Play",
    "Beautiful Nature Documentary",
]


TITLE_SUFFIXES = [
    "Full Guide",
    "Complete Tutorial",
    "2026",
    "Step by Step",
    "Episode 1",
    "Explained",
    "Beginner Guide",
    "Everything You Need to Know",
]


CHANNEL_SUFFIXES = [
    "TV",
    "Tech",
    "Studio",
    "Media",
    "Academy",
    "Daily",
    "Official",
    "Labs",
    "World",
]


CATEGORIES = [
    "All",
    "Music",
    "Gaming",
    "Live",
    "News",
    "Mixes",
    "Programming",
    "Computer Science",
    "Artificial Intelligence",
    "Cooking",
    "Travel",
    "Sports",
    "Comedy",
    "Podcasts",
    "Recently uploaded",
    "Watched",
    "New to you",
]


# ==========================================================
# View Count
# ==========================================================

def format_count(
    value: int,
) -> str:

    if value >= 1_000_000_000:

        count = (
            value
            / 1_000_000_000
        )

        text = (
            f"{count:.1f}B"
        )

        return text.replace(
            ".0B",
            "B",
        )


    if value >= 1_000_000:

        count = (
            value
            / 1_000_000
        )

        text = (
            f"{count:.1f}M"
        )

        return text.replace(
            ".0M",
            "M",
        )


    if value >= 1_000:

        count = (
            value
            / 1_000
        )

        text = (
            f"{count:.1f}K"
        )

        return text.replace(
            ".0K",
            "K",
        )


    return str(value)


# ==========================================================
# Upload Time
# ==========================================================

def generate_upload_time() -> str:

    return random.choice(
        [
            "5 minutes ago",
            "12 minutes ago",
            "30 minutes ago",
            "1 hour ago",
            "2 hours ago",
            "5 hours ago",
            "8 hours ago",
            "12 hours ago",
            "1 day ago",
            "2 days ago",
            "3 days ago",
            "5 days ago",
            "1 week ago",
            "2 weeks ago",
            "3 weeks ago",
            "1 month ago",
            "2 months ago",
            "4 months ago",
            "8 months ago",
            "1 year ago",
            "2 years ago",
            "3 years ago",
        ]
    )


# ==========================================================
# Duration
# ==========================================================

def generate_duration() -> str:

    # ------------------------------------------------------
    # Occasionally generate long-form videos
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Normal video
    # ------------------------------------------------------

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


# ==========================================================
# Video Title
# ==========================================================

def generate_video_title() -> str:

    style = random.random()


    # ------------------------------------------------------
    # Curated title
    # ------------------------------------------------------

    if style < 0.45:

        return random.choice(
            VIDEO_TOPICS
        )


    # ------------------------------------------------------
    # Faker title
    # ------------------------------------------------------

    if style < 0.75:

        return (
            fake.sentence(
                nb_words=random.randint(
                    5,
                    11,
                )
            )
            .rstrip(".")
        )


    # ------------------------------------------------------
    # Topic + suffix
    # ------------------------------------------------------

    return (
        f"{random.choice(VIDEO_TOPICS)} "
        f"| {random.choice(TITLE_SUFFIXES)}"
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel_name() -> str:

    style = random.random()


    if style < 0.30:

        return (
            f"{fake.first_name()} "
            f"{random.choice(CHANNEL_SUFFIXES)}"
        )


    if style < 0.55:

        return (
            f"{fake.word().title()} "
            f"{random.choice(CHANNEL_SUFFIXES)}"
        )


    if style < 0.75:

        return (
            f"The "
            f"{fake.last_name()} "
            f"Show"
        )


    if style < 0.90:

        return fake.name()


    return (
        f"{fake.city()} "
        f"{random.choice(CHANNEL_SUFFIXES)}"
    )


def generate_channel() -> dict[str, Any]:

    return {

        "name":
            generate_channel_name(),

        "avatar":
            get_random_avatar(),

        "verified":
            random.random()
            < 0.25,
    }


# ==========================================================
# Normal Video
# ==========================================================

def generate_video(
    video_index: int,
) -> dict[str, Any]:

    views = random.randint(
        50,
        300_000_000,
    )


    return {

        "id":
            f"video_{video_index}",

        "title":
            generate_video_title(),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            generate_duration(),

        "channel":
            generate_channel(),

        "views":
            views,

        "views_text":
            f"{format_count(views)} views",

        "uploaded":
            generate_upload_time(),

        "live":
            False,

        "new":
            random.random()
            < 0.12,
    }


# ==========================================================
# Live Video
# ==========================================================

def generate_live_video(
    video_index: int,
) -> dict[str, Any]:

    viewers = random.randint(
        100,
        250_000,
    )


    return {

        "id":
            f"video_{video_index}",

        "title":
            generate_video_title(),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            None,

        "channel":
            generate_channel(),

        "views":
            viewers,

        "views_text":
            (
                f"{format_count(viewers)} "
                f"watching"
            ),

        "uploaded":
            None,

        "live":
            True,

        "new":
            False,
    }


# ==========================================================
# Categories
# ==========================================================

def generate_categories() -> list[dict[str, Any]]:

    count = random.randint(
        8,
        min(
            14,
            len(CATEGORIES),
        ),
    )


    categories = random.sample(
        CATEGORIES[1:],
        count - 1,
    )


    categories.insert(
        0,
        "All",
    )


    # Usually one of the first few chips is active.
    selected_index = random.randint(
        0,
        min(
            3,
            len(categories) - 1,
        ),
    )


    return [

        {
            "label":
                label,

            "selected":
                index
                == selected_index,
        }

        for index, label
        in enumerate(categories)
    ]


# ==========================================================
# Sidebar Navigation
# ==========================================================

def generate_navigation() -> list[dict[str, Any]]:

    return [

        {
            "label": "Home",
            "icon": "home",
            "semantic": "home",
            "selected": True,
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
# Mobile Bottom Navigation
# ==========================================================

def generate_bottom_navigation() -> list[dict[str, Any]]:

    return [

        {
            "label": "Home",
            "icon": "home",
            "semantic": "home",
            "selected": True,
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
# Header
# ==========================================================

def generate_header() -> dict[str, Any]:

    return {

        "logo_text":
            "YouTube",

        "search_placeholder":
            random.choice(
                [
                    "Search",
                    "Search videos",
                    "Search YouTube",
                ]
            ),

        "show_voice_search":
            random.random()
            < 0.90,

        "show_create":
            random.random()
            < 0.95,

        "show_notifications":
            True,

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Layout Options
# ==========================================================

def generate_layout() -> dict[str, Any]:

    return {

        "show_sidebar":
            True,

        "show_categories":
            random.random()
            < 0.95,
    }


# ==========================================================
# Complete Home Page
# ==========================================================

def generate_home_page(
    min_videos: int = 14,
    max_videos: int = 30,
) -> dict[str, Any]:

    video_count = random.randint(
        min_videos,
        max_videos,
    )


    videos = []


    for video_index in range(
        video_count
    ):

        # --------------------------------------------------
        # Small percentage of live content
        # --------------------------------------------------

        if random.random() < 0.08:

            video = (
                generate_live_video(
                    video_index
                )
            )

        else:

            video = (
                generate_video(
                    video_index
                )
            )


        videos.append(
            video
        )


    return {

        "page_type":
            "home",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "categories":
            generate_categories(),

        "videos":
            videos,

        "layout":
            generate_layout(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = generate_home_page(
        min_videos=5,
        max_videos=5,
    )


    print(
        "\n=============================="
    )

    print(
        "YOUTUBE HOME"
    )

    print(
        "=============================="
    )


    print(
        "\nHeader:"
    )

    print(
        page["header"]
    )


    print(
        "\nCategories:"
    )

    for category in (
        page["categories"]
    ):

        print(
            "-",
            category["label"],
            "(selected)"
            if category["selected"]
            else "",
        )


    print(
        "\nVideos:"
    )

    for video in (
        page["videos"]
    ):

        print(
            f"- {video['title']}"
        )

        print(
            f"  Channel: "
            f"{video['channel']['name']}"
        )

        print(
            f"  Views: "
            f"{video['views_text']}"
        )

        print(
            f"  Live: "
            f"{video['live']}"
        )

        print()