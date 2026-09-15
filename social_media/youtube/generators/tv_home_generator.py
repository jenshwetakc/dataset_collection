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
# TV States
# ==========================================================

TV_HOME_STATES = [
    "home",
    "navigation_focused",
    "video_focused",
    "profile_menu",
    "search_focused",
]


# ==========================================================
# Helpers
# ==========================================================

def format_count(value: int) -> str:

    if value >= 1_000_000:
        return (
            f"{value / 1_000_000:.1f}M"
            .replace(".0M", "M")
        )

    if value >= 1_000:
        return (
            f"{value / 1_000:.1f}K"
            .replace(".0K", "K")
        )

    return str(value)


def generate_channel() -> dict[str, Any]:

    return {
        "name": random.choice(
            [
                fake.name(),
                f"{fake.word().title()} TV",
                f"{fake.word().title()} Studio",
                f"{fake.first_name()} Media",
            ]
        ),

        "avatar": get_random_avatar(),

        "verified": random.random() < 0.45,
    }


# ==========================================================
# Video Card
# ==========================================================

def generate_video_card(
    index: int,
    focused: bool = False,
) -> dict[str, Any]:

    views = random.randint(
        5_000,
        50_000_000,
    )

    duration = random.choice(
        [
            "4:21",
            "8:42",
            "12:09",
            "18:34",
            "26:11",
            "1:04:22",
        ]
    )

    return {
        "id": f"tv_video_{index}",

        "title": random.choice(
            [
                "Exploring Incredible Places",
                "The Best Moments of the Week",
                "Live Music Performance",
                "Amazing Technology Explained",
                "A Day in the City",
                "Top Stories You Should Know",
                "Relaxing Nature Documentary",
                "Gaming Highlights",
                fake.sentence(
                    nb_words=random.randint(
                        4,
                        8,
                    )
                ),
            ]
        ),

        "thumbnail": get_random_thumbnail(),

        "duration": duration,

        "views": views,

        "views_text": (
            f"{format_count(views)} views"
        ),

        "published": random.choice(
            [
                "2 hours ago",
                "5 hours ago",
                "1 day ago",
                "3 days ago",
                "1 week ago",
                "2 weeks ago",
            ]
        ),

        "channel": generate_channel(),

        "focused": focused,

        "badge": random.choice(
            [
                None,
                None,
                None,
                "LIVE",
                "NEW",
                "4K",
            ]
        ),
    }


# ==========================================================
# Content Rows
# ==========================================================

def generate_row(
    row_id: str,
    title: str,
    focused_index: int | None = None,
) -> dict[str, Any]:

    count = random.randint(
        5,
        8,
    )

    return {
        "id": row_id,

        "title": title,

        "items": [
            generate_video_card(
                index=index,
                focused=(
                    focused_index == index
                ),
            )
            for index in range(count)
        ],
    }


# ==========================================================
# Hero
# ==========================================================

def generate_hero() -> dict[str, Any]:

    return {
        "background":
            get_random_thumbnail(),

        "title":
            random.choice(
                [
                    "Featured for you",
                    "Watch something great",
                    "Today's top pick",
                    "Continue watching",
                ]
            ),

        "description":
            fake.sentence(
                nb_words=random.randint(
                    9,
                    18,
                )
            ),

        "channel":
            generate_channel(),

        "primary_action":
            "Watch",

        "secondary_action":
            "More info",

        "show_gradient":
            True,
    }


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation(
    state: str,
) -> list[dict[str, Any]]:

    items = [
        {
            "id": "search",
            "label": "Search",
            "icon": "search",
        },
        {
            "id": "home",
            "label": "Home",
            "icon": "home",
        },
        {
            "id": "shorts",
            "label": "Shorts",
            "icon": "smart_display",
        },
        {
            "id": "subscriptions",
            "label": "Subscriptions",
            "icon": "subscriptions",
        },
        {
            "id": "library",
            "label": "Library",
            "icon": "video_library",
        },
        {
            "id": "settings",
            "label": "Settings",
            "icon": "settings",
        },
    ]

    focused_id = None

    if state == "navigation_focused":
        focused_id = random.choice(
            [
                "home",
                "shorts",
                "subscriptions",
                "library",
            ]
        )

    if state == "search_focused":
        focused_id = "search"

    return [
        {
            **item,

            "selected":
                item["id"] == "home",

            "focused":
                item["id"] == focused_id,

            "semantic":
                f"tv_nav_{item['id']}",
        }
        for item in items
    ]


# ==========================================================
# Profile
# ==========================================================

def generate_profiles() -> list[dict[str, Any]]:

    count = random.randint(
        2,
        4,
    )

    return [
        {
            "id":
                f"profile_{index}",

            "name":
                (
                    "You"
                    if index == 0
                    else fake.first_name()
                ),

            "avatar":
                get_random_avatar(),

            "selected":
                index == 0,

            "focused":
                index == 0,
        }
        for index in range(count)
    ]


# ==========================================================
# Search
# ==========================================================

def generate_search(
    state: str,
) -> dict[str, Any]:

    focused = (
        state == "search_focused"
    )

    return {
        "focused": focused,

        "placeholder": "Search YouTube",

        "query":
            (
                random.choice(
                    [
                        "",
                        "music",
                        "news",
                        "gaming",
                    ]
                )
                if focused
                else ""
            ),

        "suggestions": (
            [
                "live music",
                "latest news",
                "gaming highlights",
                "travel videos",
                "technology",
            ]
            if focused
            else []
        ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_tv_home_page(
    state: str | None = None,
) -> dict[str, Any]:

    if state is None:
        state = random.choice(
            TV_HOME_STATES
        )

    if state not in TV_HOME_STATES:
        raise ValueError(
            f"Unknown TV state: {state}. "
            f"Expected one of: {TV_HOME_STATES}"
        )

    focused_row = None
    focused_index = None

    if state == "video_focused":
        focused_row = random.choice(
            [
                "recommended",
                "trending",
                "continue_watching",
            ]
        )

        focused_index = random.randint(
            0,
            3,
        )

    rows = [
        generate_row(
            row_id="recommended",
            title="Recommended",
            focused_index=(
                focused_index
                if focused_row == "recommended"
                else None
            ),
        ),

        generate_row(
            row_id="trending",
            title="Trending now",
            focused_index=(
                focused_index
                if focused_row == "trending"
                else None
            ),
        ),

        generate_row(
            row_id="continue_watching",
            title="Continue watching",
            focused_index=(
                focused_index
                if focused_row
                == "continue_watching"
                else None
            ),
        ),
    ]

    return {
        "page_type": "tv_home",

        "state": state,

        "hero": generate_hero(),

        "navigation":
            generate_navigation(
                state
            ),

        "rows": rows,

        "account": {
            "name": fake.first_name(),

            "avatar":
                get_random_avatar(),
        },

        "profiles":
            generate_profiles(),

        "profile_menu": {
            "open":
                state
                == "profile_menu",
        },

        "search":
            generate_search(
                state
            ),

        "layout": {
            "show_navigation":
                True,

            "show_hero":
                state
                != "search_focused",

            "show_rows":
                state
                != "search_focused",

            "show_profile_menu":
                state
                == "profile_menu",

            "show_search_overlay":
                state
                == "search_focused",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE TV HOME"
    )

    print(
        "=========================================="
    )

    for state in TV_HOME_STATES:

        page = generate_tv_home_page(
            state=state
        )

        print(
            "\n"
            "------------------------------------------"
        )

        print(
            "State:",
            page["state"]
        )

        print(
            "Rows:",
            len(page["rows"])
        )

        print(
            "Profile menu:",
            page["profile_menu"]["open"]
        )

        print(
            "Search focused:",
            page["search"]["focused"]
        )

        focused_videos = []

        for row in page["rows"]:

            for video in row["items"]:

                if video["focused"]:

                    focused_videos.append(
                        (
                            row["id"],
                            video["title"],
                        )
                    )

        print(
            "Focused videos:",
            focused_videos
        )