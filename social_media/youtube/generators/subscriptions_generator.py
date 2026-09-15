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
    "New Technology Explained",
    "Python Tutorial",
    "Machine Learning Project",
    "Daily Travel Vlog",
    "Best Street Food",
    "Programming Tips",
    "Gaming Highlights",
    "Photography Tutorial",
    "Latest AI News",
    "Study With Me",
    "Morning Routine",
    "Full Workout Session",
    "Web Development Tutorial",
    "Data Science Explained",
    "Cybersecurity Basics",
    "New Music Release",
    "Cooking at Home",
    "Weekly Tech Update",
    "Productivity Tips",
    "Documentary",
]


SECTION_TITLES = [
    "Today",
    "Yesterday",
    "This week",
    "Earlier",
]


# ==========================================================
# Utility
# ==========================================================

def format_count(
    value: int,
) -> str:

    if value >= 1_000_000_000:

        value = (
            value
            / 1_000_000_000
        )

        return (
            f"{value:.1f}B"
            .replace(
                ".0B",
                "B",
            )
        )


    if value >= 1_000_000:

        value = (
            value
            / 1_000_000
        )

        return (
            f"{value:.1f}M"
            .replace(
                ".0M",
                "M",
            )
        )


    if value >= 1_000:

        value = (
            value
            / 1_000
        )

        return (
            f"{value:.1f}K"
            .replace(
                ".0K",
                "K",
            )
        )


    return str(
        value
    )


# ==========================================================
# Duration
# ==========================================================

def generate_duration() -> str:

    if random.random() < 0.08:

        hours = random.randint(
            1,
            3,
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


# ==========================================================
# Upload Time
# ==========================================================

def generate_upload_time(
    section_title: str,
) -> str:

    if section_title == "Today":

        return random.choice(
            [
                "10 minutes ago",
                "28 minutes ago",
                "1 hour ago",
                "2 hours ago",
                "4 hours ago",
                "7 hours ago",
                "11 hours ago",
            ]
        )


    if section_title == "Yesterday":

        return random.choice(
            [
                "1 day ago",
                "20 hours ago",
                "22 hours ago",
            ]
        )


    if section_title == "This week":

        return random.choice(
            [
                "2 days ago",
                "3 days ago",
                "4 days ago",
                "5 days ago",
                "6 days ago",
            ]
        )


    return random.choice(
        [
            "1 week ago",
            "2 weeks ago",
            "3 weeks ago",
            "1 month ago",
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
            f"Official"
        ),

        (
            f"The "
            f"{fake.last_name()} "
            f"Show"
        ),

        (
            f"{fake.word().title()} "
            f"Academy"
        ),
    ]


    return random.choice(
        variants
    )


def generate_channel(
    index: int,
) -> dict[str, Any]:

    subscribers = random.randint(
        1_000,
        25_000_000,
    )


    return {

        "id":
            f"channel_{index}",

        "name":
            generate_channel_name(),

        "avatar":
            get_random_avatar(),

        "verified":
            random.random()
            < 0.35,

        "subscribers":
            subscribers,

        "subscribers_text":
            (
                f"{format_count(subscribers)} "
                f"subscribers"
            ),

        "notifications":
            random.choice(
                [
                    "all",
                    "personalized",
                    "none",
                ]
            ),
    }


# ==========================================================
# Video Title
# ==========================================================

def generate_video_title() -> str:

    if random.random() < 0.55:

        return random.choice(
            VIDEO_TOPICS
        )


    return (
        fake.sentence(
            nb_words=random.randint(
                5,
                11,
            )
        )
        .rstrip(".")
    )


# ==========================================================
# Subscription Video
# ==========================================================

def generate_video(
    index: int,
    channel: dict[str, Any],
    section_title: str,
) -> dict[str, Any]:

    views = random.randint(
        100,
        200_000_000,
    )


    live = (
        random.random()
        < 0.05
    )


    video = {

        "id":
            f"subscription_video_{index}",

        "title":
            generate_video_title(),

        "thumbnail":
            get_random_thumbnail(),

        "channel":
            channel,

        "views":
            views,

        "views_text":
            (
                f"{format_count(views)} views"
            ),

        "uploaded":
            generate_upload_time(
                section_title
            ),

        "duration":
            None
            if live
            else generate_duration(),

        "live":
            live,

        "new":
            random.random()
            < 0.18,

        "badges":
            [],
    }


    if video["new"]:

        video["badges"].append(
            "New"
        )


    if (
        not live
        and random.random() < 0.05
    ):

        video["badges"].append(
            "4K"
        )


    if live:

        video["views_text"] = (
            f"{format_count(views)} watching"
        )


    return video


# ==========================================================
# Subscribed Channel Row
# ==========================================================

def generate_subscribed_channels(
    min_channels: int = 8,
    max_channels: int = 16,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_channels,
        max_channels,
    )


    return [

        generate_channel(
            index
        )

        for index in range(
            count
        )
    ]


# ==========================================================
# Feed Sections
# ==========================================================

def generate_sections(
    channels: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    section_count = random.randint(
        2,
        4,
    )


    section_titles = (
        SECTION_TITLES[
            :section_count
        ]
    )


    sections = []


    global_video_index = 0


    for section_index, title in enumerate(
        section_titles
    ):

        video_count = random.randint(
            5,
            10,
        )


        videos = []


        for _ in range(
            video_count
        ):

            channel = random.choice(
                channels
            )


            videos.append(
                generate_video(

                    index=
                        global_video_index,

                    channel=
                        channel,

                    section_title=
                        title,
                )
            )


            global_video_index += 1


        sections.append(
            {

                "id":
                    f"section_{section_index}",

                "title":
                    title,

                "videos":
                    videos,
            }
        )


    return sections


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
                False,
        },

        {
            "label":
                "Subscriptions",

            "icon":
                "subscriptions",

            "semantic":
                "subscriptions",

            "selected":
                True,
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
                False,

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
                True,

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
# Controls
# ==========================================================

def generate_controls() -> dict[str, Any]:

    return {

        "title":
            "Subscriptions",

        "manage_label":
            "Manage",

        "view_mode":
            random.choice(
                [
                    "grid",
                    "grid",
                    "grid",
                    "list",
                ]
            ),
    }


# ==========================================================
# Subscriptions Page
# ==========================================================

def generate_subscriptions_page() -> dict[str, Any]:

    channels = (
        generate_subscribed_channels()
    )


    sections = (
        generate_sections(
            channels
        )
    )


    return {

        "page_type":
            "subscriptions",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "controls":
            generate_controls(),

        "channels":
            channels,

        "sections":
            sections,

        "layout": {

            "show_sidebar":
                True,

            "show_channel_strip":
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
        generate_subscriptions_page()
    )


    print(
        "\n"
        "=================================="
    )

    print(
        "YOUTUBE SUBSCRIPTIONS"
    )

    print(
        "=================================="
    )


    print(
        "Channels:",
        len(
            page["channels"]
        )
    )


    print(
        "Sections:",
        len(
            page["sections"]
        )
    )


    for section in (
        page["sections"]
    ):

        print(
            "\n",
            section["title"],
            ":",
            len(
                section["videos"]
            ),
            "videos",
        )


    print(
        "\nView mode:",
        page["controls"]["view_mode"]
    )