from __future__ import annotations

import random

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


PIN_DETAILS_STATES = [
    "default",
    "comments_expanded",
    "save_to_board_dialog",
    "share_dialog",
    "report_dialog",
    "image_expanded",
]

POPUP_STATES = {
    "save_to_board_dialog",
    "share_dialog",
    "report_dialog",
    "image_expanded",
}

PIN_TOPICS = [
    "Cozy living room inspiration",
    "Creative workspace ideas",
    "Minimalist bedroom design",
    "Weekend baking inspiration",
    "Beautiful garden corners",
    "Travel photography ideas",
    "Handmade ceramic inspiration",
    "Everyday outfit ideas",
]

BOARD_NAMES = [
    "Dream home",
    "Creative projects",
    "Weekend inspiration",
    "Things to try",
    "My favorite ideas",
]


def generate_initials(name: str) -> str:
    return "".join(
        part[0]
        for part in name.split()[:2]
        if part
    ).upper()


def generate_pin_details_data(
    state: str = "default",
    seed: int | None = None,
) -> dict:
    if state not in PIN_DETAILS_STATES:
        raise ValueError(
            f"Unknown Pinterest Pin Details state: {state!r}"
        )

    rng = random.Random(seed)

    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    creator_name = fake.name()
    viewer_name = fake.name()

    comments = []

    for index in range(8):
        name = fake.name()

        comments.append(
            {
                "id": index,
                "name": name,
                "initials": generate_initials(name),
                "text": rng.choice(
                    [
                        "This is such a lovely idea!",
                        "Saving this for my next project.",
                        "I really like the colors here.",
                        "Where can I find something similar?",
                        "The details make this so beautiful.",
                        "I tried this and loved the result.",
                    ]
                ),
                "likes": rng.randint(0, 85),
                "time": f"{rng.randint(1, 23)}h",
            }
        )

    boards = []

    for index, name in enumerate(BOARD_NAMES):
        boards.append(
            {
                "name": name,
                "count": rng.randint(10, 260),
                "cover": get_random_image(ASSETS_ROOT),
                "secret": index == 3,
            }
        )

    related_pins = []

    for index in range(36):
        author = fake.name()

        related_pins.append(
            {
                "id": index,
                "title": rng.choice(PIN_TOPICS),
                "image": get_random_image(ASSETS_ROOT),
                "aspect_ratio": rng.choice(
                    [
                        "3 / 4",
                        "2 / 3",
                        "1 / 1",
                        "4 / 5",
                    ]
                ),
                "author": author,
                "initials": generate_initials(author),
            }
        )

    return {
        "state": state,
        "popup_visible": state in POPUP_STATES,

        "pin": {
            "title": rng.choice(PIN_TOPICS),
            "description": (
                "Collect fresh ideas for your next project. "
                "Explore thoughtful details, interesting textures, "
                "and simple ways to make the idea your own."
            ),
            "image": get_random_image(ASSETS_ROOT),
            "domain": fake.domain_name(),
            "likes": rng.randint(50, 2400),
            "comment_count": len(comments),
            "saved": rng.choice([True, False]),
        },

        "creator": {
            "name": creator_name,
            "initials": generate_initials(creator_name),
            "followers": f"{rng.randint(2, 95)}k",
        },

        "viewer": {
            "name": viewer_name,
            "initials": generate_initials(viewer_name),
        },

        "comments": comments,
        "boards": boards,
        "related_pins": related_pins,

        "share_url": (
            "https://www.pinterest.com/pin/"
            f"{rng.randint(100000000000, 999999999999)}/"
        ),

        "share_options": [
            {
                "name": "Copy link",
                "icon": "link",
            },
            {
                "name": "Email",
                "icon": "mail",
            },
            {
                "name": "Message",
                "icon": "chat",
            },
            {
                "name": "More",
                "icon": "more_horiz",
            },
        ],

        "report_reasons": [
            "Spam",
            "Misleading information",
            "Inappropriate content",
            "Intellectual property violation",
            "Other",
        ],
    }