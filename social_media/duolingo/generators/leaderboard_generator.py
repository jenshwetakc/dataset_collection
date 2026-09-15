from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

LEAGUES = [
    "Bronze League",
    "Silver League",
    "Gold League",
    "Sapphire League",
    "Ruby League",
    "Emerald League",
    "Amethyst League",
    "Pearl League",
    "Obsidian League",
    "Diamond League",
]


LEAGUE_ICONS = [
    "shield",
    "military_tech",
    "workspace_premium",
    "diamond",
]


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
# Generate Player
# ==========================================================

def generate_player(
    rank: int,
    is_user: bool = False,
) -> dict:

    xp = random.randint(
        180,
        4200,
    )

    return {
        "rank":
            rank,

        "name":
            (
                "You"
                if is_user
                else fake.first_name()
            ),

        "avatar":
            get_random_avatar(),

        "xp":
            xp,

        "streak":
            random.randint(
                0,
                180,
            ),

        "is_user":
            is_user,

        "movement":
            random.choice(
                [
                    "up",
                    "down",
                    "same",
                    "same",
                ]
            ),

        "movement_value":
            random.randint(
                1,
                4,
            ),
    }


# ==========================================================
# Generate Leaderboard
# ==========================================================

def generate_leaderboard_data() -> dict:

    player_count = random.randint(
        15,
        22,
    )

    user_rank = random.randint(
        4,
        min(
            player_count,
            14,
        )
    )


    players = []

    for rank in range(
        1,
        player_count + 1,
    ):

        players.append(
            generate_player(
                rank=rank,
                is_user=(
                    rank
                    == user_rank
                ),
            )
        )


    # Higher ranked users need higher XP.
    base_xp = random.randint(
        2600,
        4500,
    )

    for index, player in enumerate(
        players
    ):

        player["xp"] = max(
            100,
            base_xp
            - index
            * random.randint(
                100,
                240,
            )
            + random.randint(
                -80,
                80,
            )
        )


    top_three = players[:3]

    remaining_players = players[3:]


    selected_tab = random.choice(
        [
            "league",
            "friends",
        ]
    )


    navigation_items = []

    for item in NAVIGATION_ITEMS:

        navigation_items.append(
            {
                **item,

                "selected":
                    item["key"]
                    == "leaderboard",
            }
        )


    promotion_cutoff = random.choice(
        [
            7,
            10,
        ]
    )

    demotion_cutoff = max(
        promotion_cutoff + 5,
        player_count - 4,
    )


    return {

        "league": {

            "name":
                random.choice(
                    LEAGUES
                ),

            "icon":
                random.choice(
                    LEAGUE_ICONS
                ),

            "week":
                random.randint(
                    1,
                    8,
                ),
        },


        "countdown": {

            "hours":
                random.randint(
                    0,
                    23,
                ),

            "minutes":
                random.randint(
                    0,
                    59,
                ),
        },


        "selected_tab":
            selected_tab,


        "tabs": [
            {
                "key":
                    "league",

                "label":
                    "League",

                "selected":
                    selected_tab
                    == "league",
            },
            {
                "key":
                    "friends",

                "label":
                    "Friends",

                "selected":
                    selected_tab
                    == "friends",
            },
        ],


        "top_three":
            top_three,


        "players":
            remaining_players,


        "promotion_cutoff":
            promotion_cutoff,


        "demotion_cutoff":
            demotion_cutoff,


        "navigation_items":
            navigation_items,


        "stats": {

            "streak":
                random.randint(
                    1,
                    250,
                ),

            "gems":
                random.randint(
                    100,
                    5000,
                ),

            "hearts":
                random.randint(
                    1,
                    5,
                ),
        },


        "message":
            random.choice(
                [
                    "Top learners advance to the next league.",
                    "Keep earning XP to move up the rankings.",
                    "Stay above the demotion zone this week.",
                ]
            ),
    }