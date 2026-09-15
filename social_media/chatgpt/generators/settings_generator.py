from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

SETTING_TABS = [
    {
        "id": "general",
        "label": "General",
        "icon": "tune",
    },
    {
        "id": "notifications",
        "label": "Notifications",
        "icon": "notifications",
    },
    {
        "id": "personalization",
        "label": "Personalization",
        "icon": "person",
    },
    {
        "id": "data",
        "label": "Data controls",
        "icon": "database",
    },
    {
        "id": "security",
        "label": "Security",
        "icon": "shield",
    },
]


LANGUAGES = [
    "English",
    "Korean",
    "Japanese",
    "Spanish",
    "French",
    "German",
]


THEME_OPTIONS = [
    "System",
    "Light",
    "Dark",
]


VOICE_OPTIONS = [
    "Maple",
    "Cove",
    "Juniper",
    "Vale",
    "Spruce",
]


# ==========================================================
# Sidebar History
# ==========================================================

def generate_history_sections() -> list[dict]:

    result = []

    section_labels = [
        "Today",
        "Yesterday",
        "Previous 7 days",
    ]

    examples = [
        "Python debugging",
        "UI dataset generation",
        "Research notes",
        "Paper summary",
        "Travel planning",
        "Model training",
        "Design feedback",
        "Code review",
        "Accessibility testing",
    ]

    for section_index, label in enumerate(
        section_labels
    ):

        count = random.randint(
            2,
            4,
        )

        selected = random.sample(
            examples,
            k=min(
                count,
                len(examples),
            ),
        )

        items = []

        for item_index, title in enumerate(
            selected
        ):

            items.append({
                "title":
                    title,

                "active":
                    (
                        section_index == 0
                        and item_index == 0
                    ),
            })

        result.append({
            "label":
                label,

            "items":
                items,
        })

    return result


# ==========================================================
# Setting Row Helpers
# ==========================================================

def toggle_row(
    *,
    title: str,
    description: str,
    semantic: str,
    probability: float = 0.5,
) -> dict:

    return {
        "type":
            "toggle",

        "title":
            title,

        "description":
            description,

        "semantic":
            semantic,

        "value":
            random.random()
            < probability,
    }


def select_row(
    *,
    title: str,
    description: str,
    semantic: str,
    value: str,
) -> dict:

    return {
        "type":
            "select",

        "title":
            title,

        "description":
            description,

        "semantic":
            semantic,

        "value":
            value,
    }


def action_row(
    *,
    title: str,
    description: str,
    semantic: str,
    action_label: str,
    destructive: bool = False,
) -> dict:

    return {
        "type":
            "action",

        "title":
            title,

        "description":
            description,

        "semantic":
            semantic,

        "action_label":
            action_label,

        "destructive":
            destructive,
    }


# ==========================================================
# General Settings
# ==========================================================

def generate_general_settings() -> list[dict]:

    return [

        select_row(
            title="Theme",
            description=(
                "Choose how ChatGPT appears "
                "on this device."
            ),
            semantic="theme_setting",
            value=random.choice(
                THEME_OPTIONS
            ),
        ),

        select_row(
            title="Language",
            description=(
                "Select the language used "
                "throughout the interface."
            ),
            semantic="language_setting",
            value=random.choice(
                LANGUAGES
            ),
        ),

        toggle_row(
            title="Show follow-up suggestions",
            description=(
                "Display suggested prompts "
                "after responses."
            ),
            semantic="follow_up_suggestions",
            probability=0.70,
        ),

        toggle_row(
            title="Enable animations",
            description=(
                "Use motion and transitions "
                "throughout the interface."
            ),
            semantic="interface_animations",
            probability=0.75,
        ),

        select_row(
            title="Voice",
            description=(
                "Choose the voice used during "
                "voice conversations."
            ),
            semantic="voice_setting",
            value=random.choice(
                VOICE_OPTIONS
            ),
        ),
    ]


# ==========================================================
# Notification Settings
# ==========================================================

def generate_notification_settings() -> list[dict]:

    return [

        toggle_row(
            title="Push notifications",
            description=(
                "Receive notifications about "
                "important activity."
            ),
            semantic="push_notifications",
            probability=0.70,
        ),

        toggle_row(
            title="Task updates",
            description=(
                "Get notified when scheduled "
                "tasks have updates."
            ),
            semantic="task_notifications",
            probability=0.55,
        ),

        toggle_row(
            title="Product updates",
            description=(
                "Receive occasional information "
                "about new features."
            ),
            semantic="product_notifications",
            probability=0.40,
        ),

        toggle_row(
            title="Email notifications",
            description=(
                "Receive selected notifications "
                "by email."
            ),
            semantic="email_notifications",
            probability=0.35,
        ),
    ]


# ==========================================================
# Personalization Settings
# ==========================================================

def generate_personalization_settings() -> list[dict]:

    return [

        toggle_row(
            title="Reference saved memories",
            description=(
                "Allow saved memories to help "
                "personalize responses."
            ),
            semantic="saved_memory",
            probability=0.65,
        ),

        toggle_row(
            title="Reference chat history",
            description=(
                "Allow previous chats to improve "
                "future conversations."
            ),
            semantic="chat_history_reference",
            probability=0.55,
        ),

        action_row(
            title="Manage memories",
            description=(
                "View and remove information "
                "saved for personalization."
            ),
            semantic="manage_memories",
            action_label="Manage",
        ),

        action_row(
            title="Custom instructions",
            description=(
                "Tell ChatGPT how you would "
                "like it to respond."
            ),
            semantic="custom_instructions",
            action_label="Edit",
        ),
    ]


# ==========================================================
# Data Settings
# ==========================================================

def generate_data_settings() -> list[dict]:

    return [

        toggle_row(
            title="Improve the model for everyone",
            description=(
                "Allow conversations to help "
                "improve future models."
            ),
            semantic="model_improvement",
            probability=0.45,
        ),

        action_row(
            title="Archived chats",
            description=(
                "Manage conversations you have "
                "previously archived."
            ),
            semantic="archived_chats",
            action_label="Manage",
        ),

        action_row(
            title="Export data",
            description=(
                "Request a copy of your account "
                "and conversation data."
            ),
            semantic="export_data",
            action_label="Export",
        ),

        action_row(
            title="Delete all chats",
            description=(
                "Permanently remove all "
                "conversation history."
            ),
            semantic="delete_all_chats",
            action_label="Delete",
            destructive=True,
        ),
    ]


# ==========================================================
# Security
# ==========================================================

def generate_security_settings() -> list[dict]:

    return [

        action_row(
            title="Multi-factor authentication",
            description=(
                "Add an additional verification "
                "step when signing in."
            ),
            semantic="multi_factor_auth",
            action_label=random.choice([
                "Enable",
                "Manage",
            ]),
        ),

        action_row(
            title="Active sessions",
            description=(
                "Review devices where your "
                "account is currently signed in."
            ),
            semantic="active_sessions",
            action_label="Manage",
        ),

        action_row(
            title="Log out of all devices",
            description=(
                "End every active account "
                "session."
            ),
            semantic="logout_all_devices",
            action_label="Log out",
        ),
    ]


# ==========================================================
# Section Resolver
# ==========================================================

def generate_settings_sections() -> dict:

    return {
        "general":
            generate_general_settings(),

        "notifications":
            generate_notification_settings(),

        "personalization":
            generate_personalization_settings(),

        "data":
            generate_data_settings(),

        "security":
            generate_security_settings(),
    }


# ==========================================================
# Generator
# ==========================================================

def generate_settings_data() -> dict:

    user_name = fake.name()

    email_name = (
        user_name
        .lower()
        .replace(
            " ",
            ".",
        )
    )

    active_tab = random.choice(
        SETTING_TABS
    )

    sections = (
        generate_settings_sections()
    )

    return {

        "page_variant":
            "settings",

        "model": {
            "name":
                random.choice([
                    "ChatGPT",
                    "GPT-5",
                    "GPT-5 Thinking",
                ]),
        },

        "user": {
            "name":
                user_name,

            "initials":
                "".join(
                    part[0]
                    for part in user_name.split()[:2]
                ).upper(),

            "email":
                (
                    f"{email_name}"
                    f"@example.com"
                ),
        },

        "history_sections":
            generate_history_sections(),

        "tabs":
            SETTING_TABS,

        "active_tab":
            active_tab["id"],

        "active_tab_label":
            active_tab["label"],

        "rows":
            sections[
                active_tab["id"]
            ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_settings_data()
    )