from __future__ import annotations

import random

from system.windows.generators.media_generator import (
    get_random_photo,
)


# ==========================================================
# States
# ==========================================================

PHOTOS_STATES = [
    "gallery",
    "album",
    "photo_viewer",
    "photo_selected",
    "multi_select",
    "search",
    "favorites",
    "imports",
    "slideshow",
    "edit",
    "delete_dialog",
    "empty",
]


# ==========================================================
# Navigation
# ==========================================================

PHOTOS_NAVIGATION = [
    {
        "id": "gallery",
        "label": "Gallery",
        "icon": "photo_library",
    },
    {
        "id": "albums",
        "label": "Albums",
        "icon": "collections",
    },
    {
        "id": "favorites",
        "label": "Favorites",
        "icon": "favorite",
    },
    {
        "id": "imports",
        "label": "Imports",
        "icon": "download",
    },
]


# ==========================================================
# Photo Metadata
# ==========================================================

PHOTO_NAMES = [
    "IMG_2048.jpg",
    "Seoul_Street.jpg",
    "Campus.jpg",
    "Sunset.jpg",
    "Conference.jpg",
    "Research_Lab.jpg",
    "City_Night.jpg",
    "Coffee.jpg",
    "Library.jpg",
    "Mountains.jpg",
    "River.jpg",
    "Architecture.jpg",
]


ALBUM_POOL = [
    {
        "name": "Recent",
        "icon": "history",
    },
    {
        "name": "Travel",
        "icon": "flight",
    },
    {
        "name": "Campus",
        "icon": "school",
    },
    {
        "name": "Screenshots",
        "icon": "screenshot",
    },
    {
        "name": "Favorites",
        "icon": "favorite",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_photo(
    index: int,
) -> dict:

    image = get_random_photo()

    width = random.choice(
        [
            1920,
            2560,
            4032,
            4608,
        ]
    )

    height = random.choice(
        [
            1080,
            1440,
            3024,
            3456,
        ]
    )

    return {
        "id":
            f"photo_{index}",

        "name":
            random.choice(
                PHOTO_NAMES
            ),

        "src":
            image,

        "date":
            random.choice(
                [
                    "Today",
                    "Yesterday",
                    "September 4",
                    "September 3",
                    "August 29",
                    "August 22",
                ]
            ),

        "time":
            random.choice(
                [
                    "10:18 AM",
                    "12:42 PM",
                    "3:15 PM",
                    "5:51 PM",
                    "8:20 PM",
                ]
            ),

        "width":
            width,

        "height":
            height,

        "favorite":
            random.random()
            < 0.25,

        "selected":
            False,

        "imported":
            random.random()
            < 0.25,
    }


def generate_photos(
    minimum: int = 8,
    maximum: int = 18,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    return [
        generate_photo(
            index=i
        )
        for i in range(
            count
        )
    ]


def generate_albums(
    photos: list[dict],
) -> list[dict]:

    albums = []

    for album in ALBUM_POOL:

        album_photos = random.sample(
            photos,
            k=random.randint(
                2,
                min(
                    6,
                    len(photos),
                ),
            ),
        )

        albums.append(
            {
                **album,

                "count":
                    len(
                        album_photos
                    ),

                "cover":
                    (
                        album_photos[0]["src"]
                        if album_photos
                        else None
                    ),

                "photos":
                    album_photos,
            }
        )

    return albums


# ==========================================================
# Main Generator
# ==========================================================

def generate_photos_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            PHOTOS_STATES
        )


    if state not in PHOTOS_STATES:

        raise ValueError(
            f"Unknown Photos state: "
            f"{state}"
        )


    photos = generate_photos()

    albums = generate_albums(
        photos
    )

    selected_photo = None


    # ------------------------------------------------------
    # Single selection
    # ------------------------------------------------------

    if state in {
        "photo_selected",
        "delete_dialog",
    }:

        selected_photo = random.choice(
            photos
        )

        selected_photo[
            "selected"
        ] = True


    # ------------------------------------------------------
    # Viewer / edit / slideshow
    # ------------------------------------------------------

    elif state in {
        "photo_viewer",
        "edit",
        "slideshow",
    }:

        selected_photo = random.choice(
            photos
        )


    # ------------------------------------------------------
    # Multi-select
    # ------------------------------------------------------

    if state == "multi_select":

        selected = random.sample(
            photos,
            k=random.randint(
                2,
                min(
                    5,
                    len(photos),
                ),
            ),
        )

        for photo in selected:

            photo[
                "selected"
            ] = True


    # ------------------------------------------------------
    # Favorites
    # ------------------------------------------------------

    favorites = [
        photo
        for photo in photos
        if photo[
            "favorite"
        ]
    ]

    if not favorites:

        photos[0][
            "favorite"
        ] = True

        favorites = [
            photos[0]
        ]


    # ------------------------------------------------------
    # Imports
    # ------------------------------------------------------

    imports = [
        photo
        for photo in photos
        if photo[
            "imported"
        ]
    ]

    if not imports:

        photos[0][
            "imported"
        ] = True

        imports = [
            photos[0]
        ]


    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    search_query = (
        random.choice(
            [
                "Seoul",
                "Campus",
                "Sunset",
                "Research",
                "IMG",
            ]
        )
        if state
        == "search"
        else ""
    )


    search_results = (
        random.sample(
            photos,
            k=random.randint(
                2,
                min(
                    6,
                    len(photos),
                ),
            ),
        )
        if state
        == "search"
        else []
    )


    return {
        "state":
            state,

        "navigation":
            PHOTOS_NAVIGATION,

        "photos":
            (
                []
                if state
                == "empty"
                else photos
            ),

        "albums":
            albums,

        "selected_photo":
            selected_photo,

        "favorites":
            favorites,

        "imports":
            imports,

        "search_query":
            search_query,

        "search_results":
            search_results,

        "selected_count":
            sum(
                1
                for photo in photos
                if photo[
                    "selected"
                ]
            ),

        "edit": {
            "brightness":
                random.randint(
                    20,
                    90,
                ),

            "contrast":
                random.randint(
                    20,
                    90,
                ),

            "saturation":
                random.randint(
                    20,
                    90,
                ),

            "rotation":
                random.choice(
                    [
                        0,
                        90,
                        180,
                        270,
                    ]
                ),
        },
    }