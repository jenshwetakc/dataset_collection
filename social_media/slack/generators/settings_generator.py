# social_media/slack/generators/settings_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.slack.generators.media_generator import (
    get_random_avatar,
    get_random_workspace_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Constants
# ==========================================================

WORKSPACE_NAMES = [
    "Acme Studio",
    "Northstar",
    "Orbit Labs",
    "Pixel Works",
    "Nova Research",
    "Mosaic",
    "Vertex",
    "Nimbus",
    "Launchpad",
]


SETTING_SECTIONS = [
    {
        "icon": "notifications",
        "label": "Notifications",
    },
    {
        "icon": "volume_up",
        "label": "Sound & appearance",
    },
    {
        "icon": "palette",
        "label": "Themes",
    },
    {
        "icon": "chat",
        "label": "Messages & media",
    },
    {
        "icon": "language",
        "label": "Language & region",
    },
    {
        "icon": "accessibility_new",
        "label": "Accessibility",
    },
    {
        "icon": "security",
        "label": "Privacy & visibility",
    },
    {
        "icon": "devices",
        "label": "Connected devices",
    },
    {
        "icon": "tune",
        "label": "Advanced",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def _toggle(
    label: str,
    description: str,
    probability: float = 0.6,
) -> dict:

    return {
        "label": label,
        "description": description,
        "enabled": random.random() < probability,
    }


def _select(
    label: str,
    description: str,
    options: list[str],
) -> dict:

    return {
        "label": label,
        "description": description,
        "value": random.choice(options),
        "options": options,
    }


# ==========================================================
# Settings Generator
# ==========================================================

def generate_settings_data() -> dict:

    workspace_name = random.choice(
        WORKSPACE_NAMES
    )

    profile_name = fake.name()

    profile_avatar = get_random_avatar()

    # ------------------------------------------------------
    # Notification toggles
    # ------------------------------------------------------

    notification_toggles = [
        _toggle(
            "Direct messages",
            "Notify me whenever I receive a direct message.",
            0.85,
        ),
        _toggle(
            "Mentions and keywords",
            "Notify me when someone mentions me or one of my keywords.",
            0.9,
        ),
        _toggle(
            "Thread replies",
            "Notify me about replies to threads I'm following.",
            0.72,
        ),
        _toggle(
            "Channel activity",
            "Show notifications for important channel activity.",
            0.42,
        ),
    ]

    # ------------------------------------------------------
    # Sound
    # ------------------------------------------------------

    sound_toggles = [
        _toggle(
            "Notification sounds",
            "Play a sound when a new notification arrives.",
            0.72,
        ),
        _toggle(
            "Huddle sounds",
            "Play sounds when joining or leaving a huddle.",
            0.65,
        ),
        _toggle(
            "Message send sound",
            "Play a short sound after sending a message.",
            0.48,
        ),
    ]

    # ------------------------------------------------------
    # Appearance
    # ------------------------------------------------------

    theme_options = [
        {
            "name": "Light",
            "mode": "light",
            "selected": False,
        },
        {
            "name": "Dark",
            "mode": "dark",
            "selected": False,
        },
        {
            "name": "System",
            "mode": "system",
            "selected": False,
        },
    ]

    selected_theme = random.choice(
        theme_options
    )

    selected_theme["selected"] = True

    density_options = [
        {
            "label": "Comfortable",
            "description": "More space between messages.",
            "selected": False,
        },
        {
            "label": "Compact",
            "description": "Show more content on screen.",
            "selected": False,
        },
    ]

    random.choice(
        density_options
    )["selected"] = True

    # ------------------------------------------------------
    # Accessibility
    # ------------------------------------------------------

    accessibility = [
        _toggle(
            "Reduce motion",
            "Reduce animations and motion effects.",
            0.25,
        ),
        _toggle(
            "Always underline links",
            "Make links easier to distinguish from normal text.",
            0.35,
        ),
        _toggle(
            "Increase contrast",
            "Use stronger contrast for selected interface elements.",
            0.3,
        ),
    ]

    # ------------------------------------------------------
    # Select controls
    # ------------------------------------------------------

    select_controls = [
        _select(
            "Notification schedule",
            "Pause notifications outside your preferred hours.",
            [
                "Always notify",
                "Weekdays only",
                "Custom schedule",
            ],
        ),
        _select(
            "Notification sound",
            "Choose the sound used for Slack notifications.",
            [
                "Knock",
                "Ding",
                "Ping",
                "None",
            ],
        ),
        _select(
            "Language",
            "Choose your Slack interface language.",
            [
                "English",
                "한국어",
                "日本語",
                "Deutsch",
            ],
        ),
        _select(
            "Time format",
            "Choose how times appear throughout Slack.",
            [
                "12-hour",
                "24-hour",
            ],
        ),
    ]

    # ------------------------------------------------------
    # Keywords
    # ------------------------------------------------------

    keywords = random.sample(
        [
            "release",
            "dataset",
            "annotation",
            "accessibility",
            "research",
            "testing",
            "review",
        ],
        k=random.randint(
            2,
            4,
        ),
    )

    return {

        "workspace": {
            "name":
                workspace_name,

            "image":
                get_random_workspace_image(),
        },

        "profile": {
            "name":
                profile_name,

            "avatar":
                profile_avatar,

            "email":
                fake.email(),
        },

        "sections":
            SETTING_SECTIONS,

        "selected_section":
            "Notifications",

        "notification_toggles":
            notification_toggles,

        "sound_toggles":
            sound_toggles,

        "theme_options":
            theme_options,

        "density_options":
            density_options,

        "accessibility":
            accessibility,

        "select_controls":
            select_controls,

        "keywords":
            keywords,

        "search_placeholder":
            f"Search {workspace_name}",

        "quiet_hours": {
            "enabled":
                random.random() < 0.65,

            "start":
                random.choice(
                    [
                        "8:00 PM",
                        "9:00 PM",
                        "10:00 PM",
                        "11:00 PM",
                    ]
                ),

            "end":
                random.choice(
                    [
                        "7:00 AM",
                        "8:00 AM",
                        "9:00 AM",
                    ]
                ),
        },

        "mobile_notifications":
            _toggle(
                "Mobile notifications",
                "Send notifications to your mobile device.",
                0.8,
            ),

        "email_notifications":
            _toggle(
                "Email notifications",
                "Email me when I miss important activity.",
                0.45,
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_settings_data()

    print(
        "\n=============================="
    )

    print(
        "SLACK SETTINGS DATA"
    )

    print(
        "=============================="
    )

    print(
        "Workspace:",
        data["workspace"]["name"]
    )

    print(
        "Profile:",
        data["profile"]["name"]
    )

    print(
        "Selected section:",
        data["selected_section"]
    )