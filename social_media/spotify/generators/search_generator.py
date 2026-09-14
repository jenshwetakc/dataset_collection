from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
)

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)

from social_media.spotify.generators.home_generator import (
    generate_player,
)


SEARCH_CATEGORIES = [

    "Music",
    "Podcasts",
    "Live Events",
    "Made For You",

    "New Releases",
    "Charts",
    "Pop",
    "Hip-Hop",

    "Rock",
    "Indie",
    "R&B",
    "K-Pop",

    "Dance / Electronic",
    "Jazz",
    "Classical",

    "Chill",
    "Workout",
    "Focus",
    "Sleep",

    "Mood",
    "Party",
    "Gaming",
    "Travel",

    "Wellness",
    "Trending",
]


SEARCH_PLACEHOLDERS = [

    "What do you want to play?",

    "Search artists, songs, or podcasts",

    "What do you want to listen to?",

    "Search Spotify",

    "Find music and podcasts",
]


def generate_search_category(
    title: str,
) -> dict:

    return {

        "title":
            title,

        "image":
            get_random_album_cover(),
    }


def generate_search_page() -> dict:

    category_count = random.randint(
        12,
        min(
            24,
            len(
                SEARCH_CATEGORIES
            ),
        ),
    )

    selected_categories = random.sample(
        SEARCH_CATEGORIES,
        k=category_count,
    )


    return {

        "navigation":
            generate_navigation(
                selected="search"
            ),

        "search": {

            "placeholder":
                random.choice(
                    SEARCH_PLACEHOLDERS
                ),

            "query":
                "",
        },

        "categories": [

            generate_search_category(
                category
            )

            for category
            in selected_categories
        ],

        "player":
            generate_player(),
    }