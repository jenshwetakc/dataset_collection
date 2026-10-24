from __future__ import annotations

import random
from copy import deepcopy
from datetime import date, timedelta

from faker import Faker

from social_media.webtoon.generators.reader_generator import (
    generate_footer_data,
)


fake = Faker()

NOTICE_STATES = [
    "overview",
    "updates",
    "events",
    "page_two",
    "search_results",
    "search_empty",
    "article_expanded",
    "share_dialog",
    "link_copied",
]

CATEGORIES = ["All", "Updates", "Events", "Community"]

PAGE_SIZE = 10


def generate_notices_data() -> dict:
    notices = []

    for index in range(36):
        category = CATEGORIES[1 + index % 3]
        published = date.today() - timedelta(days=index * 3)

        notices.append(
            {
                "id": f"notice_{index}",
                "title": f"{category}: {fake.sentence(nb_words=7)}",
                "category": category,
                "date": published.strftime("%m.%d.%Y"),
                "paragraphs": [
                    fake.paragraph(nb_sentences=4)
                    for _ in range(random.randint(3, 5))
                ],
                "is_new": index < 3,
                "share_url": (
                    f"https://example.invalid/notices/notice-{index}"
                ),
            }
        )

    data = {
        "notices": notices,
        "categories": list(CATEGORIES),
    }
    data.update(generate_footer_data())
    return data


def apply_notices_state(base_data: dict, state: str) -> dict:
    if state not in NOTICE_STATES:
        raise ValueError(f"Unknown notice state: {state}")

    data = deepcopy(base_data)

    category = {
        "updates": "Updates",
        "events": "Events",
    }.get(state, "All")

    query = (
        "Updates"
        if state == "search_results"
        else "unmatched-search"
        if state == "search_empty"
        else ""
    )

    filtered = [
        item
        for item in data["notices"]
        if (category == "All" or item["category"] == category)
        and (
            not query
            or query.casefold() in item["title"].casefold()
        )
    ]

    page_count = max(
        1,
        (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE,
    )
    page_number = 2 if state == "page_two" else 1
    page_number = min(page_number, page_count)

    start = (page_number - 1) * PAGE_SIZE
    visible = filtered[start:start + PAGE_SIZE]

    expanded = (
        visible[0]
        if visible and state in {
            "article_expanded",
            "share_dialog",
            "link_copied",
        }
        else None
    )

    data.update(
        {
            "state": state,
            "popup": state == "share_dialog",
            "active_category": category,
            "query": query,
            "visible_notices": visible,
            "result_count": len(filtered),
            "page_number": page_number,
            "page_count": page_count,
            "expanded": expanded,
            "copied": state == "link_copied",
        }
    )

    return data