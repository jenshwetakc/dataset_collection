from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_agent_image,
    get_random_property_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

CITIES = [
    ("Seattle", "WA"),
    ("Bellevue", "WA"),
    ("Austin", "TX"),
    ("Denver", "CO"),
    ("Portland", "OR"),
    ("San Diego", "CA"),
    ("Boston", "MA"),
]


TEXT_MESSAGES = [
    "I really like this one.",
    "The kitchen looks much better than the last house.",
    "What do you think about the neighborhood?",
    "This might be worth touring.",
    "The price is a little higher than our target.",
    "I saved another one nearby.",
    "The backyard looks perfect.",
    "I think we should compare this with the other house.",
    "Would Saturday work for a tour?",
    "This one has almost everything on our list.",
    "The commute looks pretty good from here.",
    "I like the layout but I am not sure about the price.",
]


AGENT_MESSAGES = [
    "I can help you arrange a tour.",
    "There are several available tour times this weekend.",
    "I can send you a few similar homes nearby.",
    "This listing has had quite a bit of recent interest.",
    "Let me know if you would like more details about the property.",
]


TOUR_TIMES = [
    "Sat 10:00 AM",
    "Sat 1:30 PM",
    "Sat 4:00 PM",
    "Sun 11:00 AM",
    "Sun 2:30 PM",
]


CONVERSATION_NAMES = [
    "Home shortlist",
    "Seattle search",
    "Weekend tours",
    "Family picks",
    "First home search",
    "Downtown homes",
    "Summer move",
]


# ==========================================================
# Helpers
# ==========================================================

def format_price(
    value: int,
) -> str:

    return (
        "$"
        f"{value:,}"
    )


def generate_timestamp(
    minutes_ago: int,
) -> str:

    value = (
        datetime.now()
        - timedelta(
            minutes=minutes_ago
        )
    )

    return value.strftime(
        "%I:%M %p"
    ).lstrip(
        "0"
    )


# ==========================================================
# Property
# ==========================================================

def generate_shared_property(
    index: int,
) -> dict:

    city, state = random.choice(
        CITIES
    )

    price = random.randrange(
        280_000,
        1_800_000,
        5_000,
    )

    return {

        "id":
            index,

        "price":
            price,

        "price_text":
            format_price(
                price
            ),

        "beds":
            random.randint(
                2,
                5,
            ),

        "baths":
            random.choice(
                [
                    1.5,
                    2,
                    2.5,
                    3,
                    3.5,
                ]
            ),

        "sqft":
            random.randint(
                900,
                3400,
            ),

        "address":
            fake.street_address(),

        "city":
            city,

        "state":
            state,

        "image":
            get_random_property_image(),

        "saved":
            random.random()
            < 0.45,
    }


# ==========================================================
# Participants
# ==========================================================

def generate_participant(
    role: str,
) -> dict:

    name = fake.first_name()

    return {

        "name":
            name,

        "role":
            role,

        "avatar":
            get_random_agent_image(),

        "initial":
            name[
                :1
            ].upper(),
    }


# ==========================================================
# Conversation Messages
# ==========================================================

def generate_messages(
    property_pool: list[dict],
) -> list[dict]:

    messages = []

    message_count = random.randint(
        14,
        24,
    )

    elapsed = (
        message_count
        * random.randint(
            8,
            18,
        )
    )


    for index in range(
        message_count
    ):

        roll = random.random()


        # ==================================================
        # Shared Property
        # ==================================================

        if (
            roll < 0.20
            and property_pool
        ):

            messages.append(
                {
                    "type":
                        "property",

                    "sender":
                        random.choice(
                            [
                                "me",
                                "partner",
                            ]
                        ),

                    "property":
                        random.choice(
                            property_pool
                        ),

                    "timestamp":
                        generate_timestamp(
                            elapsed
                        ),
                }
            )


        # ==================================================
        # Agent Message
        # ==================================================

        elif roll < 0.30:

            messages.append(
                {
                    "type":
                        "text",

                    "sender":
                        "agent",

                    "text":
                        random.choice(
                            AGENT_MESSAGES
                        ),

                    "timestamp":
                        generate_timestamp(
                            elapsed
                        ),
                }
            )


        # ==================================================
        # Tour Schedule
        # ==================================================

        elif roll < 0.38:

            times = random.sample(
                TOUR_TIMES,
                k=random.randint(
                    2,
                    4,
                ),
            )

            messages.append(
                {
                    "type":
                        "tour",

                    "sender":
                        "agent",

                    "title":
                        "Available tour times",

                    "text":
                        (
                            "Choose a time that works "
                            "for everyone."
                        ),

                    "times":
                        times,

                    "timestamp":
                        generate_timestamp(
                            elapsed
                        ),
                }
            )


        # ==================================================
        # Normal Text
        # ==================================================

        else:

            messages.append(
                {
                    "type":
                        "text",

                    "sender":
                        random.choice(
                            [
                                "me",
                                "partner",
                                "partner",
                            ]
                        ),

                    "text":
                        random.choice(
                            TEXT_MESSAGES
                        ),

                    "timestamp":
                        generate_timestamp(
                            elapsed
                        ),
                }
            )


        elapsed = max(
            0,
            elapsed
            - random.randint(
                3,
                25,
            ),
        )


    return messages


# ==========================================================
# Inbox Conversation
# ==========================================================

def generate_inbox_conversation(
    index: int,
) -> dict:

    participant = (
        generate_participant(
            random.choice(
                [
                    "Co-shopper",
                    "Agent",
                    "Partner",
                ]
            )
        )
    )

    return {

        "id":
            index,

        "title":
            random.choice(
                CONVERSATION_NAMES
            ),

        "participant":
            participant,

        "preview":
            random.choice(
                TEXT_MESSAGES
                + AGENT_MESSAGES
            ),

        "timestamp":
            random.choice(
                [
                    "Now",
                    "4m",
                    "18m",
                    "1h",
                    "3h",
                    "Yesterday",
                    "Mon",
                ]
            ),

        "unread":
            random.choice(
                [
                    0,
                    0,
                    0,
                    1,
                    2,
                    3,
                    5,
                ]
            ),

        "active":
            index == 0,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_messages_data() -> dict:

    partner = (
        generate_participant(
            "Co-shopper"
        )
    )

    agent = (
        generate_participant(
            "Buyer's agent"
        )
    )

    user = (
        generate_participant(
            "You"
        )
    )


    properties = [

        generate_shared_property(
            index
        )

        for index in range(
            6
        )
    ]


    inbox = [

        generate_inbox_conversation(
            index
        )

        for index in range(
            random.randint(
                6,
                10,
            )
        )
    ]


    active_title = random.choice(
        [
            "Home shortlist",
            "Weekend tours",
            "Our home search",
        ]
    )


    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "user":
            user,


        "partner":
            partner,


        "agent":
            agent,


        "inbox":
            inbox,


        "active_conversation": {

            "title":
                active_title,

            "subtitle":
                (
                    f"{partner['name']} and "
                    f"{agent['name']}"
                ),

            "participants": [
                user,
                partner,
                agent,
            ],

            "messages":
                generate_messages(
                    properties
                ),
        },


        "property_context":
            random.choice(
                properties
            ),


        "composer": {

            "placeholder":
                random.choice(
                    [
                        "Message your group",
                        "Write a message",
                        "Ask about a home",
                    ]
                ),
        },


        "mobile_navigation": [

            {
                "label": "Home",
                "icon": "home",
                "active": False,
            },

            {
                "label": "Search",
                "icon": "search",
                "active": False,
            },

            {
                "label": "Saved",
                "icon": "favorite",
                "active": False,
            },

            {
                "label": "Messages",
                "icon": "chat",
                "active": True,
            },

            {
                "label": "Profile",
                "icon": "person",
                "active": False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_messages_data()
    )

    print(
        "Inbox:",
        len(
            data[
                "inbox"
            ]
        ),
    )

    print(
        "Messages:",
        len(
            data[
                "active_conversation"
            ][
                "messages"
            ]
        ),
    )

    print(
        "Agent:",
        data[
            "agent"
        ][
            "name"
        ],
    )