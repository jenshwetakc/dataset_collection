from __future__ import annotations

import random

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)


# ==========================================================
# Split States
# ==========================================================

SPLIT_EDITOR_STATES = [
    "single",
    "vertical_half",
    "vertical_third",
    "horizontal_half",
    "three_pane",
]


# ==========================================================
# File Pool
# ==========================================================

EDITOR_FILES = [
    "main.py",
    "renderer.py",
    "dataset.py",
    "config.py",
    "utils.py",
    "pipeline.py",
    "layout_generator.py",
]


# ==========================================================
# Code Variants
# ==========================================================

CODE_VARIANTS = {

    "main.py": [
        "from dataset import DatasetGenerator",
        "",
        "def main():",
        "    generator = DatasetGenerator()",
        "    generator.generate(5000)",
        "",
        "if __name__ == '__main__':",
        "    main()",
    ],

    "renderer.py": [
        "from pathlib import Path",
        "",
        "async def render_page(",
        "    browser,",
        "    viewport,",
        "    theme,",
        "):",
        "    width = viewport['width']",
        "    height = viewport['height']",
        "    return width, height",
    ],

    "dataset.py": [
        "class DatasetGenerator:",
        "",
        "    def __init__(self):",
        "        self.samples = []",
        "",
        "    def generate(self, count):",
        "        for index in range(count):",
        "            self.samples.append(index)",
        "",
        "        return self.samples",
    ],

    "config.py": [
        "NUM_SAMPLES = 5000",
        "",
        "VIEWPORTS = [",
        "    'standard_iphone',",
        "    'tablet_portrait',",
        "    'desktop_fhd',",
        "]",
        "",
        "THEME_MODE = 'random'",
    ],

    "utils.py": [
        "def clamp(value, minimum, maximum):",
        "    return max(",
        "        minimum,",
        "        min(value, maximum),",
        "    )",
        "",
        "",
        "def normalize(value):",
        "    return value / 100",
    ],

    "pipeline.py": [
        "async def run_pipeline():",
        "    samples = generate_samples()",
        "",
        "    for sample in samples:",
        "        await render_sample(sample)",
        "",
        "    export_annotations()",
    ],

    "layout_generator.py": [
        "def generate_layout(viewport):",
        "    if viewport['width'] < 600:",
        "        return 'compact'",
        "",
        "    if viewport['width'] < 1024:",
        "        return 'medium'",
        "",
        "    return 'expanded'",
    ],
}


# ==========================================================
# Generate Pane
# ==========================================================

def generate_pane(
    filename: str,
    pane_index: int,
) -> dict:

    lines = CODE_VARIANTS[
        filename
    ]

    return {

        "id":
            f"pane_{pane_index}",

        "filename":
            filename,

        "tabs": [
            {
                "name":
                    filename,

                "active":
                    True,

                "modified":
                    random.choice(
                        [
                            True,
                            False,
                            False,
                        ]
                    ),
            },
        ],

        "code_lines": [
            {
                "number":
                    index + 1,

                "content":
                    content,
            }
            for index, content
            in enumerate(lines)
        ],

        "caret_line":
            random.randint(
                1,
                len(lines),
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_split_editor_data(
    state: str | None = None,
) -> dict:

    editor = generate_editor_data()

    selected_state = (
        state
        if state is not None
        else random.choice(
            SPLIT_EDITOR_STATES
        )
    )

    if selected_state not in SPLIT_EDITOR_STATES:

        raise ValueError(
            f"Unknown split editor state: "
            f"{selected_state}"
        )


    if selected_state == "single":

        pane_count = 1

    elif selected_state in {
        "vertical_half",
        "vertical_third",
        "horizontal_half",
    }:

        pane_count = 2

    else:

        pane_count = 3


    selected_files = random.sample(
        EDITOR_FILES,
        k=pane_count,
    )


    panes = [
        generate_pane(
            filename=filename,
            pane_index=index,
        )
        for index, filename
        in enumerate(selected_files)
    ]


    return {

        **editor,

        "split_state":
            selected_state,

        "panes":
            panes,

        "project_visible":
            random.choice(
                [
                    True,
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in SPLIT_EDITOR_STATES:

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
            generate_split_editor_data(
                state=state
            )
        )