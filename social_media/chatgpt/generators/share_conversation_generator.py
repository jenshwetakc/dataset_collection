from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Conversation Titles
# ==========================================================

CONVERSATION_TITLES = [
    "Synthetic UI dataset design",
    "Machine learning experiment notes",
    "Research paper discussion",
    "Responsive layout implementation",
    "Accessibility evaluation",
    "Object detection training",
    "Dataset annotation strategy",
    "Frontend debugging session",
]


# ==========================================================
# Messages
# ==========================================================

USER_MESSAGES = [
    "Can you help me structure this implementation?",
    "How can we make the dataset more diverse?",
    "Can we improve the annotation behavior?",
    "What should we implement next?",
]


ASSISTANT_MESSAGES = [
    (
        "Yes. I would separate the shared rendering logic "
        "from the page-specific templates and generators."
    ),
    (
        "We can improve diversity by adding more interaction "
        "states such as dialogs, menus, search, and upload flows."
    ),
    (
        "A useful next step is to ensure occluded background "
        "elements are not included in the annotations."
    ),
]


# ==========================================================
# Shared People
# ==========================================================

def generate_people() -> list[dict]:

    count = random.randint(
        1,
        4,
    )

    people = []

    for index in range(
        count
    ):

        name = fake.name()

        people.append({

            "id":
                f"person_{index}",

            "name":
                name,

            "initials":
                "".join(
                    part[0]
                    for part in name.split()[:2]
                ).upper(),

            "email":
                fake.email(),

            "permission":
                random.choice([
                    "Viewer",
                    "Editor",
                ]),
        })

    return people


# ==========================================================
# Background Messages
# ==========================================================

def generate_background_messages() -> list[dict]:

    messages = []

    count = random.randint(
        4,
        7,
    )

    for index in range(
        count
    ):

        role = (
            "user"
            if index % 2 == 0
            else "assistant"
        )

        messages.append({

            "role":
                role,

            "text":
                (
                    random.choice(
                        USER_MESSAGES
                    )
                    if role == "user"
                    else random.choice(
                        ASSISTANT_MESSAGES
                    )
                ),
        })

    return messages


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    groups = []

    for group_index, label in enumerate(
        [
            "Today",
            "Yesterday",
            "Previous 7 days",
        ]
    ):

        items = []

        for item_index in range(
            random.randint(
                2,
                4,
            )
        ):

            items.append({

                "title":
                    random.choice(
                        CONVERSATION_TITLES
                    ),

                "active":
                    (
                        group_index == 0
                        and item_index == 0
                    ),
            })

        groups.append({

            "label":
                label,

            "items":
                items,
        })

    return groups


# ==========================================================
# Main Generator
# ==========================================================

def generate_share_conversation_data() -> dict:

    user_name = fake.name()

    conversation_title = random.choice(
        CONVERSATION_TITLES
    )

    link_token = fake.lexify(
        text="????????????"
    )

    return {

        "page_variant":
            "share_conversation",

        "conversation": {

            "title":
                conversation_title,

            "messages":
                generate_background_messages(),
        },

        "model": {

            "name":
                random.choice([
                    "ChatGPT",
                    "GPT-5",
                    "GPT-5 Thinking",
                ]),
        },

        "user": {

            "name":
                user_name,

            "initials":
                "".join(
                    part[0]
                    for part in user_name.split()[:2]
                ).upper(),
        },

        "history_sections":
            generate_history(),

        "share": {

            "link":
                (
                    "https://chat.example.com/share/"
                    f"{link_token}"
                ),

            "access":
                random.choice([
                    "Anyone with the link",
                    "Only invited people",
                ]),

            "allow_continue":
                random.random()
                < 0.55,

            "include_name":
                random.random()
                < 0.45,

            "people":
                generate_people(),

            "show_people":
                random.random()
                < 0.75,
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_share_conversation_data()
    )