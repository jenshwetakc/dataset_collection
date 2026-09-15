from __future__ import annotations

import random

from system.ubuntu.generators.media_generator import (
    get_random_photo,
)


# ==========================================================
# States
# ==========================================================

CAMERA_STATES = [

    "photo_ready",

    "photo_timer",

    "photo_captured",

    "video_ready",

    "video_recording",

    "video_paused",

    "gallery_open",

    "settings_open",

    "device_menu",

    "flash_menu",

    "permission_dialog",

    "delete_media_dialog",
]


# ==========================================================
# Capture Modes
# ==========================================================

CAPTURE_MODES = [

    {
        "id":
            "photo",

        "label":
            "Photo",

        "icon":
            "photo_camera",
    },

    {
        "id":
            "video",

        "label":
            "Video",

        "icon":
            "videocam",
    },
]


# ==========================================================
# Flash Modes
# ==========================================================

FLASH_MODES = [

    {
        "id":
            "auto",

        "label":
            "Auto",

        "icon":
            "flash_auto",
    },

    {
        "id":
            "on",

        "label":
            "On",

        "icon":
            "flash_on",
    },

    {
        "id":
            "off",

        "label":
            "Off",

        "icon":
            "flash_off",
    },
]


# ==========================================================
# Devices
# ==========================================================

CAMERA_DEVICES = [

    {
        "name":
            "Integrated Camera",

        "resolution":
            "1920 × 1080",
    },

    {
        "name":
            "USB Camera",

        "resolution":
            "1280 × 720",
    },

    {
        "name":
            "External HD Webcam",

        "resolution":
            "2560 × 1440",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def format_recording_time(
    seconds: int,
) -> str:

    minutes = seconds // 60

    remaining = seconds % 60

    return (
        f"{minutes:02d}:"
        f"{remaining:02d}"
    )


def generate_gallery() -> list[dict]:

    count = random.randint(
        4,
        8,
    )

    media = []


    for index in range(
        count
    ):

        media_type = random.choice(
            [
                "photo",
                "photo",
                "video",
            ]
        )


        media.append(
            {
                "id":
                    index,

                "type":
                    media_type,

                "src":
                    get_random_photo(),

                "duration":
                    (
                        format_recording_time(
                            random.randint(
                                5,
                                180,
                            )
                        )
                        if media_type
                        == "video"
                        else ""
                    ),

                "selected":
                    False,
            }
        )


    if media:

        media[
            random.randrange(
                len(
                    media
                )
            )
        ][
            "selected"
        ] = True


    return media


# ==========================================================
# Main
# ==========================================================

def generate_camera_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CAMERA_STATES
        )


    if state not in CAMERA_STATES:

        raise ValueError(
            f"Unknown Camera state: "
            f"{state}"
        )


    # ======================================================
    # Mode
    # ======================================================

    if state in {
        "video_ready",
        "video_recording",
        "video_paused",
    }:

        mode = "video"

    else:

        mode = "photo"


    # ======================================================
    # Recording
    # ======================================================

    recording_seconds = random.randint(
        4,
        420,
    )


    # ======================================================
    # Flash
    # ======================================================

    flash_mode = random.choice(
        FLASH_MODES
    )


    # ======================================================
    # Device
    # ======================================================

    selected_device = random.choice(
        CAMERA_DEVICES
    )


    # ======================================================
    # Timer
    # ======================================================

    timer_seconds = random.choice(
        [
            3,
            5,
            10,
        ]
    )


    # ======================================================
    # Gallery
    # ======================================================

    gallery = generate_gallery()


    selected_media = next(
        (
            entry
            for entry in gallery
            if entry[
                "selected"
            ]
        ),
        None,
    )


    return {

        "state":
            state,

        "mode":
            mode,

        "capture_modes":
            [
                dict(
                    entry
                )
                for entry
                in CAPTURE_MODES
            ],

        "flash_modes":
            [
                dict(
                    entry
                )
                for entry
                in FLASH_MODES
            ],

        "flash_mode":
            dict(
                flash_mode
            ),

        "devices":
            [
                dict(
                    entry
                )
                for entry
                in CAMERA_DEVICES
            ],

        "selected_device":
            dict(
                selected_device
            ),

        "timer_seconds":
            timer_seconds,

        "recording_seconds":
            recording_seconds,

        "recording_text":
            format_recording_time(
                recording_seconds
            ),

        "show_grid":
            random.random()
            < 0.55,

        "mirror":
            random.random()
            < 0.35,

        "hdr":
            random.random()
            < 0.45,

        "brightness":
            random.randint(
                25,
                85,
            ),

        "gallery":
            gallery,

        "selected_media":
            selected_media,

        "preview_image":
            get_random_photo(),

        "filename":
            random.choice(
                [
                    "Photo_2026-09-07_1206.jpg",
                    "Camera_2026-09-07.jpg",
                    "IMG_20260907_1206.jpg",
                    "Video_2026-09-07.mp4",
                ]
            ),
    }