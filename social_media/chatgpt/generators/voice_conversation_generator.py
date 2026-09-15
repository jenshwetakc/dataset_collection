from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Voice States
# ==========================================================

VOICE_STATES = [
    {
        "id": "listening",
        "label": "Listening",
        "icon": "graphic_eq",
    },
    {
        "id": "speaking",
        "label": "Speaking",
        "icon": "volume_up",
    },
    {
        "id": "thinking",
        "label": "Thinking",
        "icon": "auto_awesome",
    },
]


# ==========================================================
# Transcript Content
# ==========================================================

USER_TRANSCRIPTS = [
    "Can you explain this in a simpler way?",
    "How can I improve the dataset quality?",
    "What would be the best next step?",
    "Can you help me understand this result?",
    "How should I structure the implementation?",
]


ASSISTANT_TRANSCRIPTS = [
    (
        "Sure. A good way to approach this is to separate "
        "the shared rendering logic from the page-specific UI."
    ),
    (
        "The important part is to keep the annotation behavior "
        "consistent across every viewport."
    ),
    (
        "You can improve diversity by generating multiple "
        "interaction states and varying the content density."
    ),
    (
        "I would first validate the bounding boxes, then check "
        "how the layout behaves on smaller screens."
    ),
]


# ==========================================================
# Voice Names
# ==========================================================

VOICE_NAMES = [
    "Maple",
    "Cove",
    "Juniper",
    "Vale",
    "Spruce",
]


# ==========================================================
# Generate Wave Bars
# ==========================================================

def generate_waveform() -> list[int]:

    return [
        random.randint(
            20,
            100,
        )
        for _ in range(
            28
        )
    ]


# ==========================================================
# Transcript Items
# ==========================================================

def generate_transcript() -> list[dict]:

    items = []

    count = random.randint(
        3,
        6,
    )

    for index in range(
        count
    ):

        if index % 2 == 0:

            items.append({
                "role":
                    "user",

                "text":
                    random.choice(
                        USER_TRANSCRIPTS
                    ),

                "timestamp":
                    fake.time(
                        pattern="%H:%M"
                    ),
            })

        else:

            items.append({
                "role":
                    "assistant",

                "text":
                    random.choice(
                        ASSISTANT_TRANSCRIPTS
                    ),

                "timestamp":
                    fake.time(
                        pattern="%H:%M"
                    ),
            })

    return items


# ==========================================================
# Main Generator
# ==========================================================

def generate_voice_conversation_data() -> dict:

    state = random.choice(
        VOICE_STATES
    )

    user_name = fake.first_name()

    duration_minutes = random.randint(
        0,
        12,
    )

    duration_seconds = random.randint(
        0,
        59,
    )

    return {

        "page_variant":
            "voice_conversation",

        "model": {
            "name":
                random.choice([
                    "ChatGPT",
                    "GPT-5",
                    "GPT-5 Thinking",
                ]),
        },

        "user": {
            "name":
                user_name,

            "initials":
                user_name[:1].upper(),
        },

        "voice": {

            "name":
                random.choice(
                    VOICE_NAMES
                ),

            "state":
                state["id"],

            "state_label":
                state["label"],

            "state_icon":
                state["icon"],

            "muted":
                random.random()
                < 0.15,

            "speaker_enabled":
                random.random()
                > 0.10,

            "camera_available":
                random.random()
                < 0.45,

            "caption_enabled":
                random.random()
                < 0.40,

            "duration":
                (
                    f"{duration_minutes:02d}:"
                    f"{duration_seconds:02d}"
                ),

            "waveform":
                generate_waveform(),
        },

        "transcript":
            generate_transcript(),

        "show_transcript":
            random.random()
            < 0.75,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_voice_conversation_data()
    )