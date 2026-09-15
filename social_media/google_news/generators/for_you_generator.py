from __future__ import annotations

import random

from faker import Faker

from social_media.google_news.generators.media_generator import (
    get_random_article_image,
    get_random_avatar,
    get_random_hero_image,
    get_random_publisher_logo,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

TOPICS = [
    "For you",
    "Top stories",
    "Local",
    "Technology",
    "Business",
    "Science",
    "Health",
    "Entertainment",
    "Sports",
    "World",
]

NAVIGATION_ITEMS = [
    {
        "label": "For you",
        "icon": "home",
        "selected": True,
    },
    {
        "label": "Headlines",
        "icon": "article",
        "selected": False,
    },
    {
        "label": "Following",
        "icon": "star",
        "selected": False,
    },
    {
        "label": "Newsstand",
        "icon": "newspaper",
        "selected": False,
    },
]

CATEGORY_OPTIONS = [
    "Technology",
    "World",
    "Business",
    "Science",
    "Health",
    "Entertainment",
    "Sports",
    "Local",
    "Politics",
    "Environment",
    "Travel",
    "Culture",
]

PUBLISHERS = [
    "Global Times",
    "Daily Report",
    "The Chronicle",
    "Morning Journal",
    "World Desk",
    "Tech Daily",
    "Business Review",
    "City News",
    "Science Today",
    "National Post",
    "News Network",
    "The Observer",
    "Current Affairs",
    "Metro Daily",
    "Insight News",
]


# ==========================================================
# Basic Helpers
# ==========================================================

def generate_timestamp() -> str:

    choices = [
        "8 min ago",
        "14 min ago",
        "27 min ago",
        "42 min ago",
        "1 hour ago",
        "2 hours ago",
        "3 hours ago",
        "5 hours ago",
        "Yesterday",
    ]

    return random.choice(
        choices
    )


def generate_publisher() -> dict:

    return {
        "name":
            random.choice(
                PUBLISHERS
            ),

        "logo":
            get_random_publisher_logo(),
    }


def generate_story_title() -> str:

    patterns = [
        fake.sentence(
            nb_words=random.randint(
                7,
                13,
            )
        ),
        fake.sentence(
            nb_words=random.randint(
                8,
                15,
            )
        ),
    ]

    return random.choice(
        patterns
    )


# ==========================================================
# Standard Story
# ==========================================================

def generate_story(
    *,
    include_image: bool = True,
) -> dict:

    publisher = (
        generate_publisher()
    )

    return {

        "publisher":
            publisher,

        "title":
            generate_story_title(),

        "summary":
            fake.text(
                max_nb_chars=random.randint(
                    90,
                    180,
                )
            ),

        "timestamp":
            generate_timestamp(),

        "image":
            (
                get_random_article_image()
                if include_image
                else None
            ),

        "saved":
            random.random()
            < 0.15,

        "full_coverage":
            random.random()
            < 0.35,
    }


# ==========================================================
# Hero Story
# ==========================================================

def generate_hero_story() -> dict:

    publisher = (
        generate_publisher()
    )

    return {

        "publisher":
            publisher,

        "title":
            generate_story_title(),

        "summary":
            fake.text(
                max_nb_chars=220
            ),

        "timestamp":
            generate_timestamp(),

        "image":
            get_random_hero_image(),

        "full_coverage":
            True,
    }


# ==========================================================
# Story Section
# ==========================================================

def generate_section(
    section_index: int,
) -> dict:

    category = random.choice(
        CATEGORY_OPTIONS
    )

    story_count = random.randint(
        3,
        5,
    )

    return {

        "id":
            section_index,

        "title":
            category,

        "subtitle":
            random.choice(
                [
                    f"Latest stories in {category}",
                    f"Top stories about {category}",
                    f"Updates selected for you",
                    f"What's happening in {category}",
                ]
            ),

        "icon":
            random.choice(
                [
                    "public",
                    "business_center",
                    "memory",
                    "science",
                    "health_and_safety",
                    "sports_soccer",
                    "movie",
                    "location_on",
                ]
            ),

        "stories": [
            generate_story()
            for _ in range(
                story_count
            )
        ],
    }


# ==========================================================
# Weather Card
# ==========================================================

def generate_weather() -> dict:

    temperature = random.randint(
        8,
        34,
    )

    return {
        "city":
            fake.city(),

        "temperature":
            temperature,

        "condition":
            random.choice(
                [
                    "Sunny",
                    "Partly cloudy",
                    "Cloudy",
                    "Clear",
                    "Light rain",
                ]
            ),

        "icon":
            random.choice(
                [
                    "sunny",
                    "partly_cloudy_day",
                    "cloud",
                    "rainy",
                ]
            ),
    }


# ==========================================================
# Topics
# ==========================================================

def generate_topic_cards() -> list[dict]:

    categories = random.sample(
        CATEGORY_OPTIONS,
        k=min(
            6,
            len(
                CATEGORY_OPTIONS
            ),
        ),
    )

    result = []

    for category in categories:

        result.append(
            {
                "name":
                    category,

                "following":
                    random.random()
                    < 0.35,

                "story_count":
                    random.randint(
                        12,
                        250,
                    ),
            }
        )

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_for_you_data() -> dict:

    sections = [
        generate_section(
            section_index=index,
        )
        for index in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    return {

        "brand": {
            "name":
                "Google News",
        },

        "user": {
            "name":
                fake.name(),

            "avatar":
                get_random_avatar(),
        },

        "search": {
            "placeholder":
                random.choice(
                    [
                        "Search for topics, locations & sources",
                        "Search Google News",
                        "Search news",
                    ]
                ),
        },

        "navigation":
            NAVIGATION_ITEMS,

        "topics":
            TOPICS,

        "selected_topic":
            "For you",

        "greeting":
            random.choice(
                [
                    "Your briefing",
                    "Good morning",
                    "Good afternoon",
                    "Top stories for you",
                    "Your news update",
                ]
            ),

        "briefing_subtitle":
            fake.date(
                pattern="%A, %B %d",
            ),

        "weather":
            generate_weather(),

        "hero_story":
            generate_hero_story(),

        "top_stories": [
            generate_story()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],

        "sections":
            sections,

        "topic_cards":
            generate_topic_cards(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_for_you_data()
    )