from __future__ import annotations

import random


# ==========================================================
# Welcome States
# ==========================================================

WELCOME_STATES = [
    "recent_projects",
    "new_project",
    "clone_repository",
    "remote_development",
    "onboarding",
]


# ==========================================================
# Recent Projects
# ==========================================================

RECENT_PROJECTS = [
    {
        "name": "gui_detector",
        "path": "~/projects/gui_detector",
        "last_opened": "Today",
        "icon": "code",
    },
    {
        "name": "synthetic_ui",
        "path": "~/research/synthetic_ui",
        "last_opened": "Yesterday",
        "icon": "dashboard",
    },
    {
        "name": "vision_lab",
        "path": "~/projects/vision_lab",
        "last_opened": "3 days ago",
        "icon": "visibility",
    },
    {
        "name": "ml_pipeline",
        "path": "~/workspace/ml_pipeline",
        "last_opened": "Last week",
        "icon": "account_tree",
    },
    {
        "name": "annotation_tools",
        "path": "~/research/annotation_tools",
        "last_opened": "2 weeks ago",
        "icon": "draw",
    },
]


# ==========================================================
# Project Templates
# ==========================================================

PROJECT_TEMPLATES = [
    {
        "id": "pure_python",
        "name": "Pure Python",
        "description": (
            "Create a Python project using "
            "a virtual environment."
        ),
        "icon": "code",
    },
    {
        "id": "django",
        "name": "Django",
        "description": (
            "Create a web application "
            "using the Django framework."
        ),
        "icon": "language",
    },
    {
        "id": "flask",
        "name": "Flask",
        "description": (
            "Create a lightweight "
            "Flask web project."
        ),
        "icon": "web",
    },
    {
        "id": "fastapi",
        "name": "FastAPI",
        "description": (
            "Create a modern Python "
            "API application."
        ),
        "icon": "api",
    },
    {
        "id": "jupyter",
        "name": "Jupyter",
        "description": (
            "Create a project for "
            "interactive notebooks."
        ),
        "icon": "analytics",
    },
]


# ==========================================================
# Remote Providers
# ==========================================================

REMOTE_PROVIDERS = [
    {
        "name": "SSH",
        "description": (
            "Connect to a remote machine "
            "and open a project over SSH."
        ),
        "icon": "terminal",
    },
    {
        "name": "WSL",
        "description": (
            "Develop using a Linux "
            "environment on Windows."
        ),
        "icon": "computer",
    },
    {
        "name": "Dev Container",
        "description": (
            "Open a project inside "
            "a configured development container."
        ),
        "icon": "deployed_code",
    },
    {
        "name": "JetBrains Gateway",
        "description": (
            "Connect to a remote IDE "
            "backend."
        ),
        "icon": "cloud",
    },
]


# ==========================================================
# Onboarding Cards
# ==========================================================

ONBOARDING_STEPS = [
    {
        "title": "Learn the Basics",
        "description": (
            "Explore navigation, search, "
            "editing, and shortcuts."
        ),
        "icon": "school",
    },
    {
        "title": "Customize PyCharm",
        "description": (
            "Choose a theme, keymap, "
            "font, and editor appearance."
        ),
        "icon": "palette",
    },
    {
        "title": "Configure Python",
        "description": (
            "Select an interpreter "
            "or create a virtual environment."
        ),
        "icon": "deployed_code",
    },
    {
        "title": "Version Control",
        "description": (
            "Connect Git and start "
            "working with repositories."
        ),
        "icon": "account_tree",
    },
]


# ==========================================================
# Recent Projects State
# ==========================================================

def generate_recent_projects_state() -> dict:

    count = random.randint(
        3,
        len(RECENT_PROJECTS),
    )

    projects = random.sample(
        RECENT_PROJECTS,
        k=count,
    )

    return {
        "projects": projects,
        "selected_index": random.randrange(
            len(projects)
        ),
        "search_query": random.choice(
            [
                "",
                "",
                "gui",
                "research",
            ]
        ),
    }


# ==========================================================
# New Project State
# ==========================================================

def generate_new_project_state() -> dict:

    selected_template = random.choice(
        PROJECT_TEMPLATES
    )

    return {
        "templates": PROJECT_TEMPLATES,
        "selected_template": selected_template["id"],
        "project_name": random.choice(
            [
                "new_project",
                "python_app",
                "research_tool",
                "demo_project",
            ]
        ),
        "location": random.choice(
            [
                "~/PycharmProjects",
                "~/projects",
                "~/workspace",
            ]
        ),
        "interpreter": random.choice(
            [
                "New Virtualenv",
                "Python 3.11",
                "Python 3.12",
                "Conda",
            ]
        ),
        "create_git": random.choice(
            [
                True,
                False,
            ]
        ),
        "create_readme": random.choice(
            [
                True,
                False,
            ]
        ),
    }


# ==========================================================
# Clone Repository State
# ==========================================================

def generate_clone_repository_state() -> dict:

    return {
        "url": random.choice(
            [
                "https://github.com/user/project.git",
                "git@github.com:user/research.git",
                "https://gitlab.com/team/gui-tools.git",
            ]
        ),
        "directory": random.choice(
            [
                "~/projects/project",
                "~/workspace/research",
                "~/PycharmProjects/gui-tools",
            ]
        ),
        "provider": random.choice(
            [
                "GitHub",
                "GitLab",
                "Generic Git",
            ]
        ),
        "recent_repositories": [
            {
                "name": "synthetic-ui",
                "owner": "research-lab",
            },
            {
                "name": "gui-detector",
                "owner": "research-lab",
            },
            {
                "name": "dataset-tools",
                "owner": "ml-team",
            },
        ],
    }


# ==========================================================
# Remote Development State
# ==========================================================

def generate_remote_development_state() -> dict:

    return {
        "providers": REMOTE_PROVIDERS,
        "selected_index": random.randrange(
            len(REMOTE_PROVIDERS)
        ),
        "recent_connections": [
            {
                "name": "gpu-server-01",
                "address": "192.168.10.21",
            },
            {
                "name": "research-node",
                "address": "research.example",
            },
        ],
    }


# ==========================================================
# Onboarding State
# ==========================================================

def generate_onboarding_state() -> dict:

    return {
        "steps": ONBOARDING_STEPS,
        "progress": random.choice(
            [
                25,
                50,
                75,
            ]
        ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_welcome_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            WELCOME_STATES
        )
    )

    if selected_state not in WELCOME_STATES:

        raise ValueError(
            f"Unknown welcome state: "
            f"{selected_state}"
        )

    result = {

        "state":
            selected_state,

        "version":
            random.choice(
                [
                    "2025.1",
                    "2025.2",
                    "2026.1",
                ]
            ),
    }


    if selected_state == "recent_projects":

        result["recent_projects"] = (
            generate_recent_projects_state()
        )

    elif selected_state == "new_project":

        result["new_project"] = (
            generate_new_project_state()
        )

    elif selected_state == "clone_repository":

        result["clone_repository"] = (
            generate_clone_repository_state()
        )

    elif selected_state == "remote_development":

        result["remote_development"] = (
            generate_remote_development_state()
        )

    elif selected_state == "onboarding":

        result["onboarding"] = (
            generate_onboarding_state()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in WELCOME_STATES:

        print(
            "\n=============================="
        )

        print(
            state.upper()
        )

        print(
            "=============================="
        )

        pprint.pp(
            generate_welcome_data(
                state=state
            )
        )