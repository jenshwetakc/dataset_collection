import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_about():

    return random.choice(
        [
            "Available",
            "Busy",
            "At work",
            "Sleeping",
            "Battery about to die",
            "Hey there! I am using WhatsApp.",
            fake.sentence(
                nb_words=random.randint(
                    3,
                    8,
                )
            ),
        ]
    )


def generate_storage_usage():

    value = random.uniform(
        0.5,
        24.0,
    )

    return f"{value:.1f} GB"


def generate_language():

    return random.choice(
        [
            "English",
            "한국어",
            "हिन्दी",
            "日本語",
            "Español",
            "Français",
        ]
    )


# ==========================================================
# Profile
# ==========================================================

def generate_profile():

    return {

        "name":
            fake.name(),

        "about":
            generate_about(),

        "avatar":
            get_random_avatar(),

        "show_qr":
            random.random() < 0.85,

        "show_camera":
            random.random() < 0.50,
    }


# ==========================================================
# Settings Item
# ==========================================================

def build_item(
    item_id,
    title,
    subtitle,
    icon,
    value=None,
    show_chevron=True,
    switch=None,
    badge=None,
):

    return {
        "id": item_id,
        "title": title,
        "subtitle": subtitle,
        "icon": icon,
        "value": value,
        "show_chevron": show_chevron,
        "switch": switch,
        "badge": badge,
    }


# ==========================================================
# Sections
# ==========================================================

def generate_settings_sections():

    sections = []


    # ------------------------------------------------------
    # Main settings
    # ------------------------------------------------------

    main_items = [

        build_item(
            item_id="account",
            title="Account",
            subtitle="Security notifications, change number",
            icon="key",
        ),

        build_item(
            item_id="privacy",
            title="Privacy",
            subtitle="Block contacts, disappearing messages",
            icon="lock",
        ),

        build_item(
            item_id="avatar",
            title="Avatar",
            subtitle="Create, edit, profile photo",
            icon="face",
        ),

        build_item(
            item_id="lists",
            title="Lists",
            subtitle="Manage people and groups",
            icon="list_alt",
        ),
    ]

    sections.append(
        {
            "id": "main",
            "items": main_items,
        }
    )


    # ------------------------------------------------------
    # App preferences
    # ------------------------------------------------------

    preference_items = [

        build_item(
            item_id="chats",
            title="Chats",
            subtitle="Theme, wallpapers, chat history",
            icon="chat",
            value=random.choice(
                [
                    "Default",
                    "Dark",
                    "Light",
                ]
            ),
        ),

        build_item(
            item_id="notifications",
            title="Notifications",
            subtitle="Message, group and call tones",
            icon="notifications",
        ),

        build_item(
            item_id="storage_data",
            title="Storage and data",
            subtitle="Network usage, auto-download",
            icon="data_usage",
            value=generate_storage_usage(),
        ),

        build_item(
            item_id="app_language",
            title="App language",
            subtitle="Choose your preferred language",
            icon="language",
            value=generate_language(),
        ),
    ]

    sections.append(
        {
            "id": "preferences",
            "items": preference_items,
        }
    )


    # ------------------------------------------------------
    # Utility
    # ------------------------------------------------------

    utility_items = [

        build_item(
            item_id="help",
            title="Help",
            subtitle="Help center, contact us, privacy policy",
            icon="help",
        ),

        build_item(
            item_id="invite_friend",
            title="Invite a friend",
            subtitle="Share WhatsApp with others",
            icon="person_add",
        ),
    ]

    sections.append(
        {
            "id": "utility",
            "items": utility_items,
        }
    )


    # ------------------------------------------------------
    # Optional settings / switches
    # ------------------------------------------------------

    optional_items = [

        build_item(
            item_id="two_step_verification",
            title="Two-step verification",
            subtitle="Extra protection for your account",
            icon="shield",
            switch=random.choice(
                [
                    True,
                    False,
                ]
            ),
            show_chevron=False,
        ),

        build_item(
            item_id="read_receipts",
            title="Read receipts",
            subtitle="Show when messages are read",
            icon="done_all",
            switch=random.choice(
                [
                    True,
                    False,
                ]
            ),
            show_chevron=False,
        ),
    ]

    if random.random() < 0.75:
        sections.append(
            {
                "id": "optional",
                "items": optional_items,
            }
        )


    return sections


# ==========================================================
# Footer Info
# ==========================================================

def generate_footer():

    return {

        "show":
            True,

        "app_name":
            "WhatsApp",

        "from_meta":
            random.random() < 0.85,
    }


# ==========================================================
# Settings Page
# ==========================================================

def generate_settings_page():

    profile = (
        generate_profile()
    )

    sections = (
        generate_settings_sections()
    )

    return {

        "title":
            "Settings",

        "profile":
            profile,

        "sections":
            sections,

        "footer":
            generate_footer(),
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_settings_page()
    )

    print(
        "\nSETTINGS PAGE"
    )

    print(
        "Title:",
        page["title"]
    )

    print(
        "Profile name:",
        page["profile"]["name"]
    )

    print(
        "About:",
        page["profile"]["about"]
    )

    print(
        "Avatar exists:",
        page["profile"]["avatar"] is not None
    )

    print(
        "Sections:",
        len(page["sections"])
    )

    for section in page["sections"]:

        print(
            f"\nSection: {section['id']}"
        )

        for item in section["items"]:

            print(
                "-",
                item["title"],
                "| icon:",
                item["icon"],
                "| value:",
                item["value"],
                "| switch:",
                item["switch"],
            )