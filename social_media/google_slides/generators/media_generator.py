from pathlib import Path

from social_media.common.media_generator import (
    get_random_image,
)


PLAYSTORE_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

ASSETS_ROOT = (
    PLAYSTORE_ROOT
    / "assets"
)

APP_ICONS_ROOT = (
    ASSETS_ROOT
    / "app_icons"
)

SCREENSHOTS_ROOT = (
    ASSETS_ROOT
    / "photos"
)