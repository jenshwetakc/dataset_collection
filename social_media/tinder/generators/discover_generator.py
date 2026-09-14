from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_avatar,
    get_random_profile_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

FIRST_NAMES = [
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
    "Amelia",
    "Ella",
    "Isabella",
    "Aria",
    "Chloe",
    "Zoe",
    "Lucy",
    "Grace",
]


JOBS = [
    "Product designer",
    "Graduate student",
    "Software engineer",
    "Photographer",
    "Marketing manager",
    "Architect",
    "UX researcher",
    "Data analyst",
    "Graphic designer",
    "Teacher",
    "Barista",
    "Fitness coach",
    "Research assistant",
    "Content creator",
    "Fashion designer",
]


SCHOOLS = [
    "Korea University",
    "Yonsei University",
    "Seoul National University",
    "Hanyang University",
    "Sungkyunkwan University",
    "Ewha Womans University",
    "KAIST",
    "Hongik University",
]


INTERESTS = [
    "Travel",
    "Coffee",
    "Photography",
    "Hiking",
    "Running",
    "Movies",
    "Music",
    "Cooking",
    "Dogs",
    "Cats",
    "K-pop",
    "Fitness",
    "Books",
    "Gaming",
    "Museums",
    "Camping",
    "Dancing",
    "Yoga",
    "Art",
    "Foodie",
    "Cycling",
    "Beach",
]


BIO_LINES = [
    "Looking for someone to explore the city with.",
    "Coffee first, adventures second.",
    "Always planning my next trip.",
    "Probably at a cafe or taking photos.",
    "I know the best hidden restaurants.",
    "Weekend hikes and late-night movies.",
    "Let's find a new place to eat.",
    "Dog person with questionable music taste.",
    "Trying every cafe in Seoul.",
    "Here for good conversations and good food.",
]


LOCATIONS = [
    "Seoul",
    "Hongdae",
    "Gangnam",
    "Itaewon",
    "Sinchon",
    "Mapo",
    "Seongsu",
    "Jamsil",
    "Yeonnam",
    "Hannam",
]


# ==========================================================
# Photo
# ==========================================================

def generate_photo() -> dict:

    return {

        "src":
            get_random_profile_image(),

        "alt":
            "Profile photo",
    }


# ==========================================================
# Profile
# ==========================================================

def generate_profile() -> dict:

    name = random.choice(
        FIRST_NAMES
    )

    age = random.randint(
        20,
        38,
    )

    photo_count = random.randint(
        2,
        5,
    )

    photos = [

        generate_photo()

        for _ in range(
            photo_count
        )
    ]

    distance = random.choice([
        1,
        2,
        3,
        4,
        5,
        7,
        9,
        12,
        15,
        18,
        24,
    ])

    verified = (
        random.random()
        < 0.48
    )

    online = (
        random.random()
        < 0.28
    )

    job = random.choice(
        JOBS
    )

    school = (
        random.choice(
            SCHOOLS
        )
        if random.random() < 0.68
        else None
    )

    interests = random.sample(
        INTERESTS,
        k=random.randint(
            3,
            5,
        ),
    )

    return {

        "id":
            fake.uuid4(),

        "name":
            name,

        "age":
            age,

        "verified":
            verified,

        "online":
            online,

        "job":
            job,

        "school":
            school,

        "bio":
            random.choice(
                BIO_LINES
            ),

        "location":
            random.choice(
                LOCATIONS
            ),

        "distance_km":
            distance,

        "interests":
            interests,

        "photos":
            photos,

        "active_photo":
            0,
    }


# ==========================================================
# Match
# ==========================================================

def generate_match() -> dict:

    name = random.choice(
        FIRST_NAMES
    )

    return {

        "id":
            fake.uuid4(),

        "name":
            name,

        "avatar":
            get_random_avatar(),

        "new":
            random.random() < 0.35,

        "message":
            random.choice([
                "Hey 👋",
                "How's your day going?",
                "That place looks amazing!",
                "Coffee sometime?",
                "Haha exactly 😄",
                "Nice to meet you!",
                "What are you doing this weekend?",
                "I love that too!",
            ]),

        "time":
            random.choice([
                "Now",
                "2m",
                "8m",
                "21m",
                "1h",
                "3h",
                "Yesterday",
            ]),
    }


# ==========================================================
# Discover Generator
# ==========================================================

def generate_discover_data() -> dict:

    current_profile = (
        generate_profile()
    )

    stacked_profiles = [

        generate_profile()
        for _ in range(
            2
        )
    ]

    matches = [

        generate_match()

        for _ in range(
            random.randint(
                5,
                10,
            )
        )
    ]

    recent_matches = [

        generate_match()

        for _ in range(
            random.randint(
                4,
                7,
            )
        )
    ]

    return {

        "app_name":
            "tinder",

        "page_title":
            "Discover",

        "current_profile":
            current_profile,

        "stacked_profiles":
            stacked_profiles,

        "matches":
            matches,

        "recent_matches":
            recent_matches,

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

        "actions": [

            {
                "semantic": "rewind",
                "icon": "replay",
                "label": "Rewind",
                "size": "small",
                "tone": "rewind",
            },

            {
                "semantic": "nope",
                "icon": "close",
                "label": "Nope",
                "size": "large",
                "tone": "nope",
            },

            {
                "semantic": "super_like",
                "icon": "star",
                "label": "Super Like",
                "size": "medium",
                "tone": "super-like",
            },

            {
                "semantic": "like",
                "icon": "favorite",
                "label": "Like",
                "size": "large",
                "tone": "like",
            },

            {
                "semantic": "boost",
                "icon": "bolt",
                "label": "Boost",
                "size": "small",
                "tone": "boost",
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_discover_data()
    )