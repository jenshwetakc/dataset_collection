from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from faker import Faker

from social_media.email.generators.media_generator import (
    get_random_attachment_image,
    get_random_avatar,
)


fake = Faker()


MESSAGE_STATES = [
    "single",
    "thread",
    "attachment_heavy",
    "reply_open",
    "forwarded",
    "expanded_details",
    "split_pane",
]


SUBJECTS = [
    "Project update and next steps",
    "Meeting notes and action items",
    "Reservation details for your trip",
    "Research progress summary",
    "Invoice and payment confirmation",
    "Design review feedback",
    "Weekly team update",
    "Important account notification",
]


PARAGRAPHS = [
    "Thanks for your message. I wanted to send a quick update with the latest information and a few items that need your attention.",
    "The latest version is now ready for review. Please check the highlighted sections and let me know if anything should be revised.",
    "I have summarized the main decisions from our discussion below. The remaining items can be handled during the next meeting.",
    "Everything is confirmed on my side. I have attached the relevant files so that you can review them when convenient.",
    "Please let me know if the proposed schedule works for you. I can adjust the timing if needed.",
]


ATTACHMENT_NAMES = [
    "report.pdf",
    "meeting-notes.docx",
    "invoice.pdf",
    "design-review.pptx",
    "photo.jpg",
    "summary.pdf",
]


def _time_text(
    hours_ago: int | None = None,
) -> str:

    now = datetime.now()

    if hours_ago is None:
        hours_ago = random.randint(
            1,
            96,
        )

    value = (
        now
        - timedelta(
            hours=hours_ago
        )
    )

    if value.date() == now.date():
        return value.strftime("%H:%M")

    if (
        now.date()
        - value.date()
    ).days == 1:
        return "Yesterday"

    return value.strftime(
        "%b %d, %Y"
    )


def _person() -> dict:

    name = fake.name()

    return {
        "name": name,
        "email": fake.email(),
        "avatar": get_random_avatar(),
    }


def _attachment(
    index: int,
) -> dict:

    filename = random.choice(
        ATTACHMENT_NAMES
    )

    is_image = filename.endswith(
        (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        )
    )

    return {
        "id": f"attachment_{index}",
        "name": filename,
        "size": f"{random.randint(80, 950)} KB",
        "preview": (
            get_random_attachment_image()
            if is_image
            else None
        ),
    }


def _body_paragraphs() -> list[str]:

    count = random.randint(
        2,
        5,
    )

    return [
        random.choice(
            PARAGRAPHS
        )
        for _ in range(
            count
        )
    ]


def _message(
    index: int,
    sender: dict,
    recipient: dict,
    hours_ago: int,
    attachment_count: int = 0,
    forwarded: bool = False,
) -> dict:

    return {
        "id": f"thread_message_{index}",
        "sender": sender,
        "recipient": recipient,
        "time": _time_text(
            hours_ago
        ),
        "body": _body_paragraphs(),
        "forwarded": forwarded,
        "expanded": False,
        "attachments": [
            _attachment(
                attachment_index
            )
            for attachment_index in range(
                attachment_count
            )
        ],
    }


def _generate_thread(
    state: str,
    current_user: dict,
    other_user: dict,
) -> list[dict]:

    if state == "single":
        count = 1

    elif state == "thread":
        count = random.randint(
            3,
            5,
        )

    elif state == "attachment_heavy":
        count = random.randint(
            2,
            4,
        )

    elif state == "forwarded":
        count = random.randint(
            2,
            4,
        )

    else:
        count = random.randint(
            1,
            3,
        )

    result = []

    for index in range(
        count
    ):

        sender = (
            other_user
            if index % 2 == 0
            else current_user
        )

        recipient = (
            current_user
            if sender is other_user
            else other_user
        )

        if state == "attachment_heavy":
            attachment_count = random.randint(
                1,
                3,
            )

        else:
            attachment_count = (
                1
                if random.random() < 0.25
                else 0
            )

        forwarded = (
            state == "forwarded"
            and index == count - 1
        )

        result.append(
            _message(
                index=index,
                sender=sender,
                recipient=recipient,
                hours_ago=(
                    count - index
                ) * random.randint(
                    3,
                    10,
                ),
                attachment_count=attachment_count,
                forwarded=forwarded,
            )
        )

    return result


def _sidebar_messages() -> list[dict]:

    return [
        {
            "id": f"preview_{index}",
            "sender": fake.name(),
            "subject": random.choice(
                SUBJECTS
            ),
            "time": _time_text(
                random.randint(
                    1,
                    72,
                )
            ),
            "unread": (
                random.random()
                < 0.35
            ),
        }
        for index in range(
            random.randint(
                8,
                14,
            )
        )
    ]


def generate_message_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            MESSAGE_STATES
        )
    )

    if selected_state not in MESSAGE_STATES:

        raise ValueError(
            f"Unknown message state: {selected_state}. "
            f"Expected one of: {MESSAGE_STATES}"
        )

    current_user = _person()
    other_user = _person()

    thread = _generate_thread(
        state=selected_state,
        current_user=current_user,
        other_user=other_user,
    )

    if (
        selected_state
        == "expanded_details"
        and thread
    ):
        thread[0]["expanded"] = True

    return {
        "state":
            selected_state,

        "subject":
            random.choice(
                SUBJECTS
            ),

        "current_user":
            current_user,

        "other_user":
            other_user,

        "thread":
            thread,

        "reply_open": (
            selected_state
            == "reply_open"
        ),

        "show_split_pane": (
            selected_state
            == "split_pane"
        ),

        "sidebar_messages":
            _sidebar_messages(),

        "reply_text":
            fake.paragraph(
                nb_sentences=random.randint(
                    2,
                    4,
                )
            ),

        "labels":
            random.sample(
                [
                    "Inbox",
                    "Work",
                    "Important",
                    "Updates",
                ],
                k=random.randint(
                    1,
                    3,
                ),
            ),
    }


if __name__ == "__main__":

    data = generate_message_data()

    print("\n==============================")
    print("EMAIL MESSAGE GENERATOR")
    print("==============================")

    print(
        "State:",
        data["state"],
    )

    print(
        "Thread length:",
        len(
            data["thread"]
        ),
    )

    print(
        "Split pane:",
        data["show_split_pane"],
    )
