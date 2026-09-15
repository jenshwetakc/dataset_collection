# social_media/facebook/generators/watch_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_post_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

WATCH_STATES = [
    "default",
    "default",
    "live_feed",
    "following",
    "saved_videos",
    "theater_mode",
    "comments_open",
    "video_menu_open",
    "search_active",
]


WATCH_CATEGORIES = [
    {
        "name": "For you",
        "icon": "home",
    },
    {
        "name": "Live",
        "icon": "live_tv",
    },
    {
        "name": "Gaming",
        "icon": "sports_esports",
    },
    {
        "name": "Music",
        "icon": "music_note",
    },
    {
        "name": "Sports",
        "icon": "sports_soccer",
    },
    {
        "name": "News",
        "icon": "newspaper",
    },
]


VIDEO_TITLES = [
    "Amazing places you should visit",
    "A relaxing afternoon in the city",
    "Best moments from this weekend",
    "Behind the scenes",
    "Daily highlights",
    "Exploring somewhere new",
    "Creative ideas worth trying",
    "A day in my life",
]


DESCRIPTIONS = [
    "A few highlights from today.",
    "Sharing this moment with everyone.",
    "Some of my favorite clips from the week.",
    "A short video from today's adventure.",
    "Hope you enjoy this video.",
]


# ==========================================================
# Video
# ==========================================================

def generate_video(
    index: int,
) -> dict:

    is_live = (
        random.random()
        < 0.18
    )

    return {
        "id":
            index,

        "creator":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "poster":
            get_random_post_image(),

        "title":
            random.choice(
                VIDEO_TITLES
            ),

        "description":
            random.choice(
                DESCRIPTIONS
            ),

        "views":
            random.randint(
                100,
                2500000,
            ),

        "likes":
            random.randint(
                5,
                98000,
            ),

        "comments":
            random.randint(
                0,
                12000,
            ),

        "shares":
            random.randint(
                0,
                4600,
            ),

        "duration":
            (
                "LIVE"
                if is_live
                else random.choice(
                    [
                        "0:42",
                        "1:15",
                        "2:38",
                        "4:20",
                        "8:11",
                        "12:46",
                    ]
                )
            ),

        "is_live":
            is_live,

        "following":
            random.random()
            < 0.4,

        "saved":
            random.random()
            < 0.25,

        "timestamp":
            random.choice(
                [
                    "Just now",
                    "1 h",
                    "3 h",
                    "Yesterday",
                    "2 days ago",
                ]
            ),
    }


def generate_videos(
    count: int = 10,
) -> list[dict]:

    return [
        generate_video(index)
        for index in range(count)
    ]


# ==========================================================
# Comments
# ==========================================================

def generate_comment(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "text":
            random.choice(
                [
                    "Great video!",
                    "Love this.",
                    "This is amazing!",
                    "Thanks for sharing.",
                    "Really enjoyed this.",
                    "Where was this filmed?",
                ]
            ),

        "timestamp":
            random.choice(
                [
                    "1m",
                    "4m",
                    "10m",
                    "30m",
                    "1h",
                ]
            ),

        "likes":
            random.randint(
                0,
                180,
            ),
    }


def generate_comments(
    count: int = 6,
) -> list[dict]:

    return [
        generate_comment(index)
        for index in range(count)
    ]


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> list[dict]:

    return [
        {
            "name": "Home",
            "icon": "smart_display",
        },
        {
            "name": "Live",
            "icon": "live_tv",
        },
        {
            "name": "Reels",
            "icon": "movie",
        },
        {
            "name": "Shows",
            "icon": "subscriptions",
        },
        {
            "name": "Saved videos",
            "icon": "bookmark",
        },
    ]


# ==========================================================
# State
# ==========================================================

def generate_watch_state(
    video_count: int,
) -> dict:

    name = random.choice(
        WATCH_STATES
    )

    selected_video = None

    if name in {
        "theater_mode",
        "comments_open",
        "video_menu_open",
    }:

        selected_video = random.randint(
            0,
            max(
                0,
                min(
                    video_count - 1,
                    5,
                )
            ),
        )

    search_text = ""

    if name == "search_active":

        search_text = random.choice(
            [
                "travel",
                "gaming",
                "music",
                "sports",
                "news",
            ]
        )

    return {
        "name":
            name,

        "selected_video":
            selected_video,

        "search_text":
            search_text,
    }


# ==========================================================
# Complete Data
# ==========================================================

def generate_watch_data() -> dict:

    videos = generate_videos(
        count=random.randint(
            8,
            13,
        )
    )

    live_videos = [
        video
        for video in videos
        if video["is_live"]
    ]

    if not live_videos:

        videos[0]["is_live"] = True
        videos[0]["duration"] = "LIVE"

        live_videos = [
            videos[0]
        ]

    following_videos = [
        video
        for video in videos
        if video["following"]
    ]

    if not following_videos:

        videos[1]["following"] = True

        following_videos = [
            videos[1]
        ]

    saved_videos = [
        video
        for video in videos
        if video["saved"]
    ]

    if not saved_videos:

        videos[2]["saved"] = True

        saved_videos = [
            videos[2]
        ]

    return {
        "navigation":
            generate_navigation(),

        "categories":
            WATCH_CATEGORIES,

        "videos":
            videos,

        "live_videos":
            live_videos,

        "following_videos":
            following_videos,

        "saved_videos":
            saved_videos,

        "comments":
            generate_comments(
                count=random.randint(
                    5,
                    8,
                )
            ),

        "state":
            generate_watch_state(
                video_count=len(
                    videos
                )
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_watch_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK WATCH GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Videos:",
        len(
            data["videos"]
        ),
    )

    print(
        "Live:",
        len(
            data["live_videos"]
        ),
    )

    print(
        "Following:",
        len(
            data["following_videos"]
        ),
    )

    print(
        "Saved:",
        len(
            data["saved_videos"]
        ),
    )

    print(
        "State:",
        data["state"],
    )