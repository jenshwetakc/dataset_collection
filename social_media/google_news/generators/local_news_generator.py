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

LOCAL_NEWS_STATES = [
    "overview",
    "map_explore",
    "multi_city",
    "local_alert",
    "location_picker",
    "empty_location",
]


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "For you",
        "icon": "home",
        "selected": False,
    },
    {
        "label": "Headlines",
        "icon": "article",
        "selected": False,
    },
    {
        "label": "Local",
        "icon": "location_on",
        "selected": True,
    },
    {
        "label": "Following",
        "icon": "star",
        "selected": False,
    },
]


# ==========================================================
# Publishers
# ==========================================================

LOCAL_PUBLISHERS = [
    "Metro News",
    "City Daily",
    "Local Chronicle",
    "Regional News",
    "Community Report",
    "Morning City",
    "Neighborhood Post",
    "Local Desk",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "5 min ago",
            "12 min ago",
            "28 min ago",
            "46 min ago",
            "1 hour ago",
            "2 hours ago",
            "4 hours ago",
            "Yesterday",
        ]
    )


def generate_location() -> dict:

    return {
        "city":
            fake.city(),

        "region":
            fake.state(),

        "following":
            True,

        "temperature":
            random.randint(
                5,
                34,
            ),

        "weather":
            random.choice(
                [
                    "Sunny",
                    "Cloudy",
                    "Partly cloudy",
                    "Light rain",
                    "Clear",
                ]
            ),

        "weather_icon":
            random.choice(
                [
                    "sunny",
                    "cloud",
                    "partly_cloudy_day",
                    "rainy",
                ]
            ),
    }


def generate_publisher() -> dict:

    return {
        "name":
            random.choice(
                LOCAL_PUBLISHERS
            ),

        "logo":
            get_random_publisher_logo(),
    }


# ==========================================================
# Story
# ==========================================================

def generate_story(
    *,
    urgent: bool = False,
) -> dict:

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

        "image":
            get_random_article_image(),

        "timestamp":
            generate_timestamp(),

        "urgent":
            urgent,

        "saved":
            random.random() < 0.20,
    }


# ==========================================================
# Map Markers
# ==========================================================

def generate_map_markers(
    count: int,
) -> list[dict]:

    markers = []

    for index in range(
        count
    ):

        markers.append(
            {
                "id":
                    index,

                # Relative CSS position.
                # This is intentionally synthetic UI geometry.
                "x":
                    random.randint(
                        12,
                        88,
                    ),

                "y":
                    random.randint(
                        14,
                        82,
                    ),

                "icon":
                    random.choice(
                        [
                            "location_on",
                            "article",
                            "emergency",
                            "traffic",
                        ]
                    ),

                "label":
                    random.choice(
                        [
                            "Local story",
                            "Traffic",
                            "Community",
                            "Breaking",
                        ]
                    ),
            }
        )

    return markers


# ==========================================================
# City Group
# ==========================================================

def generate_city_group() -> dict:

    location = (
        generate_location()
    )

    return {
        "location":
            location,

        "stories": [
            generate_story()
            for _ in range(
                random.randint(
                    3,
                    5,
                )
            )
        ],
    }


# ==========================================================
# Nearby Location Suggestions
# ==========================================================

def generate_location_suggestions() -> list[dict]:

    return [
        {
            "city":
                fake.city(),

            "region":
                fake.state(),

            "distance":
                random.randint(
                    2,
                    90,
                ),
        }
        for _ in range(
            random.randint(
                5,
                8,
            )
        )
    ]


# ==========================================================
# Main
# ==========================================================

def generate_local_news_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            LOCAL_NEWS_STATES
        )
    )


    if selected_state not in LOCAL_NEWS_STATES:

        raise ValueError(
            f"Unknown Local News state: "
            f"{selected_state}"
        )


    current_location = (
        None
        if selected_state
        ==
        "empty_location"
        else generate_location()
    )


    stories = [
        generate_story()
        for _ in range(
            random.randint(
                6,
                10,
            )
        )
    ]


    alert_story = None

    if selected_state == "local_alert":

        alert_story = (
            generate_story(
                urgent=True
            )
        )


    city_groups = []

    if selected_state == "multi_city":

        city_groups = [
            generate_city_group()
            for _ in range(
                random.randint(
                    3,
                    5,
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

        "navigation":
            NAVIGATION_ITEMS,

        "page_title":
            "Local news",

        "page_subtitle":
            (
                "Stories from your area"
                if current_location
                else
                "Set a location to discover local stories"
            ),

        "current_location":
            current_location,

        "stories":
            stories,

        "alert_story":
            alert_story,

        "map_markers":
            generate_map_markers(
                random.randint(
                    5,
                    10,
                )
            ),

        "city_groups":
            city_groups,

        "location_suggestions":
            generate_location_suggestions(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in LOCAL_NEWS_STATES:

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
            generate_local_news_data(
                state=state
            )
        )