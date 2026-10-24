from __future__ import annotations

import copy
import random
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


NEWS_STATES = (
    "overview",
    "category_filtered",
    "search_results",
    "saved_stories",
    "article_expanded",
    "share_dialog",
    "notification_settings",
)


CATEGORIES = (
    "All",
    "Forecast",
    "Severe Weather",
    "Climate",
    "Science",
    "Travel",
)


STORY_LIBRARY = (
    (
        "Rain moves across the region",
        "Forecast",
        "rainy",
        "A changing weather pattern brings scattered showers.",
    ),
    (
        "Strong winds arrive ahead of a front",
        "Severe Weather",
        "air",
        "Forecasters track a developing band of gusty conditions.",
    ),
    (
        "Why autumn skies look different",
        "Science",
        "partly_cloudy_day",
        "Cloud height and sunlight shape the changing seasonal sky.",
    ),
    (
        "A closer look at urban temperatures",
        "Climate",
        "thermostat",
        "A visual explanation of temperature differences across cities.",
    ),
    (
        "Weekend outlook for popular destinations",
        "Travel",
        "flight",
        "Compare synthetic forecasts before exploring the weekend.",
    ),
    (
        "Storm clouds build along the coast",
        "Severe Weather",
        "thunderstorm",
        "A coastal weather system becomes the focus of the forecast.",
    ),
    (
        "Clear skies return after morning clouds",
        "Forecast",
        "sunny",
        "The afternoon outlook features brighter conditions.",
    ),
    (
        "How radar reveals moving rain",
        "Science",
        "radar",
        "Explore the patterns behind a familiar weather display.",
    ),
    (
        "Changing seasons in a mountain landscape",
        "Climate",
        "landscape",
        "Seasonal conditions create a changing mountain scene.",
    ),
    (
        "A rainy day guide for city breaks",
        "Travel",
        "umbrella",
        "A weather-focused look at a flexible travel itinerary.",
    ),
    (
        "A new front changes the evening outlook",
        "Forecast",
        "cloud",
        "An approaching front reshapes the synthetic evening forecast.",
    ),
    (
        "Tracking a developing storm system",
        "Severe Weather",
        "storm",
        "Follow the stages of a simulated developing weather system.",
    ),
)


def generate_news_data(
    *,
    sample_index: int,
    images_dir: Path | None = None,
) -> dict:
    images_available = bool(
        images_dir is not None
        and images_dir.is_dir()
        and get_image_files(str(images_dir))
    )

    stories = []

    for index, (
        title,
        category,
        icon,
        summary,
    ) in enumerate(STORY_LIBRARY):
        stories.append(
            {
                "id": f"story_{index}",
                "title": title,
                "category": category,
                "icon": icon,
                "summary": summary,
                "image": (
                    get_random_image(images_dir)
                    if images_available
                    else None
                ),
                "author": random.choice(
                    [
                        "Weather Desk",
                        "Forecast Team",
                        "Science Desk",
                        "Travel Editor",
                    ]
                ),
                "published": (
                    f"{random.randint(1, 55)} minutes ago"
                ),
                "read_minutes": random.randint(3, 8),
                "saved": index in {1, 3, 7},
                "body": [
                    (
                        "This synthetic article describes a changing "
                        "weather pattern using illustrative conditions "
                        "and a fictional editorial report."
                    ),
                    (
                        "The forecast view combines cloud cover, "
                        "temperature, and precipitation information "
                        "to create a varied weather-news layout."
                    ),
                    (
                        "Conditions shown here are generated for a "
                        "UI dataset. The article provides sample "
                        "content for an expanded reading state."
                    ),
                ],
            }
        )

    random.shuffle(stories)

    return {
        "sample_index": sample_index,
        "state": "overview",
        "popup_visible": False,
        "dialog_type": None,
        "categories": list(CATEGORIES),
        "active_category": "All",
        "query": "",
        "stories": stories,
        "featured": stories[0],
        "trending": stories[1:5],
        "visible_stories": stories[1:],
        "expanded_story_id": None,
        "share_story": None,
        "share_url": "",
        "notifications": {
            "breaking": True,
            "daily": False,
            "topics": [
                "Forecast",
                "Severe Weather",
            ],
        },
        "local_weather": {
            "city": "Seoul",
            "temperature": random.randint(18, 25),
            "condition": "Partly cloudy",
            "icon": "partly_cloudy_day",
            "high": 26,
            "low": 16,
        },
    }


def apply_news_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in NEWS_STATES:
        raise ValueError(
            f"Unknown news state: {state}"
        )

    data = copy.deepcopy(base_data)
    data["state"] = state

    if state == "category_filtered":
        data["active_category"] = "Severe Weather"

        matching = [
            story
            for story in data["stories"]
            if story["category"] == "Severe Weather"
        ]

        data["featured"] = matching[0]
        data["visible_stories"] = matching[1:]

    elif state == "search_results":
        data["query"] = "rain"

        matching = [
            story
            for story in data["stories"]
            if "rain" in (
                story["title"] + " " + story["summary"]
            ).casefold()
        ]

        data["featured"] = None
        data["visible_stories"] = matching

    elif state == "saved_stories":
        data["featured"] = None
        data["visible_stories"] = [
            story
            for story in data["stories"]
            if story["saved"]
        ]

    elif state == "article_expanded":
        data["expanded_story_id"] = (
            data["featured"]["id"]
        )

    elif state == "share_dialog":
        story = data["featured"]

        data["popup_visible"] = True
        data["dialog_type"] = "share"
        data["share_story"] = story
        data["share_url"] = (
            f"https://weather.example/news/{story['id']}"
        )

    elif state == "notification_settings":
        data["popup_visible"] = True
        data["dialog_type"] = "notifications"

    data["visible_count"] = len(
        data["visible_stories"]
    )

    return data