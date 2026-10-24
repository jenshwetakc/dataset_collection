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

SEARCH_STATES = [
    "discovery",
    "series_results",
    "creator_results",
    "canvas_results",
    "genre_selected",
    "filter_menu",
    "empty_results",
    "login_dialog",
]

GENRES = [
    "All genres",
    "Romance",
    "Fantasy",
    "Drama",
    "Action",
    "Comedy",
    "Thriller",
]

COVERS_ROOT = Path(ASSETS_ROOT) / "webtoon"
AVATARS_ROOT = Path(ASSETS_ROOT)  / "avatars"


def load_image(directory: Path, fallback: Path | None = None) -> str:
    candidates = [directory]

    if fallback is not None:
        candidates.append(fallback)

    for candidate in candidates:
        if not candidate.is_dir():
            continue

        if not get_image_files(str(candidate)):
            continue

        image = get_random_image(candidate)

        if image:
            return image

    raise FileNotFoundError(
        "No supported image assets found in: "
        + ", ".join(str(path) for path in candidates)
    )


def generate_search_data() -> dict:
    # The shared search term ensures that results are genuinely
    # consistent with the displayed query.
    keyword = random.choice(
        ["Moon", "Star", "Dream", "Heart", "Shadow"]
    )

    creators = []

    for index in range(8):
        creators.append(
            {
                "id": f"creator_{index}",
                "name": f"{keyword} {fake.first_name()}",
                "avatar": load_image(
                    AVATARS_ROOT,
                    fallback=COVERS_ROOT,
                ),
                "bio": fake.sentence(nb_words=10),
                "followers": random.randint(500, 180_000),
                "series_count": random.randint(1, 6),
            }
        )

    series = []

    for index in range(24):
        creator = creators[index % len(creators)]

        series.append(
            {
                "id": f"series_{index}",
                "title": (
                    f"{keyword} "
                    f"{fake.word().capitalize()} "
                    f"{fake.word().capitalize()}"
                ),
                "creator": creator["name"],
                "genre": GENRES[1 + index % (len(GENRES) - 1)],
                "platform": "ORIGINALS" if index % 2 == 0 else "CANVAS",
                "cover": load_image(COVERS_ROOT),
                "likes": random.randint(1_000, 4_000_000),
                "is_new": random.random() < 0.2,
            }
        )

    data = {
        "keyword": keyword,
        "genres": list(GENRES),
        "series": series,
        "creators": creators,
        "trending": random.sample(series, 6),
    }

    data.update(generate_footer_data())

    return data


def apply_search_state(base_data: dict, state: str) -> dict:
    if state not in SEARCH_STATES:
        raise ValueError(f"Unknown search state: {state}")

    data = deepcopy(base_data)

    data.update(
        {
            "state": state,
            "popup": state == "login_dialog",
            "query": (
                ""
                if state == "discovery"
                else data["keyword"]
            ),
            "active_tab": (
                "creators"
                if state == "creator_results"
                else "series"
            ),
            "platform": (
                "CANVAS"
                if state == "canvas_results"
                else "All"
            ),
            "selected_genre": (
                "Romance"
                if state == "genre_selected"
                else "All genres"
            ),
            "filter_open": state == "filter_menu",
        }
    )

    if state == "empty_results":
        data["query"] = f"unmatched-{fake.uuid4()[:8]}"

    query = data["query"].casefold().strip()

    series_results = [
        item
        for item in data["series"]
        if query in item["title"].casefold()
        or query in item["creator"].casefold()
    ]

    creator_results = [
        item
        for item in data["creators"]
        if query in item["name"].casefold()
    ]

    if data["platform"] != "All":
        series_results = [
            item
            for item in series_results
            if item["platform"] == data["platform"]
        ]

    if data["selected_genre"] != "All genres":
        series_results = [
            item
            for item in series_results
            if item["genre"] == data["selected_genre"]
        ]

    data["series_results"] = series_results
    data["creator_results"] = creator_results

    data["result_count"] = (
        len(creator_results)
        if data["active_tab"] == "creators"
        else len(series_results)
    )

    return data