from __future__ import annotations

import random

from copy import deepcopy

from datetime import (
    datetime,
    timedelta,
)

from system.ios.generators.media_generators import (
    get_random_wallpaper,
)


# ==========================================================
# Lock Screen States
# ==========================================================

LOCK_SCREEN_STATES = [
    "normal",
    "notifications",
    "music",
    "incoming_call",
    "charging",
    "passcode_prompt",
]


LOCK_SCREEN_STATE_WEIGHTS = [
    28,
    22,
    16,
    12,
    12,
    10,
]


# ==========================================================
# Gradient Wallpaper Fallbacks
# ==========================================================

LOCK_WALLPAPER_FALLBACKS = [

    {
        "name": "night_blue",
        "background": (
            "linear-gradient("
            "160deg,"
            "#17233F 0%,"
            "#334867 48%,"
            "#172032 100%"
            ")"
        ),
    },

    {
        "name": "purple_glow",
        "background": (
            "radial-gradient("
            "circle at 65% 18%,"
            "#8D6AA8 0%,"
            "#473A61 38%,"
            "#1B2237 100%"
            ")"
        ),
    },

    {
        "name": "ocean",
        "background": (
            "linear-gradient("
            "145deg,"
            "#3E7B92 0%,"
            "#31546D 42%,"
            "#1A2A3F 100%"
            ")"
        ),
    },

    {
        "name": "sunset",
        "background": (
            "radial-gradient("
            "circle at 28% 18%,"
            "#D68B7E 0%,"
            "#80556E 42%,"
            "#29324D 100%"
            ")"
        ),
    },

    {
        "name": "forest",
        "background": (
            "linear-gradient("
            "155deg,"
            "#45675D 0%,"
            "#2D4A49 43%,"
            "#172B34 100%"
            ")"
        ),
    },
]


# ==========================================================
# Notification Sources
# ==========================================================

NOTIFICATION_SOURCES = [

    {
        "app": "Messages",
        "symbol": "●",
        "style": "green",
    },

    {
        "app": "Mail",
        "symbol": "✉",
        "style": "blue",
    },

    {
        "app": "Calendar",
        "symbol": "17",
        "style": "calendar",
    },

    {
        "app": "Reminders",
        "symbol": "✓",
        "style": "white",
    },

    {
        "app": "News",
        "symbol": "N",
        "style": "red",
    },

    {
        "app": "Maps",
        "symbol": "↗",
        "style": "maps",
    },

    {
        "app": "Music",
        "symbol": "♫",
        "style": "music",
    },
]


# ==========================================================
# Notification Content
# ==========================================================

NOTIFICATION_CONTENT = {

    "Messages": [
        (
            "Alex",
            "Are we still meeting later?"
        ),

        (
            "Mina",
            "I sent you the document."
        ),

        (
            "Project Group",
            "The meeting has been moved to 4 PM."
        ),

        (
            "Daniel",
            "Sounds good. See you soon!"
        ),
    ],


    "Mail": [
        (
            "University",
            "New announcement available"
        ),

        (
            "Research Team",
            "Updated experiment results"
        ),

        (
            "Newsletter",
            "Your weekly digest is ready"
        ),
    ],


    "Calendar": [
        (
            "Upcoming",
            "Team meeting in 15 minutes"
        ),

        (
            "Today",
            "Research presentation at 2:30 PM"
        ),
    ],


    "Reminders": [
        (
            "Reminder",
            "Submit weekly progress report"
        ),

        (
            "Reminder",
            "Review experiment results"
        ),
    ],


    "News": [
        (
            "Top Stories",
            "New technology updates available"
        ),

        (
            "Morning Briefing",
            "Five stories to start your day"
        ),
    ],


    "Maps": [
        (
            "Travel Time",
            "Home is 24 minutes away"
        ),

        (
            "Maps",
            "Traffic is lighter than usual"
        ),
    ],


    "Music": [
        (
            "Music",
            "Your new mix is ready"
        ),

        (
            "Music",
            "Continue listening?"
        ),
    ],
}


# ==========================================================
# Music Library
# ==========================================================

MUSIC_LIBRARY = [

    {
        "title": "Midnight Drive",
        "artist": "The Echoes",
        "album": "Night Signals",
    },

    {
        "title": "Blue Horizon",
        "artist": "Arden",
        "album": "Coastline",
    },

    {
        "title": "After Rain",
        "artist": "Nova Lane",
        "album": "Reflections",
    },

    {
        "title": "Parallel Lines",
        "artist": "Northbound",
        "album": "Motion",
    },

    {
        "title": "Quiet Morning",
        "artist": "Mira",
        "album": "Soft Light",
    },
]


# ==========================================================
# Callers
# ==========================================================

CALLERS = [
    "Alex",
    "Mina",
    "Daniel",
    "Emma",
    "Jordan",
    "Chris",
    "Sophia",
    "Research Group",
]


# ==========================================================
# Passcode Messages
# ==========================================================

PASSCODE_MESSAGES = [
    "Enter Passcode",
    "iPhone requires your passcode after restarting",
    "Face ID requires your passcode",
]


# ==========================================================
# Wallpaper Generator
# ==========================================================

def generate_lock_wallpaper() -> dict:

    image = (
        get_random_wallpaper()
    )

    fallback = deepcopy(
        random.choice(
            LOCK_WALLPAPER_FALLBACKS
        )
    )

    if image:

        return {

            "type":
                "image",

            "image":
                image,

            "name":
                "local_wallpaper",

            "background":
                fallback[
                    "background"
                ],
        }

    return {

        "type":
            "gradient",

        "image":
            None,

        "name":
            fallback[
                "name"
            ],

        "background":
            fallback[
                "background"
            ],
    }


# ==========================================================
# Date
# ==========================================================

def generate_lock_date() -> dict:

    base = datetime.now()

    offset = timedelta(
        days=random.randint(
            -20,
            20,
        )
    )

    value = (
        base
        + offset
    )

    return {

        "weekday":
            value.strftime(
                "%A"
            ),

        "month_day":
            value.strftime(
                "%B %d"
            ).replace(
                " 0",
                " ",
            ),
    }


# ==========================================================
# Time
# ==========================================================

def generate_lock_time() -> str:

    hour = random.randint(
        1,
        12,
    )

    minute = random.randint(
        0,
        59,
    )

    return (
        f"{hour}:"
        f"{minute:02d}"
    )


# ==========================================================
# Notification Time
# ==========================================================

def generate_notification_time() -> str:

    return random.choice([
        "now",
        "1m ago",
        "2m ago",
        "5m ago",
        "8m ago",
        "12m ago",
        "20m ago",
        "1h ago",
    ])


# ==========================================================
# Notifications
# ==========================================================

def generate_notifications() -> list[dict]:

    count = random.randint(
        2,
        5,
    )

    selected_sources = (
        random.choices(
            NOTIFICATION_SOURCES,
            k=count,
        )
    )

    result = []

    for index, source in enumerate(
        selected_sources
    ):

        source = deepcopy(
            source
        )

        title, message = random.choice(
            NOTIFICATION_CONTENT[
                source[
                    "app"
                ]
            ]
        )

        result.append({

            "id":
                f"notification_{index}",

            "app":
                source[
                    "app"
                ],

            "symbol":
                source[
                    "symbol"
                ],

            "style":
                source[
                    "style"
                ],

            "title":
                title,

            "message":
                message,

            "time":
                generate_notification_time(),
        })

    return result


# ==========================================================
# Music
# ==========================================================

def generate_music_data() -> dict:

    track = deepcopy(
        random.choice(
            MUSIC_LIBRARY
        )
    )

    duration = random.randint(
        180,
        320,
    )

    current = random.randint(
        15,
        duration - 20,
    )

    track.update({

        "playing":
            random.random()
            < 0.72,

        "duration":
            duration,

        "current":
            current,

        "progress":
            round(
                current
                / duration
                * 100,
                1,
            ),
    })

    return track


# ==========================================================
# Incoming Call
# ==========================================================

def generate_call_data() -> dict:

    return {

        "caller":
            random.choice(
                CALLERS
            ),

        "call_type":
            random.choice([
                "mobile",
                "FaceTime Audio",
                "FaceTime Video",
            ]),

        "label":
            "incoming call",
    }


# ==========================================================
# Charging
# ==========================================================

def generate_charging_data() -> dict:

    battery_level = random.randint(
        15,
        95,
    )

    return {

        "battery_level":
            battery_level,

        "charging_text":
            random.choice([
                "Charging",
                "Charging on Hold",
            ]),

        "estimated":
            random.choice([
                None,
                "80% by 7:15 AM",
                "Fully Charged by 8:30 AM",
            ]),
    }


# ==========================================================
# Passcode
# ==========================================================

def generate_passcode_data() -> dict:

    return {

        "title":
            random.choice(
                PASSCODE_MESSAGES
            ),

        "digits_entered":
            random.randint(
                0,
                4,
            ),

        "total_digits":
            6,
    }


# ==========================================================
# Main Lock Screen Generator
# ==========================================================

def generate_lock_screen_data(
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choices(
            LOCK_SCREEN_STATES,
            weights=
                LOCK_SCREEN_STATE_WEIGHTS,
            k=1,
        )[0]

    if state not in LOCK_SCREEN_STATES:

        raise ValueError(
            f"Unknown lock screen state: "
            f"{state}. "
            f"Available states: "
            f"{LOCK_SCREEN_STATES}"
        )


    return_data = {

        "state":
            state,

        "wallpaper":
            generate_lock_wallpaper(),

        "time":
            generate_lock_time(),

        "date":
            generate_lock_date(),

        "notifications":
            [],

        "music":
            None,

        "incoming_call":
            None,

        "charging":
            None,

        "passcode":
            None,

        "show_flashlight":
            True,

        "show_camera":
            True,

        "show_home_indicator":
            True,

        "is_overlay_state":
            state in {
                "incoming_call",
                "passcode_prompt",
            },
    }


    if state == "notifications":

        return_data[
            "notifications"
        ] = (
            generate_notifications()
        )


    elif state == "music":

        return_data[
            "music"
        ] = (
            generate_music_data()
        )


    elif state == "incoming_call":

        return_data[
            "incoming_call"
        ] = (
            generate_call_data()
        )


    elif state == "charging":

        return_data[
            "charging"
        ] = (
            generate_charging_data()
        )


    elif state == "passcode_prompt":

        return_data[
            "passcode"
        ] = (
            generate_passcode_data()
        )


    return return_data


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    example_viewport = {

        "name":
            "standard_iphone",

        "category":
            "mobile",

        "orientation":
            "portrait",

        "size_class":
            "compact",

        "width":
            390,

        "height":
            844,

        "dpr":
            3,
    }


    for state in LOCK_SCREEN_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state.upper()
        )

        print(
            "=========================================="
        )

        pprint(
            generate_lock_screen_data(
                viewport=
                    example_viewport,

                state=
                    state,
            ),
            sort_dicts=False,
        )