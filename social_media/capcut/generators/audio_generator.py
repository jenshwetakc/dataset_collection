from __future__ import annotations

import copy
import random


AUDIO_STATES = (
    "browse",
    "search_results",
    "favorites",
    "track_selected",
    "mixing",
    "recording",
    "download_progress",
    "delete_dialog",
)


def generate_audio_data(
    *,
    sample_index: int,
) -> dict:
    categories = [
        ("All", "library_music"),
        ("Travel", "flight"),
        ("Lifestyle", "local_cafe"),
        ("Cinematic", "movie"),
        ("Electronic", "equalizer"),
        ("Acoustic", "music_note"),
    ]

    titles = [
        "Golden Morning", "City Lights", "Ocean Drive",
        "Quiet Moments", "Weekend Escape", "Neon Skyline",
        "Open Roads", "Little Stories", "Summer Breeze",
        "Midnight Motion", "Warm Memories", "New Horizons",
        "Coffee Break", "Electric Dreams", "Mountain Air",
        "Slow Sunday", "Bright Future", "After Hours",
        "Home Again", "First Light", "Urban Rhythm",
        "Paper Planes", "Moonlit Walk", "Fresh Start",
    ]

    tracks = []

    for index, title in enumerate(titles):
        duration = random.randint(95, 240)

        tracks.append({
            "id": f"track_{index}",
            "title": title,
            "artist": [
                "North Avenue",
                "Studio Collective",
                "Daylight Audio",
                "Open Frame",
            ][index % 4],
            "category": categories[1 + index % 5][0],
            "duration": f"{duration // 60}:{duration % 60:02d}",
            "bpm": random.choice([80, 96, 110, 124, 140]),
            "favorite": index % 3 == 0,
            "downloaded": index % 4 != 0,
            "tag": "Trending" if index % 5 == 0 else "",
            "waveform": [
                random.randint(15, 95)
                for _ in range(24)
            ],
        })

    return {
        "sample_index": sample_index,
        "state": "browse",
        "popup_visible": False,
        "project_name": random.choice([
            "Travel diary",
            "Weekend collection",
            "City highlights",
        ]),
        "query": "",
        "active_tab": "Music",
        "tabs": ["Music", "Sound effects", "Favorites", "Your audio"],
        "categories": [
            {"name": name, "icon": icon}
            for name, icon in categories
        ],
        "active_category": "All",
        "catalog": tracks,
        "tracks": copy.deepcopy(tracks),
        "selected_track": copy.deepcopy(tracks[0]),
        "selected_track_id": None,
        "volume": 75,
        "fade_in": 1,
        "fade_out": 2,
        "noise_reduction": False,
        "ducking": False,
        "recording": False,
        "recording_seconds": 0,
        "downloading": False,
        "download_progress": 0,
        "status_text": "Find the right sound for your story",
        "sound_effects": [
            {"name": "Camera shutter", "icon": "photo_camera", "duration": "0:01"},
            {"name": "Soft whoosh", "icon": "air", "duration": "0:02"},
            {"name": "Notification", "icon": "notifications", "duration": "0:01"},
            {"name": "Ocean waves", "icon": "waves", "duration": "0:12"},
            {"name": "Applause", "icon": "celebration", "duration": "0:05"},
            {"name": "Keyboard", "icon": "keyboard", "duration": "0:03"},
        ],
        "timeline": [
            {
                "name": "Video",
                "icon": "movie",
                "clips": ["Opening", "City walk", "Sunset", "Closing"],
                "muted": False,
            },
            {
                "name": "Music",
                "icon": "music_note",
                "clips": ["Golden Morning", "Golden Morning"],
                "muted": False,
            },
            {
                "name": "Voiceover",
                "icon": "mic",
                "clips": ["Introduction", "Travel notes", "Final thoughts"],
                "muted": False,
            },
            {
                "name": "Sound FX",
                "icon": "graphic_eq",
                "clips": ["Whoosh", "Shutter", "Ocean"],
                "muted": True,
            },
        ],
    }


def apply_audio_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in AUDIO_STATES:
        raise ValueError(f"Unknown audio state: {state}")

    data = copy.deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": False,
        "query": "",
        "active_tab": "Music",
        "active_category": "All",
        "tracks": copy.deepcopy(data["catalog"]),
        "selected_track": copy.deepcopy(data["catalog"][0]),
        "selected_track_id": None,
        "volume": 75,
        "fade_in": 1,
        "fade_out": 2,
        "noise_reduction": False,
        "ducking": False,
        "recording": False,
        "recording_seconds": 0,
        "downloading": False,
        "download_progress": 0,
        "status_text": "Find the right sound for your story",
    })

    if state == "search_results":
        data["query"] = "Travel"
        data["tracks"] = [
            track
            for track in data["catalog"]
            if track["category"] == "Travel"
        ]
        data["status_text"] = "Travel music search results"

    elif state == "favorites":
        data["active_tab"] = "Favorites"
        data["tracks"] = [
            track
            for track in data["catalog"]
            if track["favorite"]
        ]
        data["status_text"] = "Your saved music"

    elif state in {
        "track_selected",
        "mixing",
        "download_progress",
        "delete_dialog",
    }:
        # Track 1 is already downloaded.
        selected_index = 0 if state == "download_progress" else 1

        data["selected_track"] = copy.deepcopy(
            data["catalog"][selected_index]
        )
        data["selected_track_id"] = data["selected_track"]["id"]
        data["status_text"] = (
            f"Selected: {data['selected_track']['title']}"
        )

        if state == "mixing":
            data.update({
                "volume": 45,
                "fade_in": 3,
                "fade_out": 4,
                "noise_reduction": True,
                "ducking": True,
                "status_text": "Audio mix adjustments ready",
            })

        elif state == "download_progress":
            data["downloading"] = True
            data["download_progress"] = random.randint(20, 85)
            data["status_text"] = "Downloading selected music"

        elif state == "delete_dialog":
            data["popup_visible"] = True

    elif state == "recording":
        data["recording"] = True
        data["recording_seconds"] = random.randint(5, 45)
        data["status_text"] = "Recording a new voiceover"

    return data