from __future__ import annotations

import random
from copy import deepcopy
from pathlib import Path

from social_media.common.media_generator import (
    get_image_files,
    get_random_image,
)


TOPIC_STATES = [
    "article",
    "expanded_summary",
    "find_in_topic",
    "references",
    "graphics",
    "contents_dialog",
    "reader_settings_dialog",
]

TOPIC_SUBJECTS = [
    "Headache",
    "Asthma",
    "Diabetes",
    "Hypertension",
    "Dizziness",
]

SECTION_TITLES = [
    "Introduction",
    "Overview",
    "Clinical presentation",
    "Evaluation",
    "Related considerations",
    "Patient resources",
    "Summary",
]


def generate_topic_data(
    sample_index: int,
    graphics_dir: Path | None = None,
) -> dict:
    subject = random.choice(TOPIC_SUBJECTS)

    sections = []

    for index, heading in enumerate(SECTION_TITLES):
        paragraphs = [
            (
                f"This synthetic reference section presents an overview "
                f"of {subject.lower()} for the topic reader interface. "
                "The content demonstrates article spacing, headings, "
                "and navigation across different screen sizes."
            ),
            (
                "Related resources appear alongside the topic. Readers "
                "can explore sections, save the resource, and adjust "
                "the reading layout using the available controls."
            ),
            (
                "The reference workspace groups background information "
                "and supporting material into clearly separated sections. "
                "This sample paragraph provides additional reading content."
            ),
        ]

        sections.append({
            "id": f"section_{index}",
            "heading": heading,
            "paragraphs": paragraphs[:random.randint(2, 3)],
        })

    image_available = (
        graphics_dir is not None
        and graphics_dir.is_dir()
        and bool(get_image_files(str(graphics_dir)))
    )

    graphics = [
        {
            "id": f"graphic_{index}",
            "title": f"{subject}: reference figure {index + 1}",
            "caption": "Synthetic reference graphic for the topic layout.",
            "image": (
                get_random_image(graphics_dir)
                if image_available else None
            ),
        }
        for index in range(random.randint(3, 5))
    ]

    return {
        "sample_index": sample_index,
        "state": "article",
        "popup_visible": False,
        "popup_kind": None,
        "subject": subject,
        "title": f"{subject}: topic overview",
        "specialty": random.choice([
            "Internal medicine",
            "Family medicine",
            "General reference",
        ]),
        "author": random.choice([
            "Alex Lee, MD",
            "Morgan Patel, MD",
            "Jordan Kim, MD",
        ]),
        "review_label": "Recently reviewed",
        "saved": random.random() < 0.4,
        "active_tab": "article",
        "summary_expanded": False,
        "summary_points": [
            "Browse the overview and related reference sections.",
            "Explore supporting graphics and references.",
            "Save the topic for later reading.",
        ],
        "sections": sections,
        "references": [
            {
                "id": f"reference_{index}",
                "number": index + 1,
                "title": (
                    f"Demonstration reference {index + 1}: "
                    f"{subject.lower()} resource overview"
                ),
                "source": "Synthetic reference collection",
            }
            for index in range(random.randint(8, 12))
        ],
        "graphics": graphics,
        "find_visible": False,
        "find_query": "reference",
        "find_match_count": 0,
        "font_size": 16,
        "font_sizes": [14, 16, 18, 20],
        "line_spacing": "Comfortable",
        "spacing_options": ["Compact", "Comfortable", "Spacious"],
        "show_related": True,
        "related_topics": [
            f"{subject}: patient resources",
            f"{subject}: related topics",
            f"{subject}: reference graphics",
        ],
    }


def apply_topic_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in TOPIC_STATES:
        raise ValueError(f"Unknown topic state: {state!r}")

    data = deepcopy(base_data)

    data.update({
        "state": state,
        "popup_visible": False,
        "popup_kind": None,
        "active_tab": "article",
        "summary_expanded": False,
        "find_visible": False,
    })

    if state == "expanded_summary":
        data["summary_expanded"] = True

    elif state == "find_in_topic":
        data["find_visible"] = True

    elif state in {"references", "graphics"}:
        data["active_tab"] = state

    elif state == "contents_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "contents"

    elif state == "reader_settings_dialog":
        data["popup_visible"] = True
        data["popup_kind"] = "reader_settings"

    # Count only the article paragraphs highlighted by the template.
    query = data["find_query"]

    data["find_match_count"] = sum(
        paragraph.count(query)
        for section in data["sections"]
        for paragraph in section["paragraphs"]
    )

    return data