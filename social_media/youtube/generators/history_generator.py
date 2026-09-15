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
    "Daily Travel Vlog",
    "Street Food Tour",
    "Gaming Highlights",
    "Photography Tips",
    "Latest Technology News",
    "Artificial Intelligence Explained",
    "Data Science Tutorial",
    "Study With Me",
    "Relaxing Music",
    "Web Development Tutorial",
    "Cybersecurity Basics",
    "Cooking at Home",
    "Workout Routine",
    "Programming Tips",
    "Productivity Guide",
    "Documentary",
    "Music Performance",
    "Weekly Tech Update",
]


HISTORY_SECTIONS = [
    "Today",
    "Yesterday",
    "This week",
    "Older",
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

def generate_upload_time() -> str:

    return random.choice(
        [
            "1 hour ago",
            "3 hours ago",
            "8 hours ago",
            "1 day ago",
            "2 days ago",
            "5 days ago",
            "1 week ago",
            "2 weeks ago",
            "1 month ago",
            "3 months ago",
            "1 year ago",
        ]
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel_name() -> str:

    return random.choice(
        [
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
        ]
    )


def generate_channel() -> dict[str, Any]:

    return {

        "name":
            generate_channel_name(),

        "verified":
            random.random()
            < 0.25,
    }


# ==========================================================
# Video
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


def generate_history_video(
    index: int,
) -> dict[str, Any]:

    views = random.randint(
        100,
        300_000_000,
    )


    watch_progress = random.randint(
        5,
        100,
    )


    return {

        "id":
            f"history_video_{index}",

        "title":
            generate_video_title(),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            generate_duration(),

        "channel":
            generate_channel(),

        "views_text":
            (
                f"{format_count(views)} views"
            ),

        "uploaded":
            generate_upload_time(),

        "description":
            (
                fake.sentence(
                    nb_words=random.randint(
                        9,
                        18,
                    )
                )
                .rstrip(".")
            ),

        "watch_progress":
            watch_progress,

        "completed":
            watch_progress >= 95,
    }


# ==========================================================
# History Sections
# ==========================================================

def generate_history_sections() -> list[dict[str, Any]]:

    section_count = random.randint(
        2,
        4,
    )


    sections = []

    global_index = 0


    for section_index in range(
        section_count
    ):

        title = (
            HISTORY_SECTIONS[
                section_index
            ]
        )


        video_count = random.randint(
            4,
            8,
        )


        videos = []


        for _ in range(
            video_count
        ):

            videos.append(
                generate_history_video(
                    global_index
                )
            )


            global_index += 1


        sections.append(
            {

                "id":
                    f"history_section_{section_index}",

                "title":
                    title,

                "videos":
                    videos,
            }
        )


    return sections


# ==========================================================
# History Controls
# ==========================================================

def generate_history_controls() -> dict[str, Any]:

    paused = (
        random.random()
        < 0.15
    )


    return {

        "title":
            "Watch history",

        "search_placeholder":
            "Search watch history",

        "history_paused":
            paused,

        "pause_label":
            (
                "Turn on watch history"
                if paused
                else "Pause watch history"
            ),

        "clear_label":
            "Clear all watch history",

        "manage_label":
            "Manage all history",
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
                True,
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
# History Page
# ==========================================================

def generate_history_page() -> dict[str, Any]:

    sections = (
        generate_history_sections()
    )


    return {

        "page_type":
            "history",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "controls":
            generate_history_controls(),

        "sections":
            sections,

        "layout": {

            "show_sidebar":
                True,

            "show_history_controls":
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
        generate_history_page()
    )


    print(
        "\n"
        "=================================="
    )

    print(
        "YOUTUBE HISTORY PAGE"
    )

    print(
        "=================================="
    )


    print(
        "Sections:",
        len(
            page["sections"]
        )
    )


    total_videos = sum(

        len(
            section["videos"]
        )

        for section
        in page["sections"]
    )


    print(
        "Total videos:",
        total_videos
    )


    print(
        "History paused:",
        page["controls"][
            "history_paused"
        ]
    )


    for section in page["sections"]:

        print(
            section["title"],
            ":",
            len(
                section["videos"]
            ),
        )