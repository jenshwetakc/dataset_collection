from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

SPAM_TRASH_STATES = [
    "spam_list",
    "trash_list",
    "bulk_selected",
    "empty_folder",
    "warning_banner",
    "restore_state",
    "delete_forever_confirm",
    "not_spam_dialog",
    "mobile_action_sheet",
]


# ==========================================================
# Pools
# ==========================================================

SUBJECTS = [
    "Limited time offer",
    "Account notice",
    "Your monthly statement",
    "Important message",
    "Special promotion",
    "Action required",
    "Delivery update",
    "Subscription reminder",
]

SNIPPETS = [
    "This message was automatically classified based on its content.",
    "Review this email if you think it was moved here by mistake.",
    "The sender is not in your contacts.",
    "This message contains promotional or suspicious content.",
    "You can restore this message or remove it permanently.",
]


# ==========================================================
# Helpers
# ==========================================================

def _time_text() -> str:

    now = datetime.now()

    value = (
        now
        - timedelta(
            hours=random.randint(
                1,
                240,
            )
        )
    )

    if value.date() == now.date():
        return value.strftime("%H:%M")

    return value.strftime("%b %d")


def _message(
    index: int,
    folder: str,
) -> dict:

    sender = fake.name()

    return {
        "id": f"{folder}_message_{index}",
        "sender": sender,
        "email": fake.email(),
        "avatar": get_random_avatar(),
        "subject": random.choice(SUBJECTS),
        "snippet": random.choice(SNIPPETS),
        "time": _time_text(),
        "selected": False,
        "starred": random.random() < 0.12,
        "suspicious": (
            folder == "spam"
            and random.random() < 0.7
        ),
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_spam_trash_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            SPAM_TRASH_STATES
        )
    )

    if selected_state not in SPAM_TRASH_STATES:

        raise ValueError(
            f"Unknown spam/trash state: {selected_state}. "
            f"Expected one of: {SPAM_TRASH_STATES}"
        )

    folder = (
        "trash"
        if selected_state
        in {
            "trash_list",
            "restore_state",
            "delete_forever_confirm",
        }
        else "spam"
    )

    if selected_state == "empty_folder":

        messages = []

    else:

        messages = [
            _message(
                index=index,
                folder=folder,
            )
            for index in range(
                random.randint(
                    10,
                    20,
                )
            )
        ]

    if (
        selected_state
        == "bulk_selected"
        and messages
    ):

        selected_count = random.randint(
            2,
            min(
                5,
                len(messages),
            ),
        )

        for message in random.sample(
            messages,
            selected_count,
        ):
            message["selected"] = True

    selected_messages = [
        message
        for message in messages
        if message["selected"]
    ]

    return {
        "state":
            selected_state,

        "folder":
            folder,

        "title":
            (
                "Trash"
                if folder == "trash"
                else "Spam"
            ),

        "messages":
            messages,

        "message_count":
            len(messages),

        "selected_count":
            len(selected_messages),

        "show_warning_banner":
            selected_state
            == "warning_banner",

        "show_restore_state":
            selected_state
            == "restore_state",

        "delete_forever_confirm_open":
            selected_state
            == "delete_forever_confirm",

        "not_spam_dialog_open":
            selected_state
            == "not_spam_dialog",

        "mobile_action_sheet_open":
            selected_state
            == "mobile_action_sheet",

        "warning_text":
            (
                "Messages in Spam may be deleted automatically after 30 days."
                if folder == "spam"
                else
                "Messages in Trash are permanently deleted after 30 days."
            ),

        "empty_title":
            (
                "No spam messages"
                if folder == "spam"
                else "Trash is empty"
            ),

        "empty_text":
            (
                "Messages marked as spam will appear here."
                if folder == "spam"
                else "Deleted messages will appear here until they are permanently removed."
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_spam_trash_data()

    print(
        "State:",
        data["state"],
    )

    print(
        "Folder:",
        data["folder"],
    )

    print(
        "Messages:",
        data["message_count"],
    )
