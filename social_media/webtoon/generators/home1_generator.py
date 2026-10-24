from __future__ import annotations

import importlib
import random
from pathlib import Path
from faker import Faker

FAKE = Faker()
STATES = ["discover", "daily", "genres", "ranking", "canvas", "search_results", "search_empty", "login_dialog", "filter_sheet"]
GENRES = ["Fantasy", "Romance", "Action", "Comedy", "Drama", "Thriller", "Slice of Life", "Sci-Fi"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def generate_home_page(package_root: str = "social_media") -> dict:
    """Generate once per sample; reuse content for every state and viewport."""
    media = importlib.import_module(f"{package_root}.common.media_generator")
    root = Path(media.ASSETS_ROOT)
    preferred = root / "webtoon" / "covers"
    image_root = preferred if media.get_image_files(str(preferred)) else root
    available = bool(media.get_image_files(str(image_root)))
    series = []
    for index in range(36):
        genre = GENRES[index % len(GENRES)]
        series.append({
            "id": index, "title": FAKE.sentence(nb_words=random.randint(2, 5)).rstrip("."),
            "creator": FAKE.name(), "genre": genre,
            "description": FAKE.paragraph(nb_sentences=3),
            "cover": media.get_random_image(image_root) if available else None,
            "rating": round(random.uniform(8.1, 9.99), 2),
            "subscribers": f"{random.uniform(0.2, 8.5):.1f}M",
            "day": DAYS[index % 7], "episodes": random.randint(12, 240),
            "badge": random.choice(["NEW", "UP", "", "", ""]),
            "canvas": index % 3 == 0,
        })
    selected = random.choice(series)
    return {"series": series, "featured": selected, "genres": GENRES,
            "days": DAYS, "selected_day": random.choice(DAYS),
            "selected_genre": random.choice(GENRES), "query": selected["title"],
            "username": FAKE.user_name(), "state": "discover", "popup": False}


def make_state(content: dict, state: str) -> dict:
    if state not in STATES:
        raise ValueError(f"Unknown WEBTOON state: {state}")
    data = dict(content)
    data.update(state=state, popup=state in {"login_dialog", "filter_sheet"})
    series = content["series"]
    if state == "daily":
        visible = [s for s in series if s["day"] == content["selected_day"]]
    elif state == "genres":
        visible = [s for s in series if s["genre"] == content["selected_genre"]]
    elif state == "ranking":
        visible = sorted(series, key=lambda s: s["rating"], reverse=True)[:20]
    elif state == "canvas":
        visible = [s for s in series if s["canvas"]]
    elif state == "search_results":
        visible = [s for s in series if content["query"].casefold() in s["title"].casefold()]
    elif state == "search_empty":
        visible = []
        data["query"] = "No matching comic 7391"
    else:
        visible = series[:24]
    data["visible_series"] = visible
    data["heading"] = {"discover": "Discover your next story", "daily": "Daily releases",
        "genres": content["selected_genre"], "ranking": "Top series", "canvas": "CANVAS · Independent creators",
        "search_results": "Search results", "search_empty": "Search results"}.get(state, "Discover your next story")
    return data
