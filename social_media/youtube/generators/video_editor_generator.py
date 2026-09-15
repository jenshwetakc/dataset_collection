from __future__ import annotations

import random

from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_thumbnail,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Editor States
# ==========================================================

EDITOR_STATES = [
    "idle",
    "playing",
    "trim_start_selected",
    "trim_end_selected",
    "playhead_middle",
]


# ==========================================================
# Utility
# ==========================================================

def format_duration(
    total_seconds: int,
) -> str:

    minutes = (
        total_seconds
        // 60
    )

    seconds = (
        total_seconds
        % 60
    )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


# ==========================================================
# Video
# ==========================================================

def generate_video() -> dict[str, Any]:

    duration_seconds = random.randint(
        20,
        180,
    )


    return {

        "title":
            (
                fake.sentence(
                    nb_words=random.randint(
                        3,
                        7,
                    )
                )
                .rstrip(".")
            ),

        # Synthetic current frame
        "preview":
            get_random_thumbnail(),

        "duration_seconds":
            duration_seconds,

        "duration_text":
            format_duration(
                duration_seconds
            ),
    }


# ==========================================================
# Timeline Frames
# ==========================================================

def generate_timeline_frames(
    min_items: int = 8,
    max_items: int = 14,
) -> list[dict[str, Any]]:

    count = random.randint(
        min_items,
        max_items,
    )


    return [

        {
            "id":
                f"timeline_frame_{index}",

            "image":
                get_random_thumbnail(),
        }

        for index in range(
            count
        )
    ]


# ==========================================================
# Trim
# ==========================================================

def generate_trim(
    duration_seconds: int,
) -> dict[str, Any]:

    # Leave enough space between handles.

    start_seconds = random.randint(
        0,
        max(
            0,
            int(
                duration_seconds
                * 0.25
            ),
        ),
    )


    end_seconds = random.randint(
        max(
            start_seconds + 5,
            int(
                duration_seconds
                * 0.65
            ),
        ),
        duration_seconds,
    )


    start_percent = (
        start_seconds
        / duration_seconds
        * 100
    )


    end_percent = (
        end_seconds
        / duration_seconds
        * 100
    )


    return {

        "start_seconds":
            start_seconds,

        "end_seconds":
            end_seconds,

        "start_text":
            format_duration(
                start_seconds
            ),

        "end_text":
            format_duration(
                end_seconds
            ),

        "start_percent":
            round(
                start_percent,
                2,
            ),

        "end_percent":
            round(
                end_percent,
                2,
            ),

        "selected_duration_seconds":
            end_seconds
            - start_seconds,

        "selected_duration_text":
            format_duration(
                end_seconds
                - start_seconds
            ),
    }


# ==========================================================
# Playhead
# ==========================================================

def generate_playhead(
    duration_seconds: int,
    trim: dict[str, Any],
    state: str,
) -> dict[str, Any]:

    # ------------------------------------------------------
    # State-specific positions
    # ------------------------------------------------------

    if state == "trim_start_selected":

        current_seconds = (
            trim[
                "start_seconds"
            ]
        )


    elif state == "trim_end_selected":

        current_seconds = (
            trim[
                "end_seconds"
            ]
        )


    elif state == "playhead_middle":

        current_seconds = int(
            (
                trim["start_seconds"]
                +
                trim["end_seconds"]
            )
            / 2
        )


    else:

        current_seconds = random.randint(
            trim["start_seconds"],
            trim["end_seconds"],
        )


    progress_percent = (
        current_seconds
        / duration_seconds
        * 100
    )


    return {

        "current_seconds":
            current_seconds,

        "current_time_text":
            format_duration(
                current_seconds
            ),

        "percent":
            round(
                progress_percent,
                2,
            ),
    }


# ==========================================================
# Playback
# ==========================================================

def generate_playback(
    state: str,
) -> dict[str, Any]:

    playing = (
        state == "playing"
    )


    return {

        "playing":
            playing,

        "paused":
            not playing,

        "play_icon":
            (
                "pause"
                if playing
                else "play_arrow"
            ),

        "play_label":
            (
                "Pause"
                if playing
                else "Play"
            ),
    }


# ==========================================================
# Trim Handle State
# ==========================================================

def generate_handle_state(
    state: str,
) -> dict[str, Any]:

    return {

        "start_selected":
            (
                state
                == "trim_start_selected"
            ),

        "end_selected":
            (
                state
                == "trim_end_selected"
            ),
    }


# ==========================================================
# Editing Tools
# ==========================================================

def generate_tools() -> list[dict[str, Any]]:

    return [

        {
            "label":
                "Sound",

            "icon":
                "music_note",

            "semantic":
                "sound_tool",

            "selected":
                False,
        },

        {
            "label":
                "Text",

            "icon":
                "text_fields",

            "semantic":
                "text_tool",

            "selected":
                False,
        },

        {
            "label":
                "Trim",

            "icon":
                "content_cut",

            "semantic":
                "trim_tool",

            "selected":
                True,
        },

        {
            "label":
                "Filters",

            "icon":
                "filter_vintage",

            "semantic":
                "filter_tool",

            "selected":
                False,
        },

        {
            "label":
                "Adjust",

            "icon":
                "tune",

            "semantic":
                "adjust_tool",

            "selected":
                False,
        },
    ]


# ==========================================================
# Top Bar
# ==========================================================

def generate_top_bar() -> dict[str, Any]:

    return {

        "title":
            "Edit video",

        "cancel_label":
            "Cancel",

        "next_label":
            "Next",

        "show_undo":
            random.random() < 0.90,

        "show_redo":
            random.random() < 0.75,
    }


# ==========================================================
# Optional Track
# ==========================================================

def generate_audio_track() -> dict[str, Any]:

    enabled = (
        random.random()
        < 0.45
    )


    return {

        "enabled":
            enabled,

        "title":
            (
                random.choice(
                    [
                        "Original sound",
                        "Summer Vibes",
                        "Ambient Mix",
                        "Daily Beat",
                        "Background Music",
                    ]
                )
                if enabled
                else None
            ),

        "volume":
            (
                random.randint(
                    20,
                    100,
                )
                if enabled
                else 0
            ),
    }


# ==========================================================
# Editor
# ==========================================================

def generate_video_editor(
    state: str | None = None,
) -> dict[str, Any]:

    if state is None:

        state = random.choice(
            EDITOR_STATES
        )


    if state not in EDITOR_STATES:

        raise ValueError(
            f"Unknown editor state: {state}. "
            f"Expected one of: {EDITOR_STATES}"
        )


    video = (
        generate_video()
    )


    trim = (
        generate_trim(
            duration_seconds=
                video[
                    "duration_seconds"
                ]
        )
    )


    playhead = (
        generate_playhead(

            duration_seconds=
                video[
                    "duration_seconds"
                ],

            trim=
                trim,

            state=
                state,
        )
    )


    return {

        "page_type":
            "video_editor",

        "state":
            state,

        "video":
            video,

        "timeline_frames":
            generate_timeline_frames(),

        "trim":
            trim,

        "playhead":
            playhead,

        "playback":
            generate_playback(
                state
            ),

        "handles":
            generate_handle_state(
                state
            ),

        "tools":
            generate_tools(),

        "top_bar":
            generate_top_bar(),

        "audio":
            generate_audio_track(),

        "layout": {

            "show_timeline":
                True,

            "show_tools":
                True,

            "show_time_labels":
                True,

            "show_audio_track":
                True,
        },
    }


# ==========================================================
# Page Wrapper
# ==========================================================

def generate_video_editor_page(
    state: str | None = None,
) -> dict[str, Any]:

    return (
        generate_video_editor(
            state=state
        )
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE VIDEO EDITOR"
    )

    print(
        "=========================================="
    )


    for state in EDITOR_STATES:

        page = (
            generate_video_editor_page(
                state=state
            )
        )


        print(
            "\n"
            "------------------------------------------"
        )


        print(
            "State:",
            page["state"]
        )


        print(
            "Video:",
            page["video"]["title"]
        )


        print(
            "Duration:",
            page["video"]["duration_text"]
        )


        print(
            "Trim:",
            (
                f"{page['trim']['start_text']}"
                f" → "
                f"{page['trim']['end_text']}"
            )
        )


        print(
            "Selected duration:",
            page["trim"][
                "selected_duration_text"
            ]
        )


        print(
            "Playhead:",
            page["playhead"][
                "current_time_text"
            ]
        )


        print(
            "Playing:",
            page["playback"][
                "playing"
            ]
        )


        print(
            "Start handle selected:",
            page["handles"][
                "start_selected"
            ]
        )


        print(
            "End handle selected:",
            page["handles"][
                "end_selected"
            ]
        )