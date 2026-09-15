from __future__ import annotations

import random

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)


# ==========================================================
# Tool Window States
# ==========================================================

TOOL_WINDOW_STATES = [
    "database_browser",
    "query_console",
    "services",
    "docker",
    "profiler",
]


# ==========================================================
# Database
# ==========================================================

DATABASE_ITEMS = [
    {
        "name": "research_db",
        "type": "database",
        "depth": 0,
        "expanded": True,
        "icon": "database",
    },
    {
        "name": "public",
        "type": "schema",
        "depth": 1,
        "expanded": True,
        "icon": "folder",
    },
    {
        "name": "users",
        "type": "table",
        "depth": 2,
        "icon": "table_chart",
    },
    {
        "name": "experiments",
        "type": "table",
        "depth": 2,
        "icon": "table_chart",
    },
    {
        "name": "samples",
        "type": "table",
        "depth": 2,
        "icon": "table_chart",
    },
    {
        "name": "annotations",
        "type": "table",
        "depth": 2,
        "icon": "table_chart",
    },
    {
        "name": "views",
        "type": "folder",
        "depth": 1,
        "expanded": False,
        "icon": "folder",
    },
]


DATABASE_ROWS = [
    {
        "id": 1001,
        "name": "sample_0001",
        "status": "ready",
        "viewport": "desktop_fhd",
    },
    {
        "id": 1002,
        "name": "sample_0002",
        "status": "ready",
        "viewport": "laptop",
    },
    {
        "id": 1003,
        "name": "sample_0003",
        "status": "pending",
        "viewport": "tablet_portrait",
    },
    {
        "id": 1004,
        "name": "sample_0004",
        "status": "ready",
        "viewport": "standard_iphone",
    },
]


# ==========================================================
# SQL
# ==========================================================

SQL_QUERIES = [
    """SELECT
    id,
    name,
    viewport,
    status
FROM samples
WHERE status = 'ready'
ORDER BY id DESC
LIMIT 100;""",

    """SELECT
    class_name,
    COUNT(*) AS total
FROM annotations
GROUP BY class_name
ORDER BY total DESC;""",

    """SELECT *
FROM experiments
WHERE created_at >= CURRENT_DATE
ORDER BY created_at DESC;""",
]


# ==========================================================
# Services
# ==========================================================

SERVICES = [
    {
        "name": "Web Server",
        "detail": "localhost:8000",
        "status": "running",
        "icon": "language",
    },
    {
        "name": "Background Worker",
        "detail": "dataset-worker",
        "status": "running",
        "icon": "memory",
    },
    {
        "name": "PostgreSQL",
        "detail": "localhost:5432",
        "status": "running",
        "icon": "database",
    },
    {
        "name": "Redis",
        "detail": "localhost:6379",
        "status": "stopped",
        "icon": "storage",
    },
    {
        "name": "Playwright Renderer",
        "detail": "chromium",
        "status": "running",
        "icon": "web_asset",
    },
]


# ==========================================================
# Docker
# ==========================================================

DOCKER_CONTAINERS = [
    {
        "name": "ui-renderer",
        "image": "synthetic-ui:latest",
        "status": "running",
        "port": "8000:8000",
    },
    {
        "name": "postgres",
        "image": "postgres:16",
        "status": "running",
        "port": "5432:5432",
    },
    {
        "name": "redis",
        "image": "redis:7",
        "status": "stopped",
        "port": "6379:6379",
    },
    {
        "name": "worker",
        "image": "dataset-worker:v2",
        "status": "running",
        "port": "—",
    },
]


# ==========================================================
# Profiler
# ==========================================================

PROFILER_FUNCTIONS = [
    {
        "name": "render_page",
        "module": "common_renderer.py",
        "time": "38.4%",
        "calls": 1240,
    },
    {
        "name": "extract_annotations",
        "module": "common_renderer.py",
        "time": "24.7%",
        "calls": 1240,
    },
    {
        "name": "draw_visualization",
        "module": "common_renderer.py",
        "time": "13.8%",
        "calls": 4960,
    },
    {
        "name": "generate_theme",
        "module": "palette_generator.py",
        "time": "9.2%",
        "calls": 310,
    },
    {
        "name": "get_random_image",
        "module": "media_generator.py",
        "time": "5.1%",
        "calls": 842,
    },
]


# ==========================================================
# State Generators
# ==========================================================

def generate_database_state() -> dict:

    return {
        "tree": DATABASE_ITEMS,
        "table_name": random.choice(
            [
                "samples",
                "annotations",
                "experiments",
            ]
        ),
        "rows": DATABASE_ROWS,
    }


def generate_query_state() -> dict:

    return {
        "connection": random.choice(
            [
                "research_db@localhost",
                "dataset_db@localhost",
            ]
        ),
        "query": random.choice(
            SQL_QUERIES
        ),
        "execution_time": random.choice(
            [
                "24 ms",
                "41 ms",
                "63 ms",
                "109 ms",
            ]
        ),
        "rows": DATABASE_ROWS,
    }


def generate_services_state() -> dict:

    return {
        "services": SERVICES,
    }


def generate_docker_state() -> dict:

    return {
        "engine": "Docker",
        "containers": DOCKER_CONTAINERS,
    }


def generate_profiler_state() -> dict:

    return {
        "duration": random.choice(
            [
                "12.8 s",
                "18.4 s",
                "24.1 s",
            ]
        ),
        "cpu": random.choice(
            [
                "42%",
                "58%",
                "71%",
            ]
        ),
        "memory": random.choice(
            [
                "1.4 GB",
                "2.1 GB",
                "3.2 GB",
            ]
        ),
        "functions": PROFILER_FUNCTIONS,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_tool_window_data(
    state: str | None = None,
    panel_open: bool | None = None,
) -> dict:

    editor = generate_editor_data()

    selected_state = (
        state
        if state is not None
        else random.choice(
            TOOL_WINDOW_STATES
        )
    )

    if selected_state not in TOOL_WINDOW_STATES:

        raise ValueError(
            f"Unknown tool window state: "
            f"{selected_state}"
        )

    is_open = (
        panel_open
        if panel_open is not None
        else random.choice(
            [
                True,
                False,
            ]
        )
    )

    result = {
        **editor,

        "tool_window_state":
            selected_state,

        "panel_open":
            is_open,
    }


    if selected_state == "database_browser":

        result["database"] = (
            generate_database_state()
        )

    elif selected_state == "query_console":

        result["query_console"] = (
            generate_query_state()
        )

    elif selected_state == "services":

        result["services"] = (
            generate_services_state()
        )

    elif selected_state == "docker":

        result["docker"] = (
            generate_docker_state()
        )

    elif selected_state == "profiler":

        result["profiler"] = (
            generate_profiler_state()
        )

    return result


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in TOOL_WINDOW_STATES:

        for open_state in [
            True,
            False,
        ]:

            print(
                "\n=============================="
            )

            print(
                state,
                "OPEN="
                + str(open_state)
            )

            print(
                "=============================="
            )

            pprint.pp(
                generate_tool_window_data(
                    state=state,
                    panel_open=open_state,
                )
            )