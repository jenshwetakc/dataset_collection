from __future__ import annotations

import random

from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
    get_random_thumbnail,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Player States
# ==========================================================

PLAYER_STATES = [
    "controls_visible",
    "controls_hidden",
    "paused",
    "seeking_backward",
    "seeking_forward",
]


# ==========================================================
# Utility
# ==========================================================

def format_count(
    value: int,
) -> str:

    if value >= 1_000_000_000:

        value = value / 1_000_000_000

        return (
            f"{value:.1f}B"
            .replace(".0B", "B")
        )

    if value >= 1_000_000:

        value = value / 1_000_000

        return (
            f"{value:.1f}M"
            .replace(".0M", "M")
        )

    if value >= 1_000:

        value = value / 1_000

        return (
            f"{value:.1f}K"
            .replace(".0K", "K")
        )

    return str(value)


# ==========================================================
# Time Formatting
# ==========================================================

def format_duration(
    total_seconds: int,
) -> str:

    hours = (
        total_seconds
        // 3600
    )

    minutes = (
        total_seconds
        % 3600
    ) // 60

    seconds = (
        total_seconds
        % 60
    )

    if hours > 0:

        return (
            f"{hours}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    return (
        f"{minutes}:"
        f"{seconds:02d}"
    )


# ==========================================================
# Channel
# ==========================================================

def generate_channel_name() -> str:

    return random.choice(
        [
            fake.name(),

            f"{fake.first_name()} Tech",

            f"{fake.word().title()} Studio",

            f"{fake.word().title()} Official",

            f"The {fake.last_name()} Show",

            f"{fake.word().title()} Academy",
        ]
    )


def generate_channel() -> dict[str, Any]:

    subscribers = random.randint(
        1_000,
        40_000_000,
    )

    return {

        "name":
            generate_channel_name(),

        "avatar":
            get_random_avatar(),

        "verified":
            random.random() < 0.40,

        "subscribers":
            subscribers,

        "subscribers_text":
            (
                f"{format_count(subscribers)} "
                f"subscribers"
            ),
    }


# ==========================================================
# Video
# ==========================================================

def generate_video_title() -> str:

    if random.random() < 0.45:

        return random.choice(
            [
                "Building a Complete App From Scratch",
                "A Day in My Life",
                "Machine Learning Explained",
                "The Ultimate Travel Guide",
                "Everything You Need to Know",
                "Programming Tips You Should Know",
                "Exploring the City at Night",
                "New Technology Explained",
                "Full Tutorial for Beginners",
                "Behind the Scenes",
            ]
        )

    return (
        fake.sentence(
            nb_words=random.randint(
                5,
                12,
            )
        )
        .rstrip(".")
    )


def generate_video() -> dict[str, Any]:

    # ------------------------------------------------------
    # Full video duration
    # ------------------------------------------------------

    duration_seconds = random.randint(
        120,
        7200,
    )


    # ------------------------------------------------------
    # Current playback position
    # ------------------------------------------------------

    current_seconds = random.randint(
        0,
        max(
            1,
            duration_seconds - 1,
        ),
    )


    progress_percent = (
        current_seconds
        / duration_seconds
        * 100
    )


    views = random.randint(
        100,
        300_000_000,
    )


    return {

        "title":
            generate_video_title(),

        # We reuse a thumbnail as a synthetic current
        # video frame.
        "frame":
            get_random_thumbnail(),

        "channel":
            generate_channel(),

        "duration_seconds":
            duration_seconds,

        "duration_text":
            format_duration(
                duration_seconds
            ),

        "current_seconds":
            current_seconds,

        "current_time_text":
            format_duration(
                current_seconds
            ),

        "progress_percent":
            round(
                progress_percent,
                2,
            ),

        "views":
            views,

        "views_text":
            (
                f"{format_count(views)} "
                f"views"
            ),
    }


# ==========================================================
# Volume
# ==========================================================

def generate_volume() -> dict[str, Any]:

    muted = (
        random.random()
        < 0.12
    )


    if muted:

        level = 0

    else:

        level = random.randint(
            10,
            100,
        )


    if muted:

        icon = "volume_off"

    elif level < 35:

        icon = "volume_down"

    else:

        icon = "volume_up"


    return {

        "muted":
            muted,

        "level":
            level,

        "icon":
            icon,
    }


# ==========================================================
# Player Settings
# ==========================================================

def generate_settings() -> dict[str, Any]:

    playback_speed = random.choice(
        [
            "0.75",
            "1",
            "1",
            "1",
            "1.25",
            "1.5",
        ]
    )


    quality = random.choice(
        [
            "360p",
            "480p",
            "720p",
            "1080p",
            "1440p",
            "2160p",
        ]
    )


    captions_enabled = (
        random.random()
        < 0.30
    )


    autoplay = (
        random.random()
        < 0.65
    )


    return {

        "playback_speed":
            playback_speed,

        "quality":
            quality,

        "captions_enabled":
            captions_enabled,

        "autoplay":
            autoplay,
    }


# ==========================================================
# Seek Feedback
# ==========================================================

def generate_seek_feedback(
    state: str,
) -> dict[str, Any] | None:

    if state == "seeking_backward":

        return {

            "direction":
                "backward",

            "seconds":
                10,

            "label":
                "10 seconds",

            "icon":
                "replay_10",
        }


    if state == "seeking_forward":

        return {

            "direction":
                "forward",

            "seconds":
                10,

            "label":
                "10 seconds",

            "icon":
                "forward_10",
        }


    return None


# ==========================================================
# Playback
# ==========================================================

def generate_playback(
    state: str,
) -> dict[str, Any]:

    # ------------------------------------------------------
    # State-specific playback status
    # ------------------------------------------------------

    if state == "paused":

        paused = True

    elif state in {
        "seeking_backward",
        "seeking_forward",
    }:

        paused = random.random() < 0.35

    else:

        paused = False


    # ------------------------------------------------------
    # Whether controls are visible
    # ------------------------------------------------------

    controls_visible = (
        state
        != "controls_hidden"
    )


    # ------------------------------------------------------
    # Center controls
    # ------------------------------------------------------

    center_controls_visible = (
        state
        in {
            "controls_visible",
            "paused",
            "seeking_backward",
            "seeking_forward",
        }
    )


    return {

        "paused":
            paused,

        "playing":
            not paused,

        "controls_visible":
            controls_visible,

        "center_controls_visible":
            center_controls_visible,

        "play_icon":
            (
                "play_arrow"
                if paused
                else "pause"
            ),

        "play_label":
            (
                "Play"
                if paused
                else "Pause"
            ),
    }


# ==========================================================
# Top Controls
# ==========================================================

def generate_top_controls() -> dict[str, Any]:

    return {

        "show_back":
            True,

        "show_cast":
            random.random() < 0.70,

        "show_more":
            True,
    }


# ==========================================================
# Bottom Controls
# ==========================================================

def generate_bottom_controls() -> dict[str, Any]:

    return {

        "show_previous":
            random.random() < 0.30,

        "show_next":
            True,

        "show_volume":
            True,

        "show_captions":
            True,

        "show_settings":
            True,

        "show_miniplayer":
            True,

        "show_theater":
            True,

        "show_fullscreen":
            True,
    }


# ==========================================================
# Center Controls
# ==========================================================

def generate_center_controls() -> dict[str, Any]:

    return {

        "seek_backward_seconds":
            10,

        "seek_forward_seconds":
            10,

        "backward_icon":
            "replay_10",

        "forward_icon":
            "forward_10",
    }


# ==========================================================
# Fullscreen Player
# ==========================================================

def generate_fullscreen_player(
    state: str | None = None,
) -> dict[str, Any]:

    if state is None:

        state = random.choice(
            PLAYER_STATES
        )


    if state not in PLAYER_STATES:

        raise ValueError(
            f"Unknown player state: {state}. "
            f"Expected one of: {PLAYER_STATES}"
        )


    video = (
        generate_video()
    )


    playback = (
        generate_playback(
            state
        )
    )


    seek_feedback = (
        generate_seek_feedback(
            state
        )
    )


    return {

        "page_type":
            "fullscreen_player",

        "state":
            state,

        "video":
            video,

        "playback":
            playback,

        "volume":
            generate_volume(),

        "settings":
            generate_settings(),

        "seek_feedback":
            seek_feedback,

        "top_controls":
            generate_top_controls(),

        "center_controls":
            generate_center_controls(),

        "bottom_controls":
            generate_bottom_controls(),

        # --------------------------------------------------
        # UI Overlay Configuration
        # --------------------------------------------------

        "overlay": {

            "show_top_gradient":
                playback[
                    "controls_visible"
                ],

            "show_bottom_gradient":
                playback[
                    "controls_visible"
                ],

            "show_title":
                playback[
                    "controls_visible"
                ],

            "show_channel":
                (
                    playback[
                        "controls_visible"
                    ]
                    and
                    random.random() < 0.65
                ),

            "show_seek_feedback":
                seek_feedback
                is not None,
        },
    }


# ==========================================================
# Page Wrapper
# ==========================================================

def generate_fullscreen_player_page(
    state: str | None = None,
) -> dict[str, Any]:

    return (
        generate_fullscreen_player(
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
        "YOUTUBE FULLSCREEN PLAYER"
    )

    print(
        "=========================================="
    )


    for state in PLAYER_STATES:

        page = (
            generate_fullscreen_player_page(
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
            "Time:",
            (
                f"{page['video']['current_time_text']}"
                f" / "
                f"{page['video']['duration_text']}"
            )
        )


        print(
            "Progress:",
            (
                f"{page['video']['progress_percent']}%"
            )
        )


        print(
            "Paused:",
            page["playback"]["paused"]
        )


        print(
            "Controls visible:",
            page["playback"][
                "controls_visible"
            ]
        )


        print(
            "Seek feedback:",
            page["seek_feedback"]
        )