from __future__ import annotations

import calendar
import copy
import random
from datetime import date


CALENDAR_STATES = (
    "overview",
    "rainy_month",
    "day_selected",
    "agenda_view",
    "saved_plans",
    "add_plan_dialog",
    "calendar_settings",
)

CONDITIONS = (
    ("Sunny", "sunny"),
    ("Partly cloudy", "partly_cloudy_day"),
    ("Cloudy", "cloud"),
    ("Light rain", "rainy"),
    ("Windy", "air"),
)

PLAN_TYPES = (
    ("Walking", "directions_walk"),
    ("Cycling", "directions_bike"),
    ("Photography", "photo_camera"),
    ("Picnic", "park"),
)


def generate_calendar_data(
    *,
    sample_index: int,
) -> dict:
    year, month = 2026, 10
    days = []

    for number in range(
        1,
        calendar.monthrange(year, month)[1] + 1,
    ):
        condition, icon = random.choice(CONDITIONS)
        high = random.randint(18, 27)
        low = high - random.randint(5, 10)
        wet = icon == "rainy"

        days.append({
            "number": number,
            "weekday": date(
                year, month, number
            ).strftime("%A"),
            "condition": condition,
            "icon": icon,
            "high": high,
            "low": low,
            "precipitation": (
                random.randint(60, 95)
                if wet
                else random.randint(0, 25)
            ),
            "wind": random.randint(6, 28),
            "humidity": random.randint(40, 85),
            "selected": False,
            "plans": [],
        })

    plans = [
        {
            "id": "plan_1",
            "day": 8,
            "title": "Riverside walk",
            "time": "08:30",
            "type": "Walking",
            "icon": "directions_walk",
            "reminder": True,
        },
        {
            "id": "plan_2",
            "day": 14,
            "title": "Weekend photo route",
            "time": "16:00",
            "type": "Photography",
            "icon": "photo_camera",
            "reminder": False,
        },
        {
            "id": "plan_3",
            "day": 22,
            "title": "Park picnic",
            "time": "12:00",
            "type": "Picnic",
            "icon": "park",
            "reminder": True,
        },
        {
            "id": "plan_4",
            "day": 27,
            "title": "Evening cycling",
            "time": "17:30",
            "type": "Cycling",
            "icon": "directions_bike",
            "reminder": True,
        },
    ]

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "dialog_type": None,
        "city": "Seoul",
        "year": year,
        "month": month,
        "month_label": "October 2026",
        "today": 6,
        "days": days,
        "plans": plans,
        "selected_number": 8,
        "view": "calendar",
        "plan_types": list(PLAN_TYPES),
        "draft": {
            "title": "Morning walk",
            "date_text": "October 8, 2026",
            "time": "08:30",
            "type": "Walking",
            "reminder": True,
        },
        "settings": {
            "show_precipitation": True,
            "show_plans": True,
            "week_start": "Monday",
        },
    }


def apply_calendar_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in CALENDAR_STATES:
        raise ValueError(
            f"Unknown calendar state: {state}"
        )

    data = copy.deepcopy(base_data)
    data["state"] = state

    if state == "rainy_month":
        for day in data["days"]:
            if day["number"] % 3 != 0:
                day["condition"] = "Rain"
                day["icon"] = "rainy"
                day["precipitation"] = random.randint(65, 95)

    elif state == "day_selected":
        data["selected_number"] = 22

    elif state == "agenda_view":
        data["view"] = "agenda"

    elif state == "saved_plans":
        data["view"] = "plans"

    elif state in {
        "add_plan_dialog",
        "calendar_settings",
    }:
        data["popup_visible"] = True
        data["dialog_type"] = (
            "plan"
            if state == "add_plan_dialog"
            else "settings"
        )

    for plan in data["plans"]:
        data["days"][plan["day"] - 1]["plans"].append(
            copy.deepcopy(plan)
        )

    for day in data["days"]:
        day["selected"] = (
            day["number"] == data["selected_number"]
        )

    data["selected_day"] = copy.deepcopy(
        data["days"][data["selected_number"] - 1]
    )

    for plan in data["plans"]:
        day = data["days"][plan["day"] - 1]
        plan["condition"] = day["condition"]
        plan["weather_icon"] = day["icon"]
        plan["high"] = day["high"]
        plan["precipitation"] = day["precipitation"]

    data["rainy_days"] = sum(
        day["icon"] == "rainy"
        for day in data["days"]
    )
    data["average_high"] = round(
        sum(day["high"] for day in data["days"])
        / len(data["days"])
    )
    data["clear_days"] = sum(
        day["icon"] == "sunny"
        for day in data["days"]
    )

    week_start = (
        calendar.MONDAY
        if data["settings"]["week_start"] == "Monday"
        else calendar.SUNDAY
    )

    month_calendar = calendar.Calendar(
        firstweekday=week_start
    )
    lookup = {
        day["number"]: day
        for day in data["days"]
    }

    data["weeks"] = [
        [
            lookup[number] if number else None
            for number in week
        ]
        for week in month_calendar.monthdayscalendar(
            data["year"], data["month"]
        )
    ]

    data["weekday_labels"] = (
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if week_start == calendar.MONDAY
        else ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    )

    return data