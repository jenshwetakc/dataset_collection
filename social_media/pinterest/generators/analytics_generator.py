from __future__ import annotations

import random
from copy import deepcopy
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


ANALYTICS_STATES = [
    "overview",
    "organic",
    "chart_tooltip",
    "empty",
    "filters_dialog",
    "export_dialog",
]

POPUP_STATES = {
    "filters_dialog",
    "export_dialog",
}


def build_chart(series: list[int]) -> dict:
    width = 900
    height = 240
    left, right, top, bottom = 60, 20, 20, 35

    maximum = max(max(series), 1)
    scale_max = max(100, ((maximum + 99) // 100) * 100)

    points = [
        {
            "x": round(
                left + index * (width - left - right) / (len(series) - 1),
                2,
            ),
            "y": round(
                top + (1 - value / scale_max) * (height - top - bottom),
                2,
            ),
            "value": value,
        }
        for index, value in enumerate(series)
    ]

    return {
        "points": points,
        "polyline": " ".join(
            f"{point['x']},{point['y']}" for point in points
        ),
        "ticks": [
            {
                "y": round(
                    top + index * (height - top - bottom) / 4,
                    2,
                ),
                "label": f"{round(scale_max * (1 - index / 4)):,}",
            }
            for index in range(5)
        ],
        "highlight": points[14],
    }


def update_metrics(data: dict) -> None:
    impressions = sum(data["series"])
    engagements = round(impressions * 0.065)
    saves = round(engagements * 0.3)
    outbound = round(engagements * 0.2)

    data["metrics"] = [
        {"label": "Impressions", "value": f"{impressions:,}"},
        {"label": "Engagements", "value": f"{engagements:,}"},
        {"label": "Saves", "value": f"{saves:,}"},
        {"label": "Outbound clicks", "value": f"{outbound:,}"},
    ]
    data["chart"] = build_chart(data["series"])


def generate_analytics_data(seed: int | None = None) -> dict:
    rng = random.Random(seed)
    fake = Faker()

    if seed is not None:
        fake.seed_instance(seed)

    end = datetime.now(ZoneInfo("Asia/Seoul")).date() - timedelta(days=1)
    start = end - timedelta(days=29)

    rows = []

    for _ in range(8):
        impressions = rng.randint(800, 5000)
        rows.append({
            "title": fake.sentence(nb_words=5).rstrip("."),
            "image": get_random_image(ASSETS_ROOT),
            "impressions": impressions,
            "saves": rng.randint(10, 90),
            "outbound": rng.randint(5, 60),
        })

    rows.sort(key=lambda row: row["impressions"], reverse=True)

    data = {
        "state": "overview",
        "popup_visible": False,
        "business_name": fake.company(),
        "content_type": "All",
        "device": "All devices",
        "date_start": start.isoformat(),
        "date_end": end.isoformat(),
        "highlight_date": (start + timedelta(days=14)).isoformat(),
        "series": [rng.randint(1200, 4500) for _ in range(30)],
        "rows": rows,
    }

    update_metrics(data)
    return data


def create_analytics_state(base_data: dict, state: str) -> dict:
    if state not in ANALYTICS_STATES:
        raise ValueError(f"Unknown Analytics state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in POPUP_STATES

    if state == "organic":
        data["content_type"] = "Organic"
        data["series"] = [round(value * 0.7) for value in data["series"]]

        for row in data["rows"]:
            for key in ["impressions", "saves", "outbound"]:
                row[key] = round(row[key] * 0.7)

    if state == "empty":
        data["series"] = [0] * 30
        data["rows"] = []

    update_metrics(data)
    return data