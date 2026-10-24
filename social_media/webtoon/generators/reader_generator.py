from __future__ import annotations

import base64
import mimetypes
import random

from functools import lru_cache
from pathlib import Path

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)


# ==========================================================
# Configuration
# ==========================================================

fake = Faker()

# Change this to your existing logo folder if it is separate.
# No specific logo filenames are required.
LOGOS_ROOT = ASSETS_ROOT / "logos"

PANELS_ROOT = ASSETS_ROOT / "webtoon"
COVERS_ROOT = ASSETS_ROOT / "webtoon"

SUPPORTED_LOGO_EXTENSIONS = {
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

READER_STATES = [
    "reading",
    "episode_list",
    "liked",
    "subscribed",
    "share_copied",
    "comments_top",
    "comments_recent",
    "comments_empty",
    "reply_expanded",
    "login_dialog",
]


# ==========================================================
# Logo Assets
# ==========================================================

@lru_cache(maxsize=1)
def get_logo_files() -> tuple[Path, ...]:
    root = Path(LOGOS_ROOT)

    if not root.is_dir():
        raise FileNotFoundError(
            f"Logo directory does not exist: {root}"
        )

    files = tuple(
        sorted(
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in SUPPORTED_LOGO_EXTENSIONS
        )
    )

    if not files:
        raise FileNotFoundError(
            f"No supported logo images found in {root}. "
            "Supported formats: SVG, PNG, JPG, JPEG, WEBP."
        )

    return files


@lru_cache(maxsize=128)
def logo_to_data_uri(path: Path) -> str:
    if path.suffix.lower() == ".svg":
        mime_type = "image/svg+xml"
    else:
        mime_type = mimetypes.guess_type(path.name)[0]

    if mime_type is None:
        raise ValueError(
            f"Could not determine image type: {path}"
        )

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return f"data:{mime_type};base64,{encoded}"


def choose_logo_assets(count: int) -> list[str]:
    if count < 1:
        raise ValueError("Logo count must be positive.")

    files = get_logo_files()

    # Select distinct files when possible.
    selected = random.sample(
        files,
        min(count, len(files)),
    )

    # Allow repetition when the directory has too few assets.
    while len(selected) < count:
        selected.append(random.choice(files))

    return [
        logo_to_data_uri(path)
        for path in selected
    ]


def generate_footer_data() -> dict:
    """
    Select logos once per sample.

    Preserve the keys expected by reader.html and footer.html.
    These are synthetic replacements, not verified brand assets.
    """
    logos = choose_logo_assets(7)

    return {
        "branding": {
            "webtoon_logo": logos[0],
            "google_play": logos[1],
            "app_store": logos[2],
        },
        "footer_social_links": [
            {
                "name": f"Social link {index + 1}",
                "url": "#",
                "logo": logos[index + 3],
            }
            for index in range(4)
        ],
    }


# ==========================================================
# Page Media
# ==========================================================

def load_optional_image(directory: Path) -> str | None:
    if not directory.is_dir():
        return None

    if not get_image_files(str(directory)):
        return None

    return get_random_image(directory)


def generate_panels() -> list[str]:
    if not PANELS_ROOT.is_dir():
        raise FileNotFoundError(
            f"Comic panel directory does not exist: {PANELS_ROOT}"
        )

    if not get_image_files(str(PANELS_ROOT)):
        raise FileNotFoundError(
            f"No comic panel images found in {PANELS_ROOT}"
        )

    panels = []

    for _ in range(random.randint(5, 8)):
        image = get_random_image(PANELS_ROOT)

        if image is None:
            raise RuntimeError(
                f"Could not load a comic panel from {PANELS_ROOT}"
            )

        panels.append(image)

    return panels


# ==========================================================
# Synthetic Content
# ==========================================================

def generate_comments() -> list[dict]:
    return [
        {
            "id": index,
            "author": fake.user_name(),
            "text": fake.paragraph(nb_sentences=2),
            "likes": random.randint(10, 2500),
            "minutes_ago": random.randint(1, 240),
            "replies": [
                {
                    "author": fake.user_name(),
                    "text": fake.sentence(nb_words=12),
                    "likes": random.randint(0, 120),
                }
                for _ in range(random.randint(1, 3))
            ],
        }
        for index in range(6)
    ]


def generate_episodes() -> list[dict]:
    return [
        {
            "number": number,
            "title": fake.sentence(nb_words=4).rstrip("."),
        }
        for number in range(1, 21)
    ]


def generate_recommendations() -> list[dict]:
    return [
        {
            "title": fake.sentence(nb_words=4).rstrip("."),
            "creator": fake.name(),
            "cover": load_optional_image(COVERS_ROOT),
        }
        for _ in range(5)
    ]


# ==========================================================
# Reader Data
# ==========================================================

def generate_reader_data() -> dict:
    episode_number = random.randint(2, 18)
    episodes = generate_episodes()

    current_episode = episodes[episode_number - 1]

    data = {
        "title": fake.sentence(nb_words=4).rstrip("."),
        "creator": fake.name(),
        "episode_number": episode_number,
        "episode_title": current_episode["title"],
        "schedule": random.choice(
            [
                "UP EVERY MONDAY",
                "UP EVERY TUESDAY",
                "UP EVERY WEDNESDAY",
                "UP EVERY THURSDAY",
                "UP EVERY FRIDAY",
                "UP EVERY SATURDAY",
                "UP EVERY SUNDAY",
            ]
        ),
        "panels": generate_panels(),
        "likes": random.randint(1000, 60000),
        "comments": generate_comments(),
        "episodes": episodes,
        "recommendations": generate_recommendations(),
    }

    # Generate once here, not inside apply_reader_state().
    data.update(generate_footer_data())

    return data


# ==========================================================
# Reader States
# ==========================================================

def apply_reader_state(content: dict, state: str) -> dict:
    if state not in READER_STATES:
        raise ValueError(
            f"Unknown reader state: {state}. "
            f"Supported states: {READER_STATES}"
        )

    # Templates only read the nested content.
    # Reuse the same artwork and logos across states.
    data = dict(content)
    comments = list(content["comments"])

    if state == "comments_recent":
        comments.sort(
            key=lambda comment: comment["minutes_ago"]
        )
    else:
        comments.sort(
            key=lambda comment: comment["likes"],
            reverse=True,
        )

    if state == "comments_empty":
        comments = []

    expanded_comment_id = None

    if state == "reply_expanded" and comments:
        expanded_comment_id = comments[0]["id"]

    data.update(
        {
            "state": state,
            "popup": state == "login_dialog",
            "liked": state == "liked",
            "subscribed": state == "subscribed",
            "episode_list_open": state == "episode_list",
            "share_copied": state == "share_copied",
            "comment_sort": (
                "Newest"
                if state == "comments_recent"
                else "Top"
            ),
            "visible_comments": comments,
            "expanded_comment_id": expanded_comment_id,
            "display_likes": (
                content["likes"] + int(state == "liked")
            ),
        }
    )

    return data