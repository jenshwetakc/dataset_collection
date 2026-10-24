from __future__ import annotations

import random

from faker import Faker

from system.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


fake = Faker()


THEMES = [
    {
        "name": "Simple",
        "primary": "#1A73E8",
        "accent": "#E8F0FE",
    },
    {
        "name": "Vision",
        "primary": "#7B1FA2",
        "accent": "#F3E8FD",
    },
    {
        "name": "Impression",
        "primary": "#00897B",
        "accent": "#E0F2F1",
    },
    {
        "name": "Aristotle",
        "primary": "#E37400",
        "accent": "#FEF7E0",
    },
]

PAGE_NAMES = [
    "Home",
    "About",
    "Services",
    "Projects",
    "Contact",
]


def get_asset_image() -> str | None:
    return get_random_image(
        ASSETS_ROOT
    )


def generate_site_page(
    index: int,
    title: str,
) -> dict:
    return {
        "id": f"page-{index}",
        "title": title,
        "slug": (
            "/"
            if index == 0
            else f"/{title.lower()}"
        ),
        "is_home": index == 0,
    }


def generate_sites_data() -> dict:
    site_title = fake.company()
    selected_theme = random.choice(
        THEMES
    )

    page_count = random.randint(3, 5)

    pages = [
        generate_site_page(
            index=index,
            title=PAGE_NAMES[index],
        )
        for index in range(page_count)
    ]

    state = random.choices(
        [
            "editor",
            "pages_panel",
            "themes_panel",
            "preview",
            "publish_dialog",
        ],
        weights=[
            38,
            18,
            18,
            16,
            10,
        ],
        k=1,
    )[0]

    return {
        "app_name": "Google Sites",
        "state": state,
        "site": {
            "title": site_title,
            "subtitle": fake.catch_phrase(),
            "hero_image": get_asset_image(),
            "hero_color": selected_theme["primary"],
            "domain": (
                f"{fake.domain_word()}-"
                f"{random.randint(100, 999)}"
            ),
        },
        "pages": pages,
        "selected_page": random.choice(
            pages
        ),
        "themes": THEMES,
        "selected_theme": selected_theme,
        "sections": [
            {
                "title": fake.sentence(
                    nb_words=random.randint(3, 6)
                ).rstrip("."),
                "body": fake.paragraph(
                    nb_sentences=2
                ),
                "image": get_asset_image(),
            }
            for _ in range(
                random.randint(2, 4)
            )
        ],
    }