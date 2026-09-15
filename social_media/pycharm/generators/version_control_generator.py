from __future__ import annotations

import random


# ==========================================================
# Version Control States
# ==========================================================

VERSION_CONTROL_STATES = [
    "local_changes",
    "commit",
    "diff",
    "history",
    "branches",
]


# ==========================================================
# Changed Files
# ==========================================================

CHANGED_FILES = [
    {
        "name": "renderer.py",
        "path": "src/renderers/renderer.py",
        "status": "modified",
        "symbol": "M",
    },
    {
        "name": "dataset.py",
        "path": "src/dataset.py",
        "status": "modified",
        "symbol": "M",
    },
    {
        "name": "settings.html",
        "path": "templates/settings.html",
        "status": "modified",
        "symbol": "M",
    },
    {
        "name": "debugger.py",
        "path": "src/debugger.py",
        "status": "added",
        "symbol": "A",
    },
    {
        "name": "old_utils.py",
        "path": "src/utils/old_utils.py",
        "status": "deleted",
        "symbol": "D",
    },
    {
        "name": "config.py",
        "path": "src/config.py",
        "status": "modified",
        "symbol": "M",
    },
]


# ==========================================================
# Commits
# ==========================================================

COMMITS = [
    {
        "hash": "a41f90c",
        "message": "Add viewport-aware editor layout",
        "author": "Shweta",
        "time": "10 minutes ago",
        "branch": "main",
    },
    {
        "hash": "76bd22a",
        "message": "Fix annotation clipping for overlays",
        "author": "Shweta",
        "time": "1 hour ago",
        "branch": "main",
    },
    {
        "hash": "2140fa9",
        "message": "Implement PyCharm workspace states",
        "author": "Shweta",
        "time": "Yesterday",
        "branch": "feature/pycharm",
    },
    {
        "hash": "be049cd",
        "message": "Update synthetic dataset generator",
        "author": "Research",
        "time": "2 days ago",
        "branch": "develop",
    },
    {
        "hash": "8945b1e",
        "message": "Refactor common renderer",
        "author": "Research",
        "time": "4 days ago",
        "branch": "develop",
    },
]


# ==========================================================
# Branches
# ==========================================================

BRANCHES = [
    {
        "name": "main",
        "current": True,
        "remote": False,
    },
    {
        "name": "develop",
        "current": False,
        "remote": False,
    },
    {
        "name": "feature/pycharm",
        "current": False,
        "remote": False,
    },
    {
        "name": "feature/layout-diversity",
        "current": False,
        "remote": False,
    },
    {
        "name": "origin/main",
        "current": False,
        "remote": True,
    },
    {
        "name": "origin/develop",
        "current": False,
        "remote": True,
    },
]


# ==========================================================
# Diff Lines
# ==========================================================

DIFF_LINES = [
    {
        "old": 18,
        "new": 18,
        "type": "context",
        "text": "async def render_page(",
    },
    {
        "old": 19,
        "new": 19,
        "type": "context",
        "text": "    browser,",
    },
    {
        "old": 20,
        "new": None,
        "type": "removed",
        "text": "    viewport_name,",
    },
    {
        "old": None,
        "new": 20,
        "type": "added",
        "text": "    viewport: dict,",
    },
    {
        "old": 21,
        "new": 21,
        "type": "context",
        "text": "    theme,",
    },
    {
        "old": None,
        "new": 22,
        "type": "added",
        "text": "    min_visible_ratio=0.20,",
    },
    {
        "old": 22,
        "new": 23,
        "type": "context",
        "text": "):",
    },
    {
        "old": 23,
        "new": 24,
        "type": "context",
        "text": "    width = viewport['width']",
    },
    {
        "old": 24,
        "new": None,
        "type": "removed",
        "text": "    height = DEFAULT_HEIGHT",
    },
    {
        "old": None,
        "new": 25,
        "type": "added",
        "text": "    height = viewport['height']",
    },
]


# ==========================================================
# Local Changes
# ==========================================================

def generate_local_changes_state() -> dict:

    count = random.randint(
        3,
        len(CHANGED_FILES),
    )

    files = random.sample(
        CHANGED_FILES,
        k=count,
    )

    return {
        "files": files,
        "selected_index": random.randrange(
            len(files)
        ),
    }


# ==========================================================
# Commit
# ==========================================================

def generate_commit_state() -> dict:

    count = random.randint(
        2,
        5,
    )

    return {
        "files": random.sample(
            CHANGED_FILES,
            k=count,
        ),
        "message": random.choice(
            [
                "Improve PyCharm UI diversity",
                "Add Version Control workspace",
                "Fix renderer annotation states",
                "Update responsive layouts",
            ]
        ),
        "amend": random.choice(
            [
                True,
                False,
            ]
        ),
        "run_checks": random.choice(
            [
                True,
                False,
            ]
        ),
    }


# ==========================================================
# Diff
# ==========================================================

def generate_diff_state() -> dict:

    return {
        "filename": random.choice(
            [
                "renderer.py",
                "dataset.py",
                "settings.html",
            ]
        ),
        "left_revision": "HEAD",
        "right_revision": "Local",
        "lines": DIFF_LINES,
    }


# ==========================================================
# History
# ==========================================================

def generate_history_state() -> dict:

    return {
        "commits": COMMITS,
        "selected_index": random.randrange(
            len(COMMITS)
        ),
    }


# ==========================================================
# Branches
# ==========================================================

def generate_branches_state() -> dict:

    return {
        "branches": BRANCHES,
        "search_query": random.choice(
            [
                "",
                "",
                "feature",
                "main",
            ]
        ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_version_control_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            VERSION_CONTROL_STATES
        )
    )

    if selected_state not in VERSION_CONTROL_STATES:

        raise ValueError(
            f"Unknown version control state: "
            f"{selected_state}"
        )

    result = {

        "state":
            selected_state,

        "project_name":
            random.choice(
                [
                    "gui_detector",
                    "synthetic_ui",
                    "vision_lab",
                    "pycharm_dataset",
                ]
            ),

        "branch":
            random.choice(
                [
                    "main",
                    "develop",
                    "feature/pycharm",
                ]
            ),
    }


    if selected_state == "local_changes":

        result["local_changes"] = (
            generate_local_changes_state()
        )

    elif selected_state == "commit":

        result["commit"] = (
            generate_commit_state()
        )

    elif selected_state == "diff":

        result["diff"] = (
            generate_diff_state()
        )

    elif selected_state == "history":

        result["history"] = (
            generate_history_state()
        )

    elif selected_state == "branches":

        result["branches"] = (
            generate_branches_state()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in VERSION_CONTROL_STATES:

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
            generate_version_control_data(
                state=state
            )
        )