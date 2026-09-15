from __future__ import annotations

import random

from faker import Faker

from social_media.kindle.generators.media_generator import (
    get_random_book_cover,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

READING_INSIGHT_STATES = [
    "overview",
    "weekly_activity",
    "monthly_activity",
    "goal_progress",
    "edit_goal",
    "date_range_menu",
    "achievement_popup",
    "empty_history",
]


# ==========================================================
# Book Titles
# ==========================================================

BOOK_TITLES = [
    "The Silent Horizon",
    "Fragments of Memory",
    "Beyond the Last City",
    "Understanding Tomorrow",
    "The Hidden Machine",
    "Notes from the River",
    "The Art of Thinking",
    "Echoes of History",
]


# ==========================================================
# Week Days
# ==========================================================

WEEK_DAYS = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
]


# ==========================================================
# Recent Session
# ==========================================================

def generate_session(
    index: int,
) -> dict:

    duration_minutes = random.randint(
        8,
        96,
    )

    return {

        "id":
            f"session_{index:03d}",

        "book_title":
            random.choice(
                BOOK_TITLES
            ),

        "cover":
            get_random_book_cover(),

        "duration":
            duration_minutes,

        "pages":
            random.randint(
                5,
                64,
            ),

        "progress_gain":
            random.randint(
                1,
                18,
            ),

        "time":
            random.choice(
                [
                    "8:12 AM",
                    "11:45 AM",
                    "2:18 PM",
                    "6:30 PM",
                    "9:14 PM",
                    "11:02 PM",
                ]
            ),

        "date":
            random.choice(
                [
                    "Today",
                    "Yesterday",
                    "2 days ago",
                    "3 days ago",
                    "Last week",
                ]
            ),
    }


# ==========================================================
# Weekly Activity
# ==========================================================

def generate_weekly_activity() -> list[dict]:

    return [
        {
            "day":
                day,

            "minutes":
                random.randint(
                    0,
                    95,
                ),

            "goal_met":
                random.random()
                < 0.45,
        }
        for day in WEEK_DAYS
    ]


# ==========================================================
# Monthly Activity
# ==========================================================

def generate_monthly_activity() -> list[dict]:

    return [
        {
            "day":
                day,

            "minutes":
                random.choice(
                    [
                        0,
                        0,
                        random.randint(
                            5,
                            30,
                        ),
                        random.randint(
                            30,
                            70,
                        ),
                        random.randint(
                            70,
                            120,
                        ),
                    ]
                ),
        }
        for day in range(
            1,
            31,
        )
    ]


# ==========================================================
# Achievements
# ==========================================================

def generate_achievements() -> list[dict]:

    return [
        {
            "title":
                "7-day streak",

            "description":
                "Read for seven days in a row.",

            "icon":
                "local_fire_department",

            "earned":
                True,
        },
        {
            "title":
                "Night reader",

            "description":
                "Read after 10 PM five times.",

            "icon":
                "dark_mode",

            "earned":
                random.random()
                < 0.7,
        },
        {
            "title":
                "Book finisher",

            "description":
                "Finish three books.",

            "icon":
                "verified",

            "earned":
                random.random()
                < 0.6,
        },
        {
            "title":
                "Focused reader",

            "description":
                "Read for 60 minutes in one session.",

            "icon":
                "timer",

            "earned":
                random.random()
                < 0.5,
        },
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_reading_insights_page() -> dict:

    state = random.choice(
        READING_INSIGHT_STATES
    )

    daily_goal = random.choice(
        [
            15,
            20,
            30,
            45,
            60,
        ]
    )

    today_minutes = random.randint(
        0,
        95,
    )

    weekly_minutes = random.randint(
        80,
        420,
    )

    monthly_minutes = random.randint(
        300,
        1800,
    )

    streak = random.randint(
        0,
        32,
    )

    books_finished = random.randint(
        0,
        14,
    )

    sessions = [
        generate_session(
            index
        )
        for index in range(
            random.randint(
                5,
                10,
            )
        )
    ]


    # ======================================================
    # Empty State
    # ======================================================

    if state == "empty_history":

        sessions = []

        today_minutes = 0

        weekly_minutes = 0

        monthly_minutes = 0

        streak = 0

        books_finished = 0


    # ======================================================
    # Popup States
    # ======================================================

    show_edit_goal = (
        state
        == "edit_goal"
    )

    show_date_range_menu = (
        state
        == "date_range_menu"
    )

    show_achievement_popup = (
        state
        == "achievement_popup"
    )

    popup_open = any(
        [
            show_edit_goal,
            show_date_range_menu,
            show_achievement_popup,
        ]
    )


    # ======================================================
    # Goal Progress
    # ======================================================

    goal_progress = min(
        100,
        round(
            (
                today_minutes
                / daily_goal
            )
            * 100
        )
        if daily_goal > 0
        else 0,
    )


    # ======================================================
    # Date Range
    # ======================================================

    if state == "monthly_activity":

        selected_range = "This month"

    elif state == "weekly_activity":

        selected_range = "This week"

    else:

        selected_range = random.choice(
            [
                "This week",
                "This month",
            ]
        )


    # ======================================================
    # Achievement Popup
    # ======================================================

    achievements = (
        generate_achievements()
    )

    earned_achievements = [
        achievement
        for achievement
        in achievements
        if achievement[
            "earned"
        ]
    ]

    active_achievement = (
        random.choice(
            earned_achievements
        )
        if earned_achievements
        else achievements[0]
    )


    return {

        "state":
            state,

        "popup_open":
            popup_open,

        "show_edit_goal":
            show_edit_goal,

        "show_date_range_menu":
            show_date_range_menu,

        "show_achievement_popup":
            show_achievement_popup,

        "show_empty":
            state
            == "empty_history",


        # ==================================================
        # Summary
        # ==================================================

        "today_minutes":
            today_minutes,

        "weekly_minutes":
            weekly_minutes,

        "monthly_minutes":
            monthly_minutes,

        "daily_goal":
            daily_goal,

        "goal_progress":
            goal_progress,

        "streak":
            streak,

        "books_finished":
            books_finished,

        "pages_read":
            random.randint(
                40,
                980,
            )
            if state != "empty_history"
            else 0,


        # ==================================================
        # Activity
        # ==================================================

        "weekly_activity":
            generate_weekly_activity(),

        "monthly_activity":
            generate_monthly_activity(),

        "selected_range":
            selected_range,


        # ==================================================
        # Sessions
        # ==================================================

        "sessions":
            sessions,


        # ==================================================
        # Achievements
        # ==================================================

        "achievements":
            achievements,

        "active_achievement":
            active_achievement,
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_reading_insights_page()
    )

    print(
        "\n=============================="
    )

    print(
        "KINDLE READING INSIGHTS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        page["state"],
    )

    print(
        "Today:",
        page["today_minutes"],
    )

    print(
        "Goal:",
        page["daily_goal"],
    )

    print(
        "Popup:",
        page["popup_open"],
    )