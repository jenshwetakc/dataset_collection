from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

from common.media_generator import (
    get_random_image,
)


fake = Faker()


# ==========================================================
# Paths
# ==========================================================

ANDROID_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

WALLPAPER_DIR = (
    ANDROID_ROOT
    / "assets"
    / "wallpapers"
)

SHARE_IMAGE_DIR = (
    ANDROID_ROOT
    / "assets"
    / "share_images"
)


# ==========================================================
# Share Apps
# ==========================================================

SHARE_APPS = [

    {
        "name": "Messages",
        "icon": "mdi:message-text",
    },

    {
        "name": "Gmail",
        "icon": "mdi:gmail",
    },

    {
        "name": "Drive",
        "icon": "mdi:google-drive",
    },

    {
        "name": "Photos",
        "icon": "mdi:image-multiple-outline",
    },

    {
        "name": "Slack",
        "icon": "mdi:slack",
    },

    {
        "name": "Meet",
        "icon": "mdi:video-outline",
    },

    {
        "name": "Keep Notes",
        "icon": "mdi:lightbulb-outline",
    },

    {
        "name": "Bluetooth",
        "icon": "mdi:bluetooth",
    },

    {
        "name": "Quick Share",
        "icon": "mdi:share-variant-outline",
    },

    {
        "name": "Files",
        "icon": "mdi:folder-outline",
    },

    {
        "name": "Chrome",
        "icon": "mdi:google-chrome",
    },

    {
        "name": "Calendar",
        "icon": "mdi:calendar-outline",
    },
]


# ==========================================================
# Utility Actions
# ==========================================================

UTILITY_ACTIONS = [

    {
        "semantic": "copy_link",
        "name": "Copy link",
        "icon": "mdi:content-copy",
    },

    {
        "semantic": "quick_share",
        "name": "Quick Share",
        "icon": "mdi:share-variant",
    },

    {
        "semantic": "print",
        "name": "Print",
        "icon": "mdi:printer-outline",
    },

    {
        "semantic": "save_to_files",
        "name": "Save to Files",
        "icon": "mdi:folder-download-outline",
    },
]


# ==========================================================
# Asset Helpers
# ==========================================================

def get_random_asset(
    directory: Path,
) -> str | None:

    if not directory.exists():

        return None

    try:

        return get_random_image(
            directory
        )

    except Exception:

        return None


# ==========================================================
# Contact Builder
# ==========================================================

def build_contact(
    index: int,
) -> dict:

    name = fake.first_name()

    app = random.choice([
        "Messages",
        "Gmail",
        "Slack",
    ])

    return {

        "semantic":
            f"share_contact_{index}",

        "name":
            name,

        "app":
            app,

        "initial":
            name[0].upper(),

        "work_profile":
            random.random()
            < 0.12,
    }


# ==========================================================
# App Target Builder
# ==========================================================

def build_app_target(
    app: dict,
    index: int,
) -> dict:

    return {

        "semantic":
            f"share_app_{index}",

        "name":
            app["name"],

        "icon":
            app["icon"],

        "pinned":
            random.random()
            < 0.15,

        "work_profile":
            random.random()
            < 0.10,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_share_sheet_data() -> dict:

    # ======================================================
    # Sheet State
    # ======================================================

    sheet_state = random.choices(
        [
            "compact",
            "expanded",
            "more_apps",
            "no_contacts",
        ],
        weights=[
            0.40,
            0.32,
            0.16,
            0.12,
        ],
        k=1,
    )[0]


    # ======================================================
    # Share Type
    # ======================================================

    share_type = random.choice([
        "text",
        "link",
        "image",
        "file",
    ])


    # ======================================================
    # Preview
    # ======================================================

    if share_type == "text":

        preview_title = random.choice([
            "Shared text",
            "Note",
            "Selected text",
        ])

        preview_subtitle = random.choice([
            "Here is some text I'd like to share.",
            "Meeting notes and reminders",
            "A short text selection",
        ])

        preview_icon = (
            "mdi:text-box-outline"
        )

        preview_image = None


    elif share_type == "link":

        preview_title = random.choice([
            "Interesting article",
            "Shared webpage",
            "Website",
        ])

        preview_subtitle = random.choice([
            "example.com/article",
            "news.example.com",
            "www.example.com",
        ])

        preview_icon = (
            "mdi:link-variant"
        )

        preview_image = None


    elif share_type == "image":

        preview_title = random.choice([
            "Photo",
            "Screenshot",
            "Image",
        ])

        preview_subtitle = random.choice([
            "1 image",
            "Screenshot",
            "Photo from gallery",
        ])

        preview_icon = (
            "mdi:image-outline"
        )

        preview_image = (
            get_random_asset(
                SHARE_IMAGE_DIR
            )
        )


    else:

        preview_title = random.choice([
            "Document.pdf",
            "Notes.txt",
            "Project.zip",
        ])

        preview_subtitle = random.choice([
            "PDF document",
            "Text document",
            "Archive",
        ])

        preview_icon = (
            "mdi:file-outline"
        )

        preview_image = None


    # ======================================================
    # Contacts
    # ======================================================

    show_contacts = (
        sheet_state
        != "no_contacts"
    )

    contact_count = (
        random.randint(
            3,
            6,
        )
        if show_contacts
        else 0
    )

    contacts = [

        build_contact(
            index
        )

        for index
        in range(
            contact_count
        )
    ]


    # ======================================================
    # App Targets
    # ======================================================

    if sheet_state == "compact":

        app_count = 4

    elif sheet_state == "expanded":

        app_count = random.randint(
            6,
            8,
        )

    elif sheet_state == "more_apps":

        app_count = random.randint(
            8,
            min(
                12,
                len(
                    SHARE_APPS
                ),
            ),
        )

    else:

        app_count = random.randint(
            5,
            8,
        )


    selected_apps = random.sample(
        SHARE_APPS,
        k=min(
            app_count,
            len(
                SHARE_APPS
            ),
        ),
    )

    app_targets = [

        build_app_target(
            app,
            index,
        )

        for index, app
        in enumerate(
            selected_apps
        )
    ]


    # ======================================================
    # Utility Actions
    # ======================================================

    action_count = random.randint(
        2,
        len(
            UTILITY_ACTIONS
        ),
    )

    utility_actions = random.sample(
        UTILITY_ACTIONS,
        action_count,
    )


    # ======================================================
    # Work Profile
    # ======================================================

    show_work_profile = (
        random.random()
        < 0.28
    )


    # ======================================================
    # Result
    # ======================================================

    return {

        "sheet_state":
            sheet_state,

        "share_type":
            share_type,

        "wallpaper":
            get_random_asset(
                WALLPAPER_DIR
            ),

        "preview": {

            "title":
                preview_title,

            "subtitle":
                preview_subtitle,

            "icon":
                preview_icon,

            "image":
                preview_image,
        },

        "show_contacts":
            show_contacts,

        "contacts":
            contacts,

        "app_targets":
            app_targets,

        "utility_actions":
            utility_actions,

        "show_work_profile":
            show_work_profile,

        "show_more_button":
            (
                sheet_state
                != "more_apps"
            ),
    }