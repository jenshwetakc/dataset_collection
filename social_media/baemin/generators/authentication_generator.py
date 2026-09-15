from __future__ import annotations

import random

from faker import Faker


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Pools
# ==========================================================

AUTH_STATES = [
    "phone",
    "phone",
    "otp",
]


PHONE_HEADLINES = [
    "Welcome to Baemin",
    "Ready for something delicious?",
    "Sign in to start ordering",
    "Your next meal is waiting",
]


PHONE_SUPPORT = [
    "Enter your mobile number to continue.",
    "We'll send a verification code to your phone.",
    "Use your mobile number to sign in or create an account.",
]


OTP_HEADLINES = [
    "Check your phone",
    "Enter verification code",
    "Verify your number",
]


OTP_SUPPORT = [
    "We sent a 6-digit verification code.",
    "Enter the code we sent to your mobile number.",
    "Your verification code should arrive shortly.",
]


SOCIAL_METHODS = [
    {
        "name": "Continue with Kakao",
        "icon": "chat_bubble",
        "semantic": "kakao_login",
    },
    {
        "name": "Continue with Google",
        "icon": "language",
        "semantic": "google_login",
    },
    {
        "name": "Continue with Apple",
        "icon": "phone_iphone",
        "semantic": "apple_login",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_phone_number() -> str:

    return (
        f"010-"
        f"{random.randint(1000, 9999)}-"
        f"{random.randint(1000, 9999)}"
    )


def mask_phone(
    phone: str,
) -> str:

    parts = phone.split("-")

    if len(parts) != 3:
        return phone

    return (
        f"{parts[0]}-"
        f"****-"
        f"{parts[2]}"
    )


def generate_otp_digits() -> list[str]:

    code = (
        f"{random.randint(0, 999999):06d}"
    )

    filled_count = random.choice(
        [
            0,
            1,
            2,
            3,
            4,
            6,
        ]
    )

    return [
        digit
        if index < filled_count
        else ""

        for index, digit
        in enumerate(
            code
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_authentication_data() -> dict:

    state = random.choice(
        AUTH_STATES
    )

    phone = generate_phone_number()

    user_name = fake.first_name()

    social_methods = random.sample(
        SOCIAL_METHODS,
        k=random.randint(
            2,
            len(
                SOCIAL_METHODS
            ),
        ),
    )

    return {

        # ==================================================
        # State
        # ==================================================

        "state":
            state,


        # ==================================================
        # Identity
        # ==================================================

        "user": {

            "name":
                user_name,

            "phone":
                phone,

            "masked_phone":
                mask_phone(
                    phone
                ),
        },


        # ==================================================
        # Brand
        # ==================================================

        "brand": {

            "title":
                "Baemin",

            "tagline":
                random.choice(
                    [
                        "Great food, delivered.",
                        "Your favorites are closer than you think.",
                        "Discover something delicious today.",
                        "Food for every moment.",
                    ]
                ),
        },


        # ==================================================
        # Phone State
        # ==================================================

        "phone_state": {

            "headline":
                random.choice(
                    PHONE_HEADLINES
                ),

            "support":
                random.choice(
                    PHONE_SUPPORT
                ),

            "country_code":
                "+82",

            "country":
                "South Korea",

            "phone":
                (
                    phone
                    if random.random() < 0.45
                    else ""
                ),

            "placeholder":
                random.choice(
                    [
                        "010-1234-5678",
                        "Enter mobile number",
                        "Mobile phone number",
                    ]
                ),

            "terms_checked":
                random.random()
                < 0.55,

            "marketing_checked":
                random.random()
                < 0.25,
        },


        # ==================================================
        # OTP State
        # ==================================================

        "otp_state": {

            "headline":
                random.choice(
                    OTP_HEADLINES
                ),

            "support":
                random.choice(
                    OTP_SUPPORT
                ),

            "digits":
                generate_otp_digits(),

            "remaining":
                random.choice(
                    [
                        "02:58",
                        "02:31",
                        "01:46",
                        "01:12",
                        "00:48",
                    ]
                ),

            "resend_enabled":
                random.random()
                < 0.35,
        },


        # ==================================================
        # Social
        # ==================================================

        "social_methods":
            social_methods,


        # ==================================================
        # Misc
        # ==================================================

        "support_text":
            random.choice(
                [
                    "Having trouble signing in?",
                    "Need help with verification?",
                    "Can't access your phone?",
                ]
            ),
    }