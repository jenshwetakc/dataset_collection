from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Project Names
# ==========================================================

PROJECT_NAMES = [
    "Synthetic GUI Dataset",
    "Research Paper",
    "Model Evaluation",
    "Accessibility Study",
    "UI Detection Pipeline",
    "Experiment Analysis",
    "Training Dashboard",
    "Dataset Annotation",
    "System Design",
    "Literature Review",
    "Presentation Project",
    "Frontend Prototype",
]


# ==========================================================
# Project Descriptions
# ==========================================================

PROJECT_DESCRIPTIONS = [
    (
        "Generate and organize synthetic user interface "
        "screens for model training and evaluation."
    ),
    (
        "Collect notes, drafts, references, and analysis "
        "for an ongoing research project."
    ),
    (
        "Track experiments, model results, and evaluation "
        "metrics across different configurations."
    ),
    (
        "Organize accessibility findings and compare "
        "interface behavior across themes."
    ),
    (
        "Plan implementation tasks and keep technical "
        "documentation in one workspace."
    ),
]


# ==========================================================
# File Names
# ==========================================================

FILE_NAMES = [
    "experiment_results.csv",
    "research_notes.pdf",
    "dataset_summary.docx",
    "evaluation_report.pdf",
    "architecture.md",
    "training_metrics.csv",
    "annotations.json",
    "presentation.pptx",
    "requirements.docx",
    "meeting_notes.txt",
]


# ==========================================================
# File Icons
# ==========================================================

FILE_TYPES = {
    "pdf": "picture_as_pdf",
    "csv": "table",
    "docx": "description",
    "pptx": "slideshow",
    "json": "data_object",
    "md": "article",
    "txt": "article",
}


# ==========================================================
# Activity Messages
# ==========================================================

ACTIVITY_MESSAGES = [
    "uploaded a new file",
    "updated the project instructions",
    "added a project member",
    "created a new conversation",
    "renamed the project",
    "added new research notes",
    "updated the dataset summary",
    "reviewed recent results",
]


# ==========================================================
# Project Colors
# ==========================================================

PROJECT_VISUALS = [
    "project-a",
    "project-b",
    "project-c",
    "project-d",
    "project-e",
    "project-f",
]


# ==========================================================
# Generate User
# ==========================================================

def generate_person() -> dict:

    name = fake.name()

    initials = "".join(
        part[0]
        for part in name.split()[:2]
    ).upper()

    return {

        "name":
            name,

        "initials":
            initials,

        "email":
            fake.email(),
    }


# ==========================================================
# Generate Project
# ==========================================================

def generate_project(
    index: int,
) -> dict:

    progress = random.randint(
        20,
        100,
    )

    member_count = random.randint(
        1,
        8,
    )

    return {

        "id":
            f"project_{index}",

        "name":
            random.choice(
                PROJECT_NAMES
            ),

        "description":
            random.choice(
                PROJECT_DESCRIPTIONS
            ),

        "visual":
            random.choice(
                PROJECT_VISUALS
            ),

        "progress":
            progress,

        "member_count":
            member_count,

        "file_count":
            random.randint(
                2,
                24,
            ),

        "conversation_count":
            random.randint(
                1,
                18,
            ),

        "updated":
            random.choice([
                "Just now",
                "12 min ago",
                "1 hour ago",
                "Yesterday",
                "2 days ago",
                "Last week",
            ]),

        "favorite":
            random.random()
            < 0.18,
    }


# ==========================================================
# Generate Recent File
# ==========================================================

def generate_file(
    index: int,
) -> dict:

    name = random.choice(
        FILE_NAMES
    )

    extension = (
        name
        .rsplit(
            ".",
            1,
        )[-1]
        .lower()
    )

    return {

        "id":
            f"file_{index}",

        "name":
            name,

        "icon":
            FILE_TYPES.get(
                extension,
                "description",
            ),

        "size":
            (
                f"{random.uniform(0.2, 12.0):.1f} MB"
            ),

        "updated":
            random.choice([
                "Just now",
                "8 min ago",
                "35 min ago",
                "Yesterday",
                "2 days ago",
            ]),
    }


# ==========================================================
# Generate Activity
# ==========================================================

def generate_activity(
    index: int,
) -> dict:

    person = (
        generate_person()
    )

    return {

        "id":
            f"activity_{index}",

        "person":
            person,

        "action":
            random.choice(
                ACTIVITY_MESSAGES
            ),

        "timestamp":
            random.choice([
                "2 min ago",
                "12 min ago",
                "1 hour ago",
                "3 hours ago",
                "Yesterday",
            ]),
    }


# ==========================================================
# Sidebar History
# ==========================================================

def generate_history() -> list[dict]:

    groups = []

    titles = [
        "Dataset planning",
        "Paper revision",
        "Model training",
        "UI implementation",
        "Experiment notes",
        "Project review",
        "Debugging session",
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
# Main Generator
# ==========================================================

def generate_projects_data() -> dict:

    user = (
        generate_person()
    )

    projects = [

        generate_project(
            index
        )

        for index in range(
            random.randint(
                6,
                10,
            )
        )
    ]

    members = [

        generate_person()

        for _ in range(
            random.randint(
                3,
                6,
            )
        )
    ]

    recent_files = [

        generate_file(
            index
        )

        for index in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    activities = [

        generate_activity(
            index
        )

        for index in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    return {

        "page_variant":
            "projects",

        "user":
            user,

        "history_sections":
            generate_history(),

        "projects":
            projects,

        "members":
            members,

        "recent_files":
            recent_files,

        "activities":
            activities,

        "filters": [

            {
                "id":
                    "all",

                "label":
                    "All projects",

                "selected":
                    True,
            },

            {
                "id":
                    "recent",

                "label":
                    "Recent",

                "selected":
                    False,
            },

            {
                "id":
                    "shared",

                "label":
                    "Shared",

                "selected":
                    False,
            },

            {
                "id":
                    "favorites",

                "label":
                    "Favorites",

                "selected":
                    False,
            },
        ],

        "summary": {

            "project_count":
                len(
                    projects
                ),

            "file_count":
                sum(
                    project["file_count"]
                    for project in projects
                ),

            "member_count":
                len(
                    members
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_projects_data()
    )