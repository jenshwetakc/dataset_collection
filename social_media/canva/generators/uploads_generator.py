from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_design_thumbnail,
    get_random_photo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

MEDIA_STATES = [
    "library",
    "uploading",
    "selected_media",
    "empty",
]


# ==========================================================
# Tabs
# ==========================================================

MEDIA_TABS = [
    {
        "label": "Images",
        "icon": "image",
        "value": "images",
    },
    {
        "label": "Videos",
        "icon": "movie",
        "value": "videos",
    },
    {
        "label": "Audio",
        "icon": "music_note",
        "value": "audio",
    },
]


# ==========================================================
# File Types
# ==========================================================

IMAGE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "webp",
]

VIDEO_EXTENSIONS = [
    "mp4",
    "mov",
]

AUDIO_EXTENSIONS = [
    "mp3",
    "wav",
]


# ==========================================================
# Media Item
# ==========================================================

def generate_media_item(
    index: int,
    media_type: str = "image",
) -> dict:

    if media_type == "image":

        extension = random.choice(
            IMAGE_EXTENSIONS
        )

        image = (
            get_random_photo()
            or get_random_design_thumbnail()
        )

        duration = None

    elif media_type == "video":

        extension = random.choice(
            VIDEO_EXTENSIONS
        )

        image = (
            get_random_design_thumbnail()
            or get_random_photo()
        )

        duration = random.choice(
            [
                "0:08",
                "0:12",
                "0:24",
                "0:35",
                "1:02",
            ]
        )

    else:

        extension = random.choice(
            AUDIO_EXTENSIONS
        )

        image = None

        duration = random.choice(
            [
                "0:18",
                "0:34",
                "1:12",
                "2:05",
                "3:42",
            ]
        )

    return {
        "id":
            index,

        "name":
            f"{fake.word()}_{index + 1}.{extension}",

        "type":
            media_type,

        "image":
            image,

        "duration":
            duration,

        "size":
            random.choice(
                [
                    "248 KB",
                    "618 KB",
                    "1.2 MB",
                    "2.4 MB",
                    "5.8 MB",
                    "12 MB",
                ]
            ),

        "favorite":
            random.random()
            < 0.15,

        "used":
            random.random()
            < 0.30,

        "selected":
            False,
    }


# ==========================================================
# Media Library
# ==========================================================

def generate_media_library(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            10,
            20,
        )

    items = []

    for index in range(
        count
    ):

        media_type = random.choices(
            [
                "image",
                "video",
                "audio",
            ],
            weights=[
                0.68,
                0.22,
                0.10,
            ],
        )[0]

        items.append(
            generate_media_item(
                index=index,
                media_type=media_type,
            )
        )

    return items


# ==========================================================
# Upload Tasks
# ==========================================================

def generate_upload_tasks() -> list[dict]:

    count = random.randint(
        2,
        5,
    )

    tasks = []

    for index in range(
        count
    ):

        media_type = random.choice(
            [
                "image",
                "video",
            ]
        )

        item = generate_media_item(
            index=index,
            media_type=media_type,
        )

        progress = random.randint(
            8,
            94,
        )

        tasks.append(
            {
                **item,

                "progress":
                    progress,

                "status":
                    (
                        "Processing"
                        if progress >= 90
                        else "Uploading"
                    ),
            }
        )

    return tasks


# ==========================================================
# Folders
# ==========================================================

def generate_folders() -> list[dict]:

    names = random.sample(
        [
            "Campaign",
            "Brand",
            "Photography",
            "Products",
            "Social",
            "Archive",
        ],
        random.randint(
            3,
            5,
        ),
    )

    return [
        {
            "name":
                name,

            "count":
                random.randint(
                    2,
                    42,
                ),
        }
        for name in names
    ]


# ==========================================================
# Main
# ==========================================================

def generate_uploads_data(
    forced_state: str | None = None,
) -> dict:

    if forced_state is not None:

        if forced_state not in MEDIA_STATES:

            raise ValueError(
                f"Unknown uploads state: "
                f"{forced_state}"
            )

        state = forced_state

    else:

        state = random.choice(
            MEDIA_STATES
        )

    active_tab = random.choice(
        MEDIA_TABS
    )

    items = generate_media_library()

    selected_media = None

    if state == "selected_media":

        candidates = [
            item
            for item in items
            if item["type"] != "audio"
        ]

        if candidates:

            selected_media = random.choice(
                candidates
            )

            selected_media[
                "selected"
            ] = True

    user_name = fake.name()

    return {

        "state":
            state,


        "title":
            "Uploads",


        "user": {

            "name":
                user_name,

            "avatar":
                get_random_avatar(),
        },


        "search": {

            "placeholder":
                random.choice(
                    [
                        "Search uploads",
                        "Search your media",
                        "Find uploaded files",
                    ]
                ),
        },


        "tabs": [
            {
                **tab,

                "selected":
                    tab["value"]
                    == active_tab["value"],
            }
            for tab
            in MEDIA_TABS
        ],


        "active_tab":
            active_tab["value"],


        "folders":
            generate_folders(),


        "items":
            items,


        "upload_tasks":
            generate_upload_tasks(),


        "selected_media":
            selected_media,


        "sort":
            random.choice(
                [
                    "Recently added",
                    "Name",
                    "File size",
                ]
            ),


        "view_mode":
            random.choice(
                [
                    "grid",
                    "compact",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_uploads_data()
    )