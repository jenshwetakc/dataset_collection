from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

SOFTWARE_STATES = [

    "home",

    "categories",

    "category_results",

    "search_open",

    "search_results",

    "app_detail",

    "install_ready",

    "installing",

    "installed",

    "updates",

    "update_available",

    "update_progress",

    "remove_dialog",

    "permissions_dialog",
]


# ==========================================================
# Categories
# ==========================================================

CATEGORIES = [

    {
        "name": "Productivity",
        "icon": "work",
    },

    {
        "name": "Development",
        "icon": "code",
    },

    {
        "name": "Graphics",
        "icon": "palette",
    },

    {
        "name": "Games",
        "icon": "sports_esports",
    },

    {
        "name": "Music & Audio",
        "icon": "music_note",
    },

    {
        "name": "Video",
        "icon": "movie",
    },

    {
        "name": "Education",
        "icon": "school",
    },

    {
        "name": "Utilities",
        "icon": "build",
    },
]


# ==========================================================
# App Definitions
# ==========================================================

APP_NAMES = [

    (
        "Code Studio",
        "code",
        "Development",
    ),

    (
        "Photo Editor",
        "photo",
        "Graphics",
    ),

    (
        "Music Player",
        "headphones",
        "Music & Audio",
    ),

    (
        "Task Planner",
        "task_alt",
        "Productivity",
    ),

    (
        "Video Player",
        "play_circle",
        "Video",
    ),

    (
        "Calculator Pro",
        "calculate",
        "Utilities",
    ),

    (
        "Notes",
        "edit_note",
        "Productivity",
    ),

    (
        "Terminal Tools",
        "terminal",
        "Development",
    ),

    (
        "Drawing Studio",
        "draw",
        "Graphics",
    ),

    (
        "Chess",
        "sports_esports",
        "Games",
    ),

    (
        "Weather",
        "partly_cloudy_day",
        "Utilities",
    ),

    (
        "Study Cards",
        "school",
        "Education",
    ),
]


# ==========================================================
# Helpers
# ==========================================================

def generate_rating() -> float:

    return round(
        random.uniform(
            3.5,
            5.0,
        ),
        1,
    )


def generate_review_count() -> int:

    return random.randint(
        15,
        8500,
    )


def generate_size() -> str:

    return (
        f"{random.randint(18, 850)} MB"
    )


def generate_version() -> str:

    return (
        f"{random.randint(1, 8)}."
        f"{random.randint(0, 9)}."
        f"{random.randint(0, 20)}"
    )


# ==========================================================
# One App
# ==========================================================

def generate_app(
    index: int,
) -> dict:

    name, icon, category = random.choice(
        APP_NAMES
    )

    installed = (
        random.random()
        < 0.24
    )

    update_available = (
        installed
        and random.random()
        < 0.38
    )

    return {

        "id":
            f"app_{index}",

        "name":
            name,

        "icon":
            icon,

        "category":
            category,

        "description":
            fake.sentence(
                nb_words=random.randint(
                    6,
                    12,
                )
            ),

        "rating":
            generate_rating(),

        "reviews":
            generate_review_count(),

        "size":
            generate_size(),

        "version":
            generate_version(),

        "installed":
            installed,

        "update_available":
            update_available,

        "featured":
            random.random()
            < 0.18,

        "verified":
            random.random()
            < 0.45,
    }


# ==========================================================
# App Collection
# ==========================================================

def generate_apps(
    minimum: int = 10,
    maximum: int = 18,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    return [

        generate_app(
            index
        )

        for index in range(
            count
        )
    ]


# ==========================================================
# Generator
# ==========================================================

def generate_software_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SOFTWARE_STATES
        )


    if state not in SOFTWARE_STATES:

        raise ValueError(
            f"Unknown Software state: "
            f"{state}"
        )


    apps = generate_apps()


    # ======================================================
    # Featured Apps
    # ======================================================

    featured_apps = [

        app

        for app in apps

        if app[
            "featured"
        ]
    ]


    if len(
        featured_apps
    ) < 3:

        featured_apps = random.sample(

            apps,

            k=min(
                4,
                len(
                    apps
                ),
            ),
        )


    # ======================================================
    # Selected App
    # ======================================================

    selected_app = None


    if state in {

        "app_detail",

        "install_ready",

        "installing",

        "installed",

        "remove_dialog",

        "permissions_dialog",

    }:

        selected_app = random.choice(
            apps
        )


    # ======================================================
    # State-Specific Install Values
    # ======================================================

    install_progress = 0


    if state == "installing":

        install_progress = random.randint(
            10,
            92,
        )

        if selected_app:

            selected_app[
                "installed"
            ] = False


    elif state == "installed":

        install_progress = 100

        if selected_app:

            selected_app[
                "installed"
            ] = True


    # ======================================================
    # Category
    # ======================================================

    selected_category = random.choice(
        CATEGORIES
    )


    category_apps = [

        app

        for app in apps

        if app[
            "category"
        ]
        == selected_category[
            "name"
        ]
    ]


    if not category_apps:

        category_apps = random.sample(

            apps,

            k=min(
                6,
                len(
                    apps
                ),
            ),
        )


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    if state in {
        "search_open",
        "search_results",
    }:

        search_query = random.choice(
            [
                "code",
                "photo",
                "music",
                "notes",
                "video",
                "tools",
            ]
        )


    search_results = random.sample(

        apps,

        k=min(
            random.randint(
                4,
                8,
            ),
            len(
                apps
            ),
        ),
    )


    # ======================================================
    # Updates
    # ======================================================

    installed_apps = [

        app

        for app in apps

        if app[
            "installed"
        ]
    ]


    if len(
        installed_apps
    ) < 4:

        installed_apps = random.sample(

            apps,

            k=min(
                5,
                len(
                    apps
                ),
            ),
        )

        for app in installed_apps:

            app[
                "installed"
            ] = True


    update_apps = [

        app

        for app in installed_apps

        if app.get(
            "update_available"
        )
    ]


    if not update_apps:

        update_apps = random.sample(

            installed_apps,

            k=min(
                2,
                len(
                    installed_apps
                ),
            ),
        )

        for app in update_apps:

            app[
                "update_available"
            ] = True


    update_progress = 0


    if state == "update_progress":

        update_progress = random.randint(
            12,
            94,
        )


    # ======================================================
    # Permission Entries
    # ======================================================

    permissions = [

        {
            "icon": "folder",
            "label": "Access files in your home folder",
        },

        {
            "icon": "language",
            "label": "Access the network",
        },

        {
            "icon": "notifications",
            "label": "Send desktop notifications",
        },

        {
            "icon": "content_paste",
            "label": "Read and write clipboard content",
        },
    ]


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "apps":
            apps,

        "featured_apps":
            featured_apps,

        "categories":
            [
                dict(
                    category
                )

                for category
                in CATEGORIES
            ],

        "selected_category":
            selected_category,

        "category_apps":
            category_apps,

        "search_query":
            search_query,

        "search_results":
            search_results,

        "selected_app":
            selected_app,

        "install_progress":
            install_progress,

        "installed_apps":
            installed_apps,

        "update_apps":
            update_apps,

        "update_progress":
            update_progress,

        "permissions":
            permissions,
    }