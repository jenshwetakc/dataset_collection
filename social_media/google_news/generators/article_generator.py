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

ARTICLE_STATES = [
    "standard",
    "immersive",
    "reader",
    "comments_sheet",
    "share_sheet",
    "save_confirmation",
]


# ==========================================================
# Content Pools
# ==========================================================

PUBLISHERS = [
    "Global News",
    "Daily Chronicle",
    "The Observer",
    "World Report",
    "Morning Journal",
    "Science Today",
    "Tech Daily",
    "Business Review",
    "National Desk",
    "Current Affairs",
]


TOPICS = [
    "Technology",
    "World",
    "Business",
    "Science",
    "Health",
    "Climate",
    "Sports",
    "Culture",
]


SHARE_TARGETS = [
    {
        "label": "Messages",
        "icon": "chat",
    },
    {
        "label": "Email",
        "icon": "mail",
    },
    {
        "label": "Copy link",
        "icon": "link",
    },
    {
        "label": "Nearby",
        "icon": "near_me",
    },
    {
        "label": "More",
        "icon": "more_horiz",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "12 min ago",
            "28 min ago",
            "1 hour ago",
            "2 hours ago",
            "4 hours ago",
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

        "following":
            random.random() < 0.4,
    }


def generate_author() -> dict:

    return {
        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "role":
            random.choice(
                [
                    "Staff writer",
                    "Technology correspondent",
                    "Senior reporter",
                    "News editor",
                    "Contributor",
                ]
            ),
    }


# ==========================================================
# Body
# ==========================================================

def generate_paragraphs() -> list[str]:

    count = random.randint(
        7,
        12,
    )

    return [
        fake.paragraph(
            nb_sentences=random.randint(
                3,
                6,
            )
        )
        for _ in range(
            count
        )
    ]


# ==========================================================
# Related Stories
# ==========================================================

def generate_related_story() -> dict:

    return {
        "title":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    13,
                )
            ),

        "publisher":
            generate_publisher(),

        "image":
            get_random_article_image(),

        "timestamp":
            generate_timestamp(),
    }


# ==========================================================
# Comments
# ==========================================================

def generate_comments() -> list[dict]:

    return [
        {
            "user":
                fake.name(),

            "avatar":
                get_random_avatar(),

            "text":
                fake.sentence(
                    nb_words=random.randint(
                        8,
                        18,
                    )
                ),

            "likes":
                random.randint(
                    0,
                    380,
                ),

            "timestamp":
                random.choice(
                    [
                        "2 min",
                        "8 min",
                        "21 min",
                        "1 hr",
                        "3 hr",
                    ]
                ),
        }
        for _ in range(
            random.randint(
                4,
                7,
            )
        )
    ]


# ==========================================================
# Main
# ==========================================================

def generate_article_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            ARTICLE_STATES
        )
    )

    if selected_state not in ARTICLE_STATES:

        raise ValueError(
            f"Unknown article state: "
            f"{selected_state}"
        )


    publisher = (
        generate_publisher()
    )


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

        "publisher":
            publisher,

        "author":
            generate_author(),

        "topic":
            random.choice(
                TOPICS
            ),

        "headline":
            fake.sentence(
                nb_words=random.randint(
                    10,
                    18,
                )
            ),

        "dek":
            fake.text(
                max_nb_chars=random.randint(
                    130,
                    230,
                )
            ),

        "hero_image":
            get_random_article_image(),

        "published":
            generate_timestamp(),

        "read_time":
            random.choice(
                [
                    "3 min read",
                    "5 min read",
                    "7 min read",
                    "9 min read",
                ]
            ),

        "paragraphs":
            generate_paragraphs(),

        "inline_image":
            get_random_article_image(),

        "caption":
            fake.sentence(
                nb_words=random.randint(
                    7,
                    12,
                )
            ),

        "saved":
            (
                selected_state
                ==
                "save_confirmation"
                or random.random()
                < 0.20
            ),

        "comment_count":
            random.randint(
                18,
                950,
            ),

        "comments":
            (
                generate_comments()
                if selected_state
                ==
                "comments_sheet"
                else []
            ),

        "share_targets":
            SHARE_TARGETS,

        "related_stories": [
            generate_related_story()
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

    for state in ARTICLE_STATES:

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
            generate_article_data(
                state=state
            )
        )