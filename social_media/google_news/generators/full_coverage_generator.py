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
# States
# ==========================================================

FULL_COVERAGE_STATES = [
    "overview",
    "timeline",
    "perspectives",
    "fact_check",
    "media_focus",
    "live_cluster",
]


# ==========================================================
# Pools
# ==========================================================

PUBLISHERS = [
    "Global News",
    "The Observer",
    "Daily Chronicle",
    "World Report",
    "National Desk",
    "Current Affairs",
    "Morning Journal",
    "News Network",
    "City Times",
    "International Review",
]


TOPICS = [
    "Artificial intelligence",
    "Global markets",
    "Climate policy",
    "Space exploration",
    "Public health",
    "Technology regulation",
    "Energy transition",
    "International trade",
    "Major sporting event",
    "Scientific discovery",
]


STANCE_LABELS = [
    "Analysis",
    "Explainer",
    "Local view",
    "Global view",
    "Opinion",
    "Background",
]


VERDICTS = [
    "Supported",
    "Needs context",
    "Partly supported",
    "Unverified",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "Just now",
            "6 min ago",
            "14 min ago",
            "29 min ago",
            "45 min ago",
            "1 hour ago",
            "2 hours ago",
            "Yesterday",
        ]
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


def generate_story(
    *,
    featured: bool = False,
    live: bool = False,
) -> dict:

    return {
        "title":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    15,
                )
            ),

        "summary":
            fake.text(
                max_nb_chars=random.randint(
                    100,
                    190,
                )
            ),

        "publisher":
            generate_publisher(),

        "image":
            get_random_article_image(),

        "timestamp":
            generate_timestamp(),

        "featured":
            featured,

        "live":
            live,

        "saved":
            random.random() < 0.20,
    }


# ==========================================================
# Timeline
# ==========================================================

def generate_timeline() -> list[dict]:

    count = random.randint(
        6,
        10,
    )

    times = [
        "09:10",
        "09:45",
        "10:20",
        "10:55",
        "11:30",
        "12:05",
        "12:42",
        "13:15",
        "14:00",
        "14:35",
    ]

    return [
        {
            "time":
                times[
                    index
                    % len(times)
                ],

            "title":
                fake.sentence(
                    nb_words=random.randint(
                        6,
                        11,
                    )
                ),

            "description":
                fake.text(
                    max_nb_chars=130
                ),

            "latest":
                index == count - 1,
        }
        for index in range(
            count
        )
    ]


# ==========================================================
# Perspectives
# ==========================================================

def generate_perspectives() -> list[dict]:

    return [
        {
            "label":
                random.choice(
                    STANCE_LABELS
                ),

            "publisher":
                generate_publisher(),

            "title":
                fake.sentence(
                    nb_words=random.randint(
                        7,
                        13,
                    )
                ),

            "summary":
                fake.text(
                    max_nb_chars=140
                ),

            "image":
                get_random_article_image(),
        }
        for _ in range(
            random.randint(
                4,
                7,
            )
        )
    ]


# ==========================================================
# Fact Checks
# ==========================================================

def generate_fact_checks() -> list[dict]:

    return [
        {
            "claim":
                fake.sentence(
                    nb_words=random.randint(
                        6,
                        11,
                    )
                ),

            "verdict":
                random.choice(
                    VERDICTS
                ),

            "explanation":
                fake.text(
                    max_nb_chars=150
                ),

            "publisher":
                generate_publisher(),
        }
        for _ in range(
            random.randint(
                3,
                6,
            )
        )
    ]


# ==========================================================
# Media
# ==========================================================

def generate_media_items() -> list[dict]:

    return [
        {
            "image":
                get_random_article_image(),

            "caption":
                fake.sentence(
                    nb_words=random.randint(
                        5,
                        10,
                    )
                ),

            "publisher":
                generate_publisher(),
        }
        for _ in range(
            random.randint(
                5,
                9,
            )
        )
    ]


# ==========================================================
# Main
# ==========================================================

def generate_full_coverage_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            FULL_COVERAGE_STATES
        )
    )

    if selected_state not in FULL_COVERAGE_STATES:

        raise ValueError(
            f"Unknown Full Coverage state: "
            f"{selected_state}"
        )


    topic = random.choice(
        TOPICS
    )


    hero_story = (
        generate_story(
            featured=True,
            live=(
                selected_state
                ==
                "live_cluster"
            ),
        )
    )


    related_stories = [
        generate_story()
        for _ in range(
            random.randint(
                6,
                10,
            )
        )
    ]


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

        "topic":
            topic,

        "page_title":
            "Full Coverage",

        "page_subtitle":
            f"Stories, context and perspectives about {topic}",

        "hero_story":
            hero_story,

        "related_stories":
            related_stories,

        "timeline":
            (
                generate_timeline()
                if selected_state
                in {
                    "timeline",
                    "live_cluster",
                }
                else []
            ),

        "perspectives":
            (
                generate_perspectives()
                if selected_state
                ==
                "perspectives"
                else []
            ),

        "fact_checks":
            (
                generate_fact_checks()
                if selected_state
                ==
                "fact_check"
                else []
            ),

        "media_items":
            (
                generate_media_items()
                if selected_state
                ==
                "media_focus"
                else []
            ),

        "sources": [
            generate_publisher()
            for _ in range(
                random.randint(
                    4,
                    7,
                )
            )
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in FULL_COVERAGE_STATES:

        print(
            "\n============================"
        )

        print(
            state.upper()
        )

        print(
            "============================"
        )

        pprint(
            generate_full_coverage_data(
                state=state
            )
        )