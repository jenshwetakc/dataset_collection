# social_media/slack/generators/later_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_attachment,
    get_random_avatar,
    get_random_emoji,
    get_random_file_preview,
    get_random_workspace_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

WORKSPACE_NAMES = [
    "Acme Studio",
    "Northstar",
    "Orbit Labs",
    "Pixel Works",
    "Nova Research",
    "Mosaic",
    "Vertex",
    "Nimbus",
]


CHANNELS = [
    "general",
    "engineering",
    "design",
    "research",
    "product",
    "release",
    "frontend",
    "accessibility",
]


SAVED_TEXTS = [
    "Please review the latest implementation before tomorrow.",
    "The mobile layout still needs one small adjustment.",
    "I added the final annotation examples to the document.",
    "Can you check the new dataset output when you have time?",
    "Let's compare this with the previous renderer result.",
    "The accessibility checks are ready for review.",
    "This should be included in the next release batch.",
]


REMINDER_LABELS = [
    "Tomorrow",
    "Later today",
    "Monday",
    "Next week",
    "No reminder",
]


PRIORITIES = [
    "high",
    "medium",
    "normal",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_person(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),
    }


def generate_saved_item(
    people: list[dict],
    index: int,
) -> dict:

    item_type = random.choice(
        [
            "message",
            "message",
            "file",
            "reminder",
        ]
    )

    author = random.choice(
        people
    )

    reaction = None

    if random.random() < 0.35:

        reaction = (
            get_random_emoji()
        )

    item = {
        "id":
            index,

        "type":
            item_type,

        "author":
            author,

        "channel":
            random.choice(
                CHANNELS
            ),

        "time":
            random.choice(
                [
                    "9:18 AM",
                    "10:42 AM",
                    "11:05 AM",
                    "1:34 PM",
                    "3:18 PM",
                    "Yesterday",
                ]
            ),

        "text":
            random.choice(
                SAVED_TEXTS
            ),

        "reminder":
            random.choice(
                REMINDER_LABELS
            ),

        "priority":
            random.choice(
                PRIORITIES
            ),

        "completed":
            random.random() < 0.22,

        "reaction":
            reaction,

        "file_preview":
            None,

        "attachment":
            None,
    }

    if item_type == "file":

        item["file_preview"] = (
            get_random_file_preview()
        )

        item["attachment"] = (
            get_random_attachment()
        )

    return item


# ==========================================================
# Generator
# ==========================================================

def generate_later_data() -> dict:

    people = [
        generate_person(
            index=index
        )
        for index in range(
            random.randint(
                10,
                16,
            )
        )
    ]

    items = [
        generate_saved_item(
            people=people,
            index=index,
        )
        for index in range(
            random.randint(
                14,
                22,
            )
        )
    ]

    visible_items = [
        item
        for item in items
        if not item["completed"]
    ]

    selected_item = random.choice(
        visible_items
        if visible_items
        else items
    )

    return {

        "workspace": {
            "name":
                random.choice(
                    WORKSPACE_NAMES
                ),

            "image":
                get_random_workspace_image(),
        },

        "items":
            items,

        "selected_item":
            selected_item,

        "tabs": [
            {
                "label":
                    "In progress",

                "count":
                    len(
                        [
                            item
                            for item in items
                            if not item["completed"]
                        ]
                    ),
            },
            {
                "label":
                    "Completed",

                "count":
                    len(
                        [
                            item
                            for item in items
                            if item["completed"]
                        ]
                    ),
            },
            {
                "label":
                    "All",

                "count":
                    len(
                        items
                    ),
            },
        ],

        "selected_tab":
            "In progress",

        "panel_mode":
            random.choice(
                [
                    "details",
                    "preview",
                ]
            ),

        "search_placeholder":
            "Search saved items",
    }


if __name__ == "__main__":

    data = generate_later_data()

    print(
        "Later items:",
        len(
            data["items"]
        )
    )

    print(
        "Selected:",
        data["selected_item"]["id"]
    )