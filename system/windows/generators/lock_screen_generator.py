from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

LOCK_SCREEN_STATES = [
    "lock_screen",
    "password",
    "pin",
    "wrong_pin",
    "signing_in",
    "user_switcher",
    "accessibility_menu",
    "network_panel",
    "power_menu",
]


# ==========================================================
# Users
# ==========================================================

USER_POOL = [
    {
        "name": "Shweta",
        "initial": "S",
        "account_type": "Local account",
    },
    {
        "name": "Alex Kim",
        "initial": "A",
        "account_type": "Microsoft account",
    },
    {
        "name": "Jordan Lee",
        "initial": "J",
        "account_type": "Local account",
    },
    {
        "name": "Taylor Park",
        "initial": "T",
        "account_type": "Microsoft account",
    },
]


# ==========================================================
# Lock Screen Messages
# ==========================================================

LOCK_MESSAGES = [
    {
        "title": "Calendar",
        "message": "Research meeting at 2:30 PM",
        "icon": "calendar_month",
    },
    {
        "title": "Mail",
        "message": "3 unread messages",
        "icon": "mail",
    },
    {
        "title": "Weather",
        "message": "Clear · 24°C",
        "icon": "sunny",
    },
]


# ==========================================================
# Networks
# ==========================================================

NETWORK_POOL = [
    "Home WiFi",
    "CampusNet",
    "KT_GiGA_5G",
    "Office WiFi",
    "Public WiFi",
]


# ==========================================================
# Accessibility
# ==========================================================

ACCESSIBILITY_ITEMS = [
    {
        "label": "Narrator",
        "icon": "record_voice_over",
    },
    {
        "label": "Magnifier",
        "icon": "zoom_in",
    },
    {
        "label": "High contrast",
        "icon": "contrast",
    },
    {
        "label": "On-screen keyboard",
        "icon": "keyboard",
    },
    {
        "label": "Sticky keys",
        "icon": "keyboard_alt",
    },
]


# ==========================================================
# Power
# ==========================================================

POWER_ITEMS = [
    {
        "label": "Sleep",
        "icon": "bedtime",
    },
    {
        "label": "Shut down",
        "icon": "power_settings_new",
    },
    {
        "label": "Restart",
        "icon": "restart_alt",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_users() -> list[dict]:

    count = random.randint(
        2,
        min(
            4,
            len(USER_POOL),
        ),
    )

    return random.sample(
        USER_POOL,
        k=count,
    )


def generate_networks() -> list[dict]:

    count = random.randint(
        3,
        len(NETWORK_POOL),
    )

    selected = random.choice(
        NETWORK_POOL
    )

    networks = []

    for name in random.sample(
        NETWORK_POOL,
        k=count,
    ):

        networks.append(
            {
                "name":
                    name,

                "connected":
                    name
                    == selected,

                "secured":
                    random.random()
                    < 0.9,

                "strength":
                    random.randint(
                        1,
                        3,
                    ),
            }
        )

    return networks


# ==========================================================
# Main Generator
# ==========================================================

def generate_lock_screen_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            LOCK_SCREEN_STATES
        )


    if state not in LOCK_SCREEN_STATES:

        raise ValueError(
            f"Unknown lock screen state: {state}"
        )


    users = generate_users()

    active_user = random.choice(
        users
    )


    return {

        "state":
            state,

        "active_user":
            active_user,

        "users":
            users,

        "lock_messages":
            random.sample(
                LOCK_MESSAGES,
                k=random.randint(
                    1,
                    len(LOCK_MESSAGES),
                ),
            ),

        "pin_length":
            random.choice(
                [
                    4,
                    6,
                ]
            ),

        "wrong_message":
            (
                "The PIN is incorrect. Try again."
                if state
                == "wrong_pin"
                else None
            ),

        "sign_in_message":
            (
                random.choice(
                    [
                        "Welcome",
                        "Signing in…",
                        "Preparing Windows…",
                    ]
                )
                if state
                == "signing_in"
                else None
            ),

        "networks":
            (
                generate_networks()
                if state
                == "network_panel"
                else []
            ),

        "accessibility_items":
            (
                ACCESSIBILITY_ITEMS
                if state
                == "accessibility_menu"
                else []
            ),

        "power_items":
            (
                POWER_ITEMS
                if state
                == "power_menu"
                else []
            ),
    }