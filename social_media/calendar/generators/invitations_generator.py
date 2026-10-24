from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


INVITATION_STATES = [
    "inbox",
    "awaiting_response",
    "accepted",
    "declined",
    "event_updates",
    "search_results",
    "empty_inbox",
    "invitation_details_dialog",
    "decline_dialog",
    "propose_time_dialog",
    "mobile_filter_sheet",
]


EVENT_TITLES = [
    "Product roadmap review",
    "Design system workshop",
    "Research sync",
    "Quarterly planning",
    "Team lunch",
    "Accessibility review",
    "Release readiness",
    "Project Atlas kickoff",
]


PEOPLE = [
    {
        "name": "Mina Park",
        "initials": "MP",
    },
    {
        "name": "Jordan Lee",
        "initials": "JL",
    },
    {
        "name": "Alex Morgan",
        "initials": "AM",
    },
    {
        "name": "Taylor Kim",
        "initials": "TK",
    },
    {
        "name": "Chris Evans",
        "initials": "CE",
    },
]


LOCATIONS = [
    "Conference Room A",
    "Google Meet",
    "Zoom",
    "Design Studio",
    "Cafeteria",
]


def generate_invitation(
    index: int,
) -> dict:
    organizer = random.choice(
        PEOPLE
    )

    start = (
        datetime.now()
        .replace(
            hour=random.randint(9, 16),
            minute=random.choice([0, 30]),
            second=0,
            microsecond=0,
        )
        + timedelta(
            days=random.randint(0, 12),
        )
    )

    status = random.choice([
        "pending",
        "pending",
        "accepted",
        "declined",
        "updated",
    ])

    return {
        "id": f"invite-{index}",

        "title":
            random.choice(
                EVENT_TITLES
            ),

        "organizer":
            organizer["name"],

        "organizer_initials":
            organizer["initials"],

        "date":
            start.strftime(
                "%a, %b %d"
            ),

        "time":
            start.strftime(
                "%I:%M %p"
            ),

        "location":
            random.choice(
                LOCATIONS
            ),

        "status":
            status,

        "unread":
            random.random() < 0.45,

        "guest_count":
            random.randint(3, 24),

        "description": (
            "Review current progress, discuss open questions, "
            "and agree on the next steps."
        ),
    }


def generate_invitations_data(
    state: str | None = None,
) -> dict:
    if state is None:
        state = random.choice(
            INVITATION_STATES
        )

    if state not in INVITATION_STATES:
        raise ValueError(
            f"Unknown invitation state: {state}. "
            f"Available states: {INVITATION_STATES}"
        )

    invitations = [
        generate_invitation(index)
        for index in range(
            1,
            random.randint(7, 12),
        )
    ]

    status_for_state = {
        "awaiting_response": "pending",
        "accepted": "accepted",
        "declined": "declined",
        "event_updates": "updated",
    }

    if state in status_for_state:
        required_status = (
            status_for_state[state]
        )

        for invitation in invitations:
            invitation["status"] = (
                required_status
            )

    if state == "search_results":
        invitations = [
            invitation
            for invitation in invitations
            if (
                "roadmap"
                in invitation["title"].lower()
            )
        ]

        if not invitations:
            invitation = generate_invitation(100)
            invitation["title"] = (
                "Product roadmap review"
            )
            invitations = [invitation]

    selected_invitation = (
        invitations[0]
        if invitations
        else generate_invitation(999)
    )

    popup_states = {
        "invitation_details_dialog",
        "decline_dialog",
        "propose_time_dialog",
        "mobile_filter_sheet",
    }

    return {
        "app_name":
            "Calendar Invitations",

        "state":
            state,

        "popup_open":
            state in popup_states,

        "page_title":
            "Invitations & updates",

        "profile": {
            "initials":
                random.choice([
                    "SK",
                    "AM",
                    "JL",
                ]),
        },

        "filters": [
            {
                "id": "inbox",
                "label": "Inbox",
                "icon": "inbox",
                "count": len(invitations),
            },
            {
                "id": "awaiting_response",
                "label": "Awaiting response",
                "icon": "schedule",
                "count": sum(
                    item["status"] == "pending"
                    for item in invitations
                ),
            },
            {
                "id": "accepted",
                "label": "Accepted",
                "icon": "event_available",
                "count": sum(
                    item["status"] == "accepted"
                    for item in invitations
                ),
            },
            {
                "id": "declined",
                "label": "Declined",
                "icon": "event_busy",
                "count": sum(
                    item["status"] == "declined"
                    for item in invitations
                ),
            },
            {
                "id": "event_updates",
                "label": "Event updates",
                "icon": "update",
                "count": sum(
                    item["status"] == "updated"
                    for item in invitations
                ),
            },
        ],

        "invitations": (
            []
            if state == "empty_inbox"
            else invitations
        ),

        "selected_invitation":
            selected_invitation,

        "search_query": (
            "roadmap"
            if state == "search_results"
            else ""
        ),
    }


if __name__ == "__main__":
    import pprint

    pprint.pp(
        generate_invitations_data()
    )