from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)


# ==========================================================
# Lock Screen Notification Apps
# ==========================================================

NOTIFICATION_APPS = [

    {
        "name":
            "Messages",

        "icon":
            "mdi:message-text-outline",
    },

    {
        "name":
            "Gmail",

        "icon":
            "mdi:email-outline",
    },

    {
        "name":
            "Calendar",

        "icon":
            "mdi:calendar-outline",
    },

    {
        "name":
            "Phone",

        "icon":
            "mdi:phone-outline",
    },

    {
        "name":
            "Photos",

        "icon":
            "mdi:image-outline",
    },

    {
        "name":
            "System",

        "icon":
            "mdi:cog-outline",
    },
]


NOTIFICATION_TITLES = [
    "New message",
    "Upcoming event",
    "Missed call",
    "Backup complete",
    "New photo memory",
    "Security update",
    "New email",
]


NOTIFICATION_BODIES = [
    "Tap to view",
    "You have new activity",
    "Open to see more",
    "Your device has finished syncing",
    "A new notification is waiting",
]


# ==========================================================
# Wallpapers
# ==========================================================

WALLPAPERS = [

    {
        "name":
            "ocean",

        "gradient":
            (
                "linear-gradient("
                "160deg,"
                "#0B3D91 0%,"
                "#1A73E8 42%,"
                "#73C8F0 100%"
                ")"
            ),
    },

    {
        "name":
            "sunset",

        "gradient":
            (
                "linear-gradient("
                "160deg,"
                "#3A1C71 0%,"
                "#D76D77 48%,"
                "#FFAF7B 100%"
                ")"
            ),
    },

    {
        "name":
            "forest",

        "gradient":
            (
                "linear-gradient("
                "160deg,"
                "#0F2027 0%,"
                "#203A43 45%,"
                "#2C5364 100%"
                ")"
            ),
    },

    {
        "name":
            "violet",

        "gradient":
            (
                "linear-gradient("
                "160deg,"
                "#24133C 0%,"
                "#6B3FA0 52%,"
                "#B47AEA 100%"
                ")"
            ),
    },

    {
        "name":
            "night",

        "gradient":
            (
                "linear-gradient("
                "165deg,"
                "#05070C 0%,"
                "#101827 50%,"
                "#22314A 100%"
                ")"
            ),
    },
]


# ==========================================================
# Unlock Methods
# ==========================================================

UNLOCK_METHODS = [
    {
        "method":
            "fingerprint",

        "icon":
            "mdi:fingerprint",

        "message":
            "Touch the fingerprint sensor",
    },

    {
        "method":
            "face",

        "icon":
            "mdi:face-recognition",

        "message":
            "Looking for your face",
    },

    {
        "method":
            "pin",

        "icon":
            "mdi:dialpad",

        "message":
            "Swipe up to enter PIN",
    },
]


# ==========================================================
# Media
# ==========================================================

MEDIA_TRACKS = [
    {
        "title":
            "Late Night Drive",

        "artist":
            "Daily Mix",
    },

    {
        "title":
            "Focus Flow",

        "artist":
            "Various Artists",
    },

    {
        "title":
            "Morning News",

        "artist":
            "Daily Brief",
    },

    {
        "title":
            "Ambient Space",

        "artist":
            "Relax Mix",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_lock_notification(
    index: int,
) -> dict:

    app = random.choice(
        NOTIFICATION_APPS
    )

    return {

        "semantic":
            f"lock_notification_{index}",

        "app":
            app["name"],

        "icon":
            app["icon"],

        "title":
            random.choice(
                NOTIFICATION_TITLES
            ),

        "body":
            random.choice(
                NOTIFICATION_BODIES
            ),

        "time":
            random.choice([
                "now",
                "2m",
                "8m",
                "15m",
                "1h",
            ]),

        "expanded":
            random.random()
            < 0.22,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_lock_screen_data() -> dict:

    # ======================================================
    # Time
    # ======================================================

    now = (
        datetime.now()
        + timedelta(
            minutes=random.randint(
                -90,
                90,
            )
        )
    )

    time_text = now.strftime(
        "%H:%M"
    )

    date_text = now.strftime(
        "%A, %B %d"
    )


    # ======================================================
    # Main States
    # ======================================================

    charging = (
        random.random()
        < 0.26
    )

    battery_level = (
        random.randint(
            5,
            100,
        )
    )

    low_battery = (
        battery_level
        <= 15
    )

    do_not_disturb = (
        random.random()
        < 0.18
    )

    show_media = (
        random.random()
        < 0.42
    )

    show_emergency = (
        random.random()
        < 0.18
    )

    show_weather = (
        random.random()
        < 0.65
    )


    # ======================================================
    # Notifications
    # ======================================================

    notification_count = (
        random.randint(
            0,
            4,
        )
    )

    notifications = [

        generate_lock_notification(
            index
        )

        for index in range(
            notification_count
        )
    ]


    # ======================================================
    # Unlock
    # ======================================================

    unlock = random.choice(
        UNLOCK_METHODS
    )


    # ======================================================
    # Wallpaper
    # ======================================================

    wallpaper = random.choice(
        WALLPAPERS
    )


    # ======================================================
    # Media
    # ======================================================

    track = random.choice(
        MEDIA_TRACKS
    )

    media_playing = (
        random.random()
        < 0.65
    )


    # ======================================================
    # Weather
    # ======================================================

    weather_temp = (
        random.randint(
            5,
            31,
        )
    )

    weather_type = random.choice([
        {
            "label":
                "Clear",
            "icon":
                "mdi:weather-sunny",
        },
        {
            "label":
                "Cloudy",
            "icon":
                "mdi:weather-cloudy",
        },
        {
            "label":
                "Rain",
            "icon":
                "mdi:weather-rainy",
        },
        {
            "label":
                "Partly cloudy",
            "icon":
                "mdi:weather-partly-cloudy",
        },
    ])


    # ======================================================
    # Status Message
    # ======================================================

    if charging:

        charging_time = random.choice([
            "1 hr 12 min until full",
            "48 min until full",
            "Charging rapidly",
            "Charging",
        ])

        status_message = (
            f"{battery_level}% · "
            f"{charging_time}"
        )

    elif low_battery:

        status_message = (
            f"{battery_level}% · "
            "Battery low"
        )

    else:

        status_message = (
            f"{battery_level}%"
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "time":
            time_text,

        "date":
            date_text,

        "wallpaper":
            wallpaper,

        "battery_level":
            battery_level,

        "charging":
            charging,

        "low_battery":
            low_battery,

        "status_message":
            status_message,

        "do_not_disturb":
            do_not_disturb,

        "show_weather":
            show_weather,

        "weather": {

            "temperature":
                weather_temp,

            "label":
                weather_type["label"],

            "icon":
                weather_type["icon"],
        },

        "unlock":
            unlock,

        "show_emergency":
            show_emergency,

        "notifications":
            notifications,

        "notification_count":
            notification_count,

        "show_media":
            show_media,

        "media": {

            "title":
                track["title"],

            "artist":
                track["artist"],

            "playing":
                media_playing,

            "play_pause_icon":
                (
                    "mdi:pause"
                    if media_playing
                    else "mdi:play"
                ),
        },
    }