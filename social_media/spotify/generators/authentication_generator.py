from __future__ import annotations

import random

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_artist_banner,
    get_random_music_cover,
    get_random_playlist_cover,
)


# ==========================================================
# Modes / Variants
# ==========================================================

AUTH_MODES = [
    "login",
    "signup",
    "forgot_password",
]

LAYOUT_VARIANTS = [
    "split",
    "centered",
]


# ==========================================================
# Data Pools
# ==========================================================

FIRST_NAMES = [
    "Alex",
    "Jamie",
    "Maya",
    "Noah",
    "Hana",
    "Daniel",
    "Sora",
    "Ava",
    "Leo",
    "Elena",
]

LAST_NAMES = [
    "Kim",
    "Park",
    "Chen",
    "Reed",
    "Stone",
    "Grey",
    "Hart",
    "Lane",
    "Cruz",
    "Lee",
]

BRAND_HEADLINES = [
    "Music for every moment.",
    "Discover your next favorite song.",
    "Listen to what moves you.",
    "Millions of tracks, one place.",
    "Podcasts, playlists, and music made for you.",
]

BRAND_SUPPORTING_TEXTS = [
    "Stream music, playlists, and podcasts tailored to your mood.",
    "Find artists, albums, and mixes you’ll want to replay.",
    "Pick up where you left off and keep listening anywhere.",
    "Build playlists, follow artists, and explore fresh recommendations.",
]

EMAIL_DOMAINS = [
    "example.com",
    "gmail.com",
    "outlook.com",
    "spotifymail.com",
]

SOCIAL_BUTTONS = [
    {
        "label": "Continue with Google",
        "icon": "language",
        "semantic": "continue_with_google",
    },
    {
        "label": "Continue with Apple",
        "icon": "phone_iphone",
        "semantic": "continue_with_apple",
    },
]

GENDER_OPTIONS = [
    "Female",
    "Male",
    "Non-binary",
    "Prefer not to say",
]


# ==========================================================
# Helpers
# ==========================================================

def random_name() -> str:
    return (
        f"{random.choice(FIRST_NAMES)} "
        f"{random.choice(LAST_NAMES)}"
    )


def random_email(name: str | None = None) -> str:
    if name is None:
        name = random_name()

    normalized = (
        name.lower()
        .replace(" ", ".")
    )

    if random.random() < 0.45:
        normalized += str(
            random.randint(1, 99)
        )

    return (
        f"{normalized}@"
        f"{random.choice(EMAIL_DOMAINS)}"
    )


def maybe_prefill(value: str) -> str:
    if random.random() < 0.45:
        return value
    return ""


def random_birth_date() -> dict:
    return {
        "day": str(random.randint(1, 28)),
        "month": random.choice(
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
        ),
        "year": str(random.randint(1988, 2005)),
    }


def generate_branding() -> dict:
    image = (
        get_random_artist_banner()
        or get_random_music_cover()
        or get_random_playlist_cover()
        or get_random_album_cover()
    )

    return {
        "headline": random.choice(
            BRAND_HEADLINES
        ),
        "supporting_text": random.choice(
            BRAND_SUPPORTING_TEXTS
        ),
        "image": image,
        "eyebrow": random.choice(
            [
                "Spotify",
                "Welcome",
                "Your music starts here",
            ]
        ),
    }


def generate_gender_options() -> list[dict]:
    options = random.sample(
        GENDER_OPTIONS,
        k=3,
    )
    selected = random.choice(options)

    return [
        {
            "label": option,
            "selected": option == selected,
        }
        for option in options
    ]


# ==========================================================
# Login
# ==========================================================

def generate_login_data() -> dict:
    sample_name = random_name()

    return {
        "title": "Welcome back",
        "subtitle": "Sign in to continue listening.",
        "email": maybe_prefill(
            random_email(sample_name)
        ),
        "password": maybe_prefill("password123"),
        "show_password": random.random() < 0.25,
        "remember_me": random.random() < 0.55,
        "primary_cta": "Log in",
        "forgot_label": "Forgot password?",
        "footer_prompt": "Don't have an account?",
        "footer_action": "Sign up",
        "social_buttons": SOCIAL_BUTTONS,
    }


# ==========================================================
# Signup
# ==========================================================

def generate_signup_data() -> dict:
    sample_name = random_name()
    birth = random_birth_date()

    return {
        "title": "Create your account",
        "subtitle": "Join Spotify and start listening.",
        "name": maybe_prefill(sample_name),
        "email": maybe_prefill(
            random_email(sample_name)
        ),
        "password": "",
        "confirm_password": "",
        "show_password": random.random() < 0.15,
        "show_confirm_password": random.random() < 0.15,
        "birth": birth,
        "gender_options": generate_gender_options(),
        "agree_terms": random.random() < 0.70,
        "primary_cta": "Create account",
        "footer_prompt": "Already have an account?",
        "footer_action": "Log in",
        "social_buttons": SOCIAL_BUTTONS,
    }


# ==========================================================
# Forgot Password
# ==========================================================

def generate_forgot_password_data() -> dict:
    sample_name = random_name()

    return {
        "title": "Forgot your password?",
        "subtitle": (
            "Enter your email address and we’ll "
            "send you a reset link."
        ),
        "email": maybe_prefill(
            random_email(sample_name)
        ),
        "primary_cta": "Send reset link",
        "secondary_cta": "Back to login",
        "helper_text": (
            "Reset instructions usually arrive "
            "within a few minutes."
        ),
    }


# ==========================================================
# Page Generator
# ==========================================================

def generate_authentication_page() -> dict:
    return {
        "mode": random.choice(
            AUTH_MODES
        ),
        "layout_variant": random.choice(
            LAYOUT_VARIANTS
        ),
        "branding": generate_branding(),
        "login": generate_login_data(),
        "signup": generate_signup_data(),
        "forgot_password": (
            generate_forgot_password_data()
        ),
    }