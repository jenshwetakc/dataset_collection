from __future__ import annotations

import random

from copy import deepcopy


ALERT_STATES = [
    "overview",
    "warning_only",
    "alert_expanded",
    "empty_alerts",
    "expired_alerts",
    "notification_settings",
    "location_dialog",
]

ALERT_TYPES = [
    {
        "key": "warning",
        "label": "Warnings",
        "icon": "warning",
    },
    {
        "key": "watch",
        "label": "Watches",
        "icon": "visibility",
    },
    {
        "key": "advisory",
        "label": "Advisories",
        "icon": "info",
    },
]

ALERT_TEMPLATES = [
    {
        "title": "Heavy Rain Warning",
        "type": "warning",
        "icon": "rainy",
        "summary": "Periods of heavy rainfall are shown in this synthetic alert.",
        "details": "The simulated forecast indicates persistent rain across the selected region.",
        "areas": ["Central district", "Riverside district"],
    },
    {
        "title": "Strong Wind Warning",
        "type": "warning",
        "icon": "air",
        "summary": "Strong winds are shown in the surrounding area.",
        "details": "The simulated alert includes elevated wind speeds and occasional stronger gusts.",
        "areas": ["Coastal district", "Northern district"],
    },
    {
        "title": "Thunderstorm Watch",
        "type": "watch",
        "icon": "thunderstorm",
        "summary": "Conditions may support thunderstorms later today.",
        "details": "The synthetic forecast shows a possibility of thunderstorms during the afternoon.",
        "areas": ["Eastern district", "Central district"],
    },
    {
        "title": "Dense Fog Advisory",
        "type": "advisory",
        "icon": "foggy",
        "summary": "Reduced visibility is shown in several districts.",
        "details": "The simulated advisory describes fog during the early morning period.",
        "areas": ["Valley district", "Southern district"],
    },
]

LOCATIONS = [
    "Seoul, South Korea",
    "Busan, South Korea",
    "Tokyo, Japan",
    "London, United Kingdom",
]


def generate_alerts_data(
    *,
    sample_index: int,
) -> dict:
    alerts = []

    for index, template in enumerate(ALERT_TEMPLATES):
        alert = deepcopy(template)

        alert.update({
            "id": index,
            "issued": f"Issued {random.randint(10, 50)} minutes ago",
            "expires": "Today at 20:00",
            "status": "Active",
            "expanded": False,
        })

        alerts.append(alert)

    return {
        "sample_index": sample_index,
        "location": random.choice(LOCATIONS),
        "locations": list(LOCATIONS),
        "alerts": alerts,
        "alert_types": deepcopy(ALERT_TYPES),
        "push_enabled": random.choice([True, False]),
        "email_enabled": random.choice([True, False]),
        "enabled_types": ["warning", "watch"],
        "email": "weather.user@example.com",
        "updated_text": (
            f"Updated {random.randint(1, 8)} minutes ago"
        ),
    }


def apply_alerts_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in ALERT_STATES:
        raise ValueError(
            f"Unknown alerts state: {state!r}"
        )

    data = deepcopy(base_data)

    popup_states = {
        "notification_settings",
        "location_dialog",
    }

    data.update({
        "state": state,
        "popup_visible": state in popup_states,
        "popup_type": state if state in popup_states else None,
        "active_filter": (
            "warning"
            if state == "warning_only"
            else "all"
        ),
        "active_tab": (
            "expired"
            if state == "expired_alerts"
            else "active"
        ),
    })

    if state == "empty_alerts":
        data["alerts"] = []

    elif state == "warning_only":
        data["alerts"] = [
            alert
            for alert in data["alerts"]
            if alert["type"] == "warning"
        ]

    elif state == "expired_alerts":
        for alert in data["alerts"]:
            alert["status"] = "Expired"
            alert["issued"] = "Issued yesterday"
            alert["expires"] = "Yesterday at 20:00"

    elif state == "alert_expanded":
        data["alerts"][0]["expanded"] = True

    data["warning_count"] = sum(
        alert["type"] == "warning"
        and alert["status"] == "Active"
        for alert in data["alerts"]
    )

    data["visible_count"] = len(data["alerts"])

    return data