from __future__ import annotations

import random

from faker import Faker

from system.ubuntu.generators.media_generator import (
    get_random_avatar,
    get_random_wallpaper,
)


fake = Faker()


# ==========================================================
# Login States
# ==========================================================

LOGIN_STATES = [

    "lock_screen",

    "password_entry",

    "password_visible",

    "wrong_password",

    "user_selection",

    "session_menu",

    "network_menu",

    "accessibility_menu",

    "power_menu",

    "shutdown_dialog",

    "restart_dialog",

    "logging_in",
]


# ==========================================================
# Session Choices
# ==========================================================

SESSION_CHOICES = [

    {
        "name":
            "Ubuntu",

        "description":
            "Ubuntu desktop session",

        "selected":
            False,
    },

    {
        "name":
            "Ubuntu on Wayland",

        "description":
            "Ubuntu Wayland session",

        "selected":
            False,
    },

    {
        "name":
            "GNOME",

        "description":
            "GNOME desktop session",

        "selected":
            False,
    },

    {
        "name":
            "GNOME Classic",

        "description":
            "Classic GNOME session",

        "selected":
            False,
    },
]


# ==========================================================
# Accessibility
# ==========================================================

ACCESSIBILITY_OPTIONS = [

    {
        "name":
            "High Contrast",

        "icon":
            "contrast",
    },

    {
        "name":
            "Large Text",

        "icon":
            "text_fields",
    },

    {
        "name":
            "Screen Reader",

        "icon":
            "record_voice_over",
    },

    {
        "name":
            "Screen Keyboard",

        "icon":
            "keyboard",
    },

    {
        "name":
            "Visual Alerts",

        "icon":
            "visibility",
    },
]


# ==========================================================
# Networks
# ==========================================================

NETWORK_NAMES = [

    "Home Wi-Fi",

    "University",

    "Office Network",

    "Guest",

    "Studio",

    "Workspace",

    "Public Wi-Fi",
]


# ==========================================================
# Generate Users
# ==========================================================

def generate_users(
    minimum: int = 2,
    maximum: int = 4,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    users = []

    for index in range(
        count
    ):

        name = fake.name()

        users.append(
            {
                "id":
                    index,

                "name":
                    name,

                "username":
                    (
                        name
                        .lower()
                        .replace(
                            " ",
                            ".",
                        )
                    ),

                "avatar":
                    get_random_avatar(),

                "active":
                    False,
            }
        )

    active_index = random.randrange(
        len(
            users
        )
    )

    users[
        active_index
    ][
        "active"
    ] = True

    return users


# ==========================================================
# Generate Networks
# ==========================================================

def generate_networks() -> list[dict]:

    count = random.randint(
        3,
        6,
    )

    selected_names = random.sample(
        NETWORK_NAMES,
        k=min(
            count,
            len(
                NETWORK_NAMES
            ),
        ),
    )

    networks = []

    connected_index = random.randrange(
        len(
            selected_names
        )
    )

    for index, name in enumerate(
        selected_names
    ):

        networks.append(
            {
                "name":
                    name,

                "level":
                    random.randint(
                        1,
                        3,
                    ),

                "secured":
                    random.random()
                    < 0.85,

                "connected":
                    index
                    == connected_index,
            }
        )

    return networks


# ==========================================================
# Main Generator
# ==========================================================

def generate_login_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            LOGIN_STATES
        )


    if state not in LOGIN_STATES:

        raise ValueError(
            f"Unknown Ubuntu login state: "
            f"{state}"
        )


    # ======================================================
    # Users
    # ======================================================

    users = generate_users()

    active_user = next(
        user
        for user in users
        if user[
            "active"
        ]
    )


    # ======================================================
    # Sessions
    # ======================================================

    sessions = [

        dict(
            session
        )

        for session
        in SESSION_CHOICES
    ]


    selected_session_index = (
        random.randrange(
            len(
                sessions
            )
        )
    )


    for index, session in enumerate(
        sessions
    ):

        session[
            "selected"
        ] = (
            index
            == selected_session_index
        )


    # ======================================================
    # Accessibility
    # ======================================================

    accessibility_entries = []

    for option in ACCESSIBILITY_OPTIONS:

        entry = dict(
            option
        )

        entry[
            "enabled"
        ] = (
            random.random()
            < 0.25
        )

        accessibility_entries.append(
            entry
        )


    # ======================================================
    # Password
    # ======================================================

    password_length = random.randint(
        6,
        12,
    )

    password_value = (
        "ubuntu"
        + str(
            random.randint(
                10,
                99,
            )
        )
    )


    # ======================================================
    # Login Progress
    # ======================================================

    progress = 0

    if state == "logging_in":

        progress = random.randint(
            15,
            85,
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "wallpaper":
            get_random_wallpaper(),

        "users":
            users,

        "active_user":
            active_user,

        "sessions":
            sessions,

        "selected_session":
            sessions[
                selected_session_index
            ],

        "networks":
            generate_networks(),

        "accessibility_entries":
            accessibility_entries,

        "password_value":
            password_value,

        "password_length":
            password_length,

        "password_visible":
            state
            == "password_visible",

        "wrong_password":
            state
            == "wrong_password",

        "progress":
            progress,

        "hostname":
            random.choice(
                [
                    "ubuntu",
                    "workstation",
                    "desktop",
                    "linux-pc",
                ]
            ),
    }