from __future__ import annotations

import random

from faker import Faker

from social_media.baemin.generators.media_generator import (
    get_random_avatar,
    get_random_food_image,
)


# ==========================================================
# Faker
# ==========================================================

fake = Faker()


# ==========================================================
# Controlled Pools
# ==========================================================

RESTAURANT_NAMES = [
    "Seoul Chicken Lab",
    "Gangnam Kitchen",
    "Han River Table",
    "Golden Chicken",
    "Daily Seoul",
    "Kitchen 88",
    "Myeongdong House",
]


FILTERS = [
    "All",
    "With photos",
    "5 stars",
    "4 stars",
    "Recent",
]


SORT_OPTIONS = [
    "Most relevant",
    "Newest",
    "Highest rated",
    "Lowest rated",
]


REVIEW_PREFIXES = [
    "Really enjoyed this order.",
    "The food arrived quickly.",
    "Everything was packed well.",
    "This was better than expected.",
    "I order from here quite often.",
    "The portion was generous.",
    "The food was still warm when it arrived.",
]


REVIEW_SUFFIXES = [
    "I would order again.",
    "Highly recommended.",
    "The delivery was also very fast.",
    "The portion size was good.",
    "Overall, I was satisfied.",
    "I will try another menu next time.",
    "Great value for the price.",
]


REPLY_PREFIXES = [
    "Thank you for your review.",
    "Thank you for ordering from us.",
    "We appreciate your kind feedback.",
    "Thank you for choosing our restaurant.",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_review_text() -> str:

    middle = fake.sentence(
        nb_words=random.randint(
            8,
            20,
        )
    )

    parts = [
        random.choice(
            REVIEW_PREFIXES
        ),
        middle,
    ]

    if random.random() < 0.75:

        parts.append(
            random.choice(
                REVIEW_SUFFIXES
            )
        )

    return " ".join(
        parts
    )


def generate_restaurant_reply() -> str:

    return (
        f"{random.choice(REPLY_PREFIXES)} "
        f"{fake.sentence(nb_words=random.randint(7, 15))}"
    )


# ==========================================================
# Review
# ==========================================================

def generate_review(
    index: int,
) -> dict:

    rating = random.choices(
        population=[
            5,
            4,
            3,
            2,
            1,
        ],
        weights=[
            62,
            24,
            9,
            3,
            2,
        ],
        k=1,
    )[0]

    photo_count = random.choices(
        population=[
            0,
            1,
            2,
            3,
        ],
        weights=[
            46,
            29,
            18,
            7,
        ],
        k=1,
    )[0]

    photos = [
        get_random_food_image()

        for _ in range(
            photo_count
        )
    ]

    photos = [
        photo
        for photo in photos
        if photo
    ]

    has_reply = (
        random.random()
        < 0.34
    )

    menu_count = random.randint(
        1,
        3,
    )

    menu_names = [

        random.choice(
            [
                "Original Fried Chicken",
                "Spicy Garlic Chicken",
                "Cheese Fries",
                "Beef Rice Bowl",
                "Kimchi Fried Rice",
                "Tteokbokki",
                "Coke",
                "Pork Cutlet",
            ]
        )

        for _ in range(
            menu_count
        )
    ]

    return {

        "id":
            index,

        "reviewer": {
            "name":
                fake.name(),

            "avatar":
                (
                    get_random_avatar()
                    if random.random() < 0.78
                    else None
                ),
        },

        "rating":
            rating,

        "date":
            fake.date_between(
                start_date="-8M",
                end_date="today",
            ).strftime(
                "%b %d, %Y"
            ),

        "timestamp":
            fake.date_time_between(
                start_date="-30d",
                end_date="now",
            ).strftime(
                "%m/%d %H:%M"
            ),

        "text":
            generate_review_text(),

        "photos":
            photos,

        "has_photos":
            bool(
                photos
            ),

        "menu_names":
            menu_names,

        "helpful_count":
            random.randint(
                0,
                240,
            ),

        "helpful":
            random.random()
            < 0.12,

        "restaurant_reply":
            (
                generate_restaurant_reply()
                if has_reply
                else None
            ),

        "reply_date":
            (
                fake.date_between(
                    start_date="-6M",
                    end_date="today",
                ).strftime(
                    "%b %d"
                )
                if has_reply
                else None
            ),
    }


# ==========================================================
# Rating Distribution
# ==========================================================

def generate_rating_distribution() -> dict:

    weights = {
        5: random.randint(55, 75),
        4: random.randint(15, 28),
        3: random.randint(4, 12),
        2: random.randint(1, 5),
        1: random.randint(1, 4),
    }

    total = sum(
        weights.values()
    )

    return {

        str(star): round(
            value
            / total
            * 100,
            1,
        )

        for star, value
        in weights.items()
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_reviews_data() -> dict:

    review_count = random.randint(
        12,
        26,
    )

    reviews = [

        generate_review(
            index
        )

        for index in range(
            review_count
        )
    ]

    photo_reviews = [

        photo

        for review in reviews
        for photo in review[
            "photos"
        ]
    ]

    # Ensure some gallery content.
    while len(
        photo_reviews
    ) < 6:

        image = (
            get_random_food_image()
        )

        if image:

            photo_reviews.append(
                image
            )

        else:

            break

    overall_rating = round(
        random.uniform(
            4.3,
            4.9,
        ),
        1,
    )

    return {

        "restaurant": {
            "name":
                random.choice(
                    RESTAURANT_NAMES
                ),
        },

        "overall_rating":
            overall_rating,

        "total_reviews":
            random.randint(
                1500,
                28000,
            ),

        "rating_distribution":
            generate_rating_distribution(),

        "reviews":
            reviews,

        "photo_reviews":
            photo_reviews[:10],

        "filters":
            FILTERS,

        "selected_filter":
            random.choice(
                FILTERS
            ),

        "sort_options":
            SORT_OPTIONS,

        "selected_sort":
            random.choice(
                SORT_OPTIONS
            ),
    }