from __future__ import annotations

import random


# ==========================================================
# Desktop States
# ==========================================================

DESKTOP_STATES = [

    "default",

    "selected_icon",

    "context_menu",

    "notification",

    "open_window",

    "multiple_windows",

    "snapped_windows",
]


# ==========================================================
# Desktop Icon Pool
# ==========================================================

DESKTOP_ICON_POOL = [

    {
        "name": "Recycle Bin",
        "icon": "delete",
    },

    {
        "name": "This PC",
        "icon": "computer",
    },

    {
        "name": "Documents",
        "icon": "description",
    },

    {
        "name": "Pictures",
        "icon": "image",
    },

    {
        "name": "Downloads",
        "icon": "download",
    },

    {
        "name": "Projects",
        "icon": "folder",
    },

    {
        "name": "Notes",
        "icon": "note",
    },

    {
        "name": "Browser",
        "icon": "public",
    },
]


# ==========================================================
# Generate Icons
# ==========================================================

def generate_desktop_icons() -> list[dict]:

    count = random.randint(
        4,
        8,
    )


    selected = random.sample(

        DESKTOP_ICON_POOL,

        k=min(
            count,
            len(
                DESKTOP_ICON_POOL
            ),
        ),
    )


    return [

        {
            **item,

            "selected":
                False,
        }

        for item in selected
    ]


# ==========================================================
# Context Menu
# ==========================================================

def generate_context_menu() -> list[dict]:

    return [

        {
            "label": "View",
            "icon": "view_module",
        },

        {
            "label": "Sort by",
            "icon": "sort",
        },

        {
            "label": "Refresh",
            "icon": "refresh",
        },

        {
            "divider": True,
        },

        {
            "label": "New",
            "icon": "add",
        },

        {
            "divider": True,
        },

        {
            "label": "Display settings",
            "icon": "display_settings",
        },

        {
            "label": "Personalize",
            "icon": "palette",
        },
    ]


# ==========================================================
# Window Generator
# ==========================================================

def generate_window(
    window_type: str,
) -> dict:

    if window_type == "explorer":

        return {

            "title":
                random.choice(
                    [
                        "Home",
                        "Documents",
                        "Downloads",
                        "Pictures",
                    ]
                ),

            "icon":
                "folder",

            "type":
                "explorer",
        }


    if window_type == "settings":

        return {

            "title":
                "Settings",

            "icon":
                "settings",

            "type":
                "settings",
        }


    return {

        "title":
            "Application",

        "icon":
            "window",

        "type":
            "generic",
    }


# ==========================================================
# Desktop Generator
# ==========================================================

def generate_desktop_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            DESKTOP_STATES
        )


    if state not in DESKTOP_STATES:

        raise ValueError(
            f"Unknown desktop state: {state}"
        )


    icons = generate_desktop_icons()


    selected_icon_index = None


    if (
        state
        == "selected_icon"
        and icons
    ):

        selected_icon_index = (
            random.randrange(
                len(
                    icons
                )
            )
        )


        icons[
            selected_icon_index
        ][
            "selected"
        ] = True


    return {

        "state":
            state,

        "icons":
            icons,

        "selected_icon_index":
            selected_icon_index,

        "context_menu":
            (
                generate_context_menu()
                if state
                == "context_menu"
                else []
            ),

        "notification":
            (
                {
                    "title":
                        random.choice(
                            [
                                "Mail",
                                "Calendar",
                                "System",
                            ]
                        ),

                    "message":
                        random.choice(
                            [
                                "You have a new message.",
                                "Your meeting starts soon.",
                                "Updates are ready to install.",
                            ]
                        ),

                    "icon":
                        random.choice(
                            [
                                "mail",
                                "event",
                                "notifications",
                            ]
                        ),
                }

                if state
                == "notification"

                else None
            ),

        "windows":
            (
                [
                    generate_window(
                        "explorer"
                    )
                ]

                if state
                == "open_window"

                else
                (
                    [
                        generate_window(
                            "explorer"
                        ),

                        generate_window(
                            "settings"
                        ),
                    ]

                    if state
                    in {
                        "multiple_windows",
                        "snapped_windows",
                    }

                    else []
                )
            ),
    }