from __future__ import annotations

import copy
import random
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    image_to_data_uri,
)


EFFECTS_STATES = (
    "browse",
    "search_results",
    "favorites",
    "effect_selected",
    "adjusting",
    "downloading",
    "remove_dialog",
)

EFFECT_CATALOG = (
    ("Soft glow", "Light", "flare"),
    ("Prism", "Light", "filter"),
    ("Neon edges", "Party", "bolt"),
    ("Film grain", "Retro", "grain"),
    ("Vintage frame", "Retro", "photo_filter"),
    ("Dream blur", "Basic", "blur_on"),
    ("Motion trail", "Basic", "animation"),
    ("Color pulse", "Party", "palette"),
    ("Light leak", "Light", "wb_sunny"),
    ("Chromatic", "Basic", "filter_b_and_w"),
    ("VHS texture", "Retro", "videocam"),
    ("Star sparkle", "Light", "auto_awesome"),
    ("Disco flash", "Party", "celebration"),
    ("Soft focus", "Basic", "center_focus_weak"),
    ("Golden hour", "Light", "sunny"),
    ("Old cinema", "Retro", "theaters"),
    ("Electric wave", "Party", "waves"),
    ("Lens bloom", "Light", "camera"),
    ("Frame shake", "Basic", "vibration"),
    ("Paper texture", "Retro", "texture"),
    ("Rainbow glow", "Party", "gradient"),
    ("Edge vignette", "Basic", "vignette"),
    ("Dust particles", "Retro", "scatter_plot"),
    ("Spotlight", "Light", "highlight"),
)


def generate_effects_data(
    *,
    sample_index: int,
    media_dir: Path,
) -> dict:
    image_paths = get_image_files(str(media_dir))

    # Keep the number of embedded source images bounded.
    selected_paths = random.sample(
        list(image_paths),
        min(6, len(image_paths)),
    )

    media_pool = [
        image_to_data_uri(path)
        for path in selected_paths
    ]

    effects = []

    for index, (name, category, icon) in enumerate(EFFECT_CATALOG):
        effects.append({
            "id": f"effect_{index}",
            "name": name,
            "category": category,
            "icon": icon,
            "image": (
                media_pool[index % len(media_pool)]
                if media_pool
                else None
            ),
            "favorite": index % 3 == 0,
            "downloaded": index % 5 != 0,
            "premium": index % 7 == 0,
            "tag": (
                "New"
                if index % 6 == 0
                else "Popular"
                if index % 4 == 0
                else ""
            ),
        })

    selected = effects[0]

    return {
        "sample_index": sample_index,
        "state": "browse",
        "popup_visible": False,
        "project_name": random.choice([
            "Weekend memories",
            "City after dark",
            "Summer collection",
            "Creative moments",
        ]),
        "query": "",
        "active_category": "All",
        "categories": [
            {"name": "All", "icon": "apps"},
            {"name": "Basic", "icon": "tune"},
            {"name": "Light", "icon": "flare"},
            {"name": "Retro", "icon": "theaters"},
            {"name": "Party", "icon": "celebration"},
        ],
        "active_tab": "Video effects",
        "tabs": ["Video effects", "Body effects", "Favorites"],
        "catalog": effects,
        "effects": copy.deepcopy(effects),
        "selected_effect_id": selected["id"],
        "selected_effect": copy.deepcopy(selected),
        "preview_image": media_pool[0] if media_pool else None,
        "preview_label": "Original preview",
        "preview_effect": "none",
        "intensity": 65,
        "speed": 40,
        "size": 55,
        "apply_all": False,
        "download_visible": False,
        "download_progress": 0,
        "status_text": "Explore effects for your next edit",
        "applied": [
            {
                "id": "applied_glow",
                "name": "Soft glow",
                "icon": "flare",
                "range": "00:02 – 00:08",
                "enabled": True,
                "selected": True,
            },
            {
                "id": "applied_grain",
                "name": "Film grain",
                "icon": "grain",
                "range": "00:08 – 00:16",
                "enabled": True,
                "selected": False,
            },
            {
                "id": "applied_prism",
                "name": "Prism",
                "icon": "filter",
                "range": "00:16 – 00:24",
                "enabled": False,
                "selected": False,
            },
        ],
        "clips": [
            {
                "name": name,
                "duration": duration,
                "image": (
                    media_pool[index % len(media_pool)]
                    if media_pool
                    else None
                ),
                "selected": index == 1,
            }
            for index, (name, duration) in enumerate([
                ("Opening", "00:06"),
                ("City walk", "00:08"),
                ("Details", "00:05"),
                ("Sunset", "00:07"),
                ("Closing", "00:04"),
            ])
        ],
    }


def apply_effects_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in EFFECTS_STATES:
        raise ValueError(
            f"Unknown effects state: {state}"
        )

    data = copy.deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": False,
        "query": "",
        "active_category": "All",
        "active_tab": "Video effects",
        "effects": copy.deepcopy(data["catalog"]),
        "download_visible": False,
        "download_progress": 0,
        "preview_effect": "none",
        "preview_label": "Original preview",
        "status_text": "Explore effects for your next edit",
    })

    if state == "search_results":
        data["query"] = "glow"
        data["effects"] = [
            effect
            for effect in data["catalog"]
            if "glow" in effect["name"].lower()
        ]
        data["status_text"] = (
            f"{len(data['effects'])} matching effects"
        )

    elif state == "favorites":
        data["active_tab"] = "Favorites"
        data["effects"] = [
            effect
            for effect in data["catalog"]
            if effect["favorite"]
        ]
        data["status_text"] = "Your saved effects"

    elif state in {"effect_selected", "adjusting"}:
        data["preview_effect"] = "glow"
        data["preview_label"] = "Soft glow preview"
        data["status_text"] = "Soft glow selected"

        if state == "adjusting":
            data["intensity"] = 85
            data["speed"] = 60
            data["size"] = 75
            data["apply_all"] = True
            data["status_text"] = "Adjustments ready to apply"

    elif state == "downloading":
        data["download_visible"] = True
        data["download_progress"] = random.randint(20, 85)
        data["status_text"] = "Downloading Soft glow"

    elif state == "remove_dialog":
        data["popup_visible"] = True
        data["preview_effect"] = "glow"
        data["preview_label"] = "Soft glow preview"
        data["status_text"] = "3 effects on your timeline"

    return data