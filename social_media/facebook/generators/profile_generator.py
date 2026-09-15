# social_media/facebook/generators/profile_generator.py

from __future__ import annotations

import random

from faker import Faker

from social_media.facebook.generators.media_generator import (
    get_random_avatar,
    get_random_cover_image,
    get_random_post_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

PROFILE_STATES = [
    "default",
    "default",
    "about_open",
    "friends_tab",
    "photos_tab",
    "edit_profile",
    "cover_menu_open",
    "avatar_preview",
    "post_menu_open",
]


PROFILE_TABS = [
    "Posts",
    "About",
    "Friends",
    "Photos",
    "Videos",
]


INTRO_ICONS = [
    "work",
    "school",
    "home",
    "location_on",
    "favorite",
]


POST_TEXTS = [
    "A few memories from this week.",
    "Beautiful day outside.",
    "Another great weekend.",
    "Sharing some recent photos.",
    "Good times with good people.",
    "Enjoying the little moments.",
]


# ==========================================================
# Profile User
# ==========================================================

def generate_profile_user() -> dict:

    return {
        "name":
            fake.name(),

        "username":
            fake.user_name(),

        "avatar":
            get_random_avatar(),

        "cover":
            get_random_cover_image(),

        "bio":
            fake.sentence(
                nb_words=random.randint(
                    6,
                    12,
                )
            ),

        "friend_count":
            random.randint(
                120,
                4900,
            ),

        "location":
            fake.city(),

        "work":
            fake.company(),

        "school":
            fake.company(),

        "relationship":
            random.choice(
                [
                    "Single",
                    "In a relationship",
                    "Married",
                    "It's complicated",
                ]
            ),
    }


# ==========================================================
# Intro
# ==========================================================

def generate_intro(
    profile: dict,
) -> list[dict]:

    return [
        {
            "icon":
                "work",

            "text":
                f"Works at {profile['work']}",
        },
        {
            "icon":
                "school",

            "text":
                f"Studied at {profile['school']}",
        },
        {
            "icon":
                "home",

            "text":
                f"Lives in {profile['location']}",
        },
        {
            "icon":
                "favorite",

            "text":
                profile["relationship"],
        },
    ]


# ==========================================================
# Friend
# ==========================================================

def generate_friend(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),
    }


def generate_friends(
    count: int = 9,
) -> list[dict]:

    return [
        generate_friend(index)
        for index in range(count)
    ]


# ==========================================================
# Photos
# ==========================================================

def generate_photos(
    count: int = 12,
) -> list[dict]:

    photos = []

    for index in range(count):

        photos.append(
            {
                "id":
                    index,

                "image":
                    get_random_post_image(),
            }
        )

    return photos


# ==========================================================
# Post
# ==========================================================

def generate_post(
    index: int,
    profile: dict,
) -> dict:

    has_image = (
        random.random()
        < 0.78
    )

    return {
        "id":
            index,

        "author":
            profile["name"],

        "avatar":
            profile["avatar"],

        "timestamp":
            random.choice(
                [
                    "Just now",
                    "2 h",
                    "Yesterday",
                    "2 days ago",
                    "Last week",
                ]
            ),

        "text":
            random.choice(
                POST_TEXTS
            ),

        "image":
            (
                get_random_post_image()
                if has_image
                else None
            ),

        "reactions":
            random.randint(
                5,
                1800,
            ),

        "comments":
            random.randint(
                0,
                250,
            ),
    }


def generate_posts(
    profile: dict,
    count: int = 6,
) -> list[dict]:

    return [
        generate_post(
            index,
            profile,
        )
        for index in range(count)
    ]


# ==========================================================
# Edit Data
# ==========================================================

def generate_edit_profile_data(
    profile: dict,
) -> dict:

    return {
        "bio":
            profile["bio"],

        "work":
            profile["work"],

        "school":
            profile["school"],

        "location":
            profile["location"],
    }


# ==========================================================
# State
# ==========================================================

def generate_profile_state(
    post_count: int,
) -> dict:

    name = random.choice(
        PROFILE_STATES
    )

    selected_post = None

    if name == "post_menu_open":

        selected_post = random.randint(
            0,
            max(
                0,
                min(
                    post_count - 1,
                    3,
                )
            ),
        )

    return {
        "name":
            name,

        "selected_post":
            selected_post,
    }


# ==========================================================
# Complete Profile Data
# ==========================================================

def generate_profile_data() -> dict:

    profile = generate_profile_user()

    posts = generate_posts(
        profile=profile,
        count=random.randint(
            5,
            8,
        ),
    )

    return {
        "profile":
            profile,

        "intro":
            generate_intro(
                profile
            ),

        "friends":
            generate_friends(
                count=9
            ),

        "photos":
            generate_photos(
                count=12
            ),

        "posts":
            posts,

        "edit":
            generate_edit_profile_data(
                profile
            ),

        "tabs":
            PROFILE_TABS,

        "state":
            generate_profile_state(
                post_count=len(posts)
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_profile_data()

    print(
        "\n"
        "=========================================="
    )

    print(
        "FACEBOOK PROFILE GENERATOR DEBUG"
    )

    print(
        "=========================================="
    )

    print(
        "Profile:",
        data["profile"]["name"],
    )

    print(
        "Friends:",
        len(
            data["friends"]
        ),
    )

    print(
        "Photos:",
        len(
            data["photos"]
        ),
    )

    print(
        "Posts:",
        len(
            data["posts"]
        ),
    )

    print(
        "State:",
        data["state"],
    )