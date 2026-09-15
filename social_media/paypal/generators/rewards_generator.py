from __future__ import annotations

import random

from faker import Faker

from social_media.paypal.generators.media_generator import (
    get_random_offer_image,
    get_random_banner,
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
# Categories
# ==========================================================

CATEGORIES = [
    {
        "label": "For you",
        "icon": "auto_awesome",
        "semantic": "for_you",
    },
    {
        "label": "Shopping",
        "icon": "shopping_bag",
        "semantic": "shopping",
    },
    {
        "label": "Food",
        "icon": "restaurant",
        "semantic": "food",
    },
    {
        "label": "Travel",
        "icon": "flight",
        "semantic": "travel",
    },
    {
        "label": "Entertainment",
        "icon": "movie",
        "semantic": "entertainment",
    },
]


MERCHANTS = [
    "Nike",
    "Adidas",
    "Starbucks",
    "Uber",
    "Airbnb",
    "Spotify",
    "Netflix",
    "Apple",
    "Amazon",
    "Booking.com",
    "Samsung",
    "Sephora",
    "H&M",
    "Uniqlo",
]


OFFER_TYPES = [
    "cashback",
    "discount",
    "points",
]


# ==========================================================
# Offer
# ==========================================================

def generate_offer(
    index: int,
) -> dict:

    merchant = random.choice(
        MERCHANTS
    )

    offer_type = random.choice(
        OFFER_TYPES
    )

    if offer_type == "cashback":

        value = random.choice([
            5,
            8,
            10,
            15,
            20,
        ])

        headline = (
            f"{value}% cash back"
        )

        description = (
            f"Earn {value}% cash back "
            f"when you pay with PayPal."
        )

    elif offer_type == "discount":

        value = random.choice([
            5,
            10,
            15,
            20,
            25,
        ])

        headline = (
            f"${value} off"
        )

        description = (
            f"Save ${value} on an "
            f"eligible purchase."
        )

    else:

        value = random.choice([
            2,
            3,
            5,
        ])

        headline = (
            f"{value}x points"
        )

        description = (
            f"Earn {value}x rewards "
            f"points on your purchase."
        )

    expires_in = random.randint(
        2,
        30,
    )

    return {
        "id":
            index,

        "merchant":
            merchant,

        "headline":
            headline,

        "description":
            description,

        "offer_type":
            offer_type,

        "image":
            get_random_offer_image(),

        "badge":
            random.choice([
                "Popular",
                "Limited time",
                "Recommended",
                "",
            ]),

        "expires":
            f"Ends in {expires_in} days",

        "saved":
            random.random()
            < 0.20,
    }


# ==========================================================
# Featured Banner
# ==========================================================

def generate_featured() -> dict:

    value = random.choice([
        5,
        10,
        15,
        20,
    ])

    return {
        "eyebrow":
            random.choice([
                "Featured reward",
                "PayPal Rewards",
                "This week's pick",
            ]),

        "title":
            random.choice([
                f"Earn up to {value}% cash back",
                "More rewards when you pay",
                "Shop smarter with PayPal",
            ]),

        "description":
            random.choice([
                "Explore personalized offers from brands you love.",
                "Activate offers and earn rewards on eligible purchases.",
                "Save offers now and use PayPal when you check out.",
            ]),

        "image":
            get_random_banner(),

        "button_label":
            random.choice([
                "Explore offers",
                "See rewards",
                "Start earning",
            ]),
    }


# ==========================================================
# Reward Progress
# ==========================================================

def generate_reward_progress() -> dict:

    current = random.randint(
        120,
        850,
    )

    target = 1000

    return {
        "current":
            current,

        "target":
            target,

        "percent":
            min(
                100,
                round(
                    current
                    / target
                    * 100
                ),
            ),

        "balance":
            f"{random.randint(100, 2500):,} pts",

        "cash_value":
            f"${random.uniform(2, 25):.2f}",
    }


# ==========================================================
# Main
# ==========================================================

def generate_rewards_data() -> dict:

    offers = [
        generate_offer(index)
        for index in range(
            random.randint(
                8,
                14,
            )
        )
    ]

    selected_offer = (
        random.choice(
            offers
        )
    )

    return {
        "title":
            random.choice([
                "Rewards",
                "Offers",
                "Deals & rewards",
            ]),

        "subtitle":
            random.choice([
                "Earn rewards and save with PayPal.",
                "Personalized deals for your next purchase.",
                "Activate offers before you shop.",
            ]),

        "featured":
            generate_featured(),

        "categories":
            CATEGORIES,

        "active_category":
            random.choice([
                "for_you",
                "shopping",
                "food",
            ]),

        "progress":
            generate_reward_progress(),

        "offers":
            offers,

        "selected_offer":
            selected_offer,

        "show_offer_sheet":
            random.random()
            < 0.30,

        "navigation":
            NAVIGATION_ITEMS,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_rewards_data()
    )