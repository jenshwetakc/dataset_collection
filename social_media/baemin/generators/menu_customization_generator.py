from __future__ import annotations

import random

from faker import Faker

from social_media.baemin.generators.media_generator import (
    get_random_food_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Controlled Pools
# ==========================================================

FOOD_NAMES = [
    "Spicy Garlic Chicken",
    "Original Fried Chicken",
    "Cheese Chicken",
    "Beef Rice Bowl",
    "Pork Cutlet",
    "Cream Pasta",
    "Seafood Noodles",
    "Tteokbokki",
    "Double Burger",
    "Cheese Pizza",
]


RESTAURANT_SUFFIXES = [
    "Kitchen",
    "Chicken",
    "Table",
    "House",
    "Bistro",
    "Cafe",
    "Grill",
]


SIZE_OPTIONS = [
    ("Regular", 0),
    ("Large", 3000),
    ("Family", 7000),
]


SPICE_OPTIONS = [
    ("Mild", 0),
    ("Medium", 0),
    ("Spicy", 0),
    ("Extra spicy", 500),
]


ADDON_POOL = [
    ("Extra cheese", 1500),
    ("Extra sauce", 700),
    ("French fries", 2500),
    ("Coleslaw", 1500),
    ("Pickles", 500),
    ("Rice", 2000),
    ("Fried egg", 1000),
    ("Soft drink", 2000),
    ("Corn cheese", 2500),
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    value: int,
) -> str:

    if value == 0:
        return "Free"

    return f"₩{value:,}"


def generate_restaurant_name() -> str:

    prefix = random.choice(
        [
            fake.first_name(),
            fake.last_name(),
            fake.city().split()[0],
            "Seoul",
            "Daily",
            "Golden",
            "Happy",
            "Fresh",
        ]
    )

    return (
        f"{prefix} "
        f"{random.choice(RESTAURANT_SUFFIXES)}"
    )


# ==========================================================
# Radio Group
# ==========================================================

def generate_radio_options(
    pool: list[tuple[str, int]],
) -> list[dict]:

    selected_index = random.randrange(
        len(pool)
    )

    return [
        {
            "id":
                index,

            "label":
                label,

            "extra_price":
                price,

            "extra_price_text":
                (
                    f"+{format_price(price)}"
                    if price > 0
                    else ""
                ),

            "selected":
                index == selected_index,
        }

        for index, (
            label,
            price,
        )
        in enumerate(
            pool
        )
    ]


# ==========================================================
# Add-ons
# ==========================================================

def generate_addons() -> list[dict]:

    selected = random.sample(
        ADDON_POOL,
        k=random.randint(
            5,
            min(
                8,
                len(
                    ADDON_POOL
                ),
            ),
        ),
    )

    return [
        {
            "id":
                index,

            "label":
                label,

            "price":
                price,

            "price_text":
                f"+₩{price:,}",

            "selected":
                random.random()
                < 0.28,
        }

        for index, (
            label,
            price,
        )
        in enumerate(
            selected
        )
    ]


# ==========================================================
# Generator
# ==========================================================

def generate_menu_customization_data() -> dict:

    base_price = random.randrange(
        8000,
        24000,
        500,
    )

    quantity = random.randint(
        1,
        3,
    )

    size_options = (
        generate_radio_options(
            SIZE_OPTIONS
        )
    )

    spice_options = (
        generate_radio_options(
            SPICE_OPTIONS
        )
    )

    addons = (
        generate_addons()
    )

    size_extra = sum(
        option["extra_price"]

        for option in size_options

        if option[
            "selected"
        ]
    )

    spice_extra = sum(
        option["extra_price"]

        for option in spice_options

        if option[
            "selected"
        ]
    )

    addon_extra = sum(
        addon["price"]

        for addon in addons

        if addon[
            "selected"
        ]
    )

    total_price = (
        base_price
        + size_extra
        + spice_extra
        + addon_extra
    ) * quantity

    return {

        # ==================================================
        # Background Restaurant Context
        # ==================================================

        "background": {

            "restaurant_name":
                generate_restaurant_name(),

            "menu_items": [
                {
                    "name":
                        random.choice(
                            FOOD_NAMES
                        ),

                    "price":
                        f"₩{random.randrange(7000, 25000, 500):,}",

                    "image":
                        get_random_food_image(),
                }

                for _ in range(
                    random.randint(
                        5,
                        8,
                    )
                )
            ],
        },


        # ==================================================
        # Selected Food
        # ==================================================

        "food": {

            "name":
                random.choice(
                    FOOD_NAMES
                ),

            "description":
                fake.sentence(
                    nb_words=random.randint(
                        8,
                        18,
                    )
                ),

            "image":
                get_random_food_image(),

            "base_price":
                base_price,

            "base_price_text":
                f"₩{base_price:,}",
        },


        # ==================================================
        # Choice Groups
        # ==================================================

        "size_group": {
            "title":
                random.choice(
                    [
                        "Choose a size",
                        "Select portion size",
                    ]
                ),

            "required":
                True,

            "options":
                size_options,
        },

        "spice_group": {
            "title":
                random.choice(
                    [
                        "Spice level",
                        "Choose your spice level",
                    ]
                ),

            "required":
                True,

            "options":
                spice_options,
        },


        # ==================================================
        # Add-ons
        # ==================================================

        "addons": {
            "title":
                random.choice(
                    [
                        "Add extras",
                        "Optional add-ons",
                        "Make it your way",
                    ]
                ),

            "required":
                False,

            "options":
                addons,
        },


        # ==================================================
        # Notes
        # ==================================================

        "notes": {

            "placeholder":
                random.choice(
                    [
                        "Add a request for the restaurant",
                        "Any special instructions?",
                        "Write a note for the restaurant",
                    ]
                ),

            "value":
                random.choice(
                    [
                        "",
                        "",
                        "Please make it less salty.",
                        "Please include extra napkins.",
                        "No onions, please.",
                        fake.sentence(
                            nb_words=random.randint(
                                4,
                                8,
                            )
                        ),
                    ]
                ),
        },


        # ==================================================
        # Quantity
        # ==================================================

        "quantity":
            quantity,


        # ==================================================
        # Total
        # ==================================================

        "total_price":
            total_price,

        "total_price_text":
            f"₩{total_price:,}",
    }