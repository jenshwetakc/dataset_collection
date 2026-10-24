from __future__ import annotations

import random
from datetime import date, timedelta

from faker import Faker


fake = Faker()


CHANNELS = [
    "Organic Search",
    "Direct",
    "Referral",
    "Organic Social",
    "Email",
    "Paid Search",
]

COUNTRIES = [
    "United States",
    "South Korea",
    "Germany",
    "Japan",
    "Canada",
    "Australia",
]


def random_series(
    length: int,
    minimum: int,
    maximum: int,
) -> list[int]:
    return [
        random.randint(minimum, maximum)
        for _ in range(length)
    ]


def calculate_change() -> str:
    sign = random.choice(["+", "-"])

    return (
        f"{sign}"
        f"{random.uniform(1.1, 28.0):.1f}%"
    )


def generate_metric(
    label: str,
    value: str,
) -> dict:
    return {
        "label": label,
        "value": value,
        "change": calculate_change(),
        "trend": random_series(
            length=12,
            minimum=25,
            maximum=100,
        ),
    }


def generate_channel_rows() -> list[dict]:
    rows = []

    for channel in CHANNELS:
        users = random.randint(300, 20_000)
        sessions = users + random.randint(
            50,
            max(200, users),
        )

        rows.append(
            {
                "channel": channel,
                "users": users,
                "sessions": sessions,
                "engagement_rate": (
                    f"{random.uniform(32, 78):.1f}%"
                ),
                "conversions": random.randint(
                    5,
                    max(20, users // 30),
                ),
            }
        )

    return rows


def generate_country_rows() -> list[dict]:
    return [
        {
            "country": country,
            "users": random.randint(
                150,
                18_000,
            ),
            "sessions": random.randint(
                200,
                25_000,
            ),
        }
        for country in COUNTRIES
    ]


def generate_analytics_data() -> dict:
    property_name = (
        f"{fake.company()} "
        f"Website"
    )

    end_date = date.today()
    start_date = (
        end_date
        - timedelta(days=27)
    )

    channel_rows = generate_channel_rows()
    country_rows = generate_country_rows()

    state = random.choices(
        [
            "overview",
            "reports",
            "acquisition",
            "date_range_dialog",
            "empty_property",
        ],
        weights=[
            36,
            22,
            22,
            12,
            8,
        ],
        k=1,
    )[0]

    return {
        "app_name": "Google Analytics",
        "state": state,
        "property": {
            "name": property_name,
            "id": (
                f"{random.randint(100000000, 999999999)}"
            ),
            "stream_name": (
                f"{fake.domain_word()}.com"
            ),
        },
        "date_range": {
            "label": (
                f"{start_date.strftime('%b %-d')} – "
                f"{end_date.strftime('%b %-d, %Y')}"
            ),
            "start_text": start_date.strftime(
                "%b %-d, %Y"
            ),
            "end_text": end_date.strftime(
                "%b %-d, %Y"
            ),
        },
        "metrics": [
            generate_metric(
                label="Active users",
                value=f"{random.randint(12_000, 250_000):,}",
            ),
            generate_metric(
                label="New users",
                value=f"{random.randint(8_000, 180_000):,}",
            ),
            generate_metric(
                label="Sessions",
                value=f"{random.randint(18_000, 380_000):,}",
            ),
            generate_metric(
                label="Engagement rate",
                value=(
                    f"{random.uniform(42, 77):.1f}%"
                ),
            ),
        ],
        "daily_users": random_series(
            length=28,
            minimum=100,
            maximum=850,
        ),
        "channel_rows": channel_rows,
        "country_rows": country_rows,
        "selected_channel": random.choice(
            channel_rows
        ),
        "top_pages": [
            {
                "path": random.choice(
                    [
                        "/",
                        "/pricing",
                        "/products",
                        "/blog",
                        "/about",
                        "/contact",
                    ]
                ),
                "views": random.randint(
                    800,
                    50_000,
                ),
                "users": random.randint(
                    300,
                    30_000,
                ),
            }
            for _ in range(6)
        ],
    }