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
# Upload States
# ==========================================================

UPLOAD_STATES = [
    "select_file",
    "uploading",
    "details",
    "processing",
    "ready_to_publish",
]


# ==========================================================
# Utility
# ==========================================================

def format_file_size(
    size_mb: float,
) -> str:

    if size_mb >= 1024:

        size_gb = (
            size_mb
            / 1024
        )

        return (
            f"{size_gb:.1f} GB"
        )

    return (
        f"{size_mb:.0f} MB"
    )


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
# Video File
# ==========================================================

def generate_video_file() -> dict[str, Any]:

    file_size_mb = random.uniform(
        30,
        2400,
    )

    duration_seconds = random.randint(
        20,
        1800,
    )

    return {

        "filename":
            random.choice(
                [
                    "my_video.mp4",
                    "final_edit.mp4",
                    "travel_vlog.mp4",
                    "tutorial_final.mp4",
                    "video_export.mp4",
                    "youtube_upload.mp4",
                    "project_video.mp4",
                ]
            ),

        "size_mb":
            round(
                file_size_mb,
                2,
            ),

        "size_text":
            format_file_size(
                file_size_mb
            ),

        "duration_seconds":
            duration_seconds,

        "duration_text":
            format_duration(
                duration_seconds
            ),

        "format":
            "MP4",

        "resolution":
            random.choice(
                [
                    "720p",
                    "1080p",
                    "1080p",
                    "1440p",
                    "2160p",
                ]
            ),
    }


# ==========================================================
# Upload Progress
# ==========================================================

def generate_upload_progress(
    state: str,
) -> dict[str, Any]:

    if state == "select_file":

        percent = 0

        status = (
            "Waiting for a file"
        )


    elif state == "uploading":

        percent = random.randint(
            8,
            92,
        )

        status = (
            f"Uploading {percent}%"
        )


    elif state == "processing":

        percent = 100

        status = (
            "Processing video"
        )


    else:

        percent = 100

        status = (
            "Upload complete"
        )


    return {

        "percent":
            percent,

        "status":
            status,

        "complete":
            percent == 100,

        "uploading":
            state == "uploading",

        "processing":
            state == "processing",
    }


# ==========================================================
# Details
# ==========================================================

def generate_title() -> str:

    return (
        fake.sentence(
            nb_words=random.randint(
                4,
                10,
            )
        )
        .rstrip(".")
    )


def generate_description() -> str:

    paragraph_count = random.randint(
        1,
        3,
    )

    return "\n\n".join(

        fake.paragraph(
            nb_sentences=random.randint(
                2,
                4,
            )
        )

        for _ in range(
            paragraph_count
        )
    )


def generate_details() -> dict[str, Any]:

    return {

        "title":
            generate_title(),

        "description":
            generate_description(),

        "title_limit":
            100,

        "description_limit":
            5000,
    }


# ==========================================================
# Thumbnail Options
# ==========================================================

def generate_thumbnail_options() -> list[dict[str, Any]]:

    count = random.randint(
        3,
        4,
    )

    selected_index = random.randint(
        0,
        count - 1,
    )


    thumbnails = []

    for index in range(
        count
    ):

        thumbnails.append(
            {
                "id":
                    f"thumbnail_{index}",

                "image":
                    get_random_thumbnail(),

                "selected":
                    index
                    == selected_index,
            }
        )

    return thumbnails


# ==========================================================
# Audience
# ==========================================================

def generate_audience() -> dict[str, Any]:

    made_for_kids = (
        random.random()
        < 0.20
    )

    return {

        "made_for_kids":
            made_for_kids,

        "options": [
            {
                "label":
                    "Yes, it's made for kids",

                "value":
                    "yes",

                "selected":
                    made_for_kids,
            },
            {
                "label":
                    "No, it's not made for kids",

                "value":
                    "no",

                "selected":
                    not made_for_kids,
            },
        ],
    }


# ==========================================================
# Visibility
# ==========================================================

def generate_visibility() -> dict[str, Any]:

    selected = random.choice(
        [
            "private",
            "unlisted",
            "public",
        ]
    )

    return {

        "selected":
            selected,

        "options": [
            {
                "label":
                    "Private",

                "value":
                    "private",

                "description":
                    (
                        "Only you and people you "
                        "choose can watch"
                    ),

                "icon":
                    "lock",

                "selected":
                    selected
                    == "private",
            },
            {
                "label":
                    "Unlisted",

                "value":
                    "unlisted",

                "description":
                    (
                        "Anyone with the link can watch"
                    ),

                "icon":
                    "link",

                "selected":
                    selected
                    == "unlisted",
            },
            {
                "label":
                    "Public",

                "value":
                    "public",

                "description":
                    (
                        "Everyone can watch this video"
                    ),

                "icon":
                    "public",

                "selected":
                    selected
                    == "public",
            },
        ],
    }


# ==========================================================
# Playlist
# ==========================================================

def generate_playlist() -> dict[str, Any]:

    enabled = (
        random.random()
        < 0.55
    )

    playlists = [
        "Uploads",
        "Tutorials",
        "Travel",
        "Favorites",
        "Tech Videos",
    ]

    selected = (
        random.choice(
            playlists
        )
        if enabled
        else None
    )

    return {

        "enabled":
            enabled,

        "selected":
            selected,

        "options":
            playlists,
    }


# ==========================================================
# Tags
# ==========================================================

def generate_tags() -> list[str]:

    possible_tags = [
        "youtube",
        "tutorial",
        "technology",
        "travel",
        "vlog",
        "education",
        "programming",
        "review",
        "tips",
        "guide",
        "video",
        "daily",
    ]

    return random.sample(
        possible_tags,
        k=random.randint(
            2,
            6,
        ),
    )


# ==========================================================
# Upload Steps
# ==========================================================

def generate_steps(
    state: str,
) -> list[dict[str, Any]]:

    steps = [
        {
            "id":
                "details",

            "label":
                "Details",
        },
        {
            "id":
                "video_elements",

            "label":
                "Video elements",
        },
        {
            "id":
                "checks",

            "label":
                "Checks",
        },
        {
            "id":
                "visibility",

            "label":
                "Visibility",
        },
    ]


    if state in {
        "select_file",
        "uploading",
    }:

        active_index = 0


    elif state in {
        "details",
        "processing",
    }:

        active_index = 0


    else:

        active_index = 3


    for index, step in enumerate(
        steps
    ):

        step["active"] = (
            index
            == active_index
        )

        step["completed"] = (
            index
            < active_index
        )

    return steps


# ==========================================================
# Checks
# ==========================================================

def generate_checks(
    state: str,
) -> dict[str, Any]:

    if state in {
        "select_file",
        "uploading",
    }:

        status = (
            "not_started"
        )

    elif state == "processing":

        status = (
            "checking"
        )

    else:

        status = random.choice(
            [
                "complete",
                "complete",
                "warning",
            ]
        )


    return {

        "status":
            status,

        "copyright":
            (
                "No issues found"
                if status == "complete"
                else
                (
                    "Checking..."
                    if status == "checking"
                    else
                    "Possible copyrighted content"
                )
            ),

        "ad_suitability":
            (
                "No issues found"
                if status == "complete"
                else
                (
                    "Checking..."
                    if status == "checking"
                    else
                    "Review recommended"
                )
            ),
    }


# ==========================================================
# Upload Area
# ==========================================================

def generate_upload_area() -> dict[str, Any]:

    return {

        "title":
            "Upload videos",

        "instruction":
            (
                "Drag and drop video files to upload"
            ),

        "privacy_note":
            (
                "Your videos will be private "
                "until you publish them."
            ),

        "select_button_label":
            "Select files",
    }


# ==========================================================
# Top Bar
# ==========================================================

def generate_top_bar(
    state: str,
) -> dict[str, Any]:

    return {

        "title":
            "Upload video",

        "show_close":
            True,

        "show_help":
            random.random()
            < 0.60,

        "show_feedback":
            random.random()
            < 0.40,

        "save_label":
            (
                "Save"
                if state
                != "ready_to_publish"
                else "Publish"
            ),
    }


# ==========================================================
# Main Upload Page
# ==========================================================

def generate_upload_page(
    state: str | None = None,
) -> dict[str, Any]:

    if state is None:

        state = random.choice(
            UPLOAD_STATES
        )


    if state not in UPLOAD_STATES:

        raise ValueError(
            f"Unknown upload state: {state}. "
            f"Expected one of: {UPLOAD_STATES}"
        )


    file_data = (
        generate_video_file()
    )


    return {

        "page_type":
            "upload",

        "state":
            state,

        "top_bar":
            generate_top_bar(
                state
            ),

        "upload_area":
            generate_upload_area(),

        "file":
            file_data,

        "progress":
            generate_upload_progress(
                state
            ),

        "details":
            generate_details(),

        "thumbnail_options":
            generate_thumbnail_options(),

        "audience":
            generate_audience(),

        "visibility":
            generate_visibility(),

        "playlist":
            generate_playlist(),

        "tags":
            generate_tags(),

        "steps":
            generate_steps(
                state
            ),

        "checks":
            generate_checks(
                state
            ),

        "preview": {

            "image":
                get_random_thumbnail(),

            "duration":
                file_data[
                    "duration_text"
                ],

            "resolution":
                file_data[
                    "resolution"
                ],
        },

        "layout": {

            "show_upload_area":
                state
                == "select_file",

            "show_details":
                state
                in {
                    "uploading",
                    "details",
                    "processing",
                    "ready_to_publish",
                },

            "show_progress":
                state
                in {
                    "uploading",
                    "processing",
                },

            "show_steps":
                state
                != "select_file",

            "show_preview":
                state
                != "select_file",

            "show_checks":
                state
                in {
                    "processing",
                    "ready_to_publish",
                },

            "show_visibility":
                state
                == "ready_to_publish",
        },
    }


# ==========================================================
# Wrapper
# ==========================================================

def generate_upload_video_page(
    state: str | None = None,
) -> dict[str, Any]:

    return (
        generate_upload_page(
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
        "YOUTUBE UPLOAD VIDEO"
    )

    print(
        "=========================================="
    )


    for state in UPLOAD_STATES:

        page = (
            generate_upload_video_page(
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
            "File:",
            page["file"]["filename"]
        )

        print(
            "Size:",
            page["file"]["size_text"]
        )

        print(
            "Duration:",
            page["file"]["duration_text"]
        )

        print(
            "Upload:",
            page["progress"]["status"]
        )

        print(
            "Visibility:",
            page["visibility"]["selected"]
        )

        print(
            "Made for kids:",
            page["audience"]["made_for_kids"]
        )