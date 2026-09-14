from __future__ import annotations

from pathlib import Path

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


# ==========================================================
# Spotify Media Directories
# ==========================================================



ALBUM_DIR = (
    ASSETS_ROOT
    / "albums"
)

PLAYLIST_DIR = (
    ASSETS_ROOT
    / "playlists"
)

ARTIST_DIR = (
    ASSETS_ROOT
    / "avatars"
)

PODCAST_DIR = (
    ASSETS_ROOT
    / "podcasts"
)
#
# BANNER_DIR = (
#     ASSETS_ROOT
#     / "banners"
# )
BANNER_DIR = (
    ASSETS_ROOT
    / "podcasts"
)


# ==========================================================
# Spotify Media Helpers
# ==========================================================

def get_random_album_cover() -> str | None:

    return get_random_image(
        ALBUM_DIR
    )


def get_random_playlist_cover() -> str | None:

    return get_random_image(
        PLAYLIST_DIR
    )


def get_random_artist_image() -> str | None:

    return get_random_image(
        ARTIST_DIR
    )


def get_random_podcast_cover() -> str | None:

    return get_random_image(
        PODCAST_DIR
    )


def get_random_artist_banner() -> str | None:

    return get_random_image(
        BANNER_DIR
    )


# ==========================================================
# Generic Music Artwork
#
# Useful if some asset folders are empty.
# ==========================================================

def get_random_music_cover() -> str | None:

    image = (
        get_random_album_cover()
    )

    if image:
        return image

    image = (
        get_random_playlist_cover()
    )

    if image:
        return image

    return get_random_artist_image()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "SPOTIFY MEDIA"
    )

    print(
        "=============================="
    )

    print(
        "Album:",
        ALBUM_DIR
    )

    print(
        "Playlist:",
        PLAYLIST_DIR
    )

    print(
        "Artist:",
        ARTIST_DIR
    )

    print(
        "Podcast:",
        PODCAST_DIR
    )

    print(
        "Banner:",
        BANNER_DIR
    )

    cover = (
        get_random_music_cover()
    )

    print(
        "Random cover loaded:",
        cover is not None
    )