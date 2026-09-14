from __future__ import annotations

import random

from faker import Faker

from social_media.steam.generators.media_generator import (
    get_random_game_cover,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_game_title() -> str:

    templates = [
        lambda: f"{fake.word().title()} Horizon",
        lambda: f"{fake.word().title()} Protocol",
        lambda: f"{fake.word().title()} Frontier",
        lambda: f"{fake.word().title()} Chronicles",
        lambda: f"Project {fake.word().title()}",
        lambda: f"{fake.word().title()} Odyssey",
    ]

    return random.choice(
        templates
    )()


def generate_price() -> dict:

    original = random.choice([
        9.99,
        14.99,
        19.99,
        24.99,
        29.99,
        39.99,
        49.99,
        59.99,
        69.99,
    ])

    has_discount = (
        random.random()
        < 0.55
    )

    if not has_discount:

        return {
            "original_value":
                original,

            "original":
                None,

            "discount_percent":
                None,

            "current_value":
                original,

            "current":
                f"${original:.2f}",
        }

    discount = random.choice([
        10,
        15,
        20,
        25,
        30,
        40,
        50,
        60,
        75,
    ])

    current = (
        original
        * (
            1
            - discount / 100
        )
    )

    return {
        "original_value":
            original,

        "original":
            f"${original:.2f}",

        "discount_percent":
            discount,

        "current_value":
            current,

        "current":
            f"${current:.2f}",
    }


# ==========================================================
# Cart Game
# ==========================================================

def generate_cart_game() -> dict:

    return {

        "title":
            generate_game_title(),

        "image":
            get_random_game_cover(),

        "price":
            generate_price(),

        "purchase_type":
            random.choice([
                "For my account",
                "Gift",
            ]),

        "platforms":
            random.sample(
                [
                    "desktop_windows",
                    "laptop_mac",
                    "terminal",
                ],
                k=random.randint(
                    1,
                    3,
                ),
            ),

        "refundable":
            random.random() < 0.85,

        "points":
            random.randint(
                500,
                7000,
            ),
    }


# ==========================================================
# Recommended Game
# ==========================================================

def generate_recommendation() -> dict:

    return {

        "title":
            generate_game_title(),

        "image":
            get_random_game_cover(),

        "price":
            generate_price(),

        "rating":
            random.randint(
                75,
                98,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_shopping_cart_data() -> dict:

    cart_games = [
        generate_cart_game()
        for _ in range(
            random.randint(
                2,
                5,
            )
        )
    ]

    subtotal = sum(
        game[
            "price"
        ][
            "current_value"
        ]
        for game
        in cart_games
    )

    tax_rate = random.choice([
        0.0,
        0.05,
        0.08,
        0.10,
    ])

    tax = (
        subtotal
        * tax_rate
    )

    wallet_balance = round(
        random.uniform(
            0,
            80,
        ),
        2,
    )

    total = (
        subtotal
        + tax
    )

    return {

        "title":
            "Your Shopping Cart",

        "cart_games":
            cart_games,

        "cart_count":
            len(
                cart_games
            ),

        "subtotal":
            f"${subtotal:.2f}",

        "tax":
            f"${tax:.2f}",

        "tax_rate":
            round(
                tax_rate
                * 100
            ),

        "total":
            f"${total:.2f}",

        "wallet_balance":
            f"${wallet_balance:.2f}",

        "wallet_value":
            wallet_balance,

        "wallet_covers_total":
            wallet_balance
            >= total,

        "points_total":
            sum(
                game["points"]
                for game
                in cart_games
            ),

        "recommended_games": [
            generate_recommendation()
            for _ in range(
                6
            )
        ],
    }