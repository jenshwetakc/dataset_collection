from __future__ import annotations

import random

from faker import Faker

from social_media.kindle.generators.media_generator import (
    get_random_book_cover,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

AUDIOBOOK_STATES = [
    "player",
    "playing",
    "paused",
    "chapter_list",
    "queue",
    "speed_sheet",
    "sleep_timer",
    "bookmark_dialog",
    "playback_error",
]


# ==========================================================
# Titles
# ==========================================================

BOOK_TITLES = [
    "The Silent Horizon",
    "Fragments of Memory",
    "Beyond the Last City",
    "Understanding Tomorrow",
    "The Hidden Machine",
    "The Art of Thinking",
    "Notes from the River",
]


# ==========================================================
# Chapter Generator
# ==========================================================

def generate_chapter(
    index: int,
) -> dict:

    duration_minutes = random.randint(
        8,
        45,
    )

    return {
        "id":
            f"chapter_{index:03d}",

        "number":
            index + 1,

        "title":
            random.choice(
                [
                    f"Chapter {index + 1}",
                    "A New Beginning",
                    "Into the Unknown",
                    "Changing Directions",
                    "The Long Road",
                    "Reflections",
                    "A Different View",
                ]
            ),

        "duration_minutes":
            duration_minutes,

        "downloaded":
            random.random()
            < 0.7,

        "played":
            random.random()
            < 0.25,
    }


# ==========================================================
# Queue Item
# ==========================================================

def generate_queue_item(
    index: int,
) -> dict:

    return {
        "id":
            f"queue_{index:03d}",

        "title":
            random.choice(
                BOOK_TITLES
            ),

        "author":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "duration":
            random.randint(
                180,
                900,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_audiobook_page() -> dict:

    state = random.choice(
        AUDIOBOOK_STATES
    )

    chapter_count = random.randint(
        8,
        18,
    )

    chapters = [
        generate_chapter(
            index
        )
        for index in range(
            chapter_count
        )
    ]

    current_chapter_index = random.randint(
        0,
        chapter_count - 1,
    )

    current_chapter = chapters[
        current_chapter_index
    ]

    duration_seconds = (
        current_chapter[
            "duration_minutes"
        ]
        * 60
    )

    elapsed_seconds = random.randint(
        30,
        max(
            31,
            duration_seconds - 30,
        ),
    )

    progress = round(
        (
            elapsed_seconds
            / duration_seconds
        )
        * 100
    )


    # ======================================================
    # Playback
    # ======================================================

    playing = state in {
        "playing",
        "player",
        "chapter_list",
        "queue",
        "speed_sheet",
        "sleep_timer",
        "bookmark_dialog",
    }

    if state == "paused":

        playing = False


    # ======================================================
    # Popup States
    # ======================================================

    show_speed_sheet = (
        state
        == "speed_sheet"
    )

    show_sleep_timer = (
        state
        == "sleep_timer"
    )

    show_bookmark_dialog = (
        state
        == "bookmark_dialog"
    )

    show_error = (
        state
        == "playback_error"
    )

    popup_open = any(
        [
            show_speed_sheet,
            show_sleep_timer,
            show_bookmark_dialog,
            show_error,
        ]
    )


    # ======================================================
    # Secondary Views
    # ======================================================

    show_chapters = (
        state
        == "chapter_list"
    )

    show_queue = (
        state
        == "queue"
    )


    # ======================================================
    # Queue
    # ======================================================

    queue = [
        generate_queue_item(
            index
        )
        for index in range(
            random.randint(
                4,
                8,
            )
        )
    ]


    # ======================================================
    # Speed
    # ======================================================

    playback_speed = random.choice(
        [
            0.75,
            1.0,
            1.25,
            1.5,
            1.75,
            2.0,
        ]
    )


    # ======================================================
    # Sleep Timer
    # ======================================================

    sleep_timer = random.choice(
        [
            "Off",
            "15 minutes",
            "30 minutes",
            "45 minutes",
            "End of chapter",
        ]
    )


    return {
        "state":
            state,

        "popup_open":
            popup_open,

        "show_speed_sheet":
            show_speed_sheet,

        "show_sleep_timer":
            show_sleep_timer,

        "show_bookmark_dialog":
            show_bookmark_dialog,

        "show_error":
            show_error,

        "show_chapters":
            show_chapters,

        "show_queue":
            show_queue,

        "playing":
            playing,

        "book_title":
            random.choice(
                BOOK_TITLES
            ),

        "author":
            fake.name(),

        "narrator":
            fake.name(),

        "cover":
            get_random_book_cover(),

        "chapters":
            chapters,

        "current_chapter":
            current_chapter,

        "current_chapter_index":
            current_chapter_index,

        "chapter_count":
            chapter_count,

        "elapsed_seconds":
            elapsed_seconds,

        "duration_seconds":
            duration_seconds,

        "progress":
            progress,

        "playback_speed":
            playback_speed,

        "sleep_timer":
            sleep_timer,

        "queue":
            queue,

        "bookmark_note":
            random.choice(
                [
                    "Important idea",
                    "Come back to this section",
                    "Interesting quote",
                    "Review later",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = generate_audiobook_page()

    print(
        "\n=============================="
    )

    print(
        "KINDLE AUDIOBOOK"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page["state"],
    )

    print(
        "Chapter:",
        page["current_chapter"]["title"],
    )

    print(
        "Progress:",
        page["progress"],
    )

    print(
        "Popup:",
        page["popup_open"],
    )