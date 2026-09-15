from __future__ import annotations

import random

from faker import Faker

from social_media.google_news.generators.media_generator import (
    get_random_article_image,
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

TOPIC_STATES = [
    "discover",
    "selected",
    "manage",
    "reorder",
    "recommendations",
    "remove_dialog",
]


# ==========================================================
# Topic Pools
# ==========================================================

TOPIC_GROUPS = {
    "News": [
        "World",
        "Politics",
        "Local",
        "Business",
        "Economy",
    ],

    "Technology": [
        "Artificial Intelligence",
        "Cybersecurity",
        "Mobile",
        "Startups",
        "Software",
    ],

    "Science": [
        "Space",
        "Physics",
        "Environment",
        "Climate",
        "Research",
    ],

    "Lifestyle": [
        "Travel",
        "Food",
        "Design",
        "Culture",
        "Fashion",
    ],

    "Entertainment": [
        "Movies",
        "Music",
        "Television",
        "Gaming",
        "Celebrities",
    ],

    "Sports": [
        "Football",
        "Basketball",
        "Baseball",
        "Tennis",
        "Motorsport",
    ],
}


GROUP_ICONS = {
    "News": "newspaper",
    "Technology": "memory",
    "Science": "science",
    "Lifestyle": "public",
    "Entertainment": "movie",
    "Sports": "sports_soccer",
}


# ==========================================================
# Helpers
# ==========================================================

def generate_topic(
    name: str,
    index: int = 0,
) -> dict:

    return {
        "id":
            index,

        "name":
            name,

        "following":
            random.random() < 0.45,

        "notifications":
            random.random() < 0.40,

        "story_count":
            random.randint(
                20,
                900,
            ),

        "image":
            (
                get_random_article_image()
                if random.random() < 0.70
                else None
            ),
    }


def all_topic_names() -> list[str]:

    return [
        topic
        for topics in TOPIC_GROUPS.values()
        for topic in topics
    ]


# ==========================================================
# Groups
# ==========================================================

def generate_groups() -> list[dict]:

    groups = []

    index = 0

    for group_name, topic_names in (
        TOPIC_GROUPS.items()
    ):

        topics = []

        for topic_name in topic_names:

            topics.append(
                generate_topic(
                    topic_name,
                    index=index,
                )
            )

            index += 1

        groups.append(
            {
                "name":
                    group_name,

                "icon":
                    GROUP_ICONS[
                        group_name
                    ],

                "topics":
                    topics,
            }
        )

    return groups


# ==========================================================
# Selected Topics
# ==========================================================

def generate_selected_topics() -> list[dict]:

    names = random.sample(
        all_topic_names(),
        k=random.randint(
            6,
            10,
        ),
    )

    topics = []

    for index, name in enumerate(
        names
    ):

        topic = generate_topic(
            name,
            index=index,
        )

        topic["following"] = True

        topics.append(
            topic
        )

    return topics


# ==========================================================
# Recommendations
# ==========================================================

def generate_recommendations() -> list[dict]:

    names = random.sample(
        all_topic_names(),
        k=random.randint(
            6,
            10,
        ),
    )

    return [
        {
            **generate_topic(
                name,
                index=index,
            ),

            "reason":
                random.choice(
                    [
                        "Based on stories you read",
                        "Trending near you",
                        "Popular with readers",
                        "Related to topics you follow",
                        "Recommended for you",
                    ]
                ),
        }
        for index, name
        in enumerate(names)
    ]


# ==========================================================
# Main
# ==========================================================

def generate_topics_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            TOPIC_STATES
        )
    )

    if selected_state not in TOPIC_STATES:

        raise ValueError(
            f"Unknown topics state: "
            f"{selected_state}"
        )


    selected_topics = (
        generate_selected_topics()
    )


    dialog = None

    if selected_state == "remove_dialog":

        target = random.choice(
            selected_topics
        )

        dialog = {
            "topic":
                target,

            "title":
                "Stop following this topic?",

            "message":
                (
                    "Stories from this topic may appear "
                    "less often in your personalized feed."
                ),
        }


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

        "page_title":
            (
                "Choose your interests"
                if selected_state == "discover"
                else "Your topics"
            ),

        "page_subtitle":
            (
                "Follow topics to personalize your news"
                if selected_state == "discover"
                else
                "Manage the topics used to personalize your feed"
            ),

        "groups":
            generate_groups(),

        "selected_topics":
            selected_topics,

        "recommendations":
            generate_recommendations(),

        "dialog":
            dialog,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in TOPIC_STATES:

        print(
            "\n"
            "============================"
        )

        print(
            state.upper()
        )

        print(
            "============================"
        )

        pprint(
            generate_topics_data(
                state=state
            )
        )