from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Conversation Topics
# ==========================================================

TOPICS = [
    "responsive web design",
    "Python debugging",
    "machine learning",
    "UI accessibility",
    "REST API design",
    "synthetic datasets",
    "database optimization",
    "research paper writing",
    "computer vision",
    "frontend architecture",
]


USER_QUESTIONS = [
    "Can you explain this step by step?",
    "Can you show me an example implementation?",
    "Why does this code fail on smaller screens?",
    "How should I structure this project?",
    "Can you improve this approach?",
    "What would be a better implementation?",
    "How can I make this more responsive?",
    "Can you help me debug this?",
]


ASSISTANT_INTROS = [
    "Yes. The main issue is the way the layout is currently structured.",
    "A good way to approach this is to separate the problem into a few parts.",
    "You can solve this cleanly by keeping the shared logic separate from the page-specific implementation.",
    "The structure is mostly correct, but there are a few details worth changing.",
    "The simplest approach is to make the layout responsive at the container level.",
]


CODE_SNIPPETS = [
    """def calculate_total(values):
    total = 0

    for value in values:
        total += value

    return total
""",

    """.page-container {
    width: min(100% - 32px, 960px);
    margin-inline: auto;
}

@media (max-width: 767px) {
    .page-container {
        width: 100%;
        padding: 0 16px;
    }
}
""",

    """async def load_data():
    response = await fetch("/api/items")

    if not response.ok:
        raise RuntimeError("Request failed")

    return await response.json()
""",

    """from pathlib import Path

ROOT = Path(__file__).resolve().parent

OUTPUT_DIR = (
    ROOT
    / "output"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
""",
]


SOURCE_TITLES = [
    "Responsive layout documentation",
    "Accessibility guidelines",
    "Python documentation",
    "Frontend design patterns",
    "UI implementation notes",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_user_message(
    index: int,
) -> dict:

    return {
        "id":
            f"user_{index}",

        "role":
            "user",

        "content":
            random.choice(
                USER_QUESTIONS
            ),

        "timestamp":
            fake.time(
                pattern="%H:%M"
            ),

        "show_edit":
            random.random() < 0.35,
    }


def generate_text_block() -> dict:

    return {
        "type":
            "paragraph",

        "text":
            random.choice(
                ASSISTANT_INTROS
            ),
    }


def generate_list_block() -> dict:

    item_count = random.randint(
        3,
        5,
    )

    items = []

    options = [
        "Keep shared rendering logic in the common renderer.",
        "Use semantic annotation names for page-specific meaning.",
        "Avoid hard-coded dimensions where responsive layout is required.",
        "Keep the main content width constrained on large screens.",
        "Use sticky elements only when they are genuinely needed.",
        "Clip annotations when elements are partially hidden.",
        "Test the layout at compact, medium, and expanded widths.",
    ]

    for item in random.sample(
        options,
        k=item_count,
    ):

        items.append(
            item
        )

    return {
        "type":
            "list",

        "items":
            items,
    }


def generate_code_block() -> dict:

    return {
        "type":
            "code",

        "language":
            random.choice([
                "python",
                "css",
                "javascript",
            ]),

        "code":
            random.choice(
                CODE_SNIPPETS
            ),

        "show_copy":
            True,
    }


def generate_source_block() -> dict:

    source_count = random.randint(
        2,
        4,
    )

    sources = []

    for index in range(
        source_count
    ):

        sources.append({
            "id":
                f"source_{index}",

            "title":
                random.choice(
                    SOURCE_TITLES
                ),

            "domain":
                fake.domain_name(),
        })

    return {
        "type":
            "sources",

        "sources":
            sources,
    }


def generate_assistant_message(
    index: int,
) -> dict:

    blocks = [
        generate_text_block(),
    ]

    if random.random() < 0.80:
        blocks.append(
            generate_list_block()
        )

    if random.random() < 0.75:
        blocks.append(
            generate_code_block()
        )

    if random.random() < 0.45:
        blocks.append(
            generate_source_block()
        )

    if random.random() < 0.70:

        blocks.append({
            "type":
                "paragraph",

            "text":
                (
                    "This keeps the page-specific UI flexible "
                    "while preserving the same annotation and "
                    "export pipeline."
                ),
        })

    return {
        "id":
            f"assistant_{index}",

        "role":
            "assistant",

        "blocks":
            blocks,

        "show_actions":
            True,
    }


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    sections = []

    labels = [
        "Today",
        "Yesterday",
        "Previous 7 days",
    ]

    for label in labels:

        count = random.randint(
            2,
            5,
        )

        items = []

        for index in range(
            count
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
                    False,
            })

        sections.append({
            "label":
                label,

            "items":
                items,
        })

    if sections:
        sections[0]["items"][0]["active"] = True

    return sections


# ==========================================================
# Generator
# ==========================================================

def generate_conversation_data() -> dict:

    topic = random.choice(
        TOPICS
    )

    message_count = random.randint(
        4,
        7,
    )

    messages = []

    for index in range(
        message_count
    ):

        messages.append(
            generate_user_message(
                index
            )
        )

        messages.append(
            generate_assistant_message(
                index
            )
        )

    return {

        "title":
            topic.title(),

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
                fake.first_name(),

            "initials":
                fake.first_name()[0].upper(),
        },

        "history_sections":
            generate_history(),

        "messages":
            messages,

        "composer": {
            "placeholder":
                random.choice([
                    "Ask anything",
                    "Reply to ChatGPT",
                    "Message ChatGPT",
                ]),

            "show_tools":
                True,

            "show_voice":
                True,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_conversation_data()
    )