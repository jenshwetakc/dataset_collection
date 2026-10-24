from __future__ import annotations

import random
from datetime import timedelta

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


fake = Faker()

PHOTO_STATES = [
    "photos_grid",
    "search_results",
    "album_open",
    "photo_viewer",
    "selection_mode",
    "create_album_dialog",
    "share_sheet",
    "delete_dialog",
    "memories_carousel",
]

ACCENTS = [
    "#1A73E8",
    "#9334E6",
    "#E8710A",
    "#188038",
    "#C5221F",
]


def make_photo(index: int) -> dict:
    date = fake.date_between(
        start_date="-2y",
        end_date="today",
    )

    return {
        "id": f"photo_{index}",
        "src": get_random_image(ASSETS_ROOT),
        "title": fake.sentence(
            nb_words=random.randint(2, 5),
        ).rstrip("."),
        "date": date.strftime("%B %d, %Y"),
        "location": fake.city(),
        "selected": random.random() < 0.28,
    }


def make_album(
    index: int,
    photos: list[dict],
) -> dict:
    title = fake.word().title()

    return {
        "id": f"album_{index}",
        "title": f"{title} memories",
        "count": random.randint(8, 64),
        "cover_src": random.choice(photos)["src"],
        "shared": random.random() < 0.45,
    }

def get_initials(
    name: str,
) -> str:
    return "".join(
        part[0].upper()
        for part in name.split()[:2]
        if part
    )

def generate_photos_data() -> dict:
    photos = [
        make_photo(index)
        for index in range(
            random.randint(18, 32),
        )
    ]

    albums = [
        make_album(index, photos)
        for index in range(
            random.randint(4, 7),
        )
    ]

    selected_photo = random.choice(photos)
    selected_photos = [
        photo
        for photo in photos
        if photo["selected"]
    ]

    if not selected_photos:
        selected_photos = photos[:2]

    state = random.choice(PHOTO_STATES)
    query = random.choice(
        [
            "Seoul",
            "food",
            "beach",
            "family",
            "birthday",
            "mountains",
        ]
    )

    return {
        "app_name": "Google Photos",
        "state": state,
        "search": {
            "visible": state == "search_results",
            "query": query,
        },
        "photos": photos,
        "albums": albums,
        "selected_photo": selected_photo,
        "selected_photos": selected_photos,
        "selected_album": random.choice(albums),
        "album_name": f"{fake.word().title()} collection",
        "memories": random.sample(
            photos,
            k=min(5, len(photos)),
        ),
        "share_people": [
            {
                "name": person_name,
                "initials": get_initials(person_name),
                "color": random.choice(ACCENTS),
            }
            for person_name in [
                fake.name()
                for _ in range(
                    random.randint(2, 4),
                )
            ]
        ],
        "storage_text": (
            f"{random.randint(2, 12)} GB of "
            f"{random.choice([15, 100, 200])} GB used"
        ),
    }