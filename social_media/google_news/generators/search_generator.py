from __future__ import annotations

import random

from faker import Faker

from social_media.google_news.generators.media_generator import (
    get_random_article_image,
    get_random_avatar,
    get_random_publisher_logo,
)


fake = Faker()


# ==========================================================
# Search States
# ==========================================================

SEARCH_STATES = [
    "idle",
    "suggestions",
    "results",
    "no_results",
    "recent",
    "voice_search",
]


# ==========================================================
# Constants
# ==========================================================

SEARCH_TERMS = [
    "Artificial intelligence",
    "Climate change",
    "Global markets",
    "Space exploration",
    "Electric vehicles",
    "Technology",
    "World news",
    "Health research",
    "Football",
    "Film industry",
    "Renewable energy",
    "Cybersecurity",
]


PUBLISHERS = [
    "Global News",
    "Morning Journal",
    "World Report",
    "Tech Daily",
    "Business Review",
    "Science Today",
    "The Observer",
    "Daily Chronicle",
    "National Desk",
    "City News",
]


TRENDING_TOPICS = [
    "Artificial Intelligence",
    "Climate",
    "Technology",
    "Business",
    "World",
    "Sports",
    "Science",
    "Entertainment",
]


TOPIC_ICONS = [
    "memory",
    "eco",
    "language",
    "business_center",
    "public",
    "sports_soccer",
    "science",
    "movie",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "8 min ago",
            "18 min ago",
            "32 min ago",
            "1 hour ago",
            "2 hours ago",
            "3 hours ago",
            "Yesterday",
        ]
    )


def generate_query() -> str:

    return random.choice(
        SEARCH_TERMS
    )


def generate_publisher() -> dict:

    return {
        "name":
            random.choice(
                PUBLISHERS
            ),

        "logo":
            get_random_publisher_logo(),

        "description":
            random.choice(
                [
                    "Latest news and analysis",
                    "Independent journalism",
                    "Breaking stories and reports",
                    "News from around the world",
                ]
            ),

        "following":
            random.random() < 0.35,
    }


# ==========================================================
# Search Result
# ==========================================================

def generate_result() -> dict:

    return {
        "title":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    14,
                )
            ),

        "summary":
            fake.text(
                max_nb_chars=random.randint(
                    100,
                    180,
                )
            ),

        "publisher":
            generate_publisher(),

        "timestamp":
            generate_timestamp(),

        "image":
            get_random_article_image(),

        "saved":
            random.random() < 0.2,

        "full_coverage":
            random.random() < 0.25,
    }


# ==========================================================
# Suggestions
# ==========================================================

def generate_suggestions(
    query: str,
) -> list[dict]:

    count = random.randint(
        5,
        8,
    )

    suggestions = []

    base_words = (
        query.lower()
        .split()
    )

    modifiers = [
        "latest",
        "today",
        "news",
        "updates",
        "analysis",
        "research",
        "companies",
        "market",
        "world",
    ]

    for index in range(
        count
    ):

        modifier = random.choice(
            modifiers
        )

        if random.random() < 0.5:

            value = (
                f"{query} {modifier}"
            )

        else:

            value = (
                f"{modifier} {query}"
            )

        suggestions.append(
            {
                "text":
                    value,

                "icon":
                    (
                        "search"
                        if index > 1
                        else "history"
                    ),
            }
        )

    return suggestions


# ==========================================================
# Recent Searches
# ==========================================================

def generate_recent_searches() -> list[dict]:

    terms = random.sample(
        SEARCH_TERMS,
        k=random.randint(
            4,
            8,
        ),
    )

    return [
        {
            "text":
                term,

            "timestamp":
                random.choice(
                    [
                        "Today",
                        "Yesterday",
                        "2 days ago",
                        "Last week",
                    ]
                ),
        }
        for term in terms
    ]


# ==========================================================
# Trending
# ==========================================================

def generate_trending_topics() -> list[dict]:

    selected = random.sample(
        TRENDING_TOPICS,
        k=random.randint(
            5,
            len(
                TRENDING_TOPICS
            ),
        ),
    )

    result = []

    for index, topic in enumerate(
        selected
    ):

        result.append(
            {
                "name":
                    topic,

                "icon":
                    TOPIC_ICONS[
                        index
                        % len(
                            TOPIC_ICONS
                        )
                    ],

                "story_count":
                    random.randint(
                        20,
                        500,
                    ),
            }
        )

    return result


# ==========================================================
# Topic Matches
# ==========================================================

def generate_topic_matches(
    query: str,
) -> list[dict]:

    count = random.randint(
        2,
        4,
    )

    return [
        {
            "name":
                (
                    query
                    if index == 0
                    else random.choice(
                        SEARCH_TERMS
                    )
                ),

            "icon":
                random.choice(
                    TOPIC_ICONS
                ),

            "following":
                random.random() < 0.35,
        }
        for index in range(
            count
        )
    ]


# ==========================================================
# Source Matches
# ==========================================================

def generate_source_matches() -> list[dict]:

    return [
        generate_publisher()
        for _ in range(
            random.randint(
                2,
                4,
            )
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_search_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            SEARCH_STATES
        )
    )

    if selected_state not in SEARCH_STATES:

        raise ValueError(
            f"Unknown search state: "
            f"{selected_state}"
        )


    # ======================================================
    # Query
    # ======================================================

    if selected_state == "idle":

        query = ""

    elif selected_state == "no_results":

        query = (
            fake.word()
            +
            str(
                random.randint(
                    1000,
                    9999,
                )
            )
        )

    else:

        query = (
            generate_query()
        )


    # ======================================================
    # State-specific Data
    # ======================================================

    suggestions = []

    results = []

    topic_matches = []

    source_matches = []

    if selected_state == "suggestions":

        suggestions = (
            generate_suggestions(
                query
            )
        )


    if selected_state == "results":

        results = [
            generate_result()
            for _ in range(
                random.randint(
                    6,
                    10,
                )
            )
        ]

        topic_matches = (
            generate_topic_matches(
                query
            )
        )

        source_matches = (
            generate_source_matches()
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            selected_state,

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

        "query":
            query,

        "search_placeholder":
            "Search topics, locations & sources",

        "suggestions":
            suggestions,

        "recent_searches":
            generate_recent_searches(),

        "trending_topics":
            generate_trending_topics(),

        "results":
            results,

        "topic_matches":
            topic_matches,

        "source_matches":
            source_matches,

        "result_count":
            random.randint(
                140,
                54000,
            ),

        "voice": {
            "status":
                random.choice(
                    [
                        "Listening...",
                        "Speak now",
                        "Listening for news",
                    ]
                ),

            "hint":
                "Try saying a topic, location or source",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in SEARCH_STATES:

        print(
            "\n"
            "================================"
        )

        print(
            state.upper()
        )

        print(
            "================================"
        )

        pprint(
            generate_search_data(
                state=state
            )
        )