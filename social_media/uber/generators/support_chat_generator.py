from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_driver_image,
)


fake = Faker()


# ==========================================================
# Message Helpers
# ==========================================================

SUPPORT_MESSAGES = [
    "Hi! How can I help with your trip today?",
    "I can help you review that charge.",
    "Thanks for sharing those details.",
    "I found the trip in your recent activity.",
    "The adjustment should appear shortly.",
    "Would you like me to check anything else?",
    "I've submitted the request for review.",
]


USER_MESSAGES = [
    "I think I was charged twice for my ride.",
    "The pickup location was different from what I selected.",
    "I left an item in the vehicle.",
    "Can you help me with my last trip?",
    "I don't recognize this charge.",
    "The fare was higher than expected.",
]


def generate_message_time(
    base_time: datetime,
    offset_minutes: int,
) -> str:

    value = (
        base_time
        + timedelta(
            minutes=offset_minutes
        )
    )

    return value.strftime(
        "%H:%M"
    )


def generate_messages() -> list[dict]:

    base_time = datetime.now().replace(
        second=0,
        microsecond=0,
    )

    count = random.randint(
        7,
        12,
    )

    messages = []

    current_sender = random.choice(
        [
            "support",
            "support",
            "user",
        ]
    )


    for index in range(count):

        if index > 0 and random.random() < 0.65:

            current_sender = (
                "user"
                if current_sender == "support"
                else "support"
            )

        if current_sender == "support":

            text = random.choice(
                SUPPORT_MESSAGES
            )

        else:

            text = random.choice(
                USER_MESSAGES
            )


        messages.append(
            {
                "sender":
                    current_sender,

                "text":
                    text,

                "timestamp":
                    generate_message_time(
                        base_time,
                        index * random.randint(
                            1,
                            4,
                        ),
                    ),

                "status":
                    (
                        random.choice(
                            [
                                "Delivered",
                                "Read",
                            ]
                        )
                        if current_sender == "user"
                        else None
                    ),
            }
        )


    return messages


# ==========================================================
# Main Generator
# ==========================================================

def generate_support_chat_data() -> dict:

    issue_title = random.choice(
        [
            "Fare review",
            "Trip support",
            "Payment issue",
            "Lost item",
            "Pickup issue",
        ]
    )

    return {

        "title":
            "Uber Support",

        "issue": {

            "title":
                issue_title,

            "trip":
                random.choice(
                    [
                        "UberX · Today",
                        "Comfort · Yesterday",
                        "Uber Green · Aug 27",
                    ]
                ),

            "status":
                random.choice(
                    [
                        "Active",
                        "Under review",
                        "Resolved",
                    ]
                ),
        },

        "support_agent": {

            "name":
                random.choice(
                    [
                        "Uber Support",
                        "Maya",
                        "Alex",
                        "Support Team",
                    ]
                ),

            "avatar":
                get_random_driver_image(),

            "online":
                random.choice(
                    [
                        True,
                        True,
                        False,
                    ]
                ),

            "response_time":
                random.choice(
                    [
                        "Usually replies instantly",
                        "Typically replies in a few minutes",
                        "Online now",
                    ]
                ),
        },

        "messages":
            generate_messages(),

        "quick_replies":
            random.sample(
                [
                    "Yes, please",
                    "No, thanks",
                    "Check my fare",
                    "I need more help",
                    "View receipt",
                    "Contact driver",
                ],
                k=random.randint(
                    3,
                    4,
                ),
            ),

        "composer_placeholder":
            random.choice(
                [
                    "Type a message",
                    "Message Uber Support",
                    "Describe your issue",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_support_chat_data()
    )