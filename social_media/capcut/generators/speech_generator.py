from __future__ import annotations

import copy
import random


SPEECH_STATES = (
    "compose",
    "voice_selected",
    "generating",
    "audio_ready",
    "empty_results",
    "generation_failed",
    "replace_dialog",
)


VOICE_CATALOG = (
    {
        "id": "aria",
        "name": "Aria",
        "description": "Clear and conversational",
        "category": "Narration",
        "icon": "record_voice_over",
        "initials": "AR",
    },
    {
        "id": "leo",
        "name": "Leo",
        "description": "Warm storytelling voice",
        "category": "Narration",
        "icon": "auto_stories",
        "initials": "LE",
    },
    {
        "id": "nova",
        "name": "Nova",
        "description": "Bright and energetic",
        "category": "Social",
        "icon": "electric_bolt",
        "initials": "NO",
    },
    {
        "id": "kai",
        "name": "Kai",
        "description": "Relaxed and natural",
        "category": "Social",
        "icon": "chat_bubble",
        "initials": "KA",
    },
    {
        "id": "atlas",
        "name": "Atlas",
        "description": "Deep cinematic delivery",
        "category": "Character",
        "icon": "movie",
        "initials": "AT",
    },
    {
        "id": "pixel",
        "name": "Pixel",
        "description": "Playful character voice",
        "category": "Character",
        "icon": "smart_toy",
        "initials": "PI",
    },
)


SAMPLE_SCRIPTS = (
    "Every great adventure begins with a small step. "
    "Today, we are taking you somewhere unexpected.",

    "Three simple ideas can transform your everyday routine. "
    "Save this video and try your favorite tomorrow.",

    "Welcome to our weekend escape. "
    "Fresh air, quiet moments, and a view worth remembering.",
)


def generate_speech_data(
    *,
    sample_index: int,
) -> dict:
    script = random.choice(SAMPLE_SCRIPTS)

    return {
        "sample_index": sample_index,
        "state": "compose",
        "popup_visible": False,
        "project_name": random.choice(
            [
                "Weekend escape",
                "Creative journal",
                "Daily inspiration",
                "Travel highlights",
            ]
        ),
        "script": script,
        "character_limit": 5000,
        "query": "",
        "categories": [
            "All",
            "Narration",
            "Social",
            "Character",
        ],
        "active_category": "All",
        "voices": [dict(voice) for voice in VOICE_CATALOG],
        "selected_voice_id": None,
        "selected_voice": None,
        "speed": random.choice([0.9, 1.0, 1.1]),
        "pitch": 0,
        "progress": 0,
        "busy": False,
        "audio_visible": False,
        "error_visible": False,
        "error_message": "",
        "audio_name": f"Voiceover {sample_index + 1:03d}",
        "duration_seconds": max(
            5,
            round(len(script.split()) / 2.5),
        ),
        "waveform": [
            random.randint(15, 95)
            for _ in range(48)
        ],
        "status_text": "Choose a voice to get started",
    }


def apply_speech_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in SPEECH_STATES:
        raise ValueError(
            f"Unknown speech state: {state}. "
            f"Expected one of {SPEECH_STATES}"
        )

    data = copy.deepcopy(base_data)

    data.update(
        state=state,
        popup_visible=False,
        selected_voice_id=None,
        selected_voice=None,
        progress=0,
        busy=False,
        audio_visible=False,
        error_visible=False,
        error_message="",
        query="",
        active_category="All",
        status_text="Choose a voice to get started",
    )

    # Rebuild the catalog so applying a new state never inherits
    # a filtered or empty voice list from a previous state.
    data["voices"] = [
        dict(voice)
        for voice in VOICE_CATALOG
    ]

    if state != "compose":
        selected = random.choice(data["voices"])
        data["selected_voice_id"] = selected["id"]
        data["selected_voice"] = dict(selected)
        data["status_text"] = (
            f"{selected['name']} is ready to generate"
        )

    if state == "voice_selected":
        data["active_category"] = (
            data["selected_voice"]["category"]
        )
        data["voices"] = [
            voice
            for voice in data["voices"]
            if voice["category"] == data["active_category"]
        ]

    elif state == "generating":
        data["busy"] = True
        data["progress"] = random.randint(18, 88)
        data["status_text"] = "Generating your voiceover"

    elif state == "audio_ready":
        data["audio_visible"] = True
        data["progress"] = 100
        data["status_text"] = "Your voiceover is ready"

    elif state == "empty_results":
        data["query"] = "whisper robot"
        data["voices"] = []
        data["selected_voice_id"] = None
        data["selected_voice"] = None
        data["status_text"] = "No matching voices"

    elif state == "generation_failed":
        data["error_visible"] = True
        data["error_message"] = (
            "We could not generate this voiceover. "
            "Try again in a moment."
        )
        data["status_text"] = "Generation failed"

    elif state == "replace_dialog":
        data["audio_visible"] = True
        data["progress"] = 100
        data["popup_visible"] = True
        data["status_text"] = "Your voiceover is ready"

    return data