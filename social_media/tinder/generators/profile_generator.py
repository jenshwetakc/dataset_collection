from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_profile_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

NAMES = [
    "Mina",
    "Sofia",
    "Emma",
    "Yuna",
    "Hana",
    "Olivia",
    "Ava",
    "Maya",
    "Nina",
    "Lena",
    "Ella",
    "Grace",
    "Aria",
    "Chloe",
]


JOBS = [
    "Product designer",
    "Graduate student",
    "Software engineer",
    "UX researcher",
    "Photographer",
    "Architect",
    "Marketing manager",
    "Data analyst",
    "Content creator",
    "Teacher",
    "Graphic designer",
    "Research assistant",
]


SCHOOLS = [
    "Korea University",
    "Yonsei University",
    "Seoul National University",
    "Hongik University",
    "Hanyang University",
    "KAIST",
    "Sungkyunkwan University",
]


INTERESTS = [
    "Coffee",
    "Travel",
    "Photography",
    "Hiking",
    "Running",
    "Dogs",
    "Cats",
    "K-pop",
    "Movies",
    "Music",
    "Cooking",
    "Gaming",
    "Books",
    "Art",
    "Museums",
    "Fitness",
    "Camping",
    "Foodie",
    "Beach",
    "Cycling",
]


ZODIAC = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


EDUCATION = [
    "Bachelor's degree",
    "Master's student",
    "Graduate degree",
    "University student",
]


COMMUNICATION = [
    "Texting",
    "Phone calls",
    "Video chat",
    "Better in person",
]


LOVE_STYLES = [
    "Quality time",
    "Acts of service",
    "Words of affirmation",
    "Physical touch",
    "Gifts",
]


DRINKING = [
    "Socially",
    "On special occasions",
    "Rarely",
    "Never",
]


SMOKING = [
    "Never",
    "Socially",
    "Trying to quit",
]


WORKOUT = [
    "Often",
    "Sometimes",
    "Every day",
    "Rarely",
]


BIO_TEXTS = [
    "Weekend explorer, coffee enthusiast, and always looking for a new restaurant.",
    "Probably planning my next trip or finding another hidden cafe in Seoul.",
    "I like good conversations, spontaneous plans, and people who can recommend a great movie.",
    "Hiking on Saturday, brunch on Sunday, and way too much coffee in between.",
    "I take too many photos, try every new restaurant, and never say no to a road trip.",
]


LOOKING_FOR = [
    "Long-term partner",
    "Long-term, open to short",
    "New friends",
    "Still figuring it out",
    "Short-term fun",
]


# ==========================================================
# Photo
# ==========================================================

def generate_photo(
    index: int,
) -> dict:

    return {

        "id":
            fake.uuid4(),

        "src":
            get_random_profile_image(),

        "index":
            index,
    }


# ==========================================================
# Lifestyle Item
# ==========================================================

def lifestyle_item(
    icon: str,
    label: str,
    value: str,
) -> dict:

    return {

        "icon":
            icon,

        "label":
            label,

        "value":
            value,
    }


# ==========================================================
# Generator
# ==========================================================

def generate_profile_data() -> dict:

    photo_count = random.randint(
        4,
        7,
    )

    name = random.choice(
        NAMES
    )

    verified = (
        random.random()
        < 0.55
    )

    online = (
        random.random()
        < 0.30
    )

    school = (
        random.choice(
            SCHOOLS
        )
        if random.random() < 0.78
        else None
    )

    job = random.choice(
        JOBS
    )

    return {

        "id":
            fake.uuid4(),

        "name":
            name,

        "age":
            random.randint(
                20,
                38,
            ),

        "verified":
            verified,

        "online":
            online,

        "distance_km":
            random.randint(
                1,
                18,
            ),

        "job":
            job,

        "school":
            school,

        "location":
            random.choice([
                "Seoul",
                "Gangnam",
                "Hongdae",
                "Mapo",
                "Seongsu",
                "Sinchon",
                "Itaewon",
            ]),

        "bio":
            random.choice(
                BIO_TEXTS
            ),

        "looking_for":
            random.choice(
                LOOKING_FOR
            ),

        "interests":
            random.sample(
                INTERESTS,
                k=random.randint(
                    5,
                    8,
                ),
            ),

        "photos": [

            generate_photo(
                index
            )

            for index in range(
                photo_count
            )
        ],

        "active_photo":
            0,

        "basics": [

            lifestyle_item(
                "school",
                "Education",
                random.choice(
                    EDUCATION
                ),
            ),

            lifestyle_item(
                "psychology",
                "Zodiac",
                random.choice(
                    ZODIAC
                ),
            ),

            lifestyle_item(
                "chat",
                "Communication",
                random.choice(
                    COMMUNICATION
                ),
            ),

            lifestyle_item(
                "favorite",
                "Love style",
                random.choice(
                    LOVE_STYLES
                ),
            ),
        ],

        "lifestyle": [

            lifestyle_item(
                "local_bar",
                "Drinking",
                random.choice(
                    DRINKING
                ),
            ),

            lifestyle_item(
                "smoke_free",
                "Smoking",
                random.choice(
                    SMOKING
                ),
            ),

            lifestyle_item(
                "fitness_center",
                "Workout",
                random.choice(
                    WORKOUT
                ),
            ),

            lifestyle_item(
                "pets",
                "Pets",
                random.choice([
                    "Dog",
                    "Cat",
                    "Love pets",
                    "No pets",
                ]),
            ),
        ],

        "navigation": [

            {
                "label": "Discover",
                "icon": "local_fire_department",
                "active": True,
                "semantic": "discover",
            },

            {
                "label": "Explore",
                "icon": "grid_view",
                "active": False,
                "semantic": "explore",
            },

            {
                "label": "Likes",
                "icon": "favorite",
                "active": False,
                "semantic": "likes",
            },

            {
                "label": "Messages",
                "icon": "chat_bubble",
                "active": False,
                "semantic": "messages",
            },

            {
                "label": "Profile",
                "icon": "person",
                "active": False,
                "semantic": "profile",
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_profile_data()
    )