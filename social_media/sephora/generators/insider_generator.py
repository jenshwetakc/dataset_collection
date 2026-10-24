from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)

fake = Faker()

INSIDER_STATES = [
    "overview",
    "history",
    "history_filter_open",
    "benefits",
    "redeem_dialog",
    "insufficient_points",
    "reward_added",
    "signed_out",
]


def generate_insider_data(
    sample_index: int = 0,
    media_dir: Path | None = None,
) -> dict:
    directory = (
        Path(media_dir)
        if media_dir is not None
        else ASSETS_ROOT
    )

    rewards = [
        {
            "id": f"reward-{index}",
            "brand": fake.company(),
            "name": name,
            "points": cost,
            "image": get_random_image(directory),
        }
        for index, (name, cost) in enumerate([
            ("Mini Hydrating Cream", 100),
            ("Travel Cleansing Gel", 100),
            ("Beauty Discovery Set", 250),
            ("Skincare Routine Set", 500),
        ])
    ]

    activity = [
        {
            "date": "Oct 02",
            "title": "Online purchase",
            "detail": fake.numerify("Order DEMO-######"),
            "points": 85,
        },
        {
            "date": "Sep 24",
            "title": "Reward redemption",
            "detail": "Mini beauty reward",
            "points": -100,
        },
        {
            "date": "Sep 18",
            "title": "Store purchase",
            "detail": f"{fake.city()} Beauty Center",
            "points": 60,
        },
        {
            "date": "Sep 10",
            "title": "Bonus points",
            "detail": "Synthetic promotional activity",
            "points": 50,
        },
    ]

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "name": fake.first_name(),
        "points": random.randint(600, 1400),
        "tier": random.choice(["Insider", "VIB", "Rouge"]),
        "rewards": rewards,
        "selected_reward": deepcopy(rewards[2]),
        "activity": activity,
        "filters": [
            "All Activity",
            "Points Earned",
            "Points Redeemed",
        ],
        "selected_filter": "All Activity",
        "benefits": [
            {
                "title": "Rewards Bazaar",
                "description": "Explore rewards available for points.",
                "icon": "redeem",
            },
            {
                "title": "Birthday Gifts",
                "description": "Check your account for birthday gift options.",
                "icon": "cake",
            },
            {
                "title": "Member Offers",
                "description": "Discover offers available to your membership.",
                "icon": "local_offer",
            },
        ],
    }


def apply_insider_state(base_data: dict, state: str) -> dict:
    if state not in INSIDER_STATES:
        raise ValueError(f"Unknown insider state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "redeem_dialog",
        "insufficient_points",
    }

    if state == "insufficient_points":
        data["points"] = 50

    elif state == "reward_added":
        data["points"] -= data["selected_reward"]["points"]

    return data