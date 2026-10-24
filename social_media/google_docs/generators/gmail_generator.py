from __future__ import annotations

import random

from faker import Faker


fake = Faker()


GMAIL_STATES = [
    "inbox",
    "search_results",
    "message_open",
    "starred",
    "sent",
    "trash",
    "labels_open",
    "compose_dialog",
]


NAVIGATION_ITEMS = [
    ("inbox", "Inbox", "inbox"),
    ("starred", "Starred", "star"),
    ("snoozed", "Snoozed", "schedule"),
    ("sent", "Sent", "send"),
    ("drafts", "Drafts", "draft"),
    ("trash", "Trash", "delete"),
]


LABEL_NAMES = [
    "Work",
    "Personal",
    "Travel",
    "Receipts",
    "Projects",
    "Important",
]


AVATAR_COLORS = [
    "#1a73e8",
    "#ea4335",
    "#34a853",
    "#fbbc04",
    "#9334e6",
    "#d93025",
]


def make_initials(
    name: str,
) -> str:

    parts = name.split()

    return "".join(
        part[0].upper()
        for part in parts[:2]
    )


def generate_message(
    index: int,
) -> dict:

    sender_name = fake.name()

    subject = random.choice(
        [
            fake.sentence(
                nb_words=random.randint(4, 8),
            ).rstrip("."),
            f"Quick update about {fake.word().title()}",
            f"Invitation: {fake.catch_phrase()}",
            f"Your {fake.word().title()} summary",
            f"Next steps for {fake.bs()}",
        ]
    )

    paragraphs = fake.paragraphs(
        nb=random.randint(2, 4),
    )

    has_attachment = (
        random.random()
        < 0.30
    )

    attachment_count = (
        random.randint(1, 3)
        if has_attachment
        else 0
    )

    attachments = []

    for attachment_index in range(
        attachment_count
    ):

        attachments.append(
            {
                "name":
                    f"{fake.word()}_"
                    f"{attachment_index + 1}.pdf",

                "size":
                    f"{random.randint(80, 940)} KB",
            }
        )

    return {
        "id":
            f"message_{index:03d}",

        "sender":
            sender_name,

        "email":
            fake.email(),

        "initials":
            make_initials(
                sender_name
            ),

        "avatar_color":
            random.choice(
                AVATAR_COLORS
            ),

        "subject":
            subject,

        "preview":
            fake.sentence(
                nb_words=random.randint(8, 15),
            ),

        "time":
            random.choice(
                [
                    "9:42 AM",
                    "8:15 AM",
                    "Yesterday",
                    "Mon",
                    "Sep 18",
                ]
            ),

        "unread":
            random.random()
            < 0.55,

        "starred":
            random.random()
            < 0.30,

        "important":
            random.random()
            < 0.20,

        "label":
            random.choice(
                LABEL_NAMES
            ),

        "body":
            paragraphs,

        "attachments":
            attachments,
    }


def generate_gmail_page(
    state: str | None = None,
) -> dict:

    state = (
        state
        or random.choice(
            GMAIL_STATES
        )
    )

    messages = [
        generate_message(index)
        for index in range(
            random.randint(10, 18)
        )
    ]

    selected_message = random.choice(
        messages
    )

    search_query = random.choice(
        [
            fake.word(),
            selected_message["sender"].split()[0],
            selected_message["subject"].split()[0],
            "project update",
            "invoice",
        ]
    )

    if state == "starred":

        visible_messages = [
            message
            for message in messages
            if message["starred"]
        ]

        if not visible_messages:

            messages[0]["starred"] = True
            visible_messages = [messages[0]]

    elif state == "sent":

        visible_messages = messages[:]

        for message in visible_messages:

            message["sender"] = "me"
            message["initials"] = "SK"
            message["avatar_color"] = "#1a73e8"

    elif state == "trash":

        visible_messages = messages[:]

    elif state == "search_results":

        visible_messages = messages[:]

    else:

        visible_messages = messages[:]

    unread_count = sum(
        message["unread"]
        for message in messages
    )

    return {
        "app_name":
            "Gmail",

        "state":
            state,

        "title":
            {
                "inbox": "Inbox",
                "search_results": "Search results",
                "message_open": "Inbox",
                "starred": "Starred",
                "sent": "Sent",
                "trash": "Trash",
                "labels_open": "Inbox",
                "compose_dialog": "Inbox",
            }[state],

        "navigation":
            NAVIGATION_ITEMS,

        "labels":
            LABEL_NAMES,

        "messages":
            visible_messages,

        "selected_message":
            selected_message,

        "search_query":
            search_query,

        "unread_count":
            unread_count,

        "compose":
            {
                "recipient":
                    (
                        fake.email()
                        if random.random() < 0.45
                        else ""
                    ),

                "subject":
                    (
                        fake.sentence(
                            nb_words=5,
                        ).rstrip(".")
                        if random.random() < 0.35
                        else ""
                    ),

                "body":
                    (
                        fake.paragraph(
                            nb_sentences=2,
                        )
                        if random.random() < 0.35
                        else ""
                    ),
            },
    }