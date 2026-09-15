import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_phone_number():

    return fake.phone_number()


def generate_about():

    return random.choice(
        [
            "Available",
            "Busy",
            "At work",
            "At the gym",
            "Battery about to die",
            "Hey there! I am using WhatsApp.",
            fake.sentence(
                nb_words=random.randint(
                    3,
                    8,
                )
            ),
        ]
    )


def generate_disappearing_message_state():

    return random.choice(
        [
            "Off",
            "24 hours",
            "7 days",
            "90 days",
        ]
    )


# ==========================================================
# Shared Group
# ==========================================================

def generate_shared_group():

    return {

        "name":
            random.choice(
                [
                    fake.catch_phrase(),
                    fake.company(),
                    f"{fake.word().title()} Group",
                ]
            ),

        "avatar":
            get_random_avatar(),

        "members":
            random.randint(
                3,
                256,
            ),

        "description":
            (
                fake.sentence(
                    nb_words=random.randint(
                        3,
                        7,
                    )
                )
                if random.random() < 0.35
                else None
            ),
    }


# ==========================================================
# Media Preview
# ==========================================================

def generate_media_preview(
    min_items=3,
    max_items=6,
):

    count = random.randint(
        min_items,
        max_items,
    )


    return [

        {
            "image":
                get_random_chat_image(),

            "type":
                random.choices(
                    [
                        "image",
                        "video",
                    ],
                    weights=[
                        0.8,
                        0.2,
                    ],
                    k=1,
                )[0],
        }

        for _ in range(
            count
        )
    ]


# ==========================================================
# Contact Info
# ==========================================================

def generate_contact_info_page():

    shared_group_count = random.randint(
        0,
        5,
    )


    shared_groups = [

        generate_shared_group()

        for _ in range(
            shared_group_count
        )
    ]


    media_preview = (
        generate_media_preview()
    )


    media_count = random.randint(
        len(media_preview),
        150,
    )


    return {

        # --------------------------------------------------
        # Contact
        # --------------------------------------------------

        "name":
            fake.name(),

        "phone":
            generate_phone_number(),

        "about":
            generate_about(),

        "avatar":
            get_random_avatar(),

        # --------------------------------------------------
        # Top Actions
        # --------------------------------------------------

        "actions": {

            "message":
                True,

            "voice_call":
                True,

            "video_call":
                True,

            "search":
                True,
        },

        # --------------------------------------------------
        # Media
        # --------------------------------------------------

        "media_preview":
            media_preview,

        "media_count":
            media_count,

        # --------------------------------------------------
        # Settings / Contact State
        # --------------------------------------------------

        "mute_notifications":
            random.random() < 0.35,

        "custom_notifications":
            random.random() < 0.20,

        "media_visibility":
            random.choice(
                [
                    "Default",
                    "Yes",
                    "No",
                ]
            ),

        "disappearing_messages":
            generate_disappearing_message_state(),

        "encryption":
            True,

        # --------------------------------------------------
        # Shared Groups
        # --------------------------------------------------

        "shared_groups":
            shared_groups,

        "shared_group_count":
            shared_group_count,

        # --------------------------------------------------
        # Safety / Destructive Actions
        # --------------------------------------------------

        "blocked":
            random.random() < 0.08,

        "show_block":
            True,

        "show_report":
            True,

        # --------------------------------------------------
        # Misc
        # --------------------------------------------------

        "verified":
            random.random() < 0.08,

        "business":
            random.random() < 0.12,
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_contact_info_page()
    )


    print(
        "\nCONTACT INFO"
    )

    print(
        "Name:",
        page["name"]
    )

    print(
        "Phone:",
        page["phone"]
    )

    print(
        "About:",
        page["about"]
    )

    print(
        "Avatar:",
        page["avatar"] is not None
    )

    print(
        "Media:",
        page["media_count"]
    )

    print(
        "Shared groups:",
        page["shared_group_count"]
    )

    print(
        "Mute:",
        page["mute_notifications"]
    )

    print(
        "Disappearing messages:",
        page["disappearing_messages"]
    )

    print(
        "Blocked:",
        page["blocked"]
    )