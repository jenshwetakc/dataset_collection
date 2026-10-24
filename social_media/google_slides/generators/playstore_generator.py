from __future__ import annotations

import random

from faker import Faker

from system.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


fake = Faker()


CATEGORIES = [
    "Productivity",
    "Photography",
    "Health & Fitness",
    "Education",
    "Finance",
    "Music & Audio",
    "Travel",
    "Shopping",
]

ICON_COLORS = [
    "#1A73E8",
    "#7B1FA2",
    "#00897B",
    "#E37400",
    "#C5221F",
    "#3C4043",
]

APP_SUFFIXES = [
    "Planner",
    "Studio",
    "Tracker",
    "Notes",
    "Wallet",
    "Player",
    "Scanner",
    "Hub",
]


def make_app_name() -> str:
    return (
        f"{fake.word().title()} "
        f"{random.choice(APP_SUFFIXES)}"
    )


def get_asset_image() -> str | None:
    """
    Select a random image from the shared assets folder.

    Returns None when the folder has no supported images,
    allowing the template to use its colored fallback.
    """

    return get_random_image(
        ASSETS_ROOT
    )


def generate_app(
    index: int,
    installed: bool | None = None,
) -> dict:
    if installed is None:
        installed = random.random() < 0.26

    screenshots = []

    for _ in range(
        random.randint(3, 5)
    ):
        screenshots.append(
            {
                "image": get_asset_image(),
                "color": random.choice(
                    ICON_COLORS
                ),
                "title": fake.sentence(
                    nb_words=random.randint(2, 5)
                ).rstrip("."),
            }
        )

    return {
        "id": f"app-{index}",
        "name": make_app_name(),
        "developer": fake.company(),
        "category": random.choice(CATEGORIES),
        "description": fake.paragraph(
            nb_sentences=random.randint(2, 4)
        ),
        "rating": round(
            random.uniform(3.8, 5.0),
            1,
        ),
        "review_count": random.randint(
            1_000,
            950_000,
        ),
        "downloads": random.choice(
            [
                "10K+",
                "50K+",
                "100K+",
                "500K+",
                "1M+",
                "5M+",
                "10M+",
            ]
        ),
        "size": (
            f"{random.randint(12, 180)} MB"
        ),
        "age_rating": random.choice(
            [
                "Everyone",
                "Everyone 10+",
                "Teen",
            ]
        ),
        "version": (
            f"{random.randint(1, 9)}."
            f"{random.randint(0, 9)}."
            f"{random.randint(0, 9)}"
        ),
        "icon_color": random.choice(
            ICON_COLORS
        ),
        "icon_text": fake.lexify(
            text="??"
        ).upper(),
        "icon_image": get_asset_image(),
        "installed": installed,
        "update_available": (
            installed
            and random.random() < 0.58
        ),
        "is_editors_choice": (
            random.random() < 0.22
        ),
        "screenshots": screenshots,
    }


def generate_playstore_data() -> dict:
    apps = [
        generate_app(index)
        for index in range(
            random.randint(18, 28)
        )
    ]

    installed_apps = [
        app
        for app in apps
        if app["installed"]
    ]

    if len(installed_apps) < 3:
        for app in apps[:3]:
            app["installed"] = True
            app["update_available"] = (
                random.random() < 0.65
            )

        installed_apps = [
            app
            for app in apps
            if app["installed"]
        ]

    update_apps = [
        app
        for app in installed_apps
        if app["update_available"]
    ]

    if not update_apps:
        installed_apps[0]["update_available"] = True
        update_apps = [
            installed_apps[0]
        ]

    state = random.choices(
        [
            "home",
            "search_results",
            "app_detail",
            "updates",
            "install_dialog",
        ],
        weights=[
            32,
            22,
            26,
            12,
            8,
        ],
        k=1,
    )[0]

    return {
        "app_name": "Google Play",
        "state": state,
        "categories": CATEGORIES,
        "featured_apps": random.sample(
            apps,
            k=min(5, len(apps)),
        ),
        "recommended_apps": random.sample(
            apps,
            k=min(8, len(apps)),
        ),
        "installed_apps": installed_apps,
        "update_apps": update_apps,
        "selected_app": random.choice(apps),
        "search_query": fake.word(),
        "search_results": random.sample(
            apps,
            k=min(
                len(apps),
                random.randint(5, 9),
            ),
        ),
    }