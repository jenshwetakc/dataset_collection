from __future__ import annotations

import random

from faker import Faker

from social_media.tinder.generators.media_generator import (
    get_random_profile_image,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

DISCOVER_STATES = [

    "ready",
    "loading",
    "empty",
    "location_required",
    "network_error",
    "profile_paused",

]


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
]


JOBS = [
    "Product Designer",
    "Software Engineer",
    "Graduate Student",
    "Photographer",
    "UX Researcher",
    "Marketing Manager",
]


BIOS = [
    "Coffee, weekend adventures, and spontaneous trips.",
    "Probably planning my next vacation.",
    "Looking for someone who enjoys good food and good conversations.",
    "Photography, hiking, and way too many playlists.",
]


INTERESTS = [
    "Travel",
    "Coffee",
    "Photography",
    "Hiking",
    "Music",
    "Movies",
    "Dogs",
    "Fitness",
    "Foodie",
    "Gaming",
]


# ==========================================================
# Profile
# ==========================================================

def generate_profile() -> dict:

    photo_count = random.randint(
        2,
        5,
    )

    return {

        "id":
            fake.uuid4(),

        "name":
            random.choice(
                NAMES
            ),

        "age":
            random.randint(
                20,
                38,
            ),

        "job":
            random.choice(
                JOBS
            ),

        "bio":
            random.choice(
                BIOS
            ),

        "verified":
            random.random() < 0.45,

        "online":
            random.random() < 0.30,

        "distance_km":
            random.randint(
                1,
                18,
            ),

        "interests":
            random.sample(
                INTERESTS,
                k=random.randint(
                    3,
                    5,
                ),
            ),

        "photos": [

            {
                "src":
                    get_random_profile_image(),
            }

            for _ in range(
                photo_count
            )
        ],
    }


# ==========================================================
# State Content
# ==========================================================

def generate_state_content(
    state: str,
) -> dict:

    if state == "loading":

        return {

            "title":
                "Finding people near you",

            "description":
                "Checking for new profiles that match your preferences.",

            "icon":
                "local_fire_department",
        }


    if state == "empty":

        return {

            "title":
                "You've seen everyone nearby",

            "description":
                "Change your discovery preferences or check back later for new people.",

            "icon":
                "person_search",
        }


    if state == "location_required":

        return {

            "title":
                "Turn on location",

            "description":
                "Tinder needs your location to show people near you.",

            "icon":
                "location_off",
        }


    if state == "network_error":

        return {

            "title":
                "Something went wrong",

            "description":
                "We couldn't load new profiles. Check your connection and try again.",

            "icon":
                "wifi_off",
        }


    if state == "profile_paused":

        return {

            "title":
                "Discovery is paused",

            "description":
                "Your profile isn't being shown to new people while Discovery is paused.",

            "icon":
                "pause_circle",
        }


    return {}


# ==========================================================
# Generator
# ==========================================================

def generate_discover_states_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            DISCOVER_STATES
        )


    if state not in DISCOVER_STATES:

        raise ValueError(
            f"Unsupported discover state: {state}"
        )


    return {

        "state":
            state,

        "profile":
            (
                generate_profile()
                if state == "ready"
                else None
            ),

        "state_content":
            generate_state_content(
                state
            ),

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
                "icon": "replay",
                "semantic": "rewind",
                "tone": "rewind",
                "size": "small",
            },

            {
                "icon": "close",
                "semantic": "nope",
                "tone": "nope",
                "size": "large",
            },

            {
                "icon": "star",
                "semantic": "super_like",
                "tone": "super-like",
                "size": "medium",
            },

            {
                "icon": "favorite",
                "semantic": "like",
                "tone": "like",
                "size": "large",
            },

            {
                "icon": "bolt",
                "semantic": "boost",
                "tone": "boost",
                "size": "small",
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    for state in DISCOVER_STATES:

        print(
            "\n================================="
        )

        print(
            state.upper()
        )

        print(
            "================================="
        )

        pprint.pp(
            generate_discover_states_data(
                state
            )
        )