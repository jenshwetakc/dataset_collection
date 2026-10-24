from __future__ import annotations

import random

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


BOARD_STATES = [
    "board",
    "signed_out_banner",
    "login_dialog",
    "login_password_visible",
]

MODAL_STATES = {
    "login_dialog",
    "login_password_visible",
}

BOARD_TOPICS = [
    {
        "eyebrow": "Eerie accents",
        "title": "Halloween home inspo",
        "description": (
            "Add a touch of frightening charm to your space "
            "with these festive home ideas."
        ),
        "creator": "Home Decor",
        "search_hint": "halloween home decor",
    },
    {
        "eyebrow": "Spaces to unwind",
        "title": "Cozy corners",
        "description": (
            "Discover inviting spaces, soft textures, "
            "and thoughtful details for your home."
        ),
        "creator": "Home Decor",
        "search_hint": "cozy living room ideas",
    },
    {
        "eyebrow": "Fresh inspiration",
        "title": "Creative workspace ideas",
        "description": (
            "Find inspiration for a workspace that makes "
            "room for your best ideas."
        ),
        "creator": "Design",
        "search_hint": "creative home office",
    },
    {
        "eyebrow": "A little everyday magic",
        "title": "Weekend baking ideas",
        "description": (
            "Discover comforting recipes and beautiful "
            "bakes to try this weekend."
        ),
        "creator": "Food",
        "search_hint": "weekend baking recipes",
    },
]


def generate_board_data(
    seed: int | None = None,
    num_pins: int = 60,
) -> dict:
    if num_pins < 1:
        raise ValueError("num_pins must be at least 1.")

    rng = random.Random(seed)

    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    topic = rng.choice(BOARD_TOPICS)

    pins = []

    for index in range(num_pins):
        pins.append(
            {
                "id": index,
                "image": get_random_image(ASSETS_ROOT),
                "aspect_ratio": rng.choice(
                    [
                        "2 / 3",
                        "3 / 4",
                        "4 / 5",
                        "1 / 1",
                        "3 / 5",
                    ]
                ),
                "is_video": rng.random() < 0.15,
                "duration": (
                    f"0:{rng.randint(10, 59):02d}"
                ),
                "alt": (
                    f"{topic['title']} inspiration "
                    f"{index + 1}"
                ),
            }
        )

    return {
        "state": "board",
        "popup_visible": False,

        "board": {
            **topic,
            "pin_count": len(pins),
            "updated": rng.choice(
                ["1w", "2w", "1mo"]
            ),
            "featured": True,
        },

        "pins": pins,

        # Fake credentials are displayed only in the
        # synthetic password-visible screenshot state.
        "login": {
            "email": fake.email(),
            "password": "ExamplePass123!",
        },
    }


def create_board_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in BOARD_STATES:
        raise ValueError(
            f"Unknown Pinterest board state: {state!r}"
        )

    # Templates only read these nested objects.
    # Reuse media instead of generating it again per state.
    return {
        **base_data,
        "state": state,
        "popup_visible": state in MODAL_STATES,
    }