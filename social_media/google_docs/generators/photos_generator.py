from __future__ import annotations

import random

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


fake = Faker()


PHOTOS_STATES = [
    "photos_grid",
    "search_results",
    "album_open",
    "photo_viewer",
    "selection_mode",
    "sharing_dialog",
    "create_album_dialog",
    "trash",
]


ALBUM_TYPES = [
    "Weekend moments",
    "Family",
    "Travel",
    "Favorites",
    "Screenshots",
    "Food ideas",
    "Work events",
    "Nature",
]


FALLBACK_BACKGROUNDS = [
    "linear-gradient(135deg, #b7d5ff, #e7f0ff)",
    "linear-gradient(135deg, #ffd6c2, #fff2db)",
    "linear-gradient(135deg, #c8ecd1, #ecfff0)",
    "linear-gradient(135deg, #e0d3ff, #f4efff)",
    "linear-gradient(135deg, #ffe0a8, #fff9e8)",
]


def generate_photo(
    index: int,
) -> dict:

    return {
        "id":
            f"photo_{index:03d}",

        "src":
            get_random_image(
                ASSETS_ROOT
            ),

        "fallback":
            random.choice(
                FALLBACK_BACKGROUNDS
            ),

        "title":
            fake.sentence(
                nb_words=random.randint(2, 5),
            ).rstrip("."),

        "date":
            fake.date_between(
                start_date="-2y",
                end_date="today",
            ).strftime(
                "%B %-d, %Y"
            ),

        "favorite":
            random.random() < 0.25,

        "selected":
            False,
    }


def generate_album(
    index: int,
    photos: list[dict],
) -> dict:

    cover = random.choice(
        photos
    )

    return {
        "id":
            f"album_{index:03d}",

        "name":
            random.choice(
                ALBUM_TYPES
            ),

        "count":
            random.randint(4, 42),

        "cover":
            cover,

        "shared":
            random.random() < 0.35,
    }


def generate_photos_page(
    state: str | None = None,
) -> dict:

    state = (
        state
        or random.choice(
            PHOTOS_STATES
        )
    )

    photos = [
        generate_photo(index)
        for index in range(
            random.randint(18, 34)
        )
    ]

    selected_photo = random.choice(
        photos
    )

    if state == "selection_mode":

        selected_count = random.randint(
            2,
            min(6, len(photos)),
        )

        for photo in random.sample(
            photos,
            k=selected_count,
        ):

            photo["selected"] = True

    albums = [
        generate_album(
            index=index,
            photos=photos,
        )
        for index in range(6)
    ]

    selected_album = random.choice(
        albums
    )

    search_query = random.choice(
        [
            fake.word(),
            "beach",
            "food",
            "family",
            "travel",
            "2026",
        ]
    )

    return {
        "app_name":
            "Google Photos",

        "state":
            state,

        "search_query":
            search_query,

        "photos":
            photos,

        "albums":
            albums,

        "selected_photo":
            selected_photo,

        "selected_album":
            selected_album,

        "selection_count":
            sum(
                photo["selected"]
                for photo in photos
            ),

        "share":
            {
                "name":
                    fake.name(),

                "email":
                    fake.email(),

                "general_access":
                    random.choice(
                        [
                            "Restricted",
                            "Anyone with the link",
                        ]
                    ),
            },
    }