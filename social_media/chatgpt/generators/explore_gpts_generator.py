from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Categories
# ==========================================================

GPT_CATEGORIES = [
    {
        "id": "featured",
        "label": "Featured",
        "icon": "stars",
    },
    {
        "id": "writing",
        "label": "Writing",
        "icon": "edit_note",
    },
    {
        "id": "productivity",
        "label": "Productivity",
        "icon": "task_alt",
    },
    {
        "id": "research",
        "label": "Research",
        "icon": "science",
    },
    {
        "id": "education",
        "label": "Education",
        "icon": "school",
    },
    {
        "id": "design",
        "label": "Design",
        "icon": "palette",
    },
    {
        "id": "coding",
        "label": "Coding",
        "icon": "code",
    },
]


# ==========================================================
# GPT Names
# ==========================================================

GPT_NAMES = [
    "Research Assistant",
    "Data Analyst",
    "Academic Writer",
    "Code Mentor",
    "Design Critic",
    "Study Companion",
    "Presentation Builder",
    "Paper Reviewer",
    "Python Tutor",
    "Productivity Planner",
    "UX Researcher",
    "Dataset Inspector",
    "Math Solver",
    "Visual Concept Studio",
    "Meeting Assistant",
    "Literature Explorer",
    "SQL Assistant",
    "Frontend Helper",
]


# ==========================================================
# Descriptions
# ==========================================================

GPT_DESCRIPTIONS = [
    (
        "Search, organize, and explain complex research "
        "topics using structured summaries."
    ),
    (
        "Analyze datasets and help turn raw information "
        "into useful insights."
    ),
    (
        "Improve academic writing, structure arguments, "
        "and review drafts."
    ),
    (
        "Explain code, find bugs, and suggest practical "
        "implementation improvements."
    ),
    (
        "Review interface designs and provide actionable "
        "feedback on layout and usability."
    ),
    (
        "Create study plans, explanations, exercises, "
        "and revision material."
    ),
    (
        "Turn notes and ideas into clear presentation "
        "structures and slide content."
    ),
]


# ==========================================================
# Visual Variants
# ==========================================================

VISUAL_VARIANTS = [
    "gpt-visual-a",
    "gpt-visual-b",
    "gpt-visual-c",
    "gpt-visual-d",
    "gpt-visual-e",
    "gpt-visual-f",
]


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    groups = []

    titles = [
        "Dataset planning",
        "Research notes",
        "UI implementation",
        "Training analysis",
        "Paper review",
        "Code debugging",
        "Project ideas",
    ]

    for group_index, label in enumerate(
        [
            "Today",
            "Yesterday",
            "Previous 7 days",
        ]
    ):

        count = random.randint(
            2,
            4,
        )

        items = []

        for item_index in range(
            count
        ):

            items.append({

                "title":
                    random.choice(
                        titles
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
# Creator
# ==========================================================

def generate_creator() -> dict:

    name = fake.name()

    return {

        "name":
            name,

        "initials":
            "".join(
                part[0]
                for part in name.split()[:2]
            ).upper(),
    }


# ==========================================================
# GPT Item
# ==========================================================

def generate_gpt_item(
    index: int,
) -> dict:

    creator = (
        generate_creator()
    )

    return {

        "id":
            f"gpt_{index}",

        "name":
            random.choice(
                GPT_NAMES
            ),

        "description":
            random.choice(
                GPT_DESCRIPTIONS
            ),

        "creator":
            creator,

        "visual":
            random.choice(
                VISUAL_VARIANTS
            ),

        "usage":
            random.choice([
                "10K+ chats",
                "25K+ chats",
                "50K+ chats",
                "100K+ chats",
                "250K+ chats",
                "500K+ chats",
                "1M+ chats",
            ]),

        "verified":
            random.random()
            < 0.45,

        "new":
            random.random()
            < 0.16,

        "featured":
            random.random()
            < 0.32,
    }


# ==========================================================
# Featured GPTs
# ==========================================================

def generate_featured_gpts() -> list[dict]:

    count = random.randint(
        4,
        6,
    )

    items = []

    for index in range(
        count
    ):

        item = generate_gpt_item(
            index
        )

        item["featured"] = True

        items.append(
            item
        )

    return items


# ==========================================================
# Trending
# ==========================================================

def generate_trending_gpts() -> list[dict]:

    count = random.randint(
        5,
        8,
    )

    items = []

    for index in range(
        count
    ):

        item = generate_gpt_item(
            index + 100
        )

        item["rank"] = (
            index + 1
        )

        items.append(
            item
        )

    return items


# ==========================================================
# Discovery Grid
# ==========================================================

def generate_discovery_gpts() -> list[dict]:

    return [

        generate_gpt_item(
            index + 200
        )

        for index in range(
            random.randint(
                6,
                10,
            )
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_explore_gpts_data() -> dict:

    user_name = fake.name()

    active_category = random.choice(
        GPT_CATEGORIES[:4]
    )

    return {

        "page_variant":
            "explore_gpts",

        "user": {

            "name":
                user_name,

            "initials":
                "".join(
                    part[0]
                    for part in user_name.split()[:2]
                ).upper(),
        },

        "history_sections":
            generate_history(),

        "search": {

            "placeholder":
                random.choice([
                    "Search GPTs",
                    "Search tools and assistants",
                    "Find a GPT",
                ]),

            "query":
                "",
        },

        "categories":
            GPT_CATEGORIES,

        "active_category":
            active_category["id"],

        "featured_gpts":
            generate_featured_gpts(),

        "trending_gpts":
            generate_trending_gpts(),

        "discovery_gpts":
            generate_discovery_gpts(),

        "hero": {

            "eyebrow":
                "Discover",

            "title":
                random.choice([
                    "Explore GPTs",
                    "Find the right GPT",
                    "Discover useful assistants",
                ]),

            "description":
                (
                    "Browse specialized GPTs for writing, "
                    "research, coding, learning, and more."
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_explore_gpts_data()
    )