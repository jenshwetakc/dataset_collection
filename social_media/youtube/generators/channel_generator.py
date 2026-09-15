from __future__ import annotations

import random

from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
    get_random_banner,
    get_random_thumbnail,
    get_random_short_image,
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
            "24 minutes ago",
            "1 hour ago",
            "4 hours ago",
            "1 day ago",
            "3 days ago",
            "1 week ago",
            "2 weeks ago",
            "1 month ago",
            "4 months ago",
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
            f"{fake.first_name()} Tech",
            f"{fake.word().title()} Studio",
            f"{fake.word().title()} Official",
            f"The {fake.last_name()} Show",
            f"{fake.word().title()} Academy",
        ]
    )


def generate_channel() -> dict[str, Any]:

    name = generate_channel_name()

    handle = (
        "@"
        + fake.user_name()
        .replace(".", "")
        .replace("-", "")
    )

    subscribers = random.randint(
        500,
        50_000_000,
    )

    total_videos = random.randint(
        10,
        3000,
    )

    return {
        "name":
            name,

        "handle":
            handle,

        "avatar":
            get_random_avatar(),

        "banner":
            get_random_banner(),

        "verified":
            random.random() < 0.45,

        "subscribed":
            random.random() < 0.35,

        "subscribers":
            subscribers,

        "subscribers_text":
            f"{format_count(subscribers)} subscribers",

        "total_videos":
            total_videos,

        "total_videos_text":
            f"{total_videos} videos",

        "description":
            fake.paragraph(
                nb_sentences=random.randint(
                    1,
                    3,
                )
            ),

        "links_count":
            random.randint(
                0,
                6,
            ),
    }


# ==========================================================
# Standard Video
# ==========================================================

def generate_video(
    index: int,
) -> dict[str, Any]:

    views = random.randint(
        100,
        300_000_000,
    )

    return {
        "id":
            f"channel_video_{index}",

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

        "views":
            views,

        "views_text":
            f"{format_count(views)} views",

        "uploaded":
            generate_upload_time(),

        "live":
            random.random() < 0.04,
    }


# ==========================================================
# Video Collection
# ==========================================================

def generate_videos(
    min_items: int = 8,
    max_items: int = 16,
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
# Shorts
# ==========================================================

def generate_short(
    index: int,
) -> dict[str, Any]:

    views = random.randint(
        100,
        100_000_000,
    )

    return {
        "id":
            f"channel_short_{index}",

        "title":
            fake.sentence(
                nb_words=random.randint(
                    3,
                    8,
                )
            ).rstrip("."),

        "image":
            get_random_short_image(),

        "views":
            views,

        "views_text":
            f"{format_count(views)} views",
    }


def generate_shorts(
    min_items: int = 5,
    max_items: int = 10,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_items,
        max_items,
    )

    return [
        generate_short(index)
        for index in range(count)
    ]


# ==========================================================
# Playlist
# ==========================================================

def generate_playlist(
    index: int,
) -> dict[str, Any]:

    video_count = random.randint(
        2,
        200,
    )

    return {
        "id":
            f"channel_playlist_{index}",

        "title":
            random.choice(
                [
                    "Popular uploads",
                    "Tutorials",
                    "Best videos",
                    "Favorites",
                    "Learning",
                    "Music",
                    "Travel",
                    "Programming",
                    "Highlights",
                ]
            ),

        "thumbnail":
            get_random_thumbnail(),

        "video_count":
            video_count,

        "video_count_text":
            f"{video_count} videos",
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
        generate_playlist(index)
        for index in range(count)
    ]


# ==========================================================
# Featured Video
# ==========================================================

def generate_featured_video() -> dict[str, Any]:

    video = generate_video(
        index=9999
    )

    video["description"] = (
        fake.paragraph(
            nb_sentences=random.randint(
                1,
                2,
            )
        )
    )

    return video


# ==========================================================
# Tabs
# ==========================================================

def generate_tabs() -> list[dict[str, Any]]:

    active = random.choice(
        [
            "home",
            "videos",
            "shorts",
            "playlists",
        ]
    )

    return [
        {
            "label": "Home",
            "semantic": "channel_home_tab",
            "value": "home",
            "selected": active == "home",
        },
        {
            "label": "Videos",
            "semantic": "channel_videos_tab",
            "value": "videos",
            "selected": active == "videos",
        },
        {
            "label": "Shorts",
            "semantic": "channel_shorts_tab",
            "value": "shorts",
            "selected": active == "shorts",
        },
        {
            "label": "Playlists",
            "semantic": "channel_playlists_tab",
            "value": "playlists",
            "selected": active == "playlists",
        },
        {
            "label": "Community",
            "semantic": "channel_community_tab",
            "value": "community",
            "selected": False,
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
# Channel Page
# ==========================================================

def generate_channel_page() -> dict[str, Any]:

    channel = (
        generate_channel()
    )

    return {
        "page_type":
            "channel",

        "header":
            generate_header(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "channel":
            channel,

        "tabs":
            generate_tabs(),

        "featured_video":
            generate_featured_video(),

        "videos":
            generate_videos(),

        "shorts":
            generate_shorts(),

        "playlists":
            generate_playlists(),

        "controls": {
            "subscribe_label":
                (
                    "Subscribed"
                    if channel["subscribed"]
                    else "Subscribe"
                ),

            "more_label":
                "More",

            "search_channel_label":
                "Search channel",
        },

        "layout": {
            "show_sidebar":
                True,

            "show_banner":
                True,

            "show_featured_video":
                True,

            "show_video_section":
                True,

            "show_shorts_section":
                True,

            "show_playlist_section":
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
        generate_channel_page()
    )

    channel = (
        page["channel"]
    )

    print(
        "\n"
        "=================================="
    )

    print(
        "YOUTUBE CHANNEL PAGE"
    )

    print(
        "=================================="
    )

    print(
        "Channel:",
        channel["name"]
    )

    print(
        "Handle:",
        channel["handle"]
    )

    print(
        "Subscribers:",
        channel["subscribers_text"]
    )

    print(
        "Videos:",
        len(page["videos"])
    )

    print(
        "Shorts:",
        len(page["shorts"])
    )

    print(
        "Playlists:",
        len(page["playlists"])
    )

    print(
        "Subscribed:",
        channel["subscribed"]
    )

    print(
        "\nTabs:"
    )

    for tab in page["tabs"]:

        print(
            tab["label"],
            "selected="
            f"{tab['selected']}"
        )