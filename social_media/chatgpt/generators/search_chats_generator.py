from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Search Queries
# ==========================================================

SEARCH_QUERIES = [
    "python",
    "machine learning",
    "UI design",
    "dataset",
    "research",
    "accessibility",
    "presentation",
    "API",
    "training",
    "responsive layout",
    "computer vision",
    "paper",
]


# ==========================================================
# Chat Titles
# ==========================================================

CHAT_TITLES = [
    "Python debugging help",
    "Machine learning experiment",
    "Synthetic UI dataset",
    "Research paper summary",
    "Accessibility testing",
    "Responsive layout design",
    "Model training results",
    "Computer vision pipeline",
    "REST API implementation",
    "Presentation preparation",
    "Frontend component architecture",
    "Object detection evaluation",
    "Dataset annotation strategy",
    "Fine-tuning configuration",
    "UI component detection",
    "Research methodology notes",
]


# ==========================================================
# Chat Preview Text
# ==========================================================

CHAT_PREVIEWS = [
    (
        "We discussed how to structure the implementation "
        "and separate shared rendering logic."
    ),
    (
        "The model can be trained using the generated "
        "screenshots and corresponding annotations."
    ),
    (
        "This approach keeps the layout responsive across "
        "mobile, tablet, and desktop viewports."
    ),
    (
        "The issue occurs because the bounding box is being "
        "calculated before clipping the visible region."
    ),
    (
        "We can improve the dataset diversity by generating "
        "multiple interaction and popup states."
    ),
    (
        "The next step is to validate the generated labels "
        "against the screenshot dimensions."
    ),
]


# ==========================================================
# Time Groups
# ==========================================================

GROUPS = [
    "Today",
    "Yesterday",
    "Previous 7 days",
    "Previous 30 days",
]


# ==========================================================
# Recent Search
# ==========================================================

def generate_recent_searches() -> list[dict]:

    count = random.randint(
        3,
        6,
    )

    selected = random.sample(
        SEARCH_QUERIES,
        k=count,
    )

    return [
        {
            "query":
                query,

            "icon":
                "history",
        }
        for query in selected
    ]


# ==========================================================
# Search Result
# ==========================================================

def generate_search_result(
    index: int,
    query: str,
) -> dict:

    title = random.choice(
        CHAT_TITLES
    )

    preview = random.choice(
        CHAT_PREVIEWS
    )

    return {

        "id":
            f"result_{index}",

        "title":
            title,

        "preview":
            preview,

        "timestamp":
            fake.time(
                pattern="%H:%M"
            ),

        "query":
            query,

        "pinned":
            random.random() < 0.12,

        "has_file":
            random.random() < 0.18,

        "has_image":
            random.random() < 0.14,

        "unread":
            random.random() < 0.10,
    }


# ==========================================================
# Result Groups
# ==========================================================

def generate_result_groups(
    query: str,
) -> list[dict]:

    group_count = random.randint(
        2,
        4,
    )

    result_groups = []

    result_index = 0

    for label in GROUPS[
        :group_count
    ]:

        count = random.randint(
            2,
            5,
        )

        items = []

        for _ in range(
            count
        ):

            items.append(
                generate_search_result(
                    index=result_index,
                    query=query,
                )
            )

            result_index += 1

        result_groups.append({

            "label":
                label,

            "items":
                items,
        })

    return result_groups


# ==========================================================
# Sidebar History
# ==========================================================

def generate_sidebar_history() -> list[dict]:

    groups = []

    for group_index, label in enumerate(
        [
            "Today",
            "Yesterday",
            "Previous 7 days",
        ]
    ):

        items = []

        count = random.randint(
            2,
            4,
        )

        for index in range(
            count
        ):

            items.append({

                "title":
                    random.choice(
                        CHAT_TITLES
                    ),

                "active":
                    False,
            })

        groups.append({

            "label":
                label,

            "items":
                items,
        })

    return groups


# ==========================================================
# Main Generator
# ==========================================================

def generate_search_chats_data() -> dict:

    query = random.choice(
        SEARCH_QUERIES
    )

    user_name = fake.first_name()

    result_groups = (
        generate_result_groups(
            query
        )
    )

    result_count = sum(

        len(
            group["items"]
        )

        for group in result_groups
    )

    return {

        "page_variant":
            "search_chats",

        "query":
            query,

        "result_count":
            result_count,

        "user": {

            "name":
                user_name,

            "initials":
                user_name[:1].upper(),
        },

        "model": {

            "name":
                random.choice([
                    "ChatGPT",
                    "GPT-5",
                    "GPT-5 Thinking",
                ]),
        },

        "recent_searches":
            generate_recent_searches(),

        "result_groups":
            result_groups,

        "history_sections":
            generate_sidebar_history(),

        "filters": [

            {
                "id":
                    "all",

                "label":
                    "All",

                "selected":
                    True,
            },

            {
                "id":
                    "chats",

                "label":
                    "Chats",

                "selected":
                    False,
            },

            {
                "id":
                    "files",

                "label":
                    "Files",

                "selected":
                    False,
            },

            {
                "id":
                    "images",

                "label":
                    "Images",

                "selected":
                    False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_search_chats_data()
    )