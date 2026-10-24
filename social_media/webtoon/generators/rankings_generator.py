from __future__ import annotations

import random

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

RANKINGS_STATES = [
    "trending",
    "popular",
    "canvas",
    "genre_selected",
    "genre_menu",
    "search_results",
    "search_empty",
    "series_preview",
]

GENRES = [
    "Romance",
    "Fantasy",
    "Drama",
    "Action",
    "Comedy",
    "Slice of life",
    "Thriller",
    "Supernatural",
]


def format_count(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    return f"{value:,}"


def generate_rankings_data() -> dict:
    covers_root = ASSETS_ROOT / "webtoon"

    if (
        not covers_root.is_dir()
        or not get_image_files(str(covers_root))
    ):
        raise FileNotFoundError(
            f"Add cover images to {covers_root}"
        )

    series = []

    for index in range(60):
        title = fake.sentence(nb_words=4).rstrip(".")

        series.append(
            {
                "id": index,
                "title": title,
                "creator": fake.name(),
                "genre": GENRES[index % len(GENRES)],
                "platform": "Originals" if index < 30 else "Canvas",
                "cover": get_random_image(covers_root),
                "likes": random.randint(10000, 9000000),
                "trending_score": random.random(),
                "movement": random.randint(-12, 12),
                "is_new": random.random() < 0.15,
                "description": fake.paragraph(nb_sentences=4),
            }
        )

    data = {
        "series": series,
        "genres": GENRES.copy(),
    }

    # Keep logos consistent across each sample's states/viewports.
    data.update(generate_footer_data())

    return data


def apply_rankings_state(content: dict, state: str) -> dict:
    if state not in RANKINGS_STATES:
        raise ValueError(f"Unknown rankings state: {state}")

    data = dict(content)

    mode = "Popular" if state == "popular" else "Trending"
    platform = "Canvas" if state == "canvas" else "Originals"
    genre = "Romance" if state == "genre_selected" else "All genres"

    candidates = [
        item
        for item in content["series"]
        if item["platform"] == platform
        and (genre == "All genres" or item["genre"] == genre)
    ]

    candidates.sort(
        key=lambda item: (
            item["likes"]
            if mode == "Popular"
            else item["trending_score"]
        ),
        reverse=True,
    )

    # Assign ranks before searching, preserving ranking positions.
    ranked = [
        {
            **item,
            "rank": index + 1,
            "likes_text": format_count(item["likes"]),
        }
        for index, item in enumerate(candidates)
    ]

    query = ""

    if state == "search_results":
        query = ranked[0]["title"].split()[0]

        ranked = [
            item
            for item in ranked
            if query.lower() in item["title"].lower()
        ]

    elif state == "search_empty":
        query = fake.uuid4()
        ranked = []

    data.update(
        {
            "state": state,
            "popup": state == "series_preview",
            "mode": mode,
            "platform": platform,
            "genre": genre,
            "genre_menu_open": state == "genre_menu",
            "query": query,
            "ranked_series": ranked,
            "preview": ranked[0] if state == "series_preview" else None,
        }
    )

    return data