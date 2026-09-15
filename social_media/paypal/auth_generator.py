from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_banner,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

AUTH_MODES = [
    "login",
    "signup",
    "forgot_password",
]


SOCIAL_OPTIONS = [
    {
        "label": "Continue with Google",
        "icon": "language",
        "semantic": "google",
    },
    {
        "label": "Continue with Apple",
        "icon": "phone_iphone",
        "semantic": "apple",
    },
]


# ==========================================================
# Field Helpers
# ==========================================================

def generate_email_field() -> dict:

    has_error = (
        random.random()
        < 0.18
    )

    return {
        "label":
            "Email",

        "placeholder":
            random.choice([
                "Email address",
                "you@example.com",
                "Enter your email",
            ]),

        "value":
            (
                fake.email()
                if random.random() < 0.45
                else ""
            ),

        "has_error":
            has_error,

        "error_message":
            (
                random.choice([
                    "Enter a valid email address.",
                    "We couldn't find that email.",
                    "Email address is required.",
                ])
                if has_error
                else ""
            ),
    }


def generate_password_field() -> dict:

    has_error = (
        random.random()
        < 0.16
    )

    return {
        "label":
            "Password",

        "placeholder":
            "Enter your password",

        "value":
            (
                fake.password(
                    length=random.randint(
                        8,
                        14,
                    )
                )
                if random.random() < 0.35
                else ""
            ),

        "visible":
            random.random()
            < 0.20,

        "has_error":
            has_error,

        "error_message":
            (
                random.choice([
                    "Your password is incorrect.",
                    "Password must contain at least 8 characters.",
                    "Password is required.",
                ])
                if has_error
                else ""
            ),
    }


# ==========================================================
# Password Strength
# ==========================================================

def generate_password_strength() -> dict:

    level = random.choice([
        "weak",
        "medium",
        "strong",
    ])

    mapping = {
        "weak": {
            "percent": 30,
            "label": "Weak",
        },
        "medium": {
            "percent": 65,
            "label": "Medium",
        },
        "strong": {
            "percent": 100,
            "label": "Strong",
        },
    }

    return {
        "level":
            level,

        **mapping[level],
    }


# ==========================================================
# Login
# ==========================================================

def generate_login_data() -> dict:

    return {
        "mode":
            "login",

        "title":
            random.choice([
                "Log in to PayPal",
                "Welcome back",
                "Sign in to your account",
            ]),

        "subtitle":
            random.choice([
                "Access your payments, wallet, and activity.",
                "Enter your details to continue.",
                "Securely access your PayPal account.",
            ]),

        "email":
            generate_email_field(),

        "password":
            generate_password_field(),

        "remember_me":
            random.choice([
                True,
                False,
            ]),

        "primary_label":
            random.choice([
                "Log in",
                "Sign in",
                "Continue",
            ]),

        "social_options":
            SOCIAL_OPTIONS,

        "show_verification_dialog":
            random.random()
            < 0.18,

        "banner":
            get_random_banner(),
    }


# ==========================================================
# Signup
# ==========================================================

def generate_signup_data() -> dict:

    first_name = (
        fake.first_name()
        if random.random() < 0.35
        else ""
    )

    last_name = (
        fake.last_name()
        if random.random() < 0.35
        else ""
    )

    phone = (
        fake.phone_number()
        if random.random() < 0.25
        else ""
    )

    return {
        "mode":
            "signup",

        "title":
            random.choice([
                "Create your PayPal account",
                "Join PayPal",
                "Let's get you started",
            ]),

        "subtitle":
            random.choice([
                "Send, spend, and manage money securely.",
                "Create an account in just a few steps.",
                "Start using PayPal for payments and transfers.",
            ]),

        "first_name":
            first_name,

        "last_name":
            last_name,

        "phone":
            phone,

        "email":
            generate_email_field(),

        "password":
            generate_password_field(),

        "password_strength":
            generate_password_strength(),

        "accept_terms":
            random.choice([
                True,
                False,
            ]),

        "primary_label":
            random.choice([
                "Create account",
                "Sign up",
                "Continue",
            ]),

        "show_verification_dialog":
            random.random()
            < 0.15,

        "banner":
            get_random_banner(),
    }


# ==========================================================
# Forgot Password
# ==========================================================

def generate_forgot_password_data() -> dict:

    return {
        "mode":
            "forgot_password",

        "title":
            random.choice([
                "Forgot your password?",
                "Reset your password",
                "Need help signing in?",
            ]),

        "subtitle":
            random.choice([
                "Enter your email and we'll help you reset your password.",
                "We'll send you instructions to recover your account.",
                "Enter the email connected to your PayPal account.",
            ]),

        "email":
            generate_email_field(),

        "primary_label":
            random.choice([
                "Send reset link",
                "Continue",
                "Reset password",
            ]),

        "show_verification_dialog":
            random.random()
            < 0.22,

        "banner":
            get_random_banner(),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_auth_data() -> dict:

    mode = random.choice(
        AUTH_MODES
    )

    if mode == "signup":

        return generate_signup_data()

    if mode == "forgot_password":

        return generate_forgot_password_data()

    return generate_login_data()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_auth_data()
    )