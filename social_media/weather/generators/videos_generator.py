from __future__ import annotations

import random

from copy import deepcopy
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


VIDEO_STATES = [
    "overview",
    "playing",
    "paused",
    "category_filtered",
    "empty_results",
    "share_dialog",
    "playback_settings",
]

CATEGORIES = [
    "All",
    "Forecast",
    "Severe Weather",
    "Science",
    "Nature",
]

VIDEO_TITLES = [
    ("Your regional forecast explained", "Forecast"),
    ("A closer look at approaching storms", "Severe Weather"),
    ("How clouds form above the mountains", "Science"),
    ("Rainfall patterns across the region", "Forecast"),
    ("The changing colors of autumn", "Nature"),
    ("Understanding lightning and thunder", "Science"),
    ("Strong winds move through the coast", "Severe Weather"),
    ("Snow transforms a mountain landscape", "Nature"),
    ("What the weekend forecast could bring", "Forecast"),
]


def time_text(seconds: int) -> str:
    minutes, remaining = divmod(seconds, 60)
    return f"{minutes}:{remaining:02d}"


def generate_videos_data(
    *,
    sample_index: int,
    images_dir: Path | None = None,
) -> dict:
    can_load_images = (
        images_dir is not None
        and Path(images_dir).is_dir()
        and bool(get_image_files(str(images_dir)))
    )

    videos = []

    for index, (title, category) in enumerate(
        random.sample(VIDEO_TITLES, len(VIDEO_TITLES))
    ):
        duration = random.randint(90, 360)

        videos.append({
            "id": index,
            "title": title,
            "category": category,
            "duration_seconds": duration,
            "duration": time_text(duration),
            "views": f"{random.randint(2, 98)}K views",
            "published": (
                f"{random.randint(1, 12)} hours ago"
            ),
            "image": (
                get_random_image(Path(images_dir))
                if can_load_images
                else None
            ),
        })

    return {
        "sample_index": sample_index,
        "location": "Seoul, South Korea",
        "categories": list(CATEGORIES),
        "videos": videos,
        "featured": deepcopy(videos[0]),
        "quality": random.choice(["Auto", "720p", "1080p"]),
        "speed": "1×",
        "captions": random.choice([True, False]),
        "autoplay": random.choice([True, False]),
        "volume": random.choice([40, 65, 85]),
    }


def apply_videos_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in VIDEO_STATES:
        raise ValueError(
            f"Unknown video state: {state!r}"
        )

    data = deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": state in {
            "share_dialog",
            "playback_settings",
        },
        "popup_type": (
            state
            if state in {
                "share_dialog",
                "playback_settings",
            }
            else None
        ),
        "playing": state == "playing",
        "started": state in {
            "playing",
            "paused",
            "share_dialog",
            "playback_settings",
        },
        "active_category": (
            "Severe Weather"
            if state == "category_filtered"
            else "All"
        ),
        "search_query": (
            "Volcanic snow forecast"
            if state == "empty_results"
            else ""
        ),
        "share_url": (
            "https://weather.example/videos/"
            f"{data['featured']['id']}"
        ),
    })

    if state == "empty_results":
        visible_videos = []

    elif state == "category_filtered":
        visible_videos = [
            video
            for video in data["videos"]
            if video["category"] == "Severe Weather"
        ]

        data["featured"] = deepcopy(visible_videos[0])

    else:
        visible_videos = deepcopy(data["videos"])

    data["visible_videos"] = visible_videos

    duration = data["featured"]["duration_seconds"]

    data["elapsed_seconds"] = (
        duration // 3
        if data["started"]
        else 0
    )

    data["elapsed"] = time_text(
        data["elapsed_seconds"]
    )

    data["progress_percent"] = round(
        data["elapsed_seconds"] / duration * 100
    )

    return data