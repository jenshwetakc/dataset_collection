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
            "20 minutes ago",
            "1 hour ago",
            "3 hours ago",
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
# Account
# ==========================================================

def generate_account() -> dict[str, Any]:

    first_name = fake.first_name()

    last_name = fake.last_name()

    name = (
        f"{first_name} "
        f"{last_name}"
    )

    handle = (
        "@"
        + fake.user_name()
        .replace(
            ".",
            ""
        )
        .replace(
            "-",
            ""
        )
    )


    subscribers = random.randint(
        0,
        2_000_000,
    )


    return {

        "name":
            name,

        "handle":
            handle,

        "avatar":
            get_random_avatar(),

        "subscribers":
            subscribers,

        "subscribers_text":
            (
                f"{format_count(subscribers)} "
                f"subscribers"
            ),

        "channel_exists":
            random.random()
            < 0.85,
    }


# ==========================================================
# Video
# ==========================================================

def generate_video(
    index: int,
) -> dict[str, Any]:

    views = random.randint(
        100,
        200_000_000,
    )


    return {

        "id":
            f"you_video_{index}",

        "title":
            (
                fake.sentence(
                    nb_words=random.randint(
                        5,
                        10,
                    )
                )
                .rstrip(".")
            ),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            generate_duration(),

        "channel":
            random.choice(
                [
                    fake.name(),
                    f"{fake.first_name()} Tech",
                    f"{fake.word().title()} Studio",
                    f"{fake.word().title()} Official",
                ]
            ),

        "views_text":
            (
                f"{format_count(views)} views"
            ),

        "uploaded":
            generate_upload_time(),

        "verified":
            random.random()
            < 0.20,
    }


# ==========================================================
# Video List
# ==========================================================

def generate_video_list(
    prefix: str,
    min_items: int = 4,
    max_items: int = 8,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_items,
        max_items,
    )


    videos = []


    for index in range(
        count
    ):

        video = generate_video(
            index
        )

        video["id"] = (
            f"{prefix}_{index}"
        )

        videos.append(
            video
        )


    return videos


# ==========================================================
# Playlists
# ==========================================================

def generate_playlist(
    index: int,
) -> dict[str, Any]:

    video_count = random.randint(
        2,
        200,
    )


    playlist_names = [
        "Favorites",
        "Study Playlist",
        "Music",
        "Watch Later",
        "Programming",
        "Travel",
        "Tutorials",
        "Interesting Videos",
        "Saved Videos",
        "Learning",
    ]


    return {

        "id":
            f"playlist_{index}",

        "title":
            random.choice(
                playlist_names
            ),

        "thumbnail":
            get_random_thumbnail(),

        "video_count":
            video_count,

        "video_count_text":
            (
                f"{video_count} videos"
            ),

        "visibility":
            random.choice(
                [
                    "Private",
                    "Public",
                    "Unlisted",
                ]
            ),
    }


def generate_playlists(
    min_items: int = 3,
    max_items: int = 7,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_items,
        max_items,
    )


    return [

        generate_playlist(
            index
        )

        for index in range(
            count
        )
    ]


# ==========================================================
# Library Actions
# ==========================================================

def generate_library_actions() -> list[dict[str, Any]]:

    return [

        {
            "label":
                "History",

            "icon":
                "history",

            "semantic":
                "history",

            "count":
                random.randint(
                    0,
                    500,
                ),
        },

        {
            "label":
                "Playlists",

            "icon":
                "playlist_play",

            "semantic":
                "playlists",

            "count":
                random.randint(
                    1,
                    30,
                ),
        },

        {
            "label":
                "Your videos",

            "icon":
                "smart_display",

            "semantic":
                "your_videos",

            "count":
                random.randint(
                    0,
                    50,
                ),
        },

        {
            "label":
                "Downloads",

            "icon":
                "download",

            "semantic":
                "downloads",

            "count":
                random.randint(
                    0,
                    100,
                ),
        },

        {
            "label":
                "Watch later",

            "icon":
                "schedule",

            "semantic":
                "watch_later",

            "count":
                random.randint(
                    0,
                    500,
                ),
        },

        {
            "label":
                "Liked videos",

            "icon":
                "thumb_up",

            "semantic":
                "liked_videos",

            "count":
                random.randint(
                    0,
                    5000,
                ),
        },
    ]


# ==========================================================
# Settings Actions
# ==========================================================

def generate_settings_actions() -> list[dict[str, Any]]:

    return [

        {
            "label":
                "Settings",

            "icon":
                "settings",

            "semantic":
                "settings",
        },

        {
            "label":
                "Help & feedback",

            "icon":
                "help",

            "semantic":
                "help_feedback",
        },
    ]


# ==========================================================
# Header
# ==========================================================

def generate_header(
    account: dict[str, Any],
) -> dict[str, Any]:

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
            account["avatar"],
    }


# ==========================================================
# Navigation
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
                True,
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
                True,

            "create":
                False,
        },
    ]


# ==========================================================
# Page Sections
# ==========================================================

def generate_sections() -> list[dict[str, Any]]:

    return [

        {
            "id":
                "history",

            "title":
                "History",

            "semantic":
                "history_section",

            "show_all":
                True,

            "videos":
                generate_video_list(
                    prefix="history",
                    min_items=4,
                    max_items=7,
                ),
        },

        {
            "id":
                "watch_later",

            "title":
                "Watch later",

            "semantic":
                "watch_later_section",

            "show_all":
                True,

            "videos":
                generate_video_list(
                    prefix="watch_later",
                    min_items=3,
                    max_items=6,
                ),
        },

        {
            "id":
                "liked_videos",

            "title":
                "Liked videos",

            "semantic":
                "liked_videos_section",

            "show_all":
                True,

            "videos":
                generate_video_list(
                    prefix="liked",
                    min_items=3,
                    max_items=6,
                ),
        },
    ]


# ==========================================================
# You Page
# ==========================================================

def generate_you_page() -> dict[str, Any]:

    account = (
        generate_account()
    )


    return {

        "page_type":
            "you",

        "header":
            generate_header(
                account
            ),

        "account":
            account,

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "library_actions":
            generate_library_actions(),

        "settings_actions":
            generate_settings_actions(),

        "playlists":
            generate_playlists(),

        "sections":
            generate_sections(),

        "layout": {

            "show_sidebar":
                True,

            "show_bottom_navigation":
                True,

            "show_library_actions":
                True,

            "show_playlists":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_you_page()
    )


    print(
        "\n"
        "=================================="
    )

    print(
        "YOUTUBE YOU PAGE"
    )

    print(
        "=================================="
    )


    print(
        "Account:",
        page["account"]["name"]
    )


    print(
        "Handle:",
        page["account"]["handle"]
    )


    print(
        "Playlists:",
        len(
            page["playlists"]
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
            section["title"],
            ":",
            len(
                section["videos"]
            ),
            "videos",
        )


    print(
        "Library actions:",
        len(
            page["library_actions"]
        )
    )