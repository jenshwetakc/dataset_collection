from __future__ import annotations

import random


# ==========================================================
# Settings States
# ==========================================================

SETTINGS_STATES = [
    "appearance",
    "editor",
    "plugins",
    "python_interpreter",
    "version_control",
]


# ==========================================================
# Settings Navigation
# ==========================================================

SETTINGS_NAVIGATION = [

    {
        "id": "appearance",
        "label": "Appearance & Behavior",
        "icon": "palette",
    },

    {
        "id": "editor",
        "label": "Editor",
        "icon": "edit_note",
    },

    {
        "id": "plugins",
        "label": "Plugins",
        "icon": "extension",
    },

    {
        "id": "python_interpreter",
        "label": "Python Interpreter",
        "icon": "deployed_code",
    },

    {
        "id": "version_control",
        "label": "Version Control",
        "icon": "account_tree",
    },

    {
        "id": "build",
        "label": "Build, Execution, Deployment",
        "icon": "build",
    },

    {
        "id": "languages",
        "label": "Languages & Frameworks",
        "icon": "code",
    },

    {
        "id": "tools",
        "label": "Tools",
        "icon": "construction",
    },

    {
        "id": "advanced",
        "label": "Advanced Settings",
        "icon": "tune",
    },
]


# ==========================================================
# Appearance
# ==========================================================

APPEARANCE_THEMES = [
    "Light",
    "Dark",
    "High Contrast",
    "System",
]

UI_DENSITIES = [
    "Compact",
    "Default",
    "Comfortable",
]


def generate_appearance_settings() -> dict:

    return {

        "theme":
            random.choice(
                APPEARANCE_THEMES
            ),

        "density":
            random.choice(
                UI_DENSITIES
            ),

        "font_size":
            random.choice(
                [
                    12,
                    13,
                    14,
                    15,
                ]
            ),

        "show_main_toolbar":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "show_navigation_bar":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "use_custom_font":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "animate_windows":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Editor
# ==========================================================

EDITOR_FONTS = [
    "JetBrains Mono",
    "Consolas",
    "Menlo",
    "Monaco",
]

COLOR_SCHEMES = [
    "Default",
    "Darcula",
    "High contrast",
]


def generate_editor_settings() -> dict:

    return {

        "font":
            random.choice(
                EDITOR_FONTS
            ),

        "font_size":
            random.choice(
                [
                    12,
                    13,
                    14,
                    15,
                    16,
                ]
            ),

        "line_spacing":
            random.choice(
                [
                    1.0,
                    1.1,
                    1.2,
                    1.3,
                ]
            ),

        "scheme":
            random.choice(
                COLOR_SCHEMES
            ),

        "show_line_numbers":
            True,

        "show_whitespaces":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "show_indent_guides":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "soft_wraps":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Plugins
# ==========================================================

PLUGIN_NAMES = [
    {
        "name": "GitToolBox",
        "description": (
            "Extends Git integration with "
            "additional status information."
        ),
        "enabled": True,
    },

    {
        "name": "Rainbow Brackets",
        "description": (
            "Colorizes matching brackets "
            "for easier code navigation."
        ),
        "enabled": True,
    },

    {
        "name": "CSV Editor",
        "description": (
            "Provides an advanced editor "
            "for CSV and TSV files."
        ),
        "enabled": False,
    },

    {
        "name": "IdeaVim",
        "description": (
            "Vim emulation for IDE editors."
        ),
        "enabled": True,
    },

    {
        "name": "Docker",
        "description": (
            "Docker integration and "
            "container management."
        ),
        "enabled": True,
    },

    {
        "name": "Database Tools",
        "description": (
            "Database browsing and "
            "SQL development support."
        ),
        "enabled": False,
    },
]


def generate_plugin_settings() -> dict:

    count = random.randint(
        4,
        len(PLUGIN_NAMES),
    )

    selected_plugins = random.sample(
        PLUGIN_NAMES,
        k=count,
    )

    return {

        "search_query":
            random.choice(
                [
                    "",
                    "git",
                    "python",
                    "editor",
                    "docker",
                ]
            ),

        "tab":
            random.choice(
                [
                    "Installed",
                    "Marketplace",
                ]
            ),

        "plugins":
            selected_plugins,
    }


# ==========================================================
# Python Interpreter
# ==========================================================

PYTHON_PACKAGES = [
    {
        "name": "numpy",
        "version": "2.1.0",
        "latest": "2.1.2",
    },

    {
        "name": "torch",
        "version": "2.5.1",
        "latest": "2.5.1",
    },

    {
        "name": "playwright",
        "version": "1.50.0",
        "latest": "1.50.0",
    },

    {
        "name": "pillow",
        "version": "11.0.0",
        "latest": "11.1.0",
    },

    {
        "name": "jinja2",
        "version": "3.1.5",
        "latest": "3.1.5",
    },

    {
        "name": "faker",
        "version": "33.1.0",
        "latest": "33.1.0",
    },

    {
        "name": "opencv-python",
        "version": "4.10.0",
        "latest": "4.11.0",
    },
]


def generate_python_interpreter_settings() -> dict:

    return {

        "interpreter":
            random.choice(
                [
                    "Python 3.10",
                    "Python 3.11",
                    "Python 3.12",
                ]
            ),

        "environment":
            random.choice(
                [
                    ".venv",
                    "conda",
                    "system",
                ]
            ),

        "path":
            random.choice(
                [
                    "/home/user/project/.venv/bin/python",
                    "/usr/bin/python3",
                    "/opt/conda/bin/python",
                ]
            ),

        "packages":
            random.sample(
                PYTHON_PACKAGES,
                k=random.randint(
                    5,
                    len(PYTHON_PACKAGES),
                ),
            ),
    }


# ==========================================================
# Version Control
# ==========================================================

def generate_version_control_settings() -> dict:

    return {

        "vcs":
            "Git",

        "git_path":
            random.choice(
                [
                    "/usr/bin/git",
                    "/usr/local/bin/git",
                    "git",
                ]
            ),

        "auto_update":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "show_diff":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "commit_interface":
            random.choice(
                [
                    "Tool Window",
                    "Modal Dialog",
                ]
            ),

        "confirm_force_push":
            True,

        "repositories": [
            {
                "directory":
                    "~/projects/gui_detector",

                "branch":
                    "main",
            },

            {
                "directory":
                    "~/research/synthetic_ui",

                "branch":
                    "feature/layouts",
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_settings_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            SETTINGS_STATES
        )
    )

    if selected_state not in SETTINGS_STATES:

        raise ValueError(
            f"Unknown settings state: "
            f"{selected_state}"
        )

    result = {

        "settings_state":
            selected_state,

        "navigation":
            SETTINGS_NAVIGATION,

        "search_query":
            random.choice(
                [
                    "",
                    "",
                    "",
                    "editor",
                    "python",
                ]
            ),
    }


    if selected_state == "appearance":

        result["appearance"] = (
            generate_appearance_settings()
        )

    elif selected_state == "editor":

        result["editor"] = (
            generate_editor_settings()
        )

    elif selected_state == "plugins":

        result["plugins"] = (
            generate_plugin_settings()
        )

    elif selected_state == "python_interpreter":

        result["python_interpreter"] = (
            generate_python_interpreter_settings()
        )

    elif selected_state == "version_control":

        result["version_control"] = (
            generate_version_control_settings()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in SETTINGS_STATES:

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
            generate_settings_data(
                state=state
            )
        )