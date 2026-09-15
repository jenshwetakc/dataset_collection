from __future__ import annotations

import random


# ==========================================================
# Project Names
# ==========================================================

PROJECT_NAMES = [
    "vision_lab",
    "gui_detector",
    "accessibility_ai",
    "synthetic_ui",
    "ml_pipeline",
    "research_tools",
    "python_workspace",
]


# ==========================================================
# Branches
# ==========================================================

BRANCHES = [
    "main",
    "develop",
    "feature/ui-dataset",
    "experiment",
    "refactor",
]


# ==========================================================
# Python Files
# ==========================================================

PYTHON_FILES = [
    "main.py",
    "train.py",
    "dataset.py",
    "renderer.py",
    "model.py",
    "config.py",
    "utils.py",
    "pipeline.py",
]


# ==========================================================
# Editor States
# ==========================================================

EDITOR_STATES = [
    "normal",
    "modified",
    "warning",
]


# ==========================================================
# Generate File Tree
# ==========================================================

def generate_project_tree(
    project_name: str,
) -> list[dict]:

    return [

        {
            "name": project_name,
            "type": "folder",
            "depth": 0,
            "expanded": True,
        },

        {
            "name": ".idea",
            "type": "folder",
            "depth": 1,
            "expanded": False,
        },

        {
            "name": "src",
            "type": "folder",
            "depth": 1,
            "expanded": True,
        },

        {
            "name": "generators",
            "type": "folder",
            "depth": 2,
            "expanded": True,
        },

        {
            "name": "dataset_generator.py",
            "type": "python",
            "depth": 3,
        },

        {
            "name": "layout_generator.py",
            "type": "python",
            "depth": 3,
        },

        {
            "name": "renderers",
            "type": "folder",
            "depth": 2,
            "expanded": False,
        },

        {
            "name": "models",
            "type": "folder",
            "depth": 2,
            "expanded": False,
        },

        {
            "name": "main.py",
            "type": "python",
            "depth": 2,
        },

        {
            "name": "config.py",
            "type": "python",
            "depth": 2,
        },

        {
            "name": "requirements.txt",
            "type": "text",
            "depth": 1,
        },

        {
            "name": "README.md",
            "type": "markdown",
            "depth": 1,
        },
    ]


# ==========================================================
# Generate Editor Tabs
# ==========================================================

def generate_editor_tabs() -> list[dict]:

    filenames = random.sample(
        PYTHON_FILES,
        k=random.randint(
            2,
            4,
        ),
    )

    active_index = random.randrange(
        len(filenames)
    )

    tabs = []

    for index, filename in enumerate(
        filenames
    ):

        tabs.append(
            {
                "name":
                    filename,

                "active":
                    index
                    == active_index,

                "modified":
                    random.random()
                    < 0.25,
            }
        )

    return tabs


# ==========================================================
# Generate Code
# ==========================================================

def generate_code_lines() -> list[dict]:

    code = [
        (
            "keyword",
            "from pathlib import Path",
        ),
        (
            "plain",
            "",
        ),
        (
            "keyword",
            "from dataset.generator import DatasetGenerator",
        ),
        (
            "keyword",
            "from models.detector import Detector",
        ),
        (
            "plain",
            "",
        ),
        (
            "plain",
            "",
        ),
        (
            "comment",
            "# Configure dataset paths",
        ),
        (
            "plain",
            'DATA_ROOT = Path("data")',
        ),
        (
            "plain",
            'OUTPUT_ROOT = Path("output")',
        ),
        (
            "plain",
            "",
        ),
        (
            "plain",
            "",
        ),
        (
            "keyword",
            "def build_dataset(num_samples: int = 1000):",
        ),
        (
            "plain",
            "    generator = DatasetGenerator(",
        ),
        (
            "plain",
            "        root=DATA_ROOT,",
        ),
        (
            "plain",
            "        output=OUTPUT_ROOT,",
        ),
        (
            "plain",
            "    )",
        ),
        (
            "plain",
            "",
        ),
        (
            "plain",
            "    samples = generator.generate(",
        ),
        (
            "plain",
            "        count=num_samples,",
        ),
        (
            "plain",
            "        validate=True,",
        ),
        (
            "plain",
            "    )",
        ),
        (
            "plain",
            "",
        ),
        (
            "keyword",
            "    return samples",
        ),
        (
            "plain",
            "",
        ),
        (
            "plain",
            "",
        ),
        (
            "keyword",
            'if __name__ == "__main__":',
        ),
        (
            "plain",
            "    dataset = build_dataset(",
        ),
        (
            "plain",
            "        num_samples=5000",
        ),
        (
            "plain",
            "    )",
        ),
        (
            "plain",
            "",
        ),
        (
            "plain",
            '    print(f"Generated {len(dataset)} samples")',
        ),
    ]

    return [
        {
            "number":
                index + 1,

            "type":
                line_type,

            "content":
                content,
        }

        for index, (
            line_type,
            content,
        )
        in enumerate(code)
    ]


# ==========================================================
# Generate Editor Data
# ==========================================================

def generate_editor_data() -> dict:

    project_name = random.choice(
        PROJECT_NAMES
    )

    tabs = generate_editor_tabs()

    active_tab = next(
        tab
        for tab in tabs
        if tab["active"]
    )

    state = random.choice(
        EDITOR_STATES
    )

    return {

        "project_name":
            project_name,

        "window_title":
            (
                f"{active_tab['name']} – "
                f"{project_name}"
            ),

        "branch":
            random.choice(
                BRANCHES
            ),

        "state":
            state,

        "tabs":
            tabs,

        "active_file":
            active_tab["name"],

        "breadcrumbs": [
            project_name,
            "src",
            active_tab["name"],
        ],

        "project_tree":
            generate_project_tree(
                project_name
            ),

        "code_lines":
            generate_code_lines(),

        "interpreter":
            random.choice(
                [
                    "Python 3.10",
                    "Python 3.11",
                    "Python 3.12",
                ]
            ),

        "encoding":
            "UTF-8",

        "line_separator":
            "LF",

        "indent":
            "4 spaces",

        "caret":
            {
                "line":
                    random.randint(
                        12,
                        28,
                    ),

                "column":
                    random.randint(
                        3,
                        24,
                    ),
            },

        "inspection": (
            "2 warnings"
            if state == "warning"
            else "No problems"
        ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_editor_data()
    )