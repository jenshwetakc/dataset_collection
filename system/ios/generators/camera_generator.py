from __future__ import annotations

import random

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


# ==========================================================
# States
# ==========================================================

CAMERA_STATES = [

    "photo_mode",

    "video_mode",

    "video_recording",

    "portrait_mode",

    "night_mode",

    "controls_expanded",

    "photo_preview",

    "camera_permission",
]


CAMERA_STATE_WEIGHTS = [

    24,

    14,

    12,

    12,

    10,

    10,

    10,

    8,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Mode Definitions
# ==========================================================

CAMERA_MODES = [

    {
        "id":
            "cinematic",

        "title":
            "CINEMATIC",
    },

    {
        "id":
            "video",

        "title":
            "VIDEO",
    },

    {
        "id":
            "photo",

        "title":
            "PHOTO",
    },

    {
        "id":
            "portrait",

        "title":
            "PORTRAIT",
    },

    {
        "id":
            "pano",

        "title":
            "PANO",
    },
]


# ==========================================================
# Zoom Levels
# ==========================================================

def generate_zoom_levels() -> list[dict]:

    available = random.choice([

        [
            "0.5",
            "1",
            "2",
        ],

        [
            "0.5",
            "1",
            "3",
        ],

        [
            "1",
            "2",
            "5",
        ],
    ])


    selected = random.choice(
        available
    )


    return [

        {
            "id":
                value,

            "label":
                f"{value}×",

            "selected":
                value
                == selected,
        }

        for value
        in available
    ]


# ==========================================================
# Camera Controls
# ==========================================================

def generate_controls() -> list[dict]:

    return [

        {
            "id":
                "flash",

            "title":
                "Flash",

            "icon":
                get_lucide_icon(
                    "zap"
                ),

            "value":
                random.choice([
                    "Auto",
                    "On",
                    "Off",
                ]),
        },

        {
            "id":
                "night",

            "title":
                "Night Mode",

            "icon":
                get_lucide_icon(
                    "moon"
                ),

            "value":
                random.choice([
                    "Auto",
                    "Off",
                    "3s",
                ]),
        },

        {
            "id":
                "live",

            "title":
                "Live Photo",

            "icon":
                get_lucide_icon(
                    "circle-dot"
                ),

            "value":
                random.choice([
                    "On",
                    "Off",
                ]),
        },

        {
            "id":
                "ratio",

            "title":
                "Aspect Ratio",

            "icon":
                get_lucide_icon(
                    "rectangle-horizontal"
                ),

            "value":
                random.choice([
                    "4:3",
                    "16:9",
                    "Square",
                ]),
        },

        {
            "id":
                "exposure",

            "title":
                "Exposure",

            "icon":
                get_lucide_icon(
                    "sun-medium"
                ),

            "value":
                random.choice([
                    "-0.7",
                    "0.0",
                    "+0.3",
                ]),
        },

        {
            "id":
                "timer",

            "title":
                "Timer",

            "icon":
                get_lucide_icon(
                    "timer"
                ),

            "value":
                random.choice([
                    "Off",
                    "3s",
                    "10s",
                ]),
        },
    ]


# ==========================================================
# Preview Objects
# ==========================================================

def generate_scene_objects() -> list[dict]:

    count = random.randint(
        4,
        8,
    )

    result = []


    for index in range(
        count
    ):

        result.append({

            "id":
                f"scene_{index}",

            "x":
                random.randint(
                    4,
                    78,
                ),

            "y":
                random.randint(
                    12,
                    74,
                ),

            "width":
                random.randint(
                    70,
                    190,
                ),

            "height":
                random.randint(
                    80,
                    220,
                ),

            "kind":
                random.choice([
                    "building",
                    "tree",
                    "person",
                    "object",
                ]),
        })


    return result


# ==========================================================
# Permission
# ==========================================================

def generate_permission() -> dict:

    return {

        "title":
            (
                "“Camera” Would Like "
                "to Access the Camera"
            ),

        "message":
            (
                "Camera access is required "
                "to take photos and videos."
            ),

        "deny":
            "Don't Allow",

        "allow":
            "Allow",
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_camera_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            CAMERA_STATES,

            weights=
                CAMERA_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in CAMERA_STATES:

        raise ValueError(
            f"Unknown Camera state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Active Mode
    # ======================================================

    state_to_mode = {

        "photo_mode":
            "photo",

        "video_mode":
            "video",

        "video_recording":
            "video",

        "portrait_mode":
            "portrait",

        "night_mode":
            "photo",

        "controls_expanded":
            "photo",

        "photo_preview":
            "photo",

        "camera_permission":
            "photo",
    }


    active_mode = state_to_mode[
        state
    ]


    # ======================================================
    # Overlay
    # ======================================================

    is_overlay_state = (
        state
        in {
            "controls_expanded",
            "camera_permission",
        }
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "active_mode":
            active_mode,


        "modes": [

            {
                **mode,

                "selected":
                    mode["id"]
                    == active_mode,
            }

            for mode
            in CAMERA_MODES
        ],


        "zoom_levels":
            generate_zoom_levels(),


        "scene":
            generate_scene_objects(),


        "controls":
            generate_controls(),


        "recording": {

            "active":
                state
                == "video_recording",

            "duration":
                random.choice([
                    "00:08",
                    "00:17",
                    "00:42",
                    "01:03",
                ]),
        },


        "night": {

            "active":
                state
                == "night_mode",

            "duration":
                random.choice([
                    "1s",
                    "2s",
                    "3s",
                ]),
        },


        "portrait": {

            "active":
                state
                == "portrait_mode",

            "instruction":
                random.choice([
                    "Move farther away.",
                    "Natural Light",
                    "Depth Effect",
                ]),
        },


        "permission":
            generate_permission(),


        "icons": {

            "flash":
                get_lucide_icon(
                    "zap"
                ),

            "flash_off":
                get_lucide_icon(
                    "zap-off"
                ),

            "chevron_down":
                get_lucide_icon(
                    "chevron-down"
                ),

            "rotate_camera":
                get_lucide_icon(
                    "switch-camera"
                ),

            "camera":
                resolve_icon(
                    "camera"
                ),

            "photo":
                resolve_icon(
                    "image",
                    "image"
                ),

            "video":
                get_lucide_icon(
                    "video"
                ),

            "moon":
                get_lucide_icon(
                    "moon"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in CAMERA_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_camera_data(
                state=
                    state
            ),

            sort_dicts=False,
        )