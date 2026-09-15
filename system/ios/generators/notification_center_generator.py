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

NOTIFICATION_CENTER_STATES = [

    "normal",

    "grouped",

    "expanded_notification",

    "notification_actions",

    "media_notification",

    "live_activity",

    "clear_confirmation",

    "empty",
]


NOTIFICATION_CENTER_STATE_WEIGHTS = [

    28,

    16,

    12,

    10,

    10,

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

    if (
        icon is None
        and fallback
    ):

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# App Definitions
# ==========================================================

APP_DEFINITIONS = [

    {
        "name":
            "Messages",

        "style":
            "green",

        "icon":
            resolve_icon(
                "message",
                "message-circle",
            ),
    },

    {
        "name":
            "Mail",

        "style":
            "blue",

        "icon":
            resolve_icon(
                "mail",
                "mail",
            ),
    },

    {
        "name":
            "Calendar",

        "style":
            "red",

        "icon":
            resolve_icon(
                "calendar",
                "calendar",
            ),
    },

    {
        "name":
            "Photos",

        "style":
            "multicolor",

        "icon":
            resolve_icon(
                "image",
                "image",
            ),
    },

    {
        "name":
            "Phone",

        "style":
            "green",

        "icon":
            resolve_icon(
                "phone",
                "phone",
            ),
    },

    {
        "name":
            "Music",

        "style":
            "red",

        "icon":
            resolve_icon(
                "music",
                "music",
            ),
    },

    {
        "name":
            "Weather",

        "style":
            "blue",

        "icon":
            get_lucide_icon(
                "cloud-sun"
            ),
    },

    {
        "name":
            "Reminders",

        "style":
            "blue",

        "icon":
            get_lucide_icon(
                "list-checks"
            ),
    },

    {
        "name":
            "Maps",

        "style":
            "green",

        "icon":
            resolve_icon(
                "map",
                "map",
            ),
    },
]


# ==========================================================
# Notification Text
# ==========================================================

NOTIFICATION_CONTENT = {

    "Messages": [

        (
            "Alex",
            "Are we still meeting at 4?"
        ),

        (
            "Project Team",
            "I uploaded the latest screenshots."
        ),

        (
            "Sam",
            "Sounds good. See you tomorrow!"
        ),
    ],


    "Mail": [

        (
            "Weekly Update",
            "Your weekly project summary is ready."
        ),

        (
            "Research Group",
            "Meeting agenda for tomorrow."
        ),

        (
            "Course Announcement",
            "New material has been posted."
        ),
    ],


    "Calendar": [

        (
            "Upcoming Event",
            "Research meeting in 30 minutes."
        ),

        (
            "Reminder",
            "Presentation rehearsal at 3:00 PM."
        ),
    ],


    "Photos": [

        (
            "Memories",
            "You have new memories from this day."
        ),
    ],


    "Phone": [

        (
            "Missed Call",
            fake.name()
        ),
    ],


    "Music": [

        (
            "New Release",
            "A new album you may like is available."
        ),
    ],


    "Weather": [

        (
            "Weather Alert",
            "Rain is expected this evening."
        ),
    ],


    "Reminders": [

        (
            "Reminder",
            random.choice([
                "Submit the report",
                "Review experiment results",
                "Send the meeting notes",
            ])
        ),
    ],


    "Maps": [

        (
            "Travel Time",
            "About 25 minutes to your destination."
        ),
    ],
}


# ==========================================================
# Time
# ==========================================================

def generate_notification_time() -> str:

    choices = [

        "now",

        "1m",

        "3m",

        "8m",

        "12m",

        "24m",

        "1h",

        "2h",
    ]

    return random.choice(
        choices
    )


# ==========================================================
# Single Notification
# ==========================================================

def generate_notification(
    index: int,
) -> dict:

    app = random.choice(
        APP_DEFINITIONS
    )


    title, message = random.choice(

        NOTIFICATION_CONTENT[
            app["name"]
        ]
    )


    return {

        "id":
            f"notification_{index}",

        "app":
            app["name"],

        "app_style":
            app["style"],

        "app_icon":
            app["icon"],

        "title":
            title,

        "message":
            message,

        "time":
            generate_notification_time(),

        "unread":
            random.random() < 0.65,

        "has_image":
            False,
    }


# ==========================================================
# Notification List
# ==========================================================

def generate_notifications(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            4,
            8,
        )


    return [

        generate_notification(
            index
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Grouped Notifications
# ==========================================================

def generate_grouped_notifications() -> dict:

    app = random.choice([

        APP_DEFINITIONS[0],

        APP_DEFINITIONS[1],

        APP_DEFINITIONS[7],
    ])


    items = []


    for index in range(
        random.randint(
            3,
            5,
        )
    ):

        title, message = random.choice(

            NOTIFICATION_CONTENT[
                app["name"]
            ]
        )


        items.append({

            "id":
                f"group_item_{index}",

            "title":
                title,

            "message":
                message,

            "time":
                generate_notification_time(),
        })


    return {

        "app":
            app["name"],

        "app_icon":
            app["icon"],

        "app_style":
            app["style"],

        "count":
            len(
                items
            ),

        "items":
            items,
    }


# ==========================================================
# Media Notification
# ==========================================================

def generate_media_notification() -> dict:

    playing = (
        random.random()
        < 0.72
    )


    return {

        "title":
            random.choice([
                "Afterglow",
                "Midnight Drive",
                "Quiet Hours",
                "City Lights",
                "Morning Focus",
            ]),

        "artist":
            random.choice([
                "Nova",
                "Night Radio",
                "Aurora",
                "Studio Sessions",
            ]),

        "playing":
            playing,

        "progress":
            random.randint(
                12,
                88,
            ),

        "icons": {

            "play":
                resolve_icon(
                    "play"
                ),

            "pause":
                resolve_icon(
                    "pause"
                ),

            "skip_back":
                resolve_icon(
                    "skip_back"
                ),

            "skip_forward":
                resolve_icon(
                    "skip_forward"
                ),
        },
    }


# ==========================================================
# Live Activity
# ==========================================================

def generate_live_activity() -> dict:

    activity_type = random.choice([

        "delivery",

        "timer",

        "navigation",
    ])


    if activity_type == "delivery":

        return {

            "type":
                "delivery",

            "title":
                "Order on the way",

            "subtitle":
                random.choice([
                    "Arriving in 12 min",
                    "Arriving in 18 min",
                    "Driver is nearby",
                ]),

            "progress":
                random.randint(
                    50,
                    92,
                ),

            "icon":
                get_lucide_icon(
                    "bike"
                ),
        }


    if activity_type == "timer":

        return {

            "type":
                "timer",

            "title":
                "Timer",

            "subtitle":
                random.choice([
                    "08:42",
                    "12:18",
                    "19:03",
                ]),

            "progress":
                random.randint(
                    20,
                    75,
                ),

            "icon":
                get_lucide_icon(
                    "timer"
                ),
        }


    return {

        "type":
            "navigation",

        "title":
            "Navigation",

        "subtitle":
            random.choice([
                "Turn right in 300 m",
                "Continue for 1.2 km",
                "Exit ahead",
            ]),

        "progress":
            random.randint(
                20,
                80,
            ),

        "icon":
            get_lucide_icon(
                "navigation"
            ),
    }


# ==========================================================
# Expanded Notification
# ==========================================================

def generate_expanded_notification(
    notifications: list[dict],
) -> dict:

    notification = random.choice(
        notifications
    )


    return {

        **notification,

        "full_message":

            notification["message"]
            +
            " "
            +
            random.choice([
                "Tap to view more details.",
                "Additional information is available.",
                "Open the app to continue.",
            ]),

        "actions": [

            {
                "id":
                    "reply",

                "label":
                    "Reply",

                "icon":
                    get_lucide_icon(
                        "reply"
                    ),
            },

            {
                "id":
                    "mark_read",

                "label":
                    "Mark as Read",

                "icon":
                    resolve_icon(
                        "check"
                    ),
            },
        ],
    }


# ==========================================================
# Notification Actions
# ==========================================================

def generate_notification_actions(
    notifications: list[dict],
) -> dict:

    target = random.choice(
        notifications
    )


    return {

        "target":
            target,

        "actions": [

            {
                "id":
                    "options",

                "label":
                    "Options",

                "icon":
                    get_lucide_icon(
                        "settings-2"
                    ),

                "destructive":
                    False,
            },

            {
                "id":
                    "clear",

                "label":
                    "Clear",

                "icon":
                    get_lucide_icon(
                        "trash-2"
                    ),

                "destructive":
                    True,
            },
        ],
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_notification_center_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choices(

            NOTIFICATION_CENTER_STATES,

            weights=
                NOTIFICATION_CENTER_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in NOTIFICATION_CENTER_STATES:

        raise ValueError(
            f"Unknown Notification Center state: {state}"
        )


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


    notifications = (

        []

        if state == "empty"

        else generate_notifications()
    )


    overlay_states = {

        "expanded_notification",

        "notification_actions",

        "clear_confirmation",
    }


    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            state
            in overlay_states,


        "date": {

            "weekday":
                datetime.now().strftime(
                    "%A"
                ),

            "month_day":
                datetime.now().strftime(
                    "%B %d"
                ).replace(
                    " 0",
                    " "
                ),
        },


        "notifications":
            notifications,


        "group":
            generate_grouped_notifications(),


        "expanded":
            (
                generate_expanded_notification(
                    notifications
                )

                if notifications
                else None
            ),


        "actions":
            (
                generate_notification_actions(
                    notifications
                )

                if notifications
                else None
            ),


        "media":
            generate_media_notification(),


        "live_activity":
            generate_live_activity(),


        "icons": {

            "close":
                resolve_icon(
                    "close"
                ),

            "clear":
                get_lucide_icon(
                    "x"
                ),

            "bell":
                resolve_icon(
                    "notifications",
                    "bell",
                ),

            "chevron":
                resolve_icon(
                    "forward",
                    "chevron-right",
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "check":
                resolve_icon(
                    "check"
                ),
        },


        "clear_confirmation": {

            "title":
                "Clear All Notifications?",

            "message":
                "This will remove all notifications from Notification Center.",

            "cancel_label":
                "Cancel",

            "confirm_label":
                "Clear All",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in NOTIFICATION_CENTER_STATES:

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

            generate_notification_center_data(
                state=
                    state
            ),

            sort_dicts=False,
        )