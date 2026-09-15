from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_reward,
)


fake = Faker()


# ==========================================================
# Navigation
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "key": "learn",
        "label": "Learn",
        "icon": "home",
    },
    {
        "key": "practice",
        "label": "Practice",
        "icon": "fitness_center",
    },
    {
        "key": "leaderboard",
        "label": "Leaderboards",
        "icon": "trophy",
    },
    {
        "key": "quests",
        "label": "Quests",
        "icon": "task_alt",
    },
    {
        "key": "shop",
        "label": "Shop",
        "icon": "storefront",
    },
    {
        "key": "profile",
        "label": "Profile",
        "icon": "person",
    },
]


# ==========================================================
# Shop Item Templates
# ==========================================================

SHOP_ITEM_TEMPLATES = [
    {
        "title": "Streak Freeze",
        "description":
            "Protect your streak if you miss a day.",
        "icon": "ac_unit",
        "prices": [100, 150, 200],
        "type": "utility",
    },
    {
        "title": "Double XP Boost",
        "description":
            "Earn twice the XP for a limited time.",
        "icon": "bolt",
        "prices": [250, 300, 350],
        "type": "boost",
    },
    {
        "title": "Heart Refill",
        "description":
            "Refill your hearts and keep learning.",
        "icon": "favorite",
        "prices": [150, 200, 250],
        "type": "hearts",
    },
    {
        "title": "Timer Boost",
        "description":
            "Get extra time in timed challenges.",
        "icon": "timer",
        "prices": [120, 180, 220],
        "type": "boost",
    },
    {
        "title": "Perfect Lesson Boost",
        "description":
            "Increase rewards from perfect lessons.",
        "icon": "verified",
        "prices": [300, 400, 500],
        "type": "boost",
    },
    {
        "title": "Quest Chest",
        "description":
            "Open a chest filled with random rewards.",
        "icon": "inventory_2",
        "prices": [180, 240, 320],
        "type": "reward",
    },
]


# ==========================================================
# Featured Offer Templates
# ==========================================================

FEATURED_OFFERS = [
    {
        "title": "Super Learner Bundle",
        "description":
            "Get boosts, streak protection, and bonus gems.",
        "icon": "workspace_premium",
    },
    {
        "title": "Weekend Boost Pack",
        "description":
            "Boost your XP and finish more lessons this weekend.",
        "icon": "rocket_launch",
    },
    {
        "title": "Streak Saver Pack",
        "description":
            "Stay protected with extra streak freezes.",
        "icon": "local_fire_department",
    },
]


# ==========================================================
# Generate Shop Item
# ==========================================================

def generate_shop_item(
    index: int,
) -> dict:

    template = random.choice(
        SHOP_ITEM_TEMPLATES
    )

    owned = random.randint(
        0,
        4,
    )

    max_owned = random.choice(
        [
            3,
            5,
            10,
        ]
    )

    sold_out = (
        owned >= max_owned
    )

    return {
        "id":
            f"shop_item_{index + 1}",

        "title":
            template["title"],

        "description":
            template["description"],

        "icon":
            template["icon"],

        "image":
            get_random_reward(),

        "price":
            random.choice(
                template["prices"]
            ),

        "type":
            template["type"],

        "owned":
            owned,

        "max_owned":
            max_owned,

        "sold_out":
            sold_out,

        "popular":
            random.random()
            < 0.25,
    }


# ==========================================================
# Generate Featured Offer
# ==========================================================

def generate_featured_offer() -> dict:

    offer = random.choice(
        FEATURED_OFFERS
    )

    return {
        "title":
            offer["title"],

        "description":
            offer["description"],

        "icon":
            offer["icon"],

        "image":
            get_random_reward(),

        "price":
            random.choice(
                [
                    450,
                    600,
                    750,
                    1000,
                ]
            ),

        "original_price":
            random.choice(
                [
                    900,
                    1200,
                    1500,
                ]
            ),

        "discount":
            random.choice(
                [
                    20,
                    25,
                    30,
                    40,
                ]
            ),
    }


# ==========================================================
# Generate Shop Data
# ==========================================================

def generate_shop_data() -> dict:

    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,

                "selected":
                    item["key"]
                    == "shop",
            }
        )

    item_count = random.randint(
        5,
        8,
    )

    return {
        "balance": {
            "gems":
                random.randint(
                    100,
                    6000,
                ),

            "hearts":
                random.randint(
                    1,
                    5,
                ),

            "streak":
                random.randint(
                    1,
                    400,
                ),
        },

        "featured_offer":
            generate_featured_offer(),

        "items": [
            generate_shop_item(
                index
            )
            for index in range(
                item_count
            )
        ],

        "subscription": {
            "title":
                random.choice(
                    [
                        "Super Duolingo",
                        "Premium Learning",
                        "Unlimited Practice",
                    ]
                ),

            "description":
                random.choice(
                    [
                        "Unlimited hearts and no interruptions.",
                        "Practice freely and unlock extra features.",
                        "Learn without limits and earn more rewards.",
                    ]
                ),

            "price":
                random.choice(
                    [
                        "$6.99 / month",
                        "$8.99 / month",
                        "$59.99 / year",
                    ]
                ),

            "trial":
                random.choice(
                    [
                        "Try free for 7 days",
                        "Start free trial",
                        "Try premium",
                    ]
                ),
        },

        "navigation_items":
            navigation_items,
    }