from __future__ import annotations

import random

from datetime import date, timedelta

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


fake = Faker()


SERIES_STATES = [
    "overview",
    "completed",
    "oldest_first",
    "page_2",
    "subscribed",
    "creator_info",
    "share_copied",
    "login_dialog",
]


GENRES = [
    "Action",
    "Fantasy",
    "Romance",
    "Drama",
    "Comedy",
    "Thriller",
]


# ==========================================================
# Media
# ==========================================================

def resolve_media_directory(name: str):
    preferred = (
        ASSETS_ROOT
        / "webtoon"
    )

    if get_image_files(str(preferred)):
        return preferred

    if name == "covers":
        if get_image_files(str(ASSETS_ROOT)):
            return ASSETS_ROOT

    return None


def load_image(directory) -> str | None:
    if directory is None:
        return None

    return get_random_image(directory)


# ==========================================================
# Generate Content Once Per Sample
# ==========================================================

def generate_series_data() -> dict:
    covers_directory = resolve_media_directory(
        "covers"
    )

    banners_directory = resolve_media_directory(
        "banners"
    )

    title = fake.sentence(
        nb_words=random.randint(3, 5),
    ).rstrip(".")

    creators = [
        {
            "role": role,
            "name": fake.name(),
        }
        for role in [
            "Original work by",
            "Written by",
            "Art by",
        ]
    ]

    episode_count = 30

    first_release = (
        date.today()
        - timedelta(
            weeks=episode_count - 1,
        )
    )

    episodes = []

    for number in range(1, episode_count + 1):
        episode_title = fake.sentence(
            nb_words=random.randint(3, 6),
        ).rstrip(".")

        release_date = (
            first_release
            + timedelta(
                weeks=number - 1,
            )
        )

        episodes.append(
            {
                "number": number,
                "title": (
                    f"Ep. {number} - "
                    f"{episode_title}"
                ),
                "date": release_date.strftime(
                    "%b %d, %Y"
                ),
                "likes": (
                    f"{random.randint(12000, 60000):,}"
                ),
                "thumbnail": load_image(
                    covers_directory
                ),
            }
        )

    recommendations = []

    for _ in range(3):
        recommendations.append(
            {
                "title": fake.sentence(
                    nb_words=4,
                ).rstrip("."),
                "creator": fake.name(),
                "cover": load_image(
                    covers_directory
                ),
                "views": (
                    f"{random.uniform(1, 90):.1f}M"
                ),
            }
        )

    return {
        "title": title,
        "genre": random.choice(GENRES),
        "creators": creators,
        "banner": load_image(
            banners_directory
        ),
        "description": fake.paragraph(
            nb_sentences=7,
        ),
        "views": (
            f"{random.uniform(2, 90):.1f}M"
        ),
        "subscribers": (
            f"{random.randint(100000, 900000):,}"
        ),
        "rating": "Young Adult (16+)",
        "schedule": "UP EVERY SUNDAY",
        "episodes": episodes,
        "recommendations": recommendations,
    }


# ==========================================================
# Apply Page State
# ==========================================================

def apply_series_state(
    content: dict,
    state: str,
) -> dict:
    if state not in SERIES_STATES:
        raise ValueError(
            f"Unknown series state: {state}"
        )

    data = dict(content)

    oldest_first = (
        state == "oldest_first"
    )

    ordered_episodes = sorted(
        content["episodes"],
        key=lambda episode: episode["number"],
        reverse=not oldest_first,
    )

    page_number = (
        2
        if state == "page_2"
        else 1
    )

    page_size = 10

    start_index = (
        (page_number - 1)
        * page_size
    )

    data.update(
        {
            "state": state,
            "popup": state in {
                "creator_info",
                "login_dialog",
            },
            "subscribed": (
                state == "subscribed"
            ),
            "sort_label": (
                "Oldest first"
                if oldest_first
                else "Newest first"
            ),
            "page_number": page_number,
            "page_count": (
                len(ordered_episodes)
                + page_size - 1
            ) // page_size,
            "visible_episodes": (
                ordered_episodes[
                    start_index:
                    start_index + page_size
                ]
            ),
            "schedule": (
                "COMPLETED"
                if state == "completed"
                else content["schedule"]
            ),
        }
    )

    return data