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

SNOOZED_STATES = [
    "snoozed_list",
    "scheduled_list",
    "snooze_menu",
    "custom_snooze_dialog",
    "scheduled_message_selected",
    "reschedule_dialog",
    "cancel_send_confirm",
    "empty_state",
    "mobile_actions_sheet",
]


# ==========================================================
# Pools
# ==========================================================

SUBJECTS = [
    "Project follow-up",
    "Meeting confirmation",
    "Travel details",
    "Invoice reminder",
    "Research update",
    "Weekly summary",
    "Design review",
    "Document request",
]


SNIPPETS = [
    "Following up on the discussion from earlier this week.",
    "Here are the details we agreed on during the meeting.",
    "Please review this when you have a chance.",
    "This message is scheduled to be delivered later.",
    "I wanted to send a quick update regarding the project.",
]


SNOOZE_OPTIONS = [
    "Later today",
    "Tomorrow",
    "This weekend",
    "Next week",
    "Pick date & time",
]


# ==========================================================
# Helpers
# ==========================================================

def _message(
    index: int,
    mode: str,
) -> dict:

    now = datetime.now()

    if mode == "scheduled":

        target = (
            now
            + timedelta(
                hours=random.randint(
                    2,
                    120,
                )
            )
        )

    else:

        target = (
            now
            + timedelta(
                hours=random.randint(
                    1,
                    72,
                )
            )
        )

    return {
        "id":
            f"{mode}_message_{index}",

        "sender":
            fake.name(),

        "email":
            fake.email(),

        "avatar":
            get_random_avatar(),

        "subject":
            random.choice(
                SUBJECTS
            ),

        "snippet":
            random.choice(
                SNIPPETS
            ),

        "target_date":
            target.strftime(
                "%b %d"
            ),

        "target_time":
            target.strftime(
                "%H:%M"
            ),

        "target_full":
            target.strftime(
                "%b %d, %H:%M"
            ),

        "starred":
            random.random()
            < 0.2,

        "has_attachment":
            random.random()
            < 0.3,
    }


# ==========================================================
# Public Generator
# ==========================================================

def generate_snoozed_data(
    state: str | None = None,
) -> dict:

    selected_state = (
        state
        if state is not None
        else random.choice(
            SNOOZED_STATES
        )
    )

    if selected_state not in SNOOZED_STATES:

        raise ValueError(
            f"Unknown snoozed state: "
            f"{selected_state}"
        )

    mode = (
        "scheduled"
        if selected_state
        in {
            "scheduled_list",
            "scheduled_message_selected",
            "reschedule_dialog",
            "cancel_send_confirm",
        }
        else "snoozed"
    )

    if selected_state == "empty_state":

        messages = []

    else:

        messages = [
            _message(
                index=index,
                mode=mode,
            )
            for index in range(
                random.randint(
                    8,
                    16,
                )
            )
        ]

    selected_message = (
        random.choice(
            messages
        )
        if messages
        else None
    )

    return {
        "state":
            selected_state,

        "mode":
            mode,

        "title":
            (
                "Scheduled"
                if mode == "scheduled"
                else "Snoozed"
            ),

        "messages":
            messages,

        "message_count":
            len(
                messages
            ),

        "selected_message":
            selected_message,

        "show_selected":
            selected_state
            == "scheduled_message_selected",

        "snooze_menu_open":
            selected_state
            == "snooze_menu",

        "custom_snooze_dialog_open":
            selected_state
            == "custom_snooze_dialog",

        "reschedule_dialog_open":
            selected_state
            == "reschedule_dialog",

        "cancel_send_confirm_open":
            selected_state
            == "cancel_send_confirm",

        "mobile_actions_sheet_open":
            selected_state
            == "mobile_actions_sheet",

        "snooze_options":
            SNOOZE_OPTIONS,

        "custom_date":
            (
                datetime.now()
                + timedelta(
                    days=random.randint(
                        1,
                        10,
                    )
                )
            ).strftime(
                "%Y-%m-%d"
            ),

        "custom_time":
            random.choice([
                "08:00",
                "09:30",
                "14:00",
                "18:30",
            ]),

        "empty_title":
            (
                "No scheduled messages"
                if mode == "scheduled"
                else "No snoozed messages"
            ),

        "empty_text":
            (
                "Messages scheduled for later delivery will appear here."
                if mode == "scheduled"
                else "Messages you snooze will return to your inbox later."
            ),
    }


if __name__ == "__main__":

    data = generate_snoozed_data()

    print(
        "State:",
        data["state"],
    )

    print(
        "Mode:",
        data["mode"],
    )