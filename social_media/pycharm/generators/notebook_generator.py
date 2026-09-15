from __future__ import annotations

import random

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)


# ==========================================================
# Notebook States
# ==========================================================

NOTEBOOK_STATES = [
    "editing",
    "running",
    "table_output",
    "error_output",
    "markdown_preview",
]


# ==========================================================
# Notebook Files
# ==========================================================

NOTEBOOK_FILES = [
    "dataset_analysis.ipynb",
    "experiment_results.ipynb",
    "gui_statistics.ipynb",
    "model_evaluation.ipynb",
    "viewport_analysis.ipynb",
]


# ==========================================================
# Code Cells
# ==========================================================

CODE_CELLS = [
    [
        "import pandas as pd",
        "import numpy as np",
        "",
        "df = pd.read_csv('samples.csv')",
        "df.head()",
    ],

    [
        "viewport_counts = (",
        "    df.groupby('viewport')",
        "      .size()",
        "      .sort_values(ascending=False)",
        ")",
        "",
        "viewport_counts",
    ],

    [
        "annotation_counts = df[",
        "    'annotation_count'",
        "].describe()",
        "",
        "annotation_counts",
    ],

    [
        "valid = df[df['status'] == 'ready']",
        "",
        "print(",
        "    f'Ready samples: {len(valid)}'",
        ")",
    ],

    [
        "classes = [",
        "    'button',",
        "    'icon',",
        "    'text',",
        "    'card',",
        "]",
        "",
        "classes",
    ],
]


# ==========================================================
# Markdown Content
# ==========================================================

MARKDOWN_CELLS = [
    {
        "title": "Synthetic GUI Dataset Analysis",
        "body": (
            "This notebook summarizes generated interface samples, "
            "annotation counts, viewport coverage, and rendering quality."
        ),
    },
    {
        "title": "Experiment Results",
        "body": (
            "The following cells compare different viewport categories "
            "and inspect the resulting annotation distributions."
        ),
    },
    {
        "title": "Viewport Coverage",
        "body": (
            "We evaluate compact, medium, and expanded layouts to ensure "
            "the synthetic dataset contains substantial structural diversity."
        ),
    },
]


# ==========================================================
# Table Output
# ==========================================================

TABLE_ROWS = [
    {
        "viewport": "standard_iphone",
        "samples": 1240,
        "annotations": 18420,
        "status": "ready",
    },
    {
        "viewport": "tablet_portrait",
        "samples": 1180,
        "annotations": 21340,
        "status": "ready",
    },
    {
        "viewport": "laptop",
        "samples": 1320,
        "annotations": 28920,
        "status": "ready",
    },
    {
        "viewport": "desktop_fhd",
        "samples": 1260,
        "annotations": 31540,
        "status": "ready",
    },
]


# ==========================================================
# Error Variants
# ==========================================================

ERROR_VARIANTS = [
    {
        "type": "KeyError",
        "message": "'viewport'",
        "file": "dataset_analysis.ipynb",
        "line": 18,
        "trace": [
            "Cell In[4], line 3",
            "viewport = sample['viewport']",
            "KeyError: 'viewport'",
        ],
    },
    {
        "type": "TypeError",
        "message": "object of type 'NoneType' has no len()",
        "file": "experiment_results.ipynb",
        "line": 27,
        "trace": [
            "Cell In[7], line 5",
            "count = len(result)",
            "TypeError: object of type 'NoneType' has no len()",
        ],
    },
    {
        "type": "ValueError",
        "message": "invalid annotation profile",
        "file": "gui_statistics.ipynb",
        "line": 42,
        "trace": [
            "Cell In[9], line 2",
            "resolve_profile(profile)",
            "ValueError: invalid annotation profile",
        ],
    },
]


# ==========================================================
# Generate Notebook Cell
# ==========================================================

def generate_code_cell(
    index: int,
) -> dict:

    code = random.choice(
        CODE_CELLS
    )

    return {
        "id":
            f"cell_{index}",

        "execution_count":
            random.randint(
                1,
                20,
            ),

        "lines": [
            {
                "number":
                    line_index + 1,

                "content":
                    content,
            }
            for line_index, content
            in enumerate(code)
        ],

        "selected":
            False,
    }


# ==========================================================
# Editing
# ==========================================================

def generate_editing_state() -> dict:

    cells = [
        generate_code_cell(0),
        generate_code_cell(1),
        generate_code_cell(2),
    ]

    selected_index = random.randrange(
        len(cells)
    )

    cells[selected_index]["selected"] = True

    return {
        "cells": cells,
        "selected_index": selected_index,
    }


# ==========================================================
# Running
# ==========================================================

def generate_running_state() -> dict:

    cells = [
        generate_code_cell(0),
        generate_code_cell(1),
        generate_code_cell(2),
    ]

    running_index = random.randrange(
        len(cells)
    )

    return {
        "cells": cells,
        "running_index": running_index,
        "kernel": random.choice(
            [
                "Python 3.10",
                "Python 3.11",
                "Python 3.12",
            ]
        ),
        "elapsed": random.choice(
            [
                "1.4 s",
                "3.8 s",
                "8.2 s",
                "12.7 s",
            ]
        ),
    }


# ==========================================================
# Table
# ==========================================================

def generate_table_output_state() -> dict:

    return {
        "cell": generate_code_cell(0),
        "rows": TABLE_ROWS,
        "row_count": len(TABLE_ROWS),
    }


# ==========================================================
# Error
# ==========================================================

def generate_error_output_state() -> dict:

    return {
        "cell": generate_code_cell(0),
        "error": random.choice(
            ERROR_VARIANTS
        ),
    }


# ==========================================================
# Markdown
# ==========================================================

def generate_markdown_state() -> dict:

    return {
        "markdown": random.choice(
            MARKDOWN_CELLS
        ),
        "code_cell": generate_code_cell(1),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_notebook_data(
    state: str | None = None,
) -> dict:

    editor = generate_editor_data()

    selected_state = (
        state
        if state is not None
        else random.choice(
            NOTEBOOK_STATES
        )
    )

    if selected_state not in NOTEBOOK_STATES:

        raise ValueError(
            f"Unknown notebook state: "
            f"{selected_state}"
        )

    result = {
        **editor,

        "notebook_state":
            selected_state,

        "filename":
            random.choice(
                NOTEBOOK_FILES
            ),

        "kernel":
            random.choice(
                [
                    "Python 3.10",
                    "Python 3.11",
                    "Python 3.12",
                ]
            ),

        "trusted":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


    if selected_state == "editing":

        result["editing"] = (
            generate_editing_state()
        )

    elif selected_state == "running":

        result["running"] = (
            generate_running_state()
        )

    elif selected_state == "table_output":

        result["table_output"] = (
            generate_table_output_state()
        )

    elif selected_state == "error_output":

        result["error_output"] = (
            generate_error_output_state()
        )

    elif selected_state == "markdown_preview":

        result["markdown_preview"] = (
            generate_markdown_state()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in NOTEBOOK_STATES:

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
            generate_notebook_data(
                state=state
            )
        )