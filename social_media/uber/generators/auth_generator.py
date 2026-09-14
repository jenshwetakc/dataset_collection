from __future__ import annotations

import random

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_promotion_image,
)


fake = Faker()


# ==========================================================
# Shared Helpers
# ==========================================================

def generate_brand_panel() -> dict:

    return {
        "title":
            random.choice(
                [
                    "Go anywhere with Uber",
                    "Your ride starts here",
                    "Move with confidence",
                    "Wherever you're going",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Reliable rides whenever you need them.",
                    "Book rides, manage trips, and get moving.",
                    "One account for rides, reservations, and more.",
                ]
            ),

        "image":
            get_random_promotion_image(),
    }


def generate_social_logins() -> list[dict]:

    methods = [
        {
            "label":
                "Continue with Google",

            "icon":
                "G",

            "semantic":
                "google",
        },
        {
            "label":
                "Continue with Apple",

            "icon":
                "apple",

            "semantic":
                "apple",
        },
    ]

    if random.random() < 0.4:

        methods.append(
            {
                "label":
                    "Continue with Facebook",

                "icon":
                    "F",

                "semantic":
                    "facebook",
            }
        )

    return methods


# ==========================================================
# Login
# ==========================================================

def generate_login_data() -> dict:

    return {

        "page_type":
            "login",

        "brand":
            generate_brand_panel(),

        "title":
            random.choice(
                [
                    "Sign in",
                    "Welcome back",
                    "Log in to Uber",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Enter your details to continue.",
                    "Access your trips, wallet, and account.",
                    "Sign in to continue using Uber.",
                ]
            ),

        "email_placeholder":
            random.choice(
                [
                    "Email or phone number",
                    "Email address",
                    "Phone or email",
                ]
            ),

        "password_placeholder":
            "Password",

        "forgot_password_label":
            "Forgot password?",

        "primary_action":
            random.choice(
                [
                    "Continue",
                    "Sign in",
                    "Log in",
                ]
            ),

        "signup_prompt":
            "Don't have an account?",

        "signup_action":
            "Sign up",

        "social_logins":
            generate_social_logins(),

        "remember_me":
            random.choice(
                [
                    True,
                    False,
                ]
            ),
    }


# ==========================================================
# Signup
# ==========================================================

def generate_signup_data() -> dict:

    return {

        "page_type":
            "signup",

        "brand":
            generate_brand_panel(),

        "title":
            random.choice(
                [
                    "Create your account",
                    "Sign up for Uber",
                    "Get started",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Create an account to start riding.",
                    "Join Uber and book your first ride.",
                    "Enter your details to create an account.",
                ]
            ),

        "fields": [
            {
                "name":
                    "full_name",

                "label":
                    "Full name",

                "placeholder":
                    fake.name(),

                "icon":
                    "person",
            },
            {
                "name":
                    "email",

                "label":
                    "Email",

                "placeholder":
                    "you@example.com",

                "icon":
                    "mail",
            },
            {
                "name":
                    "phone",

                "label":
                    "Phone number",

                "placeholder":
                    "+82 10 1234 5678",

                "icon":
                    "call",
            },
            {
                "name":
                    "password",

                "label":
                    "Password",

                "placeholder":
                    "Create a password",

                "icon":
                    "lock",
            },
        ],

        "terms_checked":
            random.choice(
                [
                    True,
                    False,
                    False,
                ]
            ),

        "terms_text":
            "I agree to the Terms of Use and Privacy Policy.",

        "primary_action":
            random.choice(
                [
                    "Create account",
                    "Sign up",
                    "Continue",
                ]
            ),

        "login_prompt":
            "Already have an account?",

        "login_action":
            "Sign in",

        "social_logins":
            generate_social_logins(),
    }


# ==========================================================
# Forgot Password
# ==========================================================

def generate_forgot_password_data() -> dict:

    verification_mode = random.choice(
        [
            "email",
            "phone",
        ]
    )

    return {

        "page_type":
            "forgot_password",

        "brand":
            generate_brand_panel(),

        "title":
            random.choice(
                [
                    "Reset your password",
                    "Forgot your password?",
                    "Recover your account",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Enter your email or phone number and we'll send you a reset link.",
                    "We'll help you get back into your account.",
                    "Choose where you'd like to receive your recovery instructions.",
                ]
            ),

        "verification_mode":
            verification_mode,

        "input_label":
            (
                "Email address"
                if verification_mode == "email"
                else "Phone number"
            ),

        "input_placeholder":
            (
                "you@example.com"
                if verification_mode == "email"
                else "+82 10 1234 5678"
            ),

        "input_icon":
            (
                "mail"
                if verification_mode == "email"
                else "call"
            ),

        "primary_action":
            random.choice(
                [
                    "Send reset link",
                    "Continue",
                    "Send instructions",
                ]
            ),

        "back_action":
            "Back to sign in",

        "help_text":
            random.choice(
                [
                    "Didn't receive anything? Check your spam folder or try again.",
                    "For security, reset links expire after a short period.",
                    "Make sure you use the email or phone connected to your account.",
                ]
            ),

        "show_success_preview":
            random.choice(
                [
                    True,
                    False,
                    False,
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    print("\nLOGIN")
    pprint(
        generate_login_data()
    )

    print("\nSIGNUP")
    pprint(
        generate_signup_data()
    )

    print("\nFORGOT PASSWORD")
    pprint(
        generate_forgot_password_data()
    )