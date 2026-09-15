from __future__ import annotations

import random

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)


# ==========================================================
# Overlay States
# ==========================================================

OVERLAY_STATES = [
    "find_replace",
    "rename",
    "run_configuration",
    "breakpoint",
    "file_chooser",
]


# ==========================================================
# Find / Replace
# ==========================================================

def generate_find_replace_state() -> dict:

    return {

        "query":
            random.choice(
                [
                    "render_page",
                    "generate_theme",
                    "viewport",
                    "annotation",
                    "dataset",
                ]
            ),

        "replacement":
            random.choice(
                [
                    "",
                    "render_pycharm_page",
                    "resolved_viewport",
                    "annotation_data",
                ]
            ),

        "scope":
            random.choice(
                [
                    "Whole Project",
                    "Current File",
                    "Open Files",
                    "Directory",
                ]
            ),

        "case_sensitive":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "regex":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Rename
# ==========================================================

def generate_rename_state() -> dict:

    old_name = random.choice(
        [
            "render_page",
            "dataset",
            "viewport",
            "theme",
            "generator",
        ]
    )

    return {

        "old_name":
            old_name,

        "new_name":
            random.choice(
                [
                    "render_workspace",
                    "dataset_builder",
                    "resolved_viewport",
                    "ui_theme",
                    "content_generator",
                ]
            ),

        "search_comments":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "search_strings":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Run Configuration
# ==========================================================

def generate_run_configuration_state() -> dict:

    return {

        "name":
            random.choice(
                [
                    "main",
                    "renderer",
                    "training",
                    "dataset generator",
                ]
            ),

        "script":
            random.choice(
                [
                    "main.py",
                    "renderer.py",
                    "train.py",
                    "generate_dataset.py",
                ]
            ),

        "parameters":
            random.choice(
                [
                    "",
                    "--samples 5000",
                    "--epochs 100",
                    "--viewport desktop_fhd",
                ]
            ),

        "working_directory":
            random.choice(
                [
                    "~/projects/gui_detector",
                    "~/research/synthetic_ui",
                    "~/workspace/pycharm",
                ]
            ),

        "interpreter":
            random.choice(
                [
                    "Python 3.10",
                    "Python 3.11",
                    "Python 3.12",
                ]
            ),
    }


# ==========================================================
# Breakpoint
# ==========================================================

def generate_breakpoint_state() -> dict:

    return {

        "file":
            random.choice(
                [
                    "main.py",
                    "renderer.py",
                    "dataset.py",
                ]
            ),

        "line":
            random.randint(
                20,
                140,
            ),

        "condition":
            random.choice(
                [
                    "",
                    "sample_index > 100",
                    "annotation_count == 0",
                    "viewport['width'] > 1024",
                ]
            ),

        "enabled":
            True,

        "suspend":
            random.choice(
                [
                    "All",
                    "Thread",
                ]
            ),

        "log_message":
            random.choice(
                [
                    "",
                    "Breakpoint reached",
                    "Rendering sample",
                ]
            ),
    }


# ==========================================================
# File Chooser
# ==========================================================

FILE_ITEMS = [
    {
        "name": "src",
        "type": "folder",
        "icon": "folder",
    },
    {
        "name": "templates",
        "type": "folder",
        "icon": "folder",
    },
    {
        "name": "renderers",
        "type": "folder",
        "icon": "folder",
    },
    {
        "name": "main.py",
        "type": "python",
        "icon": "code",
    },
    {
        "name": "config.py",
        "type": "python",
        "icon": "code",
    },
    {
        "name": "README.md",
        "type": "markdown",
        "icon": "description",
    },
]


def generate_file_chooser_state() -> dict:

    return {

        "path":
            random.choice(
                [
                    "~/projects/gui_detector",
                    "~/research/synthetic_ui",
                    "~/workspace",
                ]
            ),

        "items":
            FILE_ITEMS,

        "selected_index":
            random.randrange(
                len(FILE_ITEMS)
            ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_partial_overlay_data(
    state: str | None = None,
) -> dict:

    editor = generate_editor_data()

    selected_state = (
        state
        if state is not None
        else random.choice(
            OVERLAY_STATES
        )
    )

    if selected_state not in OVERLAY_STATES:

        raise ValueError(
            f"Unknown overlay state: "
            f"{selected_state}"
        )


    result = {

        **editor,

        "overlay_state":
            selected_state,

        "dialog_size":
            random.choice(
                [
                    "medium",
                    "wide",
                    "compact",
                ]
            ),
    }


    if selected_state == "find_replace":

        result["find_replace"] = (
            generate_find_replace_state()
        )

    elif selected_state == "rename":

        result["rename"] = (
            generate_rename_state()
        )

    elif selected_state == "run_configuration":

        result["run_configuration"] = (
            generate_run_configuration_state()
        )

    elif selected_state == "breakpoint":

        result["breakpoint"] = (
            generate_breakpoint_state()
        )

    elif selected_state == "file_chooser":

        result["file_chooser"] = (
            generate_file_chooser_state()
        )


    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in OVERLAY_STATES:

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
            generate_partial_overlay_data(
                state=state
            )
        )