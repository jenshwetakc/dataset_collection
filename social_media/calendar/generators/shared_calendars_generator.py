from __future__ import annotations

import random
from datetime import (
    datetime,
    timedelta,
)

from faker import Faker


fake = Faker()


# ==========================================================
# Page States
# ==========================================================

SHARED_CALENDAR_STATES = [
    "team_overview",
    "availability_matrix",
    "shared_calendars",
    "permissions",
    "search_results",
    "empty_team",
    "loading",
    "error",
    "member_details_dialog",
    "invite_member_dialog",
    "sharing_settings_dialog",
    "remove_member_dialog",
    "mobile_member_sheet",
]


# ==========================================================
# Generator Data
# ==========================================================

TEAM_ROLES = [
    "Product designer",
    "Software engineer",
    "Product manager",
    "Researcher",
    "Data analyst",
    "Marketing manager",
]

CALENDAR_NAMES = [
    "Product launches",
    "Design critiques",
    "Team availability",
    "Customer research",
    "Release milestones",
    "Company events",
]

CALENDAR_COLORS = [
    "#1a73e8",
    "#7b1fa2",
    "#00897b",
    "#e37400",
    "#d93025",
    "#5f6368",
]


# ==========================================================
# Helpers
# ==========================================================

def generate_initials(name: str) -> str:
    parts = [
        part
        for part in name.split()
        if part
    ]

    if not parts:
        return "U"

    if len(parts) == 1:
        return parts[0][0].upper()

    return (
        parts[0][0]
        + parts[-1][0]
    ).upper()


def generate_member(index: int) -> dict:
    name = fake.name()

    status = random.choices(
        [
            "available",
            "busy",
            "away",
            "offline",
        ],
        weights=[
            40,
            32,
            18,
            10,
        ],
        k=1,
    )[0]

    return {
        "id": f"member-{index}",
        "name": name,
        "initials": generate_initials(name),
        "email": fake.unique.email(),
        "role": random.choice(TEAM_ROLES),
        "status": status,
        "status_label": status.title(),
        "timezone": random.choice([
            "UTC−08:00",
            "UTC−05:00",
            "UTC+00:00",
            "UTC+01:00",
            "UTC+09:00",
        ]),
        "working_hours": random.choice([
            "8:00 AM – 4:00 PM",
            "9:00 AM – 5:00 PM",
            "10:00 AM – 6:00 PM",
        ]),
        "permission": random.choice([
            "See free/busy",
            "See event details",
            "Make changes",
        ]),
        "selected": index <= 4,
    }


def generate_shared_calendar(
    index: int,
    members: list[dict],
) -> dict:
    owner = random.choice(members)

    return {
        "id": f"calendar-{index}",
        "name": CALENDAR_NAMES[
            (index - 1)
            % len(CALENDAR_NAMES)
        ],
        "color": CALENDAR_COLORS[
            (index - 1)
            % len(CALENDAR_COLORS)
        ],
        "owner": owner["name"],
        "owner_initials": owner["initials"],
        "member_count": random.randint(4, 28),
        "permission": random.choice([
            "View only",
            "Edit events",
            "Manage sharing",
        ]),
        "visible": random.random() > 0.15,
    }


def generate_availability(
    members: list[dict],
) -> list[dict]:
    rows = []

    for member in members[:6]:
        cells = []

        for hour in range(8, 18):
            cell_state = random.choices(
                [
                    "free",
                    "busy",
                    "tentative",
                    "outside",
                ],
                weights=[
                    46,
                    32,
                    12,
                    10,
                ],
                k=1,
            )[0]

            cells.append({
                "hour": hour,
                "state": cell_state,
            })

        rows.append({
            "member": member,
            "cells": cells,
        })

    return rows


# ==========================================================
# Main Generator
# ==========================================================


def generate_shared_calendars_data(
    state: str | None = None,
) -> dict:
    state = (
        state
        or random.choice(
            SHARED_CALENDAR_STATES
        )
    )

    if state not in SHARED_CALENDAR_STATES:
        raise ValueError(
            f"Unknown shared calendar state: {state}. "
            f"Available states: {SHARED_CALENDAR_STATES}"
        )

    members = [
        generate_member(index)
        for index in range(
            1,
            random.randint(9, 14),
        )
    ]

    calendars = [
        generate_shared_calendar(
            index,
            members,
        )
        for index in range(1, 7)
    ]

    selected_member = members[0]
    selected_calendar = calendars[0]

    today = datetime.now()
    range_end_date = (
        today
        + timedelta(days=4)
    )

    date_range = (
        f"{today.strftime('%b %d')} – "
        f"{range_end_date.strftime('%b %d')}"
    )

    popup_states = {
        "member_details_dialog",
        "invite_member_dialog",
        "sharing_settings_dialog",
        "remove_member_dialog",
        "mobile_member_sheet",
    }

    if state == "search_results":
        members = members[:3]

    if state == "empty_team":
        members = []

    profile_name = fake.name()

    return {
        "state": state,

        "popup_open":
            state in popup_states,

        "profile": {
            "name": profile_name,
            "initials":
                generate_initials(
                    profile_name
                ),
        },

        "team_name":
            f"{fake.word().title()} Team",

        "date_label":
            today.strftime(
                "%B %d, %Y"
            ),

        "date_range":
            date_range,

        "search_query": (
            fake.first_name()
            if state == "search_results"
            else ""
        ),

        "members":
            members,

        "all_members_count":
            len(members),

        "selected_count":
            sum(
                member["selected"]
                for member in members
            ),

        "available_count":
            sum(
                member["status"]
                == "available"
                for member in members
            ),

        "busy_count":
            sum(
                member["status"]
                == "busy"
                for member in members
            ),

        "availability":
            generate_availability(
                members
            ),

        "calendars":
            calendars,

        "selected_member":
            selected_member,

        "selected_calendar":
            selected_calendar,

        "suggested_time":
            random.choice([
                "10:30 AM – 11:00 AM",
                "1:00 PM – 1:30 PM",
                "3:30 PM – 4:00 PM",
            ]),

        "invite_email":
            fake.email(),

        "error_message": (
            "Team availability could not be loaded. "
            "Check your connection and try again."
        ),
    }

# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":
    for page_state in SHARED_CALENDAR_STATES:
        page = generate_shared_calendars_data(
            page_state
        )

        print(
            page_state,
            len(page["members"]),
            page["popup_open"],
        )