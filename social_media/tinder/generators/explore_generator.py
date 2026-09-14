from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_tinder_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

CATEGORY_POOL = [

    {
        "title": "Coffee Date",
        "subtitle": "Find someone for your next cafe stop",
        "icon": "local_cafe",
        "tone": "coffee",
    },

    {
        "title": "Free Tonight",
        "subtitle": "Meet people who are ready to make plans",
        "icon": "nightlife",
        "tone": "night",
    },

    {
        "title": "Foodies",
        "subtitle": "Match over restaurants and good food",
        "icon": "restaurant",
        "tone": "food",
    },

    {
        "title": "Looking for Love",
        "subtitle": "People interested in something serious",
        "icon": "favorite",
        "tone": "love",
    },

    {
        "title": "Travel",
        "subtitle": "Meet people who love discovering new places",
        "icon": "flight",
        "tone": "travel",
    },

    {
        "title": "Music Lovers",
        "subtitle": "Find someone who shares your playlists",
        "icon": "headphones",
        "tone": "music",
    },

    {
        "title": "Gamers",
        "subtitle": "Play together or just talk games",
        "icon": "sports_esports",
        "tone": "gaming",
    },

    {
        "title": "Nature",
        "subtitle": "Hiking, camping, and weekend escapes",
        "icon": "forest",
        "tone": "nature",
    },

    {
        "title": "Creatives",
        "subtitle": "Designers, artists, photographers and more",
        "icon": "palette",
        "tone": "creative",
    },

    {
        "title": "Fitness",
        "subtitle": "Find an active match",
        "icon": "fitness_center",
        "tone": "fitness",
    },

    {
        "title": "Pet Parents",
        "subtitle": "Meet people who love animals",
        "icon": "pets",
        "tone": "pets",
    },

    {
        "title": "Movie Night",
        "subtitle": "Find someone who loves films as much as you",
        "icon": "movie",
        "tone": "movie",
    },
]


QUICK_FILTERS = [
    "Nearby",
    "New here",
    "Verified",
    "Active today",
    "Long-term",
    "Short-term",
    "Weekend plans",
    "Travel",
]


TRENDING_LABELS = [
    "Popular near you",
    "Trending today",
    "Made for you",
    "People are joining",
]


# ==========================================================
# Category
# ==========================================================

def generate_category(
    source: dict,
    index: int,
) -> dict:

    return {

        "id":
            fake.uuid4(),

        "title":
            source["title"],

        "subtitle":
            source["subtitle"],

        "icon":
            source["icon"],

        "tone":
            source["tone"],

        "image":
            get_random_tinder_image(),

        "count":
            random.randint(
                120,
                9800,
            ),

        "featured":
            index < 2,
    }


# ==========================================================
# Recommendation
# ==========================================================

def generate_recommendation() -> dict:

    source = random.choice(
        CATEGORY_POOL
    )

    return {

        "id":
            fake.uuid4(),

        "title":
            source["title"],

        "image":
            get_random_tinder_image(),

        "icon":
            source["icon"],

        "label":
            random.choice(
                TRENDING_LABELS
            ),
    }


# ==========================================================
# Generator
# ==========================================================

def generate_explore_data() -> dict:

    categories = random.sample(
        CATEGORY_POOL,
        k=random.randint(
            8,
            min(
                12,
                len(CATEGORY_POOL),
            ),
        ),
    )

    return {

        "page_title":
            "Explore",

        "subtitle":
            "Find people who are into the same things",

        "quick_filters":
            random.sample(
                QUICK_FILTERS,
                k=random.randint(
                    4,
                    6,
                ),
            ),

        "categories": [

            generate_category(
                category,
                index,
            )

            for index, category
            in enumerate(
                categories
            )
        ],

        "recommendations": [

            generate_recommendation()

            for _ in range(
                random.randint(
                    4,
                    7,
                )
            )
        ],

        "navigation": [

            {
                "label": "Discover",
                "icon": "local_fire_department",
                "active": False,
                "semantic": "discover",
            },

            {
                "label": "Explore",
                "icon": "grid_view",
                "active": True,
                "semantic": "explore",
            },

            {
                "label": "Likes",
                "icon": "favorite",
                "active": False,
                "semantic": "likes",
            },

            {
                "label": "Messages",
                "icon": "chat_bubble",
                "active": False,
                "semantic": "messages",
            },

            {
                "label": "Profile",
                "icon": "person",
                "active": False,
                "semantic": "profile",
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_explore_data()
    )