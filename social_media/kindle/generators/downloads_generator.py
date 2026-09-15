from __future__ import annotations

import random

from faker import Faker

from social_media.kindle.generators.media_generator import (
    get_random_book_cover,
)


fake = Faker()


DOWNLOAD_STATES = [
    "downloads_home",
    "downloading",
    "paused",
    "offline",
    "failed",
    "multi_select",
    "remove_download",
    "retry_download",
    "sync_conflict",
    "empty_downloads",
]


BOOK_TITLES = [
    "The Silent Horizon",
    "Fragments of Memory",
    "The Hidden Machine",
    "Beyond the Last City",
    "The Future Within",
    "Notes from the River",
    "The Art of Thinking",
    "Echoes of History",
]


def generate_download_item(
    index: int,
) -> dict:

    state = random.choice(
        [
            "downloaded",
            "queued",
            "downloading",
            "paused",
            "failed",
        ]
    )

    progress = 100

    if state == "queued":
        progress = 0

    elif state in {
        "downloading",
        "paused",
        "failed",
    }:
        progress = random.randint(
            8,
            92,
        )

    return {
        "id":
            f"download_{index:03d}",

        "title":
            random.choice(
                BOOK_TITLES
            ),

        "author":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "state":
            state,

        "progress":
            progress,

        "size_mb":
            random.randint(
                5,
                180,
            ),

        "downloaded_mb":
            round(
                random.uniform(
                    1,
                    150,
                ),
                1,
            ),

        "selected":
            False,

        "updated":
            random.choice(
                [
                    "Just now",
                    "5 min ago",
                    "1 hour ago",
                    "Yesterday",
                ]
            ),
    }


def generate_downloads_page() -> dict:

    state = random.choice(
        DOWNLOAD_STATES
    )

    item_count = random.randint(
        6,
        14,
    )

    items = [
        generate_download_item(
            index
        )
        for index in range(
            item_count
        )
    ]


    # ======================================================
    # Force Current State
    # ======================================================

    if state == "downloading" and items:

        items[0][
            "state"
        ] = "downloading"

        items[0][
            "progress"
        ] = random.randint(
            20,
            85,
        )


    if state == "paused" and items:

        items[0][
            "state"
        ] = "paused"

        items[0][
            "progress"
        ] = random.randint(
            20,
            85,
        )


    if state == "failed" and items:

        items[0][
            "state"
        ] = "failed"

        items[0][
            "progress"
        ] = random.randint(
            10,
            70,
        )


    # ======================================================
    # Empty
    # ======================================================

    if state == "empty_downloads":

        items = []


    # ======================================================
    # Multi Select
    # ======================================================

    if state == "multi_select" and items:

        selected_count = random.randint(
            1,
            min(
                4,
                len(
                    items
                ),
            ),
        )

        selected_indices = random.sample(
            range(
                len(
                    items
                )
            ),
            k=selected_count,
        )

        for index in selected_indices:

            items[
                index
            ][
                "selected"
            ] = True


    # ======================================================
    # Popup States
    # ======================================================

    show_remove_dialog = (
        state == "remove_download"
    )

    show_retry_dialog = (
        state == "retry_download"
    )

    show_sync_conflict = (
        state == "sync_conflict"
    )

    popup_open = any(
        [
            show_remove_dialog,
            show_retry_dialog,
            show_sync_conflict,
        ]
    )


    active_item = (
        random.choice(
            items
        )
        if items
        else None
    )


    # ======================================================
    # Storage
    # ======================================================

    total_storage_gb = random.choice(
        [
            8,
            16,
            32,
        ]
    )

    used_storage_gb = round(
        random.uniform(
            1.0,
            total_storage_gb * 0.85,
        ),
        1,
    )

    storage_percentage = round(
        (
            used_storage_gb
            / total_storage_gb
        )
        * 100
    )


    return {
        "state":
            state,

        "items":
            items,

        "active_item":
            active_item,

        "popup_open":
            popup_open,

        "multi_select":
            state == "multi_select",

        "offline":
            state == "offline",

        "show_remove_dialog":
            show_remove_dialog,

        "show_retry_dialog":
            show_retry_dialog,

        "show_sync_conflict":
            show_sync_conflict,

        "wifi_only":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "auto_download":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "sync_enabled":
            random.choice(
                [
                    True,
                    False,
                ]
            ),

        "last_sync":
            random.choice(
                [
                    "Just now",
                    "10 minutes ago",
                    "1 hour ago",
                    "Yesterday",
                ]
            ),

        "used_storage_gb":
            used_storage_gb,

        "total_storage_gb":
            total_storage_gb,

        "storage_percentage":
            storage_percentage,

        "downloaded_count":
            sum(
                1
                for item in items
                if item[
                    "state"
                ] == "downloaded"
            ),
    }


if __name__ == "__main__":

    page = (
        generate_downloads_page()
    )

    print(
        "\n=============================="
    )

    print(
        "KINDLE DOWNLOADS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page[
            "state"
        ]
    )

    print(
        "Items:",
        len(
            page[
                "items"
            ]
        )
    )

    print(
        "Popup:",
        page[
            "popup_open"
        ]
    )