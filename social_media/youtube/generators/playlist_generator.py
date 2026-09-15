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

        value = value / 1_000_000_000

        return (
            f"{value:.1f}B"
            .replace(".0B", "B")
        )

    if value >= 1_000_000:

        value = value / 1_000_000

        return (
            f"{value:.1f}M"
            .replace(".0M", "M")
        )

    if value >= 1_000:

        value = value / 1_000

        return (
            f"{value:.1f}K"
            .replace(".0K", "K")
        )

    return str(value)


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
            "2 hours ago",
            "6 hours ago",
            "1 day ago",
            "3 days ago",
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

def generate_channel() -> dict[str, Any]:

    name = random.choice(
        [
            fake.name(),
            f"{fake.first_name()} Tech",
            f"{fake.word().title()} Studio",
            f"{fake.word().title()} Official",
            f"The {fake.last_name()} Show",
        ]
    )

    subscribers = random.randint(
        100,
        20_000_000,
    )

    return {
        "name": name,
        "avatar": get_random_avatar(),
        "verified": random.random() < 0.30,
        "subscribers": subscribers,
        "subscribers_text":
            f"{format_count(subscribers)} subscribers",
    }


# ==========================================================
# Playlist Metadata
# ==========================================================

def generate_playlist_title() -> str:

    return random.choice(
        [
            "My Favorite Videos",
            "Programming Tutorials",
            "Study Playlist",
            "Machine Learning",
            "Travel Videos",
            "Music Mix",
            "Watch Later Collection",
            "Web Development",
            "Interesting Videos",
            "Tech Videos",
            "Learning Resources",
            "Weekend Playlist",
        ]
    )


def generate_playlist_description() -> str:

    return (
        fake.paragraph(
            nb_sentences=random.randint(
                1,
                3,
            )
        )
    )


# ==========================================================
# Video
# ==========================================================

def generate_video(
    index: int,
) -> dict[str, Any]:

    views = random.randint(
        100,
        300_000_000,
    )

    channel = generate_channel()

    return {
        "id":
            f"playlist_video_{index}",

        "index":
            index + 1,

        "title":
            fake.sentence(
                nb_words=random.randint(
                    5,
                    11,
                )
            ).rstrip("."),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            generate_duration(),

        "channel":
            channel,

        "views":
            views,

        "views_text":
            f"{format_count(views)} views",

        "uploaded":
            generate_upload_time(),

        "watched":
            random.random() < 0.30,

        "watch_progress":
            random.randint(
                5,
                100,
            ),

        "unavailable":
            random.random() < 0.03,
    }


# ==========================================================
# Videos
# ==========================================================

def generate_playlist_videos(
    min_items: int = 8,
    max_items: int = 20,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_items,
        max_items,
    )

    return [
        generate_video(index)
        for index in range(count)
    ]


# ==========================================================
# Playlist
# ==========================================================

def generate_playlist() -> dict[str, Any]:

    videos = (
        generate_playlist_videos()
    )

    owner = (
        generate_channel()
    )

    total_views = sum(
        video["views"]
        for video in videos
    )

    return {
        "title":
            generate_playlist_title(),

        "description":
            generate_playlist_description(),

        "cover":
            (
                videos[0]["thumbnail"]
                if videos
                else get_random_thumbnail()
            ),

        "owner":
            owner,

        "video_count":
            len(videos),

        "video_count_text":
            f"{len(videos)} videos",

        "total_views":
            total_views,

        "total_views_text":
            f"{format_count(total_views)} views",

        "visibility":
            random.choice(
                [
                    "Private",
                    "Public",
                    "Unlisted",
                ]
            ),

        "updated":
            random.choice(
                [
                    "Updated today",
                    "Updated yesterday",
                    "Updated 3 days ago",
                    "Updated 1 week ago",
                    "Updated 1 month ago",
                ]
            ),

        "videos":
            videos,
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
            random.random() < 0.90,

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
            "selected": True,
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
            "selected": True,
            "create": False,
        },
    ]


# ==========================================================
# Playlist Page
# ==========================================================

def generate_playlist_page() -> dict[str, Any]:

    playlist = (
        generate_playlist()
    )

    return {
        "page_type":
            "playlist",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "playlist":
            playlist,

        "controls": {
            "play_label":
                "Play all",

            "shuffle_label":
                "Shuffle",

            "save_label":
                "Save",

            "share_label":
                "Share",
        },

        "layout": {
            "show_sidebar":
                True,

            "show_bottom_navigation":
                True,

            "show_playlist_panel":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_playlist_page()
    )

    playlist = (
        page["playlist"]
    )

    print(
        "\n"
        "=================================="
    )

    print(
        "YOUTUBE PLAYLIST PAGE"
    )

    print(
        "=================================="
    )

    print(
        "Title:",
        playlist["title"]
    )

    print(
        "Owner:",
        playlist["owner"]["name"]
    )

    print(
        "Visibility:",
        playlist["visibility"]
    )

    print(
        "Videos:",
        playlist["video_count"]
    )

    print(
        "Total views:",
        playlist["total_views_text"]
    )

    print(
        "\nFirst few videos:"
    )

    for video in playlist["videos"][:5]:

        print(
            video["index"],
            video["title"],
            video["duration"],
        )