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

PROFILE_STATES = [
    "profile",
    "saved",
    "history",
    "data_controls",
    "appearance",
    "signout_dialog",
]


# ==========================================================
# Navigation
# ==========================================================

PROFILE_NAVIGATION = [
    {
        "label": "Profile",
        "icon": "person",
        "state": "profile",
    },
    {
        "label": "Saved stories",
        "icon": "bookmark",
        "state": "saved",
    },
    {
        "label": "History",
        "icon": "history",
        "state": "history",
    },
    {
        "label": "Data controls",
        "icon": "shield",
        "state": "data_controls",
    },
    {
        "label": "Appearance",
        "icon": "palette",
        "state": "appearance",
    },
]


PUBLISHERS = [
    "Global News",
    "The Observer",
    "Daily Chronicle",
    "Tech Daily",
    "Science Today",
    "World Report",
    "Business Review",
    "City News",
]


TOPICS = [
    "Technology",
    "World",
    "Business",
    "Science",
    "Climate",
    "Health",
    "Sports",
    "Entertainment",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_timestamp() -> str:

    return random.choice(
        [
            "5 min ago",
            "18 min ago",
            "1 hour ago",
            "3 hours ago",
            "Yesterday",
            "2 days ago",
            "Last week",
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


def generate_story() -> dict:

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
                    90,
                    160,
                )
            ),

        "publisher":
            generate_publisher(),

        "image":
            get_random_article_image(),

        "timestamp":
            generate_timestamp(),

        "saved":
            True,
    }


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    result = []

    for index in range(
        random.randint(
            7,
            12,
        )
    ):

        item_type = random.choice(
            [
                "article",
                "search",
                "topic",
            ]
        )

        if item_type == "article":

            result.append(
                {
                    "type":
                        "article",

                    "icon":
                        "article",

                    "title":
                        fake.sentence(
                            nb_words=random.randint(
                                6,
                                12,
                            )
                        ),

                    "subtitle":
                        random.choice(
                            PUBLISHERS
                        ),

                    "timestamp":
                        generate_timestamp(),
                }
            )

        elif item_type == "search":

            result.append(
                {
                    "type":
                        "search",

                    "icon":
                        "search",

                    "title":
                        random.choice(
                            TOPICS
                        ),

                    "subtitle":
                        "Search",

                    "timestamp":
                        generate_timestamp(),
                }
            )

        else:

            topic = random.choice(
                TOPICS
            )

            result.append(
                {
                    "type":
                        "topic",

                    "icon":
                        "interests",

                    "title":
                        topic,

                    "subtitle":
                        "Topic viewed",

                    "timestamp":
                        generate_timestamp(),
                }
            )

    return result


# ==========================================================
# Data Controls
# ==========================================================

def generate_data_controls() -> list[dict]:

    return [
        {
            "label":
                "Web & app activity",

            "description":
                "Use activity to personalize news recommendations.",

            "icon":
                "history_toggle_off",

            "enabled":
                random.random() < 0.75,
        },
        {
            "label":
                "Location personalization",

            "description":
                "Use location to improve local news suggestions.",

            "icon":
                "location_on",

            "enabled":
                random.random() < 0.70,
        },
        {
            "label":
                "Personalized recommendations",

            "description":
                "Recommend stories based on your interests.",

            "icon":
                "auto_awesome",

            "enabled":
                random.random() < 0.85,
        },
        {
            "label":
                "Search history",

            "description":
                "Save searches to make future searches easier.",

            "icon":
                "manage_search",

            "enabled":
                random.random() < 0.65,
        },
        {
            "label":
                "Activity retention",

            "description":
                "Automatically manage older activity.",

            "icon":
                "schedule",

            "enabled":
                random.random() < 0.70,
        },
    ]


# ==========================================================
# Appearance
# ==========================================================

def generate_appearance_options() -> dict:

    current_theme = random.choice(
        [
            "System default",
            "Light",
            "Dark",
        ]
    )

    current_density = random.choice(
        [
            "Comfortable",
            "Compact",
        ]
    )

    return {
        "theme":
            current_theme,

        "theme_options": [
            {
                "label": "System default",
                "icon": "settings_brightness",
            },
            {
                "label": "Light",
                "icon": "light_mode",
            },
            {
                "label": "Dark",
                "icon": "dark_mode",
            },
        ],

        "density":
            current_density,

        "density_options": [
            "Comfortable",
            "Compact",
        ],

        "large_text":
            random.random() < 0.25,

        "show_images":
            random.random() < 0.90,
    }


# ==========================================================
# Main
# ==========================================================

def generate_profile_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            PROFILE_STATES
        )
    )

    if selected_state not in PROFILE_STATES:

        raise ValueError(
            f"Unknown profile state: "
            f"{selected_state}"
        )


    user = {
        "name":
            fake.name(),

        "email":
            fake.email(),

        "avatar":
            get_random_avatar(),

        "followed_topics":
            random.randint(
                5,
                24,
            ),

        "followed_sources":
            random.randint(
                4,
                18,
            ),

        "saved_stories":
            random.randint(
                10,
                120,
            ),
    }


    return {

        "state":
            selected_state,

        "brand": {
            "name":
                "Google News",
        },

        "user":
            user,

        "navigation":
            PROFILE_NAVIGATION,

        "saved_stories": [
            generate_story()
            for _ in range(
                random.randint(
                    6,
                    10,
                )
            )
        ],

        "history":
            generate_history(),

        "data_controls":
            generate_data_controls(),

        "appearance":
            generate_appearance_options(),

        "signout_dialog": {
            "title":
                "Sign out?",

            "message":
                (
                    "You can sign in again at any time "
                    "to restore your personalized news."
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    for state in PROFILE_STATES:

        print(
            "\n=============================="
        )

        print(
            state.upper()
        )

        print(
            "=============================="
        )

        pprint(
            generate_profile_data(
                state=state
            )
        )