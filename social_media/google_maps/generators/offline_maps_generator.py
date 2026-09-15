from __future__ import annotations

import random

from faker import Faker

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_parks,
    generate_roads,
    generate_water,
)


fake = Faker()


# ==========================================================
# Download States
# ==========================================================

DOWNLOAD_STATES = [
    "downloaded",
    "downloading",
    "update_available",
]


# ==========================================================
# Offline Area
# ==========================================================

def generate_offline_area(
    index: int,
) -> dict:

    state = random.choices(
        DOWNLOAD_STATES,
        weights=[
            55,
            25,
            20,
        ],
        k=1,
    )[0]

    progress = (
        random.randint(
            15,
            92,
        )
        if state == "downloading"
        else 100
    )

    return {
        "id":
            index,

        "name":
            random.choice(
                [
                    fake.city(),
                    "Downtown",
                    "City Center",
                    "Home area",
                    "Weekend trip",
                    "Travel area",
                ]
            ),

        "state":
            state,

        "progress":
            progress,

        "size":
            f"{random.randint(45, 850)} MB",

        "updated":
            random.choice(
                [
                    "Updated today",
                    "Updated yesterday",
                    "Updated 4 days ago",
                    "Updated last week",
                ]
            ),

        "expires":
            random.choice(
                [
                    "Expires in 12 days",
                    "Expires in 28 days",
                    "Expires in 56 days",
                    "Automatically updates",
                ]
            ),
    }


# ==========================================================
# Selection Area
# ==========================================================

def generate_selection_area() -> dict:

    width = random.randint(
        38,
        58,
    )

    height = random.randint(
        32,
        52,
    )

    left = random.randint(
        18,
        max(
            19,
            82 - width,
        ),
    )

    top = random.randint(
        18,
        max(
            19,
            78 - height,
        ),
    )

    return {
        "left":
            left,

        "top":
            top,

        "width":
            width,

        "height":
            height,

        "size":
            f"{random.randint(90, 620)} MB",
    }


# ==========================================================
# Storage
# ==========================================================

def generate_storage() -> dict:

    total_gb = random.choice(
        [
            32,
            64,
            128,
            256,
        ]
    )

    used_gb = round(
        random.uniform(
            total_gb * 0.25,
            total_gb * 0.85,
        ),
        1,
    )

    offline_mb = random.randint(
        350,
        5400,
    )

    return {
        "total":
            f"{total_gb} GB",

        "used":
            f"{used_gb} GB",

        "offline":
            (
                f"{offline_mb / 1024:.1f} GB"
                if offline_mb >= 1024
                else f"{offline_mb} MB"
            ),

        "percent":
            int(
                (
                    used_gb
                    / total_gb
                )
                * 100
            ),
    }


# ==========================================================
# Main Data
# ==========================================================

def generate_offline_maps_data() -> dict:

    areas = [
        generate_offline_area(
            index
        )
        for index
        in range(
            random.randint(
                3,
                6,
            )
        )
    ]

    return {
        "selection":
            generate_selection_area(),

        "storage":
            generate_storage(),

        "offline_areas":
            areas,

        "wifi_only":
            random.random()
            < 0.72,

        "auto_update":
            random.random()
            < 0.80,

        "map": {
            "roads":
                generate_roads(
                    count=random.randint(
                        20,
                        32,
                    )
                ),

            "buildings":
                generate_buildings(
                    count=random.randint(
                        32,
                        55,
                    )
                ),

            "parks":
                generate_parks(),

            "water":
                generate_water(),

            "labels":
                generate_map_labels(
                    count=random.randint(
                        9,
                        15,
                    )
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_offline_maps_data()
    )

    print(
        "Offline areas:",
        len(
            data["offline_areas"]
        ),
    )

    print(
        "Selection:",
        data["selection"],
    )

    print(
        "Storage:",
        data["storage"],
    )