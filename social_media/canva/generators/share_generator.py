from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_photo,
)


fake = Faker()


PERMISSIONS = [
    "Can edit",
    "Can comment",
    "Can view",
]


SHARE_TABS = [
    "People",
    "Link",
]


def generate_collaborators(
    count: int | None = None,
) -> list[dict]:

    if count is None:
        count = random.randint(
            3,
            7,
        )

    collaborators = []

    for index in range(count):

        name = fake.name()

        collaborators.append(
            {
                "id":
                    index,

                "name":
                    name,

                "email":
                    fake.email(),

                "avatar":
                    get_random_avatar(),

                "permission":
                    random.choice(
                        PERMISSIONS
                    ),

                "owner":
                    index == 0,

                "online":
                    random.random() < 0.35,
            }
        )

    return collaborators


def generate_share_data() -> dict:

    active_tab = random.choice(
        SHARE_TABS
    )

    return {

        "document": {
            "name":
                random.choice(
                    [
                        "Summer Campaign",
                        "Marketing Presentation",
                        "Brand Strategy",
                        "Social Media Kit",
                        "Quarterly Review",
                    ]
                ),

            "preview":
                get_random_photo(),
        },

        "active_tab":
            active_tab,

        "tabs": [
            {
                "label":
                    tab,

                "selected":
                    tab == active_tab,
            }
            for tab in SHARE_TABS
        ],

        "invite": {
            "placeholder":
                random.choice(
                    [
                        "Add people, groups, or emails",
                        "Enter a name or email",
                        "Invite people to this design",
                    ]
                ),

            "permission":
                random.choice(
                    PERMISSIONS
                ),
        },

        "collaborators":
            generate_collaborators(),

        "link": {
            "access":
                random.choice(
                    [
                        "Anyone with the link",
                        "Only people added",
                        "Your team",
                    ]
                ),

            "permission":
                random.choice(
                    [
                        "Can view",
                        "Can comment",
                        "Can edit",
                    ]
                ),

            "url":
                "https://canva.example/design/share/8x3p92",

            "allow_download":
                random.random() < 0.70,

            "allow_comments":
                random.random() < 0.75,
        },

        "actions": {
            "send":
                "Send",

            "copy":
                "Copy link",

            "close":
                "Close",
        },
    }


if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_share_data()
    )