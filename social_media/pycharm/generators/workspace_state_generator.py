from __future__ import annotations

import random

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)


# ==========================================================
# Workspace States
# ==========================================================

WORKSPACE_STATES = [
    "run",
    "debug",
    "terminal",
    "problems",
]


# ==========================================================
# Run Output
# ==========================================================

RUN_OUTPUTS = [

    [
        {
            "type": "command",
            "text": (
                "/usr/bin/python3 "
                "/home/user/project/main.py"
            ),
        },
        {
            "type": "output",
            "text": "Loading dataset...",
        },
        {
            "type": "output",
            "text": "Generated 5000 samples",
        },
        {
            "type": "success",
            "text": (
                "Process finished "
                "with exit code 0"
            ),
        },
    ],

    [
        {
            "type": "command",
            "text": (
                "python train.py "
                "--epochs 20"
            ),
        },
        {
            "type": "output",
            "text": "Device: cuda:0",
        },
        {
            "type": "output",
            "text": "Epoch 1/20 - loss: 0.8421",
        },
        {
            "type": "output",
            "text": "Epoch 2/20 - loss: 0.6218",
        },
        {
            "type": "success",
            "text": "Training started successfully",
        },
    ],

    [
        {
            "type": "command",
            "text": "python renderer.py",
        },
        {
            "type": "output",
            "text": (
                "[FULL] editor | dark | "
                "desktop_fhd"
            ),
        },
        {
            "type": "output",
            "text": "38 annotations",
        },
        {
            "type": "success",
            "text": (
                "Process finished "
                "with exit code 0"
            ),
        },
    ],
]


# ==========================================================
# Terminal Content
# ==========================================================

TERMINAL_SESSIONS = [

    {
        "shell":
            "bash",

        "directory":
            "~/projects/gui_detector",

        "lines": [
            {
                "type": "prompt",
                "text": (
                    "$ python main.py"
                ),
            },
            {
                "type": "output",
                "text": (
                    "Loading configuration..."
                ),
            },
            {
                "type": "output",
                "text": (
                    "Dataset size: 12500"
                ),
            },
            {
                "type": "output",
                "text": (
                    "Ready."
                ),
            },
            {
                "type": "prompt",
                "text": "$ ",
            },
        ],
    },

    {
        "shell":
            "zsh",

        "directory":
            "~/research/synthetic_ui",

        "lines": [
            {
                "type": "prompt",
                "text": (
                    "$ git status"
                ),
            },
            {
                "type": "output",
                "text": (
                    "On branch feature/layouts"
                ),
            },
            {
                "type": "output",
                "text": (
                    "Changes not staged "
                    "for commit:"
                ),
            },
            {
                "type": "output",
                "text": (
                    "  modified: renderer.py"
                ),
            },
            {
                "type": "prompt",
                "text": "$ ",
            },
        ],
    },

    {
        "shell":
            "bash",

        "directory":
            "~/workspace/ml_pipeline",

        "lines": [
            {
                "type": "prompt",
                "text": (
                    "$ pip list | head"
                ),
            },
            {
                "type": "output",
                "text": (
                    "Package        Version"
                ),
            },
            {
                "type": "output",
                "text": (
                    "numpy          2.1.0"
                ),
            },
            {
                "type": "output",
                "text": (
                    "torch          2.5.1"
                ),
            },
            {
                "type": "output",
                "text": (
                    "playwright     1.50.0"
                ),
            },
        ],
    },
]


# ==========================================================
# Debug Frames
# ==========================================================

DEBUG_FRAMES = [

    {
        "function":
            "build_dataset",

        "location":
            "main.py:27",
    },

    {
        "function":
            "generate",

        "location":
            "dataset.py:84",
    },

    {
        "function":
            "render_sample",

        "location":
            "renderer.py:116",
    },

    {
        "function":
            "<module>",

        "location":
            "main.py:41",
    },
]


# ==========================================================
# Debug Variables
# ==========================================================

DEBUG_VARIABLES = [

    {
        "name":
            "num_samples",

        "value":
            "5000",

        "type":
            "int",
    },

    {
        "name":
            "validate",

        "value":
            "True",

        "type":
            "bool",
    },

    {
        "name":
            "device",

        "value":
            "'cuda:0'",

        "type":
            "str",
    },

    {
        "name":
            "batch_size",

        "value":
            "16",

        "type":
            "int",
    },

    {
        "name":
            "samples",

        "value":
            "list[428]",

        "type":
            "list",
    },
]


# ==========================================================
# Problems
# ==========================================================

PROBLEMS = [

    {
        "severity":
            "warning",

        "icon":
            "warning",

        "message":
            "Unused import 'Detector'",

        "file":
            "main.py",

        "line":
            4,
    },

    {
        "severity":
            "error",

        "icon":
            "error",

        "message":
            (
                "Unresolved reference "
                "'output_path'"
            ),

        "file":
            "renderer.py",

        "line":
            116,
    },

    {
        "severity":
            "warning",

        "icon":
            "warning",

        "message":
            (
                "Parameter 'theme' "
                "is never used"
            ),

        "file":
            "dataset.py",

        "line":
            52,
    },

    {
        "severity":
            "info",

        "icon":
            "info",

        "message":
            (
                "Simplify chained "
                "comparison"
            ),

        "file":
            "utils.py",

        "line":
            78,
    },
]


# ==========================================================
# Generate Run State
# ==========================================================

def generate_run_state() -> dict:

    return {

        "title":
            "Run",

        "configuration":
            random.choice(
                [
                    "main",
                    "train",
                    "renderer",
                ]
            ),

        "lines":
            random.choice(
                RUN_OUTPUTS
            ),
    }


# ==========================================================
# Generate Terminal State
# ==========================================================

def generate_terminal_state() -> dict:

    return random.choice(
        TERMINAL_SESSIONS
    )


# ==========================================================
# Generate Debug State
# ==========================================================

def generate_debug_state() -> dict:

    frame_count = random.randint(
        3,
        len(DEBUG_FRAMES),
    )

    variable_count = random.randint(
        3,
        len(DEBUG_VARIABLES),
    )

    return {

        "thread":
            "MainThread",

        "frames":
            DEBUG_FRAMES[
                :frame_count
            ],

        "variables":
            DEBUG_VARIABLES[
                :variable_count
            ],

        "paused_line":
            random.randint(
                14,
                27,
            ),
    }


# ==========================================================
# Generate Problems State
# ==========================================================

def generate_problems_state() -> dict:

    count = random.randint(
        2,
        len(PROBLEMS),
    )

    return {

        "items":
            random.sample(
                PROBLEMS,
                k=count,
            ),

        "count":
            count,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_workspace_state_data(
    state: str | None = None,
) -> dict:

    editor = generate_editor_data()

    selected_state = (
        state
        if state is not None
        else random.choice(
            WORKSPACE_STATES
        )
    )

    if selected_state not in WORKSPACE_STATES:

        raise ValueError(
            f"Unknown workspace state: "
            f"{selected_state}"
        )

    result = {

        **editor,

        "workspace_state":
            selected_state,

        "bottom_panel_height":
            random.choice(
                [
                    "220px",
                    "250px",
                    "280px",
                    "320px",
                ]
            ),
    }


    # ======================================================
    # State Data
    # ======================================================

    if selected_state == "run":

        result["run"] = (
            generate_run_state()
        )

    elif selected_state == "debug":

        result["debug"] = (
            generate_debug_state()
        )

    elif selected_state == "terminal":

        result["terminal"] = (
            generate_terminal_state()
        )

    elif selected_state == "problems":

        result["problems"] = (
            generate_problems_state()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in WORKSPACE_STATES:

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
            generate_workspace_state_data(
                state=state
            )
        )