# social_media/slack/generators/media_generator.py


from __future__ import annotations

import random
from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
    image_to_data_uri,
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)
# ==========================================================
# Slack Assets
# ==========================================================

ASSET_DIR = (
    PROJECT_ROOT
    / "assets"
)

# SLACK_ASSETS_ROOT = (
#     ASSETS_ROOT
#     / "slack"
# )


AVATAR_DIR = (
    ASSET_DIR
    / "avatars"
)


# WORKSPACE_DIR = (
#     ASSET_DIR
#     / "workspaces"
# )

WORKSPACE_DIR = (
    ASSET_DIR
    / "photos"
)


ATTACHMENT_DIR = (
    ASSET_DIR
    / "attachments"
)


FILE_PREVIEW_DIR = (
    ASSET_DIR
    / "file_previews"
)


# ==========================================================
# Emoji Assets
# ==========================================================

NOTO_EMOJI_DIR = (
    ASSETS_ROOT
    / "noto_emoji"
)


TWEMOJI_DIR = (
    ASSETS_ROOT
    / "twemoji"
)


# ==========================================================
# Standard Media
# ==========================================================

def get_random_avatar() -> str | None:

    return get_random_image(
        AVATAR_DIR
    )


def get_random_workspace_image() -> str | None:

    return get_random_image(
        WORKSPACE_DIR
    )


def get_random_attachment() -> str | None:

    return get_random_image(
        ATTACHMENT_DIR
    )


def get_random_file_preview() -> str | None:

    return get_random_image(
        FILE_PREVIEW_DIR
    )


# ==========================================================
# Random Emoji
# ==========================================================

def get_random_emoji(
    source: str | None = None,
) -> dict | None:
    """
    Return one random emoji asset.

    Parameters
    ----------
    source:
        None
            Randomly choose Noto Emoji or Twemoji.

        "noto"
            Noto Emoji only.

        "twemoji"
            Twemoji only.
    """

    if source is None:

        source = random.choice(
            [
                "noto",
                "twemoji",
            ]
        )


    if source == "noto":

        directory = (
            NOTO_EMOJI_DIR
        )

        source_name = (
            "noto_emoji"
        )


    elif source == "twemoji":

        directory = (
            TWEMOJI_DIR
        )

        source_name = (
            "twemoji"
        )


    else:

        raise ValueError(
            f"Unknown emoji source: {source}"
        )


    files = get_image_files(
        str(directory)
    )


    if not files:

        return None


    emoji_file = random.choice(
        files
    )


    return {

        "image":
            image_to_data_uri(
                emoji_file
            ),

        "source":
            source_name,

        "name":
            emoji_file.stem,
    }


# ==========================================================
# Random Multiple Emojis
# ==========================================================

def get_random_emojis(
    count: int,
) -> list[dict]:

    emojis = []

    for _ in range(
        count
    ):

        emoji = (
            get_random_emoji()
        )

        if emoji is not None:

            emojis.append(
                emoji
            )

    return emojis
