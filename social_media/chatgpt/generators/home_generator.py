from __future__ import annotations

import random

from faker import Faker


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Constants
# ==========================================================

MODEL_NAMES = [
    "ChatGPT",
    "GPT-5",
    "GPT-5 Thinking",
    "GPT-4.1",
    "Fast",
]

GREETING_TEMPLATES = [
    "What can I help with?",
    "How can I help today?",
    "What are you working on?",
    "Where should we begin?",
    "Ready when you are.",
    "What would you like to explore?",
]

SUGGESTION_DATA = [

    {
        "icon": "edit_note",
        "title": "Write something",
        "prompts": [
            "Draft a professional email",
            "Help me write a short introduction",
            "Create a product description",
            "Rewrite this more clearly",
        ],
    },

    {
        "icon": "lightbulb",
        "title": "Brainstorm ideas",
        "prompts": [
            "Brainstorm names for a new project",
            "Give me creative presentation ideas",
            "Suggest ideas for a weekend project",
            "Help me plan a new app",
        ],
    },

    {
        "icon": "school",
        "title": "Learn something",
        "prompts": [
            "Explain machine learning simply",
            "Teach me a useful Python concept",
            "Explain how neural networks work",
            "Help me understand this topic",
        ],
    },

    {
        "icon": "code",
        "title": "Code",
        "prompts": [
            "Help me debug Python code",
            "Write a simple REST API",
            "Explain this error message",
            "Create a responsive web layout",
        ],
    },

    {
        "icon": "travel_explore",
        "title": "Explore",
        "prompts": [
            "Plan a three-day trip",
            "Compare two technologies",
            "Help me research a topic",
            "Recommend things to explore",
        ],
    },

    {
        "icon": "analytics",
        "title": "Analyze",
        "prompts": [
            "Summarize a document",
            "Analyze these results",
            "Compare these options",
            "Find patterns in this data",
        ],
    },
]


# ==========================================================
# Conversation Titles
# ==========================================================

def generate_conversation_title() -> str:

    patterns = [

        lambda:
            fake.sentence(
                nb_words=random.randint(
                    2,
                    5,
                )
            ).rstrip("."),

        lambda:
            random.choice([
                "Python debugging help",
                "Research paper summary",
                "UI design ideas",
                "Travel planning",
                "Machine learning notes",
                "Email rewrite",
                "Dataset generation",
                "Project architecture",
                "Weekly study plan",
                "Presentation outline",
                "Code review",
                "Interview preparation",
                "Article summary",
                "API implementation",
                "Design feedback",
            ]),
    ]

    return random.choice(
        patterns
    )()


# ==========================================================
# Conversation Section
# ==========================================================

def generate_history_section(
    label: str,
    min_items: int = 2,
    max_items: int = 5,
) -> dict:

    count = random.randint(
        min_items,
        max_items,
    )

    items = []

    for index in range(
        count
    ):

        items.append({

            "id":
                f"{label.lower()}_{index}",

            "title":
                generate_conversation_title(),

            "active":
                False,

            "has_menu":
                random.random() < 0.75,
        })

    return {

        "label":
            label,

        "items":
            items,
    }


# ==========================================================
# Suggestions
# ==========================================================

def generate_suggestions() -> list[dict]:

    count = random.randint(
        4,
        6,
    )

    selected = random.sample(
        SUGGESTION_DATA,
        k=count,
    )

    suggestions = []

    for index, item in enumerate(
        selected
    ):

        suggestions.append({

            "id":
                f"suggestion_{index}",

            "icon":
                item["icon"],

            "title":
                item["title"],

            "prompt":
                random.choice(
                    item["prompts"]
                ),
        })

    return suggestions


# ==========================================================
# Main Generator
# ==========================================================

def generate_home_data() -> dict:

    history_sections = []

    section_options = [
        "Today",
        "Yesterday",
        "Previous 7 days",
        "Previous 30 days",
    ]

    section_count = random.randint(
        2,
        4,
    )

    for label in section_options[
        :section_count
    ]:

        history_sections.append(
            generate_history_section(
                label
            )
        )


    # ------------------------------------------------------
    # Occasionally highlight one history item
    # ------------------------------------------------------

    all_items = [

        item

        for section
        in history_sections

        for item
        in section["items"]
    ]

    if (
        all_items
        and random.random() < 0.30
    ):

        random.choice(
            all_items
        )["active"] = True


    # ------------------------------------------------------
    # User
    # ------------------------------------------------------

    user_name = fake.first_name()

    initials = (
        user_name[:1]
        .upper()
    )


    # ------------------------------------------------------
    # Composer
    # ------------------------------------------------------

    placeholder = random.choice([
        "Ask anything",
        "Message ChatGPT",
        "What can I help with?",
        "Type a message",
    ])


    return {

        "page_variant":
            "new_chat",

        "model": {
            "name":
                random.choice(
                    MODEL_NAMES
                ),

            "show_dropdown":
                True,
        },

        "user": {
            "name":
                user_name,

            "initials":
                initials,
        },

        "greeting":
            random.choice(
                GREETING_TEMPLATES
            ),

        "suggestions":
            generate_suggestions(),

        "history_sections":
            history_sections,

        "composer": {

            "placeholder":
                placeholder,

            "show_attach":
                True,

            "show_tools":
                random.random() < 0.70,

            "show_voice":
                True,

            "show_send":
                True,
        },

        "sidebar": {

            "show_search":
                True,

            "show_library":
                random.random() < 0.85,

            "show_projects":
                random.random() < 0.65,

            "show_gpts":
                random.random() < 0.65,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_home_data()
    )