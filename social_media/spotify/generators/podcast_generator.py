from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_podcast_cover,
    get_random_album_cover,
)

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)

from social_media.spotify.generators.home_generator import (
    generate_player,
)


# ==========================================================
# Data Pools
# ==========================================================

SHOW_NAMES = [
    "Tech Today",
    "Creative Minds",
    "Science Explained",
    "Inside Innovation",
    "Developer Radio",
    "Future Thinking",
    "Daily Conversations",
    "World Stories",
    "Design Stories",
    "The Productivity Show",
    "Startup Diaries",
    "The Learning Lab",
]


PUBLISHERS = [
    "Spotify Studios",
    "Independent Media",
    "Future Network",
    "Creative Audio",
    "Technology Weekly",
    "Studio North",
    "Open Conversations",
]


SHOW_DESCRIPTIONS = [
    (
        "Conversations about technology, creativity, "
        "design, and the ideas shaping the future."
    ),
    (
        "Weekly discussions with researchers, creators, "
        "engineers, and entrepreneurs."
    ),
    (
        "Stories and interviews exploring how people build, "
        "learn, work, and create."
    ),
    (
        "A thoughtful look at emerging technology and how "
        "it changes everyday life."
    ),
]


CATEGORIES = [
    "Technology",
    "Education",
    "Science",
    "Business",
    "Culture",
    "Design",
    "Society",
    "News",
]


EPISODE_TITLES = [
    "How AI Is Changing Creative Work",
    "The Future of Personal Computing",
    "Building Better Digital Products",
    "Why Great Teams Communicate Differently",
    "Designing for Millions of Users",
    "What Comes After Smartphones?",
    "The Science of Better Decisions",
    "Inside the Modern Startup",
    "How Developers Learn Faster",
    "The New Era of Digital Media",
    "Rethinking Productivity",
    "What Makes Technology Useful?",
    "The Future of Remote Collaboration",
    "Understanding Human-Centered Design",
]


EPISODE_DESCRIPTIONS = [
    (
        "In this episode, we explore the ideas, challenges, "
        "and opportunities behind today's rapidly changing technology."
    ),
    (
        "A conversation about how teams approach difficult problems "
        "and turn early ideas into useful products."
    ),
    (
        "We discuss current trends, practical lessons, and what they "
        "could mean for the next generation of digital experiences."
    ),
    (
        "Our guest shares experiences, mistakes, and lessons learned "
        "while building technology used by people around the world."
    ),
]


# ==========================================================
# Helpers
# ==========================================================

def format_duration(
    minutes: int,
) -> str:

    if minutes >= 60:

        hours = (
            minutes // 60
        )

        remaining = (
            minutes % 60
        )

        return (
            f"{hours} hr "
            f"{remaining} min"
        )

    return (
        f"{minutes} min"
    )


def generate_date() -> str:

    month = random.choice(
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
        ]
    )

    day = random.randint(
        1,
        28,
    )

    return (
        f"{month} {day}"
    )


# ==========================================================
# Episode
# ==========================================================

def generate_episode(
    index: int,
) -> dict:

    duration_minutes = random.randint(
        18,
        95,
    )

    has_video = (
        random.random() < 0.25
    )

    return {

        "number":
            index,

        "title":
            random.choice(
                EPISODE_TITLES
            ),

        "description":
            random.choice(
                EPISODE_DESCRIPTIONS
            ),

        "image":
            (
                get_random_podcast_cover()
                or
                get_random_album_cover()
            ),

        "date":
            generate_date(),

        "duration":
            format_duration(
                duration_minutes
            ),

        "downloaded":
            random.random() < 0.18,

        "saved":
            random.random() < 0.22,

        "played":
            random.random() < 0.28,

        "has_video":
            has_video,

        "explicit":
            random.random() < 0.08,
    }


# ==========================================================
# Podcast Page
# ==========================================================

def generate_podcast_page() -> dict:

    episode_count = random.randint(
        8,
        18,
    )


    categories = random.sample(
        CATEGORIES,
        k=random.randint(
            1,
            3,
        ),
    )


    return {

        "navigation":
            generate_navigation(
                selected="library"
            ),

        "show": {

            "name":
                random.choice(
                    SHOW_NAMES
                ),

            "publisher":
                random.choice(
                    PUBLISHERS
                ),

            "description":
                random.choice(
                    SHOW_DESCRIPTIONS
                ),

            "image":
                (
                    get_random_podcast_cover()
                    or
                    get_random_album_cover()
                ),

            "followed":
                random.random() < 0.35,

            "rating":
                round(
                    random.uniform(
                        4.0,
                        5.0,
                    ),
                    1,
                ),

            "categories":
                categories,

            "episode_count":
                episode_count,
        },

        "episodes": [

            generate_episode(
                index + 1
            )

            for index in range(
                episode_count
            )
        ],

        "sort":
            random.choice(
                [
                    "Newest",
                    "Oldest",
                    "Most relevant",
                ]
            ),

        "player":
            generate_player(),
    }