from __future__ import annotations

import random

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)


# ==========================================================
# Quality Options
# ==========================================================

QUALITY_OPTIONS = [
    "Automatic",
    "Low",
    "Normal",
    "High",
    "Very High",
]


DOWNLOAD_QUALITY_OPTIONS = [
    "Normal",
    "High",
    "Very High",
]


CROSSFADE_VALUES = [
    0,
    3,
    5,
    7,
    10,
    12,
]


LANGUAGES = [
    "English",
    "한국어",
    "日本語",
    "Español",
    "Deutsch",
    "Français",
]


# ==========================================================
# Toggle Item
# ==========================================================

def toggle_item(
    title: str,
    subtitle: str,
    semantic: str,
    enabled_probability: float = 0.5,
) -> dict:

    return {
        "type": "toggle",
        "title": title,
        "subtitle": subtitle,
        "semantic": semantic,
        "enabled": (
            random.random()
            < enabled_probability
        ),
    }


# ==========================================================
# Select Item
# ==========================================================

def select_item(
    title: str,
    subtitle: str,
    semantic: str,
    options: list[str],
) -> dict:

    return {
        "type": "select",
        "title": title,
        "subtitle": subtitle,
        "semantic": semantic,
        "value": random.choice(
            options
        ),
    }


# ==========================================================
# Navigation Item
# ==========================================================

def navigation_item(
    title: str,
    subtitle: str,
    semantic: str,
    icon: str,
) -> dict:

    return {
        "type": "navigation",
        "title": title,
        "subtitle": subtitle,
        "semantic": semantic,
        "icon": icon,
    }


# ==========================================================
# Action Item
# ==========================================================

def action_item(
    title: str,
    subtitle: str,
    semantic: str,
    icon: str,
    destructive: bool = False,
) -> dict:

    return {
        "type": "action",
        "title": title,
        "subtitle": subtitle,
        "semantic": semantic,
        "icon": icon,
        "destructive": destructive,
    }


# ==========================================================
# Settings Page
# ==========================================================

def generate_settings_page() -> dict:

    storage_used = random.randint(
        2,
        28,
    )

    storage_total = random.choice(
        [
            32,
            64,
            128,
            256,
        ]
    )

    storage_ratio = min(
        storage_used / storage_total,
        1.0,
    )


    return {

        # ==================================================
        # Navigation
        # ==================================================

        "navigation":
            generate_navigation(
                selected=""
            ),

        "title":
            "Settings",


        # ==================================================
        # Search
        # ==================================================

        "search_placeholder":
            "Search settings",


        # ==================================================
        # Account
        # ==================================================

        "account": {

            "name":
                random.choice(
                    [
                        "Alex Morgan",
                        "Jamie Park",
                        "Maya Chen",
                        "Daniel Kim",
                        "Hana Lee",
                    ]
                ),

            "plan":
                random.choice(
                    [
                        "Spotify Free",
                        "Premium Individual",
                        "Premium Duo",
                        "Premium Family",
                        "Premium Student",
                    ]
                ),

            "email":
                random.choice(
                    [
                        "alex@example.com",
                        "music@example.com",
                        "listener@example.com",
                        "spotify.user@example.com",
                    ]
                ),
        },


        # ==================================================
        # Playback
        # ==================================================

        "playback": [

            toggle_item(
                title="Autoplay",
                subtitle=(
                    "Keep listening to similar tracks "
                    "when your music ends."
                ),
                semantic="autoplay",
                enabled_probability=0.70,
            ),

            toggle_item(
                title="Gapless playback",
                subtitle=(
                    "Allow seamless transitions "
                    "between songs."
                ),
                semantic="gapless_playback",
                enabled_probability=0.65,
            ),

            toggle_item(
                title="Automix",
                subtitle=(
                    "Allow smooth transitions "
                    "between tracks."
                ),
                semantic="automix",
                enabled_probability=0.55,
            ),

            toggle_item(
                title="Normalize volume",
                subtitle=(
                    "Set the same volume level "
                    "for all tracks."
                ),
                semantic="normalize_volume",
                enabled_probability=0.75,
            ),

            select_item(
                title="Crossfade",
                subtitle=(
                    "Overlap tracks for a smooth "
                    "transition."
                ),
                semantic="crossfade",
                options=[
                    f"{value} sec"
                    for value
                    in CROSSFADE_VALUES
                ],
            ),
        ],


        # ==================================================
        # Audio Quality
        # ==================================================

        "audio_quality": [

            select_item(
                title="Wi-Fi streaming quality",
                subtitle=(
                    "Choose the quality used while "
                    "streaming over Wi-Fi."
                ),
                semantic="wifi_quality",
                options=QUALITY_OPTIONS,
            ),

            select_item(
                title="Cellular streaming quality",
                subtitle=(
                    "Higher quality uses more mobile data."
                ),
                semantic="cellular_quality",
                options=QUALITY_OPTIONS,
            ),

            select_item(
                title="Download quality",
                subtitle=(
                    "Higher quality uses more storage."
                ),
                semantic="download_quality",
                options=DOWNLOAD_QUALITY_OPTIONS,
            ),

            toggle_item(
                title="Download using cellular",
                subtitle=(
                    "Allow downloads when Wi-Fi "
                    "is unavailable."
                ),
                semantic="cellular_download",
                enabled_probability=0.20,
            ),
        ],


        # ==================================================
        # Content
        # ==================================================

        "content": [

            toggle_item(
                title="Allow explicit content",
                subtitle=(
                    "Play content marked as explicit."
                ),
                semantic="explicit_content",
                enabled_probability=0.75,
            ),

            navigation_item(
                title="Blocked content",
                subtitle=(
                    "Manage songs and artists "
                    "you've hidden."
                ),
                semantic="blocked_content",
                icon="block",
            ),

            select_item(
                title="Language",
                subtitle=(
                    "Choose the language used "
                    "throughout Spotify."
                ),
                semantic="language",
                options=LANGUAGES,
            ),
        ],


        # ==================================================
        # Data Saver
        # ==================================================

        "data_saver": [

            toggle_item(
                title="Data Saver",
                subtitle=(
                    "Reduce audio quality and limit "
                    "visual content."
                ),
                semantic="data_saver",
                enabled_probability=0.35,
            ),

            toggle_item(
                title="Audio-only podcasts",
                subtitle=(
                    "Download podcast audio without video."
                ),
                semantic="audio_only_podcasts",
                enabled_probability=0.45,
            ),
        ],


        # ==================================================
        # Social
        # ==================================================

        "social": [

            toggle_item(
                title="Private session",
                subtitle=(
                    "Listening activity won't influence "
                    "recommendations temporarily."
                ),
                semantic="private_session",
                enabled_probability=0.15,
            ),

            toggle_item(
                title="Listening activity",
                subtitle=(
                    "Share what you listen to "
                    "with followers."
                ),
                semantic="listening_activity",
                enabled_probability=0.65,
            ),

            toggle_item(
                title="Recently played artists",
                subtitle=(
                    "Show recently played artists "
                    "on your profile."
                ),
                semantic="recent_artists",
                enabled_probability=0.60,
            ),
        ],


        # ==================================================
        # Notifications
        # ==================================================

        "notifications": [

            toggle_item(
                title="New music",
                subtitle=(
                    "Receive updates about artists "
                    "you follow."
                ),
                semantic="new_music_notifications",
                enabled_probability=0.70,
            ),

            toggle_item(
                title="Playlist updates",
                subtitle=(
                    "Get notifications when collaborative "
                    "playlists change."
                ),
                semantic="playlist_notifications",
                enabled_probability=0.50,
            ),

            toggle_item(
                title="Podcast episodes",
                subtitle=(
                    "Get notified when followed shows "
                    "publish new episodes."
                ),
                semantic="podcast_notifications",
                enabled_probability=0.55,
            ),
        ],


        # ==================================================
        # Storage
        # ==================================================

        "storage": {

            "used":
                storage_used,

            "total":
                storage_total,

            "ratio":
                storage_ratio,

            "items": [

                action_item(
                    title="Clear cache",
                    subtitle=(
                        "Remove temporary files without "
                        "deleting downloads."
                    ),
                    semantic="clear_cache",
                    icon="delete_sweep",
                ),

                action_item(
                    title="Remove all downloads",
                    subtitle=(
                        "Delete downloaded music "
                        "and podcast episodes."
                    ),
                    semantic="remove_downloads",
                    icon="download_done",
                    destructive=True,
                ),
            ],
        },


        # ==================================================
        # About
        # ==================================================

        "about": [

            navigation_item(
                title="Privacy policy",
                subtitle="View Spotify's privacy information.",
                semantic="privacy_policy",
                icon="privacy_tip",
            ),

            navigation_item(
                title="Terms and conditions",
                subtitle="View Spotify's terms of use.",
                semantic="terms",
                icon="description",
            ),

            navigation_item(
                title="About Spotify",
                subtitle="Version 9.2.14",
                semantic="about_spotify",
                icon="info",
            ),

            action_item(
                title="Log out",
                subtitle="Sign out of this account.",
                semantic="logout",
                icon="logout",
                destructive=True,
            ),
        ],
    }