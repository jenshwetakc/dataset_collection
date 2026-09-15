from __future__ import annotations

import random

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)


# ==========================================================
# Popup States
# ==========================================================

POPUP_STATES = [
    "search_everywhere",
    "code_completion",
    "context_menu",
    "quick_documentation",
    "refactor",
]


# ==========================================================
# Search Everywhere
# ==========================================================

SEARCH_RESULTS = [
    {
        "name": "main.py",
        "secondary": "src",
        "icon": "code",
    },
    {
        "name": "DatasetGenerator",
        "secondary": "dataset_generator.py",
        "icon": "data_object",
    },
    {
        "name": "render_page",
        "secondary": "renderer.py",
        "icon": "function",
    },
    {
        "name": "generate_theme",
        "secondary": "palette_generator.py",
        "icon": "function",
    },
    {
        "name": "Settings",
        "secondary": "Actions",
        "icon": "settings",
    },
]


# ==========================================================
# Code Completion
# ==========================================================

COMPLETION_ITEMS = [
    {
        "name": "generate",
        "detail": "(count: int, validate: bool)",
        "kind": "method",
        "icon": "function",
    },
    {
        "name": "generate_sample",
        "detail": "(index: int)",
        "kind": "method",
        "icon": "function",
    },
    {
        "name": "generate_theme",
        "detail": "(mode: str)",
        "kind": "function",
        "icon": "function",
    },
    {
        "name": "generator",
        "detail": "DatasetGenerator",
        "kind": "variable",
        "icon": "data_object",
    },
    {
        "name": "get_random_image",
        "detail": "(directory: Path)",
        "kind": "function",
        "icon": "function",
    },
]


# ==========================================================
# Context Menu
# ==========================================================

CONTEXT_MENU_ITEMS = [
    {
        "label": "Show Context Actions",
        "shortcut": "Alt+Enter",
        "icon": "lightbulb",
    },
    {
        "label": "Go to Declaration",
        "shortcut": "Ctrl+B",
        "icon": "arrow_forward",
    },
    {
        "label": "Find Usages",
        "shortcut": "Alt+F7",
        "icon": "search",
    },
    {
        "label": "Refactor",
        "shortcut": "Ctrl+Alt+Shift+T",
        "icon": "construction",
    },
    {
        "label": "Reformat Code",
        "shortcut": "Ctrl+Alt+L",
        "icon": "format_align_left",
    },
    {
        "label": "Run 'main'",
        "shortcut": "Shift+F10",
        "icon": "play_arrow",
    },
]


# ==========================================================
# Documentation
# ==========================================================

DOCUMENTATION_VARIANTS = [
    {
        "title": "DatasetGenerator.generate",
        "signature": (
            "generate("
            "count: int, "
            "validate: bool = True"
            ") -> list"
        ),
        "description": (
            "Generate synthetic UI samples and "
            "optionally validate each generated sample."
        ),
        "module": "dataset.generator",
    },
    {
        "title": "render_page",
        "signature": (
            "render_page("
            "browser, page_data, theme, viewport"
            ")"
        ),
        "description": (
            "Render one synthetic interface and export "
            "screenshots, annotations and metadata."
        ),
        "module": "common_renderer",
    },
]


# ==========================================================
# Refactor
# ==========================================================

REFACTOR_ACTIONS = [
    {
        "label": "Rename",
        "shortcut": "Shift+F6",
        "icon": "edit",
    },
    {
        "label": "Change Signature",
        "shortcut": "Ctrl+F6",
        "icon": "function",
    },
    {
        "label": "Extract Method",
        "shortcut": "Ctrl+Alt+M",
        "icon": "call_split",
    },
    {
        "label": "Extract Variable",
        "shortcut": "Ctrl+Alt+V",
        "icon": "data_object",
    },
    {
        "label": "Inline",
        "shortcut": "Ctrl+Alt+N",
        "icon": "merge",
    },
]


# ==========================================================
# Generate Search State
# ==========================================================

def generate_search_everywhere_state() -> dict:

    query = random.choice(
        [
            "render",
            "generate",
            "dataset",
            "main",
            "theme",
        ]
    )

    return {
        "query": query,
        "results": SEARCH_RESULTS,
        "selected_index": random.randrange(
            len(SEARCH_RESULTS)
        ),
    }


# ==========================================================
# Generate Completion State
# ==========================================================

def generate_completion_state() -> dict:

    return {
        "prefix": random.choice(
            [
                "gen",
                "get_",
                "render",
                "data",
            ]
        ),
        "items": COMPLETION_ITEMS,
        "selected_index": random.randrange(
            len(COMPLETION_ITEMS)
        ),
    }


# ==========================================================
# Generate Context Menu State
# ==========================================================

def generate_context_menu_state() -> dict:

    return {
        "items": CONTEXT_MENU_ITEMS,
        "selected_index": random.randrange(
            len(CONTEXT_MENU_ITEMS)
        ),
    }


# ==========================================================
# Generate Documentation State
# ==========================================================

def generate_documentation_state() -> dict:

    return random.choice(
        DOCUMENTATION_VARIANTS
    )


# ==========================================================
# Generate Refactor State
# ==========================================================

def generate_refactor_state() -> dict:

    return {
        "items": REFACTOR_ACTIONS,
        "selected_index": random.randrange(
            len(REFACTOR_ACTIONS)
        ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_editor_popup_data(
    state: str | None = None,
) -> dict:

    editor = generate_editor_data()

    popup_state = (
        state
        if state is not None
        else random.choice(
            POPUP_STATES
        )
    )

    if popup_state not in POPUP_STATES:

        raise ValueError(
            f"Unknown popup state: {popup_state}"
        )

    result = {
        **editor,
        "popup_state": popup_state,
    }

    if popup_state == "search_everywhere":

        result["search_popup"] = (
            generate_search_everywhere_state()
        )

    elif popup_state == "code_completion":

        result["completion_popup"] = (
            generate_completion_state()
        )

    elif popup_state == "context_menu":

        result["context_popup"] = (
            generate_context_menu_state()
        )

    elif popup_state == "quick_documentation":

        result["documentation_popup"] = (
            generate_documentation_state()
        )

    elif popup_state == "refactor":

        result["refactor_popup"] = (
            generate_refactor_state()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for popup_state in POPUP_STATES:

        print(
            "\n=============================="
        )

        print(
            popup_state.upper()
        )

        print(
            "=============================="
        )

        pprint.pp(
            generate_editor_popup_data(
                state=popup_state
            )
        )