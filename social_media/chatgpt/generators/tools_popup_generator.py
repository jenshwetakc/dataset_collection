from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Tool Definitions
# ==========================================================

TOOL_OPTIONS = [
    {
        "icon": "language",
        "title": "Search the web",
        "description": "Find current information online",
        "semantic": "web_search",
    },
    {
        "icon": "image",
        "title": "Create image",
        "description": "Generate an image from a prompt",
        "semantic": "image_generation",
    },
    {
        "icon": "upload_file",
        "title": "Upload files",
        "description": "Add documents, images, or data",
        "semantic": "upload_file",
    },
    {
        "icon": "analytics",
        "title": "Analyze data",
        "description": "Work with tables and datasets",
        "semantic": "data_analysis",
    },
    {
        "icon": "school",
        "title": "Study and learn",
        "description": "Get step-by-step explanations",
        "semantic": "study_mode",
    },
    {
        "icon": "code",
        "title": "Code",
        "description": "Write, explain, and debug code",
        "semantic": "coding",
    },
]


USER_MESSAGES = [
    "Can you help me analyze this project?",
    "How should I improve this implementation?",
    "Can you explain this code?",
    "Let's continue working on the interface.",
]


ASSISTANT_MESSAGES = [
    (
        "Sure. We can continue by separating the shared "
        "infrastructure from the page-specific components."
    ),
    (
        "The current structure is a good starting point. "
        "The next useful step is to add more interface states."
    ),
    (
        "We can build this so the same renderer handles "
        "different responsive layouts and annotation profiles."
    ),
]


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    result = []

    for label in [
        "Today",
        "Yesterday",
        "Previous 7 days",
    ]:

        items = []

        for index in range(
            random.randint(
                2,
                5,
            )
        ):

            items.append({
                "title":
                    fake.sentence(
                        nb_words=random.randint(
                            2,
                            5,
                        )
                    ).rstrip("."),

                "active":
                    (
                        label == "Today"
                        and index == 0
                    ),
            })

        result.append({
            "label":
                label,

            "items":
                items,
        })

    return result


# ==========================================================
# Messages
# ==========================================================

def generate_messages() -> list[dict]:

    return [
        {
            "role":
                "user",

            "content":
                random.choice(
                    USER_MESSAGES
                ),
        },

        {
            "role":
                "assistant",

            "content":
                random.choice(
                    ASSISTANT_MESSAGES
                ),
        },

        {
            "role":
                "user",

            "content":
                "Can we add another interaction state?",
        },

        {
            "role":
                "assistant",

            "content":
                (
                    "Yes. An open tools menu is useful because "
                    "it introduces a floating overlay while the "
                    "conversation remains visible behind it."
                ),
        },
    ]


# ==========================================================
# Popup Tools
# ==========================================================

def generate_tools() -> list[dict]:

    count = random.randint(
        4,
        len(
            TOOL_OPTIONS
        ),
    )

    selected = random.sample(
        TOOL_OPTIONS,
        k=count,
    )

    return [
        {
            **tool,

            "badge":
                random.choice([
                    None,
                    None,
                    None,
                    "New",
                ]),
        }
        for tool in selected
    ]


# ==========================================================
# Generator
# ==========================================================

def generate_tools_popup_data() -> dict:

    user_name = fake.first_name()

    popup_variant = random.choice([
        "tools",
        "attachments",
    ])

    return {

        "page_variant":
            "tools_popup",

        "model": {
            "name":
                random.choice([
                    "ChatGPT",
                    "GPT-5",
                    "GPT-5 Thinking",
                ]),
        },

        "user": {
            "name":
                user_name,

            "initials":
                user_name[:1].upper(),
        },

        "history_sections":
            generate_history(),

        "messages":
            generate_messages(),

        "popup": {

            "variant":
                popup_variant,

            "title":
                (
                    "Tools"
                    if popup_variant == "tools"
                    else "Add to your message"
                ),

            "tools":
                generate_tools(),
        },

        "composer": {

            "placeholder":
                random.choice([
                    "Ask anything",
                    "Reply to ChatGPT",
                    "Message ChatGPT",
                ]),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_tools_popup_data()
    )