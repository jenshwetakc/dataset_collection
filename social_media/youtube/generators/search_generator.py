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
# Search Queries
# ==========================================================

SEARCH_QUERIES = [
    "python tutorial",
    "machine learning",
    "artificial intelligence",
    "web development",
    "javascript tutorial",
    "computer science",
    "gaming",
    "music",
    "travel vlog",
    "street food",
    "cooking recipes",
    "workout",
    "technology news",
    "photography",
    "robotics",
    "data science",
    "cybersecurity",
    "study music",
    "english learning",
    "documentary",
]


# ==========================================================
# Video Topics
# ==========================================================

VIDEO_TOPICS = [
    "Complete Beginner Tutorial",
    "Everything You Need to Know",
    "Full Course for Beginners",
    "Step by Step Guide",
    "Learn the Basics",
    "Complete Guide",
    "Beginner to Advanced",
    "Explained Simply",
    "Top Tips and Tricks",
    "What You Need to Know",
    "Full Tutorial",
    "The Ultimate Guide",
]


# ==========================================================
# Filter Tabs
# ==========================================================

FILTER_TABS = [
    "All",
    "Videos",
    "Shorts",
    "Unwatched",
    "Watched",
    "Recently uploaded",
    "Live",
]


# ==========================================================
# Count Formatter
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


# ==========================================================
# Upload Time
# ==========================================================

def generate_upload_time() -> str:

    return random.choice(
        [
            "10 minutes ago",
            "30 minutes ago",
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
            "6 months ago",
            "1 year ago",
            "2 years ago",
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
            f"Academy"
        ),

        (
            f"{fake.word().title()} "
            f"Studio"
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
        100,
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
    }


# ==========================================================
# Search Result Title
# ==========================================================

def generate_result_title(
    query: str,
) -> str:

    style = random.random()


    if style < 0.40:

        return (
            f"{query.title()} - "
            f"{random.choice(VIDEO_TOPICS)}"
        )


    if style < 0.75:

        return (
            fake.sentence(
                nb_words=random.randint(
                    6,
                    12,
                )
            )
            .rstrip(".")
        )


    return (
        f"{random.choice(VIDEO_TOPICS)} "
        f"| {query.title()} 2026"
    )


# ==========================================================
# Description
# ==========================================================

def generate_description() -> str:

    return (
        fake.sentence(
            nb_words=random.randint(
                12,
                24,
            )
        )
        .rstrip(".")
    )


# ==========================================================
# Video Result
# ==========================================================

def generate_video_result(
    result_index: int,
    query: str,
) -> dict[str, Any]:

    views = random.randint(
        100,
        400_000_000,
    )


    channel = (
        generate_channel()
    )


    return {

        "id":
            f"result_{result_index}",

        "type":
            "video",

        "title":
            generate_result_title(
                query
            ),

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

        "description":
            generate_description(),

        "channel":
            channel,

        "badges":
            generate_video_badges(),

        "live":
            False,
    }


# ==========================================================
# Live Result
# ==========================================================

def generate_live_result(
    result_index: int,
    query: str,
) -> dict[str, Any]:

    viewers = random.randint(
        100,
        250_000,
    )


    return {

        "id":
            f"result_{result_index}",

        "type":
            "video",

        "title":
            generate_result_title(
                query
            ),

        "thumbnail":
            get_random_thumbnail(),

        "duration":
            None,

        "views":
            viewers,

        "views_text":
            (
                f"{format_count(viewers)} "
                f"watching"
            ),

        "uploaded":
            None,

        "description":
            generate_description(),

        "channel":
            generate_channel(),

        "badges":
            [
                "LIVE"
            ],

        "live":
            True,
    }


# ==========================================================
# Result Badges
# ==========================================================

def generate_video_badges() -> list[str]:

    badges = []


    if random.random() < 0.15:

        badges.append(
            "New"
        )


    if random.random() < 0.06:

        badges.append(
            "4K"
        )


    if random.random() < 0.04:

        badges.append(
            "CC"
        )


    return badges


# ==========================================================
# Channel Result
# ==========================================================

def generate_channel_result(
    result_index: int,
) -> dict[str, Any]:

    channel = (
        generate_channel()
    )


    video_count = random.randint(
        10,
        5000,
    )


    return {

        "id":
            f"channel_{result_index}",

        "type":
            "channel",

        "name":
            channel["name"],

        "avatar":
            channel["avatar"],

        "verified":
            channel["verified"],

        "subscribers_text":
            channel[
                "subscribers_text"
            ],

        "video_count":
            video_count,

        "video_count_text":
            (
                f"{format_count(video_count)} "
                f"videos"
            ),

        "description":
            generate_description(),

        "subscribed":
            random.random()
            < 0.15,
    }


# ==========================================================
# Filters
# ==========================================================

def generate_filters() -> list[dict[str, Any]]:

    selected_count = random.randint(
        4,
        len(FILTER_TABS),
    )


    labels = random.sample(
        FILTER_TABS[1:],
        selected_count - 1,
    )


    labels.insert(
        0,
        "All",
    )


    return [

        {
            "label":
                label,

            "selected":
                index == 0,
        }

        for index, label
        in enumerate(labels)
    ]


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
# Header
# ==========================================================

def generate_header(
    query: str,
) -> dict[str, Any]:

    return {

        "logo_text":
            "YouTube",

        "search_value":
            query,

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
# Search Page
# ==========================================================

def generate_search_page(
    min_results: int = 12,
    max_results: int = 25,
) -> dict[str, Any]:

    query = random.choice(
        SEARCH_QUERIES
    )


    result_count = random.randint(
        min_results,
        max_results,
    )


    results = []


    # ------------------------------------------------------
    # Occasionally insert a matching channel near the top
    # ------------------------------------------------------

    include_channel = (
        random.random()
        < 0.40
    )


    if include_channel:

        results.append(
            generate_channel_result(
                0
            )
        )


    # ------------------------------------------------------
    # Video results
    # ------------------------------------------------------

    for result_index in range(
        result_count
    ):

        if random.random() < 0.07:

            result = (
                generate_live_result(
                    result_index,
                    query,
                )
            )

        else:

            result = (
                generate_video_result(
                    result_index,
                    query,
                )
            )


        results.append(
            result
        )


    return {

        "page_type":
            "search",

        "query":
            query,

        "header":
            generate_header(
                query
            ),

        "filters":
            generate_filters(),

        "navigation":
            generate_navigation(),

        "bottom_navigation":
            generate_bottom_navigation(),

        "results":
            results,

        "layout": {

            "show_sidebar":
                True,

            "show_filters":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = generate_search_page(
        min_results=5,
        max_results=5,
    )


    print(
        "\n=============================="
    )

    print(
        "YOUTUBE SEARCH"
    )

    print(
        "=============================="
    )


    print(
        "\nQuery:",
        page["query"]
    )


    print(
        "\nFilters:"
    )


    for item in (
        page["filters"]
    ):

        print(
            "-",
            item["label"],
            "(selected)"
            if item["selected"]
            else "",
        )


    print(
        "\nResults:"
    )


    for result in (
        page["results"]
    ):

        if (
            result["type"]
            == "channel"
        ):

            print(
                "[CHANNEL]",
                result["name"]
            )

        else:

            print(
                "[VIDEO]",
                result["title"]
            )