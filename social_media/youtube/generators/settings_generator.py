from __future__ import annotations

import random
from typing import Any

from faker import Faker

from social_media.youtube.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Settings Sections
# ==========================================================

SETTINGS_SECTIONS = [
    {
        "id": "account",
        "label": "Account",
        "icon": "person",
    },
    {
        "id": "notifications",
        "label": "Notifications",
        "icon": "notifications",
    },
    {
        "id": "playback",
        "label": "Playback and performance",
        "icon": "play_circle",
    },
    {
        "id": "downloads",
        "label": "Downloads",
        "icon": "download",
    },
    {
        "id": "privacy",
        "label": "Privacy",
        "icon": "lock",
    },
    {
        "id": "connected_apps",
        "label": "Connected apps",
        "icon": "link",
    },
    {
        "id": "billing",
        "label": "Billing and payments",
        "icon": "credit_card",
    },
    {
        "id": "advanced",
        "label": "Advanced settings",
        "icon": "settings",
    },
]


# ==========================================================
# User
# ==========================================================

def generate_user() -> dict[str, Any]:

    name = fake.name()

    username = (
        "@"
        + fake.user_name()
        .replace(".", "")
        .replace("_", "")[:16]
    )

    return {
        "name": name,
        "username": username,
        "email": fake.email(),
        "avatar": get_random_avatar(),
    }


# ==========================================================
# Header
# ==========================================================

def generate_header() -> dict[str, Any]:

    return {
        "logo_text": "YouTube",
        "search_placeholder": "Search",
        "show_voice_search": random.random() < 0.8,
        "show_create": True,
        "show_notifications": True,
        "avatar": get_random_avatar(),
    }


# ==========================================================
# Sidebar
# ==========================================================

def generate_settings_navigation(
    selected_section: str,
) -> list[dict[str, Any]]:

    return [
        {
            **section,
            "selected": section["id"] == selected_section,
            "semantic": f"settings_{section['id']}",
        }
        for section in SETTINGS_SECTIONS
    ]


# ==========================================================
# Common Controls
# ==========================================================

def switch_setting(
    *,
    label: str,
    description: str,
    semantic: str,
    enabled: bool | None = None,
) -> dict[str, Any]:

    if enabled is None:
        enabled = random.random() < 0.6

    return {
        "type": "switch",
        "label": label,
        "description": description,
        "semantic": semantic,
        "enabled": enabled,
    }


def select_setting(
    *,
    label: str,
    description: str,
    semantic: str,
    options: list[str],
) -> dict[str, Any]:

    return {
        "type": "select",
        "label": label,
        "description": description,
        "semantic": semantic,
        "value": random.choice(options),
        "options": options,
    }


def action_setting(
    *,
    label: str,
    description: str,
    semantic: str,
    action_label: str,
    destructive: bool = False,
) -> dict[str, Any]:

    return {
        "type": "action",
        "label": label,
        "description": description,
        "semantic": semantic,
        "action_label": action_label,
        "destructive": destructive,
    }


# ==========================================================
# Account Settings
# ==========================================================

def generate_account_settings(
    user: dict[str, Any],
) -> dict[str, Any]:

    return {
        "title": "Account",
        "subtitle": "Choose how you appear and what you see on YouTube.",
        "groups": [
            {
                "title": "Your YouTube channel",
                "description": (
                    "This is your public identity on YouTube. "
                    "You need a channel to upload videos, comment, or create playlists."
                ),
                "type": "profile",
                "profile": user,
                "actions": [
                    {
                        "label": "View channel",
                        "semantic": "view_channel_button",
                    },
                    {
                        "label": "Edit on Google",
                        "semantic": "edit_google_account_button",
                    },
                ],
            },
            {
                "title": "Your account",
                "description": "You sign in to YouTube with your Google Account.",
                "type": "settings",
                "items": [
                    action_setting(
                        label="Google Account",
                        description="Manage your account information and privacy.",
                        semantic="google_account_setting",
                        action_label="View or change",
                    ),
                    action_setting(
                        label="Membership",
                        description="Manage your YouTube memberships and purchases.",
                        semantic="membership_setting",
                        action_label="Manage",
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Notification Settings
# ==========================================================

def generate_notification_settings() -> dict[str, Any]:

    return {
        "title": "Notifications",
        "subtitle": "Choose when and how to be notified.",
        "groups": [
            {
                "title": "General",
                "type": "settings",
                "items": [
                    switch_setting(
                        label="Subscriptions",
                        description="Notify me about activity from channels I subscribe to.",
                        semantic="subscription_notifications",
                    ),
                    switch_setting(
                        label="Recommended videos",
                        description="Notify me about videos I might like based on what I watch.",
                        semantic="recommended_video_notifications",
                    ),
                    switch_setting(
                        label="Activity on my channel",
                        description="Notify me about comments and other activity on my channel.",
                        semantic="channel_activity_notifications",
                    ),
                    switch_setting(
                        label="Replies to my comments",
                        description="Notify me when someone replies to my comments.",
                        semantic="comment_reply_notifications",
                    ),
                    switch_setting(
                        label="Mentions",
                        description="Notify me when others mention my channel.",
                        semantic="mention_notifications",
                    ),
                ],
            },
            {
                "title": "Email notifications",
                "type": "settings",
                "items": [
                    switch_setting(
                        label="Permission",
                        description="Send me emails about my YouTube activity and updates.",
                        semantic="email_notifications",
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Playback
# ==========================================================

def generate_playback_settings() -> dict[str, Any]:

    return {
        "title": "Playback and performance",
        "subtitle": "Control your viewing experience.",
        "groups": [
            {
                "title": "Browsing",
                "type": "settings",
                "items": [
                    switch_setting(
                        label="Inline playback",
                        description="Play videos while you browse the Home feed.",
                        semantic="inline_playback",
                    ),
                    switch_setting(
                        label="Video previews",
                        description="Show animated video previews while browsing.",
                        semantic="video_previews",
                    ),
                ],
            },
            {
                "title": "Playback",
                "type": "settings",
                "items": [
                    switch_setting(
                        label="Autoplay",
                        description="Automatically play the next video.",
                        semantic="autoplay_setting",
                    ),
                    switch_setting(
                        label="Always show captions",
                        description="Show captions when they are available.",
                        semantic="always_show_captions",
                    ),
                    select_setting(
                        label="AV1 settings",
                        description="Choose when YouTube should use the AV1 video format.",
                        semantic="av1_setting",
                        options=[
                            "Auto",
                            "Prefer AV1 for SD",
                            "Always prefer AV1",
                        ],
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Downloads
# ==========================================================

def generate_download_settings() -> dict[str, Any]:

    return {
        "title": "Downloads",
        "subtitle": "Choose how downloaded videos are stored.",
        "groups": [
            {
                "title": "Download settings",
                "type": "settings",
                "items": [
                    select_setting(
                        label="Download quality",
                        description="Choose the default quality for downloaded videos.",
                        semantic="download_quality",
                        options=[
                            "Ask each time",
                            "360p",
                            "720p",
                            "1080p",
                        ],
                    ),
                    switch_setting(
                        label="Download over Wi-Fi only",
                        description="Avoid using mobile data for downloads.",
                        semantic="wifi_download_only",
                    ),
                    switch_setting(
                        label="Smart downloads",
                        description="Automatically download recommended videos.",
                        semantic="smart_downloads",
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Privacy
# ==========================================================

def generate_privacy_settings() -> dict[str, Any]:

    return {
        "title": "Privacy",
        "subtitle": "Manage what you share on YouTube.",
        "groups": [
            {
                "title": "Playlists and subscriptions",
                "type": "settings",
                "items": [
                    switch_setting(
                        label="Keep all my saved playlists private",
                        description="Only you can view playlists you save.",
                        semantic="private_playlists",
                    ),
                    switch_setting(
                        label="Keep all my subscriptions private",
                        description="Other users will not see the channels you subscribe to.",
                        semantic="private_subscriptions",
                    ),
                ],
            },
            {
                "title": "Ads",
                "type": "settings",
                "items": [
                    action_setting(
                        label="Google Ads settings",
                        description="Control personalization of ads shown to you.",
                        semantic="ads_settings",
                        action_label="View settings",
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Connected Apps
# ==========================================================

def generate_connected_apps_settings() -> dict[str, Any]:

    apps = random.sample(
        [
            ("Google Ads", "ads_click"),
            ("Discord", "forum"),
            ("Steam", "sports_esports"),
            ("Google Photos", "photo_library"),
        ],
        k=random.randint(2, 4),
    )

    return {
        "title": "Connected apps",
        "subtitle": "Connect YouTube with supported services.",
        "groups": [
            {
                "title": "Connected services",
                "type": "apps",
                "items": [
                    {
                        "name": name,
                        "icon": icon,
                        "connected": random.random() < 0.45,
                        "semantic": (
                            name.lower()
                            .replace(" ", "_")
                            + "_connection"
                        ),
                    }
                    for name, icon in apps
                ],
            },
        ],
    }


# ==========================================================
# Billing
# ==========================================================

def generate_billing_settings() -> dict[str, Any]:

    return {
        "title": "Billing and payments",
        "subtitle": "Manage purchases and memberships.",
        "groups": [
            {
                "title": "Purchases",
                "type": "settings",
                "items": [
                    action_setting(
                        label="Purchases and memberships",
                        description="View and manage your purchases.",
                        semantic="purchases_setting",
                        action_label="Manage",
                    ),
                    action_setting(
                        label="Payment methods",
                        description="Manage payment information for purchases.",
                        semantic="payment_methods",
                        action_label="Manage",
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Advanced
# ==========================================================

def generate_advanced_settings() -> dict[str, Any]:

    return {
        "title": "Advanced settings",
        "subtitle": "Advanced account and channel options.",
        "groups": [
            {
                "title": "User ID and channel ID",
                "type": "settings",
                "items": [
                    action_setting(
                        label="User ID",
                        description=fake.uuid4(),
                        semantic="user_id_setting",
                        action_label="Copy",
                    ),
                    action_setting(
                        label="Channel ID",
                        description=fake.uuid4(),
                        semantic="channel_id_setting",
                        action_label="Copy",
                    ),
                ],
            },
            {
                "title": "Delete channel",
                "type": "settings",
                "items": [
                    action_setting(
                        label="Remove YouTube content",
                        description="Permanently remove your YouTube content.",
                        semantic="remove_youtube_content",
                        action_label="Delete",
                        destructive=True,
                    ),
                ],
            },
        ],
    }


# ==========================================================
# Resolve Content
# ==========================================================

def generate_section_content(
    section: str,
    user: dict[str, Any],
) -> dict[str, Any]:

    mapping = {
        "account": lambda: generate_account_settings(user),
        "notifications": generate_notification_settings,
        "playback": generate_playback_settings,
        "downloads": generate_download_settings,
        "privacy": generate_privacy_settings,
        "connected_apps": generate_connected_apps_settings,
        "billing": generate_billing_settings,
        "advanced": generate_advanced_settings,
    }

    return mapping[section]()


# ==========================================================
# Full Page
# ==========================================================

def generate_settings_page(
    selected_section: str | None = None,
) -> dict[str, Any]:

    if selected_section is None:
        selected_section = random.choice(
            [section["id"] for section in SETTINGS_SECTIONS]
        )

    valid_sections = {
        section["id"]
        for section in SETTINGS_SECTIONS
    }

    if selected_section not in valid_sections:
        raise ValueError(
            f"Unknown settings section: {selected_section}. "
            f"Expected one of: {sorted(valid_sections)}"
        )

    user = generate_user()

    return {
        "page_type": "settings",
        "header": generate_header(),
        "user": user,
        "selected_section": selected_section,
        "navigation": generate_settings_navigation(
            selected_section
        ),
        "content": generate_section_content(
            selected_section,
            user,
        ),
        "layout": {
            "show_sidebar": True,
            "show_bottom_navigation": False,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    for section in SETTINGS_SECTIONS:

        page = generate_settings_page(
            selected_section=section["id"]
        )

        print(
            "\n"
            "=========================================="
        )

        print(
            "Section:",
            page["selected_section"],
        )

        print(
            "Title:",
            page["content"]["title"],
        )

        print(
            "Groups:",
            len(page["content"]["groups"]),
        )