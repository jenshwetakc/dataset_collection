from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
        "semantic": "home",
    },
    {
        "label": "Activity",
        "icon": "receipt_long",
        "semantic": "activity",
    },
    {
        "label": "Send",
        "icon": "send",
        "semantic": "send",
    },
    {
        "label": "Wallet",
        "icon": "account_balance_wallet",
        "semantic": "wallet",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_switch_setting(
    semantic: str,
    title: str,
    description: str,
    icon: str,
) -> dict:

    return {
        "semantic": semantic,
        "title": title,
        "description": description,
        "icon": icon,
        "type": "switch",
        "enabled": random.choice([
            True,
            False,
        ]),
    }


def generate_link_setting(
    semantic: str,
    title: str,
    description: str,
    icon: str,
    value: str = "",
) -> dict:

    return {
        "semantic": semantic,
        "title": title,
        "description": description,
        "icon": icon,
        "type": "link",
        "value": value,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_settings_data() -> dict:

    name = fake.name()

    language = random.choice([
        "English",
        "한국어",
        "Español",
        "Deutsch",
        "Français",
    ])

    currency = random.choice([
        "USD",
        "KRW",
        "EUR",
        "GBP",
    ])

    security_settings = [
        generate_link_setting(
            semantic="password",
            title="Password",
            description="Update your account password.",
            icon="lock",
            value="Updated recently",
        ),

        generate_link_setting(
            semantic="two_factor",
            title="2-step verification",
            description="Add another layer of account security.",
            icon="verified_user",
            value=random.choice([
                "On",
                "Off",
            ]),
        ),

        generate_link_setting(
            semantic="devices",
            title="Devices",
            description="Review devices where you're signed in.",
            icon="devices",
            value=f"{random.randint(1, 5)} devices",
        ),

        generate_switch_setting(
            semantic="biometric",
            title="Biometric login",
            description="Use fingerprint or face recognition.",
            icon="fingerprint",
        ),
    ]


    notification_settings = [
        generate_switch_setting(
            semantic="payment_notifications",
            title="Payment notifications",
            description="Get updates about payments and transfers.",
            icon="payments",
        ),

        generate_switch_setting(
            semantic="marketing_notifications",
            title="Offers and promotions",
            description="Receive personalized deals and offers.",
            icon="local_offer",
        ),

        generate_switch_setting(
            semantic="email_notifications",
            title="Email notifications",
            description="Receive account updates by email.",
            icon="mail",
        ),
    ]


    preference_settings = [
        generate_link_setting(
            semantic="language",
            title="Language",
            description="Choose the language PayPal uses.",
            icon="language",
            value=language,
        ),

        generate_link_setting(
            semantic="currency",
            title="Preferred currency",
            description="Choose your default currency.",
            icon="currency_exchange",
            value=currency,
        ),

        generate_switch_setting(
            semantic="dark_mode",
            title="Dark mode",
            description="Use a darker appearance.",
            icon="dark_mode",
        ),
    ]


    privacy_settings = [
        generate_switch_setting(
            semantic="search_visibility",
            title="Let people find you",
            description="Allow others to find you using your email or phone.",
            icon="person_search",
        ),

        generate_switch_setting(
            semantic="activity_visibility",
            title="Activity visibility",
            description="Control who can see your payment activity.",
            icon="visibility",
        ),

        generate_link_setting(
            semantic="data_privacy",
            title="Data & privacy",
            description="Manage your PayPal data and privacy controls.",
            icon="privacy_tip",
        ),
    ]


    return {

        "title":
            random.choice([
                "Settings",
                "Profile & settings",
                "Account settings",
            ]),

        "profile": {
            "name":
                name,

            "email":
                fake.email(),

            "phone":
                fake.phone_number(),

            "avatar":
                get_random_avatar(),

            "initial":
                name[0].upper(),

            "verified":
                random.random()
                < 0.85,

            "member_since":
                random.randint(
                    2016,
                    2026,
                ),
        },

        "security_settings":
            security_settings,

        "notification_settings":
            notification_settings,

        "preference_settings":
            preference_settings,

        "privacy_settings":
            privacy_settings,

        "navigation":
            NAVIGATION_ITEMS,

        "show_signout_dialog":
            random.random()
            < 0.25,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_settings_data()
    )