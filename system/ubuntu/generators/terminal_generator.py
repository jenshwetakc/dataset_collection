from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

TERMINAL_STATES = [

    "empty",

    "command_history",

    "long_output",

    "git_status",

    "package_update",

    "install_progress",

    "multiple_tabs",

    "split_terminal",

    "search_open",

    "context_menu_open",

    "sudo_prompt",

    "command_error",

    "process_running",

    "close_tab_dialog",
]


# ==========================================================
# Commands
# ==========================================================

COMMANDS = [

    "ls -la",

    "pwd",

    "cd Documents",

    "git status",

    "python main.py",

    "python3 --version",

    "pip list",

    "df -h",

    "free -h",

    "uname -a",

    "ip addr",

    "whoami",

    "ps aux",

    "top",

    "cat README.md",

    "find . -name '*.py'",
]


# ==========================================================
# Files
# ==========================================================

DIRECTORY_ENTRIES = [

    "Desktop",

    "Documents",

    "Downloads",

    "Music",

    "Pictures",

    "Projects",

    "Public",

    "Templates",

    "Videos",

    "README.md",

    "main.py",

    "requirements.txt",
]


# ==========================================================
# Git Files
# ==========================================================

GIT_FILES = [

    "README.md",

    "src/main.py",

    "src/utils.py",

    "requirements.txt",

    "tests/test_main.py",
]


# ==========================================================
# Packages
# ==========================================================

PACKAGES = [

    "libssl3",

    "python3",

    "python3-pip",

    "git",

    "curl",

    "vim",

    "ubuntu-desktop",

    "network-manager",

    "linux-image-generic",

    "software-properties-common",
]


# ==========================================================
# Context Menu
# ==========================================================

CONTEXT_MENU_ENTRIES = [

    {
        "label": "Copy",
        "icon": "content_copy",
    },

    {
        "label": "Paste",
        "icon": "content_paste",
    },

    {
        "label": "Select All",
        "icon": "select_all",
    },

    {
        "label": "Search",
        "icon": "search",
    },

    {
        "label": "Preferences",
        "icon": "settings",
    },

    {
        "label": "New Tab",
        "icon": "add",
    },

    {
        "label": "Close Tab",
        "icon": "close",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_user() -> str:

    value = (
        fake.user_name()
        .lower()
        .replace(
            ".",
            "",
        )
    )

    return value[:14]


def generate_hostname() -> str:

    return random.choice(
        [
            "ubuntu",
            "workstation",
            "desktop",
            "devbox",
            "linux-pc",
        ]
    )


def generate_directory_output() -> list[str]:

    entries = random.sample(

        DIRECTORY_ENTRIES,

        k=random.randint(
            6,
            len(
                DIRECTORY_ENTRIES
            ),
        ),
    )

    return entries


def generate_history() -> list[dict]:

    count = random.randint(
        3,
        8,
    )

    history = []

    for index in range(
        count
    ):

        command = random.choice(
            COMMANDS
        )

        history.append(
            {
                "id":
                    index,

                "command":
                    command,

                "output":
                    generate_command_output(
                        command
                    ),
            }
        )

    return history


def generate_command_output(
    command: str,
) -> list[str]:

    if command == "pwd":

        return [
            "/home/user"
        ]

    if command == "whoami":

        return [
            "user"
        ]

    if command == "python3 --version":

        return [
            random.choice(
                [
                    "Python 3.10.12",
                    "Python 3.11.8",
                    "Python 3.12.3",
                ]
            )
        ]

    if command == "ls -la":

        return [
            "drwxr-xr-x  8 user user 4096 .",
            "drwxr-xr-x  3 root root 4096 ..",
            "-rw-r--r--  1 user user  220 .bash_logout",
            "-rw-r--r--  1 user user 3771 .bashrc",
            "drwxr-xr-x  4 user user 4096 Documents",
            "drwxr-xr-x  2 user user 4096 Downloads",
        ]

    if command == "df -h":

        return [
            "Filesystem      Size  Used Avail Use% Mounted on",
            "/dev/nvme0n1p2  234G   91G  132G  41% /",
            "tmpfs           3.1G  2.1M  3.1G   1% /run",
        ]

    if command == "free -h":

        return [
            "               total        used        free",
            "Mem:            15Gi        6.2Gi       5.4Gi",
            "Swap:          2.0Gi        128Mi       1.8Gi",
        ]

    if command == "git status":

        return [
            "On branch main",
            "Your branch is up to date with 'origin/main'.",
            "",
            "Changes not staged for commit:",
            "  modified:   src/main.py",
        ]

    return [
        random.choice(
            [
                "Command completed successfully.",
                "No output.",
                "Done.",
                "Process finished with exit code 0.",
            ]
        )
    ]


# ==========================================================
# Long Output
# ==========================================================

def generate_long_output() -> list[str]:

    lines = []

    for index in range(
        random.randint(
            18,
            34,
        )
    ):

        lines.append(
            f"{index + 1:02d}  "
            f"{fake.sentence(nb_words=random.randint(5, 10))}"
        )

    return lines


# ==========================================================
# Package Update Output
# ==========================================================

def generate_package_output() -> list[str]:

    packages = random.sample(

        PACKAGES,

        k=random.randint(
            4,
            min(
                8,
                len(
                    PACKAGES
                ),
            ),
        ),
    )

    lines = [

        "Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease",

        "Get:2 http://archive.ubuntu.com/ubuntu noble-updates InRelease",

        "Reading package lists... Done",

        "Building dependency tree... Done",

        "Reading state information... Done",

        f"{len(packages)} packages can be upgraded.",
    ]

    for package in packages:

        lines.append(
            f"  {package}"
        )

    return lines


# ==========================================================
# Git State
# ==========================================================

def generate_git_entries() -> list[dict]:

    count = random.randint(
        2,
        min(
            5,
            len(
                GIT_FILES
            ),
        ),
    )

    selected = random.sample(
        GIT_FILES,
        k=count,
    )

    states = [
        "modified",
        "new file",
        "deleted",
    ]

    return [

        {
            "file":
                file_name,

            "state":
                random.choice(
                    states
                ),
        }

        for file_name in selected
    ]


# ==========================================================
# Tabs
# ==========================================================

def generate_tabs(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            2,
            4,
        )

    tabs = []

    for index in range(
        count
    ):

        tabs.append(
            {
                "id":
                    index,

                "title":
                    random.choice(
                        [
                            "Terminal",
                            "~/Projects",
                            "~/Documents",
                            "server",
                            "python",
                        ]
                    ),

                "active":
                    index == 0,
            }
        )

    return tabs


# ==========================================================
# Main
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
            f"Unknown Terminal state: "
            f"{state}"
        )


    user = generate_user()

    hostname = generate_hostname()


    # ======================================================
    # Base
    # ======================================================

    history = []

    output_lines = []

    current_command = ""

    progress = 0


    # ======================================================
    # Command History
    # ======================================================

    if state == "command_history":

        history = generate_history()


    # ======================================================
    # Long Output
    # ======================================================

    elif state == "long_output":

        current_command = random.choice(
            [
                "journalctl -n 50",
                "ps aux",
                "pip list",
                "find . -type f",
            ]
        )

        output_lines = (
            generate_long_output()
        )


    # ======================================================
    # Git
    # ======================================================

    elif state == "git_status":

        current_command = "git status"


    # ======================================================
    # Package Update
    # ======================================================

    elif state == "package_update":

        current_command = (
            "sudo apt update"
        )

        output_lines = (
            generate_package_output()
        )


    # ======================================================
    # Install Progress
    # ======================================================

    elif state == "install_progress":

        current_command = (
            "sudo apt install "
            + random.choice(
                [
                    "git",
                    "curl",
                    "vim",
                    "python3-pip",
                ]
            )
        )

        progress = random.randint(
            8,
            94,
        )


    # ======================================================
    # Error
    # ======================================================

    elif state == "command_error":

        current_command = random.choice(
            [
                "python missing.py",
                "cd unknown-folder",
                "git checkout feature-x",
                "cat missing.txt",
            ]
        )


    # ======================================================
    # Process
    # ======================================================

    elif state == "process_running":

        current_command = random.choice(
            [
                "python server.py",
                "npm run dev",
                "ping ubuntu.com",
                "python train.py",
            ]
        )

        output_lines = [

            "Starting process...",

            "Initializing resources...",

            "Listening for events...",

            "Process is running.",
        ]


    # ======================================================
    # Tabs
    # ======================================================

    if state == "multiple_tabs":

        tabs = generate_tabs(
            count=random.randint(
                3,
                5,
            )
        )

    else:

        tabs = [
            {
                "id": 0,
                "title": "Terminal",
                "active": True,
            }
        ]


    # ======================================================
    # Split Pane
    # ======================================================

    split_enabled = (
        state
        == "split_terminal"
    )


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    if state == "search_open":

        search_query = random.choice(
            [
                "error",
                "python",
                "main.py",
                "package",
                "ubuntu",
            ]
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "user":
            user,

        "hostname":
            hostname,

        "cwd":
            random.choice(
                [
                    "~",
                    "~/Documents",
                    "~/Projects",
                    "~/Downloads",
                ]
            ),

        "tabs":
            tabs,

        "history":
            history,

        "directory_entries":
            generate_directory_output(),

        "output_lines":
            output_lines,

        "current_command":
            current_command,

        "git_entries":
            generate_git_entries(),

        "progress":
            progress,

        "split_enabled":
            split_enabled,

        "search_query":
            search_query,

        "context_menu_entries":
            [
                dict(
                    entry
                )

                for entry
                in CONTEXT_MENU_ENTRIES
            ],

        "sudo_command":
            random.choice(
                [
                    "apt update",
                    "apt install git",
                    "apt upgrade",
                    "systemctl restart NetworkManager",
                ]
            ),

        "process_name":
            random.choice(
                [
                    "python",
                    "node",
                    "bash",
                    "ping",
                    "train.py",
                ]
            ),
    }