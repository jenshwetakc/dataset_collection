from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_game_cover,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

DOWNLOAD_STATES = [
    "Downloading",
    "Updating",
    "Installing",
    "Patching",
]


QUEUE_STATES = [
    "Queued",
    "Scheduled",
    "Waiting",
]


COMPLETED_STATES = [
    "Completed",
    "Installed",
    "Updated",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_game_title() -> str:

    templates = [
        lambda: f"{fake.word().title()} Frontier",
        lambda: f"{fake.word().title()} Protocol",
        lambda: f"Project {fake.word().title()}",
        lambda: f"{fake.word().title()} Chronicles",
        lambda: f"{fake.word().title()} Arena",
        lambda: f"The {fake.word().title()} Realm",
        lambda: f"{fake.word().title()} Odyssey",
    ]

    return random.choice(
        templates
    )()


def generate_size_gb(
    minimum: float = 1.0,
    maximum: float = 120.0,
) -> float:

    return round(
        random.uniform(
            minimum,
            maximum,
        ),
        1,
    )


# ==========================================================
# Active Download
# ==========================================================

def generate_active_download() -> dict:

    total_size = generate_size_gb(
        8.0,
        140.0,
    )

    progress = random.randint(
        8,
        94,
    )

    downloaded = round(
        total_size
        * (
            progress / 100
        ),
        1,
    )

    disk_total = round(
        total_size
        * random.uniform(
            1.0,
            1.4,
        ),
        1,
    )

    disk_progress = random.randint(
        max(
            1,
            progress - 20,
        ),
        min(
            100,
            progress + 12,
        ),
    )

    return {

        "title":
            generate_game_title(),

        "cover":
            get_random_game_cover(),

        "state":
            random.choice(
                DOWNLOAD_STATES
            ),

        "progress":
            progress,

        "downloaded":
            downloaded,

        "total_size":
            total_size,

        "download_speed":
            round(
                random.uniform(
                    2.0,
                    85.0,
                ),
                1,
            ),

        "peak_speed":
            round(
                random.uniform(
                    40.0,
                    120.0,
                ),
                1,
            ),

        "disk_usage":
            round(
                random.uniform(
                    10.0,
                    300.0,
                ),
                1,
            ),

        "disk_total":
            disk_total,

        "disk_progress":
            disk_progress,

        "time_remaining":
            random.choice([
                "3 minutes",
                "8 minutes",
                "12 minutes",
                "24 minutes",
                "42 minutes",
                "1 hour",
            ]),

        "paused":
            random.random() < 0.18,
    }


# ==========================================================
# Queued Game
# ==========================================================

def generate_queue_item() -> dict:

    total_size = generate_size_gb(
        3.0,
        100.0,
    )

    return {

        "title":
            generate_game_title(),

        "cover":
            get_random_game_cover(),

        "state":
            random.choice(
                QUEUE_STATES
            ),

        "total_size":
            total_size,

        "scheduled":
            random.choice([
                "Next",
                "Today",
                "Tonight",
                "Tomorrow",
                "After current download",
            ]),
    }


# ==========================================================
# Completed Item
# ==========================================================

def generate_completed_item() -> dict:

    return {

        "title":
            generate_game_title(),

        "cover":
            get_random_game_cover(),

        "state":
            random.choice(
                COMPLETED_STATES
            ),

        "size":
            generate_size_gb(
                1.0,
                110.0,
            ),

        "completed_at":
            random.choice([
                "Just now",
                "12 minutes ago",
                "1 hour ago",
                "Yesterday",
                "2 days ago",
            ]),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_downloads_data() -> dict:

    active_downloads = [
        generate_active_download()
        for _ in range(
            random.randint(
                1,
                3,
            )
        )
    ]

    queue = [
        generate_queue_item()
        for _ in range(
            random.randint(
                3,
                7,
            )
        )
    ]

    completed = [
        generate_completed_item()
        for _ in range(
            random.randint(
                3,
                6,
            )
        )
    ]

    return {

        "title":
            "Downloads",

        "subtitle":
            random.choice([
                "Manage downloads and updates",
                "Download queue",
                "Network and disk activity",
            ]),

        "active_downloads":
            active_downloads,

        "queue":
            queue,

        "completed":
            completed,

        "network": {

            "current":
                round(
                    random.uniform(
                        4,
                        100,
                    ),
                    1,
                ),

            "peak":
                round(
                    random.uniform(
                        60,
                        150,
                    ),
                    1,
                ),

            "limit_enabled":
                random.random()
                < 0.35,
        },

        "storage": {

            "used":
                random.randint(
                    250,
                    850,
                ),

            "total":
                random.choice([
                    512,
                    1000,
                    2000,
                ]),
        },
    }