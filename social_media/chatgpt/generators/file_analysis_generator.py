from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# File Types
# ==========================================================

FILE_TYPES = [
    {
        "extension": "pdf",
        "icon": "picture_as_pdf",
        "label": "PDF",
    },
    {
        "extension": "docx",
        "icon": "description",
        "label": "Document",
    },
    {
        "extension": "csv",
        "icon": "table",
        "label": "Spreadsheet",
    },
    {
        "extension": "txt",
        "icon": "article",
        "label": "Text",
    },
]


FILE_NAMES = [
    "research_paper",
    "experiment_results",
    "project_requirements",
    "dataset_summary",
    "training_report",
    "meeting_notes",
    "design_specification",
    "literature_review",
    "evaluation_results",
    "system_architecture",
]


ANALYSIS_ACTIONS = [
    {
        "icon": "summarize",
        "title": "Summarize",
        "prompt": "Give me a concise summary of this file.",
    },
    {
        "icon": "format_list_bulleted",
        "title": "Key points",
        "prompt": "Extract the most important points.",
    },
    {
        "icon": "quiz",
        "title": "Ask questions",
        "prompt": "Help me understand this document.",
    },
    {
        "icon": "analytics",
        "title": "Analyze",
        "prompt": "Analyze the main findings and patterns.",
    },
    {
        "icon": "compare_arrows",
        "title": "Compare",
        "prompt": "Compare the major sections and conclusions.",
    },
    {
        "icon": "fact_check",
        "title": "Review",
        "prompt": "Review the document for issues or inconsistencies.",
    },
]


ASSISTANT_RESPONSES = [
    (
        "I can help analyze this file. You can ask for a summary, "
        "key findings, specific sections, or a comparison."
    ),
    (
        "The file is ready. I can extract important details, "
        "summarize its contents, or answer questions about it."
    ),
    (
        "I’ve received the document. What would you like to "
        "focus on first?"
    ),
]


# ==========================================================
# File Generator
# ==========================================================

def generate_file(
    index: int,
) -> dict:

    file_type = random.choice(
        FILE_TYPES
    )

    base_name = random.choice(
        FILE_NAMES
    )

    size_value = random.uniform(
        0.4,
        18.0,
    )

    progress = random.choice([
        100,
        100,
        100,
        random.randint(
            25,
            95,
        ),
    ])

    return {

        "id":
            f"file_{index}",

        "name":
            (
                f"{base_name}_"
                f"{random.randint(1, 99)}."
                f"{file_type['extension']}"
            ),

        "extension":
            file_type["extension"],

        "type_label":
            file_type["label"],

        "icon":
            file_type["icon"],

        "size":
            f"{size_value:.1f} MB",

        "progress":
            progress,

        "complete":
            progress >= 100,
    }


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

        for _ in range(
            random.randint(
                2,
                4,
            )
        ):

            items.append({

                "title":
                    random.choice([
                        "Document analysis",
                        "Research notes",
                        "Dataset review",
                        "Experiment results",
                        "Code debugging",
                        "Paper summary",
                        "Project planning",
                    ]),

                "active":
                    False,
            })

        result.append({

            "label":
                label,

            "items":
                items,
        })

    if result:
        result[0]["items"][0]["active"] = True

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_file_analysis_data() -> dict:

    file_count = random.randint(
        1,
        3,
    )

    files = [

        generate_file(
            index
        )

        for index in range(
            file_count
        )
    ]


    action_count = random.randint(
        4,
        6,
    )

    actions = random.sample(
        ANALYSIS_ACTIONS,
        k=action_count,
    )


    user_name = fake.first_name()


    return {

        "page_variant":
            "file_analysis",

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

        "files":
            files,

        "analysis_actions":
            actions,

        "assistant_message":
            random.choice(
                ASSISTANT_RESPONSES
            ),

        "composer": {

            "placeholder":
                random.choice([
                    "Ask about these files",
                    "Ask anything about the document",
                    "Message ChatGPT",
                ]),

            "show_web":
                random.random() < 0.4,

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
        generate_file_analysis_data()
    )