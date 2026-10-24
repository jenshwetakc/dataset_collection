from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from social_media.tinypal.generators.home_generator import optional_image


LEARN_STATES = [
    "discover",
    "topic_filtered",
    "saved_articles",
    "empty_saved",
    "article_reader",
    "topic_preferences",
]


def generate_learn_data(
    sample_index: int,
    articles_dir: Path,
) -> dict:
    topics = [
        {"id": "all", "label": "All topics", "icon": "apps"},
        {"id": "play", "label": "Play", "icon": "toys"},
        {"id": "routines", "label": "Routines", "icon": "schedule"},
        {"id": "family", "label": "Family", "icon": "group"},
        {"id": "stories", "label": "Stories", "icon": "menu_book"},
    ]

    article_specs = [
        ("A basket of everyday play", "play"),
        ("Making space for quiet moments", "routines"),
        ("A family walk with little discoveries", "family"),
        ("Turning story time into together time", "stories"),
        ("Simple games with colors and shapes", "play"),
        ("Preparing for a calm evening", "routines"),
        ("Sharing small jobs as a family", "family"),
        ("Creating a cozy reading corner", "stories"),
    ]

    paragraphs = [
        (
            "Everyday moments can become opportunities for connection. "
            "Choose a comfortable space, put distractions aside, and "
            "follow your child’s interests."
        ),
        (
            "Keep the activity simple. A familiar book, a few toys, or "
            "a short walk can provide plenty to explore together."
        ),
        (
            "Leave room for pauses and changes of direction. Some days "
            "will be busy, while others will feel quieter."
        ),
        (
            "You can save ideas you enjoy and return to them when they "
            "fit your family’s day."
        ),
    ]

    articles = []

    for index, (title, topic_id) in enumerate(article_specs):
        topic = next(t for t in topics if t["id"] == topic_id)

        articles.append({
            "id": f"learn_article_{index}",
            "title": title,
            "topic_id": topic_id,
            "topic_label": topic["label"],
            "icon": topic["icon"],
            "image": optional_image(articles_dir),
            "duration": random.randint(3, 8),
            "saved": index in {0, 3, 5},
            "author": random.choice([
                "Tinypal Editorial",
                "Family Stories Team",
                "Everyday Play Team",
            ]),
            "intro": (
                "A few simple ideas to explore at your own pace "
                "and adapt to your family."
            ),
            "paragraphs": list(paragraphs),
        })

    return {
        "sample_index": sample_index,
        "state": "discover",
        "popup_visible": False,
        "popup_kind": None,
        "collection": "discover",
        "selected_topic": "all",
        "query": "",
        "topics": topics,
        "preferred_topics": ["play", "routines"],
        "articles": articles,
        "visible_articles": [],
        "featured": deepcopy(articles[0]),
        "selected_article": deepcopy(articles[0]),
        "result_count": 0,
        "saved_count": sum(article["saved"] for article in articles),
        "navigation": [
            {"label": "Today", "icon": "home", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": True},
            {"label": "Family", "icon": "group", "active": False},
        ],
    }


def apply_learn_state(base_data: dict, state: str) -> dict:
    if state not in LEARN_STATES:
        raise ValueError(f"Unknown learn state: {state}")

    data = deepcopy(base_data)
    data["state"] = state

    data["popup_visible"] = state in {
        "article_reader",
        "topic_preferences",
    }

    data["popup_kind"] = state if data["popup_visible"] else None

    if state == "topic_filtered":
        data["selected_topic"] = "play"

    elif state in {"saved_articles", "empty_saved"}:
        data["collection"] = "saved"

    if state == "empty_saved":
        for article in data["articles"]:
            article["saved"] = False

    data["saved_count"] = sum(
        article["saved"] for article in data["articles"]
    )

    visible = [
        article
        for article in data["articles"]
        if (
            data["selected_topic"] == "all"
            or article["topic_id"] == data["selected_topic"]
        )
        and (
            data["collection"] != "saved"
            or article["saved"]
        )
    ]

    data["visible_articles"] = visible
    data["result_count"] = len(visible)

    data["show_featured"] = (
        data["collection"] == "discover"
        and data["selected_topic"] == "all"
    )

    return data