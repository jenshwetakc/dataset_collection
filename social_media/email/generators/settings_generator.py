from __future__ import annotations

import random

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Settings States
# ==========================================================

SETTINGS_STATES = [
    "general",
    "notifications",
    "appearance",
    "signature",
    "forwarding",
    "blocked_senders",
    "vacation_responder",
    "theme_picker_popup",
    "save_confirmation",
]


# ==========================================================
# Helpers
# ==========================================================

def _bool(
    probability: float = 0.5,
) -> bool:

    return random.random() < probability


def _account() -> dict:

    name = fake.name()

    return {
        "name": name,
        "email": fake.email(),
        "avatar": get_random_avatar(),
    }


def _blocked_sender(
    index: int,
) -> dict:

    return {
        "id": f"blocked_sender_{index}",
        "name": fake.name(),
        "email": fake.email(),
    }


def _theme_option(
    key: str,
    label: str,
    description: str,
) -> dict:

    return {
        "key": key,
        "label": label,
        "description": description,
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_settings_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            SETTINGS_STATES
        )
    )

    if selected_state not in SETTINGS_STATES:

        raise ValueError(
            f"Unknown settings state: {selected_state}. "
            f"Expected one of: {SETTINGS_STATES}"
        )

    if selected_state in [
        "theme_picker_popup",
        "appearance",
    ]:
        selected_section = "appearance"

    elif selected_state == "signature":
        selected_section = "signature"

    elif selected_state == "forwarding":
        selected_section = "forwarding"

    elif selected_state == "blocked_senders":
        selected_section = "blocked_senders"

    elif selected_state == "vacation_responder":
        selected_section = "vacation_responder"

    elif selected_state == "notifications":
        selected_section = "notifications"

    else:
        selected_section = "general"

    theme_options = [
        _theme_option(
            "light",
            "Light",
            "Bright interface for daytime use",
        ),
        _theme_option(
            "dark",
            "Dark",
            "Low-light appearance",
        ),
        _theme_option(
            "system",
            "Use device theme",
            "Automatically match your system",
        ),
    ]

    selected_theme = random.choice(
        ["light", "dark", "system"]
    )

    blocked_count = random.randint(
        4,
        8,
    )

    blocked_senders = [
        _blocked_sender(index)
        for index in range(
            blocked_count
        )
    ]

    settings_sections = [
        {
            "key": "general",
            "label": "General",
            "icon": "tune",
        },
        {
            "key": "notifications",
            "label": "Notifications",
            "icon": "notifications",
        },
        {
            "key": "appearance",
            "label": "Appearance",
            "icon": "palette",
        },
        {
            "key": "signature",
            "label": "Signature",
            "icon": "draw",
        },
        {
            "key": "forwarding",
            "label": "Forwarding",
            "icon": "forward",
        },
        {
            "key": "blocked_senders",
            "label": "Blocked",
            "icon": "block",
        },
        {
            "key": "vacation_responder",
            "label": "Vacation responder",
            "icon": "beach_access",
        },
    ]

    return {
        "state":
            selected_state,

        "title":
            "Settings",

        "account":
            _account(),

        "sections":
            settings_sections,

        "selected_section":
            selected_section,

        "search_text":
            random.choice([
                "",
                "notification",
                "theme",
                "signature",
            ]),

        "general": {
            "conversation_view": _bool(0.75),
            "desktop_notifications": _bool(0.55),
            "keyboard_shortcuts": _bool(0.45),
            "smart_compose": _bool(0.70),
            "undo_send_seconds": random.choice([
                5,
                10,
                20,
                30,
            ]),
            "default_reply_action": random.choice([
                "Reply",
                "Reply all",
            ]),
        },

        "notifications": {
            "new_mail_push": _bool(0.75),
            "important_only": _bool(0.4),
            "sound_enabled": _bool(0.55),
            "newsletter_digest": _bool(0.3),
            "desktop_alert_preview": _bool(0.7),
            "quiet_hours": _bool(0.35),
            "quiet_hours_range": random.choice([
                "22:00 - 07:00",
                "23:00 - 06:30",
                "21:30 - 07:30",
            ]),
        },

        "appearance": {
            "selected_theme": selected_theme,
            "message_density": random.choice([
                "Default",
                "Comfortable",
                "Compact",
            ]),
            "inbox_type": random.choice([
                "Default",
                "Priority",
                "Multiple inboxes",
            ]),
            "preview_pane": random.choice([
                "No split",
                "Right of inbox",
                "Below inbox",
            ]),
            "theme_options": theme_options,
        },

        "signature": {
            "enabled": _bool(0.8),
            "use_for_replies": _bool(0.6),
            "name": fake.name(),
            "role": random.choice([
                "Research Assistant",
                "Graduate Student",
                "Product Designer",
                "Software Engineer",
            ]),
            "organization": random.choice([
                "Open Research Lab",
                "Example University",
                "Design Systems Team",
                "Mail Studio",
            ]),
            "phone": fake.phone_number(),
        },

        "forwarding": {
            "enabled": _bool(0.45),
            "email": fake.email(),
            "keep_copy": _bool(0.8),
            "mark_forwarded_as_read": _bool(0.5),
            "forward_selected_only": _bool(0.35),
        },

        "blocked_senders": {
            "rows": blocked_senders,
            "search_term": random.choice([
                "",
                "alex",
                "support",
                "promo",
            ]),
        },

        "vacation_responder": {
            "enabled": _bool(0.5),
            "start_date": "2026-09-10",
            "end_date": "2026-09-18",
            "send_to_contacts_only": _bool(0.6),
            "subject": "Out of office",
            "message": (
                "Thank you for your email. "
                "I am currently away and may have limited access "
                "to email. I will respond as soon as possible."
            ),
        },

        "theme_picker_open": (
            selected_state
            == "theme_picker_popup"
        ),

        "save_confirmation_open": (
            selected_state
            == "save_confirmation"
        ),

        "mobile_nav_items": [
            ("inbox", "Inbox"),
            ("search", "Search"),
            ("edit", "Compose"),
            ("settings", "Settings"),
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_settings_data()

    print("\n==============================")
    print("EMAIL SETTINGS GENERATOR")
    print("==============================")

    print(
        "State:",
        data["state"],
    )

    print(
        "Selected section:",
        data["selected_section"],
    )

    print(
        "Blocked senders:",
        len(
            data["blocked_senders"]["rows"]
        ),
    )
