from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)
from social_media.webtoon.generators.reader_generator import (
    generate_footer_data,
)


fake = Faker()

GENRE_STATES = [
    "drama",
    "fantasy",
    "romance",
    "sort_likes",
    "sort_date",
    "sort_menu",
    "completed",
    "empty_results",
    "series_preview",
]

GENRES = [
    "Drama",
    "Fantasy",
    "Comedy",
    "Action",
    "Slice of life",
    "Romance",
    "Superhero",
    "Sci-fi",
    "Thriller",
    "Supernatural",
    "Mystery",
    "Sports",
    "Historical",
    "Heartwarming",
    "Horror",
    "Graphic Novel",
    "Informative",
]

SORT_OPTIONS = {
    "popularity": "by Popularity",
    "likes": "by Likes",
    "date": "by Date",
}

COVERS_ROOT = Path(ASSETS_ROOT) / "webtoon"


def load_cover() -> str:
    if not COVERS_ROOT.is_dir():
        raise FileNotFoundError(
            f"Cover directory does not exist: {COVERS_ROOT}"
        )

    if not get_image_files(str(COVERS_ROOT)):
        raise FileNotFoundError(
            f"No supported cover images in: {COVERS_ROOT}"
        )

    image = get_random_image(COVERS_ROOT)

    if not image:
        raise RuntimeError(
            f"Could not load a cover from: {COVERS_ROOT}"
        )

    return image


def generate_genres_data() -> dict:
    series = []

    # Enough entries per genre for meaningful scrolling.
    for genre_index, genre in enumerate(GENRES):
        for index in range(24):
            series.append(
                {
                    "id": f"genre_{genre_index}_series_{index}",
                    "title": fake.sentence(
                        nb_words=random.randint(2, 5)
                    ).rstrip("."),
                    "creator": fake.name(),
                    "genre": genre,
                    "cover": load_cover(),
                    "description": fake.paragraph(
                        nb_sentences=4
                    ),
                    "likes": random.randint(1_000, 5_000_000),
                    "popularity": random.random(),
                    "days_since_release": random.randint(0, 900),
                    # Guarantee completed examples in each genre.
                    "completed": index % 3 == 0,
                    "episodes": random.randint(12, 250),
                    "badge": random.choice(
                        ["", "", "", "NEW", "UP"]
                    ),
                }
            )

    data = {
        "genres": list(GENRES),
        "sort_options": dict(SORT_OPTIONS),
        "series": series,
    }

    data.update(generate_footer_data())

    return data


def apply_genres_state(base_data: dict, state: str) -> dict:
    if state not in GENRE_STATES:
        raise ValueError(f"Unknown genre state: {state}")

    data = deepcopy(base_data)

    active_genre = {
        "fantasy": "Fantasy",
        "romance": "Romance",
    }.get(state, "Drama")

    sort_key = {
        "sort_likes": "likes",
        "sort_date": "date",
    }.get(state, "popularity")

    completed_only = state == "completed"

    results = [
        item
        for item in data["series"]
        if item["genre"] == active_genre
        and (not completed_only or item["completed"])
    ]

    if sort_key == "date":
        results.sort(key=lambda item: item["days_since_release"])
    else:
        results.sort(
            key=lambda item: item[sort_key],
            reverse=True,
        )

    if state == "empty_results":
        # Deliberate synthetic empty fixture.
        results = []

    data.update(
        {
            "state": state,
            "active_genre": active_genre,
            "sort_key": sort_key,
            "sort_label": SORT_OPTIONS[sort_key],
            "sort_open": state == "sort_menu",
            "completed_only": completed_only,
            "results": results,
            "result_count": len(results),
            "popup": state == "series_preview",
            "preview": (
                deepcopy(results[0])
                if state == "series_preview" and results
                else None
            ),
        }
    )

    return data