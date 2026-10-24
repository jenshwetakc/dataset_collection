from __future__ import annotations

import random

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_image_files,
    get_random_image,
)
from social_media.webtoon.generators.reader_generator import (
    generate_footer_data,
)


fake = Faker()

CREATOR_STATES = [
    "overview",
    "following",
    "series_tab",
    "posts_empty",
    "post_liked",
    "poll_voted",
    "profile_menu",
    "report_dialog",
    "share_copied",
]

REPORT_REASONS = [
    "Spam or misleading content",
    "Harassment or abusive content",
    "Inappropriate content",
    "Impersonation",
    "Other",
]


def load_media(directory: str, fallback: str | None = None) -> str:
    candidates = [directory]

    if fallback:
        candidates.append(fallback)

    for name in candidates:
        path = ASSETS_ROOT / "webtoon"

        if path.is_dir() and get_image_files(str(path)):
            image = get_random_image(path)

            if image:
                return image

    raise FileNotFoundError(
        "Add images to one of these directories: "
        + ", ".join(
            str(ASSETS_ROOT / "webtoon")
            for name in candidates
        )
    )


def generate_creator_data() -> dict:
    options = [
        "Character sketches",
        "Behind-the-scenes artwork",
        "World-building notes",
    ]

    votes = [random.randint(40, 300) for _ in options]

    posts = [
        {
            "id": index,
            "text": fake.paragraph(nb_sentences=3),
            "image": (
                load_media("posts", fallback="covers")
                if index in {0, 2}
                else None
            ),
            "likes": random.randint(30, 3000),
            "comments": random.randint(2, 180),
            "days_ago": index * 3 + 1,
        }
        for index in range(4)
    ]

    data = {
        "name": fake.name(),
        "handle": fake.user_name(),
        "bio": fake.paragraph(nb_sentences=2),
        "avatar": load_media("avatars", fallback="covers"),
        "followers": random.randint(1000, 250000),
        "series": [
            {
                "title": fake.sentence(nb_words=4).rstrip("."),
                "genre": random.choice(
                    ["Fantasy", "Romance", "Drama", "Comedy"]
                ),
                "cover": load_media("covers"),
                "subscribers": random.randint(1000, 200000),
            }
            for _ in range(3)
        ],
        "posts": posts,
        "poll": {
            "question": "What would you like to see next?",
            "options": options,
            "votes": votes,
        },
        "report_reasons": REPORT_REASONS.copy(),
    }

    data.update(generate_footer_data())

    return data


def apply_creator_state(content: dict, state: str) -> dict:
    if state not in CREATOR_STATES:
        raise ValueError(f"Unknown creator state: {state}")

    data = dict(content)

    posts = [
        {
            **post,
            "liked": state == "post_liked" and index == 0,
            "display_likes": (
                post["likes"]
                + int(state == "post_liked" and index == 0)
            ),
        }
        for index, post in enumerate(content["posts"])
    ]

    votes = list(content["poll"]["votes"])
    selected_option = 1 if state == "poll_voted" else None

    if selected_option is not None:
        votes[selected_option] += 1

    total_votes = sum(votes)

    data.update(
        {
            "state": state,
            "popup": state == "report_dialog",
            "following": state == "following",
            "display_followers": (
                content["followers"] + int(state == "following")
            ),
            "active_tab": "Series" if state == "series_tab" else "Posts",
            "visible_posts": [] if state == "posts_empty" else posts,
            "menu_open": state == "profile_menu",
            "share_copied": state == "share_copied",
            "selected_report_reason": 0,
            "poll_voted": state == "poll_voted",
            "selected_poll_option": selected_option,
            "poll_options": [
                {
                    "label": label,
                    "votes": votes[index],
                    "percentage": round(
                        votes[index] / total_votes * 100
                    ),
                }
                for index, label in enumerate(content["poll"]["options"])
            ],
            "total_votes": total_votes,
        }
    )

    return data