from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

REMINDERS_STATES = [

    "smart_lists",

    "task_list",

    "completed",

    "flagged",

    "task_detail",

    "new_reminder",

    "tag_filter",

    "delete_confirmation",
]


REMINDERS_STATE_WEIGHTS = [

    20,

    24,

    10,

    10,

    12,

    10,

    8,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# List Definitions
# ==========================================================

LIST_DEFINITIONS = [

    {
        "id": "today",
        "title": "Today",
        "color": "#0A84FF",
        "icon": "calendar-days",
    },

    {
        "id": "scheduled",
        "title": "Scheduled",
        "color": "#FF453A",
        "icon": "calendar-clock",
    },

    {
        "id": "all",
        "title": "All",
        "color": "#8E8E93",
        "icon": "tray",
    },

    {
        "id": "flagged",
        "title": "Flagged",
        "color": "#FF9F0A",
        "icon": "flag",
    },

    {
        "id": "completed",
        "title": "Completed",
        "color": "#6E6E73",
        "icon": "circle-check-big",
    },
]


CUSTOM_LISTS = [

    {
        "id": "work",
        "title": "Work",
        "color": "#0A84FF",
    },

    {
        "id": "research",
        "title": "Research",
        "color": "#BF5AF2",
    },

    {
        "id": "personal",
        "title": "Personal",
        "color": "#30D158",
    },

    {
        "id": "shopping",
        "title": "Shopping",
        "color": "#FF9F0A",
    },
]


# ==========================================================
# Reminder
# ==========================================================

def generate_reminder(
    index: int,
) -> dict:

    titles = [

        "Review experiment results",

        "Prepare presentation slides",

        "Send meeting notes",

        "Read related paper",

        "Run validation",

        "Check annotation output",

        "Update implementation",

        "Submit report",

        "Buy groceries",

        "Call Alex",

        "Prepare dataset",

        "Review code changes",
    ]


    notes = [

        "",

        "Check the latest version before finishing.",

        "Remember to attach the updated file.",

        "Review previous results first.",

        "Complete before the next meeting.",
    ]


    tags = random.sample(

        [
            "work",
            "research",
            "important",
            "personal",
            "today",
        ],

        k=random.randint(
            0,
            2,
        ),
    )


    has_date = (
        random.random()
        < 0.65
    )


    due_date = None


    if has_date:

        offset = random.randint(
            0,
            5,
        )

        due = (
            datetime.now()
            + timedelta(
                days=offset
            )
        )

        due_date = (
            "Today"

            if offset == 0

            else (
                "Tomorrow"

                if offset == 1

                else due.strftime(
                    "%a, %b %d"
                ).replace(
                    " 0",
                    " "
                )
            )
        )


    return {

        "id":
            f"reminder_{index}",

        "title":
            random.choice(
                titles
            ),

        "notes":
            random.choice(
                notes
            ),

        "completed":
            random.random() < 0.18,

        "flagged":
            random.random() < 0.22,

        "priority":
            random.choice([
                "none",
                "none",
                "low",
                "medium",
                "high",
            ]),

        "due_date":
            due_date,

        "due_time":
            (
                random.choice([
                    "9:00 AM",
                    "11:30 AM",
                    "2:00 PM",
                    "5:30 PM",
                    "8:00 PM",
                ])

                if has_date
                and random.random() < 0.65

                else None
            ),

        "tags":
            tags,

        "list":
            random.choice(
                CUSTOM_LISTS
            ),
    }


# ==========================================================
# Reminders
# ==========================================================

def generate_reminders(
    count: int = 14,
) -> list[dict]:

    return [

        generate_reminder(
            index
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Smart Lists
# ==========================================================

def generate_smart_lists(
    reminders: list[dict],
) -> list[dict]:

    completed_count = sum(
        1
        for reminder
        in reminders
        if reminder["completed"]
    )

    flagged_count = sum(
        1
        for reminder
        in reminders
        if reminder["flagged"]
    )


    result = []


    for definition in LIST_DEFINITIONS:

        if definition["id"] == "completed":

            count = (
                completed_count
            )

        elif definition["id"] == "flagged":

            count = (
                flagged_count
            )

        else:

            count = random.randint(
                2,
                15,
            )


        result.append({

            **definition,

            "count":
                count,

            "icon_data":
                get_lucide_icon(
                    definition["icon"]
                ),
        })


    return result


# ==========================================================
# Custom Lists
# ==========================================================

def generate_custom_lists() -> list[dict]:

    return [

        {
            **item,

            "count":
                random.randint(
                    2,
                    18,
                ),

            "icon":
                get_lucide_icon(
                    "list"
                ),
        }

        for item
        in CUSTOM_LISTS
    ]


# ==========================================================
# Tags
# ==========================================================

def generate_tags() -> list[dict]:

    definitions = [

        "work",

        "research",

        "important",

        "personal",

        "today",
    ]


    return [

        {
            "id":
                tag,

            "title":
                f"#{tag}",

            "count":
                random.randint(
                    1,
                    9,
                ),
        }

        for tag
        in definitions
    ]


# ==========================================================
# New Reminder
# ==========================================================

def generate_new_reminder() -> dict:

    return {

        "title":
            random.choice([
                "",
                "New Reminder",
                "Review notes",
            ]),

        "notes":
            random.choice([
                "",
                "Add details here",
            ]),

        "date_enabled":
            random.random() < 0.60,

        "time_enabled":
            random.random() < 0.45,

        "flagged":
            random.random() < 0.20,

        "priority":
            random.choice([
                "None",
                "Low",
                "Medium",
                "High",
            ]),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_reminders_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            REMINDERS_STATES,

            weights=
                REMINDERS_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in REMINDERS_STATES:

        raise ValueError(
            f"Unknown Reminders state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Reminders
    # ======================================================

    reminders = (
        generate_reminders()
    )


    active_reminder = random.choice(
        reminders
    )


    # ======================================================
    # Filtered Data
    # ======================================================

    completed = [

        reminder

        for reminder
        in reminders

        if reminder["completed"]
    ]


    if not completed:

        completed = reminders[:3]


    flagged = [

        reminder

        for reminder
        in reminders

        if reminder["flagged"]
    ]


    if not flagged:

        flagged = reminders[:3]


    tags = generate_tags()


    selected_tag = random.choice(
        tags
    )


    tag_filtered = [

        reminder

        for reminder
        in reminders

        if selected_tag["id"]
        in reminder["tags"]
    ]


    if not tag_filtered:

        tag_filtered = random.sample(

            reminders,

            k=min(
                4,
                len(
                    reminders
                ),
            ),
        )


    # ======================================================
    # Overlay
    # ======================================================

    is_overlay_state = (
        state
        in {
            "task_detail",
            "new_reminder",
            "delete_confirmation",
        }
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        "title":
            "Reminders",


        "reminders":
            reminders,

        "active_reminder":
            active_reminder,


        "completed":
            completed,

        "flagged":
            flagged,


        "smart_lists":
            generate_smart_lists(
                reminders
            ),

        "custom_lists":
            generate_custom_lists(),


        "tags":
            tags,

        "selected_tag":
            selected_tag,

        "tag_filtered":
            tag_filtered,


        "new_reminder":
            generate_new_reminder(),


        "delete_confirmation": {

            "title":
                "Delete Reminder?",

            "message":
                (
                    "This reminder will be "
                    "permanently deleted."
                ),

            "cancel":
                "Cancel",

            "confirm":
                "Delete Reminder",
        },


        # --------------------------------------------------
        # Icons
        # --------------------------------------------------

        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "back":
                resolve_icon(
                    "back"
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis"
                ),

            "flag":
                get_lucide_icon(
                    "flag"
                ),

            "calendar":
                resolve_icon(
                    "calendar"
                ),

            "clock":
                get_lucide_icon(
                    "clock-3"
                ),

            "tag":
                get_lucide_icon(
                    "tag"
                ),

            "list":
                get_lucide_icon(
                    "list"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "info":
                resolve_icon(
                    "info"
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right"
                ),

            "close":
                resolve_icon(
                    "close"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in REMINDERS_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_reminders_data(
                state=
                    state
            ),

            sort_dicts=False,
        )