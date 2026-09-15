from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_design_thumbnail,
    get_random_photo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

PRESENTATION_STATES = [
    "editing",
    "speaker_notes",
    "presenter_view",
    "recording",
    "share_preview",
]


# ==========================================================
# Slide Themes
# ==========================================================

SLIDE_TITLES = [
    "Designing for Growth",
    "The Future of Creativity",
    "Launch Strategy",
    "Brand Evolution",
    "Product Vision",
    "Marketing Playbook",
    "Building Better Experiences",
]


SLIDE_SUBTITLES = [
    "A practical framework for the next stage.",
    "Ideas, insights, and opportunities.",
    "Turning strategy into measurable outcomes.",
    "Building clarity across every touchpoint.",
    "A simple roadmap for meaningful growth.",
]


# ==========================================================
# Slides
# ==========================================================

def generate_slides() -> list[dict]:

    count = random.randint(
        5,
        9,
    )

    selected_index = random.randrange(
        count
    )

    slides = []

    for index in range(count):

        slides.append(
            {
                "number":
                    index + 1,

                "title":
                    random.choice(
                        SLIDE_TITLES
                    ),

                "subtitle":
                    random.choice(
                        SLIDE_SUBTITLES
                    ),

                "image":
                    (
                        get_random_design_thumbnail()
                        or get_random_photo()
                    ),

                "selected":
                    index == selected_index,

                "hidden":
                    random.random() < 0.08,
            }
        )

    return slides


# ==========================================================
# Comments
# ==========================================================

def generate_slide_comments() -> list[dict]:

    return [
        {
            "name":
                fake.name(),

            "avatar":
                get_random_avatar(),

            "text":
                random.choice(
                    [
                        "Can we simplify this slide?",
                        "The visual works well here.",
                        "Maybe add one supporting statistic.",
                    ]
                ),

            "time":
                random.choice(
                    [
                        "2m",
                        "15m",
                        "1h",
                    ]
                ),
        }
        for _ in range(
            random.randint(
                2,
                4,
            )
        )
    ]


# ==========================================================
# Notes
# ==========================================================

def generate_notes() -> list[str]:

    return [
        random.choice(
            [
                "Introduce the key idea before revealing the visual.",
                "Pause here and explain the customer problem.",
                "Mention the year-over-year growth result.",
                "Keep this section under two minutes.",
                "Transition into the next slide with the launch example.",
            ]
        )
        for _ in range(
            random.randint(
                3,
                5,
            )
        )
    ]


# ==========================================================
# Recording
# ==========================================================

def generate_recording() -> dict:

    return {
        "elapsed":
            random.choice(
                [
                    "00:18",
                    "00:42",
                    "01:15",
                    "02:08",
                ]
            ),

        "mic_on":
            random.random() > 0.15,

        "camera_on":
            random.random() > 0.30,

        "paused":
            random.random() < 0.20,
    }


# ==========================================================
# Main
# ==========================================================

def generate_presentation_data(
    forced_state: str | None = None,
) -> dict:

    if forced_state is not None:

        if forced_state not in PRESENTATION_STATES:

            raise ValueError(
                f"Unknown presentation state: "
                f"{forced_state}"
            )

        state = forced_state

    else:

        state = random.choice(
            PRESENTATION_STATES
        )

    slides = generate_slides()

    selected_slide = next(
        (
            slide
            for slide in slides
            if slide["selected"]
        ),
        slides[0],
    )

    return {

        "state":
            state,


        "document": {

            "name":
                random.choice(
                    [
                        "Product Strategy",
                        "Brand Presentation",
                        "Creative Review",
                        "Quarterly Update",
                        "Launch Plan",
                    ]
                ),

            "owner":
                fake.name(),

            "avatar":
                get_random_avatar(),
        },


        "slides":
            slides,


        "selected_slide":
            selected_slide,


        "notes":
            generate_notes(),


        "comments":
            generate_slide_comments(),


        "recording":
            generate_recording(),


        "presenter": {

            "current":
                selected_slide["number"],

            "total":
                len(slides),

            "next_slide":
                slides[
                    min(
                        selected_slide["number"],
                        len(slides) - 1,
                    )
                ],

            "timer":
                random.choice(
                    [
                        "03:12",
                        "08:43",
                        "12:04",
                    ]
                ),
        },


        "share": {

            "title":
                "Share presentation",

            "link_access":
                random.choice(
                    [
                        "Anyone with the link",
                        "Only people added",
                        "Team members",
                    ]
                ),

            "permission":
                random.choice(
                    [
                        "Can view",
                        "Can comment",
                    ]
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_presentation_data()
    )