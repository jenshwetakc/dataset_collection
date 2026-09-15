from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

TERMINAL_STATES = [
    "default",
    "multiple_tabs",
    "split_pane",
    "command_running",
    "command_error",
    "search",
    "history",
    "ssh_session",
    "powershell",
    "command_prompt",
    "settings_menu",
    "connection_lost",
]


# ==========================================================
# Profiles
# ==========================================================

TERMINAL_PROFILES = [
    {
        "id": "powershell",
        "label": "PowerShell",
        "icon": "terminal",
        "prompt": "PS C:\\Users\\User>",
    },
    {
        "id": "cmd",
        "label": "Command Prompt",
        "icon": "terminal",
        "prompt": "C:\\Users\\User>",
    },
    {
        "id": "ubuntu",
        "label": "Ubuntu",
        "icon": "terminal",
        "prompt": "user@windows:~$",
    },
]


# ==========================================================
# Commands
# ==========================================================

COMMAND_POOL = [
    {
        "command": "dir",
        "output": [
            " Volume in drive C is Windows",
            " Directory of C:\\Users\\User",
            "",
            "09/05/2026  07:12 PM    <DIR>          Desktop",
            "09/05/2026  07:12 PM    <DIR>          Documents",
            "09/05/2026  07:12 PM    <DIR>          Downloads",
            "09/05/2026  07:12 PM    <DIR>          Pictures",
        ],
    },
    {
        "command": "python --version",
        "output": [
            "Python 3.12.4",
        ],
    },
    {
        "command": "git status",
        "output": [
            "On branch main",
            "Your branch is up to date with 'origin/main'.",
            "",
            "nothing to commit, working tree clean",
        ],
    },
    {
        "command": "pip list",
        "output": [
            "Package            Version",
            "------------------ --------",
            "numpy              2.1.1",
            "pandas             2.2.2",
            "playwright         1.55.0",
            "jinja2             3.1.4",
        ],
    },
]


# ==========================================================
# Errors
# ==========================================================

ERROR_POOL = [
    {
        "command": "python missing_script.py",
        "output": [
            "python: can't open file 'missing_script.py':",
            "[Errno 2] No such file or directory",
        ],
    },
    {
        "command": "git checkout unknown-branch",
        "output": [
            "error: pathspec 'unknown-branch'",
            "did not match any file(s) known to git",
        ],
    },
    {
        "command": "npm run missing",
        "output": [
            "npm error Missing script: \"missing\"",
        ],
    },
]


# ==========================================================
# History
# ==========================================================

HISTORY_COMMANDS = [
    "dir",
    "cd Documents",
    "python train.py",
    "git status",
    "git pull",
    "pip list",
    "cls",
    "nvidia-smi",
]


# ==========================================================
# SSH
# ==========================================================

SSH_HOSTS = [
    "research-server",
    "gpu-node-02",
    "dev-server",
    "compute-cluster",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_tab(
    index: int,
) -> dict:

    profile = random.choice(
        TERMINAL_PROFILES
    )

    return {
        "id":
            f"tab_{index}",

        "label":
            profile["label"],

        "icon":
            profile["icon"],

        "profile":
            profile["id"],

        "active":
            False,
    }


def generate_tabs(
    minimum: int = 1,
    maximum: int = 4,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    tabs = [
        generate_tab(
            index
        )
        for index in range(
            count
        )
    ]

    active_index = random.randrange(
        len(tabs)
    )

    tabs[
        active_index
    ]["active"] = True

    return tabs


def generate_terminal_lines(
    profile: dict,
    command_count: int = 3,
) -> list[dict]:

    lines = []

    commands = random.sample(
        COMMAND_POOL,
        k=min(
            command_count,
            len(
                COMMAND_POOL
            ),
        ),
    )

    for command in commands:

        lines.append(
            {
                "type": "prompt",
                "text":
                    f"{profile['prompt']} "
                    f"{command['command']}",
            }
        )

        for output in command["output"]:

            lines.append(
                {
                    "type": "output",
                    "text": output,
                }
            )

    lines.append(
        {
            "type": "prompt",
            "text":
                profile["prompt"],
        }
    )

    return lines


# ==========================================================
# Main Generator
# ==========================================================

def generate_terminal_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            TERMINAL_STATES
        )


    if state not in TERMINAL_STATES:

        raise ValueError(
            f"Unknown terminal state: "
            f"{state}"
        )


    if state == "powershell":

        profile = TERMINAL_PROFILES[0]

    elif state == "command_prompt":

        profile = TERMINAL_PROFILES[1]

    elif state == "ssh_session":

        profile = TERMINAL_PROFILES[2]

    else:

        profile = random.choice(
            TERMINAL_PROFILES
        )


    tabs = generate_tabs(
        minimum=(
            2
            if state
            == "multiple_tabs"
            else 1
        ),
        maximum=(
            4
            if state
            == "multiple_tabs"
            else 2
        ),
    )


    lines = generate_terminal_lines(
        profile,
        command_count=random.randint(
            2,
            4,
        ),
    )


    # ------------------------------------------------------
    # Command Running
    # ------------------------------------------------------

    progress = None

    if state == "command_running":

        lines.append(
            {
                "type": "prompt",
                "text":
                    f"{profile['prompt']} "
                    "python train.py",
            }
        )

        lines.extend(
            [
                {
                    "type": "output",
                    "text":
                        "Loading dataset...",
                },
                {
                    "type": "output",
                    "text":
                        "Starting training...",
                },
            ]
        )

        progress = random.randint(
            5,
            90,
        )


    # ------------------------------------------------------
    # Error
    # ------------------------------------------------------

    if state == "command_error":

        error = random.choice(
            ERROR_POOL
        )

        lines.append(
            {
                "type": "prompt",
                "text":
                    f"{profile['prompt']} "
                    f"{error['command']}",
            }
        )

        for output in error["output"]:

            lines.append(
                {
                    "type": "error",
                    "text": output,
                }
            )


    # ------------------------------------------------------
    # SSH
    # ------------------------------------------------------

    ssh_host = None

    if state == "ssh_session":

        ssh_host = random.choice(
            SSH_HOSTS
        )

        lines = [
            {
                "type": "prompt",
                "text":
                    f"PS C:\\Users\\User> "
                    f"ssh user@{ssh_host}",
            },
            {
                "type": "output",
                "text":
                    f"Connected to {ssh_host}.",
            },
            {
                "type": "output",
                "text":
                    "Ubuntu 24.04 LTS",
            },
            {
                "type": "prompt",
                "text":
                    f"user@{ssh_host}:~$ nvidia-smi",
            },
            {
                "type": "output",
                "text":
                    "NVIDIA-SMI 550.144.03",
            },
            {
                "type": "output",
                "text":
                    "GPU 0  NVIDIA RTX A5000",
            },
            {
                "type": "prompt",
                "text":
                    f"user@{ssh_host}:~$",
            },
        ]


    return {
        "state":
            state,

        "profile":
            profile,

        "tabs":
            tabs,

        "lines":
            lines,

        "progress":
            progress,

        "history":
            random.sample(
                HISTORY_COMMANDS,
                k=random.randint(
                    4,
                    len(
                        HISTORY_COMMANDS
                    ),
                ),
            ),

        "search_query":
            (
                random.choice(
                    [
                        "git",
                        "python",
                        "error",
                        "dataset",
                    ]
                )
                if state
                == "search"
                else ""
            ),

        "ssh_host":
            ssh_host,

        "split": {
            "left_profile":
                random.choice(
                    TERMINAL_PROFILES
                ),

            "right_profile":
                random.choice(
                    TERMINAL_PROFILES
                ),
        },

        "settings_menu": [
            {
                "label": "New tab",
                "icon": "add",
            },
            {
                "label": "Split pane",
                "icon": "vertical_split",
            },
            {
                "label": "Settings",
                "icon": "settings",
            },
            {
                "label": "Command palette",
                "icon": "keyboard_command_key",
            },
        ],
    }