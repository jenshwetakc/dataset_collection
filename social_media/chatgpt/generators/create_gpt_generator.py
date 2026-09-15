from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# GPT Names
# ==========================================================

GPT_NAMES = [
    "Research Companion",
    "Dataset Assistant",
    "Code Reviewer",
    "Academic Writing Helper",
    "UI Design Assistant",
    "Experiment Analyst",
    "Study Mentor",
    "Paper Reviewer",
    "Accessibility Assistant",
    "Project Planner",
]


# ==========================================================
# Descriptions
# ==========================================================

GPT_DESCRIPTIONS = [
    (
        "Helps organize research questions, summarize papers, "
        "and explain technical concepts."
    ),
    (
        "Assists with dataset preparation, annotation review, "
        "and experiment planning."
    ),
    (
        "Reviews code, explains bugs, and suggests practical "
        "implementation improvements."
    ),
    (
        "Helps improve academic writing, structure arguments, "
        "and refine research documents."
    ),
    (
        "Reviews interface layouts and suggests improvements "
        "for usability and accessibility."
    ),
]


# ==========================================================
# Instructions
# ==========================================================

GPT_INSTRUCTIONS = [
    (
        "You are a research assistant. Give structured, concise "
        "answers. Explain technical concepts clearly and provide "
        "step-by-step guidance when implementation is required."
    ),
    (
        "You are an expert software assistant. Focus on practical "
        "solutions, readable code, debugging, and implementation "
        "details. Avoid unnecessary complexity."
    ),
    (
        "You help users analyze datasets and experiments. Explain "
        "results, identify possible issues, and suggest next steps."
    ),
]


# ==========================================================
# Conversation Starters
# ==========================================================

STARTER_OPTIONS = [
    "Help me summarize this research paper",
    "Review this implementation",
    "Analyze these experiment results",
    "Help me structure my dataset",
    "Explain this concept simply",
    "Review this UI design",
    "Suggest the next implementation step",
    "Help me debug this code",
]


# ==========================================================
# Capability Definitions
# ==========================================================

CAPABILITIES = [
    {
        "id": "web",
        "title": "Web search",
        "description": "Search the web for current information.",
        "icon": "language",
    },
    {
        "id": "image",
        "title": "Image generation",
        "description": "Create and edit images.",
        "icon": "image",
    },
    {
        "id": "code",
        "title": "Code interpreter",
        "description": "Run code and analyze files.",
        "icon": "terminal",
    },
    {
        "id": "canvas",
        "title": "Document workspace",
        "description": "Work with longer structured content.",
        "icon": "article",
    },
]


# ==========================================================
# Knowledge Files
# ==========================================================

KNOWLEDGE_FILES = [
    {
        "name": "research_guidelines.pdf",
        "type": "PDF",
        "icon": "picture_as_pdf",
    },
    {
        "name": "dataset_specification.docx",
        "type": "Document",
        "icon": "description",
    },
    {
        "name": "experiment_results.csv",
        "type": "Spreadsheet",
        "icon": "table",
    },
    {
        "name": "project_notes.txt",
        "type": "Text",
        "icon": "article",
    },
    {
        "name": "evaluation_metrics.json",
        "type": "JSON",
        "icon": "data_object",
    },
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
        "Model evaluation",
        "Code debugging",
        "Paper analysis",
    ]

    for label in [
        "Today",
        "Yesterday",
        "Previous 7 days",
    ]:

        items = []

        for _ in range(
            random.randint(
                2,
                4,
            )
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
# Capabilities
# ==========================================================

def generate_capabilities() -> list[dict]:

    result = []

    for capability in CAPABILITIES:

        result.append({
            **capability,

            "enabled":
                random.random()
                < 0.65,
        })

    return result


# ==========================================================
# Knowledge
# ==========================================================

def generate_knowledge_files() -> list[dict]:

    count = random.randint(
        1,
        4,
    )

    selected = random.sample(
        KNOWLEDGE_FILES,
        k=count,
    )

    result = []

    for index, item in enumerate(
        selected
    ):

        result.append({
            "id":
                f"knowledge_{index}",

            **item,

            "size":
                f"{random.uniform(0.4, 8.5):.1f} MB",
        })

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_create_gpt_data() -> dict:

    user_name = fake.name()

    name = random.choice(
        GPT_NAMES
    )

    description = random.choice(
        GPT_DESCRIPTIONS
    )

    instructions = random.choice(
        GPT_INSTRUCTIONS
    )

    starters = random.sample(
        STARTER_OPTIONS,
        k=random.randint(
            3,
            4,
        ),
    )

    return {

        "page_variant":
            "create_gpt",

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

        "tabs": [
            {
                "id": "configure",
                "label": "Configure",
                "selected": True,
            },
            {
                "id": "create",
                "label": "Create",
                "selected": False,
            },
        ],

        "gpt": {

            "name":
                name,

            "description":
                description,

            "instructions":
                instructions,

            "icon":
                random.choice([
                    "smart_toy",
                    "science",
                    "auto_awesome",
                    "school",
                    "code",
                ]),

            "visibility":
                random.choice([
                    "Only me",
                    "Anyone with the link",
                    "Public",
                ]),

            "conversation_starters":
                starters,

            "capabilities":
                generate_capabilities(),

            "knowledge_files":
                generate_knowledge_files(),
        },

        "preview_messages": [
            {
                "role": "assistant",
                "text":
                    (
                        f"Hi! I'm {name}. "
                        "How can I help you today?"
                    ),
            },
            {
                "role": "user",
                "text":
                    random.choice(
                        starters
                    ),
            },
            {
                "role": "assistant",
                "text":
                    (
                        "Absolutely. I can help with that. "
                        "Share the relevant details and I'll "
                        "work through it with you."
                    ),
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_create_gpt_data()
    )