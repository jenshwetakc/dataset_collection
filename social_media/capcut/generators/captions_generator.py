from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


CAPTION_STATES = [
    "setup",
    "generating",
    "captions_ready",
    "caption_editing",
    "style_editing",
    "clear_dialog",
]

CAPTION_TEXTS = [
    "Welcome to a new day.",
    "Sometimes the smallest moments matter most.",
    "Take a little time to explore.",
    "There is something beautiful around every corner.",
    "Find your own rhythm.",
    "Make memories along the way.",
    "Keep creating and keep discovering.",
    "This is just the beginning.",
]

CAPTION_STYLES = [
    {"id": "simple", "name": "Simple", "weight": 400},
    {"id": "bold", "name": "Bold", "weight": 800},
    {"id": "boxed", "name": "Boxed", "weight": 700},
    {"id": "rounded", "name": "Rounded", "weight": 600},
]


def format_time(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def generate_captions_data(
    sample_index: int,
    media_dir: Path | None = None,
) -> dict:
    preferred = media_dir or ASSETS_ROOT / "capcut" / "captions"

    directory = next(
        (
            candidate
            for candidate in (preferred, ASSETS_ROOT)
            if get_image_files(str(candidate))
        ),
        None,
    )

    segments = []
    cursor = 0

    for index, text in enumerate(CAPTION_TEXTS):
        duration = random.randint(3, 6)

        segments.append({
            "id": f"caption_{sample_index}_{index}",
            "start": format_time(cursor),
            "end": format_time(cursor + duration),
            "text": text,
            "selected": False,
        })

        cursor += duration

    return {
        "sample_index": sample_index,
        "state": "setup",
        "popup_visible": False,
        "project_name": random.choice([
            "Morning vlog",
            "Travel story",
            "Creative journal",
        ]),
        "preview_image": (
            get_random_image(directory)
            if directory is not None
            else None
        ),
        "language": random.choice(["English", "Korean", "Japanese"]),
        "languages": ["English", "Korean", "Japanese", "Spanish"],
        "source": "Original audio",
        "sources": ["Original audio", "Voiceover", "All audio"],
        "remove_filler": random.choice([True, False]),
        "bilingual": False,
        "progress": random.randint(25, 85),
        "segments": segments,
        "selected_caption": dict(segments[1]),
        "duration": format_time(cursor),
        "styles": [dict(style) for style in CAPTION_STYLES],
        "selected_style": "boxed",
        "font_size": random.randint(24, 36),
        "position": "Bottom",
        "positions": ["Top", "Center", "Bottom"],
        "show_captions": False,
    }


def apply_captions_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in CAPTION_STATES:
        raise ValueError(f"Unknown caption state: {state}")

    data = dict(base_data)
    data["segments"] = [
        dict(segment)
        for segment in base_data["segments"]
    ]
    data["selected_caption"] = dict(base_data["selected_caption"])
    data["state"] = state
    data["popup_visible"] = state == "clear_dialog"
    data["show_captions"] = state not in {"setup", "generating"}

    if state in {"caption_editing", "style_editing"}:
        data["segments"][1]["selected"] = True
        data["selected_caption"] = dict(data["segments"][1])

    return data