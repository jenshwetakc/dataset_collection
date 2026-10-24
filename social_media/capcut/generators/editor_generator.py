from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


EDITOR_STATES = [
    "overview",
    "clip_selected",
    "text_editing",
    "audio_editing",
    "effects",
    "export_dialog",
]

EDITOR_TOOLS = [
    {"id": "media", "label": "Media", "icon": "video_library"},
    {"id": "audio", "label": "Audio", "icon": "music_note"},
    {"id": "text", "label": "Text", "icon": "title"},
    {"id": "effects", "label": "Effects", "icon": "auto_awesome"},
]

AUDIO_NAMES = [
    "Morning light",
    "City rhythm",
    "Quiet moments",
    "Summer breeze",
    "After sunset",
]

EFFECTS = [
    {"name": "Original", "icon": "image"},
    {"name": "Soft glow", "icon": "flare"},
    {"name": "Film grain", "icon": "grain"},
    {"name": "Dreamy", "icon": "blur_on"},
    {"name": "Neon", "icon": "wb_iridescent"},
    {"name": "Vintage", "icon": "filter_vintage"},
]


def resolve_media_directory(
    preferred: Path,
) -> Path | None:
    for directory in (preferred, ASSETS_ROOT):
        if get_image_files(str(directory)):
            return directory

    return None


def generate_editor_data(
    sample_index: int,
    media_dir: Path | None = None,
) -> dict:
    directory = resolve_media_directory(
        media_dir or ASSETS_ROOT / "capcut" / "editor"
    )

    media = []

    for index in range(random.randint(6, 10)):
        media.append({
            "id": f"media_{sample_index}_{index}",
            "name": f"Clip {index + 1:02d}",
            "image": (
                get_random_image(directory)
                if directory is not None
                else None
            ),
            "duration": random.randint(3, 9),
        })

    clips = []
    start = 0

    for index, item in enumerate(media[:5]):
        duration = item["duration"]

        clips.append({
            "id": f"clip_{sample_index}_{index}",
            "name": item["name"],
            "image": item["image"],
            "start": start,
            "duration": duration,
            "selected": False,
        })

        start += duration

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "project_name": random.choice([
            "Weekend diary",
            "City memories",
            "My creative story",
            "Travel highlights",
        ]),
        "active_tool": "media",
        "tools": [dict(tool) for tool in EDITOR_TOOLS],
        "media": media,
        "clips": clips,
        "preview_image": media[0]["image"],
        "duration": start,
        "duration_text": f"00:{start:02d}",
        "current_time": "00:03",
        "playhead_percent": round(3 / start * 100, 2),
        "selected_clip": dict(clips[0]),
        "show_text": False,
        "overlay_text": "My favorite moments",
        "font_size": 32,
        "text_style": "Bold",
        "volume": random.randint(55, 90),
        "speed": "1.0×",
        "audio_tracks": [
            {
                "id": f"audio_{index}",
                "name": name,
                "duration": random.choice(["01:24", "02:10", "00:58"]),
            }
            for index, name in enumerate(AUDIO_NAMES)
        ],
        "effects": [dict(effect) for effect in EFFECTS],
        "selected_effect": "Soft glow",
        "effect_intensity": 65,
        "export_name": f"capcut_project_{sample_index:04d}",
        "resolution": "1080p",
        "frame_rate": "30 fps",
        "format": "MP4",
        "save_to_device": True,
        "estimated_size": f"{random.randint(25, 95)} MB",
    }


def apply_editor_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in EDITOR_STATES:
        raise ValueError(f"Unknown editor state: {state}")

    data = dict(base_data)
    data["clips"] = [
        dict(clip)
        for clip in base_data["clips"]
    ]
    data["selected_clip"] = dict(base_data["selected_clip"])
    data["state"] = state
    data["popup_visible"] = state == "export_dialog"
    data["show_text"] = state == "text_editing"

    data["active_tool"] = {
        "overview": "media",
        "clip_selected": "media",
        "text_editing": "text",
        "audio_editing": "audio",
        "effects": "effects",
        "export_dialog": "media",
    }[state]

    if state == "clip_selected":
        data["clips"][0]["selected"] = True

    return data