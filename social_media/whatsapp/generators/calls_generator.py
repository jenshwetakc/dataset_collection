import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Time
# ==========================================================

def generate_call_time():

    return random.choice(
        [
            fake.time(
                pattern="%H:%M"
            ),
            "Yesterday",
            "Monday",
            "Tuesday",
        ]
    )


# ==========================================================
# Call Type
# ==========================================================

def generate_call_type():

    return random.choice(
        [
            "voice",
            "video",
        ]
    )


# ==========================================================
# Call Direction
# ==========================================================

def generate_call_direction():

    return random.choices(
        [
            "incoming",
            "outgoing",
            "missed",
        ],
        weights=[
            0.40,
            0.40,
            0.20,
        ],
        k=1,
    )[0]


# ==========================================================
# Recent Call
# ==========================================================

def generate_recent_call():

    direction = (
        generate_call_direction()
    )

    count = random.choices(
        [
            1,
            random.randint(2, 4),
            random.randint(5, 10),
        ],
        weights=[
            0.70,
            0.25,
            0.05,
        ],
        k=1,
    )[0]


    return {

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "direction":
            direction,

        "call_type":
            generate_call_type(),

        "time":
            generate_call_time(),

        "count":
            count,

        "missed":
            direction == "missed",
    }


# ==========================================================
# Favorite Contact
# ==========================================================

def generate_favorite():

    return {

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "call_type":
            generate_call_type(),
    }


# ==========================================================
# Call Link
# ==========================================================

def generate_call_link():

    return {

        "title":
            "Create call link",

        "subtitle":
            "Share a link for your WhatsApp call",

        "show":
            True,
    }


# ==========================================================
# Calls Page
# ==========================================================

def generate_calls_page(
    min_recent_calls: int = 5,
    max_recent_calls: int = 12,
    min_favorites: int = 0,
    max_favorites: int = 4,
):

    recent_call_count = random.randint(
        min_recent_calls,
        max_recent_calls,
    )


    favorite_count = random.randint(
        min_favorites,
        max_favorites,
    )


    recent_calls = [

        generate_recent_call()

        for _ in range(
            recent_call_count
        )
    ]


    favorites = [

        generate_favorite()

        for _ in range(
            favorite_count
        )
    ]


    return {

        "title":
            "Calls",

        "call_link":
            generate_call_link(),

        "favorites":
            favorites,

        "favorite_count":
            favorite_count,

        "recent_calls":
            recent_calls,

        "recent_call_count":
            recent_call_count,

        "selected_navigation":
            "calls",

        "fab": {

            "show":
                True,

            "semantic":
                "new_call_button",
        },
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_calls_page()
    )


    print(
        "\nCALLS PAGE"
    )

    print(
        "Title:",
        page["title"]
    )

    print(
        "Favorites:",
        page["favorite_count"]
    )

    print(
        "Recent calls:",
        page["recent_call_count"]
    )


    print(
        "\nFAVORITES"
    )

    for favorite in page[
        "favorites"
    ]:

        print(
            favorite
        )


    print(
        "\nRECENT CALLS"
    )

    for call in page[
        "recent_calls"
    ]:

        print(
            call
        )