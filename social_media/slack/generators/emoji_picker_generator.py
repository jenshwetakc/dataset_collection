# social_media/slack/generators/emoji_picker_generator.py

from __future__ import annotations

import random

from social_media.slack.generators.media_generator import (
    get_random_emojis,
)


# ==========================================================
# Categories
# ==========================================================

EMOJI_CATEGORIES = [
    {
        "id": "recent",
        "label": "Recent",
        "icon": "schedule",
    },
    {
        "id": "smileys",
        "label": "Smileys",
        "icon": "sentiment_satisfied",
    },
    {
        "id": "people",
        "label": "People",
        "icon": "person",
    },
    {
        "id": "animals",
        "label": "Animals",
        "icon": "pets",
    },
    {
        "id": "food",
        "label": "Food",
        "icon": "restaurant",
    },
    {
        "id": "activities",
        "label": "Activities",
        "icon": "sports_soccer",
    },
    {
        "id": "travel",
        "label": "Travel",
        "icon": "flight",
    },
    {
        "id": "objects",
        "label": "Objects",
        "icon": "lightbulb",
    },
    {
        "id": "symbols",
        "label": "Symbols",
        "icon": "favorite",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_emoji_items(
    count: int,
) -> list[dict]:

    emojis = get_random_emojis(
        count=count
    )

    return [
        {
            "id":
                index,

            "image":
                emoji["image"],

            "source":
                emoji["source"],

            "name":
                emoji["name"],
        }

        for index, emoji
        in enumerate(emojis)
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_emoji_picker_data() -> dict:

    selected_category = random.choice(
        EMOJI_CATEGORIES[
            1:
        ]
    )

    # Dense grid.
    emoji_count = random.randint(
        60,
        96,
    )

    all_emojis = generate_emoji_items(
        emoji_count
    )

    recent_emojis = generate_emoji_items(
        random.randint(
            8,
            14,
        )
    )

    quick_reactions = generate_emoji_items(
        random.randint(
            5,
            7,
        )
    )

    return {

        "selected_category":
            selected_category["id"],

        "categories":
            EMOJI_CATEGORIES,

        "recent_emojis":
            recent_emojis,

        "quick_reactions":
            quick_reactions,

        "emojis":
            all_emojis,

        "search_placeholder":
            "Search emoji",

        "title":
            random.choice(
                [
                    "Add reaction",
                    "Choose an emoji",
                    "Emoji",
                ]
            ),

        "show_skin_tone":
            random.random() < 0.65,

        "show_recent":
            random.random() < 0.85,

        "selected_emoji":
            (
                random.choice(
                    all_emojis
                )
                if all_emojis
                and random.random() < 0.35
                else None
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_emoji_picker_data()

    print(
        "Category:",
        data["selected_category"]
    )

    print(
        "Emoji count:",
        len(
            data["emojis"]
        )
    )

    print(
        "Recent:",
        len(
            data["recent_emojis"]
        )
    )